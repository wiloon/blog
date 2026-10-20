---
title: "AFK Agent: 让 Claude Code 自主处理 GitHub Issue"
author: "-"
date: 2026-10-17T07:17:29+08:00
lastmod: 2026-10-17T07:17:29+08:00
url: afk-agent-github-issues
draft: true
categories:
  - AI
tags:
  - claude-code
  - agent
  - github
  - loop-engineering
  - remix
  - AI-assisted
---

记录给 ENX 项目搭一个无人值守（AFK）agent 的过程：它定时从 GitHub 上挑一个标了 `ready-for-agent` 的 issue，在独立的 git worktree 里开发、测试、开 PR，满足条件就自己合并。人这边不再盯着它写代码，只负责把 issue 推进到 ready。

Claude Code 相关的参数和 hook 机制在 [Claude Code 使用笔记](./claude-code.md) 里有单独的说明，这里只写怎么把它们组合起来。

## 真正的限制是什么

一开始担心的是上下文超限。实际上 Claude Code 接近上限时会自动压缩上下文，这不是问题。会让 agent 停下来的是这几样：

| 限制 | 说明 | 对策 |
| ---- | ---- | ---- |
| 5 小时用量窗口 | 订阅按 5 小时滚动窗口计额度 | 一轮只做一个 issue；撞到限额就冷却 5 小时 |
| 每周用量上限 | 一周总量 | 每天最多跑 4 轮 |
| 权限确认 | 没人点「允许」，会话就卡住 | `dontAsk` 模式 + 白名单 + PreToolUse hook |
| 机器睡眠/终端关闭 | 本机会话会断 | 放到常开的 Linux 主机上（见下文） |

额度是**按账号算的**。交互用的 Claude Code 和自主 agent 用的是同一个订阅，两个循环同时跑会共用同一个 5 小时窗口和每周上限。所以 agent 那边的每日上限要留出余量给交互使用。

## 两个循环

整个流程分成两个同时运行的循环，中间用 GitHub issue 衔接：

**循环一：人和 agent 一起工作（交互）**

- 发现问题、讨论方案、确认细节
- 产出是 ADR（`docs/architecture/`）和 GitHub issue
- 一个 issue 写清楚了，就打上 `ready-for-agent`
- 回答自主 agent 留下的问题（`needs-info`），再把 issue 改回 `ready-for-agent`
- 审核 agent 留给人的 PR（`ready-for-human`），做浏览器里的人工检查

**循环二：agent 自主工作（无人值守）**

- 定时检查有没有 `ready-for-agent` 的 issue
- 挑一个，建 worktree，按 TDD 开发，跑完测试/类型检查/lint/build
- 开 PR；CI 通过且不需要人工检查就自己合并
- 遇到不确定的问题，不猜，在 issue 上留言提问后停下

人的时间主要花在循环一：需要判断的设计、细节和未知问题。agent 的时间花在循环二：已经说清楚的开发和测试。两边是异步的。

### 什么样的 issue 算 ready

瓶颈在 issue 的质量。标 `ready-for-agent` 之前，issue 里至少要有：

- 验收标准：做到什么程度算完成
- 怎么证明：哪些测试，或者哪个行为可以被测试断言
- 范围：哪些明确不做
- 已经做出的决定：关联的 ADR 或讨论结论

写不清楚的就不标 ready，留在循环一里继续讨论。

## Issue 状态和标签

| 标签 | 含义 | 谁来改 |
| ---- | ---- | ---- |
| `ready-for-agent` | 已经说清楚，agent 可以做 | 人 |
| `agent-wip` | agent 正在做（防止重复领取） | 脚本 |
| `needs-info` | agent 有问题要问，已在 issue 上留言 | agent |
| `ready-for-human` | 需要人：人工检查或人来实现（PR 和 issue 都可以打） | agent / 人 |

流转：

```text
ready-for-agent ──(脚本领取)──> + agent-wip
    ├─ 做完，CI 绿，无人工检查项 ──> PR 合并，issue 自动关闭，下一轮清理 worktree
    ├─ 做完，但有人工检查项 ──────> PR 打 ready-for-human，等人审
    ├─ 遇到未知 ─────────────────> 去掉 ready-for-agent，加 needs-info，留言提问
    │                               人回答后改回 ready-for-agent，下一轮在原 worktree 继续
    └─ 撞到用量上限 ──────────────> 去掉 agent-wip，冷却 5 小时后继续
```

### agent 遇到未知问题时怎么留言

prompt 里要求它：

1. 先 commit 并 push 已完成的部分
2. 在 issue 上评论：完成了什么、分支或 PR 名、问题列表。每个问题编号，列出它看到的选项，并给出推荐
3. 把 `ready-for-agent` 换成 `needs-info`，然后停止

这样人回来时看到的是一个可以直接选择的问题列表，而不是一个半成品。

## 权限：三层

无人值守时不能靠「点允许」，权限要提前定好。

**第一层：`dontAsk` + 白名单。** 启动参数 `--permission-mode dontAsk --permission-prompts none`。白名单里只有开发需要的工具：读写文件、`git`、`gh`、`go`、`pnpm`、`task` 和常用文本命令。白名单外的调用直接拒绝，agent 收到拒绝后会换办法或停下汇报，不会卡住。

**第二层：PreToolUse hook。** 前缀规则表达不了「能 `git push`，但不能推 tag」这种情况，所以加一个 hook 脚本 `guard.sh` 兜底，拒绝：

- `git tag`，推 tag，推 main，force push（`--force-with-lease` 推自己的分支可以）
- `gh release`、`gh workflow`（生产部署也能手动触发）、`gh api`、`gh repo`、`gh secret`
- `gh pr merge` 带 `--admin`；关闭自动合并时所有 `gh pr merge`
- `kubectl`、`ssh`、`docker`/`nerdctl`、`tofu`、`stripe`、`launchctl` 等主机和基础设施工具
- 名字里带 deploy/release/publish 的 `task`
- 写 worktree 以外的文件；`git -C` 指向主 checkout；`cd` 进主 checkout

这个项目里**推 `v*` tag 就会部署生产**，所以 tag 是重点拦截对象。

**第三层：不在主 checkout 里跑。** 交互时点过的「总是允许」都存在项目的 `.claude/settings.local.json` 里，ENX 这里已经有 `kubectl *`、`git push *`、`ssh *`。agent 用 `--setting-sources user` 只读用户级配置，再用 `--settings` 传入自己的白名单和 hook，并且只在单独的 worktree 里工作。

hook 和 permissions 都只检查命令字符串，不是沙箱：`pnpm test` 调用的脚本里做了什么，它们看不到。所以还需要系统层面的底线：

- **GitHub 分支保护**：main 加了 ruleset（禁止直接 push、禁止 force push、禁止删除，必须走 PR）。只有一个维护者，所以不要求审批；CI 按路径触发，所以也没有把 CI 设成必需检查，否则没改到那些路径的 PR 会一直卡住
- **单独的机器**：见下一节
- **待做**：给 agent 单独的 GitHub 账号。现在 agent 用的是我自己的 token，我是仓库管理员，ruleset 的 bypass 规则区分不出「我」和「agent」。换成独立账号后，可以用 tag ruleset 限制只有我能创建 `v*` 和 `chrome-v*` tag

## 两台机器分工

一开始把自主循环装在 MacBook 上，后来改成两台机器：

| 机器 | 跑什么 | 产出 |
| ---- | ---- | ---- |
| MacBook Air | 循环一：人 + agent 交互 | ADR、GitHub issue、对 `needs-info` 的回答、PR 审核 |
| ser8（Linux，Omarchy，常开） | 循环二：自主 agent | 分支、PR、合并 |

两台机器之间不直接通信，只通过 GitHub（issue、标签、PR、main 分支）交换状态。

这样分的好处：

- **隔离**：MacBook 上有 kubectl 配置、ssh 密钥、Stripe live key、各种 token。agent 放在另一台机器上，即使 hook 漏了什么，它也够不到这些东西
- **不和人抢工作目录**：不会和交互会话同时改主 checkout
- **常开**：不受 MacBook 合盖、睡眠影响，用 systemd timer 代替 launchd
- **权限可以从零配置**：Linux 上可以建一个专用用户，只放 agent 需要的凭据

需要注意的：

- **额度不会变多**：两台机器用同一个 Claude 订阅，额度还是共用的
- **环境要在 Linux 上重建**：Go、Node 24 + corepack pnpm、本地 ECDICT 副本、各子项目的 `.env`（含 Clerk dev 密钥）、私有 Nexus 的 CA 证书、Playwright 浏览器（扩展的 e2e 需要 xvfb）
- **Claude Code 登录**：在 Linux 上用订阅账号登录一次
- **脚本要改成 Linux 版本**：通知（macOS 的 `osascript` 换成手机推送之类）、`date -r` 等 BSD 写法、launchd 换成 systemd timer

### 用哪个系统用户运行

一开始建了一个专用用户 `enx-agent`：不能 sudo，不在 `docker` 组（docker 组等同于 root），主目录 700，读不到 `/home/wiloon`。后来决定不用它，直接在 wiloon 账户下运行，专用用户已经删掉：

```bash
sudo loginctl terminate-user enx-agent   # its linger-started systemd --user blocks userdel
sudo userdel -r enx-agent
```

用 wiloon 的理由是省事：已经配好了 GitHub 的 SSH key 和 Claude Code 登录。代价是隔离变弱：这把 SSH key 能推 wiloon 名下的所有仓库，wiloon 的主目录里也有别的凭据。目前靠 guard 兜底（禁止读 `~/.ssh`、`~/.config/gh`、`~/.config/enx-agent`，禁止直接执行 `ssh`，写文件限定在 worktree 内）。

ser8 上没有装 zsh，所以脚本都改写成 bash。目录布局：

```text
~/enx-agent/
  bin/          run.sh guard.sh settings.json prompt.md config.env env.sh
  mise.toml     go 1.27.0, node 24.21.0, task, golangci-lint 2.14.0 (mise walks up parent dirs)
  enx/          agent-only clone; worktrees branch off it
  worktrees/    issue-<n>/ per issue
~/.config/enx-agent/   telegram.env (600), CA bundle, env-files/ for .worktreeinclude
~/.local/state/enx-agent/   lock, cooldown, daily run counter, logs/
```

`mise.toml` 放在 `~/enx-agent/` 而不是仓库里：mise 会沿父目录向上找配置，所以 clone 和所有 worktree 里自动用项目锁定的版本，出了这个目录还是 wiloon 全局的 Node 26。

ser8 通过 WireGuard 连到局域网里的 50.73，那台机器上的 xray 做透明代理和分流。wg-quick 的规则是整机流量都进隧道（不是按用户），所以 ser8 上任何用户都能连上 Telegram。

### ser8 上的工具链

不改系统包。ser8 是 Arch 系，pacman 数据库已经一个多月没同步，用 pacman 装新包要先做全系统升级，所以改用 mise 按用户安装。agent 用的版本由 `~/enx-agent/mise.toml` 固定，和项目锁定的一致（gh、claude 用 wiloon 全局的 mise 配置；golangci-lint 2.14.0 全局也装了一份）：

```bash
cd ~/enx-agent && mise trust mise.toml && mise install
corepack enable && mise reshim   # pnpm comes from corepack, version from packageManager (12.6.0)
```

私有 Nexus 用的是自签的根 CA，只给这个用户配置，不加进系统信任库。写在 `~/.config/enx-agent/env.sh` 里，由 `~/.bashrc` 和 `run.sh` 加载：

```bash
export SSL_CERT_FILE="$HOME/.config/enx-agent/ca-bundle.crt"   # system bundle + homelab root CA
export GIT_SSL_CAINFO="$SSL_CERT_FILE"
export NODE_EXTRA_CA_CERTS="$HOME/.config/enx-agent/wiloon-root-ca.crt"   # Node ignores the OS store
export GOPROXY="https://nexus.wiloon.com/repository/go-group/,https://goproxy.cn,direct"
```

验证：仓库 clone 到 `/home/enx-agent/enx`，`pnpm --version` 自动下载到 12.6.0，`go mod download` 通过 Nexus 成功。

### 通知

agent 用的是我自己的 GitHub token，以我的身份开 PR、在 issue 上留言。GitHub 不会因为「我自己」的操作给我发通知，所以不能指望 GitHub App 的推送，需要单独的手机推送。候选方案和对比见 [ntfy](../development/ntfy.md)，最后选了 Telegram Bot。

两个要处理的点：

- **网络**：家里的网络直连不了 `api.telegram.org`（MacBook 和 ser8 都超时），需要走代理，或者在 Cloudflare Worker 上做一个转发
- **bot token 放哪**：不放进全局环境变量。`claude -p` 会继承启动它的进程的环境变量，agent 跑一句 `env` 就能看到。token 放在 `enx-agent` 用户下一个权限 600 的文件里，只在 `run.sh` 的通知函数里读取，不 export 给 Claude；agent 的 settings 里再加一条 deny 规则，禁止读这个文件

### Claude Code 的 agent teams 用不上

Claude Code 有一个实验性的 agent teams 功能：一个会话当 lead，再起几个 teammate，各自有独立的上下文，可以互相发消息、共享任务列表。它不适合这里的自主循环：

- 官方文档写明 teammate 只能在交互会话里创建，`claude -p` 下不会创建 teammate
- teammate 不继承 `dontAsk` 模式，权限请求会冒泡到 lead 等人批准
- token 消耗随 teammate 数量线性增长，和省额度的目标冲突

它更适合 MacBook 上的交互循环，比如让几个 teammate 从不同角度审一个 ADR 或 PR。

## 已经准备好的东西

目前写在 MacBook 的 `~/.local/share/enx-agent/` 下，迁到 ser8 时照搬并改成 Linux 版本：

| 文件 | 作用 |
| ---- | ---- |
| `config.env` | 仓库路径、是否自动合并、每日上限（4）、冷却时长（5 小时）、单轮超时（150 分钟）、暂停开关 |
| `prompt.md` | 给 agent 的 prompt 模板：工作规则、未知问题的处理方式、合并条件、结尾输出 `RESULT:` 行 |
| `run.sh` | 一轮的执行：加锁 → 检查冷却和每日上限 → 清理已关闭 issue 的 worktree → 挑 issue（先续做，再挑新的，跳过已有 PR 的）→ 建 worktree 并复制 `.env` → 跑 `claude -p` → 按 `RESULT:` 行处理标签和通知 |
| `settings.json` | agent 专用的权限白名单、deny 规则、PreToolUse hook 配置 |
| `guard.sh` | PreToolUse hook，拦截上面列出的危险操作 |

`run.sh` 里调用 Claude Code 的部分：

```bash
ENX_AGENT=1 ENX_AGENT_WORKTREE="$WT" ENX_AGENT_AUTO_MERGE="$AUTO_MERGE" \
  claude -p "$prompt" \
    --model "$MODEL" \
    --setting-sources user \
    --settings "$SELF_DIR/settings.json" \
    --permission-mode dontAsk \
    --permission-prompts none \
    --output-format stream-json --verbose \
    > "$run_log" 2>&1 < /dev/null
```

`stream-json --verbose` 会把每一步工具调用都写进日志，事后可以回看 agent 做了什么。

仓库这边：

- 新建标签 `needs-info`、`ready-for-human`、`agent-wip`（`ready-for-agent` 原来就有）
- main 分支 ruleset `protect-main`

### 验证

- `guard.sh` 单独测了 27 个用例：tag、推 tag、推 main、force push、`gh workflow run`、`gh api`、关闭自动合并时的 `gh pr merge`、`kubectl`、`task deploy:homelab`、`rm -rf /`、写 `~/.zshrc` 都被拒绝；推功能分支、`--force-with-lease`、`go test`、`task test`、`rm -rf node_modules`、写 worktree 内文件都放行
- 用真实的 `claude -p`（haiku 模型，临时 git 仓库）跑了一次：`git tag` 和 `osascript` 被 hook 拒绝，Claude 收到 `PreToolUse:Bash hook error: enx-agent guard: no git tags (v* deploys production)`，没有重试；`ls` 正常执行；仓库里没有生成 tag

### 第一轮实测（#117）

在 ser8 上手动触发了一轮，关闭自动合并：

```bash
systemd-run --user --unit=enx-agent-manual-117 --collect ~/enx-agent/bin/run.sh 117
```

issue #117 是修 enx-api 的 57 个 errcheck/staticcheck 告警，并启用 golangci-lint 的 standard 规则集。结果：

- 5.5 分钟、53 轮，`total_cost_usd` 显示约 1 美元（订阅账号不按这个计费，但可以当作额度消耗的参考）
- 开了 PR #204：改了 25 个文件，+93/-68，正文有 `Closes #117`、改动说明、跑过的检查和没跑的测试（integration 标签的 e2e 只做了 lint 和 vet）
- CI 全绿：go test、golangci-lint、ko image build
- 自动合并关着，所以它给 PR 打了 `ready-for-human`，Telegram 收到「needs review」
- issue 里留给判断的 4 处 S1016，它逐个做了决定并写明理由；issue 范围外发现的 8 处 `resp.Body.Close` 也一起修了；范围外的 gofmt 问题没动，只在 PR 里提了一句

权限方面：guard 一次都没触发；`dontAsk` 拒绝了 6 次，都是白名单匹配不了的复杂命令（`for` 循环、多行命令、`${PIPESTATUS}`、很长的 `&&`/`;` 链）。每次被拒后它都会拆成简单命令重试，没有卡住。

## 开发 agent + 审查 agent

第一轮之后加了审查步骤。最初想用 Claude Code 的 agent teams，但它在 `claude -p` 下不会创建 teammate，teammate 也不继承 `dontAsk`，无人值守用不了。所以改由 `run.sh` 依次启动几个独立的 `claude -p`，每个都是全新上下文：

```text
开发 run ──开 PR──> 审查 run (round 1)
                      ├─ REVIEW: pass    → runner 合并 / ready-for-human
                      └─ REVIEW: changes → 修改 run → 审查 run (round 2)
                                                        ├─ pass    → 同上
                                                        └─ changes → ready-for-human，交给人
```

三个角色：

| 角色 | prompt | 权限 |
| ---- | ---- | ---- |
| 开发 | `prompt.md` | 改 worktree 里的文件、commit、push 自己的分支、开 PR |
| 审查 | `review-prompt.md` | 只读：看 diff、跑测试和 lint，只能写 `/tmp` 和发一条 PR 评论；不能 commit、push、改标签 |
| 修改 | `fix-prompt.md` | 同开发，按审查意见改，push 后发一条 PR 评论逐条说明 |

### 防止两个 agent 循环停不下来

循环由 bash 脚本控制，不由 agent 决定：

- **轮数上限**：最多审 2 轮，第 2 轮还有必改项就打 `ready-for-human` 交给人
- **只有必改项阻塞**：错误行为、没达到验收标准、行为变化没有测试、违反 AGENTS.md、检查失败，才算 Must fix；其余都是 Nit，不阻塞。拿不准的算 Nit
- **第 2 轮只验收**：只检查第 1 轮的必改项有没有解决、修改有没有引入新问题；没被修改碰到的代码，新发现一律算 Nit。这样问题清单只会变短，审查者不能每轮提新要求
- **没进展就停**：修改 run 没有产生新 commit，直接交给人
- **额度**：每个 `claude -p` 都计入每日上限（12 次）

### 人的审查意见也走修改步骤

人在 PR 上写完审查意见后，给 PR 打 `agent-fix` 标签。下一轮 runner 优先处理这类 PR：回到原 worktree，把意见交给修改 run，改完再进审查循环（第 1 轮重点核对人的每条意见）。

仓库是公开的，任何人都能评论，所以交给 agent 的意见**只取仓库所有者写的**（review、普通评论、行内评论），其他人的评论不传进去。agent 自己发的评论用 `<!-- enx-agent-review round=N -->`、`<!-- enx-agent-fix -->` 开头做标记，用来区分人和 agent（它们用的是同一个 GitHub 账号），也用来只取上次修改之后的新意见。

### 实测：PR #204 处理人的审查意见

我在 #204 上留了 3 条非阻塞意见，然后给 PR 打 `agent-fix`：

| 步骤 | 用时 | 结果 |
| ---- | ---- | ---- |
| 修改 run | 61 秒、29 轮 | 3 条都改了（加了 `mustSave` 测试辅助函数、删掉不再需要的 IDE 注释、拆开过长的一行），push 一个 commit，发评论逐条说明 |
| 审查 run，第 1 轮 | 31 秒、11 轮 | 逐条核对 3 条意见并跑了 `go vet`、`go test`，`REVIEW: pass`，Must fix 和 Nits 都是 none |

`AUTO_MERGE=0`，所以最后打了 `ready-for-human`，Telegram 收到「review passed」。CI 全绿。

发现的问题：审查 agent 跑不了 golangci-lint（ser8 上没单独装，审查角色的白名单也没放行），它在评论里如实写了「没能运行 lint，等 CI 结果」。修复：在 `~/enx-agent/mise.toml` 里固定 `golangci-lint = "2.14.0"`（和 CI 同版本），审查白名单加上 `golangci-lint *`。

### 合并改由脚本执行

三个 agent 都不能执行 `gh pr merge`（guard 拦截）。审查通过后，由 `run.sh` 检查：CI 全绿（`gh pr checks --watch`）、PR 正文的 `## Manual checks` 是 none，都满足才合并；`AUTO_MERGE=0` 时只打 `ready-for-human`。合并条件写在脚本里，比写在 prompt 里让 agent 自己判断更可靠。

### systemd timer

定时触发用 systemd 的用户级 timer（wiloon 开着 linger，不登录也会运行）。两个文件放在 `~/.config/systemd/user/`：

```ini
# enx-agent.service
[Service]
Type=oneshot
ExecStart=%h/enx-agent/bin/run.sh
# run.sh limits each claude run itself (MAX_MINUTES); a tick may chain dev, review and fix runs.
TimeoutStartSec=infinity
Nice=10
```

```ini
# enx-agent.timer
[Timer]
OnCalendar=*-*-* 00/2:15:00
RandomizedDelaySec=5min
Persistent=true

[Install]
WantedBy=timers.target
```

- `OnCalendar` 按 ser8 的本地时区（America/Los_Angeles）解释，每 2 小时的第 15 分钟左右触发
- `Persistent=true`：机器关机错过的那次，开机后补跑一次
- 上一轮还没跑完时，新一轮会因为拿不到 `flock` 锁直接退出

装好后先不启用，需要时：

```bash
systemctl --user enable --now enx-agent.timer   # start
systemctl --user list-timers enx-agent.timer    # next run
systemctl --user disable --now enx-agent.timer  # stop
```

临时暂停也可以不动 timer，把 `config.env` 里的 `PAUSED` 设为 1。

## 合并的条件

agent 只有在以下条件都满足时才会自己合并：

- CI 通过（`gh pr checks --watch`）。enx-chrome 没有 CI，只改它时以本地测试为准
- 本地的测试、类型检查、lint、build 都通过
- PR 描述里的 `## Manual checks` 是 none

布局、颜色、动画这类 jsdom 测不出来、需要在真实浏览器里看的改动，agent 不合并，给 PR 打 `ready-for-human` 等人检查。合并到 main 不会触发部署，部署只认 `v*` tag，而 tag 被 hook 拦掉了。

## 待办

- [x] 决定以 wiloon 运行，删掉试建的 `enx-agent` 用户
- [x] ser8 上装工具链（mise：Go、Node、pnpm、gh、task、Claude Code）和私有 CA
- [x] Claude Code、gh（SSH + fine-grained PAT）登录
- [x] 脚本改成 bash 的 Linux 版本；通知用 Telegram Bot
- [x] 第一轮手动跑 #117：PR #204，CI 全绿
- [x] 加审查循环；PR #204 处理人的审查意见并通过审查
- [x] 安装并启用 systemd timer（每 2 小时，2026-10-18 启用）
- [ ] ECDICT、`.env`、Playwright（需要时再准备）
- [ ] 跑一周后再决定是否保持自动合并
- [ ] 给 agent 单独的 GitHub 账号，加 tag ruleset
