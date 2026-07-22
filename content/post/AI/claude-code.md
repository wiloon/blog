---
title: Claude Code 使用笔记
author: "-"
date: 2026-04-20T12:54:03+08:00
lastmod: 2026-07-21T15:00:30+08:00
url: claude-code
categories:
  - AI
tags:
  - claude-code
  - remix
  - AI-assisted
---
## 安装 Claude Code

```bash
# macOS 用 brew 安装（推荐）
brew install --cask claude-code

# 或安装最新版
brew install --cask claude-code@latest

# 用 npm 安装
npm install -g @anthropic-ai/claude-code
```

## 安装 cc-switch（多账号切换工具）

```bash
brew install --cask cc-switch
```

安装后从 Launchpad 或用以下命令启动：

```bash
open -a cc-switch
```

## 认证冲突处理

cc-switch 会设置 `ANTHROPIC_AUTH_TOKEN` 环境变量，若同时存在 `claude /login` 的 key，启动时会出现：

```text
⚠ Auth conflict: Both a token (ANTHROPIC_AUTH_TOKEN) and an API key (/login managed key) are set.
```

**想用 cc-switch 管理的账号：**

```bash
claude /logout
```

**想用 `/login` 的 key：**

```bash
unset ANTHROPIC_AUTH_TOKEN
# 或从 ~/.zshrc 中删除该变量
```

## claude command

```bash
claude whoami
claude chat --prompt "你当前是哪个模型？请给出模型名称。"

export ANTHROPIC_BASE_URL=http://127.0.0.1:4141 && \
export ANTHROPIC_AUTH_TOKEN=sk-ant-api03-bridging-locally-format-check-passed-xxxxxxxxxxxx && \
claude
```

## CLAUDE.md 与 AGENTS.md

不同 AI 编程工具各自识别不同的项目指令文件：

| 工具 | 识别的指令文件 |
|---|---|
| VS Code Copilot | `AGENTS.md`、`.github/copilot-instructions.md` |
| Claude Code CLI | `CLAUDE.md`（项目根目录或父目录） |
| OpenAI Codex CLI | `AGENTS.md` |

两者**不会**自动识别对方的约定文件：

- 项目只有 `AGENTS.md`：Claude Code 不会加载它
- 项目只有 `CLAUDE.md`：VS Code Copilot 不会加载它

### 同时使用两个工具的方案

**推荐：软链接**（以 `AGENTS.md` 为主文件）

```bash
ln -s AGENTS.md CLAUDE.md
```

优点：单一事实来源，改一处两个工具都生效，不依赖任何工具特定语法。

**不推荐：`@include`**

Claude Code 支持 `@path/to/file` 语法，但 VS Code Copilot 的 `AGENTS.md` 不支持 `@include`，只能单向引用，不是真正的双向共享。

### 踩坑记录：项目里只有 AGENTS.md，规则被静默忽略

本博客仓库最初根目录只有 `AGENTS.md`（写了文件名、URL、categories、`lastmod`、标签等一整套强制规则），没有 `CLAUDE.md`。结果是：Claude Code 在编辑文章时完全没有加载这些规则，`lastmod` 没更新、标签也没按规则加，而且**不会报错或提示**——因为 Claude Code 本身就不认识 `AGENTS.md` 这个文件名，不是规则被违反，而是规则从没被读到过。

排查方法：确认项目根目录下是否存在 `CLAUDE.md`（或 `CLAUDE.local.md`），如果只有 `AGENTS.md`，Claude Code 不会自动读取。

修复：在根目录新建 `CLAUDE.md`，内容只写一行：

```markdown
@AGENTS.md
```

这样每次会话都会通过 import 语法把 `AGENTS.md` 的内容加载进上下文，无需维护两份文件。

## 常见错误

### model_max_prompt_tokens_exceeded

```text
API Error: 400 {"error":{"code":"model_max_prompt_tokens_exceeded","message":"prompt token count of 133252 exceeds the limit of 128000"}}
```

**原因：** 当前对话的上下文（prompt）超过了模型的最大 token 限制。

Claude 原生 API 的上下文窗口为 **200k tokens**（claude-3-5-sonnet 等主流模型）。如果报错显示 128k 限制，通常是因为使用了**中转代理**（通过 `ANTHROPIC_BASE_URL` 设置的第三方或本地 API），代理服务自身限制了 prompt 大小为 128k。

Claude Code 有**自动压缩**机制：当上下文接近限制时会自动触发 `/compact`，把对话历史总结压缩。但以下情况仍会绕过自动压缩直接报错：

- **单次操作本身就超限**：比如一次性读取多个大文件，单个请求的 prompt 已经超过 128k，还没来得及压缩
- **CLAUDE.md 本身过大**：每次请求都会带上指令文件，如果文件很长会持续占用大量 token
- **自动压缩触发太晚**：压缩是在接近上限时触发，但如果下一步操作读取的内容很大，仍可能超出

**解决方法：**

- 手动执行 `/compact` 压缩当前对话历史
- 开启新对话（`/clear`），彻底清空上下文
- 减少一次性加载的文件数量，分批处理
- 精简 CLAUDE.md / AGENTS.md 的内容，删除冗余说明

## 用 --add-dir / /add-dir 实现类似 multi-root workspace

Claude Code 默认只能访问启动时所在的目录。额外授权其他目录后，效果类似 VS Code 的 multi-root workspace（同时打开多个项目目录）。有两种时机：

| 方式 | 时机 | 说明 |
| ---- | ---- | ---- |
| `claude --add-dir ...` | 启动前 | 可一次指定多个目录 |
| `/add-dir ...` | 会话已启动 | 每次加一个；不写路径则弹出交互选择 |

两者主要授予文件读写权限；附加目录里的大部分 `.claude/` 配置通常不会被自动发现。默认只对当前会话生效，下次启动需重新添加，或在 settings 里配置 `permissions.additionalDirectories` 做持久化。

### 启动时用 --add-dir

```bash
claude --add-dir ../other-project --add-dir ../shared-lib
```

可以叠加多个 `--add-dir`，每个都会被加入可访问目录白名单。

### 已启动会话里用 /add-dir

直接指定路径：

```text
/add-dir ~/workspace/w10n-config
```

不写路径时只输入 `/add-dir`，会弹出交互式目录选择。多个目录就多次执行，每次加一个。

若只是想额外访问某个目录、不想把会话工作目录迁过去，用 `/add-dir`；若要把当前会话迁到另一个目录，用 `/cd`（需较新版本）。

### zshrc 里定义 alias，一条命令进入多目录项目

在 `~/.zshrc` 里写一个函数（不能用普通 alias，因为需要拼接多个路径参数）：

```bash
# 进入主项目目录，并把关联目录加入 Claude Code 的可访问范围
ccx() {
  cd ~/workspace/blog && claude --add-dir ~/workspace/w10n-config --add-dir ~/workspace/other-project
}
```

`source ~/.zshrc` 之后，直接执行：

```bash
ccx
```

即可一条命令进入项目目录并启动带多目录访问权限的 Claude Code 会话。

## /loop 与 /schedule：定时/循环任务

Claude Code 里有两种让任务重复执行的机制，容易混淆，核心区别是**跑在哪**。

### /loop —— 挂在当前会话上的循环

```text
/loop 5m /babysit-prs          # 固定间隔：每 5 分钟跑一次
/loop check the deploy every 20m  # 固定间隔的另一种写法
/loop check the deploy         # 不写间隔：自适应节奏，AI 自己判断下次什么时候该看
```

三种模式：

| 写法 | 行为 |
| ---- | ---- |
| `/loop <间隔> <任务>` | 转成 cron 表达式，固定间隔重复执行 |
| `/loop <任务>`（不写间隔） | 先立即跑一次，之后自己判断下次唤醒时机（等事件或等一段时间），直到任务完成自动停止 |
| 间隔 ≥60 分钟，或「每天/每天早上」这种日频任务 | 会先询问要不要改用云端方案（见下） |

**关键限制：`/loop` 本质是"到点唤醒当前这个会话继续跑"**，不是独立后台进程。关掉终端/结束会话，循环就停了。固定间隔任务默认 7 天后自动过期。

### /schedule —— 云端定时任务

`/schedule` 把任务调度到 Anthropic 云端执行，不依赖本地会话是否开着，电脑关机也照常触发。但代价是**访问不到本地专属资源**：

- 本地未提交的改动、未 push 的分支
- localhost 服务、本地数据库、本地起的开发服务器
- 只存在于本机的文件（没进 git 的配置、密钥等）
- 本地环境变量、本地安装的 CLI 工具（除非云端环境也配置了）

云端只能看到 git 远程仓库（如 GitHub）上已 push 的内容。

### 怎么选

| 场景 | 选择 |
| ---- | ---- |
| 任务要碰本地资源（改代码、跑本地测试/构建、访问本地服务） | `/loop`，或直接在当前会话里手动迭代 |
| 纯粹定期检查 GitHub 上的 PR / issue / CI 状态，不依赖本地环境 | `/schedule`，可以放心关机 |
| 短时间、当前会话内的重复检查 | `/loop` |
| 长期、每天/每周固定跑，不想一直开着电脑 | `/schedule` |

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-13 | 标题改为「Claude Code 使用笔记」；补 AGENTS.md 踩坑与 `/add-dir` 会话内加目录说明 | 原标题过简；补规则未加载问题，以及已启动会话如何加目录 |
| 2026-07-21 | 新增「/loop 与 /schedule」章节 | 原文档缺少定时/循环任务相关内容 |
