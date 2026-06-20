---
title: HotSpot JVM 启动参数
author: "-"
date: 2026-06-19T22:27:49+08:00
lastmod: 2026-06-19T22:27:49+08:00
url: hotspot-options
categories:
  - language
tags:
  - hotspot
  - java
  - jvm
  - remix
  - AI-assisted
---

## 背景

本文汇总 **OpenJDK HotSpot** 常用启动参数（`-`、`-X`、`-XX`）。这些开关 **不是 JVM 规范的一部分**，其他实现（OpenJ9 等）名称与语义可能不同。

JVM 生态选型见 [jvm](./jvm.md)；HotSpot 架构索引见 [hotspot](./hotspot.md)。GC 算法细节见 [java-gc](./java-gc.md)；JIT 与分层编译见 [jvm-compiler](../../cs/jvm-compiler.md)。

## 参数分类

HotSpot 命令行参数分三类：

| 类型 | 前缀 | 说明 |
| ---- | ---- | ---- |
| 标准参数 | `-` | 规范要求所有实现支持，如 `-version` |
| 非标准参数 | `-X` | 实现相关，如 `-Xms`、`-Xmx`；不保证跨版本兼容 |
| 不稳定参数 | `-XX` | HotSpot 专有调优项，可能无预警变更或移除 |

查看当前生效的 HotSpot 参数：

```bash
java -XX:+PrintCommandLineFlags -version
java -XX:+PrintFlagsFinal -version | grep -i gc
```

## 堆与元空间

### 堆大小

| 参数 | 别名 | 说明 |
| ---- | ---- | ---- |
| `-Xms<size>` | `-XX:InitialHeapSize` | 初始堆大小；常与 `-Xmx` 设相同，避免运行期扩堆 |
| `-Xmx<size>` | `-XX:MaxHeapSize` | 最大堆大小 |
| `-Xmn<size>` | `-XX:NewSize` 等 | 年轻代大小（eden + 2×survivor）；显式设置会干扰 G1 等区域自适应，现代应用更常用比例或交给 G1 自动调整 |

`<size>` 可用 `k`/`m`/`g`（如 `-Xmx2g`）。

```bash
java -Xms512m -Xmx2g MyApp
```

### 分代比例（传统分代 GC）

对 **G1、ZGC** 等，以下参数意义减弱或无效；主要用于 Parallel GC、CMS 等经典分代收集器：

| 参数 | 说明 |
| ---- | ---- |
| `-XX:NewRatio=n` | 年轻代 : 老年代 = 1 : n |
| `-XX:SurvivorRatio=n` | Eden : 单个 Survivor = n : 1（两个 Survivor） |
| `-XX:MaxTenuringThreshold=n` | 对象在 Survivor 中经历 Minor GC 的次数上限，超过则晋升老年代 |

### 元空间（JDK 8+）

JDK 8 起永久代（PermGen）移除，类元数据进入 **元空间**（本地内存）：

| 参数 | 说明 |
| ---- | ---- |
| `-XX:MetaspaceSize` | 元空间初始阈值；达到后可能触发 GC |
| `-XX:MaxMetaspaceSize` | 元空间上限 |

> JDK 7 及更早使用 `-XX:PermSize` / `-XX:MaxPermSize`，已废弃。

### 堆外与直接内存

| 参数 | 说明 |
| ---- | ---- |
| `-XX:MaxDirectMemorySize` | `DirectByteBuffer` 等堆外内存上限 |

## 线程栈

| 参数 | 说明 |
| ---- | ---- |
| `-Xss<size>` | 每线程栈大小；`-Xss` 为跨实现常用写法 |
| `-XX:ThreadStackSize` | HotSpot 专有等价项 |

Linux x64 上 HotSpot 默认栈约 **1MB**。栈过小易 `StackOverflowError`；过大则同进程可创建的线程数减少。线程栈内存向 **操作系统** 申请，不属于 Java 堆。

## 对象指针压缩（64 位）

| 参数 | 说明 |
| ---- | ---- |
| `-XX:+UseCompressedOops` | 压缩普通对象指针（默认在 64 位堆 < 32GB 时常开） |
| `-XX:+UseCompressedClassPointers` | 压缩类指针 |

## 垃圾收集器选择

通过 `-XX:+Use...GC` 选择收集器（布尔开关 **不要** 写 `=true`）：

| 参数 | 收集器 | 备注 |
| ---- | ------ | ---- |
| `-XX:+UseSerialGC` | Serial | 单线程，小堆或客户端 |
| `-XX:+UseParallelGC` | Parallel（吞吐优先） | JDK 8 默认 Server 之一 |
| `-XX:+UseG1GC` | G1 | JDK 9+ 默认；JDK 21+ 仍为主流选择之一 |
| `-XX:+UseZGC` | ZGC | 低延迟；JDK 23+ 默认分代 |
| `-XX:+UseShenandoahGC` | Shenandoah | 低延迟；JDK 25 起分代模式正式可用 |
| `-XX:+UseConcMarkSweepGC` | CMS | **JDK 14 移除**，仅旧版本文档参考 |

并行度与停顿目标（Parallel / G1 等）：

| 参数 | 说明 |
| ---- | ---- |
| `-XX:ParallelGCThreads=n` | 并行 GC 线程数 |
| `-XX:MaxGCPauseMillis=n` | G1 等：期望最大停顿毫秒数（启发式，非硬保证） |
| `-XX:GCTimeRatio=n` | GC 时间占比目标，约 1/(1+n) |

显式 GC 与 RMI：

| 参数 | 说明 |
| ---- | ---- |
| `-XX:+DisableExplicitGC` | 忽略 `System.gc()` |
| `-Dsun.rmi.dgc.server.gcInterval=ms` | RMI 分布式 GC 间隔（默认较短，可能频繁触发 GC） |

## GC 日志

### 现代写法（JDK 9+，推荐）

统一用 **Unified JVM Logging**（`-Xlog`）：

```bash
# 控制台输出 GC 详情
java -Xlog:gc*:stdout:time,uptime,level,tags MyApp

# 写入文件
java -Xlog:gc*:file=gc.log:time,uptime,level,tags MyApp
```

### 旧参数（已废弃，仅供读老日志）

| 旧参数 | 替代 |
| ---- | ---- |
| `-XX:+PrintGC`、`-verbose:gc` | `-Xlog:gc` |
| `-XX:+PrintGCDetails` | `-Xlog:gc*` |
| `-XX:+PrintGCTimeStamps` | `-Xlog` 的 `time` / `uptime` |
| `-Xloggc:file` | `-Xlog:gc*:file=...` |

GC 日志分析与 `jstat` 见 [java-gc-jstat](./java-gc-jstat.md)。

## JIT 与编译

| 参数 | 说明 |
| ---- | ---- |
| `-XX:CICompilerCount=n` | JIT 编译器后台线程数 |
| `-XX:+TieredCompilation` | 分层编译（默认开启） |
| `-XX:-TieredCompilation` | 关闭分层，解释器 + C2 |
| `-XX:TieredStopAtLevel=n` | 最高编译级别，1=C1，4=C2 |
| `-XX:+PrintCompilation` | 控制台打印编译事件 |
| `-XX:+LogCompilation` | 详细编译日志（需配合 `-XX:LogFile=`） |
| `-XX:InitialCodeCacheSize` | 代码缓存初始大小 |
| `-XX:ReservedCodeCacheSize` | 代码缓存上限；满后可能降级为仅解释执行 |
| `-XX:+UseCodeCacheFlushing` | 代码缓存满时尝试淘汰部分已编译代码 |

详见 [jvm-compiler](../../cs/jvm-compiler.md)。

## 诊断与排错

### 堆转储与 OOM

| 参数 | 说明 |
| ---- | ---- |
| `-XX:+HeapDumpOnOutOfMemoryError` | OOM 时自动写 heap dump |
| `-XX:HeapDumpPath=<path>` | dump 文件路径 |

### 类加载日志

| 参数 | 说明 |
| ---- | ---- |
| `-Xlog:class+load=info` | 类加载日志（JDK 16+ 替代 `-XX:+TraceClassLoading`） |

### 常用 JDK 工具（HotSpot）

| 工具 | 用途 |
| ---- | ---- |
| `jcmd <pid> VM.flags` | 查看生效标志 |
| `jmap -heap <pid>` | 堆配置与各区域使用 |
| `jstat -gcutil <pid> 1s` | GC 统计 |
| `jcmd <pid> GC.heap_dump` | 手动 heap dump |

## VM Thread 与 CPU 100%

**VM Thread** 是 HotSpot 内部线程，负责 GC 协调、部分对象分配与 safepoint 等。若 `top` / 线程 dump 显示 **VM Thread 占满 CPU**，且伴随老年代已满，常见原因是 **短时间内大量对象分配** 导致 GC 跟不上。思路：看 GC 日志、堆使用与分配速率，而非只盯业务线程。

## 典型示例

```bash
# 服务端常见起点：固定堆、G1、OOM 时 dump、GC 日志
java -Xms2g -Xmx2g \
  -XX:+UseG1GC \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/tmp/heap.hprof \
  -Xlog:gc*:file=gc.log:time,uptime,level,tags \
  -jar app.jar
```

调优应结合压测与 GC 日志迭代，避免照搬 JDK 5/6 时代的 `-Xmn` + CMS 配方。

## 参考

- [Java HotSpot VM Options（JDK 21）](https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html)
- [Unified JVM Logging](https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html#enable-logging-with-the-application-class-data-sharing-appcds-feature)
- 本站：[java-gc](./java-gc.md)、[hotspot](./hotspot.md)
