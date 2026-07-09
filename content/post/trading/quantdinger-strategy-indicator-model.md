---
author: "-"
date: 2026-07-08T19:30:16+08:00
lastmod: 2026-07-08T19:30:16+08:00
title: "QuantDinger: 策略与指标模型"
url: quantdinger-strategy-indicator-model
categories:
  - trading
tags:
  - original
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

## 完整链路与开发流程

完整链路是这样的：策略的 `timeframe` 决定 K 线收盘的时间点，引擎在收盘点把数据喂给策略绑定的那个指标，指标算出四个信号列返回给引擎，引擎据此下单或平仓。

QuantDinger 的 agent 工作流按以下顺序推进：写指标代码（照着 I/O 契约）→ 校验（sandbox 检查）→ 存进指标库 → 创建策略（stopped 状态）→ 回测（`strict_mode` 打开，更贴近实盘）→ 根据结果决定是否跑 paper 单或小仓位实盘。中间每一步都不应跳过，尤其是回测和 paper 单这两步，实盘之前需要先确认止损止盈和仓位控制的行为符合预期。
