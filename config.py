"""
配置
"""

import os
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 第一步：加载环境变量
# 优先加载 .env（用户配置），不存在则回退到 example.env（示例配置）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
dotenv_path = Path(__file__).parent / ".env"
if not dotenv_path.exists():
    dotenv_path = Path(__file__).parent / "example.env"
    logging.warning("⚠️ 未找到 .env 文件，已回退加载 example.env。建议：cp example.env .env 并填入真实 API Key")
load_dotenv(dotenv_path)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 第二步：API 密钥配置
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
SEARCH_ENGINE = "google"

SILICONFLOW_API_KEY = "sk-mpuduvmnxfipztvbjxjonzmivjugmaeijjffqfuawpisrvrm"
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/chat/completions"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 第三步：模型名称配置
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OLLAMA_MODEL_NAME = "deepseek-r1:8b"
SILICONFLOW_MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
RERANK_METHOD = "cross_encoder"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 第四步：RAG 超参数
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHUNK_SIZE = 400          # 文本分块大小（字符数）
CHUNK_OVERLAP = 40        # 相邻分块的重叠字符数
HYBRID_ALPHA = 0.7        # 混合检索中语义检索的权重（0-1）
RETRIEVAL_TOP_K = 10      # 检索返回的候选文档数量
RERANK_TOP_K = 5          # 重排序后保留的文档数量
MAX_RETRIEVAL_ITERATIONS = 3  # 递归检索的最大迭代轮数

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 第五步：运行时环境配置
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
requests.adapters.DEFAULT_RETRIES = 3

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 第六步：LLM 后端自动检测
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def detect_default_model():
    """
    自动检测可用的 LLM 后端，返回默认模型选择
    """
    if SILICONFLOW_API_KEY and SILICONFLOW_API_KEY.strip() and not SILICONFLOW_API_KEY.startswith("Your"):
        logging.info("✅ 检测到 SiliconFlow API Key, 默认使用云端模型")
        return "siliconflow"

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            logging.info("✅ 检测到本地 Ollama 服务，默认使用本地模型")
            return "ollama"
    except Exception:
        pass

    logging.warning("⚠️ 未检测到可用 LLM 后端，请配置 SiliconFlow API Key 或启动 Ollama")
    return "siliconflow"

DEFAULT_MODEL_CHOICE = detect_default_model()
