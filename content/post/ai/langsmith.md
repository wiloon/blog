---
title: LangSmith - LLM 应用的可观测性平台
author: "-"
date: 2026-07-26T23:14:18+08:00
lastmod: 2026-07-26T23:14:18+08:00
url: langsmith
categories:
  - AI
tags:
  - AI-assisted
  - remix
  - LangChain
  - LangGraph
  - observability
  - LLM
---

## 什么是 LangSmith

LangSmith 是 LangChain 团队推出的 LLM 应用可观测性与评估平台，用于追踪（trace）、调试、测试和监控基于 LLM 的应用。它不要求应用一定使用 LangChain 或 LangGraph 构建——任何调用 LLM 的代码都可以接入 LangSmith，但与 LangChain / LangGraph 的集成是开箱即用的。

**核心定位**：LLM 应用的"生产环境可观测性 + 离线评估"工具，解决 LLM 应用调试困难、行为不透明、质量难以量化的问题。

**官方仓库 / 产品**：`langchain-ai/langsmith-sdk`（SDK 开源，平台本身为托管 SaaS，也提供自托管方案）。

## 为什么需要 LangSmith

传统软件的日志和监控体系（APM、ELK 等）不足以覆盖 LLM 应用的调试需求：

1. **多步骤链路不透明**：一次 Agent 调用可能包含多次 LLM 请求、工具调用、检索操作，普通日志难以还原完整调用树
2. **Prompt 调试依赖人工**：Prompt 的微小改动可能显著影响输出质量，缺乏系统化的对比手段
3. **输出质量难以量化**：LLM 输出是非确定性的自然语言，传统的断言测试不适用
4. **成本和延迟不可见**：Token 消耗、模型延迟分散在各次调用中，难以聚合分析

LangSmith 针对这些痛点提供了追踪、数据集管理、评估和监控能力。

## 核心功能

### 1. Tracing（追踪）

记录一次请求内所有 LLM 调用、工具调用、检索操作的完整调用树，包括输入、输出、耗时、Token 用量。

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# LangChain / LangGraph applications are traced automatically
# once the environment variables above are set
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
result = llm.invoke("Explain what LangSmith does")
```

对于不使用 LangChain 的代码，可以用 `@traceable` 装饰器手动接入：

```python
from langsmith import traceable

@traceable
def retrieve_documents(query: str) -> list[str]:
    # custom retrieval logic
    return search_index(query)

@traceable
def generate_answer(query: str, docs: list[str]) -> str:
    # custom LLM call
    return call_llm(query, docs)
```

### 2. Datasets（数据集）

将真实调用中的输入输出保存为测试用例，用于回归测试和评估。

```python
from langsmith import Client

client = Client()

dataset = client.create_dataset(
    dataset_name="qa-eval-set",
    description="Regression set collected from production traces"
)

client.create_example(
    inputs={"question": "What is LangSmith?"},
    outputs={"answer": "An LLM observability and evaluation platform."},
    dataset_id=dataset.id,
)
```

### 3. Evaluation（评估）

对数据集运行自动化评估，支持内置评估器（如正确性、相关性）和自定义评估函数，也支持用另一个 LLM 作为评委（LLM-as-judge）。

```python
from langsmith.evaluation import evaluate

def correctness_evaluator(run, example):
    predicted = run.outputs["answer"]
    expected = example.outputs["answer"]
    score = 1.0 if predicted.strip() == expected.strip() else 0.0
    return {"key": "correctness", "score": score}

results = evaluate(
    lambda inputs: {"answer": generate_answer(inputs["question"], [])},
    data="qa-eval-set",
    evaluators=[correctness_evaluator],
)
```

### 4. Monitoring（监控）

生产环境的实时监控面板，展示请求量、延迟、错误率、Token 消耗和成本趋势，支持按 tag、metadata 过滤。

### 5. Prompt Hub

集中管理和版本化 Prompt 模板，支持团队协作和 Prompt 的 A/B 对比。

## 与 LangGraph 集成

[LangGraph](./langgraph.md) 应用开启 `LANGCHAIN_TRACING_V2` 后，图中每个节点的执行都会被记录为独立的 span，可以在 LangSmith 中直接查看状态在各节点间的流转：

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"

# after running app.invoke(inputs), the full graph execution
# (node inputs/outputs, conditional edges taken) appears in LangSmith
result = app.invoke(inputs)
```

## 优势与劣势

### 优势

1. **调试效率高**：完整调用树 + 输入输出回放，排查 Agent 异常行为比读日志快得多
2. **与 LangChain / LangGraph 无缝集成**：只需设置环境变量，无需改动业务代码
3. **支持非 LangChain 项目**：通过 `traceable` 装饰器可接入任意 Python/JS 代码
4. **评估体系完整**：数据集、评估器、LLM-as-judge 覆盖离线测试到线上监控全链路

### 劣势

1. **托管版为付费 SaaS**：免费额度有限，生产环境用量大时成本上升
2. **额外依赖**：引入外部服务依赖，需要考虑数据隐私和网络可用性
3. **自托管配置复杂**：企业自托管方案部署和维护成本高于直接使用 SaaS

## 使用建议

**适合接入 LangSmith 的场景**：

1. ✅ 使用 LangChain / LangGraph 构建的多步骤 Agent，调试调用链路
2. ✅ 需要系统化评估 Prompt 或模型效果（回归测试、A/B 对比）
3. ✅ 生产环境需要监控 LLM 调用的延迟、成本、错误率

**可以不引入 LangSmith 的场景**：

1. ❌ 简单的单次 LLM 调用，日志已足够定位问题
2. ❌ 对数据外发有严格合规要求且未评估自托管方案
3. ❌ 团队已有成熟的自建可观测性体系，接入成本大于收益

## 总结

LangSmith 补齐了 LLM 应用从开发调试到生产监控的可观测性缺口：调用链路靠 Tracing 还原，输出质量靠 Datasets + Evaluation 量化，线上表现靠 Monitoring 持续观察。它不绑定 LangChain 生态，但与 [LangChain](./langchain.md)、[LangGraph](./langgraph.md) 的集成成本最低，是这套技术栈里天然的调试搭子。

## 相关文章

- [LangChain](./langchain.md)
- [LangGraph](./langgraph.md)
