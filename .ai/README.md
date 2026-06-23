# 博客 AI 文档

本目录 **不会** 被 Hugo 发布（位于 `content/` 之外，不参与站点构建）。

## 文档索引

| 文件                                             | 用途                                                                                     |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| [article-sdd.md](article-sdd.md)                 | **文章 SDD**：Spec 驱动写作流程、AI 约束、Spec 是否上线                                  |
| [delivery-style.md](delivery-style.md)           | **仅 SDD 交付物**：共通 prose 文风（加粗、人称适度用「我」、语气）；无 Spec 的文章不适用 |
| [content-constraints.md](content-constraints.md) | **全站内容约束**：VPN 相关表述（WireGuard/OpenVPN 除外不写软件名）；代码块注释用英文等 |
| [internal-links.md](internal-links.md)           | **全站内链**：相对 `.md` + Hugo embedded hook                                            |
| [specs/](specs/)                                 | 各篇文章 Spec（**作者维护**；AI 按 Spec 润色/输出交付物）                                |

## 文章 Spec 一览

| Spec                                                                                 | 交付物                                                                                                                                             |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [specs/exploration.md](specs/exploration.md)                                         | [career/exploration.md](../content/post/career/exploration.md)                                                                                     |
| [specs/booster-recovery.md](specs/booster-recovery.md)                               | [content/post/starship/booster-recovery.md](../content/post/starship/booster-recovery.md)                                                          |
| [specs/java-knowledge-map.md](specs/java-knowledge-map.md)                           | [java-knowledge-map.md](../content/post/language/java/java-knowledge-map.md) + **全站**内链迁移（`scripts/migrate-internal-links.py --scope all`） |
| [specs/iot-protocol-oom-mysql-influxdb.md](specs/iot-protocol-oom-mysql-influxdb.md) | （review）[career/iot-protocol-oom-mysql-influxdb.md](../content/post/career/iot-protocol-oom-mysql-influxdb.md)                                   |
| [specs/pve-storage.md](specs/pve-storage.md)                                         | （review）[cloud/pve-storage.md](../content/post/cloud/pve-storage.md)                                                                             |
| [specs/android-apk-security-assessment.md](specs/android-apk-security-assessment.md) | `content/post/career/android-apk-security-assessment.md`                                                                                           |
| [specs/weekly-2026-w23.md](specs/weekly-2026-w23.md)                                 | `content/post/career/weekly-2026-w23.md`                                                                                                           |
| [specs/weekly-2026-w24.md](specs/weekly-2026-w24.md)                                 | `content/post/career/weekly-2026-w24.md`                                                                                                           |
| [specs/starbucks-latte-vs-indie-cafe.md](specs/starbucks-latte-vs-indie-cafe.md)     | `content/post/life/starbucks-latte-vs-indie-cafe.md`                                                                                               |
| [specs/weekly-2026-w25.md](specs/weekly-2026-w25.md)                                 | `content/post/career/weekly-2026-w25.md`                                                                                                           |
| [specs/weekly-2026-w26.md](specs/weekly-2026-w26.md)                                 | `content/post/career/weekly-2026-w26.md`                                                                                                           |
| [specs/spring-boot-container-packaging.md](specs/spring-boot-container-packaging.md) | [spring/spring-boot-container-packaging.md](../content/post/language/java/spring/spring-boot-container-packaging.md)                               |
| [specs/cloud-native-buildpacks.md](specs/cloud-native-buildpacks.md)                 | [cloud/cloud-native-buildpacks.md](../content/post/cloud/cloud-native-buildpacks.md)                                                               |
| [specs/iot-third-party-data-push.md](specs/iot-third-party-data-push.md)             | `content/post/career/iot-third-party-data-push.md`                                                                                                 |
**内容目录 `content/post/career/`**：职业/面试向叙事与项目故事（[exploration](../content/post/career/exploration.md)、[conflict-check](../content/post/career/conflict-check.md)、OOM 案例等）。

## 工作流（SDD）

1. **你** 在 `.ai/specs/{slug}.md` 写需求与验收。
2. **AI** 阅读 Spec + [AGENTS.md](../AGENTS.md)，更新 `content/post/.../{slug}.md`。
3. 用 Spec 里的验收清单自查；Spec **不** 出现在最终 blog 页面。

详见 [article-sdd.md](article-sdd.md)。新建 Spec 可复制 [specs/_template.md](specs/_template.md)。

**SDD 交付物标签：** `original` + `AI-assisted`（不用 `remix`）。
