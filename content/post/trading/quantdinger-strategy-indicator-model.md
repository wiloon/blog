---
author: "-"
date: 2026-07-08T19:30:16+08:00
lastmod: 2026-07-09T15:05:13+08:00
title: "QuantDinger: 策略与指标模型"
url: quantdinger-strategy-indicator-model
categories:
  - trading
tags:
  - remix
  - AI-assisted
  - quantdinger
  - python
  - quant-trading
---

[QuantDinger](https://github.com/kiritoko1029/QuantDinger) 部署在 homelab 的 k8s 环境里，UI 上可以直接完成交易所的挂单和平仓操作。要开发策略并测试自动交易，需要先理清"策略""指标""交易引擎"这几个概念之间的关系。

## 指标（Indicator）是什么

指标很容易被理解成常见的技术指标，比如一条均线。实际上 QuantDinger 里的指标是一段 Python 脚本，同时做两件事：

1. 计算，用来在图表上画线（比如 EMA、RSI）；
2. 产出四列交易信号，这才是核心：

```python
df['open_long']   # open long signal
df['close_long']  # close long signal
df['open_short']  # open short signal
df['close_short'] # close short signal
```

策略执行引擎读的就是这四列。止损止盈、仓位比例这些风控参数通过 `# @strategy` 注解声明，由引擎统一执行，回测和实盘共用一套逻辑。

一个最简单的例子，快慢均线交叉：

```python
my_indicator_name = "Agent SMA"
my_indicator_description = "SMA crossover"
df = df.copy()
fast = close.rolling(10).mean()
slow = close.rolling(30).mean()
cross_up = (fast > slow) & (fast.shift(1) <= slow.shift(1))
cross_dn = (fast < slow) & (fast.shift(1) >= slow.shift(1))
df['open_long'] = cross_up.fillna(False).astype(bool)
df['close_long'] = cross_dn.fillna(False).astype(bool)
df['open_short'] = False
df['close_short'] = False
output = {'name': my_indicator_name, 'plots': [], 'signals': []}
```

指标脚本本身是无状态的：每次被调用时拿到一批 K 线数据（`df`），一次性向量化算出所有信号，不记得上一次调用发生了什么，也不会自己去拉数据或者下单。

## df 里的 OHLCV 是什么

`df` 这个变量是引擎注入进来的 K 线（OHLCV）数据，一个 pandas DataFrame，至少包含这五列：

- **O**pen：开盘价，这根 K 线周期开始时的成交价
- **H**igh：最高价，这根 K 线周期内出现过的最高成交价
- **L**ow：最低价，这根 K 线周期内出现过的最低成交价
- **C**lose：收盘价，这根 K 线周期结束时的成交价
- **V**olume：成交量，这根 K 线周期内一共成交了多少数量的标的

每一行对应一根 K 线（一个 bar），按时间顺序排列，具体周期由策略的 `timeframe` 决定（比如 1 小时线就是每行一根 1 小时 K 线）。OHLCV 不是量化领域独有的发明，而是股票、期货这类传统市场里画 K 线图、做技术分析时就在用的行业标准术语，交易所 API、数据供应商返回的历史行情都是这五个字段，量化系统只是直接沿用了这套已有的数据契约。

指标代码里常见的 `df = df.copy()` 是在拷贝一份，避免直接在引擎传进来的原始 DataFrame 上加列（后面要给它加 `open_long`、`close_long` 等新列），防止 pandas 报 `SettingWithCopyWarning`，也避免意外修改到引擎内部持有的原始对象。

## 交易引擎和指标的分工

指标不会主动"监控"行情，真正持续盯盘的是交易引擎（`trading_executor`）。引擎负责拉最新数据、按周期调用指标、执行下单和平仓、管理止损止盈。指标只回答"给定这批数据，现在该不该动作"。

引擎里有三种不同的轮询周期：

- **价格 tick**：默认 10 秒一次（`STRATEGY_TICK_INTERVAL_SEC`），拉最新成交价、判断触发条件；网格/定投类策略默认 1 秒一次，因为这类策略靠价格穿越触发，10 秒粒度太粗。
- **K 线刷新 / 指标重算**：不是固定秒数，而是对齐到 K 线收盘边界。比如策略用 1 小时周期，指标就在每个 UTC 整点后 2 秒左右被调用一次；用日线就是每天 UTC 00:00 左右调用一次。收盘时间点用 Unix 时间戳对齐计算：`(now // timeframe_seconds + 1) * timeframe_seconds`，跟交易所的 K 线收盘约定一致。
- **挂单扫描**：单独的 worker，固定 1 秒一次，跟前两个逻辑分开，为了让下单响应更快。

所以指标不会被高频调用，而是每根新 K 线收盘时调用一次，这也是为什么指标要写成无状态、一次性处理整批数据的原因。

## 周期是策略的属性，不是指标的属性

周期（比如 1 小时线还是日线）容易被当成指标自带的配置，实际上周期是策略的属性，在创建策略时的 `trading_config.timeframe` 里指定，跟指标代码本身没关系：

```python
create_strategy(
    strategy_name="...",
    market_category="crypto",
    indicator_id=123,
    trading_config={
        "symbol": "BTCUSDT",
        "timeframe": "1H",
        "tick_interval_sec": 10,
    }
)
```

指标脚本是周期无关的，同一份 EMA 交叉指标换个 `timeframe` 就能从短线策略变成长线策略，不用改代码。当然指标参数（比如均线周期 `fast_period=10`）在不同的 K 线周期下含义不一样，这个需要自己权衡，系统不会帮忙自动适配。

## 一个策略对应一个指标

`create_strategy` 里 `indicator_id` 是单数字段，不是列表，所以一个策略只绑定一个指标。想同时用多个信号（比如 RSI + MACD），不是挂多个指标对象，而是把多个条件写进同一份指标代码里，用 `&`、`|` 组合判断，最终还是只输出那四列信号。

反过来，同一个指标可以被多个不同 `trading_config`（不同周期、不同交易对）的策略复用。

## `@strategy` 注解：写在注释里的配置协议

指标代码里经常能看到这种写法：

```python
# @strategy stopLossPct 0.03
# @strategy takeProfitPct 0.06
# @strategy entryPct 0.25
```

`@strategy` 看起来有点像 Python 的装饰器语法（`@decorator`），但**它只是普通的 Python 注释**，Python 解释器执行这段代码时完全不识别 `@strategy`，跟写一句随便的话没有区别，删掉也不会报语法错误。

真正让这几行有意义的是 QuantDinger 后端自己的解析逻辑：拿到指标源码文本后，用正则表达式逐行扫描，把匹配到的 `# @strategy <key> <value>` 提取出来，对照一个白名单（`stopLossPct`、`takeProfitPct`、`entryPct`、`trailingEnabled`、`tradeDirection` 等）做类型和范围校验，最终转成引擎的风控配置。

这跟其他生态里"注释里携带语义"的做法是同一类思路，比如 Java 的 Javadoc 标签、pytest 的 marker 注释——对解释器/编译器是空的，但上层工具会额外解析出来，当成配置或元数据使用。

具体到 `# @strategy stopLossPct 0.03` 这一行：代表策略的止损比例是 3%，持仓价格往不利方向移动 3% 时，由**引擎**强制平仓，跟指标自己算出来的 `close_long`/`close_short` 信号是两套独立的退出机制——指标的信号负责"结构性反转要不要平仓"，`@strategy` 声明的止损止盈是引擎兜底的风控安全网，两者谁先触发就按谁执行。

白名单里另外三个参数，含义分别是：

- `entryPct`：单次开仓占用的资金比例，取值 `0.01–1`，`1` 表示 100% 仓位，`0.25` 表示每次只用 25% 的可用资金开仓。这个值只影响仓位大小，跟止损止盈的触发条件无关。
- `trailingEnabled`：是否启用移动止损（trailing stop），布尔值。开启后还需要配合 `trailingStopPct`（回撤多少比例触发止损）和 `trailingActivationPct`（价格先要往有利方向移动多少比例，移动止损才开始生效）一起使用，三者共同决定移动止损的行为，单独声明 `trailingEnabled true` 没有意义。
- `tradeDirection`：允许的交易方向，取值 `long`、`short` 或 `both`。它还决定了引擎怎么解释指标输出的 `buy`/`sell` 两列布尔信号（如果指标用的是这种两列写法而不是四列写法）：`long` 模式下 `buy` 是开多、`sell` 是平多；`short` 模式下 `buy` 是平空、`sell` 是开空；`both` 模式下 `buy` 是开多（如果当前持空则先平空再开多）、`sell` 是开空（如果当前持多则先平多再开空）。

## 移动止损（Trailing Stop）是什么

固定止损（`stopLossPct`）是一个死点：开仓价往不利方向移动固定比例就平仓，这个触发线从开仓那一刻起就不再变化。移动止损不一样，它的触发线会跟着价格往有利方向移动而不断上移（多仓）或下移（空仓），目的是在保住已有浮盈的前提下，尽量让盈利继续跑，而不是像固定止盈那样一到目标位就直接平仓、可能错过后续更大的涨幅。

移动止损需要三个参数配合才有意义：

- `trailingEnabled`：总开关，决定这套逻辑要不要生效
- `trailingActivationPct`：价格要先往有利方向移动多少比例，移动止损才开始工作。这个参数是为了避免刚开仓、价格还没怎么动的时候就被小幅回撤误触发
- `trailingStopPct`：激活之后，价格从最高点（多仓）或最低点（空仓）回撤多少比例就平仓

举个例子，假设开多仓价格是 100，`trailingActivationPct` 设为 0.05（5%），`trailingStopPct` 设为 0.02（2%）：

1. 价格先要涨到 105 以上，移动止损才会被激活，在这之前即使价格从 102 跌回 100，也不会触发移动止损
2. 假设价格一路涨到 110，引擎会持续记录这个阶段的最高点（110）
3. 之后价格从 110 回落，只要跌破 110 × (1 − 0.02) = 107.8，就触发平仓，锁定大约 7.8% 的浮盈，而不是等价格跌回开仓价甚至触发固定止损才离场

所以移动止损本质上是把"止盈点"从一个固定数字，变成一个跟随价格最高点动态上移的浮动数字，兼顾了"让盈利继续跑"和"回撤到一定程度就落袋"两个诉求，跟固定止损止盈是两套互补的退出逻辑，实践中可以同时声明，谁先触发就按谁执行。

## 换个角度理解：移动止盈

上面的例子也可以反过来从"止盈"的角度理解，会更直观：固定止盈（`takeProfitPct`）是提前定好一个目标价，价格一到就无条件平仓，不管之后还会不会继续涨；移动止损则完全不设死的目标价，只要激活后价格还在创新高，就一直不平仓，直到价格从最高点回撤超过 `trailingStopPct` 才平仓。

也就是说，触发移动止损离场时，**止盈的目标位可能压根还没到**——K 线只是涨到某个高点后开始回撤，回撤幅度一碰到 `trailingStopPct` 这条线，就会提前平仓，而不是等回撤到开仓价、甚至反转触发固定止损才离场。这也是它常被称为"移动止盈"的原因：本质上是在保护已经产生的浮盈，而不是单纯防止亏损扩大。

延续前面的例子：开多仓 100，`trailingActivationPct` 0.05，`trailingStopPct` 0.02。价格涨到 110 后开始回落，只要跌破 107.8 就平仓——此时如果原本还设了 `takeProfitPct 0.2`（目标价 120），这笔交易在触发移动止损离场时，固定止盈的目标价 120 根本还没到，是价格自己"涨上去又缩回来"提前触发的平仓，而不是碰到了止盈线。

## 完整链路与开发流程

完整链路是这样的：策略的 `timeframe` 决定 K 线收盘的时间点，引擎在收盘点把数据喂给策略绑定的那个指标，指标算出四个信号列返回给引擎，引擎据此下单或平仓。

QuantDinger 的 agent 工作流按以下顺序推进：写指标代码（照着 I/O 契约）→ 校验（sandbox 检查）→ 存进指标库 → 创建策略（stopped 状态）→ 回测（`strict_mode` 打开，更贴近实盘）→ 根据结果决定是否跑 paper 单或小仓位实盘。中间每一步都不应跳过，尤其是回测和 paper 单这两步，实盘之前需要先确认止损止盈和仓位控制的行为符合预期。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-09 | 补充"移动止损（Trailing Stop）是什么"、"换个角度理解：移动止盈"、"df 里的 OHLCV 是什么"三节，说明移动止损参数与触发时机、`df` 的 OHLCV 字段含义及来源 | 原文仅列出参数名和 `df` 变量名，未解释移动止损原理、`df` 具体包含哪些字段及其行业来源 |
