---
title: Java 诊断工具 BTrace
author: "-"
date: 2018-06-02T03:42:52+00:00
lastmod: 2026-05-31T07:36:44+08:00
url: btrace
categories:
  - language
tags:
  - java
  - btrace
  - jvm
  - remix
  - AI-assisted
---

## 背景

本文记录的是 JDK 8 生产环境下的实践：线上出现问题时，在不改代码、不重启的前提下，用 BTrace attach 到运行中的 JVM，按条件过滤慢方法并持续输出。

[BTrace](https://github.com/btraceio/btrace)

概念与相关文章的关系见 [Java 领域知识关系图](/java-knowledge-map)。

### 何时需要 BTrace（生产动机）

| 动机 | 说明 |
| ---- | ---- |
| 不能停机 | 滚动重启成本高或 SLA 不允许 |
| **保留故障现场** | 重启后偶现问题、特定请求参数、堆内对象态、当时流量下的慢调用往往 **难以复现**；需要在 **故障仍在发生时** 对当前 JVM 取样 |
| 观测而非热修 | BTrace 用于 **慢调用过滤、参数、耗时、调用路径** 等可观测数据，不是用 agent 临时改业务逻辑修 Bug（机制上 agent 能改字节码，但 BTrace 产品侧用脚本校验限制为安全探针） |

临时排查可配合 [生产环境诊断工具选型](/production-diagnostics-tooling)（Arthas、JFR 等）；BTrace 适合 **脚本化、持续输出** 的采集。

## 安装

BTrace **不是**单个原生二进制，而是 **Java 工具发行包**（压缩包 + shell 脚本 + JAR），运行时依赖本机 **JDK**。

从 [GitHub Releases](https://github.com/btraceio/btrace/releases) 下载 `btrace-bin.tar.gz` 或 `.zip`，解压后大致结构：

```text
btrace/
├── bin/
│   ├── btrace      # 客户端：attach 并下发脚本
│   ├── btracec     # 编译 BTrace 脚本
│   └── btracer     # 启动时带 agent 运行应用
└── libs/           # client、agent、boot 等 JAR
```

JDK 8 时代常见做法：

```bash
tar -xzf btrace-2.x.tar.gz
export BTRACE_HOME=/path/to/btrace
export PATH=$BTRACE_HOME/bin:$PATH
btrace -h
```

文档中的 `/bin/btrace <PID> ...` 即上述 `bin/btrace` 脚本（内部用 `java` 启动 client JAR）。

较新安装方式（JBang、SDKMan、Docker 等）见文末「其它 JDK 版本」。

## 运行依赖与架构

BTrace **全程依赖 Java / JVM**，且涉及 **两个进程、两个 JVM**：

| 角色 | 是什么 | 依赖 |
| ---- | ------ | ---- |
| 客户端 | 执行 `btrace` 命令的 Java 进程 | 本机 JDK，跑 client JAR |
| 业务 JVM | 正在运行的应用 | 被 attach 的 HotSpot JVM |
| Agent | 加载进业务 JVM 的 `btrace-agent.jar` | 在业务进程内执行织入与探针 |

**不是**像 `tcpdump` 那样不依赖 Java 的原生工具。客户端与目标 JVM 通常在同一台机器、可用同一套 JDK 安装；版本不必完全一致，但需在目标 JDK 上实测 Agent 兼容性。

整体链路：

```text
客户端 JVM（btrace 命令）
  │ ① Attach API：loadAgent(btrace-agent.jar)  ──►  业务 JVM（Agent 启动）
  │ ② Socket：下发脚本/探针定义，回收 println 输出
  ▼
业务 JVM 内：Agent 用 ASM + Instrumentation 织入业务类；探针在业务线程里执行
```

注意：

- 通过 Attach 进入业务 JVM 的是 **Agent JAR**，**不是**把脚本编译成 jar 再 attach 进去。
- Agent 是加载进业务 JVM 的一整套代码（含 Socket 服务等，可能起监听线程），**不等于**业务 JVM 里的「一个线程」；探针跑在业务方法调用栈上（如 `method0` 返回前）。
- Socket 是 **两个进程之间** 的通信，不是两个 JVM 内部随便传数据。

## 概念厘清

本节汇总 attach、Agent、ClassLoader、线程与开发热替换等易混点（与 [java-asm](/java-asm)、[Attach API](/attach-api) 一致）。

### loadAgent 之后：不是 `main`，是 `agentmain`

| 普通 JAR | Agent JAR（`btrace-agent.jar`） |
| -------- | ------------------------------- |
| manifest `Main-Class` → `public static void main` | manifest `Agent-Class` → `public static void agentmain(String, Instrumentation)` |
| `java -jar app.jar` | [Attach API](/attach-api) `loadAgent` 或启动时 `-javaagent`（`premain`） |

`loadAgent` 由 **业务 JVM 进程内** 的 HotSpot 完成加载并调用 `agentmain`，**不会** 执行 agent 的 `main`，也 **不会** 在此时加载你的 BTrace 脚本。

### 两阶段：先基础设施，后脚本

```text
阶段 1  loadAgent(btrace-agent.jar)
          → agentmain：Instrumentation、Socket 服务等就绪

阶段 2  客户端编译 script.java（在客户端 JVM）
          → Socket 下发探针定义
          → Agent：ASM + retransform，织入业务类
```

attach 的是 **agent JAR**；脚本 **不以 jar 形式 attach**，而是织进目标类字节码。

### 同一 OS 进程，不同 ClassLoader

| 维度 | 说明 |
| ---- | ---- |
| 进程 | 只有一个业务 JVM；`btrace` 命令是 **另一个客户端进程** |
| Agent 类 | 多由 JVM **agent 加载路径** 加载，一般不当作业务 `AppClassLoader` 的普通 classpath |
| 业务类 | 仍由 `AppClassLoader`（等）定义；`retransform` 改的是这些类的方法 **字节码** |
| 探针执行 | 在 **业务线程** 调用栈上（如 `method0` 返回前），不是「每个方法一个 agent 线程」 |

命名空间与「子可见父、兄弟互不可见」见 [java classloader](/classloader) §不同 ClassLoader。

### Agent 能力 vs BTrace 限制

| 层面 | 能力 |
| ---- | ---- |
| JVM + `Instrumentation` + [ASM](/java-asm) | 理论上可大幅改写已加载类（含改返回值等） |
| **BTrace 产品** | 脚本编译/校验：禁止 `new`、循环、抛异常等；API 限于 `BTraceUtils` → **以观测为主** |
| 恶意 agent | 同进程、同用户权限下风险大；生产需管控 attach 与 agent 来源 |

Hook 点除方法入口/返回外，还有 `CALL`、`LINE`、异常相关等（见下文 `@Location`）；**机制上** 可在这些位置插字节码，**BTrace** 则限制探针体为安全子集。

### 与开发期热替换的区别

| | BTrace attach | IDE HotSwap / [DCEVM](/dcevm-hotswapagent) |
| -- | ------------- | ------------------------------------------- |
| 目的 | **观测** 已运行进程 | **修改** 自己的业务代码并立刻跑 |
| 路径 | Attach + `retransform` 探针 | [JPDA](/java-debug-jpda) → [JVMTI](/jvmti) / 增强 redefine |
| 与 Spring DevTools | 无关 | [DevTools](/spring-boot-devtools) 是上下文 Restart，不是 JVM HotSwap |

## 打印慢调用

### 编写 BTrace 脚本

BTrace 脚本常用 `.java` 扩展名，语法大体是 Java 的子集，但**不是标准 Java 源文件**，而是带 BTrace 注解的探针脚本：

- 必须有 `@BTrace`，探针方法用 `@OnMethod`、`@Location` 等注解声明 hook 点
- 常用 `import static com.sun.btrace.BTraceUtils.*` 中的 `println`、`timestamp` 等 API
- 由 BTrace 编译器在 **客户端 JVM** 中编译（`btrace <PID> script.java` 或事先 `btracec`），不能用 `javac` 当普通业务类编译运行
- 不进业务应用的 classpath；探针逻辑由 Agent 织入目标 JVM 的类中，而不是在脚本的 `main` 里执行

| 方面 | 标准 Java | BTrace 脚本 |
| ---- | --------- | ----------- |
| 编译 | `javac` 生成可独立运行的 class | BTrace 编译器 + 校验 |
| 运行 | `main`、实例方法、可 `new` 对象 | 无独立 `main`；探针注入目标方法 |
| 限制 | 无特殊限制 | 不能 `new`、不能循环、不能抛异常、须 `static` 等 |
| 注解 | JDK / 第三方注解 | `com.sun.btrace.annotations.*` |

示例脚本：

```java
// MethodDuration_redis.java
import com.sun.btrace.annotations.*;
import static com.sun.btrace.BTraceUtils.*;

@BTrace
public class MethodDuration_redis {
    private static int i = 0;

    @OnMethod(clazz = "com.wiloon.package0.Class0", method = "method0",
              location = @Location(Kind.RETURN))
    public static void printMethodRunTime(@ProbeClassName String probeClassName,
                                          @Duration long duration) {
        long d = duration / 1000000;
        if (d > 9) { // 大于 9 毫秒的调用
            i++;
            println("index: " + i + ", timestamp:" + timestamp("HH:mm:ss")
                + ", " + probeClassName + ", duration: " + d + " ms");
        }
    }
}
```

### 找到 Java 进程并执行 BTrace

```bash
# 打印 Java 进程
jcmd -l
# 执行 btrace，Ctrl-C 退出
/bin/btrace <PID> MethodDuration_redis.java
```

## Attach 原理

BTrace 的 attach 走 JDK 官方的动态 attach + Java Agent + Instrumentation 字节码改写，不是重启进程。可概括为：

```text
Client（Attach API + 脚本编译）+ Agent（[ASM](/java-asm) + Instrumentation）+ Socket
```

### 执行流程（Attach 模式）

1. **启动客户端 JVM**

   执行 `btrace <PID> script.java` 会拉起独立的 Java 进程（客户端），用本机 JDK 运行 BTrace client。

2. **Attach API 加载 Agent**

   客户端使用 [Attach API](/attach-api)（`com.sun.tools.attach.VirtualMachine`）：

   ```java
   VirtualMachine vm = VirtualMachine.attach(pid);
   vm.loadAgent("/path/to/btrace-agent.jar", "port=2020,...");
   vm.detach();
   ```

   `attach(pid)` 通过操作系统本地机制连接目标 JVM（Linux 上常见为 `/tmp/.java_pid<pid>` 一类 socket）。通常要求同一台机器、同一用户。

   `loadAgent` 把 **btrace-agent.jar** 载入业务 JVM，调用 **`agentmain`**（非 `main`），获得 `Instrumentation`。**不是** 载入脚本 jar。Agent 框架见 [java-asm](/java-asm) §Agent 框架、`ClassFileTransformer`。

3. **Agent 在业务 JVM 内就绪**

   Agent 在业务进程内启动（可能包含监听 Socket 的线程），等待客户端连接。

4. **客户端编译并下发脚本**

   - 在 **客户端 JVM** 读取 `script.java`，经 BTrace 编译器编译、校验
   - 经 **Socket** 把探针定义发给业务 JVM 内的 Agent（不是 attach 脚本 jar）
   - 也可用 `btracec` 预编译后再 attach

5. **Agent 在业务 JVM 内织入探针**

   - 解析 hook 点（`@OnMethod`、`@Location` 等）
   - 用 [ASM](/java-asm) 生成探针字节码，做 verification
   - 注册 `ClassFileTransformer`，对目标类 `retransformClasses`，在方法入口/返回前插入探针
   - 探针在 **业务线程** 中执行；`println` 等经 Socket 回到客户端终端

   这与 IDE 的 HotSwap（[JPDA](/java-debug-jpda) / 有限 redefine）不同：是 Instrumentation 的 **retransform**，由 [ASM](/java-asm) 在已加载类上插探针字节码。

6. **结束**

   Ctrl-C 退出客户端；探针是否完全移除取决于 detach 行为，生产上仍按「可能需重启业务 JVM」对待。

### 常见误解

| 误解 | 实际情况 |
| ---- | -------- |
| attach 的是脚本编译出的 jar | attach 的是 **btrace-agent.jar**；脚本以探针形式 **织进业务类** |
| Agent 是业务 JVM 里的一个线程 | Agent 是整份 agent 代码；探针跑在业务方法调用栈上 |
| 两个 JVM 长期对等通信 | Attach 一次性加载 Agent；之后主要通过 Socket 传脚本与输出 |
| BTrace 是单个原生二进制 | 是 **脚本 + JAR**，客户端与目标都依赖 JVM |
| `loadAgent` 会执行 agent 的 `main` | 执行 **`agentmain`**，manifest 为 `Agent-Class` |
| loadAgent 时脚本已进业务 JVM | **否**；脚本在 agent 就绪后经 **Socket** 下发再织入 |
| Agent 与业务是不同 JVM 进程 | **同一业务进程**；客户端 `btrace` 是另一进程 |
| JVM 禁止 agent 改业务类 | **不禁止**；BTrace **校验脚本** 限制为观测型探针 |
| 开发 HotSwap 与 BTrace 同一路 | **否**；见 §概念厘清 |

### 两种启动方式

| 方式 | 命令 | Agent 何时加载 |
| ---- | ---- | -------------- |
| Attach 模式 | `btrace <PID> script.java` | 进程已运行，动态 `loadAgent` |
| 启动时 Agent | `btracer ...` 或 `-javaagent:btrace.jar` | JVM 启动时 `premain` |

JDK 8 生产排查常用 Attach 模式。

### 脚本限制的原因

探针字节码会进入业务方法的热路径。若允许在探针里创建对象、抛异常、加锁或写循环，可能改变 GC/锁行为，甚至导致 JVM 校验失败。因此 BTrace 强制脚本几乎全是 static、无堆分配、无异常的子集。

## BTrace 简介

BTrace 是 Sun 推出的 Java 动态、安全追踪工具：不重启即可监控运行情况，获取方法参数、返回值、堆栈等，侵入性较低。

由于脚本逻辑会织入运行中的代码，使用上有较多限制：

1. 不能创建对象
2. 不能使用数组
3. 不能抛出或捕获异常
4. 不能使用循环
5. 不能使用 `synchronized`
6. 属性和方法必须使用 `static` 修饰

不当使用可能导致 JVM 崩溃，上生产前应在本地充分验证脚本。移除探针后，通常需重启才能完全恢复被改写的类（取决于 detach 行为，生产上仍按「可能需重启」对待）。

### 典型用途

1. 接口变慢，分析方法耗时
2. Map 大量插入时观察扩容
3. 分析谁调用了 `System.gc()` 及调用栈
4. 方法抛异常时查看运行时参数

## 第一个例子

被跟踪的 Java 类：

```java
package com.metty.rpc.common;
import java.util.Random;

public class BtraceCase {
    public static Random random = new Random();
    public int size;

    public static void main(String[] args) throws Exception {
        new BtraceCase().run();
    }

    public void run() throws Exception {
        while (true) {
            add(random.nextInt(10), random.nextInt(10));
        }
    }

    public int add(int a, int b) throws Exception {
        Thread.sleep(random.nextInt(10) * 100);
        return a + b;
    }
}
```

通过 `jps` 获取 PID，执行 `btrace <pid> Debug.java` 即可在每次 `add` 调用时看到参数、返回值与耗时。

## 注解说明

### @OnMethod

定义要分析的方法入口。`class`、`method` 指定方式示例：

1. 全限定名：`clazz="com.metty.rpc.common.BtraceCase"`, `method="add"`
2. 正则：`clazz="/javax\.swing\..*/"`, `method="/.*/"`
3. 接口：`clazz="+com.ctrip.demo.Filter"`, `method="doFilter"`
4. 注解：`clazz="@javax.jws.WebService"`, `method="@javax.jws.WebMethod"`
5. 构造方法：`method="<init>"`

### @Location

定义拦截位置，默认为 `Kind.ENTRY`：

1. `Kind.ENTRY`：进入方法时执行脚本
2. `Kind.RETURN`：方法返回前执行；只有此时能拿到 `@Return` 和 `@Duration`
3. `Kind.CALL`：分析方法内对其它方法的调用；细粒度耗时常配合 `Where.AFTER`
4. `Kind.LINE`：是否执行到指定行号
5. `Kind.ERROR` / `Kind.THROW` / `Kind.CATCH`：异常相关跟踪

## 使用 BTrace 定位问题

1. 找出耗时超过阈值的 Filter：`@Duration` 为纳秒，需除以 `1_000_000` 得到毫秒；可再用 `@Location(Kind.CALL)` 细查
2. 分析谁调用了 `System.gc()`：在调用栈中定位类与方法
3. 统计方法调用次数：`@OnTimer` 可定时执行脚本中的方法
4. 查看实例属性：通过 BTrace 提供的反射能力读取字段

## 相关博客（本专题）

| 主题 | 文章 |
| ---- | ---- |
| 知识关系总图 | [Java 领域知识关系图](/java-knowledge-map) |
| Attach、`loadAgent`、jcmd | [Java Attach API](/attach-api) |
| ASM、Instrumentation、retransform | [Java ASM 与运行时字节码织入](/java-asm) |
| ClassLoader、Agent 与业务可见性 | [java classloader](/classloader) |
| HotSpot、JVMTI、JPDA | [HotSpot 简介](/hotspot)、[JVMTI](/jvmti)、[JAVA 调试与 JPDA](/java-debug-jpda) |
| 开发热替换（对比用） | [开发期热替换](/dcevm-hotswapagent)、[Spring Boot DevTools](/spring-boot-devtools) |
| jcmd、工具选型 | [jcmd](/jcmd)、[生产环境诊断工具选型](/production-diagnostics-tooling) |

## 参考

- [BTrace 项目](https://github.com/btraceio/btrace)
- [生产环境诊断工具选型](/production-diagnostics-tooling)（其它 JDK 版本下的工具对照）
- [rowkey: btrace 介绍](http://www.rowkey.me/blog/2016/09/20/btrace/)
- [calvin1978: btrace](http://calvin1978.blogcn.com/articles/btrace1.html)
- [json-liu btrace gitbook](https://legacy.gitbook.com/book/json-liu/btrace/details)
- [greys-anatomy](https://github.com/oldmanpushcart/greys-anatomy)（Arthas 前身之一）

## 其它 JDK 版本

以下内容超出 JDK 8 当时的生产环境，供升级 JDK 后参考。

### 安装方式补充

除解压发行包外，还可：

```bash
# SDKMan
sdk install btrace

# JBang（从 Maven 拉 client/agent，无需手动下 tar.gz）
curl -Ls https://sh.jbang.dev | bash -s - app setup
jbang catalog add --name btraceio https://raw.githubusercontent.com/btraceio/jbang-catalog/main/jbang-catalog.json
jbang btrace@btraceio <PID> script.java
```

### JDK 11 及以后

- JFR 自 JDK 11 起免费，许多场景可用 `jcmd <pid> JFR.start` 做 GC、锁、分配等分析，见 [Java Flight Recorder](/java-flight-recorder-jfr)。
- BTrace 2.x 仍维护，支持 oneliner，例如：

  ```bash
  btrace -n 'com.myapp.*::* @return if duration>100ms { print method, duration }' <PID>
  ```

### JDK 21 及以后

运行时动态加载 agent 可能需目标 JVM 增加：

```bash
-XX:+EnableDynamicAgentLoading
```

若存在 `-XX:+DisableAttachMechanism` 则需移除。BTrace、Arthas、async-profiler 的 attach 模式均受影响。

### 更高版本 JDK 与工具选型

JDK 已升级到 Java 26 时，BTrace 仍可用于「慢调用过滤 + 持续采集」等脚本化场景，但通常不再是默认首选：临时排查多用 Arthas（`trace` / `watch`），CPU/GC 多用 JFR 与 async-profiler。

详见 [Java 生产环境诊断工具选型](/production-diagnostics-tooling)。
