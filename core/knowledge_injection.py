import json

from openai import OpenAI
from tqdm import tqdm
from time import sleep
"""
3. 知识注入模块，结合GPT-4生成解释并由专家校验。
"""

OPENAI_BASE_URL="http://10.2.32.201:8080/v1"
OPENAI_API_KEY="bef71d1b-cb00-40b0-974f-4a07a8c0a17c"
OPENAI_MODEL_NAME="Qwen2_5-Coder-32B-Instruct"

client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY
)


def generate_explanations(logs):
    """
    使用 LLM 生成日志解释。
    :param logs: 日志列表
    :return: 生成的解释列表
    """
    KNOWN_FAULT_PATTERNS = """
    ### 1. 数据库相关故障
    - `Database connection failed`  
    - `Database timeout`  
    - `Query execution failed`  
    - `Deadlock detected`  
    - `Transaction rollback`  
    - `Connection pool exhausted`  
    - `Invalid SQL syntax`  
    - `Database corruption`
    
    ### 2. 网络相关故障
    - `Connection refused`  
    - `Connection timeout`  
    - `DNS resolution failed`  
    - `SSL handshake error`  
    - `Network unreachable`  
    - `High latency detected`  
    - `Packet loss detected`
    
    ### 3. 认证授权故障
    - `Invalid credentials`  
    - `Authentication failed`  
    - `Token expired`  
    - `Permission denied`  
    - `Rate limit exceeded`  
    - `IP blocked`  
    - `Invalid API key`
    
    ### 4. 资源相关故障
    - `Out of memory`  
    - `Disk space exhausted`  
    - `CPU overload`  
    - `File descriptor limit reached`  
    - `Thread pool exhausted`
    
    ### 5. 服务依赖故障
    - `Service unavailable`  
    - `Dependency service timeout`  
    - `Circuit breaker triggered`  
    - `Health check failed`  
    - `Version mismatch`
    
    ### 6. 数据格式/业务逻辑故障
    - `Invalid input format`  
    - `Data validation failed`  
    - `Missing required field`  
    - `Duplicate entry`  
    - `Business rule violation`
    
    ### 7. 文件/IO故障
    - `File not found`  
    - `Permission denied`  
    - `Disk I/O error`  
    - `File system full`  
    - `File write failed`
    
    ### 8. 配置相关故障
    - `Invalid configuration`  
    - `Missing configuration`  
    - `Environment variable not set`  
    - `Certificate expired`
    """
    print("使用大模型生成日志解释")
    explanations = []
    for log in tqdm(logs):
        sleep(0.25)
        # prompt = f"Explain the following log message: {log['message']}"
        prompt = f"""
        你是一位专业的日志故障诊断专家，负责基于大语言模型为给定的日志数据提供准确且可解释的故障诊断建议。
        首先，请仔细阅读以下日志数据：
        <logs>
        {log['message']}
        </logs>
        同时，参考以下已知故障模式：
        <known_fault_patterns>
        {KNOWN_FAULT_PATTERNS}
        </known_fault_patterns>
        在进行故障诊断时，请按照以下步骤操作：
        1. 仔细分析日志数据，识别其中的关键信息和异常点。
        2. 将日志数据与已知故障模式进行对比，找出可能匹配的故障模式。
        3. 考虑日志的上下文和相关信息，判断故障的可能性和严重程度。
        4. 形成初步的故障诊断结果和处理建议。
        5. 再次检查，确保没有遗漏重要细节。
        
        在<思考>标签中详细分析日志数据与已知故障模式的匹配情况，包括关键信息的提取、异常点的发现以及故障可能性的判断。然后在<诊断结果>标签中给出故障诊断结果，使用简洁明了的语言描述故障情况。接着在<解释>标签中详细解释诊断的推理过程，说明为什么得出这样的诊断结果。最后在<建议>标签中给出针对该故障的处理建议，建议应具有可操作性和针对性。
        
        <思考>
        [在此详细分析日志数据与已知故障模式的匹配情况]
        </思考>
        <诊断结果>
        [在此给出故障诊断结果]
        </诊断结果>
        <解释>
        [在此详细解释诊断的推理过程]
        </解释>
        <建议>
        [在此给出故障处理建议]
        </建议>
        请确保你的诊断和建议准确、可解释，并且基于给定的日志数据和已知故障模式。
        """
        response = client.chat.completions.create(
            model=OPENAI_MODEL_NAME,
            messages=[{"role": "system", "content": "用中文回复"}, {"role": "user", "content": prompt}]
        )
        explanations.append({
            'log': log,
            'explanation': response.choices[0].message.content if response else ""
        })
    return explanations


def validate_explanations(explanations, expert_feedback):
    """
    由专家校验生成的解释。
    :param explanations: 生成的解释列表
    :param expert_feedback: 专家反馈
    :return: 校验后的解释列表
    """
    print("专家校验生成的解释")
    # TODO: 待实现专家校验逻辑
    validated_explanations = []
    for idx, explanation in enumerate(explanations):
        if expert_feedback[idx]:
            validated_explanations.append(explanation)
    return validated_explanations

def write_dataset_to_file(explanations, file_path):
    """
    将解释写入文件。
    data/knowledge_base/log_diagnosis_dataset.json
    :param explanations:
    :return:
    """
    with open(file_path, 'w') as f:
        for explanation in explanations:
            data_line = json.dumps({"messages": [{"role": "user", "content": explanation['log']['message']},
                                                 {"role": "assistant", "content": explanation['explanation']}]},
                                   ensure_ascii=False)
            f.write(data_line+"\n")


if __name__ == "__main__":
    # 示例用法
    fols_logs = [
        {'client_ip': '122.44.77.239',
         'level': 'ERROR',
         'message': 'Database connection failed',
         'method': 'POST',
         'path': '/api/v1/products',
         'request_id': '902e3eed-c119-469e-88c1-ca939255f28b',
         'response_time': 286,
         'service': 'notification-service',
         'status_code': 200,
         'timestamp': '2025-08-21T02:09:27.285420'},
    ]
    # 调用 generate_explanations 函数
    explanations = generate_explanations(fols_logs)
    print(explanations)
    file_path = "../data/knowledge_base/log_diagnosis_dataset.jsonl"
    write_dataset_to_file(explanations, file_path)

    # # 示例2
    # from preprocessing import preprocess_logs
    # from fols import generate_fols
    # sample_logs = preprocess_logs(open("../data/raw_logs/rfc_logs.log", "r").read())
    # fols_logs = generate_fols(sample_logs)
    # # 调用 generate_explanations 函数
    # explanations = generate_explanations(fols_logs)
    # print(explanations)
    # file_path = "../data/knowledge_base/log_diagnosis_dataset.jsonl"
    # write_dataset_to_file(explanations, file_path)

    ## 模拟专家反馈
    # expert_feedback = [True, True, True]
    # validated = validate_explanations(explanations, expert_feedback)
    # print(validated)
