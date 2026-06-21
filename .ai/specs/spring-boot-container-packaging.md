# Spec: Spring Boot Container Packaging: Fat JAR、分层 JAR 与 Buildpacks

| 字段 | 值 |
| ---- | -- |
| 状态 | draft-written |
| 交付物 | `content/post/language/java/spring/spring-boot-container-packaging.md` |
| Hugo url | `spring-boot-container-packaging` |
| 标题 | Spring Boot Container Packaging: Fat JAR、分层 JAR 与 Buildpacks |
| 分类 | language |

---

## 1. 目的

为 Spring Boot REST API 容器化部署提供一篇索引型说明：fat jar、分层 JAR、Cloud Native Buildpacks（`bootBuildImage`）、Paketo jlink 裁剪 JRE 的关系、官方文档入口与选型要点。

## 2. 读者

已会用 Spring Boot 写 REST API、准备上 Docker/K8s，想系统了解官方推荐的几种 JVM 容器打包路径（不含 GraalVM Native Image 专文，可互链）。

## 3. 核心信息（必须传达）

- Fat jar 是可执行 uber jar，`java -jar` 即可跑；容器里可直接 COPY，但不是镜像缓存最优解。
- 分层 JAR（`layers.idx`）把依赖与业务代码拆层，利于 Docker 层缓存；Boot 2.3+ 默认开启。
- `spring-boot:build-image` / `bootBuildImage` 走 Paketo CNB；会读 `layers.idx` 切镜像层。
- Paketo jlink 默认关闭，需 `BP_JVM_JLINK_ENABLED=true` 才裁剪 JRE；与 GraalVM Native 是不同路径。
- 提供官方文档链接地图，便于延伸阅读。

## 4. 必须包含（验收清单）

- [ ] 标题、url、分类与 Spec 表一致
- [ ] 正文从 `##` 起，无 `#`（MD025）
- [ ] 标签（SDD）：`original`、`AI-assisted` + 内容标签；无 `remix`、`reprint`
- [ ] 三节主体：fat jar、分层 JAR + Buildpack、Buildpack + jlink
- [ ] 路径关系图（mermaid 或 ascii）
- [ ] 官方文档索引表
- [ ] 与 [spring-boot.md](../content/post/language/java/spring/spring-boot.md)、[graalvm-native-image.md](../content/post/language/java/graalvm-native-image.md) 互链

## 5. 禁止包含（Do NOT）

- 不把 GraalVM Native Image 当本文主线（仅对比一句 + 外链专文）
- 不写「最佳实践」「终极指南」类标题
- 不编造 Paketo 默认开启 jlink

## 6. 语气与风格（本篇特有）

技术说明/索引文；客观叙述；其余见 [delivery-style.md](../delivery-style.md)。

## 7. 建议结构（大纲）

1. 背景与三条路径总览
2. Fat JAR
3. 分层 JAR
4. Cloud Native Buildpacks
5. Buildpack + jlink
6. 选型简表
7. 官方文档索引
8. 参考

---

## A. 原始素材

> **AI 禁止修改本章节任何内容。**

### 2026-06-21

用户希望有一篇 blog 文档用于了解 Spring Boot 容器化部署的几点：

1. fat jar
2. 分层 JAR + Cloud Native Buildpacks（bootBuildImage）
3. Buildpack + jlink 裁剪 JRE

来源：与 AI 对话中整理的 Spring Boot 官方 Packaging → Container Images 文档地图；需纠正「Buildpack 默认 jlink」——Paketo 文档写明 `BP_JVM_JLINK_ENABLED` 默认 false。

---

## B. AI 审阅 · 问答

### Round 1

**Q:** 是否把 GraalVM Native Image 写入本文主体？

**A:** 否，仅对比一句并链到 graalvm-native-image.md；本文聚焦 JVM 三条路径。

**Q:** 是否包含手写 Dockerfile + jarmode 示例？

**A:** 是，作为分层 JAR 的 Dockerfile 路径简要示例，与 Buildpack 并列。

建议进入 ready-to-write。

---

## C. 批注

---

## 10. 变更记录

| 日期 | 变更 |
| ---- | ---- |
| 2026-06-21 | 初版 Spec；直接输出正文（作者明确要 blog 文档） |
