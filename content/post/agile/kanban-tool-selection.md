---
title: "看板工具选型：一人公司的项目管理工具"
author: "-"
date: 2026-06-15T11:52:11+08:00
lastmod: 2026-06-15T11:52:11+08:00
url: kanban-tool-selection
categories:
  - agile
tags:
  - linear
  - jira
  - kanban
  - original
  - AI-assisted
---

## 背景

我把自己的职业和生活当作一人公司来经营（详见 [一人公司：我对个人运营的理解](../life/one-person-company.md)），公司运营本质上就是个人运营。我需要一个看板工具来管理：

- 日常任务和待办事项
- 项目进度追踪
- 个人运营规划

我熟悉 Jira，也知道 Trello，但想在选型时认真考虑 **AI 集成能力**（MCP/CLI/API），因为工作流中越来越多地用到 AI 工具。

## 候选工具

| 排名 | 工具 | AI/MCP 集成 | UI 直观度 | 适合一人公司 |
| --- | --- | --- | --- | --- |
| 1 | **Linear** | 官方 MCP server，REST API 完善 | 极简优雅 | ✅ |
| 2 | **Notion** | 官方 MCP server，API 完善 | 灵活但需配置 | ✅ |
| 3 | **Height** | API + 内置 AI 功能 | 现代，接近 Linear | ✅ |
| 4 | **Todoist** | 社区 MCP，REST API | 简洁直观 | ✅ |
| 5 | **Obsidian** | 社区 MCP 插件，本地控制好 | Markdown，需适应 | ⚠️ |
| 6 | **Trello** | 有 MCP，API 可用但功能有限 | 看板直观 | ⚠️ |
| 7 | **Jira** | Atlassian MCP，API 完善 | 功能丰富但偏重 | ❌ |
| 8 | **Things 3** | 几乎无 API | 最美 macOS 体验 | ❌ |

## Linear vs Jira 详细对比

### 核心定位

Linear 是为小团队和快速迭代设计的，Jira 是面向大型企业复杂流程的。Linear 本身就是为了解决"Jira 太重"这个问题而造的。

### 项目结构

- **Linear**：Issues → Projects → Cycles（Sprint）→ Roadmap，层级清晰不复杂
- **Jira**：Epic → Story → Task → Sub-task，加上 Board/Backlog/Sprint，配置项极多

概念基本一致：Cycle ≈ Sprint，Issue ≈ Story/Task，Project ≈ Board。熟悉 Jira 的人半天内可以上手 Linear。

### AI / MCP 集成

- **Linear**：官方维护 `linear-mcp`，可以直接让 AI 创建/查询/更新 issues，体验原生
- **Jira**：Atlassian 有 MCP，但偏企业方向，个人用配置复杂

### 速度与体验

- **Linear**：键盘快捷键完善，创建一个 issue 几秒钟，页面响应快
- **Jira**：页面加载慢，字段多，每次操作有摩擦感

### 价格

- **Linear**：免费版支持无限 issues，一人公司完全够用
- **Jira**：免费版限 10 人，个人用免费，但功能受限

## 选型结论

选择 **Linear**。

主要理由：

1. 官方 MCP 集成，可以在 AI 工作流（Claude、Copilot）中直接操作 issues
2. 对熟悉 Jira 的人几乎没有学习成本，概念体系一致
3. UI 更轻量，日常操作摩擦更小
4. 免费版对一人公司足够

Jira 作为备选了解即可，如果未来需要和使用 Jira 的客户/团队协作，熟悉 Jira 的概念依然有价值。
