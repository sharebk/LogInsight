from core.preprocessing import preprocess_logs
from core.fols import generate_fols
from core.knowledge_injection import generate_explanations, validate_explanations, write_dataset_to_file
from core.fine_tuning import fine_tune_model

"""
主程序入口，整合所有模块功能。
"""

def main():
    """
    主程序入口，整合所有模块功能。
    """
    # 1. 预处理日志
    with open("data/raw_logs/rfc_logs.log", "r") as file:
        raw_logs = file.read()
    structured_logs = preprocess_logs(raw_logs)

    # 2. 生成故障日志摘要
    core_logs = generate_fols(structured_logs)

    # 3. 知识注入
    explanations = generate_explanations(core_logs)
    # validated_explanations = validate_explanations(explanations, [True] * len(explanations))  # 模拟专家反馈
    file_path = "./data/knowledge_base/log_diagnosis_dataset.jsonl"
    write_dataset_to_file(explanations, file_path)

    # 4. 模型微调
    # dataset_path = "./data/knowledge_base/log_diagnosis_dataset.jsonl"
    # model = fine_tune_model(dataset_path=dataset_path)

    print("LogInsight pipeline completed!")


if __name__ == "__main__":
    main()