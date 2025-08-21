# LogInsight 基于大语言模型的准确而可解释的日志故障诊断方法
> - 项目思路来源: https://mp.weixin.qq.com/s/IfdhN2vnNXvYWnZZfoe-KA
> - 文章内容: [reference.md](reference.md)

> - 关键依赖：Python 3.8+, scikit-learn 1.2+, PyTorch 2.0+, HuggingFace Transformers 4.28+ 
> - 硬件建议：预处理阶段需16GB内存，模型微调需A100 40GB GPU

# 简介
**LogInsight - 智能化日志故障诊断系统**
* 基于大语言模型的准确而可解释的日志故障诊断方法
* 核心架构：预处理 → 日志摘要 → 知识注入 → 模型微调

## LogInsight的整体框架包括四个主要步骤：
| 步骤 | 名称             |描述|
|----|----------------|-|
| 1  | 日志预处理模块        |利用正则表达式对原始日志进行预处理，提取关键内容形成结构化日志序列。|
| 2  | 故障日志摘要（FOLS）模块 |通过聚类和TF-IDF排序，聚合和筛选故障相关的核心日志信息，减少冗余。|
| 3  | 知识注入模块         |结合GPT-4自动生成解释并由专家人工校验，构建高质量的指令数据集。|
| 4  | 模型微调模块         |利用LoRA技术对开源中等规模LLM进行监督微调，使模型具备领域特定知识和解释能力。|

## 项目结构说明
```shell
LogInsight/
├── core/                         # 核心实现
│   ├── preprocessing.py          # 1. 日志解析
│   ├── fols.py                   # 2. 摘要算法
│   ├── knowledge_injection.py    # 3. 知识构建
│   └── fine_tuning.py            # 4. 模型微调
├── data/
│   ├── raw_logs/                 # 原始日志
│   └── knowledge_base/           # 校验后知识库
├── config.py                     # 正则模式/API密钥等配置
├── train.py                      # 训练入口
└── main.py                       # 诊断服务入口
```

## 关键技术实现要点
1. 正则预处理优化
 - 动态模式匹配：支持多格式日志模板
 - 噪声过滤：移除IP、时间戳等干扰信息
2. FOLS摘要算法
 - 自适应聚类：基于日志密度动态调整参数
 - 冗余控制：TF-IDF权重+位置加权
3. 知识注入流程
graph TD
    A[原始摘要] --> B(GPT-4生成解释)
    B --> C{专家校验}
    C -->|通过| D[知识库]
    C -->|拒绝| E[标注修正]
    E --> B
4. 高效微调方案
 - LoRA参数配置：聚焦注意力机制层
 - 混合精度训练：减少显存消耗
 - 灾难遗忘防护：Layer-wise学习率衰减


## 使用方法
```shell
python main.py


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
    
```
## 部署建议
日志处理流水线：
```shell
cd core
python preprocessing.py --input syslog.txt --output parsed.json
python fols.py --input parsed.json --ratio 0.3
```

## 二次开发
```shell
# 已存在项目
uv sync
```
```shell
# 创建或初始化项目时
uv venv .venv --python 3.10   # 指定python版本
source .venv/bin/activate
uv init
uv add scikit-learn
```

##
```shell
# 基于RFC模板生成1万行日志（RFC标准的日志格式）
python utils/log_generator.py
```