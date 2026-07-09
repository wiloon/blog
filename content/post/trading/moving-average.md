---
title: "Moving Average 移动平均线（均线 MA）"
author: "-"
date: 2015-06-04T14:45:35+00:00
lastmod: 2026-07-09T15:45:36+08:00
url: moving-average
categories:
  - trading
tags:
  - MT4
  - remix
  - AI-assisted

---
## Moving Average 移动平均线（均线 MA）

移动平均线（Moving Average，简称 MA，也叫均线）是把某一段时间的收盘价加总后除以该周期得到的数值，比如日线 MA5 就是最近 5 天收盘价的平均。它由美国投资专家 Joseph E. Granville（葛兰碧，又译格兰威尔）在 20 世纪中期提出，是应用最普遍的技术指标之一，用于确认现有趋势、判断可能出现的趋势、发现过度延伸即将反转的走势。

移动平均线的不足之一是滞后于市场，不一定能作为趋势转变的标志。为缓解这个问题，用 5 或 10 天的较短周期会比 40 或 200 天的长周期更快反映近期价格变化；也可以同时使用两条不同周期的均线组合判断——较短周期均线上穿较长周期均线通常是买入信号，下穿则是卖出信号。

## 常见的均线类型

- **SMA**（Simple Moving Average）：简单移动平均线，把研究时间段内所有价格视为同等权重
- **EMA**（Exponential Moving Average）：指数移动平均线，价格权重随时间指数衰减，越新的价格权重越大，对最新行情更敏感
- **SMMA**（Smoothed Moving Average）：平滑移动平均线，目的是让线条更加平滑
- **LWMA**（Linear Weighted Moving Average）：线性加权移动平均线，因为 MA 是滞后指标，给最近的价格更高权重以减少滞后
- **WMA**（Weighted Moving Average）：加权移动平均线，计算时给个别数据乘以不同数值，n 日 WMA 中最近一个数值乘以 n、次近的乘以 n-1，依次递减到 0

解释均线最常用的方法是把它的走势与价格走势比较：价格上穿均线通常视为买入信号，价格跌破均线则视为卖出信号。这类基于均线的交易体系不是为了精确抄底摸顶设计的，而是跟随趋势——价格探底后开始买入，价格转跌后开始卖出。均线也可以应用在其他技术指标上：指标上穿自身的均线，说明当前走势可能延续；跌破则说明可能反转。

## 计算方法

### SMA

汇总某几个时段内的收盘价，再除以时段数：

$$
SMA = \frac{\sum_{i=1}^{N} \text{Close}_i}{N}
$$

- $N$：计算用的时段数目

### EMA

把当前收盘价按权重 $\alpha$ 与上一个 EMA 值相加，越近的价格权重越大：

$$
EMA_t = \alpha \cdot Close_t + (1-\alpha) \cdot EMA_{t-1}
$$

- $Close_t$：当前时段收盘价
- $EMA_{t-1}$：上一时段的 EMA 值
- $\alpha$：当前价格所占的百分比权重

### SMMA

第一个值的计算方式和 SMA 相同，之后的值用递推公式：

$$
SUM_1 = \sum_{i=1}^{N} \text{Close}_i, \quad SMMA_1 = \frac{SUM_1}{N}
$$

$$
SMMA_t = \frac{SUM_1 - SMMA_1 + Close_t}{N}
$$

- $SUM_1$：N 个时段收盘价的总值
- $SMMA_1$：第一根柱形的 SMMA
- $SMMA_t$：当前柱形的 SMMA（第一根除外）

### LWMA

给序列里离当前最近的数据更高的权重：

$$
LWMA = \frac{\sum_{i=1}^{N} Close_i \cdot i}{\sum_{i=1}^{N} i}
$$

- $\sum_{i=1}^{N} i$：权重系数总和，即 $1 + 2 + \cdots + N$

## 参考链接

- <http://ta.mql4.com/cn/indicators/trends/moving_average>
- <http://baike.baidu.com/view/7973.htm>
- <http://zh.wikipedia.org/zh-cn/%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87>
- <http://www.icbc.com.cn/ICBCCollege/client/page/KnowledgeDetail.aspx?ItemID=633787143344519034>
- <http://blog.sina.com.cn/s/blog_6004493e0100e2rw.html>

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-09 | 文件从 `content/post/other/移动平均线-均线-moving-average-ma.md` 重命名为 `moving-average.md` 并移入 `trading` 目录；title 改为英中混写；url 改为英文；categories 从 `Inbox` 改为 `trading`；删除重复段落及转载页面噪音信息；按"是什么/常见类型/计算方法/参考链接"重新组织全文；公式改为 KaTeX 数学语法 | 文件名、url 含中文且分类为 Inbox，不符合规范；原文重复且结构混乱；纯文本公式不易读，改成数学公式渲染更直观 |
