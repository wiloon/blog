---
title: EAFP vs LBYL
author: "-"
date: 2026-03-23T10:29:23+08:00
url: eafp-vs-lbyl
categories:
  - cs
tags:
  - Python
  - remix
  - AI-assisted
---

两种处理错误/边界条件的编程风格，在 Python 社区尤为常见。

## LBYL — Look Before You Leap（先检查再操作）

**谚语来源：** "Look Before You Leap" 字面意思是"跳跃之前，先看清脚下"。想象要跳过一条沟——不先看清落脚点就跳，可能会摔进坑里。引申为**行动之前先确认条件是否安全**，对应中文谚语"三思而后行"、"谋定而后动"。

在编程里，"leap"（跳跃）= 执行操作，"look"（看）= `if` 条件检查。

操作前先检查前提条件是否满足。

```python
# LBYL 风格
if key in my_dict:
    value = my_dict[key]
else:
    value = default

if os.path.exists(filepath):
    with open(filepath) as f:
        data = f.read()
```

**特点：**

- 逻辑清晰，防御性强
- 存在 **TOCTOU（Time-Of-Check-Time-Of-Use）竞态条件**风险——检查和使用之间状态可能改变
- 代码中充满 `if` 判断，容易冗长

## EAFP — Easier to Ask Forgiveness than Permission（先操作再处理异常）

**短语来源：** 这句话来自生活场景的比喻——想做某事时，与其事先去**请示许可**（可能被拒绝、很麻烦），不如**直接去做**，事后出了问题再**道歉求谅解**，因为道歉往往比请示更容易。

| 英文 | 字面意思 | 编程含义 |
|---|---|---|
| Ask Permission | 事先请求许可 | 用 `if` 检查条件是否满足 |
| Ask Forgiveness | 事后请求原谅 | 用 `except` 处理出错的异常 |

这个说法由 Python 之父 Guido van Rossum 推广，体现了 Python 的哲学：**代码应该表达意图，而不是充满防御性检查**。

直接尝试操作，失败了再捕获异常。

```python
# EAFP 风格
try:
    value = my_dict[key]
except KeyError:
    value = default

try:
    with open(filepath) as f:
        data = f.read()
except FileNotFoundError:
    ...
```

**特点：**

- Python 官方推荐风格（PEP 文化）
- 天然避免 TOCTOU 竞态问题
- 代码更简洁，尤其是"成功路径"占多数时
- 依赖异常机制，性能上异常路径略有开销

## 对比总结

| | LBYL | EAFP |
|---|---|---|
| 风格 | 防御性检查 | try/except |
| Python 偏好 | 较少 | **官方推荐** |
| 竞态安全 | 有风险 | 更安全 |
| 可读性 | 条件多时冗长 | 主路径清晰 |
| 适用场景 | 简单条件判断 | I/O、类型转换、网络等 |

## 选择建议

- 成功路径是常态 → 用 **EAFP**，异常只是意外
- 条件判断代价低且语义更清晰 → 用 **LBYL**
- 涉及文件系统、数据库、网络等 I/O → 优先 **EAFP**，避免竞态

Python 之禅里有一句 *"It's easier to ask forgiveness than permission"*，这正是 EAFP 名字的来源。
