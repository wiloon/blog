---
title: "Output Constraint: LLM 输出约束"
author: "-"
date: 2026-04-26T14:39:27+08:00
lastmod: 2026-07-23T15:30:26+08:00
url: agent-output-constraint
categories:
  - AI
tags:
  - ai-agent
  - structured-output
  - prompt
  - LLM
  - remix
  - AI-assisted
---

## Output Constraint（输出约束）

Output Constraint 是通过提示词、格式规范或模型能力，对 LLM 的输出内容、结构、长度、风格等进行约束，使输出结果可预期、可解析、可被下游系统直接消费的一类技术。

在 AI Agent 场景中，输出约束尤为重要——Agent 的输出往往需要被代码解析、传递给下一个工具，或渲染到 UI，任何格式偏差都可能导致流程中断。

### 约束维度

| 维度 | 说明 | 示例 |
|------|------|------|
| **格式约束** | 要求输出为特定结构 | JSON、XML、Markdown 表格、YAML |
| **内容约束** | 限定输出范围或值域 | 只能从给定选项中选择、不得包含某类内容 |
| **长度约束** | 限制输出的字数或条数 | "不超过 100 字"、"恰好输出 3 条建议" |
| **风格约束** | 限定语气、人称、语言 | 正式/口语、中文/英文、第一人称 |
| **Schema 约束** | 强制输出符合 JSON Schema | 字段类型、必填项、枚举值 |

### 方式一：提示词约束（Prompt-based）

最简单直接的方式，在 System Prompt 或 User Prompt 中明确描述输出格式：

```python
system_prompt = """
你是一个情感分析助手。

输出要求：
- 只输出 JSON，不要有任何额外文字
- 格式如下：
{
  "sentiment": "positive" | "negative" | "neutral",
  "confidence": 0.0 ~ 1.0,
  "reason": "简短理由（不超过 20 字）"
}
"""

response = llm.call(system_prompt, user_input="这个产品真的太好用了！")
# 输出：{"sentiment": "positive", "confidence": 0.95, "reason": "用户使用了强烈的赞美语气"}
```

**优点**：通用，任何模型都支持
**缺点**：无法 100% 保证格式，模型偶尔会"越界"

### 方式二：结构化输出（Structured Outputs）

OpenAI、Google Gemini 等主流模型提供了原生的结构化输出能力，通过 JSON Schema 约束输出，**保证格式 100% 合规**：

```python
from openai import OpenAI
from pydantic import BaseModel

class SentimentResult(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float
    reason: str

client = OpenAI()
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "这个产品真的太好用了！"}],
    response_format=SentimentResult,
)

result = response.choices[0].message.parsed
print(result.sentiment)    # positive
print(result.confidence)   # 0.95
```

底层原理是通过**引导采样（Constrained Decoding）**实现的——在 token 生成阶段，对不符合 Schema 的 token 赋予零概率，强制模型只生成合法结构。

### 方式三：引导采样（Constrained Decoding）

本地部署场景下（如 vLLM、llama.cpp），可以使用 [outlines](https://github.com/dottxt-ai/outlines)、[guidance](https://github.com/guidance-ai/guidance) 等库，在推理层面直接约束输出：

```python
import outlines

model = outlines.models.transformers("mistralai/Mistral-7B-v0.1")

# 定义 Schema
schema = """{
  "type": "object",
  "properties": {
    "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
    "confidence": {"type": "number"},
    "reason": {"type": "string"}
  },
  "required": ["sentiment", "confidence", "reason"]
}"""

generator = outlines.generate.json(model, schema)
result = generator("这个产品真的太好用了！")
# result 是一个合法的 Python dict，不可能格式错误
```

这种方式从根本上杜绝了格式错误，适合对稳定性要求极高的生产环境。

### 方式四：输出解析 + 重试（Parse + Retry）

当无法使用原生结构化输出时，常见的工程兜底方案：

```python
import json
import re

def parse_with_retry(prompt: str, max_retries: int = 3) -> dict:
    for attempt in range(max_retries):
        raw = llm.call(prompt)
        try:
            # 尝试提取 JSON 块
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                return json.loads(match.group())
        except json.JSONDecodeError:
            if attempt < max_retries - 1:
                # 追加修正提示，让模型重新生成
                prompt += f"\n\n上次输出格式有误：{raw}\n请严格按 JSON 格式重新输出，不要添加任何解释文字。"
    raise ValueError(f"连续 {max_retries} 次解析失败")
```

### 在 Agent 中的实践建议

1. **优先使用 Structured Outputs** — 只要模型支持，就用原生结构化输出，彻底消除格式错误
1. **关键节点加校验** — 工具调用的入参、多 Agent 之间传递的消息，都应该用 Pydantic 等做 Schema 校验
1. **提示词要具体** — 不要说"输出 JSON"，要提供完整的格式示例，包括字段名、类型、枚举值
1. **设计容错机制** — 对于无法保证格式的场景，加入重试逻辑和降级策略，避免单次格式错误导致整个流程崩溃

## 相关文章

- [AI Agent Development](./ai-agent-development.md)
- [Intent Recognition and Slot Filling](./agent-intent-and-slot-filling.md)
- [Function Calling](./agent-function-calling.md)
- [Tool Calling Patterns](./agent-tool-calling-patterns.md)
- [Chain of Thought (CoT)](./agent-chain-of-thought.md)
- [LangChain](./langchain.md)
- [LlamaIndex](./llamaindex.md)
- [Agent Token Routing](./agent-token-routing.md)


## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-23 | 自 `ai-agent-development.md` 拆出为本篇 | 母文过长，按主题拆分为独立文档 |

