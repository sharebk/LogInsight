from pprint import pprint

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

"""
2. 故障日志摘要模块，通过聚类和TF-IDF排序筛选核心日志信息。
"""

def generate_fols(structured_logs):
    """
    生成面向故障的日志摘要（FOLS），通过聚类和TF-IDF排序筛选核心日志信息。
    :param structured_logs: 结构化日志列表
    :return: 故障相关的核心日志信息
    """
    # 提取日志消息
    log_messages = [log['message'] for log in structured_logs if log['message']]

    # 使用TF-IDF向量化日志消息
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(log_messages)

    # 使用K-Means聚类
    num_clusters = min(3, len(log_messages))  # 聚类数量不超过日志数量
    kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(tfidf_matrix)

    # 获取每个聚类的中心点
    cluster_centers = kmeans.cluster_centers_

    # 计算每条日志与聚类中心的距离
    distances = np.linalg.norm(tfidf_matrix.toarray() - cluster_centers[kmeans.labels_], axis=1)

    # 选择距离最小的日志作为核心日志
    core_logs = []
    for cluster_id in range(num_clusters):
        cluster_indices = np.where(kmeans.labels_ == cluster_id)[0]
        if len(cluster_indices) > 0:
            representative_idx = cluster_indices[np.argmin(distances[cluster_indices])]
            core_logs.append(structured_logs[representative_idx])

    return core_logs


if __name__ == "__main__":
    # 示例用法
    # sample_logs = [
    #     {'timestamp': '2025-08-19 10:00:00', 'level': 'INFO', 'message': 'Starting service'},
    #     {'timestamp': '2025-08-19 10:00:05', 'level': 'ERROR', 'message': 'Failed to connect to database'},
    #     {'timestamp': '2025-08-19 10:00:10', 'level': 'WARNING', 'message': 'High memory usage detected'}
    # ]
    # fols_logs = generate_fols(sample_logs)
    # print(fols_logs)

    ## 示例2:
    from preprocessing import preprocess_logs
    sample_logs = preprocess_logs(open("../data/raw_logs/rfc_logs.log", "r").read())
    fols_logs = generate_fols(sample_logs)
    pprint(fols_logs)
