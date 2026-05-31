---
title: Java ASM 与运行时字节码织入
author: "-"
date: 2012-12-15T14:16:51+00:00
lastmod: 2026-05-31T07:36:44+08:00
url: java-asm
categories:
  - language
tags:
  - java
  - asm
  - jvm
  - instrumentation
  - javaagent
  - remix
  - AI-assisted
aliases:
  - /p4904/
---

## 背景

[BTrace](/btrace)、Arthas、Spring LTW、部分 AOP 框架都会在 **不改变业务源码** 的前提下改写字节码。底层常依赖 **ASM**（或其它字节码库）配合 JVM 的 **`java.lang.instrument`** API。

本文说明 ASM 做什么、运行时织入怎么走，以及与 [Attach API](/attach-api) / Agent 的关系。BTrace 的 attach 与脚本下发见 [BTrace](/btrace)。概念总图见 [Java 领域知识关系图](/java-knowledge-map)。ClassLoader 可见性见 [java classloader](/classloader)。

## JLS 与 java.lang.instrument 分别指什么

- **JLS**（Java Language Specification）：Java **语言**规范，定义语法、类型、可见性等；**不**规定 Agent 怎么 attach。
- **`java.lang.instrument`**：JDK 里的 **标准 API 包**，定义 `Instrumentation`、`ClassFileTransformer`，以及 Agent 入口约定（`premain` / `agentmain` 的方法签名、manifest 的 `Premain-Class` / `Agent-Class`）。

日常说「走 instrument 机制」= 用这套 API + JVM 内置实现，在类加载或 retransform 时回调你的 transformer。

## Agent 框架定义了什么、解决什么问题

Agent **不是**一个限制能力的沙箱，而是一套 **标准钩子 + 能力接口**：

| 约定 / 能力 | 作用 |
| ----------- | ---- |
| manifest `Agent-Class` / `Premain-Class` | 告诉 JVM 加载 agent 后调用哪个类的哪个入口 |
| `agentmain` / `premain` + `Instrumentation` | 在 JVM 启动后或 attach 后执行你的初始化逻辑 |
| `ClassFileTransformer` | 在类字节码进入 JVM 前（或 retransform 时）允许你 **替换** 字节码 |
| [Attach API](/attach-api) `loadAgent` | 运行中的 JVM 也能挂上 agent |

**要解决的问题**：在 **不重启、不改磁盘上已部署 jar** 的前提下，对 **已在内存中的类** 做字节码级增强（监控、诊断、部分场景下的热修复）。

JVM **几乎不** 规定 agent 只能做什么；安全靠运维权限、agent 来源信任，以及产品自己的校验（如 BTrace 脚本限制）。

## ClassFileTransformer 做什么

实现 `ClassFileTransformer`，在 `transform` 里对传入的 `classfileBuffer` 用 ASM（等）改写字节码并 **return 新数组**；返回 `null` 表示不修改。

| 场景 | 解决的问题 |
| ---- | ---------- |
| 类 **首次加载** | 新加载的业务类自动带探针（LTW、`-javaagent` 启动即挂载） |
| **`retransformClasses`** | 进程已跑很久，类早已加载，仍可在下次执行方法前换上带探针的字节码（BTrace attach 后常用） |
| **`redefineClasses`** | 用全新 class 字节替换已加载类（热修复、mock 等会用到，约束比 retransform 更严） |

一个 JVM 可注册 **多个** transformer，按注册顺序链式处理同一份字节码。

## ASM 是什么

[ASM](https://asm.ow2.io/) 是 Java **字节码** 读写与生成库，不是汇编器。它直接处理 `.class` 里的指令与常量池，可以：

- 解析已有 class，遍历方法体指令
- 在指定位置 **插入** 或 **替换** 指令序列
- 生成全新 class 文件

与早期 BCEL 等相比，ASM 用 **树 + Visitor（访问者）** 模型：按事件遍历 class 结构，只处理关心的节点（例如某个 `visitMethodInsn`），不必手写完整 class 文件格式。

典型 API 层次：`ClassReader`（读）→ `ClassVisitor` / `MethodVisitor`（改）→ `ClassWriter`（写）。

## 运行时织入：Instrumentation

仅靠 ASM 改磁盘上的 `.class` 不会影响 **已在跑** 的 JVM。运行时织入需要 JVM 提供的 **`Instrumentation`**（由 Java Agent 的 `premain` / `agentmain` 拿到）：

| API | 作用 |
| ---- | ---- |
| `addTransformer(ClassFileTransformer)` | 在类 **加载** 或 **retransform** 时回调，可替换返回的字节码 |
| `retransformClasses(Class<?>...)` | 对已加载类再次走 transformer（BTrace attach 后改已加载类靠这个） |
| `redefineClasses(ClassDefinition...)` | 用新字节码替换已加载类（能力更强，限制更多） |

`ClassFileTransformer.transform(...)` 收到 **原始字节码**，返回 **新字节码**；实现里通常用 ASM 读入、插桩、写出。

```text
业务 JVM 启动 / loadAgent
  → agentmain(premain) 拿到 Instrumentation
  → agent 注册 ClassFileTransformer
  → 需要织入时：ASM 生成「探针片段」并插入目标方法
  → instrumentation.retransformClasses(目标类)
  → 之后业务线程执行的是「已插入探针」的方法字节码
```

这与 IDE **Hotswap**（改源码、有限字段/方法体替换）不是同一条路：织入是 **直接改字节码**，由 Agent 控制插入点。

## 与 BTrace / Attach 的关系

[BTrace](/btrace) 链路可以拆成两层：

1. **[Attach API](/attach-api)** `loadAgent(btrace-agent.jar)`：在 **同一业务进程** 内加载 agent，调用 **`agentmain`**（不走业务 `main`，也不走 `AppClassLoader` 去 `java -jar` agent）。
2. **Agent 内 ASM + Instrumentation**：客户端经 Socket 下发脚本定义后，agent 用 ASM 生成探针字节码，`retransform` 目标类；探针在 **业务线程** 的方法入口/返回等位置执行。

脚本 **不会** 在 `loadAgent` 时进 JVM；agent 只是基础设施，监控逻辑在 agent 就绪后由客户端下发再织入。

## 织入发生在哪里

常见插入点（以 BTrace 的 `@Location` 为例）：

| Kind | 含义 |
| ---- | ---- |
| `ENTRY` | 方法入口 |
| `RETURN` | 正常返回前（可拿 `@Duration`、`@Return`） |
| `CALL` | 方法体内调用其它方法的前后 |
| `LINE` | 执行到某行 |
| `ERROR` / `THROW` / `CATCH` | 异常相关 |

从 **机制** 上说，只要在字节码里能定位到的位置，ASM **都可以** 插入任意逻辑（包括改参数、改返回值、抛异常）——**JVM 不会因为你是 agent 就禁止改业务类**。

[BTrace](/btrace) 则在 **脚本编译/校验** 阶段限制：不能 `new`、不能循环、不能抛异常等，并把 API 收敛到 `BTraceUtils`，目的是 **可观测、低侵入**，而不是 JVM 装了一个「agent 沙箱」。

| 层面 | 能力 |
| ---- | ---- |
| JVM + Instrumentation + ASM | 理论上可大幅改写已加载类 |
| BTrace 产品 | 故意只允许安全子集的探针 |
| 恶意 agent JAR | 同进程、同用户下危害可以很大（改字节码、反射、JNI 等），生产 attach 需管控权限与来源 |

## 同一进程、不同 ClassLoader

`loadAgent` 发生在 **业务 JVM 的那一个 OS 进程** 里：attach 线程（或 JVM 内部线程）执行 `agentmain`，与跑 `main` 的业务线程 **同属一个进程**。

「不经过 AppClassLoader」指的是 **加载 agent JAR 里类的机制** 与加载 `com.yourapp.*` 的路径不同，避免 agent 与业务 classpath 搅在一起；不是另起一个 JVM。子加载器能否看到父加载器上的类、兄弟加载器是否互不可见，见 [java classloader](/classloader)#不同-classloader谁能看到谁。

```text
同一 OS 进程（业务 JVM）
  ├─ 业务线程：AppClassLoader → 业务类 → 已织入探针的方法
  ├─ Agent 基础设施线程：Socket、定时器等（实现相关）
  └─ Agent 类：由 JVM agent 加载路径加载（非典型 AppClassLoader 加载 agent.jar）
```

## 示例：在方法入口插入 INVOKESTATIC

下面是一段 **示意**（非完整可运行 agent），说明 transformer 里如何用 ASM 在 **每个方法入口** 多调用一句静态探针：

```java
// ClassFileTransformer.transform(...) 内，简化示意
ClassReader reader = new ClassReader(classfileBuffer);
ClassWriter writer = new ClassWriter(reader, ClassWriter.COMPUTE_FRAMES);
reader.accept(new ClassVisitor(Opcodes.ASM9, writer) {
    @Override
    public MethodVisitor visitMethod(int access, String name, String descriptor,
            String signature, String[] exceptions) {
        MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);
        return new MethodVisitor(Opcodes.ASM9, mv) {
            @Override
            public void visitCode() {
                super.visitCode();
                // 等价于在 Java 源码方法体第一行加: Probe.onEnter();
                mv.visitMethodInsn(Opcodes.INVOKESTATIC,
                        "com/example/Probe", "onEnter", "()V", false);
            }
        };
    }
}, 0);
return writer.toByteArray();
```

注册 transformer 后对目标类执行 `instrumentation.retransformClasses(Foo.class)`，之后业务线程执行 `Foo.bar()` 时会先进入 `Probe.onEnter()`。BTrace 生成的探针比「整方法包一层」更细，但原理同样是改方法字节码里的指令序列。

## Agent 能否临时修业务 Bug、替换整个方法

**理论上可以**（同一进程、同权限、可改字节码），**生产上极少当作正式修复手段**。

| 场景 | 说明 |
| ---- | ---- |
| 诊断 / 观测 | BTrace、async-profiler、部分 `-javaagent` 监控 |
| 交互式临时改行为 | Arthas `watch`、`trace`、`return`/`mock`（有范围与版本限制） |
| 开发期热替换 | IDE HotSwap（[JPDA](/java-debug-jpda)）、JRebel、[开发期热替换](/dcevm-hotswapagent)（DCEVM + HotSwapAgent） |
| `redefineClasses` | 用新字节码替换已加载类；**整段方法实现**可换成新逻辑，但需满足 JVM 校验（签名、结构变更等有限制，标准 HotSpot 比 DCEVM 严） |

对 **不能停机的关键系统**：

- **可行但高风险**：attach 错 agent、织入有误可能导致 `VerifyError`、逻辑错乱，回滚往往仍要 **重启** 或重新发布。
- **更常见做法**：紧急时 attach 做 **止血观测**（看谁调了错接口、慢在哪），真正修 bug 仍走 **发版/滚动重启**；少数团队会用 Arthas 等做 **极短窗口** 的参数/mock，需审计与预案。

「整个替换业务方法实现」在字节码层面 = 生成一份 **新方法体** 的 class 字节码，经 `redefine`/`retransform` 换进去；不是换 `.java` 源文件。能否一次换掉整个类里所有方法，取决于变更是否符合 JVM 的 redefine 规则（新增方法/字段等在不同 JVM/工具下能力不同）。

## 与其它织入方式对比

| 方式 | 时机 | 典型工具 |
| ---- | ---- | -------- |
| 编译时织入 (CTW) | 编译期生成 class | AspectJ `ajc` |
| 加载时织入 (LTW) | 类首次加载前 | AspectJ + `-javaagent` |
| 运行时 attach + retransform | 进程已运行 | BTrace、Arthas |

ASM 常出现在 **LTW 与 attach 探针** 两类场景；CTW 也可能在编译器里用字节码库，但不依赖 attach。

## 参考

- [ASM 官网](https://asm.ow2.io/)
- [java.lang.instrument](https://docs.oracle.com/en/java/javase/21/docs/api/java.instrument/java/lang/instrument/package-summary.html)
- [BTrace](/btrace)
- [Java Attach API](/attach-api)
- [java classloader](/classloader)
- [AspectJ 编译时织入](/AspectJ)
- [DCEVM, HotSwapAgent](/dcevm-hotswapagent)
- IBM developerWorks：[使用 ASM 体验字节码操纵](https://www.ibm.com/developerworks/cn/java/j-lo-asm30/)（较早，概念仍可用）
