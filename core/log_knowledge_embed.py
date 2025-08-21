import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

"""
3.1 日志背景信息检索：结合知识库获取日志对应的影响范围
"""
class LogKnowledgeEmbed:
    def __init__(self, jsonl_file_path):
        self.jsonl_file_path = jsonl_file_path
        self.vectorizer = TfidfVectorizer()
        self.log_data = []
        self.vectors = None

    def load_and_process_logs(self):
        """
        读取 JSONL 文件并提取 logMessage 和 description 字段
        """
        with open(self.jsonl_file_path, 'r') as file:
            for line in file:
                log_entry = json.loads(line)
                self.log_data.append({
                    'message': log_entry.get('message', ''),
                    'description': json.dumps(log_entry, ensure_ascii=False)
                })

        # 将 logMessage 转换为向量
        log_messages = [entry['message'] for entry in self.log_data]
        self.vectors = self.vectorizer.fit_transform(log_messages)

    def save_vectors_to_file(self, output_file_path):
        """
        将向量和对应的 description 存储到文件
        """
        if self.vectors is None:
            raise ValueError("Vectors not generated. Call load_and_process_logs() first.")

        with open(output_file_path, 'w') as file:
            for idx, entry in enumerate(self.log_data):
                vector_str = ' '.join(map(str, self.vectors[idx].toarray().flatten()))
                file.write(f"{vector_str}|{entry['description']}\n")

    def search_description_by_vector(self, query_vector, top_k=1):
        """
        通过向量检索对应的 description
        """
        if self.vectors is None:
            raise ValueError("Vectors not generated. Call load_and_process_logs() first.")

        query_vector = self.vectorizer.transform([query_vector])
        similarities = cosine_similarity(query_vector, self.vectors)
        top_indices = np.argsort(similarities[0])[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append(self.log_data[idx]['description'])

        return results


# 示例用法
if __name__ == "__main__":
    log_embed = LogKnowledgeEmbed("../data/knowledge_base/log_knowledge.jsonl")
    log_embed.load_and_process_logs()
    log_embed.save_vectors_to_file("../data/knowledge_base/log_knowledge_vectors.data")

    # # 示例检索
    query = "The settlement file could not be generated due to format"
    descriptions = log_embed.search_description_by_vector(query)
    print(f"Descriptions for query '{query}': {descriptions}")