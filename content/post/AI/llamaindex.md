---
title: "LlamaIndex"
author: "-"
date: 2026-04-26T14:39:27+08:00
lastmod: 2026-07-23T00:30:26+08:00
url: llamaindex
categories:
  - AI
tags:
  - ai-agent
  - llamaindex
  - RAG
  - LLM
  - remix
  - AI-assisted
---

## LlamaIndex 详解

### 什么是 LlamaIndex

LlamaIndex（原名 GPT Index）是一个专注于**数据连接和检索**的开源框架，主要用于构建 RAG（检索增强生成）应用。与 LangChain 相比，LlamaIndex 更专注于**数据索引、检索和查询**，是构建知识库和文档问答系统的首选工具。

**核心定位**：数据框架（Data Framework for LLM Applications）

**官方仓库**：`run-llama/llama_index`

**设计哲学**：
- LangChain：通用的 LLM 应用框架（Chain、Agent、Memory 等）
- LlamaIndex：专注于数据摄入、索引和检索

#### ⚠️ 名称说明：LlamaIndex vs Llama2

**重要澄清**：LlamaIndex 与 Meta 的 Llama2/Llama3 开源模型**没有任何关系**，它们是完全独立的项目：

| 项目 | 类型 | 开发者 | 功能 |
|-----|------|--------|------|
| **LlamaIndex** | 开发框架 | LlamaIndex 团队（原 run-llama） | 数据索引和检索框架 |
| **Llama2/Llama3** | 大语言模型 | Meta（Facebook） | 开源 LLM 模型 |

**为什么叫 "Llama"？**
- LlamaIndex 的命名来自"Large Language Model Applications"的缩写
- 与 Meta 的 Llama 模型纯属巧合（命名冲突）

**实际关系**：
- LlamaIndex 框架可以**使用** Llama2/Llama3 作为底层 LLM
- 但 LlamaIndex 也支持 OpenAI、Claude、Gemini 等任何 LLM
- 两者是"框架"与"模型"的关系，而非从属关系

**示例**：
```python
# LlamaIndex 框架 + Llama2 模型
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# 使用本地 Llama2 模型
llm = Ollama(model="llama2")

# LlamaIndex 框架进行索引和检索
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

# 查询（底层调用 Llama2）
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("问题")
```

**总结**：
- ❌ **不是**：LlamaIndex 不是 Llama2 的配套工具
- ❌ **不是**：LlamaIndex 不是只能用 Llama 模型
- ✅ **是**：LlamaIndex 是通用的 RAG 框架，可以使用任何 LLM（包括 Llama2）

### 核心概念

#### 1. **Documents（文档）**

原始数据的容器：

```python
from llama_index.core import Document

# 创建文档
doc1 = Document(
    text="LlamaIndex 是一个数据框架...",
    metadata={
        "author": "张三",
        "date": "2025-11-19",
        "category": "技术文档"
    }
)

# 从文件加载
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()
```

#### 2. **Nodes（节点）**

文档切分后的基本单元：

```python
from llama_index.core.node_parser import SentenceSplitter

# 切分文档
parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
nodes = parser.get_nodes_from_documents(documents)

# 节点包含：
# - text: 文本内容
# - metadata: 元数据
# - relationships: 与其他节点的关系
```

#### 3. **Index（索引）**

数据的组织结构，支持高效检索：

```python
from llama_index.core import VectorStoreIndex, SummaryIndex, TreeIndex

# 向量索引（最常用）
vector_index = VectorStoreIndex.from_documents(documents)

# 摘要索引
summary_index = SummaryIndex.from_documents(documents)

# 树索引
tree_index = TreeIndex.from_documents(documents)
```

#### 4. **Query Engine（查询引擎）**

处理用户查询的接口：

```python
# 创建查询引擎
query_engine = index.as_query_engine()

# 查询
response = query_engine.query("LlamaIndex 的主要功能是什么？")
print(response)
```

#### 5. **Chat Engine（对话引擎）**

支持多轮对话的查询接口：

```python
# 创建对话引擎
chat_engine = index.as_chat_engine()

# 多轮对话
response1 = chat_engine.chat("LlamaIndex 是什么？")
response2 = chat_engine.chat("它和 LangChain 有什么区别？")  # 保持上下文
```

### 快速开始示例

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# 1. 加载数据
documents = SimpleDirectoryReader("./data").load_data()

# 2. 创建索引
index = VectorStoreIndex.from_documents(documents)

# 3. 查询
query_engine = index.as_query_engine()
response = query_engine.query("文档的主要内容是什么？")
print(response)

# 4. 持久化索引
index.storage_context.persist(persist_dir="./storage")

# 5. 加载索引
from llama_index.core import load_index_from_storage, StorageContext

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

### 主要索引类型

#### 1. **VectorStoreIndex（向量索引）**

最常用的索引类型，使用语义相似度检索：

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)

# 配置检索参数
query_engine = index.as_query_engine(
    similarity_top_k=5,  # 返回前5个最相关结果
    response_mode="compact"  # 响应模式
)

response = query_engine.query("查询内容")
```

#### 2. **SummaryIndex（摘要索引）**

适合需要遍历所有文档的场景：

```python
from llama_index.core import SummaryIndex

index = SummaryIndex.from_documents(documents)

# 会考虑所有文档生成答案
query_engine = index.as_query_engine()
response = query_engine.query("总结所有文档的内容")
```

#### 3. **TreeIndex（树索引）**

层次化的索引结构：

```python
from llama_index.core import TreeIndex

index = TreeIndex.from_documents(documents)

# 从根节点开始，自上而下查询
query_engine = index.as_query_engine()
response = query_engine.query("查询内容")
```

#### 4. **KeywordTableIndex（关键词索引）**

基于关键词匹配：

```python
from llama_index.core import KeywordTableIndex

index = KeywordTableIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("Python")  # 匹配包含 "Python" 的文档
```

### 高级特性

#### 1. **自定义 LLM 和 Embedding**

```python
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

# 配置 LLM
Settings.llm = OpenAI(model="gpt-4", temperature=0.1)

# 配置 Embedding
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")

# 创建索引（会使用上述配置）
index = VectorStoreIndex.from_documents(documents)
```

#### 2. **集成向量数据库**

```python
# Chroma
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.create_collection("my_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# 使用向量存储创建索引
from llama_index.core import StorageContext

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
import pinecone

pinecone.init(api_key="your-api-key", environment="us-west1-gcp")
pinecone_index = pinecone.Index("my-index")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# Weaviate、Milvus、Qdrant 等都支持
```

#### 3. **自定义 Prompt**

```python
from llama_index.core import PromptTemplate

# 自定义查询提示模板
qa_prompt_tmpl = (
    "上下文信息如下：\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "基于上述信息（不要使用先验知识），回答问题：{query_str}\n"
)

qa_prompt = PromptTemplate(qa_prompt_tmpl)

# 使用自定义提示
query_engine = index.as_query_engine(
    text_qa_template=qa_prompt
)
```

#### 4. **Retriever（检索器）**

更灵活的检索控制：

```python
from llama_index.core.retrievers import VectorIndexRetriever

# 创建检索器
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

# 检索
nodes = retriever.retrieve("查询内容")

# 自定义查询引擎
from llama_index.core.query_engine import RetrieverQueryEngine

query_engine = RetrieverQueryEngine(retriever=retriever)
response = query_engine.query("查询内容")
```

#### 5. **Re-ranking（重排序）**

提高检索质量：

```python
from llama_index.core.postprocessor import SimilarityPostprocessor

# 创建后处理器
postprocessor = SimilarityPostprocessor(similarity_cutoff=0.7)

# 应用到查询引擎
query_engine = index.as_query_engine(
    node_postprocessors=[postprocessor]
)
```

#### 6. **Sub-Question Query Engine（子问题查询）**

将复杂问题分解：

```python
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool

# 创建多个专业索引
tech_index = VectorStoreIndex.from_documents(tech_docs)
business_index = VectorStoreIndex.from_documents(business_docs)

# 定义工具
query_engine_tools = [
    QueryEngineTool(
        query_engine=tech_index.as_query_engine(),
        metadata={"name": "tech", "description": "技术文档"}
    ),
    QueryEngineTool(
        query_engine=business_index.as_query_engine(),
        metadata={"name": "business", "description": "商业文档"}
    ),
]

# 创建子问题查询引擎
query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=query_engine_tools
)

# 复杂查询会自动分解
response = query_engine.query(
    "比较技术方案和商业模式的优劣"
)
```

### 实战示例：完整的文档问答系统

```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
import os

class DocumentQASystem:
    def __init__(self, data_dir: str, persist_dir: str = "./storage"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        
        # 配置
        Settings.llm = OpenAI(model="gpt-4", temperature=0)
        Settings.embed_model = OpenAIEmbedding()
        
        self.index = None
        self.query_engine = None
        
    def build_index(self):
        """构建索引"""
        # 加载文档
        documents = SimpleDirectoryReader(self.data_dir).load_data()
        
        # 创建索引
        self.index = VectorStoreIndex.from_documents(documents)
        
        # 持久化
        self.index.storage_context.persist(persist_dir=self.persist_dir)
        
        print(f"索引已创建，共 {len(documents)} 个文档")
        
    def load_index(self):
        """加载已有索引"""
        if not os.path.exists(self.persist_dir):
            raise ValueError("索引不存在，请先构建索引")
        
        storage_context = StorageContext.from_defaults(
            persist_dir=self.persist_dir
        )
        self.index = load_index_from_storage(storage_context)
        
        print("索引已加载")
        
    def create_query_engine(self, similarity_top_k: int = 3):
        """创建查询引擎"""
        if self.index is None:
            raise ValueError("请先加载或构建索引")
        
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=similarity_top_k,
            response_mode="compact"
        )
        
    def query(self, question: str):
        """查询"""
        if self.query_engine is None:
            self.create_query_engine()
        
        response = self.query_engine.query(question)
        
        # 返回答案和来源
        return {
            "answer": str(response),
            "source_nodes": [
                {
                    "text": node.node.text[:200] + "...",
                    "score": node.score,
                    "metadata": node.node.metadata
                }
                for node in response.source_nodes
            ]
        }

# 使用
qa_system = DocumentQASystem(data_dir="./docs")

# 首次使用：构建索引
qa_system.build_index()

# 后续使用：加载索引
# qa_system.load_index()

# 查询
result = qa_system.query("LlamaIndex 的主要功能是什么？")
print(result["answer"])
print("\n来源：")
for i, source in enumerate(result["source_nodes"], 1):
    print(f"{i}. 分数: {source['score']:.2f}")
    print(f"   内容: {source['text']}")
```

### LlamaIndex vs LangChain

| 维度 | LlamaIndex | LangChain |
|-----|-----------|-----------|
| **核心定位** | 数据框架（RAG 专家） | 通用 LLM 框架 |
| **主要用途** | 数据索引、检索、查询 | Chain、Agent、Memory 全栈 |
| **RAG 能力** | ⭐⭐⭐⭐⭐ 最强 | ⭐⭐⭐⭐ 完善 |
| **Agent 能力** | ⭐⭐⭐ 基础支持 | ⭐⭐⭐⭐⭐ 全面 |
| **学习曲线** | 较平缓（专注 RAG） | 陡峭（概念多） |
| **文档质量** | 优秀 | 良好 |
| **适用场景** | 文档问答、知识库 | 复杂 Agent、多步骤流程 |
| **生态系统** | 丰富（数据连接器） | 极其丰富（各类集成） |

### 使用场景建议

**优先选择 LlamaIndex：**

1. ✅ **文档问答系统**
   - 企业知识库
   - 技术文档查询
   - 法律/医疗文档分析

2. ✅ **RAG 应用**
   - 需要引用来源的回答
   - 大量文档的语义检索
   - 结构化+非结构化数据查询

3. ✅ **数据密集型应用**
   - PDF、Word、Excel 等多格式数据
   - 需要自定义索引结构
   - 复杂的检索策略

**优先选择 LangChain：**

1. ✅ **Agent 应用**
   - 需要动态工具调用
   - 多步骤决策流程
   - 复杂的任务编排

2. ✅ **对话系统**
   - 多轮对话管理
   - 上下文记忆
   - 个性化助手

3. ✅ **工作流自动化**
   - Chain 组合
   - 条件分支
   - 循环和迭代

**混合使用：**

```python
# LlamaIndex 做检索，LangChain 做 Agent
from llama_index.core import VectorStoreIndex
from langchain.tools import Tool
from langchain.agents import initialize_agent

# 1. LlamaIndex 索引
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# 2. 包装成 LangChain 工具
def search_docs(query: str) -> str:
    response = query_engine.query(query)
    return str(response)

search_tool = Tool(
    name="DocumentSearch",
    func=search_docs,
    description="在知识库中搜索信息"
)

# 3. LangChain Agent
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# 4. 执行
result = agent.run("查询并总结文档中关于 AI 的内容")
```

### LlamaIndex 生态

**数据连接器（Data Loaders）**：

- **文档**：PDF、Word、Markdown、HTML
- **数据库**：PostgreSQL、MySQL、MongoDB
- **API**：Notion、Google Docs、Slack、GitHub
- **网页**：BeautifulSoup、Selenium
- **音视频**：Whisper（语音转文本）

**向量数据库集成**：

- Chroma、Pinecone、Weaviate、Milvus、Qdrant、FAISS

**LLM 集成**：

- OpenAI、Anthropic、Google、Azure、本地模型（Ollama、Llama.cpp）

### 总结

**LlamaIndex 的核心优势**：

1. ✅ **RAG 专家**：专为数据索引和检索优化
2. ✅ **易用性**：API 设计简洁，学习曲线平缓
3. ✅ **数据连接器丰富**：支持各种数据源
4. ✅ **检索质量高**：内置多种优化策略
5. ✅ **与 LangChain 互补**：可以混合使用

**适合 LlamaIndex 的团队**：

- 主要需求是文档问答和知识库
- 希望快速上手 RAG 应用
- 需要高质量的检索和引用
- 不需要复杂的 Agent 功能

**技术选型建议**：

- **纯 RAG 应用** → LlamaIndex（首选）
- **复杂 Agent + RAG** → LangChain + LlamaIndex（混合）
- **通用 LLM 应用** → LangChain（首选）

LlamaIndex 在 RAG 领域是最专业的工具，如果你的核心需求是文档问答和知识库，LlamaIndex 是比 LangChain 更好的选择。

## 相关文章

- [AI Agent Development](./ai-agent-development.md)
- [Intent Recognition and Slot Filling](./agent-intent-and-slot-filling.md)
- [Function Calling](./agent-function-calling.md)
- [Tool Calling Patterns](./agent-tool-calling-patterns.md)
- [Chain of Thought (CoT)](./agent-chain-of-thought.md)
- [Output Constraint](./agent-output-constraint.md)
- [LangChain](./langchain.md)
- [Agent Token Routing](./agent-token-routing.md)


## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-23 | 自 `ai-agent-development.md` 拆出为本篇 | 母文过长，按主题拆分为独立文档 |

