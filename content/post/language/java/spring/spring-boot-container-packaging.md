---
title: Spring Boot Container Packaging: Fat JAR、分层 JAR 与 Buildpacks
author: "-"
date: 2026-06-21T19:04:35+08:00
lastmod: 2026-06-21T19:04:35+08:00
url: spring-boot-container-packaging
categories:
  - language
tags:
  - original
  - AI-assisted
  - java
  - spring
  - spring-boot
  - docker
  - container
---

## 背景

Spring Boot REST API 打成 jar 之后，放进容器常见有三层递进：先有一个能跑的 fat jar，再用分层 JAR 优化 Docker 缓存，最后用 Cloud Native Buildpacks 一键出镜像；若还要缩小运行时，可在 Buildpack 上显式开启 jlink 裁剪 JRE。

Spring Framework 本身几乎不讲容器镜像；相关说明集中在 Spring Boot Reference 的 Packaging → Container Images。本文把 fat jar、分层 JAR、`bootBuildImage`、Paketo jlink 串成一条阅读路径，并附上官方文档索引。GraalVM Native Image 是另一条路线，见 [GraalVM Native Image 简介](../graalvm-native-image.md)。

## 三条路径总览

```mermaid
flowchart TB
  subgraph build [构建]
    SRC[源码 mvn package / bootJar]
    FAT[Fat JAR 可执行 uber jar]
    LAY[分层 JAR 含 layers.idx]
  end

  subgraph deploy [容器化]
    D1[简单 Dockerfile<br/>COPY jar + java -jar]
    D2[分层 Dockerfile<br/>jarmode extract --layers]
    BP[bootBuildImage / build-image<br/>Paketo Buildpacks]
  end

  subgraph runtime [运行时 JVM]
    JRE[完整 JRE]
    JLINK[jlink 精简 JRE<br/>BP_JVM_JLINK_ENABLED]
  end

  SRC --> FAT
  FAT --> LAY
  FAT --> D1
  LAY --> D2
  LAY --> BP
  D1 --> JRE
  D2 --> JRE
  BP --> JRE
  BP -.->|可选| JLINK
```

| 路径 | 典型产物 | 主要收益 | 复杂度 |
| ---- | -------- | -------- | ------ |
| Fat jar + 简单镜像 | 单层 `app.jar` + JRE 基础镜像 | 上手最快 | 低 |
| 分层 JAR + Dockerfile | 多 `COPY` 层 + JRE | 推送镜像时依赖层可缓存 | 中 |
| Buildpack（`bootBuildImage`） | OCI 镜像，自动检测 jar | 零 Dockerfile、与 Paketo 生态一致 | 低～中 |
| Buildpack + jlink | 同上，运行时 JRE 更小 | 缩小镜像体积 | 中（需调 env） |

## Fat JAR

Fat jar、uber jar、executable jar 在 Spring Boot 语境下指同一件事：一个「全包」可执行 jar。Fat jar 与 uber jar 只是不同叫法（uber 来自德语 über，意为「之上 / 全部」）；Spring 官方文档更常写 executable jar。

与 Maven/Gradle 默认打出的普通 jar（常称 thin jar / plain jar）对比如下：

| | 普通 jar（thin / plain jar） | Fat jar（uber jar / executable jar） |
| ---- | ---------------------------- | ------------------------------------ |
| 内容 | 通常只有项目自己的 `.class` 与资源 | 应用代码 + 全部依赖 + `spring-boot-loader`（及内嵌服务器等） |
| 依赖在哪 | 不在 jar 内，需 classpath 或外部 lib | 嵌在 `BOOT-INF/lib/*.jar` |
| `java -jar` | 一般不能直接跑（缺依赖） | 可以，一条命令启动 |
| Spring Boot 谁生成 | `jar` 任务 / `mvn package` 的原始产物（常被重命名为 `*.jar.original`） | `repackage` / `bootJar` 的产物 |
| 典型用途 | 作为库被别的项目依赖 | 部署、容器镜像、`java -jar` 运行 |

Fat jar 把应用类、第三方依赖、内嵌 Tomcat（或 Jetty/Undertow）和 `spring-boot-loader` 打成一个文件，`java -jar app.jar` 即可启动独立进程。这与 [Spring Boot](./spring-boot.md) 里「内嵌服务器 + 可执行 JAR」的设计一致。

布局要点：

```text
app.jar
├── META-INF/MANIFEST.MF     # Main-Class → JarLauncher，Start-Class → 你的 @SpringBootApplication
├── org/springframework/boot/loader/   # 启动引导
└── BOOT-INF/
    ├── classes/             # 你的代码与配置
    └── lib/                 # 依赖 jar
```

构建方式：

- Maven：`spring-boot-maven-plugin` 的 `repackage`（使用 `spring-boot-starter-parent` 时通常已绑定到 `package` 阶段）
- Gradle：`bootJar`（`build` / `assemble` 会自动执行）

```bash
./mvnw package
java -jar target/myapp.jar

# Gradle
./gradlew bootJar
java -jar build/libs/myapp.jar
```

容器里最直白的 Dockerfile：

```dockerfile
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

能跑，但整个 uber jar 在一个 Docker layer 里：业务代码一改，依赖层也无法被缓存复用。官方 [Efficient Container Images](https://docs.spring.io/spring-boot/reference/packaging/container-images/efficient-images.html) 明确建议不要长期把 fat jar 原样塞进单层镜像。

## 分层 JAR

分层 JAR 在 fat jar 布局不变的前提下，额外写入 `BOOT-INF/layers.idx`，声明哪些路径属于哪一层、层的写入顺序。Spring Boot 2.3 起默认开启；Maven `repackage` / Gradle `bootJar` 的 `layered` 无需额外配置即可得到。

默认四层（从不易变到易变）：

| 层名 | 典型内容 |
| ---- | -------- |
| `dependencies` | 非 SNAPSHOT 的 `BOOT-INF/lib/*.jar` |
| `spring-boot-loader` | `org/springframework/boot/loader/**` |
| `snapshot-dependencies` | 版本号含 `SNAPSHOT` 的依赖 |
| `application` | `BOOT-INF/classes`、清单、索引文件等 |

`layers.idx` 片段示例：

```yaml
- "dependencies":
  - BOOT-INF/lib/library1.jar
- "spring-boot-loader":
  - org/springframework/boot/loader/launch/JarLauncher.class
- "snapshot-dependencies":
- "application":
  - BOOT-INF/classes/
  - META-INF/MANIFEST.MF
```

查看分层（需 jar 内带 `spring-boot-jarmode-tools`）：

```bash
java -Djarmode=tools -jar my-app.jar list-layers
java -Djarmode=tools -jar my-app.jar extract --layers --destination extracted
```

### 手写 Dockerfile（jarmode）

官方 [Dockerfiles](https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html) 推荐多阶段构建：builder 阶段解压分层，runtime 阶段按层 `COPY`：

```dockerfile
FROM eclipse-temurin:21-jre AS builder
WORKDIR /builder
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} application.jar
RUN java -Djarmode=tools -jar application.jar extract --layers --destination extracted

FROM eclipse-temurin:21-jre
WORKDIR /application
COPY --from=builder /builder/extracted/dependencies/ ./
COPY --from=builder /builder/extracted/spring-boot-loader/ ./
COPY --from=builder /builder/extracted/snapshot-dependencies/ ./
COPY --from=builder /builder/extracted/application/ ./
ENTRYPOINT ["java", "-jar", "application.jar"]
```

业务代码变更时，通常只需重建最后的 `application` 层；依赖层可命中 Docker 缓存。同一文档还介绍在该布局上叠加 AOT Cache / CDS 以缩短 JVM 冷启动（与分层正交，本文不展开）。

自定义分层规则见 Maven [Packaging Layered Jar](https://docs.spring.io/spring-boot/maven-plugin/packaging.html) 或 Gradle [Packaging Layered Jar or War](https://docs.spring.io/spring-boot/gradle-plugin/packaging.html)。

## Cloud Native Buildpacks（bootBuildImage）

CNB 规范与 Paketo 实现见专文 [CNB: Cloud Native Buildpacks 与 Paketo](../../cloud/cloud-native-buildpacks.md)。下文只保留与 Spring Boot 插件相关的要点。

Spring Boot 内置 [Cloud Native Buildpacks](https://docs.spring.io/spring-boot/reference/packaging/container-images/cloud-native-buildpacks.html) 集成：插件把可执行 jar 交给 builder（默认 Paketo），buildpack 检测 artifact、安装 JRE、生成启动命令并产出 OCI 镜像。

```bash
./mvnw spring-boot:build-image
# Gradle
./gradlew bootBuildImage
```

要点：

- 无需先手动 `repackage`：插件会在需要时自动打可执行 jar。
- 需要本机可访问的 Docker daemon（或按插件文档配置远程构建）。
- 默认 builder 为 `paketobuildpacks/builder-noble-java-tiny:latest`（以当前 Spring Boot 插件文档为准）。
- [Paketo Spring Boot buildpack](https://github.com/paketo-buildpacks/spring-boot) 会读取 jar 中的 `Spring-Boot-Layers-Index` / `layers.idx`，日志里可见 `Creating slices from layers index`，把应用切成多个镜像层——与上一节分层 JAR 设计对齐。

Maven 配置 JVM 版本示例（传给 Paketo 环境变量）：

```xml
<plugin>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-maven-plugin</artifactId>
  <configuration>
    <image>
      <env>
        <BP_JVM_VERSION>21</BP_JVM_VERSION>
      </env>
    </image>
  </configuration>
</plugin>
```

Gradle 等价配置见 [BootBuildImage](https://docs.spring.io/spring-boot/gradle-plugin/api/java/org/springframework/boot/gradle/tasks/bundling/BootBuildImage.html) API 文档中的 `environment` / `builder`。

Buildpack 路径下，运行时默认安装的是 JRE（`BP_JVM_TYPE` 默认为 `JRE`），不是 GraalVM Native；Native 需另开 `BP_NATIVE_IMAGE=true` 等配置，见 [GraalVM Native Image 简介](../graalvm-native-image.md)。

## Buildpack + jlink 裁剪 JRE

jlink（JDK 9+ 模块系统）可从完整 JDK 生成只含所需模块的定制 JRE，仍用 HotSpot 跑字节码，与 GraalVM Native Image（AOT 成本地二进制）不同。手工多阶段 Dockerfile 里常用 `jdeps` + `jlink`；走 Paketo 时由 Java buildpack 代为执行。

重要事实：Paketo 文档写明 [Install a Minimal JRE with JLink](https://paketo.io/docs/howto/java/) 中 `BP_JVM_JLINK_ENABLED` 默认为 `false`。即 `bootBuildImage` 默认装完整 JRE，不会自动 jlink；要缩小运行时需显式开启。

```bash
pack build my-app \
  --path target/myapp.jar \
  --env BP_JVM_JLINK_ENABLED=true
```

自定义 jlink 参数（传入后不再使用 Paketo 默认参数集）：

```bash
pack build my-app \
  --env BP_JVM_JLINK_ENABLED=true \
  --env BP_JVM_JLINK_ARGS="--no-header-files --compress=1 --add-modules java.base,java.se"
```

在 Spring Boot 插件中通过 `image.env` 传入相同变量即可。典型场景：JVM 发行版只提供 JDK、镜像里被迫带完整 JDK 时，用 jlink 生成精简 JRE（Paketo 文档以 Amazon Corretto 为例）。

| 维度 | 默认 Buildpack（JRE） | Buildpack + jlink | GraalVM Native（另文） |
| ---- | --------------------- | ----------------- | ---------------------- |
| 运行时 | HotSpot + 完整 JRE | HotSpot + 定制 JRE | Substrate VM，无 `java -jar` |
| 应用形态 | 字节码 fat jar | 字节码 fat jar | AOT 本地可执行文件 |
| 默认是否开启 | 是 | 否，需 `BP_JVM_JLINK_ENABLED=true` | 否，需 native profile / env |
| Spring AOT | 不需要 | 不需要 | 需要 |

jlink 模块裁剪与 JPMS 关系见 [JPMS 与 Jigsaw](../../../cs/jpms-jigsaw.md)；与 [Spring AOT](./spring-aot.md) 无直接关系。

## 如何选型（简表）

| 场景 | 建议 |
| ---- | ---- |
| 本地试容器、学习 | Fat jar + 简单 Dockerfile |
| 自建 CI、要控制每一层 COPY | 分层 JAR + 官方 Dockerfile 模板 |
| 团队想少维护 Dockerfile、与 Paketo 生态一致 | `bootBuildImage` / `spring-boot:build-image` |
| 镜像体积敏感、仍要完整 JVM 语义 | Buildpack + `BP_JVM_JLINK_ENABLED=true`，或手写 jlink 多阶段构建 |
| 冷启动毫秒级、接受 AOT 约束 | 见 [GraalVM Native Image 简介](../graalvm-native-image.md)，不是本文三条 JVM 路径的延伸 |

多数长期运行的 REST 服务：分层 JAR + Buildpack 或分层 Dockerfile 即可；jlink 在镜像体积成为瓶颈时再开。

## 官方文档索引

| 主题 | 链接 |
| ---- | ---- |
| Packaging 总览 | https://docs.spring.io/spring-boot/reference/packaging/index.html |
| Container Images 章节入口 | https://docs.spring.io/spring-boot/reference/packaging/container-images/index.html |
| Efficient Container Images（分层 JAR 原理） | https://docs.spring.io/spring-boot/reference/packaging/container-images/efficient-images.html |
| Dockerfiles + jarmode | https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html |
| Cloud Native Buildpacks 概述 | https://docs.spring.io/spring-boot/reference/packaging/container-images/cloud-native-buildpacks.html |
| Maven `spring-boot:build-image` | https://docs.spring.io/spring-boot/maven-plugin/build-image.html |
| Gradle `bootBuildImage` | https://docs.spring.io/spring-boot/gradle-plugin/api/java/org/springframework/boot/gradle/tasks/bundling/BootBuildImage.html |
| Maven 可执行 jar / 分层配置 | https://docs.spring.io/spring-boot/maven-plugin/packaging.html |
| Gradle `bootJar` / 分层配置 | https://docs.spring.io/spring-boot/gradle-plugin/packaging.html |
| Paketo Java（含 jlink env） | https://paketo.io/docs/howto/java/ |
| Paketo Spring Boot buildpack | https://github.com/paketo-buildpacks/spring-boot |

## 参考

- [CNB: Cloud Native Buildpacks 与 Paketo](../../cloud/cloud-native-buildpacks.md)
- [Spring Boot](./spring-boot.md)
- [Spring AOT 简介](./spring-aot.md)
- [GraalVM Native Image 简介](../graalvm-native-image.md)
- [JPMS 与 Jigsaw](../../../cs/jpms-jigsaw.md)
