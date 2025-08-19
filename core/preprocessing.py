import re
from pprint import pprint

"""
1. 日志预处理模块，用于提取关键内容并形成结构化日志序列。
"""
def preprocess_logs(raw_logs):
    """
    预处理原始日志，提取关键内容并形成结构化日志序列。
    :param raw_logs: 原始日志文本
    :return: 结构化日志列表
    """
    # 定义正则表达式模式，匹配日志中的关键信息
    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.*)$'
    structured_logs = []
    for log in raw_logs.split('\n'):
        match = re.match(pattern, log.strip())
        if match:
            structured_logs.append({
                'timestamp': match.group(1),
                'level': match.group(2),
                'message': match.group(3)
            })
    return structured_logs

if __name__ == "__main__":
    # 示例用法
    sample_logs = """
    2025-08-19 10:00:00 INFO Starting service
    2025-08-19 10:00:05 ERROR Failed to connect to database
    2025-08-19 10:00:10 WARNING High memory usage detected
    """
    processed_logs = preprocess_logs(sample_logs)
    pprint(processed_logs)