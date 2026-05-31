---
title: Java Attach API
author: "-"
date: 2026-05-30T19:45:11+08:00
lastmod: 2026-05-31T07:36:44+08:00
url: attach-api
categories:
  - language
tags:
  - AI-assisted
  - attach-api
  - java
  - javaagent
  - jcmd
  - jvm
  - remix
---

## 背景

JDK 8 生产排查里，[BTrace](./btrace.md)、[jcmd](./jcmd.md) 等工具都需要在 **不重启业务 JVM** 的前提下与之交互。底层机制是 JDK 自带的 **Attach API**（`com.sun.tools.attach`，`jdk.attach` 模块）：一个本地进程通过 PID 连上目标 HotSpot JVM，再在这条 attach 通道上发送不同种类的请求。

Attach 不是只有 `loadAgent` 一种用法。[jcmd](./jcmd.md) 的 `Thread.print`、`JFR.start` 等走 **JVM 内置 Diagnostic Command**，一般 **不需要** 再加载外部 agent JAR；[BTrace](./btrace.md) 等才典型地 `loadAgent`。

本文说明 Attach 通道、公开 API、与 jcmd / BTrace 的关系。概念总图见 [Java 领域知识关系图](./java-knowledge-map.md)。容器、新版 JDK 注意点见文末。

## 是什么

Attach 让**已启动的 HotSpot JVM** 在运行中被另一进程「挂上」：

- 连接入口：`VirtualMachine.attach(pid)`（及 `AttachProvider` 发现 JVM）
- 通道上可发多种 attach **操作**（见下节），不限于 `loadAgent`
- 其中一类操作会加载外部 Agent JAR，调用 **`agentmain`**（启动时 `-javaagent` 则走 **`premain`**）

不是远程 RPC：必须在**本机**（或共享进程命名空间，见文末），且一般要求**与目标 JVM 相同的有效用户/组**。

## 版本历史

**Attach API 自 Java 6（JDK 6）起提供。** `com.sun.tools.attach` 包（如 `VirtualMachine`、`loadAgent`）官方标注 Since 1.6，用于在目标 JVM **已运行**时动态 attach 并加载 Agent。

| 版本 | 相关内容 |
| ---- | -------- |
| JDK 6 | Attach API（`VirtualMachine.attach`、`loadAgent` 等） |
| JDK 7 | [jcmd](./jcmd.md) 与 Diagnostic Command 框架（[JEP 137](https://openjdk.org/jeps/137)），在 attach 通道上触发内置诊断命令 |
| JDK 9 | API 收入 **`jdk.attach`** 模块；模块化项目引用时常需 `requires jdk.attach` |

注意：动态 attach 从 **JDK 6** 就有；**jcmd / 内置 Diagnostic Command 是 JDK 7 起**叠在 attach 之上的能力，不等于 Attach API 本身到 JDK 7 才出现。JDK 8 上的 BTrace、[jcmd](./jcmd.md) 均建立在此基础之上。

早期实现主要面向 **HotSpot**；目标 JVM 若带 `-XX:+DisableAttachMechanism` 则无法 attach。

## 一条通道，两类典型用法

```text
Attach 通道（.java_pid socket 等）
  ├─ 执行内置 Diagnostic Command   ← jcmd：Thread.print、JFR.start、GC.heap_dump …
  └─ loadAgent 外部 JAR              ← BTrace、Arthas、async-profiler …
```

| 能力 | JVM 内置？ | 典型工具 | 是否 loadAgent |
| ---- | ---------- | -------- | -------------- |
| 线程栈 `Thread.print` | 是 | `jcmd` | 否 |
| 堆 dump `GC.heap_dump` | 是 | `jcmd` | 否 |
| JFR `JFR.start` 等 | 是（JDK 8 需解锁商业特性） | `jcmd` | 否 |
| 自定义方法探针 | 否 | BTrace | 是 |
| 交互式诊断命令 | 否 | Arthas | 是 |
| CPU/alloc 采样（async-profiler） | 否 | async-profiler | 是 |

内置诊断不是「挂了一个诊断 agent.jar」，而是 HotSpot 启动时就有 **AttachListener** 与 **Diagnostic Command（DCmd）框架**（[JEP 137](https://openjdk.org/jeps/137)），`jcmd` attach 上去后直接触发这些命令。

## 公开 Attach API

应用开发者能稳定依赖的主要是 `jdk.attach` 包：

```java
import com.sun.tools.attach.VirtualMachine;

VirtualMachine vm = VirtualMachine.attach(pid);
try {
    vm.loadAgent("/path/to/agent.jar", "key=value");
} finally {
    vm.detach();
}
```

| 方法 | 作用 |
| ---- | ---- |
| `VirtualMachine.attach(pid)` |  按操作系统 PID 连接目标 JVM |
| `loadAgent(jar, args)` | 加载外部 Agent JAR，调用 `agentmain` |
| `loadAgentLibrary` / `loadAgentPath` | 加载本地库 Agent（JVMTI） |
| `detach()` | 断开 attach 连接（不一定会卸载已加载的 Agent） |
| `AttachProvider` / `VirtualMachine.list()` | 发现本机可 attach 的 JVM |

**没有**对外公开的 `runDiagnostic("Thread.print")` 之类 API。`jcmd` 发 Diagnostic Command 用的是 JDK **内部** 类 `sun.tools.attach.HotSpotVirtualMachine`（非标准 API，第三方不宜依赖）。

## jcmd 如何通过 Attach 调用 Diagnostic Command

[jcmd](./jcmd.md) 列进程、发 `Thread.print` / `JFR.start` 等，底层都走 attach，但 **不走 `loadAgent`**。

调用链（简化）：

```text
jcmd 客户端
  │ VirtualMachine.attach(pid)                    ← 公开 Attach API
  │ HotSpotVirtualMachine.executeJCmd("Thread.print")  ← JDK 内部
  │ native execute("jcmd", "Thread.print")
  ▼
目标 JVM：AttachListener 收到操作类型 "jcmd"
  │ DCmd::parse_and_execute("Thread.print", ...)   ← HotSpot 内置 DCmd 框架
  ▼
结果经 attach 通道返回终端
```

JDK 内部等价逻辑（`sun.tools.attach.HotSpotVirtualMachine`，仅供理解）：

```java
public InputStream executeJCmd(String command) throws IOException {
    return executeCommand("jcmd", command);
}
```

同一 attach 通道上还有其它操作码，例如 `"load"`（对应 `loadAgent`）、`"properties"`（读系统属性）等；**Diagnostic Command 与 loadAgent 是不同 attach 操作，不是同一 API 的两种配置**。

`jcmd -l` 则通过 **AttachProvider** 扫描 attach 标记发现 JVM，同样不是 `loadAgent`，也与 `ps` 扫 `/proc` 不同（见 [jcmd](./jcmd.md)）。

## premain 与 agentmain

| 方式 | 何时加载 | 入口 | 典型场景 |
| ---- | -------- | ---- | -------- |
| `-javaagent:agent.jar` | JVM 启动 | `premain` | 启动即埋点、AOP LTW |
| Attach `loadAgent` | JVM 已运行 | `agentmain` | BTrace、Arthas、async-profiler |

Agent JAR 的 `MANIFEST.MF` 需包含 `Agent-Class`（`agentmain`）或 `Premain-Class`（`premain`）。

## Linux 上的 attach 标记

HotSpot 在 **`java.io.tmpdir`**（Linux 上常见 `/tmp`）创建 **attach 专用标记**，常见路径为 `/tmp/.java_pid<pid>`。表面像文件名，实际是 **UNIX domain socket**，供 attach 客户端连上目标 JVM 内的 AttachListener。

该标记 **专门服务于 Attach 机制**（`jcmd`、`VirtualMachine.attach`、`loadAgent` 等），不是泛用的 Java 临时文件。

| 路径示例 | 用途 |
| -------- | ---- |
| `/tmp/.java_pid<pid>` | Attach API / attach 通道 |
| `/tmp/hsperfdata_<user>/<pid>` | 性能计数器共享；[jps](./java-command-jps.md) 等常靠它列进程 |

注意：

- 目录可被 `-Djava.io.tmpdir=...` 改变，不限于 `/tmp`
- `-XX:+DisableAttachMechanism` 时可能不创建标记，attach 与 `jcmd -l` 会失败
- 容器内标记在容器自己的 tmp，宿主机 `jcmd -l` 往往看不到（[jcmd](./jcmd.md)）

## 谁在用 Attach API

| 工具 | attach 之后做什么 |
| ---- | ----------------- |
| [jcmd](./jcmd.md) | 发内置 Diagnostic Command（线程栈、堆 dump、JFR 等） |
| [BTrace](./btrace.md) | `loadAgent(btrace-agent.jar)`，Socket 下发探针 |
| Arthas | `loadAgent`，提供 `trace` / `watch` 等 |
| async-profiler | `loadAgent`，CPU/alloc 采样 |

上层协议不同，但「连上目标 JVM」这一步共用 attach 通道。

## 与 BTrace 的关系（简图）

```text
客户端进程（btrace 命令）
  │ VirtualMachine.attach(pid)
  │ loadAgent("btrace-agent.jar")     ← attach 操作 "load"
  ▼
业务 JVM（agentmain → Instrumentation → ASM 织入）
  │ Socket：脚本/输出（BTrace 特有）
  ▼
客户端终端
```

BTrace 脚本编译、Socket、探针织入在 Agent 之上，见 [BTrace Attach 原理](./btrace.md)。

## 限制与常见错误

- **同一用户**：否则 `Unable to attach to target VM`
- **本机 attach**：不能跨机器 attach（远程需 SSH 再执行工具）
- **`-XX:+DisableAttachMechanism`**：目标 JVM 禁用 attach 时失败
- **非 HotSpot / 非 Java 进程**：attach 无效
- **loadAgent 之后**：Agent 是否可完全卸载取决于实现；生产上常按「可能需重启业务」处理

## 参考

- [VirtualMachine (Java SE)](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.attach/com/sun/tools/attach/VirtualMachine.html)
- [JEP 137: Diagnostic-Command Framework](https://openjdk.org/jeps/137)
- [java.lang.instrument](https://docs.oracle.com/en/java/javase/21/docs/api/java.instrument/java/lang/instrument/package-summary.html)
- [jcmd](./jcmd.md)
- [BTrace](./btrace.md)

## 其它 JDK 版本

### JDK 21 及以后：动态 Agent 加载

运行时 **`loadAgent`** 可能要求目标 JVM 开启：

```bash
-XX:+EnableDynamicAgentLoading
```

主要影响 BTrace、Arthas、async-profiler 等 **loadAgent** 路径；`jcmd` 内置 Diagnostic Command 也依赖 attach 通道，若完全禁用 attach 同样不可用。

### 容器与 Kubernetes

- **推荐**：`docker exec` 进入**跑 Java 的业务容器**，在同一命名空间内 `jcmd -l` / `btrace <PID> ...`
- **多阶段镜像**：从 `btrace/btrace` 等镜像 **COPY** 工具到业务 JDK 镜像，见 [BTrace 安装](./btrace.md)
- **Sidecar**：同 Pod 需 `shareProcessNamespace: true`，并常需 `SYS_PTRACE`

Attach 不提供跨容器网络 attach；可见性由进程/PID 命名空间决定。

### 工具选型

升级 JDK 后，列进程仍多用 [jcmd -l](./jcmd.md)；内置诊断与 loadAgent 系工具的分工见 [生产环境诊断工具选型](./java-production-diagnostics-tooling.md)。
