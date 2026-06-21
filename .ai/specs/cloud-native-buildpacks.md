# Spec: CNB: Cloud Native Buildpacks 与 Paketo

| 字段 | 值 |
| ---- | -- |
| 状态 | draft-written |
| 交付物 | `content/post/cloud/cloud-native-buildpacks.md` |
| Hugo url | `cloud-native-buildpacks` |
| 标题 | CNB: Cloud Native Buildpacks 与 Paketo |
| 分类 | cloud |

---

## 1. 目的

介绍 CNB 规范与 Paketo 实现，帮助读者理解 buildpack / builder / lifecycle，以及与 Spring Boot `bootBuildImage` 的关系。

## 2. 读者

用过 Docker、准备或正在用 Spring Boot 容器化，想弄清 Paketo 在生态中的位置。

## 3. 核心信息

- CNB 是容器镜像构建规范与生态，不是某一个产品
- Paketo 是常用开源 CNB 实现
- Spring Boot 默认 builder 指向 Paketo
- 与手写 Dockerfile、分层 JAR 的关系链到 spring-boot-container-packaging

## 4. 验收清单

- [ ] 标题含英文、url `cloud-native-buildpacks`
- [ ] 标签 original + AI-assisted
- [ ] 互链 spring-boot-container-packaging

## A. 原始素材

### 2026-06-21

用户问 blog 是否有 CNB/Paketo 文档；没有则新建，用于学习了解。

---

## B. AI 审阅 · 问答

### Round 1

**Q:** 一篇还是两篇？

**A:** 一篇：CNB 讲规范与概念，Paketo 作为主流实现专节；避免两篇过薄。

建议进入 ready-to-write。

---

## C. 批注

---

## 10. 变更记录

| 日期 | 变更 |
| ---- | ---- |
| 2026-06-21 | 初版 |
