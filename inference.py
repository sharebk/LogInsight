# inference.py
"""
模型服务化：
"""

from transformers import pipeline

# TODO: 待实现, 从模型路径加载微调后的模型
diag_pipeline = pipeline('text-generation', model='./fine_tuned_model')
summary = ""
diag_pipeline(summary, max_length=200)