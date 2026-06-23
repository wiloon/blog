# Spec: 2026 W26

| 字段     | 值                                       |
| -------- | ---------------------------------------- |
| 状态     | collecting                               |
| 交付物   | `content/post/career/weekly-2026-w26.md` |
| Hugo url | `weekly-2026-w26`                        |
| 标题     | 2026 W26                                 |
| 分类     | career                                   |

---

## 验收清单

- [ ] 标题、url、分类与 Spec 表一致
- [ ] 正文从 `##` 起，无 `#`（MD025）
- [ ] 标签（SDD）：`original`、`AI-assisted` + 内容标签；无 `remix`、`reprint`

---

## A. 原始素材

> **AI 禁止修改本章节任何内容。** 以下是作者的原始输入，可能是语音转文字或意识流记录，结构不完整、语言口语化均可。每次补充时新增带日期的子节。

### 2026-06-23（来自 W25 交接）

W25 周记只写「产生给 enx 加 Java 后端」的想法；本周（W26）写 6/22 起的实际动手：enx-api-java 脚手架、Homelab 部署与 CI/CD 等。

---

## B. AI 审阅 · 问答

> **规则：**
>
> - AI 只在此处末尾追加新 Round，**不修改已有 Round 的任何内容**
> - 每轮结束时 AI 判断信息是否充分，若充分则写"建议进入 ready-to-write"，**状态由作者手动更新**
> - 作者在"作者回答"下填写，完成后通知 AI 继续下一轮或输出正文

---

## C. 批注

> AI 在生成正文过程中发现的歧义或待确认项，记录于此，供作者参考。

### 与 W25 的衔接

- W25 已交代 enx Cognito 部署与「加 Java 后端」动机；W26 从实施写起，避免重复 W25 叙述
- W25 脱敏的简历/PDF 流程若 6/22 还有收尾 commit，已在 W25 侧处理，W26 除非有新进展否则不写招聘

---

## D. Commit 整理（AI · 种子）

> 统计范围：ISO 2026-W26 起（6/22 周一—）。随本周推进由 AI 或作者补充。
>
> 来源：`blog`、`w10n-config`、`enx` 三仓库 `git log`。

### 6/22（W26 第一天）

**enx**

- `enx-api-java` Spring Boot 项目脚手架（Gradle、分层结构、Cognito Security、前端日志 API）
- TASK-SPEC 文档（`TASK-SPEC-enx-api-java.md`、`TASK-SPEC-enx-api-gateway-v1.md`）
- Containerfile、Nexus Maven 私服 CI 构建配置（`gradle/ci.init.gradle`）

**w10n-config**

- k8s `deployment-java.yaml`、`service-java.yaml`、ingress 调整
- Tekton `pipeline-build-enx-api-java`、`task-pack-build-java`
- workstation Cursor 双安装（AppImage + AUR）playbook
- resume PDF 流水线收尾（`markdown to pdf`、`resume typeset`）— 若 W25 已写完可不在 W26 重复
- `ops/finance/` 理财文档更新（京东小金保、汇丰港险等）

**blog**

- resume 相关 markdown（若属 W25 简历叙事则 W26 跳过）

### 周记正文建议结构（草案）

1. **enx-api-java 启动** — 从 W25 想法到脚手架：技术选型、模块划分、与现有 Go API / Cognito 的关系
2. **Homelab 集成** — Tekton 构建、k8s 部署、Nexus 依赖拉取
3. **其它** — 待本周素材补充（finance、homelab 等是否写入由作者决定）

**状态：** collecting，待作者补充 A 节素材或确认 6/22 种子是否足够起草。
