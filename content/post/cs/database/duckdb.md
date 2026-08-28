---
title: "DuckDB: 嵌入式 OLAP 数据库"
author: "-"
date: 2026-08-28T19:04:07+08:00
lastmod: 2026-08-28T19:04:07+08:00
url: duckdb
categories:
  - Database
tags:
  - duckdb
  - sqlite
  - olap
  - remix
  - AI-assisted
---

## DuckDB

DuckDB 是一个进程内（in-process）的分析型数据库，常被称作「分析界的 SQLite」：不需要单独的服务进程，一个库文件就是一个数据库，直接嵌入到应用里运行。区别在于它面向 OLAP——列式存储、向量化执行，为聚合与扫描大量数据做优化。

- 官网：[https://duckdb.org/](https://duckdb.org/)
- 单文件数据库，零依赖，零配置
- 可直接查询 CSV / Parquet / JSON 文件，不必先导入
- 与 Python / R / Pandas / Arrow 深度集成

### 安装

```bash
# archlinux
sudo pacman -S duckdb

# macOS
brew install duckdb

# Python
pip install duckdb
```

### CLI 常用命令

```sql
-- 打开或新建一个数据库文件
duckdb my.duckdb

-- 纯内存模式（进程退出即丢失）
duckdb

.tables          -- 列出所有表
.schema table0   -- 查看表结构
.mode box        -- 结果以表格形式输出
.timer on        -- 显示查询耗时
.help
.quit
```

### 直接查询文件

DuckDB 最实用的能力：把文件当表用，不用建表和导入。

```sql
-- 查询单个 Parquet 文件
SELECT * FROM 'data.parquet';

-- 通配符匹配多个文件
SELECT * FROM read_csv_auto('logs/*.csv');

-- 查询 JSON
SELECT * FROM read_json_auto('events.json');

-- 结果写回 Parquet
COPY (SELECT * FROM users WHERE age > 18) TO 'adults.parquet' (FORMAT PARQUET);
```

### 分析函数示例

```sql
SELECT
    date_trunc('month', create_time) AS month,
    count(*) AS user_count,
    percentile_cont(0.95) WITHIN GROUP (ORDER BY age) AS p95_age
FROM users
GROUP BY month
ORDER BY month;
```

### 与 Python / Pandas 集成

```python
import duckdb
import pandas as pd

df = pd.read_csv("sales.csv")

# 直接在 DataFrame 上跑 SQL，无需导入
result = duckdb.sql("SELECT region, SUM(amount) AS revenue FROM df GROUP BY region").df()
```

### ATTACH 混用其他数据库

```sql
-- 挂载一个 SQLite 库，直接用 DuckDB 的分析能力查它
ATTACH 'app.db' AS app (TYPE SQLITE);
SELECT date_trunc('day', order_time) AS day, SUM(amount) AS revenue
FROM app.orders
GROUP BY day;

-- 也支持 ATTACH PostgreSQL
```

## DuckDB vs SQLite

两者都是嵌入式单文件数据库，用法相似，但设计目标相反：SQLite 面向 OLTP（事务、点查询、高频写入），DuckDB 面向 OLAP（聚合、扫描、分析）。

| 维度 | SQLite | DuckDB |
| ---- | ---- | ---- |
| 定位 | OLTP，事务处理 | OLAP，分析查询 |
| 存储方式 | 行式 | 列式 + 向量化执行 |
| 擅长场景 | 点查询、频繁增删改 | 聚合统计、扫描大量数据 |
| 写入性能 | 优秀，支持高并发写 | 一般，批量写较好 |
| 并发模型 | 多读单写 | 基本按单进程设计 |
| 内存占用 | 极低（KB 级） | 较高（为内存计算优化） |
| 数据类型 | 动态类型，5 种基础类型 | 丰富：ARRAY / STRUCT / MAP / JSON / TIMESTAMPTZ 等 |
| 文件格式支持 | 有限（`.import` CSV） | 原生读写 Parquet / CSV / JSON |
| 成熟度 | 2000 年至今，生产验证充分 | 2019 年发布，迭代快 |

### 什么时候用哪个

- **用 SQLite**：应用的持久化层、移动端 / IoT、配置与缓存、需要频繁事务写入的小型服务。
- **用 DuckDB**：数据分析与数据科学、处理 CSV / Parquet / JSON、复杂聚合与统计、替代 Pandas 处理较大数据集、ETL 转换、BI 嵌入式分析引擎。
- **不是替代关系**：可以组合——SQLite 存事务数据，DuckDB 通过 `ATTACH ... (TYPE SQLITE)` 或 `sqlite_scan()` 直接读同一个库做分析。

性能直观对比（约 1000 万行，按月聚合）：SQLite 需要几十秒（行式扫描读取所有列），DuckDB 通常 1–3 秒（列式存储只读需要的列）。反过来，单条记录插入 SQLite 更快。

SQLite 的更多用法见 [SQLite](../sqlite.md)。
