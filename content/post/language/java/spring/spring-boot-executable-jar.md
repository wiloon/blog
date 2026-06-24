---
title: "Spring Boot Executable JAR: Fat JAR 与 JarLauncher"
author: "-"
date: 2026-06-24T13:35:21+08:00
lastmod: 2026-06-24T13:35:21+08:00
url: spring-boot-executable-jar
categories:
  - language
tags:
  - original
  - AI-assisted
  - java
  - spring
  - spring-boot
  - maven
  - gradle
---

## 背景

Spring Boot 把应用打成单个可执行 JAR，`java -jar app.jar` 即可启动内嵌 Tomcat（或 Jetty/Undertow）与全部依赖。这与传统「WAR 部署到外部 Tomcat、classpath 由容器管理」不同，也不同于 Maven `jar-with-dependencies` 那种把依赖 class 解压合并进一个 jar 的做法。

本文说明 Spring Boot 可执行 JAR 的内部布局、`JarLauncher` 如何启动应用，以及 `repackage` / `bootJar` 如何生成该产物。容器镜像、分层 JAR、Buildpack 等部署话题见 [Spring Boot Container Packaging](./spring-boot-container-packaging.md)；框架层面的「内嵌服务器 + 可执行 JAR」见 [Spring Boot](./spring-boot.md)。

## Thin jar 与 fat jar

Fat jar、uber jar、executable jar 在 Spring Boot 语境下指同一件事：一个「全包」可执行 jar。Fat jar 与 uber jar 只是不同叫法（uber 来自德语 über，意为「之上 / 全部」）；Spring 官方文档更常写 executable jar。

与 Maven/Gradle 默认打出的普通 jar（常称 thin jar / plain jar）对比如下：

| | 普通 jar（thin / plain jar） | Fat jar（uber jar / executable jar） |
| ---- | ---------------------------- | ------------------------------------ |
| 内容 | 通常只有项目自己的 `.class` 与资源 | 应用代码 + 全部依赖 + `spring-boot-loader`（及内嵌服务器等） |
| 依赖在哪 | 不在 jar 内，需 classpath 或外部 lib | 嵌在 `BOOT-INF/lib/*.jar` |
| `java -jar` | 一般不能直接跑（缺依赖） | 可以，一条命令启动 |
| Spring Boot 谁生成 | `jar` 任务 / `mvn package` 的原始产物（常被重命名为 `*.jar.original`） | `repackage` / `bootJar` 的产物 |
| 典型用途 | 作为库被别的项目依赖 | 部署、`java -jar` 运行、作为容器镜像输入 |

## 布局与 MANIFEST.MF

Spring Boot 可执行 JAR 使用固定目录约定，而不是把依赖 class 全部解压到 jar 根目录：

```text
app.jar
├── META-INF/MANIFEST.MF     # Main-Class → JarLauncher，Start-Class → 你的 @SpringBootApplication
├── org/springframework/boot/loader/   # spring-boot-loader 启动类
└── BOOT-INF/                # Spring Boot 专有布局，非 Java/JAR 标准
    ├── classes/             # 你的代码、application.yml、static/ 等
    └── lib/                 # 第三方依赖，每个依赖仍是独立 .jar
```

`BOOT-INF/`、`BOOT-INF/classes/`、`BOOT-INF/lib/` 是 **Spring Boot 为可执行 JAR 定义的约定**，不是 [JAR 文件格式](https://docs.oracle.com/javase/8/docs/technotes/guides/jar/jar.html) 或 JDK 规范的一部分。标准 JAR 只约定 `META-INF/MANIFEST.MF` 等元数据，应用 class 通常直接放在 jar 根目录的包路径下；标准 classpath 也不支持「jar 内嵌套 jar 自动可用」，因此需要 `JarLauncher` 与自定义 ClassLoader。

`META-INF/MANIFEST.MF` 里与启动相关的关键项：

| 属性 | 含义 |
| ---- | ---- |
| `Main-Class` | JVM 执行 `java -jar` 时加载的类，Spring Boot 设为 `org.springframework.boot.loader.launch.JarLauncher` |
| `Start-Class` | 你的业务主类（带 `public static void main` 的 `@SpringBootApplication` 类） |

可用下面命令查看打包结果：

```bash
unzip -p target/myapp.jar META-INF/MANIFEST.MF
```

`Main-Class` 与 `Start-Class` 的分工是 Spring Boot 可执行 JAR 的核心：`Main-Class` 不是业务类，而是 loader 入口。`MANIFEST.MF` 通用字段说明见 [MANIFEST.MF](../../../other/manifest-mf.md)。

## JarLauncher 启动链

执行 `java -jar app.jar` 时，JVM 只认 `MANIFEST.MF` 里的 `Main-Class`，因此实际入口是 `JarLauncher`，而不是你的 `MyApplication`。

```text
java -jar app.jar
  → JVM 启动 JarLauncher.main()
  → 自定义 ClassLoader 挂载 BOOT-INF/classes 与 BOOT-INF/lib 内嵌套 jar
  → 读取 Start-Class，反射调用业务 main()
  → SpringApplication.run(...) 启动内嵌服务器与 Spring 容器
```

JarLauncher 来自 `spring-boot-loader` 模块，打进可执行 jar 的 `org/springframework/boot/loader/` 目录。它解决的是标准 JAR 布局的限制：应用类在 `BOOT-INF/classes/`，依赖在 `BOOT-INF/lib/*.jar` 里仍是嵌套 jar，普通 classpath 无法直接加载；loader 在启动阶段把这些路径挂到可搜索的 classpath 上，再转调 `Start-Class`。

这与 [Spring Boot](./spring-boot.md) §启动应用 里「一条 `java -jar` 拉起内嵌 Tomcat」的用户体验一致；内嵌 Tomcat 的启动发生在 `SpringApplication.run` 之后，属于业务主类一侧的逻辑。

## Fat jar 与 Web 服务

Fat jar 不限于纯 REST API：`java -jar` 启动后会拉起内嵌 Web 容器（默认 Tomcat 监听 **8080**），同时提供 HTTP API 与静态资源。

`src/main/resources/` 下的内容会打进 `BOOT-INF/classes/`，例如：

```text
src/main/resources/
├── application.yml
├── static/              # 静态前端：html、js、css、图片
│   ├── index.html
│   └── js/app.js
└── templates/           # Thymeleaf 等服务端模板（可选）
```

打包后对应 `BOOT-INF/classes/static/index.html` 等路径。浏览器访问 `http://localhost:8080/` 或 `/index.html` 可拿到页面；`/api/...` 由 `@RestController` 处理。前后端分离项目也常把 React/Vue 的 `dist/` 在构建时拷入 `static/`，与 API 打进同一个 jar，一个进程同时提供接口与静态站点。

| 前端形态 | 能否打进 fat jar | 说明 |
| -------- | ---------------- | ---- |
| 纯静态 HTML/JS/CSS | 是 | 放 `resources/static/` |
| SPA 构建产物（React/Vue 等） | 是 | 构建输出拷入 `static/` |
| Thymeleaf 等服务端模板 | 是 | 模板在 `resources/templates/` |
| JSP | 可执行 JAR 基本不行 | 需打 WAR；见 [Spring MVC](./spring-mvc.md) §Spring Boot 与 JSP |

WAR 只是另一种打包格式，并不等同于「带前端页面」——纯 JSON 的 REST API 也可以打成 WAR 部署到外部 Tomcat，见下一节。

## 可执行 WAR 与 JAR 选型

除可执行 JAR 外，Spring Boot 还可打成 **可执行 WAR**：在 Servlet 规范的 `WEB-INF/` 布局上写入 `WarLauncher`，`MANIFEST.MF` 的 `Main-Class` 指向 `org.springframework.boot.loader.launch.WarLauncher`。

```text
app.war
├── META-INF/MANIFEST.MF       # Main-Class → WarLauncher
├── org/springframework/boot/loader/
└── WEB-INF/                   # Servlet 规范目录（WEB-INF 本身来自 Servlet 规范）
    ├── classes/
    ├── lib/
    └── lib-provided/          # provided 依赖，供外部容器使用
```

可执行 WAR 支持两种部署方式：

1. `java -jar app.war` —— 与 JAR 类似，内嵌 Tomcat 独立进程启动
2. 拷贝到外部 Tomcat 的 `webapps/` —— 由容器加载，此时内嵌 Tomcat 依赖以 `provided` 形式放在 `WEB-INF/lib-provided/`，不打进运行时 classpath

Tomcat 只提供 Servlet 容器；返回 JSON 还是 HTML 对容器无区别。**RESTful API 完全可以打成 WAR 部署在外部 Tomcat**，传统 Spring MVC 时代很常见。Spring Boot 默认推 JAR，是因为微服务场景更倾向「每个应用独立进程、`java -jar` 即可」，而不是 WAR 不能跑 API。

| | 可执行 JAR | 可执行 WAR |
| ---- | ---------- | ---------- |
| 布局 | `BOOT-INF/`（Spring Boot 约定） | `WEB-INF/`（Servlet 规范） |
| Launcher | `JarLauncher` | `WarLauncher` |
| `java -jar` | 是 | 是 |
| 外部 Tomcat 部署 | 否 | 是 |
| `static/` 静态资源 | 是 | 是 |
| JSP（`src/main/webapp/`） | 基本不行 | 可以 |

日常 REST 服务默认 `JarLauncher` + JAR 即可。需要外部 Tomcat、或必须用 JSP 时再选 WAR。`PropertiesLauncher` 支持更灵活的 classpath（如外部 `lib/` 目录），需在 `MANIFEST.MF` 配置 `Loader` 等属性，使用较少。

## 构建：repackage 与 bootJar

可执行 JAR 由 Spring Boot 打包插件在默认 `jar` / `bootJar` 任务之上二次处理生成：

- Maven：`spring-boot-maven-plugin` 的 `repackage` goal（使用 `spring-boot-starter-parent` 时通常已绑定到 `package` 阶段）
- Gradle：`bootJar` 任务（`build` / `assemble` 会自动执行）

WAR 对应 Maven 的 `repackage` + `<packaging>war</packaging>`，或 Gradle 的 `bootWar` 任务。

```bash
./mvnw package
java -jar target/myapp.jar

# Gradle
./gradlew bootJar
java -jar build/libs/myapp.jar
```

`repackage` 会把 Maven 默认 `jar` 任务产出的 thin jar 重命名为 `*.jar.original`，再写出可执行 fat jar 覆盖最终文件名。若项目要同时作为库被依赖，应保留 thin jar（`*.jar.original`），不要把 fat jar 发布到 Maven 仓库供他人 compile 依赖。

官方打包说明：

- Maven：https://docs.spring.io/spring-boot/maven-plugin/packaging.html
- Gradle：https://docs.spring.io/spring-boot/gradle-plugin/packaging.html

## 与普通可执行 jar 的区别

在 Spring Boot 之前或之外，Java 生态里也有「可执行 fat jar」，常见做法不同：

| 方式 | 机制 | 与 Spring Boot 的差异 |
| ---- | ---- | --------------------- |
| Maven Assembly `jar-with-dependencies` | 依赖解压合并，`Main-Class` 直接指向业务类 | 无 `BOOT-INF`、无嵌套 lib jar、无 JarLauncher |
| Maven Shade Plugin | 重定位/合并 class，防冲突 | 同上，且侧重 uber jar 冲突处理 |
| Gradle `application` 插件 | 生成带脚本与 lib 目录的分发物 | 常是目录 + 启动脚本，而非单 jar 嵌套 lib |

本站笔记：[Maven 可执行 jar](../../../cs/maven-executable-jar.md)、[Gradle application 插件](../../../cs/gradle-executable-jar.md)、[maven-shade-plugin](../../../cs/maven-shade-plugin.md)。Spring Boot 选择「嵌套 jar + loader」布局，是为了加快打包、避免类冲突合并，并支持后续分层 JAR（`layers.idx`）与 Buildpack 切层——分层与容器化见 [Spring Boot Container Packaging](./spring-boot-container-packaging.md)。

## 参考

- [Spring Boot](./spring-boot.md)
- [Spring MVC](./spring-mvc.md)
- [Spring Boot Container Packaging](./spring-boot-container-packaging.md)
- [MANIFEST.MF](../../../other/manifest-mf.md)
- [Maven 可执行 jar](../../../cs/maven-executable-jar.md)
- [Spring Boot Packaging 官方文档](https://docs.spring.io/spring-boot/reference/packaging/index.html)
