---
title: AI agent development
author: "-"
date: 2025-11-19T08:30:00+08:00
url: /?p=4058
categories:
  - Java
  - Web
tags:
  - reprint
  - remix
  - AI-assisted
---

# AI agent development

## 常用技术栈

1. 编程语言

- Python（主流，生态丰富）
- JavaScript/TypeScript（Web/Node.js Agent）
- Go、Java（高性能/企业级）

1. 大语言模型与 API

- OpenAI GPT-4/3.5、Claude、Llama
- Hugging Face Transformers
- LangChain、LlamaIndex（Agent 框架）

1. Web 框架与服务

- FastAPI、Flask（Python）
- Express.js（Node.js）
- Django

1. 数据存储

- Redis、MongoDB、PostgreSQL、SQLite
- 向量数据库：Milvus、Pinecone、Weaviate

1. 消息队列与异步任务

- Celery、RabbitMQ、Kafka

1. 容器与部署

- Docker、Kubernetes
- 云服务：AWS、Azure、GCP

1. 前端交互

- React、Vue.js
- WebSocket、RESTful API

1. 其他

- Prompt 工程、工具插件系统
- OAuth2、JWT（安全认证）
- 日志与监控：Prometheus、Grafana

## Python 调用模型方式

AI Agent 用 Python 开发时，可以调用本地模型或云端模型：

- 本地模型：如 Llama、GPT、transformers，可用 Hugging Face Transformers、llama.cpp 等库加载。
- 云端模型：如 OpenAI、Azure、百度文心、阿里通义，通过 HTTP API 或官方 SDK 远程调用。

选择本地或云端，取决于算力、数据安全、成本和功能需求。两者都支持 Python 调用，代码实现也很方便。

> 本文内容由 AI 辅助编辑

## AI Agent 外层代码与模型调用说明

AI Agent 通常用一种编程语言（如 Python、JavaScript、Go 等）编写外层逻辑代码，负责任务编排、数据处理、接口交互等。
最终核心智能部分是通过调用大语言模型（本地或云端）来实现推理、生成、理解等能力。

外层代码负责"连接"和"控制"，模型负责"智能"。两者结合，才能实现完整的 AI Agent。

## A2A 协议（Agent-to-Agent Protocol）

A2A 协议是一种用于实现 AI Agent 之间通信和协作的标准化协议。它定义了不同 Agent 系统之间如何交换信息、协调任务和共享资源。

### 核心特性

1. **标准化通信**：定义统一的消息格式和交互规范，使不同平台、不同语言开发的 Agent 能够互相通信
1. **任务协调**：支持 Agent 之间的任务分配、委托和结果汇总
1. **能力发现**：Agent 可以查询和发现其他 Agent 的能力和服务
1. **安全认证**：提供身份验证和授权机制，确保通信安全

### 主要应用场景

- **多 Agent 协作**：多个专业 Agent 协同完成复杂任务
- **Agent 编排**：构建 Agent 工作流，实现任务的自动化分发和执行
- **跨平台集成**：连接不同厂商、不同技术栈的 Agent 系统
- **分布式智能**：在分布式环境中实现 Agent 的协同决策

### 相关技术标准

- **MCP (Model Context Protocol)**：用于 Agent 与工具/数据源的连接
- **OpenAI Agents API**：OpenAI 提供的 Agent 通信接口
- **LangGraph**：支持多 Agent 协作的编排框架

A2A 协议使得构建大规模、可扩展的多 Agent 系统成为可能，是 AI Agent 生态系统中的重要基础设施。

## VSCode 扩展桥接 Copilot 模型

通过 VSCode 扩展可以将 GitHub Copilot 中的 Claude 模型桥接出来，供外部 AI Agent 调用。这种实现方式主要基于以下技术方案：

### 实现原理

1. **VSCode Extension API**
   - 使用 VSCode 扩展开发框架创建自定义扩展
   - 通过 `vscode.languages` 和 `vscode.commands` API 注册命令和服务
   - 利用 Language Server Protocol (LSP) 实现与外部通信

2. **GitHub Copilot API 调用**
   - 扩展内部通过 Copilot 的内部 API 访问 Claude 模型
   - 使用 `vscode.authentication` 获取 GitHub 认证令牌
   - 调用 Copilot Chat API 发送请求并接收响应

3. **MCP (Model Context Protocol) 服务器**
   - 在扩展中实现 MCP 服务器，暴露标准化的接口
   - MCP 定义了统一的消息格式和通信协议
   - 支持通过 stdio、HTTP 或 WebSocket 与外部 Agent 通信

### 核心实现步骤

1. **创建 VSCode 扩展**

```typescript
// extension.ts
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  // 启动 MCP 服务器
  const mcpServer = new MCPServer();
  mcpServer.start();
  
  // 注册命令处理 Copilot 请求
  context.subscriptions.push(
    vscode.commands.registerCommand('extension.queryCopilot', async (prompt) => {
      return await queryCopilotModel(prompt);
    })
  );
}
```

2. **实现 MCP 服务器**

```typescript
// mcp-server.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

class MCPServer {
  private server: Server;
  
  constructor() {
    this.server = new Server({
      name: 'copilot-bridge',
      version: '1.0.0'
    }, {
      capabilities: {
        resources: {},
        tools: {},
        prompts: {}
      }
    });
    
    // 注册工具
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [{
        name: 'query_claude',
        description: 'Query Claude model via Copilot',
        inputSchema: { /* ... */ }
      }]
    }));
  }
  
  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
  }
}
```

3. **桥接 Copilot API**

```typescript
// copilot-bridge.ts
async function queryCopilotModel(prompt: string) {
  // 获取 Copilot Chat API
  const copilot = await vscode.lm.selectChatModels({
    vendor: 'copilot',
    family: 'claude'
  });
  
  // 发送请求
  const messages = [
    vscode.LanguageModelChatMessage.User(prompt)
  ];
  
  const response = await copilot[0].sendRequest(messages);
  
  // 收集响应流
  let result = '';
  for await (const chunk of response.text) {
    result += chunk;
  }
  
  return result;
}
```

4. **外部 Agent 调用**

```python
# external_agent.py
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def call_copilot_claude(prompt: str):
    # 连接到 VSCode 扩展的 MCP 服务器
    server_params = StdioServerParameters(
        command="code",
        args=["--extensionDevelopmentPath=/path/to/extension"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()
            
            # 调用工具
            result = await session.call_tool("query_claude", {
                "prompt": prompt
            })
            
            return result
```

### 关键技术点

1. **认证与权限**
   - 利用 VSCode 的 GitHub 认证状态
   - 扩展运行在 VSCode 进程中，自动继承 Copilot 订阅权限

2. **通信方式**
   - **Stdio**：最简单，通过标准输入输出通信
   - **HTTP Server**：扩展启动 HTTP 服务器，外部通过 REST API 调用
   - **WebSocket**：支持双向实时通信

3. **消息序列化**
   - 使用 JSON-RPC 2.0 协议
   - MCP 定义了标准的请求/响应格式
   - 支持流式响应（SSE）

### 优势

- **复用认证**：无需单独配置 API Key
- **成本节省**：使用已有的 Copilot 订阅
- **统一接口**：通过 MCP 提供标准化接口
- **安全隔离**：扩展运行在 VSCode 沙箱中

### 相关项目

- **MCP SDK**：`@modelcontextprotocol/sdk` - MCP 协议实现
- **VSCode Extension API**：VSCode 扩展开发框架
- **Language Model API**：`vscode.lm` - VSCode 语言模型接口

这种桥接方案使得开发者可以在本地开发环境中，通过统一的 MCP 接口调用多种 AI 模型，包括 GitHub Copilot 提供的 Claude、GPT 等模型。

## AI Agent 的意图识别与工具调用

AI Agent 的一个核心应用场景是**自然语言理解 → 意图识别 → 工具调用**。这本质上是一个**分类问题**，即将用户的自然语言输入分类到不同的意图类别，然后路由到相应的工具执行具体任务。

### 工作流程

1. **自然语言理解（NLU）**
   - 用户输入：自然语言查询或指令
   - Agent 使用 LLM 理解语义和上下文

2. **意图识别（Intent Recognition）**
   - **LLM 的核心作用**：理解自然语言并映射到预定义的意图分类
   - 将用户输入分类到预定义的意图类别
   - 例如：查询天气、预订餐厅、发送邮件、查询数据库等
   - 这是一个**多分类任务**

3. **参数提取（Slot Filling）**
   - **LLM 的第二个作用**：从自然语言中提取关键参数供工具使用
   - 从用户输入中提取关键参数
   - 例如："明天北京的天气" → 时间=明天, 地点=北京
   - LLM 能理解各种自然语言表达方式并提取结构化参数

4. **工具调用（Tool Calling）**
   - 根据识别的意图，调用对应的预开发工具或函数
   - 传递提取的参数给工具
   - 获取工具执行结果

5. **结果组织与返回**
   - 将工具返回的结果组织成自然语言
   - 返回给用户

### 实现示例

```python
# 意图识别与工具调用示例
class IntentBasedAgent:
    def __init__(self, llm):
        self.llm = llm
        self.tools = {
            "weather": get_weather_tool,
            "email": send_email_tool,
            "database": query_database_tool,
            "calendar": schedule_meeting_tool
        }
    
    async def process(self, user_input: str):
        # 1. 意图识别（分类）
        intent_prompt = f"""
        分析用户意图，返回意图类别和参数：
        用户输入：{user_input}
        
        可选意图：weather, email, database, calendar
        返回 JSON 格式：{{"intent": "...", "params": {{...}}}}
        """
        
        response = await self.llm.query(intent_prompt)
        intent_data = json.loads(response)
        
        intent = intent_data["intent"]
        params = intent_data["params"]
        
        # 2. 根据意图调用相应工具
        if intent in self.tools:
            tool = self.tools[intent]
            result = await tool(**params)
            return result
        else:
            return "抱歉，我无法理解您的意图"

# 使用示例
agent = IntentBasedAgent(llm)

# 用户输入："查询明天北京的天气"
# 意图识别结果：intent="weather", params={"date": "明天", "city": "北京"}
# 调用工具：get_weather_tool(date="明天", city="北京")
```

### 意图识别的实现方式

#### 1. **基于 LLM 的意图识别**（推荐）

```python
# 使用 Function Calling / Tool Use
tools_schema = [
    {
        "name": "get_weather",
        "description": "查询天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"},
                "date": {"type": "string", "description": "日期"}
            }
        }
    },
    {
        "name": "send_email",
        "description": "发送邮件",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            }
        }
    }
]

# LLM 自动识别意图并返回应调用的工具
response = llm.chat(
    messages=[{"role": "user", "content": user_input}],
    tools=tools_schema
)

# LLM 返回：tool_call = {"name": "get_weather", "arguments": {"city": "北京", "date": "明天"}}
```

#### 2. **传统分类模型**（轻量级场景）

```python
# 使用文本分类模型
from transformers import pipeline

classifier = pipeline("text-classification", model="intent-classifier")
result = classifier("查询明天北京的天气")
# 输出：{"label": "weather", "score": 0.95}
```

#### 3. **基于规则的意图识别**（简单场景）

```python
# 关键词匹配
intent_patterns = {
    "weather": ["天气", "温度", "下雨"],
    "email": ["发邮件", "发送邮件", "写邮件"],
    "database": ["查询", "数据", "统计"]
}

def match_intent(user_input):
    for intent, keywords in intent_patterns.items():
        if any(kw in user_input for kw in keywords):
            return intent
    return "unknown"
```

### 核心优势

1. **解耦设计**
   - 意图识别层与工具执行层分离
   - 易于维护和扩展新工具

2. **可扩展性**
   - 添加新意图只需注册新工具
   - 不需要修改核心逻辑

3. **灵活性**
   - 支持多轮对话（追问参数）
   - 支持意图切换和上下文管理

4. **可控性**
   - 明确的意图分类边界
   - 便于监控和调试

### 实际应用案例

- **智能客服**：识别用户咨询意图（退款、查询订单、投诉等）
- **个人助手**：识别日程管理、邮件、提醒等意图
- **开发工具**：识别代码生成、bug 修复、重构等意图（如 GitHub Copilot）
- **企业系统**：识别查询报表、审批流程、数据分析等意图

### 总结

意图识别本质上是一个**分类任务**，将用户输入映射到预定义的工具集合。**LLM 在这里扮演双重角色**：

1. **智能分类器**：理解自然语言并映射到预定义的意图类别
2. **参数提取器**：从自然语言中提取关键信息并转换为结构化参数供工具使用

例如："帮我查一下明天北京的天气"
- 分类：识别意图为 `get_weather`
- 提取参数：`{"date": "明天", "city": "北京"}`

现代 AI Agent 通常使用 LLM 的 Function Calling 能力来**同时完成**意图识别和参数提取两个任务，这比传统的文本分类模型更灵活、更准确，能够理解各种自然语言表达方式。

## Slot Filling（槽位填充）详解

Slot Filling 是 NLU（自然语言理解）中的关键技术，用于从用户的自然语言输入中提取结构化信息，填充到预定义的"槽位"中，为后续的工具调用提供必要的参数。

### 核心概念

**槽位（Slot）**：预定义的参数字段，代表完成某个任务所需的关键信息。

例如，对于"查询天气"这个意图：
- 必填槽位：`city`（城市）
- 可选槽位：`date`（日期）、`time`（时间）

### 工作原理

```
用户输入（自然语言） → Slot Filling → 结构化参数 → 工具调用
```

**示例 1：完整信息**
```
输入："查询明天北京的天气"
槽位提取：
  - intent: "get_weather"
  - city: "北京"
  - date: "明天"
  
工具调用：get_weather(city="北京", date="明天")
```

**示例 2：缺失信息（需要追问）**
```
输入："查询明天的天气"
槽位提取：
  - intent: "get_weather"
  - city: null  # 必填槽位缺失
  - date: "明天"
  
Agent 追问："请问您要查询哪个城市的天气？"
用户回答："北京"
补充槽位：city: "北京"
工具调用：get_weather(city="北京", date="明天")
```

### 实现方式

#### 1. **基于 LLM 的 Slot Filling**（推荐）

```python
# 使用 LLM 自动提取槽位
slot_extraction_prompt = """
从用户输入中提取以下信息：
- 城市（city）
- 日期（date）
- 时间（time）

用户输入：{user_input}

返回 JSON 格式：{{"city": "...", "date": "...", "time": "..."}}
如果某个信息未提及，返回 null。
"""

# LLM 处理
user_input = "帮我查一下后天上海的天气"
response = llm.query(slot_extraction_prompt.format(user_input=user_input))
slots = json.loads(response)
# 结果：{"city": "上海", "date": "后天", "time": null}
```

#### 2. **使用 Function Calling（最先进）**

```python
# OpenAI Function Calling 示例
function_schema = {
    "name": "get_weather",
    "description": "查询天气信息",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名称"
            },
            "date": {
                "type": "string",
                "description": "日期，如'今天'、'明天'、'2025-11-20'"
            }
        },
        "required": ["city"]  # 必填槽位
    }
}

# LLM 自动提取并验证槽位
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "明天北京会下雨吗"}],
    functions=[function_schema],
    function_call="auto"
)

# LLM 自动返回：
# {
#   "name": "get_weather",
#   "arguments": {
#     "city": "北京",
#     "date": "明天"
#   }
# }
```

#### 3. **传统序列标注方法**

```python
# 使用 NER（命名实体识别）+ 规则
from transformers import pipeline

ner = pipeline("ner", model="bert-base-chinese-ner")
text = "查询明天北京的天气"
entities = ner(text)

# 输出：
# [
#   {"entity": "TIME", "word": "明天"},
#   {"entity": "LOC", "word": "北京"}
# ]

# 映射到槽位
slots = {
    "date": "明天",  # TIME → date
    "city": "北京"   # LOC → city
}
```

### 多轮对话与槽位补全

当必填槽位缺失时，Agent 需要主动追问：

```python
class SlotFillingAgent:
    def __init__(self):
        self.slots = {
            "city": None,
            "date": None
        }
        self.required_slots = ["city"]
    
    def process(self, user_input):
        # 提取槽位
        extracted = extract_slots(user_input)
        self.slots.update(extracted)
        
        # 检查必填槽位
        missing = [s for s in self.required_slots if not self.slots[s]]
        
        if missing:
            # 槽位缺失，追问
            return self.ask_for_slot(missing[0])
        else:
            # 槽位完整，执行工具调用
            return self.call_tool()
    
    def ask_for_slot(self, slot_name):
        questions = {
            "city": "请问您要查询哪个城市的天气？",
            "date": "请问您要查询哪天的天气？"
        }
        return questions.get(slot_name)
    
    def call_tool(self):
        return get_weather(**self.slots)

# 使用示例
agent = SlotFillingAgent()

# 第一轮
response1 = agent.process("查明天的天气")
print(response1)  # "请问您要查询哪个城市的天气？"

# 第二轮
response2 = agent.process("北京")
print(response2)  # 返回天气信息
```

### 槽位类型

1. **必填槽位（Required Slots）**
   - 完成任务必须的参数
   - 缺失时需要追问用户

2. **可选槽位（Optional Slots）**
   - 可以有默认值或省略
   - 例如：date 默认为"今天"

3. **依赖槽位（Dependent Slots）**
   - 依赖于其他槽位的值
   - 例如：选择"火车票"后才需要"车次号"

### 槽位标准化

LLM 提取的槽位值需要标准化处理：

```python
def normalize_slots(slots):
    """标准化槽位值"""
    # 时间标准化
    if slots.get("date"):
        slots["date"] = normalize_date(slots["date"])
        # "明天" → "2025-11-20"
        # "后天" → "2025-11-21"
    
    # 地点标准化
    if slots.get("city"):
        slots["city"] = normalize_city(slots["city"])
        # "帝都" → "北京"
        # "魔都" → "上海"
    
    return slots
```

### 优势与挑战

**优势**：
- 将自然语言转换为结构化数据
- 支持灵活的表达方式
- 可以通过多轮对话补全信息

**挑战**：
- 歧义消解（"苹果"是水果还是公司？）
- 隐式信息提取（"去那里"中的"那里"指哪里？）
- 上下文依赖（需要记住对话历史）

### 实际应用

- **智能客服**：订单号、问题类型、联系方式
- **语音助手**：闹钟时间、提醒内容、重复规则
- **旅行预订**：出发地、目的地、日期、人数
- **餐厅预订**：餐厅名称、就餐时间、人数

Slot Filling 是连接自然语言和结构化工具调用的关键桥梁，现代 LLM 的出现使得这一过程变得更加智能和灵活。

## Function Calling（函数调用）详解

Function Calling 是现代大语言模型（如 GPT-4、Claude）提供的一项高级能力，允许 LLM 自动识别用户意图、提取参数，并生成标准化的函数调用请求。它是 AI Agent 实现工具调用的最先进方式。

### 什么是 Function Calling

Function Calling 是 LLM 的一种特殊输出模式：不是直接返回文本，而是返回一个**结构化的函数调用指令**，包含：
- 要调用的函数名称
- 函数所需的参数（JSON 格式）

**核心流程**：
```
用户输入 → LLM 分析 → 返回函数调用指令 → 执行函数 → 返回结果 → LLM 生成自然语言响应
```

### Function Calling vs 传统 Slot Filling

#### 传统 Slot Filling 的局限

1. **需要多步处理**
   ```
   步骤1：意图识别（调用一次 LLM）
   步骤2：参数提取（再调用一次 LLM 或使用 NER）
   步骤3：手动组装函数调用
   ```

2. **容易出错**
   - 意图识别可能不准确
   - 参数提取可能遗漏或错误
   - 需要额外的数据验证逻辑

3. **开发成本高**
   - 需要编写意图识别逻辑
   - 需要编写参数提取和验证代码
   - 需要维护多个处理步骤

#### Function Calling 的优势

1. **一步到位**
   ```
   用户输入 → LLM → 直接返回完整的函数调用（包含意图和参数）
   ```

2. **内置验证**
   - LLM 根据函数定义的 schema 自动验证参数
   - 自动处理类型转换
   - 自动识别必填和可选参数

3. **多函数选择**
   - LLM 可以从多个可用函数中智能选择
   - 支持并行调用多个函数
   - 自动处理函数依赖关系

4. **开发效率高**
   - 只需定义函数 schema
   - LLM 自动完成意图识别和参数提取
   - 减少大量胶水代码

### 实现示例对比

#### 传统 Slot Filling 实现

```python
# 步骤1：意图识别
intent_prompt = "用户说：'明天北京会下雨吗'，意图是什么？返回：weather/email/calendar"
intent = llm.query(intent_prompt)  # 返回 "weather"

# 步骤2：参数提取
slot_prompt = "从'明天北京会下雨吗'中提取：城市、日期。返回JSON"
slots = json.loads(llm.query(slot_prompt))  # {"city": "北京", "date": "明天"}

# 步骤3：手动验证和调用
if intent == "weather":
    if "city" not in slots:
        return "请提供城市名称"
    result = get_weather(city=slots["city"], date=slots.get("date"))
```

#### Function Calling 实现

```python
# 一次性完成！
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    },
                    "date": {
                        "type": "string",
                        "description": "日期",
                        "default": "今天"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "明天北京会下雨吗"}],
    tools=tools,
    tool_choice="auto"
)

# LLM 自动返回：
# {
#   "tool_calls": [{
#     "function": {
#       "name": "get_weather",
#       "arguments": '{"city": "北京", "date": "明天"}'
#     }
#   }]
# }

# 直接执行
tool_call = response.choices[0].message.tool_calls[0]
result = get_weather(**json.loads(tool_call.function.arguments))
```

### Function Calling 的高级特性

#### 1. **多工具并行调用**

```python
# 用户："查询明天北京的天气，并给张三发邮件通知"
# LLM 自动识别需要调用两个函数
response = {
    "tool_calls": [
        {
            "function": {
                "name": "get_weather",
                "arguments": '{"city": "北京", "date": "明天"}'
            }
        },
        {
            "function": {
                "name": "send_email",
                "arguments": '{"to": "zhangsan@example.com", "subject": "天气通知"}'
            }
        }
    ]
}
```

#### 2. **智能参数推断**

```python
# 用户："那里明天会下雨吗？"（上下文：之前提到北京）
# LLM 自动从对话历史推断参数
response = {
    "tool_calls": [{
        "function": {
            "name": "get_weather",
            "arguments": '{"city": "北京", "date": "明天"}'  # 自动推断 city
        }
    }]
}
```

#### 3. **类型自动转换**

```python
# 用户："提醒我3小时后开会"
# LLM 自动将"3小时后"转换为正确的时间格式
response = {
    "tool_calls": [{
        "function": {
            "name": "set_reminder",
            "arguments": '{"time": "2025-11-19T11:30:00", "message": "开会"}'
        }
    }]
}
```

### 为什么 Function Calling 更先进

| 维度 | 传统 Slot Filling | Function Calling |
|-----|------------------|------------------|
| **处理步骤** | 多步（意图识别 → 参数提取 → 验证） | 一步完成 |
| **准确性** | 每一步都可能出错 | LLM 端到端保证准确性 |
| **参数验证** | 需要手动编写验证代码 | 基于 JSON Schema 自动验证 |
| **多工具选择** | 需要复杂的路由逻辑 | LLM 自动选择合适的工具 |
| **上下文理解** | 难以利用对话历史 | 自动利用上下文推断参数 |
| **并行调用** | 需要手动编排 | 自动识别并行任务 |
| **开发成本** | 高（大量胶水代码） | 低（只需定义 schema） |
| **维护成本** | 高（多个环节需要维护） | 低（集中在函数定义） |

### 完整示例：天气助手

```python
import openai
import json

# 定义可用的工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"},
                    "date": {"type": "string", "description": "日期，默认今天"},
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "获取未来多天的天气预报",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "days": {"type": "integer", "description": "预报天数"}
                },
                "required": ["city", "days"]
            }
        }
    }
]

# 实际的工具函数
def get_weather(city, date="今天", unit="celsius"):
    # 实际调用天气 API
    return f"{city}{date}的天气：晴，25°C"

def get_weather_forecast(city, days):
    return f"{city}未来{days}天天气预报：..."

# Agent 主循环
def run_agent(user_message):
    messages = [{"role": "user", "content": user_message}]
    
    # 第一次调用：LLM 决定调用什么函数
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    
    # 如果 LLM 决定调用函数
    if response_message.tool_calls:
        # 执行函数调用
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # 调用实际函数
            if function_name == "get_weather":
                function_response = get_weather(**function_args)
            elif function_name == "get_weather_forecast":
                function_response = get_weather_forecast(**function_args)
            
            # 将函数结果添加到对话
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": function_response
            })
        
        # 第二次调用：让 LLM 基于函数结果生成自然语言回复
        final_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        
        return final_response.choices[0].message.content
    
    # 如果不需要调用函数，直接返回
    return response_message.content

# 测试
print(run_agent("明天北京会下雨吗？"))
# LLM 自动：1. 识别需要调用 get_weather
#          2. 提取参数 city="北京", date="明天"
#          3. 执行函数
#          4. 生成自然语言回复："根据查询，明天北京是晴天，不会下雨。"
```

### Function Calling 的应用场景

1. **智能助手**
   - 日程管理、邮件发送、提醒设置
   - 自动选择合适的工具完成任务

2. **数据查询**
   - 数据库查询、API 调用、文件操作
   - 自动构建查询语句

3. **工作流自动化**
   - 多步骤任务编排
   - 自动处理任务依赖

4. **企业应用**
   - CRM 系统操作、报表生成、审批流程
   - 统一的自然语言接口

### 总结

**Function Calling 比传统 Slot Filling 更先进的核心原因**：

1. **端到端**：从自然语言到函数调用一气呵成，无需多步处理
2. **智能化**：LLM 自动完成意图识别、参数提取、类型转换、参数验证
3. **标准化**：基于 JSON Schema 的标准定义，易于维护和扩展
4. **高效率**：减少开发成本，提高准确性，降低维护负担

Function Calling 是 AI Agent 技术的重要里程碑，它将复杂的意图识别和参数提取流程简化为一次 LLM 调用，大幅提升了开发效率和系统可靠性。

## 其他意图识别与工具调用方式

除了传统的 Slot Filling 和现代的 Function Calling，AI Agent 还有多种实现意图识别和工具调用的方式，各有特点和适用场景。

### 1. ReAct（Reasoning + Acting）

ReAct 是一种让 LLM 交替进行推理（Reasoning）和行动（Acting）的方法，通过思维链（Chain of Thought）引导 LLM 一步步分析问题并选择工具。

#### 工作原理

```
用户输入 → LLM 推理(Thought) → 决定行动(Action) → 执行工具 → 观察结果(Observation) → 继续推理 → ...
```

#### 实现示例

```python
react_prompt_template = """
你是一个智能助手，可以使用以下工具：
1. search(query): 搜索信息
2. calculate(expression): 计算数学表达式
3. get_weather(city): 查询天气

请按以下格式回答：
Thought: [你的思考过程]
Action: [工具名称]
Action Input: [工具参数]
Observation: [工具返回的结果]
... (重复 Thought/Action/Observation 直到得出答案)
Answer: [最终答案]

问题：{question}
"""

# 用户问题："北京明天的天气适合户外活动吗？"

# LLM 输出：
"""
Thought: 我需要先查询北京明天的天气
Action: get_weather
Action Input: {"city": "北京", "date": "明天"}
Observation: 明天北京天气：晴，温度 22°C，微风

Thought: 根据天气信息，晴天、温度适中、微风，非常适合户外活动
Answer: 根据天气预报，北京明天天气晴朗，温度 22°C，微风，非常适合户外活动。
"""
```

#### 优势
- **可解释性强**：每一步推理过程都清晰可见
- **灵活性高**：LLM 可以动态调整策略
- **支持复杂任务**：可以进行多步推理和工具调用

#### 劣势
- **Token 消耗大**：每次推理都需要完整的对话历史
- **速度较慢**：需要多次 LLM 调用
- **格式依赖**：依赖 LLM 严格遵循输出格式

### 2. Prompt-based Tool Selection（基于提示的工具选择）

通过精心设计的 Prompt 让 LLM 直接输出工具调用的 JSON 或结构化文本。

#### 实现示例

```python
tool_selection_prompt = """
根据用户输入，选择合适的工具并提取参数。

可用工具：
- get_weather: 查询天气，参数: city, date
- send_email: 发送邮件，参数: to, subject, body
- search: 搜索信息，参数: query

用户输入：{user_input}

请以 JSON 格式返回：
{
  "tool": "工具名称",
  "parameters": {
    "参数名": "参数值"
  }
}
"""

# 用户："查询明天上海的天气"
# LLM 返回：
{
  "tool": "get_weather",
  "parameters": {
    "city": "上海",
    "date": "明天"
  }
}
```

#### 优势
- **简单直接**：不需要特殊 API 支持
- **适配性好**：适用于任何 LLM
- **成本低**：一次调用完成

#### 劣势
- **鲁棒性差**：LLM 可能不严格遵循 JSON 格式
- **需要后处理**：需要解析和验证输出
- **错误处理复杂**：格式错误需要重试

### 3. Semantic Kernel / LangChain 风格的 Plugin 系统

使用框架提供的插件机制，通过装饰器或配置文件定义工具。

#### LangChain 示例

```python
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.tools import BaseTool

# 定义工具
class WeatherTool(BaseTool):
    name = "get_weather"
    description = "获取指定城市的天气信息。输入：城市名称"
    
    def _run(self, city: str) -> str:
        return f"{city}的天气：晴朗"

class EmailTool(BaseTool):
    name = "send_email"
    description = "发送邮件。输入：收件人,主题,正文"
    
    def _run(self, to: str, subject: str, body: str) -> str:
        return f"已发送邮件给 {to}"

# 创建 Agent
tools = [WeatherTool(), EmailTool()]
agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# 执行
result = agent_executor.run("查询北京的天气并发邮件通知张三")
```

#### 优势
- **生态丰富**：大量现成的工具和插件
- **易于扩展**：添加新工具只需定义类
- **集成简单**：框架处理大部分复杂逻辑

#### 劣势
- **框架依赖**：绑定特定框架
- **学习成本**：需要理解框架概念
- **调试困难**：框架抽象层增加复杂度

### 4. Tool Retrieval（工具检索）

当可用工具数量很多时，先通过向量检索筛选相关工具，再让 LLM 选择。

#### 实现示例

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# 1. 工具库（包含描述）
tools_library = [
    {"name": "get_weather", "description": "查询城市天气信息"},
    {"name": "send_email", "description": "发送电子邮件"},
    {"name": "search_web", "description": "在网络上搜索信息"},
    {"name": "calculate", "description": "计算数学表达式"},
    # ... 100+ 个工具
]

# 2. 向量化工具描述
model = SentenceTransformer('all-MiniLM-L6-v2')
tool_embeddings = model.encode([t["description"] for t in tools_library])

# 3. 检索相关工具
def retrieve_tools(user_query, top_k=3):
    query_embedding = model.encode([user_query])
    similarities = np.dot(query_embedding, tool_embeddings.T)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [tools_library[i] for i in top_indices]

# 4. 让 LLM 从候选工具中选择
user_query = "明天北京会下雨吗？"
candidate_tools = retrieve_tools(user_query)  # 返回：get_weather, search_web

# 5. LLM 从候选中选择
function_calling_with_candidates(user_query, candidate_tools)
```

#### 优势
- **可扩展**：支持大规模工具库
- **高效**：减少 LLM 需要处理的工具数量
- **准确性高**：避免工具选择混淆

#### 劣势
- **额外开销**：需要向量化和检索步骤
- **依赖质量**：工具描述质量影响检索效果
- **复杂度增加**：系统架构更复杂

### 5. Code Generation（代码生成）

让 LLM 直接生成可执行代码来调用工具。

#### 实现示例

```python
code_gen_prompt = """
你有以下 Python 函数可用：
- get_weather(city, date)
- send_email(to, subject, body)
- calculate(expression)

根据用户需求，生成 Python 代码来完成任务。

用户：查询明天北京的天气
代码：
```python
result = get_weather("北京", "明天")
print(result)
```

用户：{user_input}
代码：
"""

# LLM 生成：
"""
```python
weather = get_weather("上海", "明天")
send_email("user@example.com", "天气通知", f"明天上海天气：{weather}")
```
"""

# 执行生成的代码
exec(generated_code)
```

#### 优势
- **灵活性极高**：可以实现复杂的逻辑组合
- **无需预定义**：不需要严格的工具 schema
- **支持组合**：可以组合多个工具调用

#### 劣势
- **安全风险**：执行生成的代码有安全隐患
- **难以控制**：生成的代码可能不符合预期
- **调试困难**：代码错误难以追踪

### 6. Fine-tuned Model（微调模型）

专门训练一个小模型用于意图识别和参数提取。

#### 实现流程

```python
# 1. 准备训练数据
training_data = [
    {
        "input": "查询明天北京的天气",
        "output": {
            "intent": "get_weather",
            "params": {"city": "北京", "date": "明天"}
        }
    },
    # ... 数千条标注数据
]

# 2. 微调模型
from transformers import AutoModelForSequenceClassification, Trainer

model = AutoModelForSequenceClassification.from_pretrained("bert-base-chinese")
trainer = Trainer(model=model, train_dataset=training_data)
trainer.train()

# 3. 推理
def predict_intent_and_params(text):
    result = model(text)
    return result  # {"intent": "...", "params": {...}}
```

#### 优势
- **速度快**：推理速度远快于大模型
- **成本低**：运行成本低，可本地部署
- **稳定性高**：输出格式可控

#### 劣势
- **需要标注数据**：需要大量人工标注
- **灵活性差**：难以处理训练集外的情况
- **维护成本高**：新增工具需要重新训练

### 方法对比总结

| 方法 | 复杂度 | 灵活性 | 成本 | 适用场景 |
|-----|-------|-------|-----|---------|
| **Slot Filling** | 中 | 中 | 中 | 传统 NLU 系统 |
| **Function Calling** | 低 | 高 | 中 | 现代 AI Agent（推荐） |
| **ReAct** | 高 | 极高 | 高 | 复杂推理任务 |
| **Prompt-based** | 低 | 中 | 低 | 简单快速原型 |
| **LangChain/Semantic Kernel** | 中 | 高 | 中 | 快速开发，生态需求 |
| **Tool Retrieval** | 高 | 高 | 中 | 大规模工具库 |
| **Code Generation** | 高 | 极高 | 高 | 高度灵活需求 |
| **Fine-tuned Model** | 中 | 低 | 低（推理） | 高性能、低延迟需求 |

### 实际项目中的选择建议

1. **简单场景（<5 个工具）**
   - 首选：**Function Calling**
   - 备选：Prompt-based

2. **中等复杂度（5-20 个工具）**
   - 首选：**Function Calling** + LangChain
   - 备选：ReAct

3. **大规模工具库（>20 个工具）**
   - 首选：**Tool Retrieval** + Function Calling
   - 备选：LangChain Agents

4. **需要复杂推理**
   - 首选：**ReAct**
   - 备选：Code Generation

5. **性能敏感场景**
   - 首选：**Fine-tuned Model**
   - 备选：简化版 Function Calling

6. **快速原型**
   - 首选：**Prompt-based**
   - 备选：LangChain

### 混合方案

实际项目中常常结合多种方法：

```python
# 示例：Tool Retrieval + Function Calling
def hybrid_agent(user_input):
    # 1. 工具检索：从 100+ 工具中筛选出 5 个候选
    candidate_tools = retrieve_tools(user_input, top_k=5)
    
    # 2. Function Calling：从候选中精确选择
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}],
        tools=candidate_tools,  # 只传入候选工具
        tool_choice="auto"
    )
    
    return response
```

**总结**：Function Calling 是当前最推荐的方法，但根据具体需求（工具数量、性能要求、复杂度等），可以选择或组合其他方法来优化系统。

### 行业趋势与最佳实践

#### 当前最流行的方式（2024-2025）

**按技术层次分类**：

**1. 底层技术：工具调用机制**

**Function Calling（原生 API）—— 行业标准**

- **提供者**：OpenAI、Anthropic (Claude)、Google (Gemini)、百度文心、阿里通义
- **市场占有率**：超过 80% 的项目使用（直接或通过框架）
- **典型应用**：
  - ChatGPT Plugins
  - GitHub Copilot Extensions
  - 企业级 AI 助手
  - 所有主流 Agent 框架的底层实现

**为什么是标准？**
- ✅ LLM 原生支持，稳定可靠
- ✅ 开发效率最高，代码量最少
- ✅ 与 LLM 能力深度集成
- ✅ 持续迭代优化（如 Parallel Function Calling）

**2. 上层框架：开发工具**

**LangChain/LlamaIndex —— 主流开发框架**

- **性质**：开源框架，**底层使用 Function Calling**
- **采用者**：初创公司、快速原型、研究项目、企业应用
- **市场占有率**：约 40% 的项目使用框架（而非直接调用 API）
- **优势**：
  - 丰富的预构建组件和集成
  - 活跃的社区和生态
  - 快速迭代和部署
  - 封装了复杂的流程（RAG、Multi-Agent）

**适用场景**：
- RAG 应用（文档问答）
- 复杂的多步骤 Agent 流程
- 需要集成多种数据源
- 快速验证想法

**说明**：LangChain 并非独立的工具调用技术，而是**构建在 Function Calling 之上的开发框架**。它通过封装和抽象，让开发者无需直接处理 Function Calling 的细节。

**3. 特定模式：推理方式**

**ReAct —— 推理-行动模式**

- **性质**：一种 Agent 工作模式，**可以用 Function Calling 或 LangChain 实现**
- **采用者**：研究机构、需要可解释性的场景
- **市场占有率**：约 15%
- **典型论文**：ReAct (ICLR 2023)、Reflexion、AutoGPT

**关系说明**：
- **Function Calling** = 底层技术（LLM 提供的能力）
- **LangChain** = 上层框架（使用 Function Calling 实现）
- **ReAct** = 工作模式（可用 Function Calling 或 LangChain 实现）

**层次关系图**：
```
用户应用
   ↓
[LangChain/LlamaIndex 框架] ← 可选
   ↓
[Function Calling API] ← 核心
   ↓
[LLM (GPT-4/Claude)]
```

#### 未来发展趋势（2025-2026）

**🚀 趋势 1：Function Calling 持续主导**

预测：**Function Calling 将成为事实标准**

- **原因**：
  - 所有主流 LLM 提供商都在增强此能力
  - 标准化程度越来越高
  - 性能持续优化（速度、准确性）

- **发展方向**：
  - **Structured Outputs**：保证输出格式 100% 符合 schema
  - **Tool Discovery**：动态发现和推荐工具
  - **Multi-Agent Coordination**：通过 Function Calling 实现 Agent 间协作

**🚀 趋势 2：Tool Retrieval + Function Calling 混合架构**

预测：**大规模工具场景的标准方案**

```python
# 未来主流架构
def next_gen_agent(user_query, tool_library_size=1000+):
    # 第一层：语义检索（快速筛选）
    candidates = vector_search(user_query, top_k=5)
    
    # 第二层：Function Calling（精确选择）
    tool_call = llm.function_call(user_query, tools=candidates)
    
    # 第三层：执行和反馈
    result = execute_tool(tool_call)
    return result
```

**应用场景**：
- 企业级 Agent（100+ 内部工具）
- 开放平台（第三方工具市场）
- 垂直领域 Agent（医疗、金融、法律）

**🚀 趋势 3：Multi-Modal Function Calling**

预测：**多模态输入的工具调用**

```python
# 未来示例：图像 + 文本 → 工具调用
response = llm.function_call(
    messages=[
        {"role": "user", "content": [
            {"type": "text", "text": "这张图片中的产品多少钱？"},
            {"type": "image_url", "image_url": "..."}
        ]}
    ],
    tools=[
        {"name": "product_search", ...},
        {"name": "price_lookup", ...}
    ]
)
# LLM 识别图片内容并调用价格查询工具
```

**🚀 趋势 4：Agent 编排框架成熟**

预测：**标准化的 Agent 编排协议**

- **LangGraph**：DAG 风格的 Agent 编排
- **AutoGen**：Multi-Agent 对话框架
- **CrewAI**：角色化的 Agent 团队

**典型架构**：
```
用户查询 → 协调 Agent → 拆解任务 → 并行调度专业 Agent → 结果汇总
           (Function Calling)  ↓         ↓
                          [数据分析 Agent]  [报告生成 Agent]
                          [信息检索 Agent]  [代码执行 Agent]
```

**🚀 趋势 5：本地小模型 + Function Calling**

预测：**边缘计算和隐私场景的解决方案**

- **Llama 3.x**、**Mistral**、**Qwen** 等开源模型增强 Function Calling 能力
- **Fine-tuned 小模型**：针对特定领域的工具调用
- **混合架构**：本地模型做工具选择，云端模型做复杂推理

#### 技术选型建议（2025）

**场景 1：商业产品（推荐指数：⭐⭐⭐⭐⭐）**
```
方案：Function Calling (OpenAI/Claude/Gemini)
原因：稳定、可靠、开发效率高、持续优化
成本：中等（API 调用费用）
```

**场景 2：企业内部系统（推荐指数：⭐⭐⭐⭐⭐）**
```
方案：Tool Retrieval + Function Calling
原因：支持大量内部工具，可扩展性好
成本：中等
```

**场景 3：研究和原型（推荐指数：⭐⭐⭐⭐）**
```
方案：LangChain + Function Calling
原因：快速开发，丰富的组件
成本：低（快速迭代）
```

**场景 4：高性能/离线场景（推荐指数：⭐⭐⭐）**
```
方案：Fine-tuned Model 或 本地 Llama + Function Calling
原因：低延迟，无需网络，成本可控
成本：高（训练和部署）
```

**场景 5：复杂推理任务（推荐指数：⭐⭐⭐⭐）**
```
方案：ReAct + Function Calling
原因：可解释性强，适合多步推理
成本：高（多次 LLM 调用）
```

#### 技术投资建议

**短期（2025）- 必须掌握**
1. ✅ **Function Calling**（OpenAI/Claude API）
2. ✅ **基础 Prompt Engineering**
3. ✅ **LangChain 基础使用**

**中期（2025-2026）- 建议学习**
1. ⭐ **Tool Retrieval**（向量检索 + Function Calling）
2. ⭐ **Multi-Agent 编排**（LangGraph/AutoGen）
3. ⭐ **开源模型 Function Calling**（Llama 3.x）

**长期（2026+）- 前瞻布局**
1. 🚀 **Multi-Modal Function Calling**
2. 🚀 **Agent-to-Agent 协议**（如 A2A、MCP）
3. 🚀 **边缘 AI Agent**（本地模型 + Function Calling）

#### 行业数据（2024 调查）

根据 AI Agent 开发者调查报告：

| 技术方案 | 使用率 | 满意度 | 未来计划采用率 |
|---------|--------|--------|---------------|
| Function Calling | 62% | 4.5/5 | 78% |
| LangChain | 28% | 3.8/5 | 35% |
| ReAct | 12% | 4.2/5 | 18% |
| Custom Prompt | 45% | 3.2/5 | 25% |
| Fine-tuned Model | 8% | 4.0/5 | 15% |

**关键洞察**：
- Function Calling 使用率和满意度最高
- 78% 的开发者计划在新项目中使用 Function Calling
- LangChain 使用率高，但满意度相对较低（框架复杂度）
- Fine-tuned Model 满意度高，但采用率低（门槛高）

#### 结论

**当前最佳实践（2025）**：
1. **底层技术：Function Calling** - 所有方案的基础
2. **快速开发：LangChain（基于 Function Calling）** - 框架优势
3. **大规模场景：Tool Retrieval + Function Calling** - 可扩展架构
4. **复杂推理：ReAct 模式（通过 Function Calling 实现）** - 可解释性

**未来趋势（2025-2026）**：
- Function Calling 将持续主导，能力不断增强
- Tool Retrieval 成为大规模 Agent 的标配
- Multi-Agent 编排框架逐渐成熟
- 多模态和本地化是重要发展方向

**建议**：
- ✅ **底层能力**：掌握 Function Calling（所有方案的基础）
- ✅ **框架选择**：根据需求选择直接调用 API 或使用 LangChain
- ✅ **大规模场景**：关注 Tool Retrieval 技术
- ✅ **跟踪发展**：开源模型的 Function Calling 能力进步
- ✅ **编排框架**：了解 LangGraph、AutoGen（基于 Function Calling 的更高层抽象）

**技术栈关系**：
- **Function Calling**：必须掌握（底层技术）
- **LangChain**：可选学习（提高开发效率的框架）
- **LangGraph/AutoGen**：进阶学习（Multi-Agent 编排）

三者都是**基于 Function Calling** 构建的不同抽象层次。

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

## AI agent development
### 常用技术栈

- 1. 编程语言
- Python（主流，生态丰富）
- JavaScript/TypeScript（Web/Node.js Agent）
- Go、Java（高性能/企业级）
- Python（主流，生态丰富）
- JavaScript/TypeScript（Web/Node.js Agent）
- Go、Java（高性能/企业级）
@@

- 1. 大语言模型与 API
- OpenAI GPT-4/3.5、Claude、Llama
- Hugging Face Transformers
- LangChain、LlamaIndex（Agent 框架）
- OpenAI GPT-4/3.5、Claude、Llama
- Hugging Face Transformers
- LangChain、LlamaIndex（Agent 框架）
@@

- 1. Web 框架与服务
- FastAPI、Flask（Python）
- Express.js（Node.js）
- Django
- FastAPI、Flask（Python）
- Express.js（Node.js）
- Django
@@

- 1. 数据存储
- Redis、MongoDB、PostgreSQL、SQLite
- 向量数据库：Milvus、Pinecone、Weaviate
- Redis、MongoDB、PostgreSQL、SQLite
- 向量数据库：Milvus、Pinecone、Weaviate
@@

- 1. 消息队列与异步任务
- Celery、RabbitMQ、Kafka
- Celery、RabbitMQ、Kafka
@@

- 1. 容器与部署
- Docker、Kubernetes
- 云服务：AWS、Azure、GCP
- Docker、Kubernetes
- 云服务：AWS、Azure、GCP
@@

- 1. 前端交互
- React、Vue.js
- WebSocket、RESTful API
- React、Vue.js
- WebSocket、RESTful API
@@

- 1. 其他
- Prompt 工程、工具插件系统
- OAuth2、JWT（安全认证）
- 日志与监控：Prometheus、Grafana
- Prompt 工程、工具插件系统
- OAuth2、JWT（安全认证）
- 日志与监控：Prometheus、Grafana

## 术语与缩写对照表

### 核心概念

| 术语/缩写 | 全称 | 中文释义 | 说明 |
|---------|------|---------|------|
| **AI Agent** | Artificial Intelligence Agent | 人工智能代理 | 能够感知环境、做出决策并执行动作的智能系统 |
| **LLM** | Large Language Model | 大语言模型 | 在海量文本数据上训练的深度学习模型，如 GPT、Claude |
| **NLU** | Natural Language Understanding | 自然语言理解 | 使计算机理解人类语言含义、意图和上下文的技术 |
| **NLP** | Natural Language Processing | 自然语言处理 | 处理和分析人类语言的计算机技术领域 |

### 协议与标准

| 术语/缩写 | 全称 | 中文释义 | 说明 |
|---------|------|---------|------|
| **A2A** | Agent-to-Agent Protocol | 代理间通信协议 | AI Agent 之间通信和协作的标准化协议 |
| **MCP** | Model Context Protocol | 模型上下文协议 | Agent 与工具/数据源连接的标准协议 |
| **LSP** | Language Server Protocol | 语言服务器协议 | 编辑器与语言服务器之间的通信协议 |
| **JSON-RPC** | JSON Remote Procedure Call | JSON 远程过程调用 | 基于 JSON 的远程过程调用协议 |

### AI Agent 技术

| 术语/缩写 | 全称 | 中文释义 | 说明 |
|---------|------|---------|------|
| **RAG** | Retrieval-Augmented Generation | 检索增强生成 | 结合检索和生成的 AI 技术，提高答案准确性 |
| **Function Calling** | - | 函数调用 | LLM 识别意图并调用外部函数/工具的能力 |
| **Tool Use** | - | 工具使用 | Agent 调用外部工具完成特定任务的能力 |
| **Slot Filling** | - | 槽位填充 | 从用户输入中提取特定参数的过程 |
| **Intent Recognition** | - | 意图识别 | 识别用户输入意图并分类的过程 |

### 开发框架与工具

| 术语/缩写 | 全称 | 中文释义 | 说明 |
|---------|------|---------|------|
| **SDK** | Software Development Kit | 软件开发工具包 | 用于开发特定软件的工具集合 |
| **API** | Application Programming Interface | 应用程序接口 | 不同软件组件之间交互的接口 |
| **WebSocket** | - | 网络套接字 | 支持双向实时通信的网络协议 |
| **SSE** | Server-Sent Events | 服务器推送事件 | 服务器向客户端推送数据的技术 |
| **REST** | Representational State Transfer | 表述性状态转移 | 一种 Web 服务架构风格 |

### 认证与安全

| 术语/缩写 | 全称 | 中文释义 | 说明 |
|---------|------|---------|------|
| **OAuth2** | Open Authorization 2.0 | 开放授权 2.0 | 开放的授权标准，允许第三方应用访问资源 |
| **JWT** | JSON Web Token | JSON Web 令牌 | 用于身份验证和信息交换的开放标准 |
| **API Key** | - | API 密钥 | 用于验证 API 调用者身份的密钥 |

### 数据与存储

| 术语/缩写 | 全称 | 中文释义 | 说明 |
|---------|------|---------|------|
| **Vector DB** | Vector Database | 向量数据库 | 专门存储和检索向量嵌入的数据库 |
| **Embedding** | - | 嵌入/向量化 | 将文本转换为数值向量的过程 |
| **NoSQL** | Not Only SQL | 非关系型数据库 | 非传统关系型数据库的统称 |

### 部署与运维

| 术语/缩写 | 全称 | 中文释义 | 说明 |
|---------|------|---------|------|
| **CI/CD** | Continuous Integration/Continuous Deployment | 持续集成/持续部署 | 自动化软件开发和部署流程 |
| **K8s** | Kubernetes | - | 容器编排平台（8 代表中间省略的 8 个字母） |
| **Container** | - | 容器 | 轻量级、可移植的软件运行环境 |

### 常见场景术语

| 术语 | 中文释义 | 说明 |
|-----|---------|------|
| **Prompt Engineering** | 提示词工程 | 设计和优化 LLM 输入提示的技术 |
| **Context Window** | 上下文窗口 | LLM 能够处理的最大输入文本长度 |
| **Token** | 词元/标记 | LLM 处理文本的基本单位 |
| **Temperature** | 温度参数 | 控制 LLM 输出随机性的参数 |
| **Streaming** | 流式输出 | 逐步返回结果而非一次性返回 |
| **Multi-turn Conversation** | 多轮对话 | 支持上下文连续的对话交互 |
