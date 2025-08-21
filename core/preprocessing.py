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
    pattern = r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}) (\w+) (\S+) ([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}) (\d+\.\d+\.\d+\.\d+) (\w+) (\S+) (\d+) (\d+)ms(?: error=\"(.*)\")?$'
    structured_logs = []
    for log in raw_logs.split('\n'):
        match = re.match(pattern, log.strip())
        if match:
            structured_logs.append({
                'timestamp': match.group(1),
                'level': match.group(2),
                'service': match.group(3),
                'request_id': match.group(4),
                'client_ip': match.group(5),
                'method': match.group(6),
                'path': match.group(7),
                'status_code': int(match.group(8)),
                'response_time': int(match.group(9)),
                'message': match.group(10) if match.group(10) else None
            })
    return structured_logs

if __name__ == "__main__":
    # 示例用法
    sample_logs = """
    2025-08-21T01:55:07.285420 INFO notification-service 3ad7e0c1-038b-42ac-b56d-75e82b5cdbba 7.205.108.198 PUT /api/v1/payments 200 4695ms
    2025-08-20T17:41:50.285420 INFO order-service 85ea5266-5931-419a-9930-d94caf4ef747 237.167.107.80 PUT /api/v1/orders 200 4714ms
    2025-08-20T22:52:59.285420 ERROR inventory-service 22a731c6-9e01-4a14-8853-21420492a238 196.179.206.45 GET /api/v1/users 400 1155ms error="Invalid request payload"
    2025-08-21T11:15:57.285420 INFO auth-service a1f7ce28-9d08-4815-88d5-9f65ab80ecf3 132.63.155.142 POST /api/v1/products 500 4668ms
    2025-08-20T18:48:49.285420 INFO order-service 60d2373f-ab6d-4002-97c1-2fbbc2621a38 97.40.170.91 POST /api/v1/orders 400 891ms
    """
    # processed_logs = preprocess_logs(sample_logs)
    # pprint(processed_logs)
    # 示例2
    raw_logs = open("../data/raw_logs/rfc_logs.log", "r").read()
    processed_logs = preprocess_logs(raw_logs)
    pprint(processed_logs)