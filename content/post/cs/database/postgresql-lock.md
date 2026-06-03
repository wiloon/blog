---
title: PostgreSQL 锁机制
author: "-"
date: 2026-06-03T21:40:30+08:00
lastmod: 2026-06-03T21:46:40+08:00
url: postgresql-lock
categories:
  - CS
tags:
  - postgresql
  - lock
  - original
---

PostgreSQL 的锁机制分为多个层级，从应用层的 Advisory Lock 到行级、表级，再到内核内部的 LWLock，每一层都有其适用场景。

## 锁的层级总览

| 层级              | 类型             | 由谁控制                | 可见性              |
| ----------------- | ---------------- | ----------------------- | ------------------- |
| 表级锁            | 8 种模式         | SQL 语句或 `LOCK TABLE` | `pg_locks`          |
| 行级锁            | 4 种模式         | `SELECT FOR ...`        | `pg_locks` (元组锁) |
| 页级锁            | 共享/排他        | Buffer Manager 内部     | 不可见              |
| Advisory Lock     | 会话级/事务级    | 应用程序                | `pg_locks`          |
| Predicate Lock    | 谓词锁           | 串行化隔离级别 (SSI)    | `pg_locks`          |
| LWLock / Spinlock | 内核共享内存保护 | 内核内部                | 不可见              |

---

## 表级锁

PostgreSQL 表级锁有 8 种模式，从弱到强排列。**冲突**意味着两个锁不能被同时持有。

### 8 种模式

| 模式                     | 缩写 | 典型操作                                              | 说明                                                                    |
| ------------------------ | ---- | ----------------------------------------------------- | ----------------------------------------------------------------------- |
| `ACCESS SHARE`           | AS   | `SELECT`                                              | 最弱，只与 `ACCESS EXCLUSIVE` 冲突                                      |
| `ROW SHARE`              | RS   | `SELECT FOR UPDATE/SHARE`                             | 与 `EXCLUSIVE`、`ACCESS EXCLUSIVE` 冲突                                 |
| `ROW EXCLUSIVE`          | RE   | `INSERT`、`UPDATE`、`DELETE`                          | 与 `SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE`、`ACCESS EXCLUSIVE` 冲突 |
| `SHARE UPDATE EXCLUSIVE` | SUE  | `VACUUM`、`ANALYZE`、`CREATE INDEX CONCURRENTLY`      | 与自身及更强模式冲突                                                    |
| `SHARE`                  | S    | `CREATE INDEX`（非 CONCURRENTLY）                     | 阻止并发写                                                              |
| `SHARE ROW EXCLUSIVE`    | SRE  | `CREATE TRIGGER`、部分 `ALTER TABLE`                  | 比 `SHARE` 更强，与自身冲突                                             |
| `EXCLUSIVE`              | E    | `REFRESH MATERIALIZED VIEW CONCURRENTLY`              | 只允许并发 `ACCESS SHARE`（即普通 SELECT）                              |
| `ACCESS EXCLUSIVE`       | AE   | `DROP TABLE`、`TRUNCATE`、`ALTER TABLE`、`LOCK TABLE` | 最强，与所有模式冲突，阻塞所有操作包括 SELECT                           |

### 冲突矩阵

```text
              AS  RS  RE  SUE  S  SRE  E  AE
ACCESS SHARE   -   -   -   -   -   -   -  ✗
ROW SHARE      -   -   -   -   -   -   ✗  ✗
ROW EXCLUSIVE  -   -   -   -   ✗   ✗   ✗  ✗
SHARE UPD EXC  -   -   -   ✗   ✗   ✗   ✗  ✗
SHARE          -   -   ✗   ✗   -   ✗   ✗  ✗
SHARE ROW EXC  -   -   ✗   ✗   ✗   ✗   ✗  ✗
EXCLUSIVE      -   ✗   ✗   ✗   ✗   ✗   ✗  ✗
ACCESS EXCL    ✗   ✗   ✗   ✗   ✗   ✗   ✗  ✗
```

### 显式表锁

```sql
-- 显式加表锁，默认 ACCESS EXCLUSIVE
LOCK TABLE orders;

-- 指定模式
LOCK TABLE orders IN SHARE MODE;
LOCK TABLE orders IN ROW EXCLUSIVE MODE;

-- 非阻塞，获取不到立即失败
LOCK TABLE orders IN ACCESS EXCLUSIVE MODE NOWAIT;
```

常见场景：批量数据迁移时先 `LOCK TABLE ... IN EXCLUSIVE MODE`，防止迁移过程中有新写入。

---

## 行级锁

行级锁在 `SELECT ... FOR ...` 语句执行时获取，事务结束时自动释放。

### 4 种模式

| 语法                | 强度 | 说明                                           |
| ------------------- | ---- | ---------------------------------------------- |
| `FOR KEY SHARE`     | 最弱 | 允许其他事务修改非主键列，阻止 `FOR UPDATE`    |
| `FOR SHARE`         | 弱   | 阻止其他事务修改行，允许多个事务同时持有共享锁 |
| `FOR NO KEY UPDATE` | 强   | 修改行但不影响主键/唯一键时使用                |
| `FOR UPDATE`        | 最强 | 排他锁，阻止其他事务的任何写和锁               |

### 冲突关系

|                   | FOR KEY SHARE | FOR SHARE | FOR NO KEY UPDATE | FOR UPDATE |
| ----------------- | ------------- | --------- | ----------------- | ---------- |
| FOR KEY SHARE     | -             | -         | -                 | ✗          |
| FOR SHARE         | -             | -         | ✗                 | ✗          |
| FOR NO KEY UPDATE | -             | ✗         | ✗                 | ✗          |
| FOR UPDATE        | ✗             | ✗         | ✗                 | ✗          |

### 阻塞行为选项

```sql
-- 默认：阻塞等待直到获取成功
SELECT * FROM orders WHERE id = 1 FOR UPDATE;

-- NOWAIT：获取不到立即报错
SELECT * FROM orders WHERE id = 1 FOR UPDATE NOWAIT;

-- SKIP LOCKED：跳过已被锁定的行（任务队列场景常用）
SELECT * FROM tasks WHERE status = 'pending' FOR UPDATE SKIP LOCKED LIMIT 10;
```

### `SKIP LOCKED` 实现任务队列

`SKIP LOCKED` 是实现**无竞争任务队列**的标准做法，多个 worker 并发消费时互不阻塞：

```sql
-- Worker 抢任务：跳过其他 worker 已锁定的行
BEGIN;
SELECT id, payload
FROM tasks
WHERE status = 'pending'
ORDER BY created_at
FOR UPDATE SKIP LOCKED
LIMIT 1;

-- 处理完成后更新状态
UPDATE tasks SET status = 'done' WHERE id = $1;
COMMIT;
```

---

## Advisory Lock 咨询锁

### 什么是 Advisory Lock

Advisory Lock (咨询锁) 是 PostgreSQL 提供的一种**应用层协调机制**。与行锁、表锁保护的是数据库内部的数据对象不同, Advisory Lock 的含义完全由**应用自己定义** —— 数据库只负责加锁/解锁的原子性和互斥性, 至于这把锁代表什么、保护什么资源, 完全取决于应用程序的约定。

Advisory Lock 使用一个 64 位整数 (或两个 32 位整数) 作为锁的 key, 存储在**共享内存**中, 不写入 WAL, 不占用磁盘空间。

### 核心 API

#### Session 级别 (会话级)

```sql
-- 获取排他锁 (阻塞, 直到获取成功)
SELECT pg_advisory_lock(key bigint);

-- 尝试获取排他锁 (非阻塞, 成功返回 true, 失败返回 false)
SELECT pg_try_advisory_lock(key bigint);

-- 获取共享锁 (多个会话可同时持有共享锁)
SELECT pg_advisory_lock_shared(key bigint);

-- 尝试获取共享锁 (非阻塞)
SELECT pg_try_advisory_lock_shared(key bigint);

-- 释放排他锁
SELECT pg_advisory_unlock(key bigint);

-- 释放共享锁
SELECT pg_advisory_unlock_shared(key bigint);

-- 释放当前会话所有 Advisory Lock
SELECT pg_advisory_unlock_all();
```

#### Transaction 级别 (事务级)

```sql
-- 获取事务级排他锁 (事务结束时自动释放, 无法手动解锁)
SELECT pg_advisory_xact_lock(key bigint);

-- 尝试获取事务级排他锁
SELECT pg_try_advisory_xact_lock(key bigint);
```

#### 两个 int4 参数版本

当业务 key 由两个维度组成时 (如 resource_type + resource_id), 可以用两个 int4:

```sql
-- 等效于 pg_advisory_lock((int8(class) << 32) | int8(id))
SELECT pg_advisory_lock(class int4, id int4);
SELECT pg_try_advisory_lock(class int4, id int4);
```

### Session 级 vs Transaction 级的区别

| 维度         | Session 级                                | Transaction 级                              |
| ------------ | ----------------------------------------- | ------------------------------------------- |
| 释放时机     | 手动调用 `pg_advisory_unlock` 或连接断开  | 事务提交或回滚时自动释放                    |
| 可重入       | ✅ 同一 Session 可多次加锁, 需同等次数解锁 | ✅ 事务内多次加锁只需一次 (事务结束统一释放) |
| 可手动解锁   | ✅                                         | ❌ 只能等事务结束                            |
| 连接池兼容性 | ⚠️ 有风险 (见下文)                         | ✅ 使用 `AUTOCOMMIT` 时自然归还              |

### Advisory Lock 的重要特性

#### 1. 存储在共享内存, 不写 WAL

Advisory Lock 不记录到 WAL (Write-Ahead Log), 因此:

- **不会复制**到 Standby, 主从切换后锁状态消失
- 服务器崩溃重启后锁状态消失
- 性能极高, 无磁盘 I/O

这与行级锁表方案形成对比: 行级锁写入 WAL, 可以通过同步复制保证 Failover 后锁一致性。

#### 2. 可重入性

Session 级 Advisory Lock 是**可重入**的: 同一会话可以对同一个 key 多次调用 `pg_advisory_lock`, 内部维护一个计数器, 必须调用相同次数的 `pg_advisory_unlock` 才能真正释放。

```sql
SELECT pg_advisory_lock(100);   -- count = 1
SELECT pg_advisory_lock(100);   -- count = 2
SELECT pg_advisory_unlock(100); -- count = 1, 锁仍持有
SELECT pg_advisory_unlock(100); -- count = 0, 锁释放
```

#### 3. 连接断开自动释放

持有 Session 级 Advisory Lock 的连接断开后 (正常关闭或异常崩溃), PostgreSQL 会自动释放该会话持有的所有 Advisory Lock。这天然解决了**死锁**问题 —— 持有锁的进程崩溃后锁不会永久阻塞其他进程。

### 使用连接池的注意事项

使用 PgBouncer 等连接池时, Session 级 Advisory Lock 存在风险:

```text
应用 A: 从连接池借到连接 conn-1
应用 A: pg_advisory_lock(100) → 加锁成功
应用 A: 完成业务, 将 conn-1 归还连接池  ← 忘记 unlock!

应用 B: 从连接池借到 conn-1
应用 B: 以为是干净连接, 实际上 conn-1 仍持有 key=100 的锁
应用 B: 对其他 key 加锁, 操作共享资源 → 产生意外的锁竞争
```

**解决方案:**

1. **始终在 finally 块中解锁**, 确保归还连接前释放锁
2. **优先使用 Transaction 级 `pg_advisory_xact_lock`**, 事务结束时自动释放, 配合 `AUTOCOMMIT` 使用时尤其安全
3. **在 `pg_advisory_lock` 前先调用 `pg_advisory_unlock_all()`** 作为保险措施 (不推荐, 副作用大)

### 典型使用场景

#### 场景一: 分布式定时任务防重

多个实例同时运行定时任务时, 用 Advisory Lock 保证只有一个实例执行:

```sql
-- 在应用代码中 (伪代码)
connection.execute("SELECT pg_try_advisory_lock(hashtext('daily_report_job'))");
if result == true:
    run_daily_report()
    connection.execute("SELECT pg_advisory_unlock(hashtext('daily_report_job'))")
else:
    log("Another instance is running the job, skip")
```

#### 场景二: 防止并发处理同一业务对象

```sql
-- 对 order_id=12345 加锁, 防止并发处理
SELECT pg_try_advisory_xact_lock(12345);
-- 返回 true: 获取成功, 处理订单
-- 返回 false: 已有其他事务在处理, 跳过或等待

-- 事务提交时自动释放, 无需手动 unlock
COMMIT;
```

#### 场景三: 与 SELECT FOR UPDATE 配合

先用 Advisory Lock 防止并发, 再用 `SELECT FOR UPDATE` 锁定行:

```sql
BEGIN;
SELECT pg_advisory_xact_lock(order_id);
SELECT * FROM orders WHERE id = order_id FOR UPDATE;
-- 处理业务逻辑
COMMIT;
```

### Advisory Lock vs 其他方案对比

| 方案                    | 性能  | 复制到 Standby | 崩溃后自动释放 | 适用场景                 |
| ----------------------- | ----- | -------------- | -------------- | ------------------------ |
| Advisory Lock (Session) | ⭐⭐⭐⭐⭐ | ❌              | ✅ (连接断开)   | 任务调度, 轻量协调       |
| Advisory Lock (Xact)    | ⭐⭐⭐⭐⭐ | ❌              | ✅ (事务结束)   | 短事务内互斥             |
| 行级锁表                | ⭐⭐⭐   | ✅ (同步复制时) | ✅ (TTL + 清理) | 强一致性, 跨服务         |
| Redis SET NX            | ⭐⭐⭐⭐⭐ | ❌ (异步复制)   | ✅ (TTL)        | 高并发, 允许极低概率失败 |
| ZooKeeper / etcd        | ⭐⭐⭐   | ✅ (Raft)       | ✅              | 强一致性要求             |

### 主从切换与数据库重启对 Advisory Lock 的影响

**结论先行: Advisory Lock 在主从切换和数据库重启后会完全消失。**

#### 为什么会消失

Advisory Lock 存储在 PostgreSQL 的**共享内存 (Shared Memory)** 中, 不写入 WAL (Write-Ahead Log)。这意味着:

- 进程内存的数据在进程终止后即消失
- 没有 WAL 就无法复制到 Standby
- 没有 WAL 就无法在崩溃恢复时重放

#### 场景一: 数据库重启

```text
应用 A 持有 Advisory Lock(100) ← 存在共享内存中

数据库重启 (计划内 or 崩溃)
    ↓
共享内存清空
    ↓
Advisory Lock(100) 消失

数据库重启完成后:
- 应用 A 的连接已断开 (连接断开时锁本来就会自动释放)
- 即使应用 A 重新连接, 也需要重新申请锁
- 其他应用可以正常申请 Lock(100)
```

**影响**: 数据库重启后锁状态清空, **行为是符合预期的**。因为持有锁的连接在重启时已强制断开, 锁随之释放, 不存在「锁记录残留但持有者已消失」的僵尸状态。

#### 场景二: 主从切换 (Failover)

```text
应用 A 连接 Primary, 持有 Advisory Lock(100)
Primary 宕机
    ↓
Standby 晋升为新 Primary
    ↓
新 Primary 共享内存中没有 Advisory Lock(100)
    ↓
应用 B 连接新 Primary, 申请 Advisory Lock(100) → 成功! ⚠️

同时:
应用 A 的连接已断开 (Primary 宕机)
应用 A 重连新 Primary, 发现自己没有锁了
```

**影响**: Failover 窗口期内存在**互斥性被短暂破坏**的风险 —— 原持有锁的客户端还没意识到 Primary 已切换, 而新 Primary 上已经可以申请到同一把锁。

#### 与行级锁表的对比

| 事件           | Advisory Lock  | 行级锁表 (异步复制) | 行级锁表 (同步复制) |
| -------------- | -------------- | ------------------- | ------------------- |
| 数据库重启     | 锁消失 (正常)  | 锁记录保留          | 锁记录保留          |
| 主从切换       | 锁消失         | ❌ 可能丢锁          | ✅ 锁记录保留        |
| 对互斥性的影响 | 短暂窗口期风险 | 短暂窗口期风险      | 安全                |

#### 实际应对方式

**方案一: 业务幂等兜底 (最重要)**

无论用何种分布式锁方案, 幂等性都是最后一道防线。Failover 期间即使两个客户端同时获得锁, 幂等检查也能保证业务结果正确:

```sql
-- 获得锁后, 先检查业务状态
SELECT pg_try_advisory_xact_lock(order_id);
IF acquired THEN
    -- 检查幂等: 是否已经处理过?
    IF NOT EXISTS (SELECT 1 FROM orders WHERE id = order_id AND status = 'processed') THEN
        -- 处理业务
        UPDATE orders SET status = 'processed' WHERE id = order_id;
    END IF;
END IF;
```

**方案二: 客户端感知重连**

应用层在重连后重新申请锁, 并检查业务状态是否需要重新处理。

**方案三: 对强一致性要求高时, 改用行级锁表 + 同步复制**

如果业务绝对不能容忍 Failover 期间的短暂互斥失效, 应改用行级锁表方案并开启同步复制:

```ini
# postgresql.conf
synchronous_commit = remote_apply
synchronous_standby_names = 'standby1'
```

#### 总结

| 场景             | Advisory Lock 行为     | 是否需要担心                         |
| ---------------- | ---------------------- | ------------------------------------ |
| 计划内重启       | 锁随连接断开消失, 正常 | 不需要, 持有锁的连接会重新连接并申请 |
| 崩溃重启         | 锁消失, 正常           | 不需要, 配合业务幂等即可             |
| 主从切换         | 锁消失, 存在短暂窗口期 | 需要幂等兜底                         |
| Standby 上申请锁 | Standby 只读, 无法申请 | 不适用                               |

> **Advisory Lock 不适合需要跨 Failover 保持严格互斥的场景。** 对于这类需求, 应使用行级锁表 + 同步复制, 或 etcd/ZooKeeper。大多数场景下, Advisory Lock + 业务幂等是足够且高效的组合。

### 查看当前 Advisory Lock 状态

```sql
-- 查看当前所有 Advisory Lock
SELECT
    pid,
    locktype,
    classid,
    objid,
    mode,
    granted
FROM pg_locks
WHERE locktype = 'advisory';

-- 结合进程信息
SELECT
    l.pid,
    a.usename,
    a.application_name,
    l.classid,
    l.objid,
    l.mode,
    l.granted
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE l.locktype = 'advisory';
```

---

## Predicate Lock 谓词锁

谓词锁是 PostgreSQL 在**串行化隔离级别 (`SERIALIZABLE`)** 下自动使用的锁，普通 `READ COMMITTED` 下不涉及。

### 目的

防止**序列化异常**（包括幻读）。普通的行锁和表锁只能防止对**已存在行**的并发修改，无法防止「一个事务读取了某个范围，另一个事务在该范围内插入了新行」这类幻读。谓词锁通过追踪**读取谓词**（即 WHERE 条件所覆盖的范围）来检测潜在冲突。

### 工作方式

```sql
-- 开启串行化隔离
BEGIN ISOLATION LEVEL SERIALIZABLE;

-- 读取操作会隐式在读取范围上加谓词锁
SELECT SUM(amount) FROM accounts WHERE user_id = 1;

-- 如果另一个并发事务在 user_id=1 的范围内插入了新行
-- PostgreSQL 会检测到冲突，并在提交时回滚其中一个事务
COMMIT;
```

当检测到序列化冲突时，PostgreSQL 会抛出：

```text
ERROR:  could not serialize access due to concurrent update
SQLSTATE: 40001
```

应用需要捕获 `40001` 错误并重试事务。

### 与行级锁的区别

|          | 行级锁     | 谓词锁             |
| -------- | ---------- | ------------------ |
| 保护对象 | 已存在的行 | 查询谓词覆盖的范围 |
| 防幻读   | ❌          | ✅                  |
| 隔离级别 | 任意       | 仅 SERIALIZABLE    |
| 冲突处理 | 阻塞等待   | 事务回滚（需重试） |

---

## 查看锁状态

### pg_locks 视图

```sql
-- 查看所有锁
SELECT
    pid,
    locktype,
    relation::regclass AS table_name,
    mode,
    granted,
    transactionid,
    classid,
    objid
FROM pg_locks
ORDER BY pid;
```

`locktype` 常见值：

| 值              | 含义           |
| --------------- | -------------- |
| `relation`      | 表级锁         |
| `tuple`         | 行级锁（元组） |
| `advisory`      | Advisory Lock  |
| `transactionid` | 事务 ID 锁     |
| `virtualxid`    | 虚拟事务 ID 锁 |

### 查看锁持有时长

```sql
-- 查看锁：持有时长、模式、所属进程，按持有时间倒序
SELECT locker.pid,
       pc.relname,
       locker.mode,
       locker_act.application_name,
       least(query_start, xact_start)                        start_time,
       locker_act.state,
       CASE
           WHEN granted = 'f' THEN 'wait_lock'
           WHEN granted = 't' THEN 'get_lock'
       END                                                    lock_status,
       current_timestamp - least(query_start, xact_start) AS runtime,
       locker_act.query
FROM pg_locks locker
JOIN pg_stat_activity locker_act ON locker.pid = locker_act.pid
JOIN pg_class pc ON locker.relation = pc.oid
WHERE NOT locker.pid = pg_backend_pid()
  AND pc.reltype <> 0
ORDER BY runtime DESC;
```

### 查看锁等待

```sql
-- 查看正在等待锁的会话
SELECT
    blocked.pid          AS blocked_pid,
    blocked_act.query    AS blocked_query,
    blocking.pid         AS blocking_pid,
    blocking_act.query   AS blocking_query,
    blocked_locks.mode   AS waiting_for_mode
FROM pg_locks blocked_locks
JOIN pg_stat_activity blocked_act ON blocked_act.pid = blocked_locks.pid
JOIN pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_stat_activity blocking_act ON blocking_act.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

### 查看 Advisory Lock

```sql
SELECT
    l.pid,
    a.usename,
    a.application_name,
    l.classid,
    l.objid,
    l.mode,
    l.granted
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE l.locktype = 'advisory';
```

---

## 各锁类型对比

| 类型                 | 粒度     | 自动释放 | 持久化 | 跨 Failover | 适用场景            |
| -------------------- | -------- | -------- | ------ | ----------- | ------------------- |
| 表级锁               | 表       | 事务结束 | ✅ WAL  | ✅           | DDL、批量操作       |
| 行级锁               | 行       | 事务结束 | ✅ WAL  | ✅           | 并发更新同一行      |
| Advisory Lock (会话) | 自定义   | 连接断开 | ❌ 内存 | ❌           | 任务调度、轻量协调  |
| Advisory Lock (事务) | 自定义   | 事务结束 | ❌ 内存 | ❌           | 短事务内互斥        |
| Predicate Lock       | 谓词范围 | 事务结束 | ❌ 内存 | ❌           | SERIALIZABLE 防幻读 |
