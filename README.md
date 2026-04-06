# 本地化智能文档问答系统

基于 **检索增强生成 (RAG)** 技术的本地智能文档问答系统，支持多种文档格式，采用混合检索策略，提供 Web UI 和 REST API 两种访问方式。

---

## ✨ 主要特性

- 📄 **多格式支持** - PDF、Word、Excel、PPT、TXT、Markdown
- 🔍 **混合检索** - FAISS 向量检索 + BM25 关键词检索
- 🤖 **双模型后端** - 本地 Ollama / 云端 SiliconFlow 灵活切换
- 🌐 **联网搜索** - 可选集成网络搜索增强回答
- 📊 **可视化调试** - 文档分块可视化、系统监控面板
- 🔒 **完全本地化** - 支持离线部署，数据隐私安全
- 🚀 **REST API** - 提供 FastAPI 接口便于集成

---

## 🛠 技术栈

| 类别                 | 技术                                     |
| -------------------- | ---------------------------------------- |
| **前端**       | Gradio 6.x                               |
| **向量存储**   | FAISS                                    |
| **关键词检索** | BM25 + jieba 中文分词                    |
| **嵌入模型**   | sentence-transformers (all-MiniLM-L6-v2) |
| **LLM 后端**   | Ollama (本地) / SiliconFlow (云端)       |
| **文档处理**   | LangChain + PyPDF2 + python-docx         |
| **API 框架**   | FastAPI + Uvicorn                        |

---

## 📦 快速开始

### 1️⃣ 安装依赖

```bash
# 克隆项目
cd Local_Pdf_Chat_RAG

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2️⃣ 配置环境变量

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，填入 API 密钥（可选）
# - SILICONFLOW_API_KEY: 云端模型 API（推荐）
# - SERPAPI_KEY: 联网搜索功能（可选）
```

### 3️⃣ 启动服务

#### 方式一：Web UI（推荐）

```bash
python rag_demo.py
```

启动后自动打开浏览器，访问 `http://127.0.0.1:17995`

#### 方式二：REST API

```bash
python api_router.py
```

API 地址：`http://127.0.0.1:8000`

---

## ⚙️ 配置说明

在 `config.py` 中可调整以下参数：

```python
# 文本分块参数
CHUNK_SIZE = 400          # 分块大小（字符数）
CHUNK_OVERLAP = 40        # 重叠字符数

# 检索参数
HYBRID_ALPHA = 0.7        # 向量检索权重 (0-1)
RETRIEVAL_TOP_K = 10      # 检索候选数量
RERANK_TOP_K = 5          # 重排序后保留数量

# 模型配置
OLLAMA_MODEL_NAME = "deepseek-r1:8b"
SILICONFLOW_MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
```

---

## 📂 项目结构

```
Local_Pdf_Chat_RAG/
├── rag_demo.py              # Gradio Web UI 主程序
├── api_router.py            # FastAPI REST API 服务
├── config.py                # 配置文件
├── requirements.txt         # Python 依赖
├── .env                     # 环境变量配置
│
├── core/                    # 核心 RAG 模块
│   ├── document_loader.py   # 文档加载
│   ├── text_splitter.py     # 文本分块
│   ├── embeddings.py        # 向量嵌入
│   ├── vector_store.py      # FAISS 向量存储
│   ├── bm25_index.py        # BM25 索引
│   ├── retriever.py         # 混合检索器
│   ├── reranker.py          # 重排序器
│   └── generator.py         # LLM 生成器
│
└── utils/                   # 工具模块
    └── network.py           # 网络工具
```

---

## 💡 使用示例

### Web UI 方式

1. 打开 `http://127.0.0.1:17995`
2. 上传文档（支持多选）
3. 等待处理完成
4. 输入问题，开始对话

### REST API 方式

```bash
# 上传文档
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "files=@document.pdf"

# 提问
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "文档的主要内容是什么？"}'
```

---

## 🎯 核心 RAG 流程

```
用户上传文档
    ↓
[文档提取] 支持多格式
    ↓
[智能分块] chunk_size=400, overlap=40
    ↓
[向量嵌入] all-MiniLM-L6-v2
    ↓
┌───────────────┬───────────────┐
│  FAISS索引    │   BM25索引    │
│  (语义检索)   │  (关键词检索) │
└───────────────┴───────────────┘
    ↓
[混合检索] α=0.7 + 0.3
    ↓
[重排序] 交叉编码器
    ↓
[答案生成] LLM (Ollama/SiliconFlow)
```

---

## 📌 注意事项

1. **首次运行**会自动下载嵌入模型 (~80MB)，请确保网络畅通
2. 使用本地 Ollama 需先安装并启动 [Ollama](https://ollama.ai/)
3. SiliconFlow API Key 可在 [硅基流动](https://siliconflow.cn/) 获取
4. 建议使用 Python 3.8+ 环境
