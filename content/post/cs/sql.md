---
title: sql basic
author: "-"
date: 2026-04-18T11:07:43+08:00
url: sql
categories:
  - Database
tags:
  - remix
  - AI-assisted
---

## between and

BETWEEN 用以查询确定范围的值，这些值可以是数字，文本或日期 。  
BETWEEN 运算符是闭区间的：包括开始 和 结束值 。  
not between 则是不包含前后边界的  

## select

```SQL
select * from table0 where column0!='';
```

!='' 会过滤掉值为 null 的数据.

The reason is simple: nulls are neither equal, nor not equal, to anything. This makes sense when you consider that null means "unknown", and the truth of a comparison to an unknown value is also unknown.

The corollary is that:

null = null is not true
null = some_value is not true
null != some_value is not true
The two special comparisons IS NULL and IS NOT NULL exist to deal with testing if a column is, or is not, null. No other comparisons to null can be true.

[https://stackoverflow.com/questions/19974472/postgres-excludes-null-in-where-id-int-query](https://stackoverflow.com/questions/19974472/postgres-excludes-null-in-where-id-int-query)

## IN 与 EXISTS 的区别

面试常考题：`WHERE col IN (subquery)` 和 `WHERE EXISTS (subquery)` 有什么区别？

### 语义差异

- **IN**：先执行子查询，将结果集全部返回，再逐行与外层字段做等值匹配。
- **EXISTS**：对外层每一行，执行一次子查询，只要子查询返回至少一行即为 `TRUE`，立即短路，不关心子查询返回什么值。

```sql
-- IN：orders 表 customer_id 在子查询结果列表中
SELECT * FROM customers
WHERE id IN (SELECT customer_id FROM orders);

-- EXISTS：对每个 customer，检查 orders 中是否存在匹配行
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

### 性能差异

| 场景 | 推荐 |
|---|---|
| 外层表大、子查询结果集**小** | `IN`（子查询结果缓存后做 hash lookup） |
| 外层表小、子查询结果集**大** | `EXISTS`（找到第一条即短路，不需要全表扫描子查询） |
| 子查询结果集含有 `NULL` | `EXISTS`（`IN` 遇到 NULL 会导致整个条件失败） |

#### 以 customers / orders 为例的执行过程对比

以常见的 `customers`（小表）关联 `orders`（大表）场景为例：

| | IN | EXISTS |
|---|---|---|
| 子查询执行次数 | 1 次，全表扫描 orders，把所有 `customer_id` 加载到内存 | N 次（N = customers 行数），每次找到一条就停 |
| 内存占用 | 需要缓存整个子查询结果集 | 几乎不占额外内存 |
| 有索引时 | orders 上有索引也得先把结果集建出来 | 每次子查询直接走索引，找到即停 |

#### 现代数据库会自动优化

MySQL 5.7+、PostgreSQL、Oracle 的优化器会把这两种写法转换成同一个执行计划（通常是 hash join 或 index nested loop join），实际性能差异可能很小。

可以用 `EXPLAIN` 验证：

```sql
-- MySQL / PostgreSQL
EXPLAIN SELECT * FROM customers WHERE id IN (SELECT customer_id FROM orders);
EXPLAIN SELECT * FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- 对比 type、key、rows 三列是否相同
```

#### 选择建议

- 数据量不大、有索引、用现代数据库 → 两者性能**基本一样**，优先选可读性好的。
- orders 表极大（百万+）且无索引 → `EXISTS` 有实质性优势。
- 涉及 `NOT IN` / `NOT EXISTS` → **一定用 `NOT EXISTS`**，避免 NULL 陷阱。

### NULL 的陷阱

`IN` 对 `NULL` 敏感：如果子查询结果中包含 `NULL`，`NOT IN` 的结果会永远为 `FALSE`（因为 `x != NULL` 的结果是 `UNKNOWN`）。

```sql
-- 假设 orders 中有 customer_id = NULL
-- 以下查询将返回 0 行！
SELECT * FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);

-- 用 NOT EXISTS 则不受影响
SELECT * FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

### 关联子查询 vs 非关联子查询

- `IN` 的子查询通常是**非关联**的（独立执行一次）。
- `EXISTS` 的子查询通常是**关联**的（每行执行一次，可以引用外层表字段）。

现代数据库（MySQL 5.7+、PostgreSQL、Oracle）的查询优化器已经能在很多情况下自动将两者转换为等价执行计划，但理解语义差异对于写出正确、可预期的 SQL 仍然至关重要。
