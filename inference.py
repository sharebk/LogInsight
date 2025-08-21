# inference.py
"""
模型服务化：
"""

from transformers import pipeline

diag_pipeline = pipeline('text-generation', model='./fine_tuned_model')
summary = ""
diag_pipeline(summary, max_length=200)