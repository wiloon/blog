# Spec: Spring Boot Executable JAR: Fat JAR 与 JarLauncher

| 字段 | 值 |
| ---- | -- |
| 状态 | draft-written |
| 交付物 | `content/post/language/java/spring/spring-boot-executable-jar.md` |
| Hugo url | `spring-boot-executable-jar` |
| 标题 | Spring Boot Executable JAR: Fat JAR 与 JarLauncher |
| 分类 | language |

---

## 1. 目的

说明 Spring Boot 可执行 JAR（fat jar）的产物结构、`JarLauncher` 启动链，以及 Maven `repackage` / Gradle `bootJar` 的构建方式。从 [spring-boot-container-packaging.md](spring-boot-container-packaging.md) 拆出，供容器打包文与 [spring-boot.md](../content/post/language/java/spring/spring-boot.md) 互链。

## 2. 读者

已会用 Spring Boot 写应用、执行过 `java -jar`，想理解「为什么一个 jar 能带齐依赖跑起来」。

## 3. 核心信息（必须传达）

- Fat jar / uber jar / executable jar 在 Spring Boot 语境下同义；与 thin jar 对比。
- 布局：`BOOT-INF/classes`、`BOOT-INF/lib`、`spring-boot-loader`。
- `MANIFEST.MF`：`Main-Class` → JarLauncher，`Start-Class` → 业务主类。
- JarLauncher 负责嵌套 jar 的 classpath 与转调 `Start-Class`。
- `repackage` / `bootJar` 生成可执行 jar；plain jar 常被重命名为 `*.jar.original`。
- `BOOT-INF/` 为 Spring Boot 约定，非 Java/JAR 标准。
- Fat jar 可含 `static/` 静态前端；`java -jar` 启动内嵌 Web 容器监听端口。
- 可执行 WAR（`WarLauncher`）兼顾 `java -jar` 与外部 Tomcat；REST API 也可打 WAR。
- 容器镜像优化见 container-packaging 专文，本文不展开 Docker。

## 4. 必须包含（验收清单）

- [ ] 标题、url、分类与 Spec 表一致
- [ ] 正文从 `##` 起，无 `#`（MD025）
- [ ] 标签：`original`、`AI-assisted` + 内容标签
- [ ] thin vs fat 对比表、目录树、启动流程说明
- [ ] 与 spring-boot.md、spring-boot-container-packaging.md 互链
- [ ] 可选互链 maven-executable-jar（通用 fat jar，机制不同）

## 5. 禁止包含（Do NOT）

- 不把 Docker / Buildpack / 分层 JAR 当本文主线
- 不写「最佳实践」「终极指南」类标题

## 6. 语气与风格

技术说明；客观叙述；见 [delivery-style.md](../delivery-style.md)。

## 7. 建议结构（大纲）

1. 背景
2. Thin jar 与 fat jar
3. 布局与 MANIFEST.MF
4. JarLauncher 启动链
5. Fat jar 与 Web 服务（静态资源、JSP 限制）
6. 可执行 WAR 与 JAR 选型
7. 构建（Maven / Gradle）
8. 与普通可执行 jar 的区别
9. 参考

## 10. 变更记录

| 日期 | 变更 |
| ---- | ---- |
| 2026-06-24 | 从 container-packaging 拆出专文 Spec |
| 2026-06-24 | 补充 BOOT-INF 约定、Web 静态资源、可执行 WAR 与 JAR 选型 |
