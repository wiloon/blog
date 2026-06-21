---
title: OpenJDK JDK 发行版：Temurin、Corretto、Dragonwell
author: "-"
date: 2026-06-21T18:19:51+08:00
lastmod: 2026-06-21T18:19:51+08:00
url: openjdk-distributions
categories:
  - language
tags:
  - java
  - openjdk
  - temurin
  - corretto
  - dragonwell
  - remix
  - AI-assisted
---

## OpenJDK 与「发行版」

[OpenJDK](https://openjdk.org/) 是 Java 平台的开源**参考实现**（源码项目）。日常 `java -version` 看到的并不是「裸 OpenJDK 源码」，而是各厂商/社区基于该源码（或与之同步的分支）**构建、测试、打包**后的 **JDK 发行版**（distribution）。

多数发行版默认捆绑 **HotSpot** 虚拟机，因此 Temurin、Corretto、Dragonwell 之间换的是**供应商、构建渠道与支持策略**，不是换一套 JVM 实现。JVM 实现层选型见 [Java 虚拟机](./jvm.md)。

```text
OpenJDK 源码（openjdk/jdk）
        │
        ├── 各发行版构建 + TCK / 内部 QA
        │
        ▼
  Temurin / Corretto / Dragonwell / Oracle JDK …
        │
        └── 默认内含 HotSpot（Semeru 等除外，见下文）
```

## 常见发行版对照

| 发行版 | 维护方 | 许可 / 费用 | 典型特点 |
| ---- | ------ | ----------- | -------- |
| **Eclipse Temurin** | Eclipse Adoptium | 免费（GPLv2 + Classpath） | AdoptOpenJDK 继任；通过 Java SE TCK；**无特殊理由时的默认推荐** |
| **Amazon Corretto** | Amazon | 免费 | AWS 生态常用；长期支持声明；Corretto 补丁分支 |
| **Dragonwell**（含 Alibaba Dragonwell） | 阿里云 | 免费 | 面向国内与大促场景优化；部分版本含 Wisp 协程、增强 GC 等 Alibaba 扩展 |
| **Oracle JDK** | Oracle | 免费（个人/开发等，见 Oracle 许可 FAQ）/ 商业订阅 | Oracle 官方构建；与 OpenJDK 功能同步策略见 Oracle 文档 |
| **Microsoft Build of OpenJDK** | Microsoft | 免费 | Azure / Windows / GitHub Actions 场景常见 |
| **Red Hat Build of OpenJDK** | Red Hat | 免费 / 随 RHEL 订阅支持 | OpenShift、RHEL 企业环境 |
| **Azul Platform Core**（Zulu 等） | Azul | 免费构建 + 商业支持 | 多版本、多平台；企业 SLA |
| **IBM Semeru** | IBM | 免费 / 商业 | **OpenJ9** 虚拟机，**不是 HotSpot**；见 [jvm.md](./jvm.md) |

Linux 发行版自带的 `openjdk-*-jdk`（Debian/Ubuntu/Arch 包）也是基于 OpenJDK 源码的构建，可视为「 distro 维护的发行版」，更新节奏跟随各发行版仓库。

macOS 上 **Homebrew `openjdk`** 同理：从 `openjdk/jdk*u` 的 GA 标签（如 `jdk-26.0.1-ga`）编译，`java -version` 显示 `IMPLEMENTOR=Homebrew`，不是 Temurin 等品牌包，但仍是 HotSpot + 上游源码。

## 三个名字分别是什么

### Eclipse Temurin（Adoptium）

- 前身 **AdoptOpenJDK**，现由 Eclipse **Adoptium** 项目发布，品牌名 **Temurin**
- 构建公开、通过 **TCK**，与 Java 生态兼容性目标明确
- 下载：[adoptium.net](https://adoptium.net/)
- 社区与文档引用率最高，**通用服务端默认选它**通常没问题

### Amazon Corretto

- Amazon 维护的 OpenJDK 下游构建，**免费**，提供 LTS 版本的安全更新
- AWS 文档与 AMI/容器镜像中常见；不绑定 AWS 也能用
- 下载：[aws.amazon.com/corretto](https://aws.amazon.com/corretto/)

### Dragonwell（Alibaba Dragonwell / 龙井）

- 阿里云基于 OpenJDK 的发行版，面向高并发、大堆、国内生产环境优化
- 标准版贴近上游 OpenJDK；部分版本带 **Alibaba 扩展**（如 Wisp 2、Enhanced ZGC 等），需看版本说明是否启用
- 下载与文档：[dragonwell-jdk.io](https://dragonwell-jdk.io/) / 阿里云文档

## 怎么选

| 场景 | 建议 |
| ---- | ---- |
| 无特殊约束的新项目 | **Temurin**（LTS 版本，如 21 / 17） |
| 主要跑在 AWS | **Corretto** 与 AWS 支持矩阵一致，省心 |
| 阿里云 / 已有 Dragonwell 运维体系 | **Dragonwell** |
| 需要 Oracle 商业支持或 Oracle 工具链合同 | **Oracle JDK** |
| Azure / GitHub-hosted runner | **Microsoft Build of OpenJDK** |
| 要 OpenJ9 省内存 | **Semeru**，不是 Temurin/Corretto |

**版本**：优先选 **LTS**（当前常用 17、21；见 [Java 版本历史](./java-version-history.md)）。**虚拟机**：未特别说明时，上述 HotSpot 系发行版可互换性高，迁移成本主要在镜像与运维习惯，不在字节码。

## 同源构建：差异在哪

同一 GA 版本（如 **26.0.1**）的 Temurin、Corretto、Homebrew `openjdk` 等，**源码逻辑一致**——都来自 OpenJDK 更新分支（如 `jdk26u`）。`26.0.1` 里的 bug/安全修复由 **上游 OpenJDK 项目**合并，Temurin **不会**单独维护一套私有 JVM 逻辑（仅可能有少量**构建/打包**补丁）。

若出现差异，通常来自：

| 维度 | 说明 |
| ---- | ---- |
| 编译与打包参数 | boot JDK、编译器版本、`--with-debug-level`、vendor 字符串（Temurin vs Homebrew）等 |
| 构建号 | Temurin 如 `26.0.1+8` 中 `+8` 为 Adoptium 构建批次，不代表 API 不同 |
| 发布节奏 | 上游新 fix 合入后，各发行版 formula/流水线更新时间可能不同步 |
| 测试与支持 | Temurin 强调 **Java SE TCK**；Homebrew 面向本机开发便利 |

日常开发下可视为**同一套 Java**；生产环境选 Temurin 等多为 **TCK、安全更新节奏与镜像生态**，不是因为 bytecode 语义不同。真正改运行时逻辑的是 **Dragonwell 扩展**、**Semeru（OpenJ9）** 等，不属于「只换编译参数」。

## 与安装文档的关系

各平台 `apt`/`brew`/手动下载等命令见 [openjdk](./openjdk.md)（安装备忘）。本文只讨论**发行版是什么、如何选型**。

## 参考

- [OpenJDK](https://openjdk.org/)
- [Eclipse Adoptium / Temurin](https://adoptium.net/)
- [Amazon Corretto](https://aws.amazon.com/corretto/)
- [Alibaba Dragonwell](https://dragonwell-jdk.io/)
- [Java 虚拟机生态与选型](./jvm.md)
