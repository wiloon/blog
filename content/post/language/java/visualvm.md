---
title: "VisualVM: 线程与堆内存监控分析工具"
author: "-"
date: 2015-11-04T02:02:03+00:00
lastmod: 2026-07-16T05:20:05+08:00
url: visualvm
categories:
  - language
tags:
  - java
  - jvm
  - visualvm
  - thread-dump
  - jmx
  - remix
  - AI-assisted
---

## VisualVM 是什么

VisualVM 是一个图形化的 JVM 监控与分析工具，可以查看应用程序的 CPU、内存占用，监控线程状态，生成线程转储（Thread Dump）或堆转储（Heap Dump），跟踪内存泄漏，监控垃圾回收，并支持简单的 CPU/内存 profiling。它也能浏览和操作 MBean，配合 JMX 做远程监控。

VisualVM 曾在 JDK 6 Update 7 之后随 Sun/Oracle JDK 一起分发；从 **JDK 9 起被移出 JDK 发行包**，独立成开源项目 [visualvm.github.io](https://visualvm.github.io/)，需要单独下载安装，本身要求 JDK 8 及以上运行，但可以监控 JDK 1.4 以上版本的目标进程。

## 安装与启动

从 [visualvm.github.io](https://visualvm.github.io/) 下载对应平台的安装包，解压后运行 `visualvm`（Windows 下是 `visualvm.exe`）。

如果 VisualVM 找不到本机 JDK，用 `-jdkhome` 显式指定：

```bash
visualvm -jdkhome /path/to/jdk
```

插件默认安装在用户目录下，例如 Windows：

```text
%APPDATA%\VisualVM\<version>
```

## 线程监控与 Thread Dump

启动 VisualVM 后，"应用程序 > 本地" 节点会列出本机正在运行的 Java 进程。双击目标进程，切换到「线程」标签页，可以看到各线程的实时状态跟踪。

点击「线程 Dump」按钮会生成当前时刻的线程转储文件，里面包含每个线程的调用栈、锁等待对象等信息，用来定位线程阻塞、死锁的位置；关于线程转储的字段含义与死锁排查方法，参考 [jstack](../../cs/jstack.md)。

### VisualVM 线程状态

| 状态 | 说明 |
| ---- | ---- |
| Running | 正在运行 / 可运行（runnable） |
| Sleeping | 线程调用了 `Thread.sleep()` |
| Wait | 线程处于 `wait` 或 `timed_waiting` |
| Park | 线程调用了 `LockSupport.park()` |
| Monitor | 线程被 monitor 锁阻塞（blocked） |

## 远程监控

VisualVM 也可以通过 JMX 或 `jstatd` 监控远程 JVM 进程，思路和本地类似，多了一步网络连接配置。

### 用 jstatd 暴露远程 JVM 统计信息

1. 新建一个 `jstatd.all.policy` 策略文件，避免 `jstatd` 启动时报权限异常：

   ```text
   grant codebase "file:${java.home}/../lib/tools.jar" {
       permission java.security.AllPermission;
   };
   ```

2. 检查默认端口（1099）是否被占用：

   ```bash
   netstat -ano | grep -i 1099
   ```

3. 端口被占用时指定其他端口启动：

   ```bash
   rmiregistry 2020 & jstatd -J-Djava.security.policy=jstatd.all.policy -p 2020
   ```

### 用 JMX 远程连接

1. 在目标 JVM 启动参数里开放 JMX 端口（生产环境务必开启鉴权与 TLS，以下为最简示例）：

   ```bash
   JAVA_OPTS="-Dcom.sun.management.jmxremote.port=2899 \
   -Dcom.sun.management.jmxremote.ssl=false \
   -Dcom.sun.management.jmxremote.authenticate=false \
   -Djava.rmi.server.hostname=<host-ip>"
   ```

2. 检查端口是否已监听：

   ```bash
   netstat -a | grep -i 2899
   ```

3. 在 VisualVM 中「添加 JMX 连接」，填入目标地址和端口即可看到远程进程的监控数据。

## JDK 26 时代还推荐用 VisualVM 吗

VisualVM 项目仍在维护，本地开发机上临时看看线程状态、堆占用、做一次快速的 heap/thread dump，依然好用，尤其是不想额外安装工具时的顺手选择。

但作为现代 JDK 诊断栈的**主力工具**，它已经不是首选：

- **CPU 热点分析**：更推荐 async-profiler，基于硬件/软件事件采样，不受安全点偏差影响，还能直接产出火焰图；VisualVM 内置的 CPU profiler 依赖字节码插桩，开销大、数据也不够准。
- **GC、锁、内存分配、虚拟线程 pinning 等**：官方标准做法是 [Java Flight Recorder](./java-flight-recorder-jfr.md)（JFR），持续录制、开销低，再用 JDK Mission Control（JMC）离线分析，而不是 VisualVM 的实时图表。
- **命令行诊断入口**：Oracle 现在统一推荐 [jcmd](./jcmd.md) 而不是 `jstack`/`jmap` 等独立小工具。

更完整的现代诊断工具选型对比见 [Java 生产环境诊断工具选型](./java-production-diagnostics-tooling.md)。

结论：VisualVM 可以留着应急，但生产环境的常态化监控和性能分析，JDK 26 下更推荐 JFR + JMC + async-profiler 这套组合。

## 参考

- [VisualVM 官网](https://visualvm.github.io/)
- [VisualVM 插件中心](https://visualvm.github.io/plugins.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-16 | 文件重命名为 `visualvm.md`；标题、url、分类改为 `language`；标签由 `reprint` 改为 `remix` + `AI-assisted`；全文重新整理为分节结构；删除 YourKit 段落；补充「JDK 26 时代还推荐用 VisualVM 吗」一节并内链 JFR、jcmd、生产诊断工具选型文章 | 原文中文文件名不合规，内容是 WordPress 导入的碎片化段落，且未反映 VisualVM 自 JDK 9 起移出 JDK 发行包的现状 |
