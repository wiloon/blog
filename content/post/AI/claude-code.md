---
title: Claude Code 使用笔记
author: "-"
date: 2026-04-20T12:54:03+08:00
lastmod: 2026-11-25T15:32:16+08:00
ShowToc: true
TocOpen: true
UseHugoToc: true
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

以前用 cc-switch 切换多个账号，现在已不再使用，相关内容移到了 [cc-switch：Claude Code 多账号切换](./cc-switch.md)。

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
| --- | --- |
| VS Code Copilot | `AGENTS.md`、`.github/copilot-instructions.md` |
| Claude Code CLI | `CLAUDE.md`、`.claude/CLAUDE.md`、`CLAUDE.local.md`；v2.1.277 起也直接读 `AGENTS.md` |
| OpenAI Codex CLI | `AGENTS.md` |

官方文档：<https://code.claude.com/docs/en/memory>

### Claude Code 什么时候读 AGENTS.md

从 v2.1.277 起，Claude Code 可以**直接加载 `AGENTS.md`**，不再需要 `CLAUDE.md`、软链接或 import。但默认是**二选一**，不是合并：

| 仓库里有什么（工作目录及其上级目录） | 默认加载 |
| ---- | ---- |
| 只有 `AGENTS.md` | 所有 `AGENTS.md` 和 `.claude/AGENTS.md` |
| `AGENTS.md` + `CLAUDE.md`（或 `.claude/CLAUDE.md`、`CLAUDE.local.md`） | **只读 `CLAUDE.md`**，`AGENTS.md` 被忽略 |

几个细节：

- 会话启动时加载工作目录及所有上级目录里的 `AGENTS.md`；子目录里的 `AGENTS.md` 在 Claude 用 Read 工具打开那个目录下的文件时才加载（前提是该子目录没有自己的 `CLAUDE.md`）
- `AGENTS.md` 里同样支持 `@path` import，规则和 `CLAUDE.md` 一样（相对路径从当前文件算起，最多嵌套 4 层）
- `AGENTS.local.md`、`AGENTS.override.md` 和 `.agents/` 目录下的文件**不会**加载
- 坑：一个项目本来靠 `AGENTS.md` 工作，你又加了个 `CLAUDE.local.md` 放个人配置，`AGENTS.md` 就不读了
- 早期版本有些例外：v2.1.281 之前，部分会话（比如走 Amazon Bedrock、关闭遥测）只读 `CLAUDE.md`；v2.1.280 之前，`/memory`、`/context` 里看不到直接加载的 `AGENTS.md`

### 用 /config 调整加载策略

`/config` 里的 **Project instructions** 有四个取值：

| 值 | 行为 |
| ---- | ---- |
| `claude-md-or-agents-md`（默认） | 有 `CLAUDE.md` 就只读 `CLAUDE.md`，没有就读 `AGENTS.md` |
| `claude-md-and-agents-md` | 两个都读，每个目录先 `CLAUDE.md` 后 `AGENTS.md` |
| `claude-md` | 只读 `CLAUDE.md`（旧行为） |
| `managed-only` | 只读托管策略的指令文件 |

这个设置也可以写进 `~/.claude/settings.json`（`pluginConfigs` → `cc-plugin-agents-md@builtin` → `options.instructionFiles`），但只有用户级设置、`--settings` 文件或托管设置里的这一项会生效，写在项目级 settings 里会被忽略。

### 同时使用多个工具的方案

现在多数情况下**只放一个 `AGENTS.md` 就够了**，Claude Code、Copilot、Codex 都能读到。

需要给 Claude 加专属内容时，用 `CLAUDE.md` + import（以 `AGENTS.md` 为主文件）：

```markdown
@AGENTS.md

<!-- Claude Code-only additions go below -->
```

一旦有了 `CLAUDE.md`，默认就不再直接读 `AGENTS.md`，所以第一行的 `@AGENTS.md` 不能省。这种写法也不会导致 `AGENTS.md` 被读两遍。设成 `claude-md`，或者会话本身读不了 `AGENTS.md` 时，也用这个写法。

**软链接**（`ln -s AGENTS.md CLAUDE.md`）也能用，但 Claude Code 的 Edit/Write 工具拒绝透过软链接写文件，让 Claude 改规则时会碰壁；Windows 上更推荐 import。

旧版本只放 `AGENTS.md`、规则被静默忽略的经历，见文末「踩坑记录」。

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

官方文档：<https://code.claude.com/docs/en/goal>

#### 用法

| 命令 | 作用 |
| ---- | ---- |
| `/goal <条件>` | 设定目标，并**立刻**以这个条件为指令开始一轮；已有目标时直接替换（一个 session 同时只有一个目标） |
| `/goal` | 不带参数：查看当前目标的状态，没有活跃目标时显示最近一次达成的目标 |
| `/goal clear` | 提前取消目标；`stop`、`off`、`reset`、`none`、`cancel` 都是同义词，成功会提示 `Goal cleared: …` |
| `/clear` | 开新对话，目标也一并清掉 |

条件最长 4000 字符。**没有内置的轮次/时间上限参数**，想限制就直接写进条件里，比如「……或跑满 20 轮后停止」，Claude 每轮会汇报进度，评估器根据对话内容判断是否到限。

#### 运行状态

- 目标生效时界面上有 `◎ /goal active` 指示器，显示已运行时长
- `/goal` 状态里能看到：条件、运行时长、已评估轮数、当前 token 花费、评估器最近一次给出的理由
- 每次评估的结论会出现在 transcript（会话记录，见下文「Transcript：会话记录」）里，按 `Ctrl+O` 打开 transcript 视图可以看到理由

#### 评估是怎么做的

`/goal` 本质上是一个 **session 范围、基于 prompt 的 Stop hook**。每轮结束后，Claude Code 把「条件 + 到目前为止的对话」发给评估模型，得到三种结论之一：

| 结论 | 后果 |
| ---- | ---- |
| 未满足（not yet met） | 继续下一轮，评估器给的理由会作为下一轮的指引 |
| 已满足（met） | 目标清除，记一条「达成」记录 |
| 不可能达成（impossible） | 目标清除，记一条「失败」记录并附理由 |

关键限制：**评估器不调用工具、不跑命令、不读文件**，它只能看 Claude 已经在对话里展示出来的东西。所以条件里要写「怎么验证」，逼 Claude 每轮把证据摆出来——比如让它跑 `npm test`，测试输出出现在 transcript 里，评估器才有依据。写成「代码质量好」这种条件，评估器没法判断，只会无限循环或乱判。

另一个保护：如果 Claude 连续好几轮只回话、不调用任何工具（原地空转），Claude Code 会停掉循环、打印警告、把控制权还给你，但目标仍保留，你下一次发消息后继续评估。

#### 写好条件

一个好的条件通常包含：

- **一个可衡量的终态**：测试结果、退出码、文件数量、队列清空，而不是「做得不错」这类模糊描述
- **明确的检查方式**：比如「`npm test` 退出码为 0」「`git status` 干净」
- **不能变的约束**：比如「不修改其他测试文件」
- **兜底上限**（可选）：比如「或跑满 20 轮后停止」

几个例子：

```text
/goal src/legacy/ 下所有调用点都迁移到新 API，go build ./... 和 go test ./... 都通过，不修改 *_test.go 的断言
/goal docs/design.md 里的每条验收标准都有对应测试且通过；每轮结束列出剩余未满足的标准
/goal 拆分 big.ts，直到每个模块都小于 300 行，pnpm typecheck 退出码为 0
/goal 处理完所有带 ready-for-agent 标签的 issue，gh issue list --label ready-for-agent 返回空；或跑满 30 轮停止
```

适合迁移大量调用点直到全部编译通过、按设计文档实现直到验收标准全部满足、拆分大文件直到每个模块都在体积预算内、清空一个 issue backlog 这类需要多轮迭代、又不想每轮手动确认「继续」的场景。一两轮能搞定的事不需要它。

#### 和权限模式配合：无人值守要开 auto mode

`/goal` **不改变权限模式**。手动模式下，Claude 遇到 settings 没放行的工具调用照样停下来问你，循环就卡在那。真想放手跑，要在 auto mode 下用 `/goal`（auto mode 的细节见下文「auto mode 详解」）：

- auto mode 去掉的是「每次工具调用」的确认
- `/goal` 去掉的是「每一轮」的确认（auto mode 本身不会主动开始新一轮）

两者叠加才是真正的无人值守。

#### 非交互模式（headless）

```bash
claude -p "/goal CHANGELOG.md 里包含本周每个合并 PR 的条目"
```

一次调用就会跑到目标完成为止。默认文本输出只打印最终回复，想看过程用 `--output-format stream-json --verbose`；`Ctrl+C` 中止。桌面端和 Remote Control 里也能用。

#### 出错、后台任务与 check-in

- **必须人工处理的错误会清掉目标**：认证失败、额度用完、磁盘满、上下文溢出且自动压缩也救不回来、模型不可用等，提示以 `Goal cleared after an unrecoverable error` 开头，修好后重新 `/goal`
- **其他错误目标保留**（v2.1.269+）：可重试的错误会显示 `Goal still active` 并自动重试，重试三次后暂停；遇到限流、用量上限或某个 hook 结束了本轮，会显示 `Goal paused` 并写明原因，等用量上限重置后会自动接着干。随时发一条消息就能立即开始下一轮
- **后台任务**：一轮结束时如果还有 subagent 或后台 shell 在跑，这一轮跳过评估，等到某一轮结束时没有后台任务了再评估
- **check-in**：后台任务把目标挂住 30 分钟后，Claude 会做一次 check-in——列出在跑的任务、读输出，判断是继续等还是修掉/停掉卡住的任务；之后间隔退避（30 分钟 → 1 小时 → 之后每 2 小时）。交互模式下空闲时也会主动 check-in，但两次用户输入之间最多 3 次。`-p` 模式只在轮次结束时 check-in
- 环境变量 `CLAUDE_CODE_GOAL_CHECKIN_MINUTES` 调整首次 check-in 间隔（默认 30，后续间隔按比例缩放），设为 `0` 同时关闭 check-in 和自动重试
- `claude --resume` 从 v2.1.239 起会恢复会话里的目标

#### 评估模型、费用与限制

- 评估器用的是「配置的小而快的模型」，跟主会话走同一个 provider。想换就设 `ANTHROPIC_DEFAULT_HAIKU_MODEL`——注意这会同时改掉 `haiku` 别名和其他后台任务（比如生成会话标题）用的模型
- 评估消耗的 token **单独计费**，叠加在主轮次花费之上；长时间跑之前看一眼 `/goal` 状态里的 token 花费
- `/goal` 跟 settings 里的 hooks 遵循同样的 workspace trust 规则；如果最终生效的设置里 `disableAllHooks: true`，或托管设置开了 `allowManagedHooksOnly`，`/goal` 不可用

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

也可以用 `--permission-mode` 设置整个会话的基线：`acceptEdits` 允许写文件和 `mkdir`/`mv`/`cp` 等常见文件操作；`dontAsk` 则拒绝一切不在 `permissions.allow` 规则里的操作，适合锁死权限的 CI 场景。各个模式的区别见下文「权限模式（--permission-mode）」。

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

### 无人值守机器上的登录：claude setup-token

`claude auth login`（会话里的 `/login`）是交互式浏览器登录，凭证存在本机：macOS 存 Keychain，Linux 存 `~/.claude/.credentials.json`（权限 0600）。这种登录有到期日，用 Claude Code 不会延长它，到期后要再跑一次 `/login`。在服务器上跑 `claude -p` 时，到期前会看到这样的提示：

```text
Warning: this sign-in can end at any time from now until 2026-11-25. Renewing it does not move that date. Run claude auth login now, or use claude setup-token for unattended jobs.
```

`claude setup-token` 是官方给 CI、脚本、无人值守服务器准备的方式：

- 走和 `/login` 一样的浏览器授权，批准后在终端打印一个**有效期一年**的 OAuth token
- 它**不保存**这个 token，要自己复制下来，放进 `CLAUDE_CODE_OAUTH_TOKEN` 环境变量
- 需要 Pro、Max、Ultra、Team 或 Enterprise 订阅，用量算在订阅里，不走 API 计费
- 只能发模型请求：不能建立 Remote Control 会话，也拿不到 claude.ai 上配置的 connectors；本地配置的 MCP server 照常可用

```bash
# Run once on a machine with a browser; the token is printed, not saved
claude setup-token

# On the headless machine (keep the value in a secret store, not in shell history)
export CLAUDE_CODE_OAUTH_TOKEN="$(rbw get claude/setup-token)"
claude -p "Reply with OK"

# Check which login is in use and when it ends (v2.1.318+)
claude auth status --text
```

几个要注意的地方：

- **优先级**：`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_API_KEY`、`apiKeyHelper` 都排在 `CLAUDE_CODE_OAUTH_TOKEN` 前面；`-p` 模式下只要设了 `ANTHROPIC_API_KEY` 就一定用它，改走 API 计费。用 setup-token 时确认这几个变量没设。`/login` 存下的订阅登录排在最后。
- **`--bare` 不读这个变量**：`--bare` 模式不读 OAuth 凭证和 Keychain，只能用 `ANTHROPIC_API_KEY` 或 `apiKeyHelper`。官方说 `--bare` 以后会变成 `-p` 的默认行为，到时候脚本要显式处理。
- **token 绑定个人订阅**：它属于运行 `setup-token` 的那个人的订阅。多人共享、组织级的 CI secret，官方建议用 API key 或 workload identity federation。
- **撤销**：文档没写怎么撤销或列出 setup-token；GitHub Actions 文档还提到删掉 secret 不会让里面的凭证失效。当密码一样保管，不要提交进 git。
- **GitHub Actions**：存成仓库 secret `CLAUDE_CODE_OAUTH_TOKEN`，在 `anthropics/claude-code-action@v1` 里写 `claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}`；`/install-github-app` 可以替你创建这个 secret。

参考：[Authentication](https://code.claude.com/docs/en/authentication)、[GitHub Actions](https://code.claude.com/docs/en/github-actions)、[Headless](https://code.claude.com/docs/en/headless)

## 权限模式（--permission-mode）

Claude Code 每次调用工具（跑命令、改文件、联网）前都要过一道权限检查。权限模式决定「没有规则明确说可以或不可以」的那些调用怎么处理。启动时用 `--permission-mode <mode>` 指定，交互会话里也可以按 Shift+Tab 切换。以 2.1.301 版本的 `claude --help` 为准，可选值有：

| 模式 | 没有匹配规则时 | 适合 |
| ---- | ---- | ---- |
| `manual` | 弹窗问人（即通常说的默认模式） | 日常交互 |
| `acceptEdits` | 自动允许改文件和 `mkdir`/`mv`/`cp` 等文件操作，其余照常问 | 信任它改代码，但命令还想过目 |
| `plan` | 只读，只能调研和出方案，不能改 | 先讨论方案再动手 |
| `auto` | 由一个安全分类器判断风险，低风险直接放行，高风险拒绝（详见下文「auto mode 详解」） | 有人在旁边、但不想频繁点确认 |
| `dontAsk` | **直接拒绝**，不弹窗 | 无人值守：只有 `permissions.allow` 里列出的操作能执行 |
| `bypassPermissions` | 全部放行（等同 `--dangerously-skip-permissions`） | 只在一次性沙箱/容器里用 |

几个要点：

- 规则的优先级是 **deny > ask > allow**。`deny` 里写了的，哪怕 `allow` 里也有，照样拒绝。
- `dontAsk` 和无人值守最搭：遇到白名单以外的操作，Claude 只是收到「被拒绝」，会换别的办法或停下汇报，**不会卡住等人点允许**。
- headless 模式（`-p`）下还有一个 `--permission-prompts none`：任何本来要弹窗的地方都直接拒绝。和 `dontAsk` 一起用是双保险。
- 规则写在 settings 的 `permissions` 里，Bash 规则按命令前缀匹配，复合命令（`a && b`）会拆开逐段检查：

```json
{
  "permissions": {
    "allow": ["Read", "Edit", "Bash(git *)", "Bash(go test *)", "Bash(pnpm *)"],
    "deny":  ["Bash(git tag *)", "Bash(gh release *)", "Bash(kubectl *)"]
  }
}
```

### auto mode 详解

auto mode 的思路是：**不再逐个问你，而是让另一个模型（安全分类器）在每个动作执行前审一遍**。它会拦下超出你请求范围的操作、针对陌生基础设施的操作，以及看起来是被 Claude 读到的恶意内容（prompt injection）驱动的操作。官方原话也提醒了：auto mode 减少了确认弹窗，但**不保证安全**。

官方文档：<https://code.claude.com/docs/en/permission-modes>、<https://code.claude.com/docs/en/auto-mode>

#### 一个动作是怎么被判定的

1. 先看 `permissions` 里的 allow / ask / deny 规则。deny 直接拒绝，ask 照样弹窗（即使在 auto mode 下）
2. 只读操作、工作目录里的文件编辑直接放行
3. 其余的交给分类器判断
4. 被拦下时，Claude 会收到拒绝原因（通常是一个策略名，比如 `[Destructive or Unwanted Actions]`），然后可以换别的办法

分类器看到的是：你的消息、Claude 的工具调用（文件读取、搜索这类只读查询除外）、`CLAUDE.md` 的内容。**工具返回的结果会被剥掉**，这样网页、文件里的恶意内容就没法直接「说服」分类器。它只信任工作目录和会话启动时已配置的 git remote。

#### 默认拦什么、放什么

| 默认拦下 | 默认放行 |
| ---- | ---- |
| 下载并执行代码，比如 `curl \| bash` | 工作目录里的本地文件操作 |
| 把敏感数据发往外部、把密钥推出仓库 | 安装项目里已声明的依赖 |
| 生产部署、数据库迁移 | 只读的 HTTP 请求 |
| force push、`git reset --hard`、`git clean -fd` 等丢弃改动的操作 | push 到当前仓库的分支（包括默认分支，但 `production`、`gh-pages` 这类像部署目标的分支除外） |
| `terraform destroy` 之类的销毁操作、删除已有文件 | |
| 合并未经批准的 PR、关掉 CI 检查 | |

#### 开启方式

- **交互模式**：新版本（v2.1.283 起）交互式终端和 VS Code 会话默认就从 auto mode 开始。按 Shift+Tab 切换：在 `auto` 下按一次切到 `default`，之后按 `default` → `acceptEdits` → `plan` 循环
- **命令行**：`claude --permission-mode auto`
- **设置默认值**：`permissions.defaultMode: "auto"` 只能写在 `~/.claude/settings.json`；写在项目的 `.claude/settings.json` 或 `settings.local.json` 里**不生效**（防止仓库替你打开 auto mode）
- **headless**：`claude -p` 默认是手动模式，要显式加 `--permission-mode auto`
- 需要较新的模型，旧模型不支持；Team / Enterprise 管理员可以在托管设置里用 `permissions.disableAutoMode` 关掉

#### 被拦下之后

- 界面会弹通知，`/permissions` 的 **Recently blocked** 里能看到。按 `r` 批准后 Claude 可以重试，但这**不会**新增一条权限规则，重试时还会重新过一次检查
- **连续被拦 3 次，或一个会话累计被拦 20 次**，auto mode 暂停，回到逐个弹窗确认；你批准一次后恢复。这两个阈值不能改
- headless 模式下没有弹窗可以退回：被拦的动作就不执行，Claude 继续干别的，不会中止整个运行
- 分类器模型不可用时，所有需要检查的动作都会被拒绝

#### 自定义

- 用 `permissions.allow` / `ask` / `deny` 规则做硬性约束，deny 在分类器之前生效
- 用 settings 里的 `autoMode` 块，以**自然语言**告诉分类器你的环境：`environment`（比如「`*.internal.example.com` 是我们自己的服务」）、`allow`、`soft_deny`、`hard_deny`。每个列表里要带上 `"$defaults"`，否则会覆盖掉内置规则。`autoMode` 同样只从用户级设置、托管设置或 `--settings` 读取，项目级设置里写了也不生效
- 工具：`claude auto-mode defaults` 看内置规则，`/auto-mode-setup` 帮你起草配置，`/permissions` 里有 **Auto mode** 标签页

#### 费用

走 API、Bedrock、Vertex、Foundry 或 Enterprise 计划时，分类器调用的 token 计入你的用量；每次检查也会多一次往返延迟。

#### auto mode 和其他模式怎么选

- 有人在旁边、想少点确认：`auto`
- 无人值守、白名单之外一律拒绝：`dontAsk` + `permissions.allow`，行为完全可预测
- 想让 `/goal` 自己跑完：`auto` + `/goal`（auto mode 去掉每次工具调用的确认，`/goal` 去掉每一轮的确认）
- `bypassPermissions` 只在隔离的容器、虚拟机里用

## Transcript：会话记录

transcript 指的是**一次会话的完整记录**：你的消息、Claude 的回复、每次工具调用及其结果。它有两种形态。

### 界面里的 transcript 视图（Ctrl+O）

平时的聊天界面会把工具调用折叠成一行摘要，按 `Ctrl+O` 打开 transcript 视图，能看到每次工具调用的详细输入输出，每条回复还带时间戳和所用模型。`/goal` 每轮评估的结论和理由，也是在这里展开看的。

视图里常用的键：

| 键 | 作用 |
| ---- | ---- |
| `q` / `Esc` / `Ctrl+C` | 退出 transcript 视图 |
| `{` / `}` | 跳到上一条/下一条用户消息（全屏渲染时） |
| `[` | 把整段对话写到终端原生 scrollback，之后可以用 `Cmd+F` 搜索（全屏渲染时） |
| `v` | 把对话写到临时文件，用 `$VISUAL` / `$EDITOR` 打开（全屏渲染时） |
| `Ctrl+E` | 显示全部内容（经典渲染时） |
| `?` | 快捷键帮助（全屏渲染时） |

### 磁盘上的 transcript 文件

所有经过工具的内容都会写进磁盘上的 transcript：

```text
~/.claude/projects/<project>/<session-id>.jsonl           # main session: messages, tool calls, tool results
~/.claude/projects/<project>/<session-id>/subagents/      # subagent transcripts
~/.claude/projects/<project>/<session-id>/tool-results/   # oversized tool outputs
```

- 格式是 JSONL，一行一条记录。`--resume`、`--continue` 和回退（rewind）都依赖这些文件，删掉 `~/.claude/projects/` 就没法恢复以前的会话了
- **明文存储、不加密**，命令输出里出现过的密钥也会留在里面
- 默认保留 30 天，用 settings 里的 `cleanupPeriodDays` 调整（最小 1，设 0 会报错）
- 不想落盘：headless 模式加 `--no-session-persistence`，或者设环境变量 `CLAUDE_CODE_SKIP_PROMPT_HISTORY`
- hook 的输入里有 `transcript_path` 字段指向这个文件。但它是异步写入的，hook 触发时可能还没写进本轮最新的消息；Stop hook 想拿 Claude 的最后一条回复，用输入里的 `last_assistant_message` 更可靠

## Hooks：在工具调用前后插入自己的脚本

Hook 是 Claude Code 在特定事件发生时**由 harness 执行**的命令（不是让模型「记住」规则，而是确定性地每次都跑）。常用事件：

| 事件 | 时机 | 典型用途 |
| ---- | ---- | ---- |
| `PreToolUse` | 工具调用执行**之前** | 拦截危险命令、限制可写目录 |
| `PostToolUse` | 工具调用成功之后 | 改完文件自动跑 formatter/lint |
| `UserPromptSubmit` | 用户提交 prompt 时 | 注入上下文、过滤输入 |
| `Stop` | Claude 准备结束这一轮时 | 跑测试，不通过就让它继续（见上文 Stop Hook） |
| `SessionStart` / `SessionEnd` | 会话开始/结束 | 加载环境、清理 |
| `Notification` | 需要人关注时 | 转发到手机通知 |

### PreToolUse 怎么工作

1. Claude 决定调用某个工具，比如 `Bash` 执行 `git tag v1.0.0`
2. harness 把这次调用以 JSON 形式从 stdin 传给 hook 脚本，主要字段有 `tool_name`、`tool_input`（Bash 是 `command`，Edit/Write 是 `file_path`）、`cwd`、`session_id`
3. 脚本自己判断，然后：
   - 什么都不输出、exit 0：不表态，交给正常的权限规则
   - 输出 `permissionDecision: "deny"`：拒绝，`permissionDecisionReason` 会作为错误信息返回给 Claude
   - 输出 `"allow"` / `"ask"`：直接放行 / 强制弹窗问人
   - 或者 exit 2：拒绝，stderr 内容反馈给 Claude

配置写在 settings 里，`matcher` 是匹配工具名的正则：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [{ "type": "command", "command": "$HOME/bin/guard.sh" }]
      }
    ]
  }
}
```

一个最小的 guard 脚本：

```bash
#!/bin/zsh
# Deny git tags; stay silent (no opinion) for everything else.
input=$(cat)
[[ $(jq -r '.tool_name' <<<"$input") == Bash ]] || exit 0
cmd=$(jq -r '.tool_input.command' <<<"$input")
if print -r -- "$cmd" | grep -qE '(^|[;&|])[[:space:]]*git[[:space:]]+tag\b'; then
  jq -n '{hookSpecificOutput: {hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason: "no git tags: v* deploys production"}}'
fi
exit 0
```

实测在 `claude -p` 里，Claude 收到的是 `PreToolUse:Bash hook error: <你的 reason>`，它会说明被拒并停止重试。

### permissions 规则和 PreToolUse 的分工

- **permissions 规则**：声明式、按前缀匹配，适合「哪些命令能用」的白名单/黑名单。
- **PreToolUse hook**：可以写任意逻辑，适合规则表达不了的情况，比如「`git push` 可以，但不能推 tag、不能推 main、不能 force」，「只能写某个 worktree 里的文件」，「只在某个环境变量存在时才生效」。
- 两者都只看命令字符串，不是沙箱。`pnpm test` 跑的脚本、`node -e` 里的代码它们都看不到。真正的底线要放在系统外面：GitHub 分支保护、独立账号、容器或单独的机器。

## 没有 profile，用 settings 分层代替

Claude Code 没有「切换 profile」这样的命名概念，但 settings 本身是分层合并的，加上几个启动参数，就能做出「有人在时宽松、无人值守时收紧」的两套配置。

settings 的来源和优先级（高的覆盖低的，permissions 规则则合并起来一起生效）：

1. 企业托管策略（managed settings，个人一般没有）
2. 命令行参数，包括 `--settings <file>`
3. 项目本地 `.claude/settings.local.json`（不进 git，个人在这个项目里点过的「总是允许」都在这）
4. 项目共享 `.claude/settings.json`（进 git）
5. 用户级 `~/.claude/settings.json`

做法是：**交互用默认配置，无人值守的 agent 用一条固定的启动命令**：

```bash
# Unattended "profile": only user settings + an agent-specific file, nothing else.
ENX_AGENT=1 claude -p "$prompt" \
  --setting-sources user \
  --settings ~/.local/share/enx-agent/settings.json \
  --permission-mode dontAsk \
  --permission-prompts none
```

- `--setting-sources user` 只加载用户级配置，不读项目的 `settings.json` / `settings.local.json`。这一点很重要：你在交互时点过的「总是允许 `kubectl *`」都存在 `settings.local.json` 里，不排除掉的话无人值守的 agent 会继承这些权限。
- `--settings` 传入 agent 专用的白名单和 hook。
- hook 脚本里检查 `ENX_AGENT` 这类环境变量，可以让同一个脚本只在 agent 模式下生效。
- 把这条命令写成 shell 脚本或 alias，就相当于一个「agent profile」；交互时照常敲 `claude`，什么限制都不带。

无人值守 agent 的完整搭建过程见 [让 Claude Code 自主处理 GitHub Issue](./afk-agent-github-issues.md)。

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

## 踩坑记录

### 项目里只有 AGENTS.md，规则被静默忽略（v2.1.277 之前）

> 这是旧版本的问题，v2.1.277 起只有 `AGENTS.md` 的项目也能正常加载规则，下面保留作为历史记录。

本博客仓库最初根目录只有 `AGENTS.md`（写了文件名、URL、categories、`lastmod`、标签等一整套强制规则），没有 `CLAUDE.md`。结果是：Claude Code 在编辑文章时完全没有加载这些规则，`lastmod` 没更新、标签也没按规则加，而且**不会报错或提示**——因为当时的 Claude Code 不认识 `AGENTS.md` 这个文件名，不是规则被违反，而是规则从没被读到过。

当时的修复：在根目录新建 `CLAUDE.md`，内容只写一行 `@AGENTS.md`。这个文件现在仍然保留着，在新版本里也没有副作用。

现在排查「规则没生效」，先用 `/memory` 或 `/context` 看实际加载了哪些指令文件，再检查是不是同时存在 `CLAUDE.md` / `CLAUDE.local.md` 把 `AGENTS.md` 挡掉了。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-13 | 标题改为「Claude Code 使用笔记」；补 AGENTS.md 踩坑与 `/add-dir` 会话内加目录说明 | 原标题过简；补规则未加载问题，以及已启动会话如何加目录 |
| 2026-07-21 | 新增「/loop 与 /schedule」章节 | 原文档缺少定时/循环任务相关内容 |
| 2026-07-25 | 新增「Headless 模式（非交互式）」章节 | 原文档缺少 `-p`/`--print` 非交互模式、CI/CD 自动化相关内容 |
| 2026-07-30 | 新增「Subagents 子代理」章节 | 原文档缺少子代理定义格式、存放位置、`/agents` 管理、调用方式相关内容 |
| 2026-10-17 | 新增「权限模式」「Hooks：PreToolUse」「没有 profile，用 settings 分层代替」三节 | 搭建无人值守 agent 时需要 `dontAsk`、PreToolUse hook 和两套权限配置 |
| 2026-11-21 | 扩充 `/goal` 小节；cc-switch 内容移到单独文档；重写「CLAUDE.md 与 AGENTS.md」 | 补充官方文档里的用法、评估机制和错误处理；已不再使用 cc-switch；Claude Code v2.1.277 起原生加载 AGENTS.md |
| 2026-11-21 | 新增「auto mode 详解」「Transcript：会话记录」；「踩坑记录」移到文末 | 补充 auto mode 的判定机制和 transcript 的含义；踩坑记录集中放在最后 |
| 2026-11-22 | 开启文章目录（`ShowToc`）；站内链接改为相对 `.md`；代码块注释改为英文 | 文章较长，需要从开头跳转到各章节；遵守博客内链与代码块规范 |
| 2026-11-25 | 「Headless 模式」下新增「无人值守机器上的登录：claude setup-token」 | 服务器上的交互式登录会到期，需要长期 token 的用法 |
