---
title: "Pandas"
author: "-"
date: 2026-07-09T16:09:33+08:00
lastmod: 2026-07-09T16:09:33+08:00
url: pandas
categories:
  - Python
tags:
  - python
  - pandas
  - original
  - AI-assisted
---

## 简介

pandas 是 Python 中最常用的数据处理库，核心数据结构是 `Series`（一维）和 `DataFrame`（二维表格）。常用于读写数据文件、清洗数据、做统计分析。

## 安装

```bash
pip install pandas
# 或者用 uv，速度更快
uv pip install pandas
```

## 核心数据结构

### Series

一维带标签的数组。

```python
import pandas as pd

s = pd.Series([1, 2, 3], index=["a", "b", "c"])
print(s["b"])  # 2
```

### DataFrame

二维表格，每列可以是不同的数据类型。

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol"],
    "age": [25, 30, 35],
})
print(df)
```

## 读写数据

```python
# 读 CSV
df = pd.read_csv("data.csv")

# 写 CSV
df.to_csv("output.csv", index=False)

# 读 Excel
df = pd.read_excel("data.xlsx")

# 读 JSON
df = pd.read_json("data.json")
```

## 查看数据

```python
df.head()      # 前 5 行
df.tail(3)     # 后 3 行
df.shape       # (行数, 列数)
df.columns     # 列名
df.dtypes      # 每列的数据类型
df.info()      # 概览
df.describe()  # 数值列的统计摘要
```

## 选择数据

```python
df["age"]              # 选一列，返回 Series
df[["name", "age"]]     # 选多列，返回 DataFrame

df.loc[0]               # 按标签选行
df.iloc[0]              # 按位置选行

df[df["age"] > 28]      # 条件筛选
```

## 常见操作

### 新增列

```python
df["age_plus_1"] = df["age"] + 1
```

### 缺失值处理

```python
df.isna().sum()          # 每列缺失值数量
df.dropna()               # 删除含缺失值的行
df.fillna(0)               # 用 0 填充缺失值
```

### 分组聚合

```python
df.groupby("name")["age"].mean()
```

### 排序

```python
df.sort_values("age", ascending=False)
```

### 合并

```python
# 按列拼接（类似 SQL join）
pd.merge(df1, df2, on="id", how="left")

# 按行堆叠
pd.concat([df1, df2])
```

## copy() 与 SettingWithCopyWarning

对 `DataFrame` 做切片或筛选后再赋值，pandas 可能不确定是在原对象上改还是在副本上改，从而报 `SettingWithCopyWarning`。显式调用 `.copy()` 可以避免这个问题：

```python
sub = df[df["age"] > 28].copy()
sub["age"] = sub["age"] + 1  # 不会触发警告
```

## 常见应用场景

- 数据清洗（缺失值、去重、类型转换）
- 探索性数据分析（EDA）
- 量化交易中处理 K 线（OHLCV）数据，参见 [quantdinger-strategy-indicator-model](../../trading/quantdinger-strategy-indicator-model.md)
