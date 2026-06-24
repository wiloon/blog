---
title: "CNB: Cloud Native Buildpacks 与 Paketo"
author: "-"
date: 2026-06-21T19:40:12+08:00
lastmod: 2026-06-21T19:40:12+08:00
url: cloud-native-buildpacks
categories:
  - cloud
tags:
  - remix
  - AI-assisted
  - cloud
  - docker
  - container
  - paketo
  - spring-boot
---

## 是什么

Cloud Native Buildpacks（常缩写 **CNB**）是一套把应用源码或编译产物自动打成 **OCI 容器镜像**的规范与工具生态，站点在 [buildpacks.io](https://buildpacks.io/)。思路类似早年 Heroku、Cloud Foundry 上的 buildpack：平台检测你推上来的是什么（Java jar、Node 项目等），自动选运行时、装依赖、写好启动命令，不必为每种语言手写 Dockerfile。

**Paketo**（[paketo.io](https://paketo.io/)）是 CNB 生态里常用的**开源实现**，提供现成的 builder 镜像和一系列 language buildpack（Java、Node.js、Go、Python 等）。它与 Spring 无隶属关系，但 Spring Boot 的 `bootBuildImage` / `spring-boot:build-image` **默认使用 Paketo 的 builder**。

```text
CNB          ← 规范 + 生态（buildpack / builder / lifecycle）
  │
  ├── Paketo ← 开源实现（Spring Boot 默认路径）
  ├── Heroku buildpacks
  └── Google Cloud buildpacks …

调用方：
  pack CLI、Spring Boot 插件、Tekton、CI … → 拉 builder → 跑 buildpack → 出 OCI 镜像
```

Spring Boot 侧如何把 fat jar、分层 JAR、jlink 与 Buildpack 串起来，见 [Spring Boot Container Packaging](../language/java/spring/spring-boot-container-packaging.md)。

## 和 Dockerfile 比什么

| 维度 | 手写 Dockerfile | CNB / Paketo |
| ---- | --------------- | ------------ |
| 镜像内容从哪来 | 你在 Dockerfile 里写死 `FROM`、`COPY`、`RUN` | buildpack 根据检测结果自动贡献层 |
| 语言运行时 | 自己选基础镜像、装 JRE/Node | Java buildpack 自动装 JRE（可配版本、jlink） |
| 可重复性 | 取决于你怎么写 | 同一 builder 版本 + 同一输入，产物更一致 |
| 灵活度 | 最高 | 受 buildpack 能力与环境变量约束 |
| 学习成本 | 要会 Docker 分层、多阶段构建 | 先理解 builder + buildpack + 几个 `BP_*` 变量 |

CNB 不是取代 Dockerfile，而是另一种「声明应用、让工具生成镜像」的路径；复杂定制仍常用手写 Dockerfile 或多阶段构建。

## 核心概念

### Buildpack

单个 buildpack 负责检测与构建的一小块逻辑，例如：

- 发现 `pom.xml` → 用 Maven 编译
- 发现可执行 jar → 配置 `java -jar` 启动
- 为 Spring Boot jar 读取 `layers.idx` 切成多个镜像层

多个 buildpack 按顺序执行；前面的可能编译出 jar，后面的再装 JRE、写启动命令。

### Builder

Builder 是一个 **OCI 镜像**，里面打包了一组 buildpack 及其执行环境（称为 **lifecycle**）。构建时平台拉取 builder，在 builder 容器里按顺序跑 buildpack。

Spring Boot 插件默认 builder 示例（以当前文档为准）：

```text
paketobuildpacks/builder-noble-java-tiny:latest
```

名字里的 `java-tiny` 表示面向 Java 应用、基础镜像偏精简。

### Lifecycle

CNB 规定的构建阶段（detect、analyze、build、export 等），由 builder 内的 lifecycle 二进制执行。应用开发者通常不直接调用 lifecycle，而是通过 `pack` 或 Spring Boot 插件触发。

### Platform

执行构建的环境：本机 Docker、`pack` CLI、Spring Boot Maven/Gradle 插件、K8s 上的 build service 等。Platform 把应用目录或 jar 交给 builder，最后得到镜像推入本地或仓库。

关系简图：

```mermaid
flowchart LR
  APP[应用 jar 或源码]
  PLAT[Platform<br/>pack / bootBuildImage]
  BLD[Builder 镜像<br/>Paketo]
  BP1[Buildpack A<br/>例如 Maven]
  BP2[Buildpack B<br/>例如 Java JRE]
  BP3[Buildpack C<br/>例如 Spring Boot]
  IMG[OCI 镜像]

  APP --> PLAT
  PLAT --> BLD
  BLD --> BP1 --> BP2 --> BP3 --> IMG
```

## Paketo 是什么

Paketo 由 VMware（后与 Broadcom 相关的开源脉络）主导维护，是 CNB 的参考级开源发行版之一。对 Java/Spring 开发者最相关的部分：

| 组件 | 作用 |
| ---- | ---- |
| [Paketo Java Buildpack](https://github.com/paketo-buildpacks/java) | 元 buildpack，编排 Maven/Gradle、JVM、可执行 jar 等子 buildpack |
| [Paketo Spring Boot Buildpack](https://github.com/paketo-buildpacks/spring-boot) | 识别 Spring Boot jar、按 `layers.idx` 切片、Spring Cloud Bindings 等 |
| [Paketo Java Native Image Buildpack](https://github.com/paketo-buildpacks/java-native-image) | GraalVM Native 路径（与 JVM + jlink 不同，见 [GraalVM Native Image 简介](../language/java/graalvm-native-image.md)） |
| Builder 镜像 | 如 `paketobuildpacks/builder-jammy-base`、`builder-noble-java-tiny` |

配置多通过 **构建期环境变量** 传入，命名惯例：

- `BP_*`：build-time（写入镜像）
- `BPL_*`：launch-time（容器启动时）

Java 常用示例：

| 变量 | 含义 |
| ---- | ---- |
| `BP_JVM_VERSION` | JRE 主版本，如 `21` |
| `BP_JVM_TYPE` | `JRE`（默认）或 `JDK` |
| `BP_JVM_JLINK_ENABLED` | 是否用 jlink 生成精简 JRE，默认 `false` |
| `BP_NATIVE_IMAGE` | 是否走 Native Image 构建 |

完整列表见 [Paketo Java 文档](https://paketo.io/docs/howto/java/)。

## 怎么用

### Spring Boot（最常见）

```bash
./mvnw spring-boot:build-image
# Gradle
./gradlew bootBuildImage
```

插件会打可执行 jar（若尚未 repackage），再调用 Paketo builder 生成镜像。需本机可访问 Docker daemon。

Maven 指定 JVM 版本：

```xml
<configuration>
  <image>
    <env>
      <BP_JVM_VERSION>21</BP_JVM_VERSION>
    </env>
  </image>
</configuration>
```

### pack CLI（语言无关入口）

不经过 Spring 插件，直接对 jar 或源码目录构建：

```bash
pack build my-app \
  --builder paketobuildpacks/builder-jammy-base \
  --path target/myapp.jar
```

安装见 [Pack 文档](https://buildpacks.io/docs/for-platform-operators/how-to/integrate-ci/pack/)。

### 启用 jlink（缩小 JRE）

```bash
pack build my-app \
  --path target/myapp.jar \
  --env BP_JVM_JLINK_ENABLED=true
```

默认不开启；详见 [Spring Boot Container Packaging](../language/java/spring/spring-boot-container-packaging.md) 中的 jlink 一节。

## 构建时大致发生什么

以「已有 Spring Boot fat jar + Paketo Java builder」为例：

1. Platform 启动 builder 容器，挂载应用 artifact
2. 各 buildpack **detect**：是否参与本次构建
3. **build**：例如 JVM buildpack 下载/安装 Liberica JRE；Spring Boot buildpack 读 `layers.idx` 规划镜像层
4. **export**：lifecycle 把各层写入最终 OCI 镜像，设置 `ENTRYPOINT`（多为 `java -jar` 或 wrapper 脚本）
5. 镜像 tag 为 `docker.io/library/项目名:版本` 等，出现在本地 Docker

日志里若出现 `Creating slices from layers index`，说明 Paketo Spring Boot buildpack 正在按分层 JAR 切 Docker 层——与手写多段 `COPY` 的目的一致。

## 生态里还有哪些 CNB 实现

| 实现 | 说明 |
| ---- | ---- |
| Paketo | 开源、Spring Boot 默认、文档全 |
| Heroku | 商业 PaaS 起家，CNB 重要推动者之一 |
| Google Cloud Buildpacks | GCP 场景 |
| 自建 buildpack | 公司内定制检测与构建逻辑 |

同一 CNB 规范下，builder 可换，但 buildpack 集合与默认行为不同；换 builder 前要核对是否支持 Spring Boot layered jar、JVM 版本等。

## 何时用、何时不用

适合：

- Spring Boot 服务想少维护 Dockerfile
- 希望 Java 版本、JRE、启动参数有约定好的 `BP_*` 配置面
- CI 里一条 `bootBuildImage` 出可部署镜像

不太适合：

- 镜像里要强依赖大量系统包、定制 OS 布局（更常多阶段 Dockerfile）
- 构建逻辑与官方 Java buildpack 假设差异很大
- 需要完全控制每一层 Dockerfile 指令

## 参考

- [buildpacks.io 官方文档](https://buildpacks.io/docs/)
- [Paketo 文档](https://paketo.io/docs/)
- [Paketo Java How-to](https://paketo.io/docs/howto/java/)
- [Spring Boot — Cloud Native Buildpacks](https://docs.spring.io/spring-boot/reference/packaging/container-images/cloud-native-buildpacks.html)
- [Spring Boot Container Packaging](../language/java/spring/spring-boot-container-packaging.md)
- [Spring Boot](../language/java/spring/spring-boot.md)
- [GraalVM Native Image 简介](../language/java/graalvm-native-image.md)
