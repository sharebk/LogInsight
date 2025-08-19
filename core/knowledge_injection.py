from openai import OpenAI

"""
3. 知识注入模块，结合GPT-4生成解释并由专家校验。
"""

client = OpenAI(
    base_url="http://10.2.32.201:8080/v1",
    api_key="bef71d1b-cb00-40b0-974f-4a07a8c0a17c"
)


def generate_explanations(logs):
    """
    使用GPT-4生成日志解释。
    :param logs: 日志列表
    :return: 生成的解释列表
    """
    explanations = []
    for log in logs:
        prompt = f"Explain the following log message: {log['message']}"
        response = client.chat.completions.create(
            model="Qwen2_5-Coder-32B-Instruct",
            messages=[{"role": "user", "content": prompt}]
        )
        explanations.append({
            'log': log,
            'explanation': response.choices[0].message.content
        })
    return explanations


def validate_explanations(explanations, expert_feedback):
    """
    由专家校验生成的解释。
    :param explanations: 生成的解释列表
    :param expert_feedback: 专家反馈
    :return: 校验后的解释列表
    """
    validated_explanations = []
    for idx, explanation in enumerate(explanations):
        if expert_feedback[idx]:
            validated_explanations.append(explanation)
    return validated_explanations


if __name__ == "__main__":
    # 示例用法
    sample_logs = [
        {'timestamp': '2025-08-19 10:00:05', 'level': 'ERROR', 'message': 'Failed to connect to database'}
    ]
    explanations = generate_explanations(sample_logs)
    print(explanations)

    # 模拟专家反馈
    expert_feedback = [True]
    validated = validate_explanations(explanations, expert_feedback)
    print(validated)
