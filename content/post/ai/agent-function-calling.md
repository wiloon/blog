---
title: "Function Calling: LLM 函数调用"
author: "-"
date: 2026-04-26T14:39:27+08:00
lastmod: 2026-07-23T15:30:26+08:00
url: agent-function-calling
categories:
  - AI
tags:
  - ai-agent
  - function-calling
  - tool-use
  - LLM
  - remix
  - AI-assisted
---

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

## 相关文章

- [AI Agent Development](./ai-agent-development.md)
- [Intent Recognition and Slot Filling](./agent-intent-and-slot-filling.md)
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

