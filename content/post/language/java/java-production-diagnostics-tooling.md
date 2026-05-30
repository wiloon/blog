---
title: Java 生产环境诊断工具选型
author: "-"
date: 2026-05-30T16:56:29+08:00
lastmod: 2026-05-30T19:45:37+08:00
url: production-diagnostics-tooling
categories:
  - language
tags:
  - java
  - btrace
  - jfr
  - arthas
  - async-profiler
  - jvm
  - remix
  - AI-assisted
---

## 背景

生产环境曾运行在 JDK 8。线上出现问题时，用 [BTrace](/btrace) attach 到运行中的 JVM：按条件过滤慢方法（例如耗时超过 9ms），持续输出，不改代码、不重启。

当时 JFR 仍是商业特性，attach 式动态追踪是可行且低成本的方案之一。本文先记录 JDK 8 时代的诉求与 BTrace 用法，其它 JDK 版本下的工具对照见文末章节。

## JDK 8 时代 BTrace 在解决什么

从 [BTrace 使用笔记](/btrace) 中的脚本可以看出，核心需求是：

1. attach 到运行中的 JVM，不重启
2. 按条件过滤慢方法（例如大于 9ms）
3. 持续输出，而不是只看一次快照
4. 必要时查看参数、返回值、调用栈

示例脚本（慢调用过滤 + 计数）：

```java
@OnMethod(clazz = "com.wiloon.package0.Class0", method = "method0",
          location = @Location(Kind.RETURN))
public static void printMethodRunTime(@ProbeClassName String probeClassName,
                                      @Duration long duration) {
    long d = duration / 1000000;
    if (d > 9) {
        i++;
        println("index: " + i + ", timestamp:" + timestamp("HH:mm:ss")
            + ", " + probeClassName + ", duration: " + d + " ms");
    }
}
```

执行方式：

```bash
jcmd -l
/bin/btrace <PID> MethodDuration_redis.java
```

### Attach 原理（简述）

BTrace 通过 JDK [Attach API](/attach-api) 把 agent JAR 加载进目标 JVM，在 `agentmain` 里注册 `ClassFileTransformer`，用 ASM 织入探针并对已加载类 `retransform`。客户端经 Socket 下发脚本、回收输出。细节见 [BTrace](/btrace) 中的「Attach 原理」一节。

## JDK 8 下的结论

在 JDK 8 生产环境中，针对「不重启、按条件持续盯某个方法」这类问题，BTrace 是合理且常用的选择。脚本需遵守 BTrace 的安全限制，上线前在本地充分验证。

## 参考（JDK 8 相关）

- [BTrace 使用笔记](/btrace)
- [BTrace 项目](https://github.com/btraceio/btrace)
- [jcmd](/jcmd)

## 其它 JDK 版本

以下供 JDK 升级后的选型参考；不再以 JDK 8 为前提。

### JDK 11 及以后：JFR 与 BTrace 2.x

从 JDK 11 起 JFR 免费，许多 GC、锁、分配类问题可用 `jcmd <pid> JFR.start` 等命令处理，见 [Java Flight Recorder](/java-flight-recorder-jfr)。

BTrace 2.x 仍在维护，支持 oneliner，文档写明兼容 Java 8–25（更高版本需实测）：

```bash
btrace -n 'com.myapp.*::* @return if duration>100ms { print method, duration }' <PID>
```

### JDK 21 及以后：动态 Agent 加载

attach 动态 agent 时，目标 JVM 通常需要：

```bash
-XX:+EnableDynamicAgentLoading
```

否则可能失败或告警。勿使用 `-XX:+DisableAttachMechanism`。

### Java 25 / 26：JDK 自带能力与工具分工

| 需求 | 更常见的做法 |
| ---- | ------------ |
| 谁在吃 CPU | async-profiler（`asprof -e cpu --jfrsync`）或 JFR |
| GC、锁、分配、虚拟线程 pinning | JFR |
| 临时看方法参数、返回值、耗时 | Arthas `watch` / `trace` / `monitor` |
| 线程卡死、CPU 飙高 | Arthas `thread` + `jcmd` / `jstack` |
| 持续、带条件的慢调用统计 | JFR 持续录制，或 BTrace 脚本 |

Java 25 引入实验性 `jdk.CPUTimeSample`（JEP 509），用 CPU 时间采样；目前主要面向 Linux，尚不能替代 async-profiler 的全部能力。

### BTrace 与 Arthas 的分工

| 维度 | Arthas | BTrace |
| ---- | ------ | ------ |
| 交互方式 | 命令行，即查即看 | 写脚本，持续运行 |
| 上手成本 | 低 | 高 |
| 适用问题 | 「现在出了什么事？」 | 「持续多久、频率多高、满足什么条件？」 |
| 条件过滤 + 累计统计 | 弱 | 强 |
| 追踪方法内对特定类的 `new` | 做不到 | 可以 |

对应当年慢调用脚本的现代写法：

```bash
# 一次性定位（Arthas）
trace com.wiloon.package0.Class0 method0 '#cost>9'
watch com.wiloon.package0.Class0 method0 '{params,returnObj,#cost}' '#cost>9'

# 持续计数（BTrace oneliner）
btrace -n 'com.wiloon.package0.Class0::method0 @return if duration>9ms { print method, duration }' <PID>
```

概括：Arthas 像手电筒，BTrace 像监控摄像头。

### 升级后的选型建议（2026）

第一层（减少临时 attach）：

- 应用指标：Micrometer / Prometheus
- 分布式追踪：OpenTelemetry
- JVM 基线：JFR 模板或周期性 `jcmd JFR.dump`

第二层（出问题时 attach，不重启）：

1. Arthas — 快速看线程、慢方法、参数、调用栈
2. JFR — GC、锁、分配、虚拟线程
3. async-profiler — CPU 热点、火焰图

第三层（BTrace 仍适合）：

- 长时间、带条件、可累计的探针
- 追踪特定类的对象分配
- 自定义输出到文件或 StatsD
- Arthas 表达不了的复杂逻辑

### 升级后的结论

在 Java 26 等较新 JDK 上，BTrace 不是解决同类问题的默认最佳实践；标准答案更接近 JFR + async-profiler + Arthas，再叠加 metrics / tracing。

BTrace 仍有效，尤其「慢调用过滤 + 持续采集」，但更像专项工具。若保留 JDK 8 时代的脚本库，建议：少数持续监控脚本留 BTrace；临时排查迁 Arthas；性能分析迁 JFR + async-profiler；在新 JDK 上实测 BTrace 2.2.x 与 `-XX:+EnableDynamicAgentLoading`。

### 场景对照

| 场景 | JDK 8（BTrace） | 较新 JDK |
| ---- | --------------- | -------- |
| 慢方法过滤 | `@OnMethod` + `@Duration` | Arthas `trace` / `watch`，或 BTrace oneliner |
| CPU 热点 | 不擅长 | `asprof -d 30 -e cpu --jfrsync profile.jfr <pid>` |
| GC 与延迟 | 需自定义脚本 | JFR `default.jfc` |
| 看方法参数 | BTrace 脚本 | Arthas `watch` |

### 参考（其它 JDK 版本）

- [Arthas](https://github.com/alibaba/arthas)
- [async-profiler](https://github.com/async-profiler/async-profiler)
- [BTrace 项目](https://github.com/btraceio/btrace)
