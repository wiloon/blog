---
title: jcmd
author: "-"
date: 2017-02-06T04:58:07+00:00
lastmod: 2026-05-30T19:45:37+08:00
url: jcmd
categories:
  - language
tags:
  - java
  - jcmd
  - jvm
  - remix
  - AI-assisted
---

## 背景

本文记录 JDK 8 生产环境下的用法：在主机上查看正在运行的 Java 进程 PID，并向目标 JVM 发送诊断命令（线程栈、堆 dump、JVM 参数等）。常与 [BTrace](/btrace) attach 前配合使用（`jcmd -l` 列进程）。

New Features in JDK7 update 4

JRockit command line utility JRCMD (JRockit Command). JRCMD was a command line tool to enumerate the Java processes running on the local machine, and to send commands (referred to as "Diagnostic Commands") to them. JRCMD has been renamed JCMD (Java Command).

jcmd 用于向正在运行的 JVM 发送诊断信息请求，从 JDK 1.7 开始提供，可以说是 jstack 和 jps 的结合体。

## 列出 Java 进程

不带参数等价于 `jcmd -l`，列出本机 Java 进程的 PID、主类名和启动命令行：

```bash
jcmd
# 或
jcmd -l
```

要求：在与 JVM **同一台机器**、**同一有效用户/组** 下执行（与启动该 JVM 的用户一致）。

## 常用命令

语法：`jcmd [ pid | main-class ] command [ arguments ]`

```bash
# 列出该 JVM 支持的诊断命令
jcmd PID help

# 某一命令的帮助
jcmd PID help ManagementAgent.start

# 线程栈
jcmd PID Thread.print

# 线程栈 + 锁信息
jcmd PID Thread.print -l

# 堆 dump（HPROF），建议用绝对路径与 .hprof 扩展名
jcmd PID GC.heap_dump /tmp/dump.hprof

# 堆直方图（存活对象数目）
jcmd PID GC.class_histogram

# 启动命令行
jcmd PID VM.command_line

# JVM 参数（如 -XX:MaxHeapSize）
jcmd PID VM.flags

# 运行时长
jcmd PID VM.uptime

# 系统属性
jcmd PID VM.system_properties

# 版本
jcmd PID VM.version
```

### 与 jstack、kill -3 的关系

JDK 8 时代也可单独使用：

```bash
jstack <PID>      # 线程栈
kill -3 <PID>     # 仅 Linux，让 JVM 把线程栈打到标准错误/日志
```

故障排查时更推荐统一走 `jcmd PID Thread.print`，与后续堆、JFR 等命令同一工具链。

### GC 相关

```bash
jcmd PID GC.heap_dump <filename>   # 同 jmap dump
jcmd PID GC.class_histogram        # 同 jmap -histo，浅尺寸
jcmd PID GC.run_finalization
jcmd PID GC.run                    # 建议 GC，不保证立即执行
jcmd PID GC.rotate_log             # 轮转 GC 日志
```

`GC.class_stats` 需在启动时加 `-XX:+UnlockDiagnosticVMOptions`。

### NMT（Native Memory Tracking）

```bash
jcmd PID VM.native_memory
```

### JMX 远程

```bash
jcmd PID ManagementAgent.stop
jcmd PID ManagementAgent.start_local
jcmd PID ManagementAgent.start
```

### JFR（JDK 8）

JDK 8 上 JFR 属于商业特性，需先解锁：

```bash
jcmd PID VM.check_commercial_features
jcmd PID VM.unlock_commercial_features
jcmd PID JFR.check
jcmd PID JFR.start name=jfr0 delay=10s duration=10s filename=jfr0.jfr
jcmd PID JFR.dump
jcmd PID JFR.stop
```

详见 [Oracle JDK 8 故障排查：jcmd](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr007.html)。

## 参考（JDK 8）

- [rowkey: Java troubleshooting](http://www.rowkey.me/blog/2016/11/16/java-trouble-shooting/)
- [hirt.se: jcmd](http://hirt.se/blog/?p=211)
- [生产环境诊断工具选型](/production-diagnostics-tooling)

## 其它 JDK 版本

以下供 JDK 升级后参考；正文以上以 JDK 8 为准。

### 列出 Java 进程：Java 26 仍是 jcmd

在 Java 26 等较新 JDK 上，**查看本机运行中的 Java 进程仍推荐 `jcmd` / `jcmd -l`**，没有新的官方替代工具。Oracle 故障排查文档建议诊断优先用 `jcmd`，而不是单独依赖实验性的 `jstack`、`jinfo`、`jmap`。

```bash
jcmd -l
```

变化在于：`jcmd` 承担更多诊断职责（JFR、统一子命令），而不是换掉「列 PID」这一步。

### 与 jps、ps 的分工

| 场景 | 工具 | 说明 |
| ---- | ---- | ---- |
| 本机列 Java 进程（推荐） | `jcmd -l` | PID + 主类 + 完整启动参数 |
| 只要 PID + 短类名 | `jps -l` | 仍随 JDK 提供，输出更简 |
| 操作系统层面 | `ps`、`pgrep -f java` | 不区分是否 JVM；容器内有时需先用 |
| Kubernetes | `kubectl exec … jcmd -l` | 需在 Pod 内执行 |

`jps` 未被废弃，但官方叙事中心在 `jcmd`；列完进程后的线程栈、堆 dump、JFR 等也应继续用同一 `jcmd`，无需换工具链。

### 容器与 Docker

JDK 26 手册说明：若 JVM 运行在**独立的 Docker 进程**中，宿主机上的 `jcmd -l` **可能列不出**该进程，需用 `ps` 查 PID，或进入容器后再执行 `jcmd`。

#### 为什么 ps 能看到，jcmd -l 却列不出

`ps` 和 `jcmd -l` 找的不是同一类东西：

- `ps` 读宿主机 `/proc`，列出内核上的所有进程。容器里的 Java 仍是普通 Linux 进程，有**宿主机 PID**，所以 `ps aux | grep java` 通常能看到。
- `jcmd -l` 不走全量扫 PID，而是通过 [Attach API](/attach-api) 发现 JVM：在当前环境能访问的路径里找 attach 标记（Linux 上常见为 `/tmp/.java_pid<pid>` 一类 socket），再确认是否可对话的 HotSpot JVM。

容器有 **mount namespace** 隔离：JVM 在容器内创建的 attach 文件在**容器 `/tmp`**，不在宿主机 `/tmp`。宿主机 `jcmd -l` 扫描的是本机路径，因此发现不了。较新 JDK 还可能主动跳过判定为在 Docker/cgroup 内的 JVM。

| | `ps` | `jcmd -l` |
| --- | --- | --- |
| 数据来源 | 宿主机 `/proc` | attach 标记 + Attach API |
| 是否依赖 JVM 配合 | 否 | 是 |
| attach 文件位置 | 不关心 | 多在容器内 `/tmp` |

#### 知道宿主机 PID 后能否 jcmd

`jcmd -l` 列不出，不等于完全不能 attach。若用 `ps` 已得到宿主机 PID，有时可：

```bash
jcmd <宿主机PID> Thread.print
```

能否成功取决于用户/权限是否一致、能否经 `/proc/<pid>/root/tmp/…` 连上 attach socket、SELinux 等限制。生产上更稳妥的是**进容器再执行**：

```bash
kubectl exec -it <pod> -- jcmd -l
```

概括：`ps` 看「整栋楼有哪些房间」；`jcmd -l` 只认「从当前大厅能走过去、且挂了 JVM 门牌」的进程——门牌在容器里面，站在宿主机大厅自动巡楼会漏掉。

### JFR（JDK 11 及以后）

从 JDK 11 起 JFR **免费**，无需 `VM.unlock_commercial_features`。可直接：

```bash
jcmd PID help
jcmd PID JFR.start name=rec duration=60s filename=/tmp/rec.jfr
jcmd PID JFR.dump
jcmd PID JFR.stop
```

见 [Java Flight Recorder](/java-flight-recorder-jfr)。

### 升级后的使用建议

只查「这台机器上有哪些 Java 进程」：

```bash
jcmd -l              # 首选
jps -lv              # 备选，输出更短
ps aux | grep java   # 容器或权限异常时兜底
```

列 PID 后做诊断（与 JDK 8 相同入口，子命令以 `jcmd PID help` 为准）：

```bash
jcmd <PID> Thread.print
jcmd <PID> GC.heap_dump /tmp/dump.hprof
jcmd <PID> JFR.start ...
```

与 BTrace、Arthas、async-profiler 等 attach 类工具的关系见 [生产环境诊断工具选型](/production-diagnostics-tooling)。

### 参考（其它 JDK 版本）

- [The jcmd Command (Java SE 26)](https://docs.oracle.com/en/java/javase/26/docs/specs/man/jcmd.html)
- [Diagnostic Tools (Java SE 17+)](https://docs.oracle.com/en/java/javase/17/troubleshoot/diagnostic-tools.html)
