---
title: "LangChain"
author: "-"
date: 2026-04-26T14:39:27+08:00
lastmod: 2026-07-23T00:30:26+08:00
url: langchain
categories:
  - AI
tags:
  - ai-agent
  - langchain
  - RAG
  - LLM
  - remix
  - AI-assisted
---

## LangChain 详解

### 什么是 LangChain

LangChain 是一个用于构建基于大语言模型（LLM）应用的开源框架。它提供了一套标准化的组件和工具，简化了 AI Agent、聊天机器人、问答系统等应用的开发过程。

**核心理念**：通过"链（Chain）"将多个组件连接起来，构建复杂的 LLM 应用。

**官方仓库**：
- Python：`langchain-ai/langchain`
- JavaScript/TypeScript：`langchain-ai/langchainjs`

### 核心组件

#### 1. **Models（模型）**

支持多种 LLM 提供商：

```python
from langchain.llms import OpenAI, Anthropic, HuggingFaceHub
from langchain.chat_models import ChatOpenAI, ChatAnthropic

# OpenAI
llm = OpenAI(temperature=0.7)

# Claude
chat = ChatAnthropic(model="claude-3-sonnet-20240229")

# 本地模型
from langchain.llms import Ollama
local_llm = Ollama(model="llama2")
```

#### 2. **Prompts（提示模板）**

管理和复用提示词：

```python
from langchain.prompts import PromptTemplate, ChatPromptTemplate

# 简单模板
prompt = PromptTemplate(
    input_variables=["product"],
    template="给{product}写一个广告语"
)

# 聊天模板
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}"),
    ("human", "{user_input}")
])

# 使用
formatted = prompt.format(product="智能手表")
result = llm(formatted)
```

#### 3. **Chains（链）**

将多个组件串联：

```python
from langchain.chains import LLMChain, SimpleSequentialChain

# 单个链
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(product="智能手表")

# 顺序链
chain1 = LLMChain(llm=llm, prompt=prompt1)  # 生成产品描述
chain2 = LLMChain(llm=llm, prompt=prompt2)  # 生成广告语

overall_chain = SimpleSequentialChain(
    chains=[chain1, chain2],
    verbose=True
)
result = overall_chain.run("智能手表")
```

#### 4. **Agents（代理）**

动态决策和工具调用：

```python
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import BaseTool

# 定义工具
class WeatherTool(BaseTool):
    name = "Weather"
    description = "查询天气信息。输入：城市名称"
    
    def _run(self, city: str) -> str:
        return f"{city}的天气：晴朗，25°C"
    
    async def _arun(self, city: str) -> str:
        return self._run(city)

# 创建 Agent
tools = [WeatherTool()]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 执行
result = agent.run("北京明天会下雨吗？")
```

#### 5. **Memory（记忆）**

维护对话上下文：

```python
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain

# 完整历史记忆
memory = ConversationBufferMemory()

# 摘要记忆（节省 Token）
summary_memory = ConversationSummaryMemory(llm=llm)

# 对话链
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# 多轮对话
conversation.predict(input="我叫张三")
conversation.predict(input="我的名字是什么？")  # 回答：张三
```

#### 6. **Document Loaders（文档加载器）**

加载各种格式的数据：

```python
from langchain.document_loaders import (
    TextLoader, PDFLoader, CSVLoader,
    UnstructuredHTMLLoader, GitbookLoader
)

# PDF 文档
loader = PDFLoader("document.pdf")
documents = loader.load()

# 网页
from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://example.com")
documents = loader.load()
```

#### 7. **Vector Stores（向量存储）**

支持 RAG（检索增强生成）：

```python
from langchain.vectorstores import Chroma, FAISS, Pinecone
from langchain.embeddings import OpenAIEmbeddings

# 创建向量存储
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings
)

# 相似度检索
results = vectorstore.similarity_search("查询文本", k=3)

# RAG 链
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

answer = qa_chain.run("用户问题")
```

### LangChain 的 Agent 类型

#### 1. **Zero-shot ReAct**

不需要示例，直接根据工具描述决策：

```python
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```

#### 2. **Conversational ReAct**

带记忆的对话型 Agent：

```python
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)
```

#### 3. **OpenAI Functions**

使用 OpenAI Function Calling：

```python
agent = initialize_agent(
    tools=tools,
    llm=ChatOpenAI(model="gpt-4"),
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)
```

#### 4. **Structured Chat**

支持多参数输入的 Agent：

```python
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```

### 实战示例：完整的 RAG 问答系统

```python
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. 加载文档
loader = DirectoryLoader(
    "./docs",
    glob="**/*.txt",
    loader_cls=TextLoader
)
documents = loader.load()

# 2. 切分文档
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# 3. 创建向量存储
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 4. 定义提示模板
prompt_template = """
基于以下上下文回答问题。如果不知道答案，就说不知道，不要编造答案。

上下文：{context}

问题：{question}

答案：
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# 5. 创建 QA 链
llm = ChatOpenAI(model="gpt-4", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)

# 6. 使用
query = "LangChain 是什么？"
result = qa_chain({"query": query})

print(result["result"])
print("\n来源文档：")
for doc in result["source_documents"]:
    print(f"- {doc.metadata['source']}")
```

### LangChain Expression Language (LCEL)

新一代的链式编程方式（推荐）：

```python
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# 使用 LCEL 构建链
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 执行
result = chain.invoke("LangChain 是什么？")

# 流式输出
for chunk in chain.stream("LangChain 是什么？"):
    print(chunk, end="", flush=True)

# 批量处理
results = chain.batch([
    "问题1",
    "问题2",
    "问题3"
])

# 异步执行
result = await chain.ainvoke("问题")
```

### LangGraph - 高级工作流编排

LangGraph 是 LangChain 的扩展，用于构建复杂的 Agent 工作流：

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated

# 定义状态
class AgentState(TypedDict):
    messages: list
    next: str

# 定义节点
def call_model(state):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def should_continue(state):
    last_message = state["messages"][-1]
    if "FINAL ANSWER" in last_message.content:
        return "end"
    return "continue"

# 构建图
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", call_tools)

workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)
workflow.add_edge("tools", "agent")

app = workflow.compile()

# 执行
result = app.invoke({"messages": [HumanMessage(content="查询天气")]})
```

### LangChain 的优势与劣势

#### 优势

1. **生态丰富**
   - 100+ 集成（LLM、向量数据库、工具）
   - 活跃的社区和文档

2. **快速开发**
   - 预构建的组件和模板
   - 减少样板代码

3. **灵活性**
   - 支持多种 LLM 提供商
   - 可自定义组件

4. **RAG 支持完善**
   - 文档加载、切分、向量化一体化
   - 多种检索策略

5. **持续更新**
   - LCEL、LangGraph 等新特性
   - 跟进 LLM 最新能力

#### 劣势

1. **学习曲线陡峭**
   - 概念较多（Chain、Agent、Memory 等）
   - API 频繁变动

2. **抽象层复杂**
   - 调试困难
   - 性能开销

3. **版本兼容性**
   - 大版本升级可能破坏兼容性
   - 需要频繁更新代码

4. **过度工程**
   - 简单任务可能不需要框架
   - Function Calling 场景可能更简洁

### LangChain vs 原生 Function Calling

| 维度 | LangChain | 原生 Function Calling |
|-----|-----------|---------------------|
| **学习成本** | 高 | 低 |
| **开发速度** | 快（RAG、复杂流程） | 快（简单工具调用） |
| **代码可读性** | 中（抽象层多） | 高 |
| **调试难度** | 高 | 低 |
| **灵活性** | 极高 | 中 |
| **性能** | 中（额外开销） | 高 |
| **适用场景** | RAG、多步骤、复杂编排 | 工具调用、简单 Agent |

### 使用建议

**适合使用 LangChain 的场景**：

1. ✅ **RAG 应用**（文档问答、知识库）
2. ✅ **复杂多步骤流程**（需要编排多个操作）
3. ✅ **需要快速原型**（利用预构建组件）
4. ✅ **多数据源集成**（文档、数据库、API）
5. ✅ **实验和研究**（快速尝试不同架构）

**不适合使用 LangChain 的场景**：

1. ❌ **简单的工具调用**（直接用 Function Calling）
2. ❌ **性能敏感场景**（减少抽象层开销）
3. ❌ **生产环境稳定性要求高**（版本兼容性问题）
4. ❌ **团队对框架不熟悉**（学习成本高）

### 实际项目架构建议

**混合架构（最佳实践）**：

```python
# 使用 LangChain 做 RAG
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# RAG 部分使用 LangChain
vectorstore = Chroma.from_documents(documents, OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# 工具调用使用原生 Function Calling
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "在知识库中搜索信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                }
            }
        }
    }
]

def search_knowledge_base(query: str):
    # 使用 LangChain 的检索器
    docs = retriever.get_relevant_documents(query)
    return "\n".join([doc.page_content for doc in docs])

# Agent 主循环使用原生 API
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages,
    tools=tools_schema
)

# 结合两者优势：LangChain 处理复杂数据，Function Calling 做工具调用
```

### 总结

LangChain 是一个**功能强大但复杂的框架**：

- **适合**：RAG、复杂编排、快速原型、多数据源集成
- **不适合**：简单工具调用、性能敏感场景
- **最佳实践**：在需要的地方使用 LangChain（如 RAG），简单场景使用原生 Function Calling
- **学习建议**：
  1. 先掌握 LangChain 基础组件（Prompts、Chains、Memory）
  2. 重点学习 RAG 相关功能（Document Loaders、Vector Stores）
  3. 了解 LCEL 新语法（推荐）
  4. 关注 LangGraph（Multi-Agent 编排）

LangChain 在 AI Agent 生态中占据重要位置，尤其是在 RAG 和复杂流程编排方面，但不是所有场景的最佳选择。根据具体需求灵活选择技术方案，才是明智之举。

## 相关文章

- [AI Agent Development](./ai-agent-development.md)
- [Intent Recognition and Slot Filling](./agent-intent-and-slot-filling.md)
- [Function Calling](./agent-function-calling.md)
- [Tool Calling Patterns](./agent-tool-calling-patterns.md)
- [Chain of Thought (CoT)](./agent-chain-of-thought.md)
- [Output Constraint](./agent-output-constraint.md)
- [LlamaIndex](./llamaindex.md)
- [Agent Token Routing](./agent-token-routing.md)


## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-23 | 自 `ai-agent-development.md` 拆出为本篇 | 母文过长，按主题拆分为独立文档 |

