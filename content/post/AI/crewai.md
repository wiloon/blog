---
title: CrewAI - 多智能体协作框架
author: "-"
date: 2026-01-18T10:30:00+08:00
url: crewai
categories:
  - AI
tags:
  - AI-assisted
  - agent
  - LLM
  - python
---

## 什么是 CrewAI

CrewAI 是一个开源的 Python 框架，专门用于构建和管理多智能体（Multi-Agent）系统。它允许开发者创建一个由多个 AI 智能体组成的"团队"（Crew），这些智能体可以协同工作，共同完成复杂的任务。

## 核心概念

### Agent（智能体）

Agent 是 CrewAI 中的基本执行单元，代表一个具有特定角色和能力的 AI 助手。每个 Agent 具有：

- **Role**（角色）：定义 Agent 的身份和职责
- **Goal**（目标）：Agent 要达成的目标
- **Backstory**（背景故事）：为 Agent 提供上下文和个性
- **Tools**（工具）：Agent 可以使用的工具集合

```python
from crewai import Agent

researcher = Agent(
    role='研究员',
    goal='收集和分析相关信息',
    backstory='你是一位经验丰富的研究专家，擅长从各种来源收集准确信息',
    tools=[search_tool, scrape_tool],
    verbose=True
)
```

### Task（任务）

Task 定义了需要完成的具体工作，包括：

- **Description**（描述）：任务的详细说明
- **Agent**：负责执行该任务的智能体
- **Expected Output**（期望输出）：任务完成后的预期结果

```python
from crewai import Task

research_task = Task(
    description='研究 AI 领域的最新发展趋势',
    agent=researcher,
    expected_output='一份包含最新 AI 趋势的详细报告'
)
```

### Crew（团队）

Crew 是多个 Agent 和 Task 的组合，负责协调整个工作流程：

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, write_task, review_task],
    process=Process.sequential  # 顺序执行
)

result = crew.kickoff()
```

## 执行流程

CrewAI 支持两种执行流程：

### Sequential（顺序执行）

任务按照定义的顺序依次执行，每个任务完成后才开始下一个：

```python
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential
)
```

### Hierarchical（层级执行）

引入一个管理者角色，由管理者协调和分配任务：

```python
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4")
)
```

## 核心特性

### 1. 灵活的工具集成

CrewAI 支持集成各种工具，包括：

- 搜索工具（Google Search、Bing Search）
- 文件操作工具
- API 调用工具
- 自定义工具

```python
from crewai_tools import SerperDevTool, FileReadTool

search_tool = SerperDevTool()
file_tool = FileReadTool()

agent = Agent(
    role='数据分析师',
    tools=[search_tool, file_tool]
)
```

### 2. 记忆管理

CrewAI 提供三种记忆类型：

- **Short-term Memory**（短期记忆）：任务执行期间的临时信息
- **Long-term Memory**（长期记忆）：持久化存储的历史信息
- **Entity Memory**（实体记忆）：关于特定实体的信息

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True  # 启用记忆功能
)
```

### 3. 协作机制

Agent 之间可以通过以下方式协作：

- **Delegation**（委托）：Agent 可以将子任务委托给其他 Agent
- **Communication**（通信）：Agent 之间可以交换信息
- **Consensus**（共识）：多个 Agent 可以协商达成一致

## 实际应用场景

### 内容创作团队

```python
from crewai import Agent, Task, Crew

# 创建研究员
researcher = Agent(
    role='内容研究员',
    goal='研究主题并收集相关资料',
    backstory='你是一位专业的内容研究员'
)

# 创建作者
writer = Agent(
    role='内容作者',
    goal='根据研究结果撰写高质量文章',
    backstory='你是一位经验丰富的内容创作者'
)

# 创建编辑
editor = Agent(
    role='内容编辑',
    goal='审核并优化文章质量',
    backstory='你是一位严谨的内容编辑'
)

# 定义任务
research_task = Task(
    description='研究关于 AI 的最新趋势',
    agent=researcher
)

write_task = Task(
    description='根据研究结果撰写一篇文章',
    agent=writer
)

edit_task = Task(
    description='审核并优化文章',
    agent=editor
)

# 创建团队
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential
)

result = crew.kickoff()
```

### 数据分析团队

```python
data_collector = Agent(
    role='数据收集员',
    goal='从各种来源收集数据',
    tools=[api_tool, database_tool]
)

data_analyst = Agent(
    role='数据分析师',
    goal='分析数据并提取洞察',
    tools=[pandas_tool, visualization_tool]
)

report_writer = Agent(
    role='报告撰写员',
    goal='生成数据分析报告',
    tools=[document_tool]
)
```

## 与其他框架对比

### CrewAI vs LangChain

- **CrewAI**：专注于多智能体协作，提供角色化的 Agent 系统
- **LangChain**：更通用的 LLM 应用框架，提供链式调用和更多工具

### CrewAI vs AutoGPT

- **CrewAI**：结构化的多智能体框架，有明确的角色和任务分工
- **AutoGPT**：自主 Agent 系统，更注重 Agent 的自主决策能力

## 安装和快速开始

### 安装

```bash
pip install crewai
pip install 'crewai[tools]'  # 安装额外工具
```

### 快速示例

```python
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

# 创建工具
search_tool = SerperDevTool()

# 创建 Agent
agent = Agent(
    role='研究助手',
    goal='帮助用户研究问题',
    backstory='你是一位乐于助人的研究助手',
    tools=[search_tool],
    verbose=True
)

# 创建任务
task = Task(
    description='研究 Python 3.12 的新特性',
    agent=agent,
    expected_output='详细的特性列表和说明'
)

# 创建团队并执行
crew = Crew(
    agents=[agent],
    tasks=[task]
)

result = crew.kickoff()
print(result)
```

## 最佳实践

### 1. 明确的角色定义

为每个 Agent 设计清晰的角色和职责，避免角色重叠：

```python
# 好的做法
researcher = Agent(role='研究员', goal='收集信息')
analyst = Agent(role='分析师', goal='分析数据')
writer = Agent(role='作者', goal='撰写内容')
```

### 2. 详细的任务描述

提供清晰、具体的任务描述和期望输出：

```python
task = Task(
    description='''
    请研究以下主题：
    1. 定义和核心概念
    2. 实际应用案例
    3. 优缺点分析
    ''',
    expected_output='一份包含以上三部分的详细报告'
)
```

### 3. 合理使用工具

根据任务需求选择合适的工具，避免给 Agent 提供不必要的工具：

```python
# 研究员只需要搜索工具
researcher = Agent(
    role='研究员',
    tools=[search_tool]  # 只提供搜索工具
)

# 数据分析师需要数据处理工具
analyst = Agent(
    role='分析师',
    tools=[pandas_tool, sql_tool]  # 提供数据处理工具
)
```

### 4. 启用记忆功能

对于需要上下文的任务，启用记忆功能：

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,
    cache=True  # 启用缓存以提高性能
)
```

## 高级特性

### 自定义工具

```python
from crewai_tools import BaseTool

class CustomSearchTool(BaseTool):
    name: str = "自定义搜索工具"
    description: str = "用于执行特定搜索的工具"
    
    def _run(self, query: str) -> str:
        # 实现自定义搜索逻辑
        return f"搜索结果：{query}"

custom_tool = CustomSearchTool()
agent = Agent(role='研究员', tools=[custom_tool])
```

### 回调函数

```python
def task_callback(output):
    print(f"任务完成：{output}")

task = Task(
    description='执行研究',
    agent=agent,
    callback=task_callback
)
```

### 异步执行

```python
import asyncio

async def run_crew():
    result = await crew.kickoff_async()
    return result

result = asyncio.run(run_crew())
```

## 注意事项

1. **API 成本**：CrewAI 依赖 LLM API 调用，多个 Agent 协作会增加 API 使用成本
1. **执行时间**：多 Agent 协作需要更多时间，特别是顺序执行模式
1. **提示词设计**：Agent 的表现很大程度取决于角色定义和任务描述的质量
1. **工具选择**：合理选择和配置工具，避免给 Agent 过多不必要的工具

## 资源链接

- 官方网站：https://www.crewai.com
- 官方文档：https://docs.crewai.com
- GitHub 仓库：https://github.com/joaomdmoura/crewAI
- 社区讨论：https://discord.gg/crewai

## 小结

CrewAI 提供了一个强大而灵活的框架，用于构建协作式 AI 智能体系统。通过角色化的设计和清晰的任务分工，CrewAI 使得复杂的多步骤任务可以被有效地分解和执行。无论是内容创作、数据分析还是自动化工作流，CrewAI 都能提供简洁的解决方案。
