---
title: LangGraph - 构建状态化 AI 工作流的框架
author: "-"
date: 2026-01-18T10:45:00+08:00
url: langgraph
categories:
  - AI
tags:
  - AI-assisted
  - LangChain
  - agent
  - workflow
  - python
---

## 什么是 LangGraph

LangGraph 是 LangChain 生态系统中的一个框架，专门用于构建有状态的、多步骤的 AI 应用程序。它通过图（Graph）的方式来定义和管理复杂的 AI 工作流，让开发者能够创建具有循环、条件分支和持久化状态的智能体系统。

LangGraph 的核心理念是将 AI 应用程序建模为**状态机**，其中节点代表操作步骤，边代表流程控制，状态在节点之间传递和更新。

## 核心概念

### State（状态）

State 是在整个工作流中传递和更新的数据结构。通常使用 TypedDict 定义：

```python
from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_input: str
    analysis_result: str
```

### Node（节点）

Node 是执行具体操作的函数，接收当前状态并返回更新后的状态：

```python
def research_node(state: AgentState):
    # 执行研究任务
    result = do_research(state['user_input'])
    return {
        "analysis_result": result,
        "messages": [("assistant", f"研究完成：{result}")]
    }
```

### Edge（边）

Edge 定义节点之间的连接关系：

- **Normal Edge**（普通边）：直接连接两个节点
- **Conditional Edge**（条件边）：根据状态决定下一个节点

```python
from langgraph.graph import StateGraph, END

# 普通边
workflow.add_edge("node_a", "node_b")

# 条件边
def should_continue(state):
    if state['done']:
        return END
    return "continue_node"

workflow.add_conditional_edges(
    "decision_node",
    should_continue
)
```

### Graph（图）

Graph 是完整的工作流定义，包含所有节点、边和状态管理：

```python
from langgraph.graph import StateGraph

workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("research", research_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("respond", respond_node)

# 定义边
workflow.add_edge("research", "analyze")
workflow.add_edge("analyze", "respond")

# 设置入口点
workflow.set_entry_point("research")

# 编译图
app = workflow.compile()
```

## 核心特性

### 1. 状态持久化

LangGraph 支持状态的持久化存储，可以实现：

- 会话恢复
- 长时间运行的任务
- 断点续传

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# 使用 SQLite 作为检查点存储
memory = SqliteSaver.from_conn_string("checkpoints.db")

app = workflow.compile(checkpointer=memory)

# 运行时指定线程 ID
config = {"configurable": {"thread_id": "conversation-1"}}
result = app.invoke({"messages": [("user", "你好")]}, config)
```

### 2. 循环和迭代

支持在图中创建循环，实现迭代式的任务处理：

```python
def should_continue(state):
    if len(state['messages']) > 10:
        return END
    if state['task_done']:
        return END
    return "continue_processing"

workflow.add_conditional_edges(
    "process_node",
    should_continue,
    {
        "continue_processing": "process_node",  # 循环回自己
        END: END
    }
)
```

### 3. 人机协作（Human-in-the-Loop）

可以在工作流中插入人工干预节点：

```python
from langgraph.checkpoint.memory import MemorySaver

workflow.add_node("human_review", human_review_node)
workflow.add_edge("agent_action", "human_review")

# 使用中断点暂停执行
workflow.add_edge("human_review", "continue_action")

app = workflow.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["human_review"]  # 在此节点前暂停
)

# 首次运行，会在 human_review 前暂停
result = app.invoke(input_data, config)

# 人工审核后继续
result = app.invoke(None, config)  # 从暂停点继续
```

### 4. 条件分支

根据状态动态决定执行路径：

```python
def route_question(state):
    question_type = classify_question(state['question'])
    
    if question_type == "math":
        return "math_solver"
    elif question_type == "search":
        return "web_search"
    else:
        return "general_qa"

workflow.add_conditional_edges(
    "classifier",
    route_question,
    {
        "math_solver": "math_node",
        "web_search": "search_node",
        "general_qa": "qa_node"
    }
)
```

## 与 LangChain 的关系

LangGraph 是 LangChain 生态系统的一部分，两者的关系：

- **LangChain**：提供基础组件（LLM、Prompt、Chain、Tool 等）
- **LangGraph**：提供工作流编排和状态管理能力

LangGraph 可以无缝集成 LangChain 的组件：

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph

llm = ChatOpenAI(model="gpt-4")

def agent_node(state):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
```

## 实际应用场景

### 智能客服系统

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, add_messages

class CustomerServiceState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: str
    resolved: bool

def classify_intent(state):
    # 意图识别
    last_message = state['messages'][-1].content
    intent = intent_classifier(last_message)
    return {"intent": intent}

def handle_inquiry(state):
    # 处理查询
    response = handle_customer_inquiry(state['intent'])
    return {
        "messages": [("assistant", response)],
        "resolved": True
    }

def escalate_to_human(state):
    # 转人工
    return {
        "messages": [("assistant", "正在为您转接人工客服...")],
        "resolved": True
    }

def should_escalate(state):
    if state['intent'] == "complex" or state['intent'] == "complaint":
        return "escalate"
    return "handle"

# 构建工作流
workflow = StateGraph(CustomerServiceState)
workflow.add_node("classify", classify_intent)
workflow.add_node("handle", handle_inquiry)
workflow.add_node("escalate", escalate_to_human)

workflow.set_entry_point("classify")
workflow.add_conditional_edges(
    "classify",
    should_escalate,
    {
        "handle": "handle",
        "escalate": "escalate"
    }
)
workflow.add_edge("handle", END)
workflow.add_edge("escalate", END)

app = workflow.compile()
```

### 研究助手

```python
class ResearchState(TypedDict):
    question: str
    research_data: list
    analysis: str
    final_report: str
    iterations: int

def search_node(state):
    # 搜索相关信息
    results = web_search(state['question'])
    return {"research_data": results}

def analyze_node(state):
    # 分析数据
    analysis = llm_analyze(state['research_data'])
    return {"analysis": analysis}

def should_search_more(state):
    if state['iterations'] >= 3:
        return "report"
    if is_enough_data(state['research_data']):
        return "report"
    return "search_more"

def report_node(state):
    # 生成最终报告
    report = generate_report(state['analysis'])
    return {"final_report": report}

workflow = StateGraph(ResearchState)
workflow.add_node("search", search_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("report", report_node)

workflow.set_entry_point("search")
workflow.add_edge("search", "analyze")
workflow.add_conditional_edges(
    "analyze",
    should_search_more,
    {
        "search_more": "search",  # 循环搜索
        "report": "report"
    }
)
workflow.add_edge("report", END)

app = workflow.compile()
```

### 多工具 Agent

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    return str(eval(expression))

@tool
def search(query: str) -> str:
    """搜索信息"""
    return web_search_api(query)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    tool_calls: list

def agent_node(state):
    # Agent 决策
    response = llm_with_tools.invoke(state['messages'])
    return {"messages": [response]}

def tool_node(state):
    # 执行工具
    last_message = state['messages'][-1]
    results = execute_tools(last_message.tool_calls)
    return {"messages": results}

def should_continue(state):
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)
workflow.add_edge("tools", "agent")  # 工具执行后返回 agent

app = workflow.compile()
```

## 安装和快速开始

### 安装

```bash
pip install langgraph
pip install langchain-openai  # 如果使用 OpenAI
```

### 快速示例

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, add_messages
from langchain_openai import ChatOpenAI

# 定义状态
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 创建 LLM
llm = ChatOpenAI(model="gpt-4")

# 定义节点
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# 构建图
workflow = StateGraph(State)
workflow.add_node("chatbot", chatbot)
workflow.set_entry_point("chatbot")
workflow.add_edge("chatbot", END)

# 编译并运行
app = workflow.compile()

result = app.invoke({
    "messages": [("user", "你好，介绍一下你自己")]
})

print(result["messages"][-1].content)
```

## 高级特性

### 并行执行

多个节点可以并行执行：

```python
from langgraph.graph import StateGraph

workflow = StateGraph(State)
workflow.add_node("task_a", task_a_node)
workflow.add_node("task_b", task_b_node)
workflow.add_node("merge", merge_node)

workflow.set_entry_point("task_a")
workflow.set_entry_point("task_b")  # 并行入口

workflow.add_edge("task_a", "merge")
workflow.add_edge("task_b", "merge")
workflow.add_edge("merge", END)
```

### 子图（Subgraph）

可以将复杂的工作流模块化：

```python
# 定义子图
sub_workflow = StateGraph(SubState)
sub_workflow.add_node("step1", step1_node)
sub_workflow.add_node("step2", step2_node)
sub_workflow.set_entry_point("step1")
sub_workflow.add_edge("step1", "step2")
sub_workflow.add_edge("step2", END)

sub_graph = sub_workflow.compile()

# 在主图中使用子图
main_workflow = StateGraph(MainState)
main_workflow.add_node("subprocess", sub_graph)
main_workflow.add_edge("start", "subprocess")
```

### 流式输出

支持流式处理，实时获取输出：

```python
inputs = {"messages": [("user", "讲个故事")]}

# 流式输出每个节点的结果
for output in app.stream(inputs):
    for key, value in output.items():
        print(f"节点 '{key}':")
        print(value)
        print("\n---\n")
```

### 时间旅行和回放

利用检查点机制实现时间旅行：

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}

# 第一次运行
app.invoke(input1, config)

# 第二次运行
app.invoke(input2, config)

# 获取状态历史
state_history = app.get_state_history(config)

# 回到之前的状态
for state in state_history:
    print(f"时间点: {state.created_at}")
    print(f"状态: {state.values}")
```

## 最佳实践

### 1. 状态设计

保持状态简洁，只包含必要信息：

```python
# 好的设计
class State(TypedDict):
    user_input: str
    context: list
    result: str

# 避免过度复杂
class BadState(TypedDict):
    user_input: str
    intermediate_step_1: str
    intermediate_step_2: str
    intermediate_step_3: str
    # ... 太多中间状态
```

### 2. 错误处理

在节点中添加错误处理：

```python
def robust_node(state):
    try:
        result = risky_operation(state['input'])
        return {"result": result, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}

def error_router(state):
    if state.get('error'):
        return "error_handler"
    return "next_node"
```

### 3. 测试策略

单独测试每个节点：

```python
def test_research_node():
    test_state = {
        "question": "测试问题",
        "research_data": []
    }
    result = research_node(test_state)
    assert "research_data" in result
    assert len(result["research_data"]) > 0
```

### 4. 性能优化

- 使用异步节点处理 I/O 密集型任务
- 合理使用并行执行
- 限制循环次数，避免无限循环

```python
async def async_node(state):
    result = await async_operation()
    return {"result": result}

def limit_iterations(state):
    if state.get('iterations', 0) >= MAX_ITERATIONS:
        return END
    return "continue"
```

## LangGraph vs 其他框架

### LangGraph vs CrewAI

- **LangGraph**：底层工作流框架，灵活但需要更多代码
- **CrewAI**：高层多智能体框架，更关注角色和任务抽象

### LangGraph vs LangChain Expression Language (LCEL)

- **LCEL**：链式调用，适合简单的线性流程
- **LangGraph**：图结构，适合复杂的分支和循环逻辑

### 选择建议

- 简单链式调用 → LCEL
- 需要循环、分支、状态管理 → LangGraph
- 需要角色化多智能体 → CrewAI + LangGraph

## 注意事项

1. **状态管理**：合理设计状态结构，避免状态过于庞大
1. **循环控制**：必须有明确的终止条件，防止无限循环
1. **内存使用**：持久化检查点会占用存储空间，定期清理
1. **调试复杂度**：复杂图的调试较困难，建议使用 LangSmith 追踪
1. **版本兼容性**：LangGraph 更新较快，注意版本兼容性

## 可视化工具

LangGraph 支持将工作流可视化：

```python
from IPython.display import Image, display

# 生成图的可视化
display(Image(app.get_graph().draw_mermaid_png()))
```

生成 Mermaid 图：

```python
print(app.get_graph().draw_mermaid())
```

## 调试和监控

使用 LangSmith 进行追踪：

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"

# 运行后可以在 LangSmith 中查看完整追踪
result = app.invoke(inputs)
```

## 资源链接

- 官方网站：https://www.langchain.com/langgraph
- 官方文档：https://langchain-ai.github.io/langgraph/
- GitHub 仓库：https://github.com/langchain-ai/langgraph
- LangChain 官网：https://www.langchain.com/
- 教程和示例：https://github.com/langchain-ai/langgraph/tree/main/examples

## 小结

LangGraph 提供了一个强大的框架来构建复杂的、有状态的 AI 应用程序。通过图结构、状态管理和灵活的控制流，LangGraph 让开发者能够创建具有循环、分支、人机协作等高级特性的智能体系统。它是构建生产级 AI 应用的理想选择，特别适合需要复杂决策逻辑和长期状态维护的场景。
