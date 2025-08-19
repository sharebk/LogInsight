from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
import torch

"""
4. 模型微调模块，利用LoRA技术对开源LLM进行监督微调。
"""

def fine_tune_model(dataset_path, base_model_name="gpt2"):
    """
    使用LoRA技术对开源LLM进行监督微调。
    :param dataset_path: 指令数据集路径
    :param base_model_name: 基础模型名称
    :return: 微调后的模型
    """
    # 加载基础模型和分词器
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    model = AutoModelForCausalLM.from_pretrained(base_model_name)

    # 配置LoRA
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)

    # 配置训练参数
    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=4,
        num_train_epochs=3,
        save_steps=1000,
        logging_steps=100,
        learning_rate=2e-5,
        fp16=True
    )

    # 加载数据集
    from datasets import load_dataset
    train_dataset = load_dataset("json", data_files=dataset_path, split="train")

    # 训练模型
    from transformers import Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer
    )
    trainer.train()

    # 保存微调后的模型
    model.save_pretrained("./fine_tuned_model")

    return model


if __name__ == "__main__":
    # 示例用法
    model = fine_tune_model("../data/knowledge_base/log_diagnosis_dataset.json")
    print("Model fine-tuning completed!")