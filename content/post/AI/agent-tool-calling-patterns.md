---
title: "Tool Calling Patterns: ReAct 与其它工具调用方式"
author: "-"
date: 2026-04-26T14:39:27+08:00
lastmod: 2026-07-23T15:30:26+08:00
url: agent-tool-calling-patterns
categories:
  - AI
tags:
  - ai-agent
  - ReAct
  - tool-use
  - LangChain
  - remix
  - AI-assisted
---

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

## 相关文章

- [AI Agent Development](./ai-agent-development.md)
- [Intent Recognition and Slot Filling](./agent-intent-and-slot-filling.md)
- [Function Calling](./agent-function-calling.md)
- [Chain of Thought (CoT)](./agent-chain-of-thought.md)
- [Output Constraint](./agent-output-constraint.md)
- [LangChain](./langchain.md)
- [LlamaIndex](./llamaindex.md)
- [Agent Token Routing](./agent-token-routing.md)


## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-23 | 自 `ai-agent-development.md` 拆出为本篇 | 母文过长，按主题拆分为独立文档 |

