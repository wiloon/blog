---
title: 开发期热替换（HotSwap、DCEVM、HotSwapAgent）
author: "-"
date: 2019-12-17T04:29:09+00:00
lastmod: 2026-05-31T07:25:07+08:00
url: dcevm-hotswapagent
categories:
  - language
aliases:
  - /p15208/
tags:
  - AI-assisted
  - dcevm
  - hotspot
  - hotswap
  - java
  - jpda
  - jvm
  - remix
---

## 背景

开发时希望改 Java 代码后 **少重启** 就能看到效果。这与生产上 [BTrace](../language/java/btrace.md) attach **观测** 不是同一条路。本文归纳 **HotSwap** 及相关工具，并说明各自边界。

字节码织入与 `redefine` 机制见 [java-asm](../language/java/java-asm.md)；调试协议见 [JPDA](../language/java/java-debug-JPDA.md)、[JVMTI](../language/java/jvmti.md)。

## HotSwap 是什么

**HotSwap**（热替换）泛指：**不重启整个 JVM**，把 **已在内存中的类** 换成新字节码。

HotSpot **自带** 的热替换能力很窄（通过 **调试器** 触发，底层 [JVMTI](../language/java/jvmti.md) / `redefine`）：

- 常见成功：改 **已有方法的方法体**
- 常见失败：新增方法/字段、改签名、改继承、新 import 等

因此 IDE 在 **Debug** 下保存后提示 "Hot swap" 成功或失败，依赖的是 **JPDA → JDWP → JVMTI**，**不是** [Attach API](../language/java/attach-api.md) 加载 BTrace agent 那条栈。

```text
开发期 HotSwap（典型）
  IDE 编译 .class → JDWP 命令 → JVM redefine 已加载类

生产期 BTrace（对比）
  loadAgent → Instrumentation + ASM retransform → 插探针（观测）
```

## 几种开发期方案

| 方案 | 怎么做 | 能力边界 |
| ---- | ------ | -------- |
| **IDE HotSwap** | Debug + JPDA | 方法体为主，标准 HotSpot 最严 |
| **JRebel** | 商业 agent | 类加载/字节码策略更激进，需授权 |
| **DCEVM** | 替换/并行使用 **修改版 HotSpot**（`-XXaltjvm=dcevm`） | 放宽 redefine：可加删方法/字段等 |
| **HotSwapAgent** | `-javaagent:hotswapagent.jar` + 常配合 DCEVM | 用 **Javassist** 改字节码；插件重载 Spring/Hibernate 等配置 |
| **Spring Boot DevTools** | 双 ClassLoader **快速 Restart** | 重建 Spring 上下文，**不是** JVM 级 HotSwap |

Spring DevTools 细节见 [Spring Boot DevTools](../language/java/spring-boot-devtools.md)。

## DCEVM 是什么

**DCEVM**（Dynamic Code Evolution VM）是对 **HotSpot** 的补丁/替代 JVM，目标是运行时 **更自由地 redefine 已加载类**（加方法、改继承等），超出标准 HotSpot 调试热替换限制。

- 项目：[dcevm.github.io](https://dcevm.github.io/)
- 安装常见方式：用 DCEVM 安装器 **Install DCEVM as altjvm**，启动参数 `-XXaltjvm=dcevm`

需与所用 **JDK 大版本** 匹配；属于 **开发机** 工具，不是生产 JVM 标配。

## HotSwapAgent 是什么

[HotSwapAgent](https://www.hotswapagent.org/) 是 **开发用** 的 `-javaagent`：

- 监听 classpath / 资源变更
- 通过 **Javassist** 做运行时字节码修改
- 插件体系：在类变更时触发 **Spring、MyBatis、Tomcat** 等框架的重新注册/刷新

通常与 **DCEVM** 一起用：DCEVM 放宽 VM 的 redefine 规则，HotSwapAgent 负责「改完类之后框架层怎么跟上」。

启动示例（示意，以官方文档为准）：

```bash
-javaagent:/path/hotswap-agent.jar
-XXaltjvm=dcevm
```

## 与 BTrace / Arthas 的区别

| | 开发 HotSwap / DCEVM | BTrace attach |
| -- | -------------------- | ------------- |
| 目的 | 改 **自己的** 业务代码并立刻跑 | **观测** 已上线进程 |
| 入口 | Debug 或 dev javaagent | `loadAgent` + 脚本 |
| 风险 | 开发环境可接受 | 生产需谨慎 |

## 参考

- [DCEVM](https://dcevm.github.io/)
- [HotSwapAgent](https://www.hotswapagent.org/)
- [java-asm](../language/java/java-asm.md)
- [JPDA](../language/java/java-debug-JPDA.md)
- [JVMTI](../language/java/jvmti.md)
- [HotSpot 简介](../language/java/hotspot.md)
