---
title: "Intent Recognition and Slot Filling: 意图识别与槽位填充"
author: "-"
date: 2026-04-26T14:39:27+08:00
lastmod: 2026-07-23T15:30:26+08:00
url: agent-intent-slot-filling
categories:
  - AI
tags:
  - ai-agent
  - intent
  - slot-filling
  - NLU
  - remix
  - AI-assisted
---

## AI Agent 的意图识别与工具调用

AI Agent 的一个核心应用场景是**自然语言理解 → 意图识别 → 工具调用**。这本质上是一个**分类问题**，即将用户的自然语言输入分类到不同的意图类别，然后路由到相应的工具执行具体任务。

固定 FAQ、按钮选项等不必每次都调大模型：见 [Agent Token Routing](./agent-token-routing.md)（本地匹配 → 轻量分类 → 缓存 → LLM）。

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

## 相关文章

- [AI Agent Development](./ai-agent-development.md)
- [Function Calling](./agent-function-calling.md)
- [Tool Calling Patterns](./agent-tool-calling-patterns.md)
- [Chain of Thought (CoT)](./agent-chain-of-thought.md)
- [Output Constraint](./agent-output-constraint.md)
- [LangChain](./langchain.md)
- [LlamaIndex](./llamaindex.md)
- [Agent Token Routing](./agent-token-routing.md)


## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-23 | 自 `ai-agent-development.md` 拆出为本篇 | 母文过长，按主题拆分为独立文档 |

