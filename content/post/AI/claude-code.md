---
title: Claude Code 使用笔记
author: "-"
date: 2026-04-20T12:54:03+08:00
lastmod: 2026-07-30T13:14:28+08:00
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

## Loop Engineering：让 Agent 自我修正到完成条件为止

Loop Engineering 是 2026 年上半年在 AI agent 圈子里流行起来的说法：与其每一步都手动给 agent 写 prompt（prompt engineering），不如设计一个自动循环系统——定好目标、检查方式和停止条件，让 agent 自己「感知 → 行动 → 观察 → 再决策」，反复迭代直到任务完成。这个模式可以追溯到 ReAct（Reason + Act）范式：模型思考、采取行动、观察结果、再思考、再行动，这个「推理-行动-观察-重复」的循环就是 loop engineering 的核心，和 prompt engineering（人类每一步手写指令、评估结果、写下一步指令）的区别在于：loop engineering 构建的是能自我提示、自我评估直到达成目标的系统，适合长时间运行的自主任务。

一个绕不开的背景术语是 **Ralph 技术**：由 Geoffrey Huntley 在 2025 年提出，本质是一个不断把同一个 prompt 喂给 agent、直到任务完成的 bash 循环，现在是 Claude Code 社区里最经典的「外部驱动式」loop engineering 实现，具体写法见下文「Headless 模式」里的「Ralph 循环」小节。

Claude Code 里支持这个模式的机制有好几种，容易混淆，核心区别是**谁来判断"完成了"**、**下一轮由谁触发**、**跑在哪**。

### /goal —— 设定完成条件，自动循环直到达标

`/goal` 让你设一个可验证的完成条件，每轮结束后由**一个独立的小模型**（默认 Haiku）检查条件是否满足，不满足就自动开始下一轮，不需要手动催促「继续」。

```text
/goal 所有 test/auth 下的测试通过，且 lint 检查干净
```

写条件时注意几点：

- 给一个可衡量的终态：测试结果、构建退出码、文件数量等，而不是「做得不错」这类模糊描述
- 写明验证方式：比如「`npm test` 退出码为 0」
- 写清不能变的约束：比如「不要动其他测试文件」
- 可以加轮次/时间上限：比如「或最多跑 20 轮后停止」

非交互模式下也能用，配合 headless 一起跑：

```bash
claude -p "/goal CHANGELOG.md 里包含本周每个合并 PR 的条目"
```

适合迁移大量调用点直到全部编译通过、按设计文档实现直到验收标准全部满足、拆分大文件直到每个模块都在体积预算内、清空一个 issue backlog 这类需要多轮迭代、又不想每轮手动确认「继续」的场景。

### /loop 与 /schedule：定时/循环任务

Claude Code 里还有两种让任务重复执行的机制，容易混淆，核心区别是**跑在哪**。

#### /loop —— 挂在当前会话上的循环

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
| 完全不给 prompt | 跑内置的「维护型」prompt：处理未完成工作、PR 评论、CI 失败等；可以用项目里的 `.claude/loop.md` 自定义这个默认内容 |

**关键限制：`/loop` 本质是"到点唤醒当前这个会话继续跑"**，不是独立后台进程。关掉终端/结束会话，循环就停了。固定间隔任务默认 7 天后自动过期；会话内最多同时保留 50 个已调度任务。

#### /schedule —— 云端定时任务

`/schedule` 把任务调度到 Anthropic 云端执行（即 Routines），不依赖本地会话是否开着，电脑关机也照常触发。但代价是**访问不到本地专属资源**：

- 本地未提交的改动、未 push 的分支
- localhost 服务、本地数据库、本地起的开发服务器
- 只存在于本机的文件（没进 git 的配置、密钥等）
- 本地环境变量、本地安装的 CLI 工具（除非云端环境也配置了）

云端只能看到 git 远程仓库（如 GitHub）上已 push 的内容。类似定位的还有 GitHub Actions 的 schedule trigger（适合 CI 层面的自动化）、桌面端 scheduled tasks（本机定时任务，可访问本地文件，但机器要开着）。

### Stop Hook —— 自定义、确定性的评估逻辑

如果 `/goal` 用模型评估完成条件不够精确，可以自己写 Stop hook（脚本或 prompt 形式），在每轮结束后跑确定性检查——比如直接执行测试命令拿 exit code，而不是让模型「判断」测试是否通过。`/goal` 本质上就是一个 session 范围内、预置好的 prompt-based Stop hook 封装；需要更精确的判据时，自己写 Stop hook 是更底层的选择。

### /goal vs. 不用 /goal 直接说任务

核心区别在于：**谁来判断"完成了"、完成之后谁来触发下一步**。

| | 不用 `/goal` | 用 `/goal` |
| ---- | ---- | ---- |
| "完成"标准 | Claude 自己临场判断 | 预先写死的可验证条件 |
| 判断者 | 做事的同一个模型（自己既当运动员又当裁判） | 独立的评估模型（默认 Haiku），跟做事的不是同一次推理 |
| 下一轮是否自动开始 | 否，做完一轮通常会停下汇报，等你说「继续」 | 是，条件不满足就自动继续，不需要你介入 |
| 何时把控制权还给你 | 它觉得完成/不确定时 | 只有裁判确认条件真正满足时 |

类比：不用 `/goal` 相当于让一个人做完一件事**自己觉得差不多了就下班**；用 `/goal` 相当于给了他一张验收清单，旁边站着一个质检员，没在清单上打勾之前不允许下班——即使他自己觉得「应该可以了」。简单一两轮能搞定的任务，两者区别不大；差别主要体现在需要多轮迭代、且不想每轮都手动确认「继续」的场景。

### 怎么选

| 需求 | 选择 |
| ---- | ---- |
| session 内，跑到某个可验证条件达成为止 | `/goal` |
| session 内，按固定/动态间隔反复检查（任务要碰本地资源） | `/loop`，或直接在当前会话里手动迭代 |
| 纯粹定期检查 GitHub 上的 PR / issue / CI 状态，不依赖本地环境，长期跑、不想一直开着电脑 | `/schedule`（Routines）/ GitHub Actions |
| 完全自动化、脱离交互、多轮迭代直到 PRD 任务全部完成 | headless 模式 + 外部 bash 循环（Ralph，见下文） |
| 需要确定性（非模型判断）的完成检查 | Stop hook |

## Headless 模式（非交互式）

给任意 `claude` 命令加上 `-p`（或 `--print`）参数，就能把它变成非交互模式：跑一次 agent loop，打印结果，然后退出，不进入交互式 UI。适合脚本、CI/CD、构建流程里调用。

```bash
claude -p "What does the auth module do?"
```

### --bare：跳过本地配置，加快启动

默认情况下 `claude -p` 会加载和交互式会话一样多的上下文：项目里的 hooks、skills、plugins、MCP servers、auto memory、`CLAUDE.md` 全部自动发现并加载。加上 `--bare` 可以跳过这些自动发现，只用显式传入的参数，启动更快，而且在不同机器上结果一致（不会因为某个人 `~/.claude` 里配的 hook 而跑出不同结果）。CI 和脚本场景推荐总是加 `--bare`。

```bash
claude --bare -p "Summarize this file" --allowedTools "Read"
```

bare 模式下默认只有 Bash、文件读、文件写权限，也跳过 OAuth/keychain 认证，需要用 `ANTHROPIC_API_KEY` 或 `--settings` 里的 `apiKeyHelper`。想额外加载系统提示、settings、MCP、自定义 agent、plugin，用对应的 `--append-system-prompt`、`--settings`、`--mcp-config`、`--agents`、`--plugin-dir` 参数显式传入。

### 管道输入输出

非交互模式会读 stdin，可以像普通命令行工具一样管道进出：

```bash
cat build-error.txt | claude -p '简要说明这个构建错误的根因' > output.txt
```

用在 `package.json` 脚本里做项目专属 lint/review 也很自然：

```json
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

### 结构化输出：--output-format

| 值 | 说明 |
| ---- | ---- |
| `text`（默认） | 纯文本 |
| `json` | 结构化 JSON，含 `result`、`session_id`、`total_cost_usd` 等元数据 |
| `stream-json` | 按行输出的 JSON 事件流，配合 `--verbose --include-partial-messages` 可实现逐 token 流式输出 |

```bash
claude -p "Summarize this project" --output-format json | jq -r '.result'
```

想让输出严格符合某个 JSON Schema，加 `--json-schema`，结果会放在 `structured_output` 字段：

```bash
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

### 自动放行工具：--allowedTools / --permission-mode

交互模式下工具调用会弹窗确认，headless 模式没有人盯着，需要提前放行，否则遇到未授权的工具调用会直接中止：

```bash
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

也可以用 `--permission-mode` 设置整个会话的基线：`acceptEdits` 允许写文件和 `mkdir`/`mv`/`cp` 等常见文件操作；`dontAsk` 则拒绝一切不在 `permissions.allow` 规则里的操作，适合锁死权限的 CI 场景。

`--allowedTools` 支持前缀匹配，常用来只放行特定 git 子命令：

```bash
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

### 延续对话：--continue / --resume

```bash
claude -p "Review this codebase for performance issues"
claude -p "Now focus on the database queries" --continue

# 并行跑多个会话时，用 session id 精确恢复某一个
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

`--continue` 接续最近一次会话，`--resume <session_id>` 接续指定会话；session id 的查找范围是当前项目目录（含 git worktree），需要在同一目录下执行。

### Ralph 循环：用 bash 反复调用 headless 模式

Ralph 循环（见前文「Loop Engineering」一节）就是用 `claude -p` 在 bash 脚本里反复调用：**每次迭代都是全新 context**，靠外部文件（PRD + progress.txt 之类）当「持久记忆」：

```bash
#!/bin/bash
while true; do
  claude -p "读取 feature-requirements.md 和 progress.txt，
  挑一个未完成的任务实现它，跑测试，commit，更新 progress.txt。
  如果全部完成，输出 DONE 并退出。" \
    --allowedTools "Read,Write,Bash" \
    --permission-mode acceptEdits

  grep -q "DONE" progress.txt && break
done
```

几个关键设计原则：

- 每次迭代 context 干净，避免长会话里的「上下文腐化」
- 任务完成的判断标准必须是**可验证的**（测试通过，而不是 agent 自己说「做完了」）
- 必须有明确的退出条件，否则循环要么提前退出要么永不停止
- 权限要限定在沙箱内（Docker/devcontainer/独立 git worktree），避免在主机上裸跑 `--dangerously-skip-permissions`

### 典型用途

- CI/CD 流水线：跑测试、修 lint、生成 PR review
- 构建脚本里当项目专属 linter/reviewer 用
- 批量/并行跑多个独立任务，用 JSON 输出做后续解析

## Subagents 子代理

Subagent 是预先配置好的专用 AI 助手：有自己独立的**上下文窗口**、独立的 **system prompt**、可单独限定的**工具权限**，甚至可以指定不同的模型。主会话在合适的场景把任务委派给它，处理完只把结果带回主会话，中间过程不会塞进主对话的上下文。

### 存放位置与定义格式

Subagent 是一个带 YAML frontmatter 的 Markdown 文件：

```markdown
---
name: code-reviewer
description: Use this agent to review code changes for bugs, security issues, and style violations before committing.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer. Focus on correctness, security, and
maintainability. Be specific: cite file paths and line numbers.
```

| 字段 | 是否必填 | 说明 |
| ---- | ---- | ---- |
| `name` | 必填 | 子代理标识，kebab-case |
| `description` | 必填 | 决定 Claude 何时自动委派给它，写清楚适用场景 |
| `tools` | 可选 | 限定可用工具；不写则继承主会话全部工具 |
| `model` | 可选 | 覆盖默认模型（如指定 `haiku` 跑量大的简单任务省成本）；不写则继承主会话模型 |

frontmatter 之后的正文就是这个子代理的 system prompt。

存放路径两级，同名时**项目级覆盖用户级**：

| 位置 | 作用范围 |
| ---- | ---- |
| `.claude/agents/*.md` | 仅当前项目，可随代码一起提交进 git，团队共享 |
| `~/.claude/agents/*.md` | 当前用户的所有项目 |

### 作用范围：项目级 / 用户级 / 内置通用

自定义 subagent 不是全局共享的，而是跟你选择的存放位置绑定：

- **项目级**（`.claude/agents/*.md`）：只在这个项目里可见，换到别的项目就用不了；优点是能随项目一起提交进 git，团队成员共用同一套子代理
- **用户级**（`~/.claude/agents/*.md`）：跟具体项目无关，本机所有项目都能用，相当于个人工具箱；同名时项目级会覆盖用户级

除此之外还有一类**内置通用 subagent**，不需要自己定义、开箱即用、不受项目限制，比如 `Explore`（只读代码搜索）、`general-purpose`（通用多步任务）、`Plan`（架构规划）。

所以准确的说法是：自定义 subagent 默认跟特定范围（项目或用户）绑定，但这个范围可以自己选；同时系统还自带一批不受此限制的通用 subagent。

### 创建与管理：/agents

交互式管理入口是 `/agents`，可以新建、编辑、删除子代理，也能直接浏览内置的几种通用类型（如 `Explore`——只读代码搜索、`general-purpose`——通用多步任务、`Plan`——架构规划）。不想手写 frontmatter 时，用 `/agents` 走一遍向导即可生成文件。

### 调用方式

- **自动委派**：Claude 读取所有可用子代理的 `description`，判断当前任务是否匹配，匹配就自动派发，无需用户手动指定
- **`@` 提及（推荐，强制生效）**：输入 `@` 会弹出子代理选择列表，或直接手打 `@agent-<name>`，例如 `@agent-code-reviewer 看一下这次改动`；plugin 里的子代理写作 `@agent-<plugin-name>:<agent-name>`。这种写法是**确定性调用**，不依赖 Claude 自己判断
- **自然语言点名（启发式，不保证生效）**：直接在对话里说「用 code-reviewer 子代理看一下这次改动」，Claude 通常会据此委派，但最终是否触发仍取决于它的判断，不如 `@` 提及可靠
- **整个会话固定用某个子代理**：启动时加 `claude --agent code-reviewer`，或在 `.claude/settings.json` 里配置 `"agent": "code-reviewer"`

`/agents` 只负责新建、编辑、浏览子代理，**不能**用它来触发某次具体的调用。

### 典型使用场景

- **代码审查（code-reviewer）**：改动提交前自动审查安全漏洞、代码风格、逻辑问题。`tools` 只给 `Read/Grep/Glob/Bash`，不给 `Edit`，防止它顺手改代码
- **测试与调试（test-runner / debugger）**：跑测试套件、分析失败原因、定位到具体代码行。这类任务过程会产生大量日志输出，丢进独立子代理的上下文里，不会把主对话塞满
- **开放式调研（research / explore）**：比如「这个仓库里所有用到 Redis 的地方」这种需要读很多文件、试很多次 grep 才能收敛的搜索，交给子代理，只把结论带回主会话
- **固定流程的内容生成**：把一套反复执行的规则（比如本博客 `AGENTS.md` 里「检查文件名、URL、标签、lastmod」的固定流程）封装成子代理的 system prompt，以后每次都能稳定复用，不用每次在主对话里重新讲一遍规则

一个最小示例，`.claude/agents/test-runner.md`：

```markdown
---
name: test-runner
description: Use proactively after code changes to run the test suite and report failures with file:line references.
tools: Bash, Read, Grep
---

You are a test automation specialist. Run the relevant test suite,
parse failures, and report each as `file:line — reason`. Do not
attempt to fix the code yourself, just report.
```

改完代码后，Claude 判断到有子代理的 `description` 匹配当前场景，就会自动委派给它去跑测试、汇总失败点，而不是主会话自己执行一堆测试命令、把大段日志堆进对话历史。

### 为什么要用子代理

- **上下文隔离**：子代理内部的搜索、读文件、试错过程不会污染主对话的上下文窗口，主会话只看到最终结果
- **权限最小化**：给子代理配置的 `tools` 可以比主会话更窄，比如一个只读的审查类子代理没必要拿到 `Edit`/`Bash` 权限
- **并行处理**：多个独立子任务可以同时派发给不同子代理并行跑，比串行一个个做更快
- **可复用、可共享**：项目级子代理进 git 后，团队所有人用同一套审查/测试/调试规范，不用每人各自维护一份 prompt

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-13 | 标题改为「Claude Code 使用笔记」；补 AGENTS.md 踩坑与 `/add-dir` 会话内加目录说明 | 原标题过简；补规则未加载问题，以及已启动会话如何加目录 |
| 2026-07-21 | 新增「/loop 与 /schedule」章节 | 原文档缺少定时/循环任务相关内容 |
| 2026-07-25 | 新增「Headless 模式（非交互式）」章节 | 原文档缺少 `-p`/`--print` 非交互模式、CI/CD 自动化相关内容 |
| 2026-07-30 | 新增「Subagents 子代理」章节 | 原文档缺少子代理定义格式、存放位置、`/agents` 管理、调用方式相关内容 |
