---
title: "Claude Code + Cursor: 两家 agent 在一台家用服务器上协作开发"
author: "-"
date: 2026-10-22T12:12:28+08:00
lastmod: 2026-10-22T12:12:28+08:00
url: claude-cursor-cross-review-agents
draft: true
categories:
  - AI
tags:
  - claude-code
  - cursor
  - agent
  - github
  - remix
  - AI-assisted
---

这是 [AFK Agent: 让 Claude Code 自主处理 GitHub Issue](/afk-agent-github-issues/) 的后续。那篇写的是 Claude Code 一个人在 homelab 的 ser8 上挑 issue、写代码、开 PR。这篇记录最近两天的变化：Cursor 加了进来，两家模型分工、互相审查。记下来的是现在的状态、踩过的坑，以及下一步打算看什么。

## 为什么要两个模型

最早的版本里，Claude 写代码，再开一个 Claude 会话审自己的 PR。问题是同一个模型有同样的盲区，自己审自己，能看出来的东西有限。

另一个问题出在动手之前。ENX 的 issue 和 ADR 多半是我在 Mac 上和 Claude Code 一起写的，从来没有第二个模型看过。有一个 issue 写好三天后，里面的验收标准已经和 main 对不上了。

所以现在的分工是：

- Cursor 负责实现。它在 ser8 本机运行（`cursor-agent` 命令行），不再用云端的定时任务。
- Claude 负责规划和评审：按 Cursor 的意见修订 issue，再审 Cursor 的 PR。
- 我只在两个模型都定不了的时候出现。

我把“谁写的就由另一个模型来审”写成了项目的一条原则（P-4）。

## 一条流水线

入口是 GitHub issue 上的 `ready-for-agent` 标签。这个名字来自 Matt Pocock 的 skills，他的 triage 标签和建 issue 的技能都用这个词，建好的 issue 不用再换标签。

一个 issue 进来之后：

1. 方案评审。Cursor 读 issue 和它依据的 ADR，提意见；Claude 按意见修订。最多三轮。Claude 定不了的问题标 `ready-for-human`，等我在 issue 下回答。
2. Cursor 在独立的 git worktree 和分支上实现，runner 开 PR。
3. Claude 评审。有必须改的地方，Cursor 改，再审。
4. CI 全绿、没有需要人在浏览器里看的检查项，runner 自己合并；否则交给我。
5. 合并后收尾：PR 评审里顺手发现、但不属于这个 issue 的问题，开成新的 issue；只有我能做的事（比如在生产主机上配密钥）建成 Linear 任务。

除此之外还有几个从中途接进来的入口：我自己写的 PR 打 `agent-review` 标签，由 Cursor 审、Claude 修；我对 Cursor 的 PR 有意见，打 `cursor-fix` 标签，让 Cursor 按评论改。

调度全靠一个 bash 脚本 `run.sh`，现在大约 1170 行。它没有自己的数据库，状态全在 GitHub 上：标签、评论里埋的 HTML 注释标记、PR 状态，再加几个本地的标记文件。不需要判断的事都交给 bash：轮询 CI、贴标签、收集 follow-up。模型只用在需要判断的地方。

## 现在还是手动触发

timer 在 10 月 20 日就关掉了。现在是我挑一个 issue，在 Mac 上一条 ssh 命令触发：

```bash
# run one issue through the pipeline on ser8
ssh ser8 'systemd-run --user --unit=enx-agent-issue278 --collect ~/enx-agent/bin/run.sh 278'
```

每跑完一个，我和 Mac 上的 Claude Code 一起看日志和 GitHub 上的来回评论，找出 runner 的问题，改脚本，再跑下一个。这样做慢，但每跑一个 issue 都能找出一两个问题，这个阶段我不急着开 timer。

## 踩过的坑

几个印象比较深的：

- **两套流程并存。** 探索阶段留下了一条旧路径：`ready-for-agent` 的 issue 还是由 Claude 自己实现、自己审，和新流程不一样。我手动测试新流程，本来就是为了以后让 timer 自动跑，所以把旧路径直接删了，只留一条。
- **手动运行被每日上限拦住。** Cursor 有每天最多跑几次的上限，本意是防止 timer 失控，结果连我手动触发也拦。改成上限只管 timer。
- **纯文档 PR 被判 CI 失败。** 只改文档的 PR 不触发 CI，`gh pr checks` 返回 “no checks reported”，脚本当成了失败。改成隔一分钟再看一次，仍然没有检查就算通过。
- **我手动合并的 PR，收尾就丢了。** follow-up 和要我动手的事项只在 runner 自己合并时收集。有一次我在 GitHub 上加标签时顺手点了 merge，这些东西就没人管了。现在每次运行都会扫最近 7 天合并的、runner 评审过的 PR，每个只收一次，不花模型的 token。
- **follow-up 的 follow-up。** 每次评审都会留几个小建议，开成 follow-up issue；做这个 issue 时又留几个，一层层开下去，越来越小，但停不下来。现在做 follow-up 的 PR 不再开 follow-up，值得改的当场改。
- **我的判断错了，被 Cursor 纠正。** 有个测试断言，我在 Mac 上判断它“永远不会失败”，开了 issue 让 ser8 修，还附了建议的写法。Cursor 在方案评审里指出：原来的断言在某种数据下会失败，我建议的写法才是真的什么都没检查，并改了方案。这件事正好说明为什么动手前要让另一个模型看一遍方案，规划的人自己也会错。

## 原则文档

每次我被叫出来做决定，就问一句：这个决定能不能写下来，下次不用再问我？能写的就进 ENX 仓库的 `docs/agents/principles.md`。两个模型在评审方案、写代码、审 PR 之前都会先读它。

现在有七条，比如“PR 只做它的 issue”、“测试必须真的检查了东西”、“在任何地方查词都算一次查词，管理员也一样”。最后这条来自一个 issue：方案评审时 Cursor 问管理员查词要不要计数，Claude 定不了，交给了我。我回答之后，这个答案就成了原则。

我希望看到的趋势是：原则越来越多，我被叫出来的次数越来越少。现在还没有数据证明这一点。

## 现状

- 流水线跑通了几个 issue：方案评审修过方案、Claude 评审后 Cursor 改过代码、我回答问题后流程接着跑，这几条路径都走过了。
- 还没测到的：我在 Cursor 的 PR 上提意见、让它改的那条路径。
- timer 和自动扫描代码找 bug 的功能都关着。
- Claude Code 订阅的额度这周只剩不到 10%，大规模测试要等周五额度重置。

## 业界有没有现成的方案

额度不够跑测试，正好查一下别人怎么做。我们的做法可以概括成：GitHub 当消息总线，一个脚本按标签调度，两家厂商的命令行 agent 分工并互审，人只在定不了的时候出现。

查到的东西大致分三类：

- **并行管理多个 agent 的工具。** Claude Squad（开源，用 tmux 加 git worktree）、Conductor（Mac 应用）、Vibe Kanban（看板，支持十几种 agent，原公司已停止维护，现在社区接手）、Emdash、amux 等。它们支持 Claude Code、Codex、Cursor 等多家，但解决的是“同时开很多个 agent，人来挑结果”，是交互式的，不做按标签触发、无人值守的流水线。
- **跨厂商互审。** OpenAI 今年 3 月开源了 codex-plugin-cc，在 Claude Code 里直接调 Codex 审代码，还有一个对抗式审查模式。思路和我们的“另一个模型来审”一样，但用在交互会话里。
- **同一家的多 agent。** Claude Code 自带 subagent；DeepSeek 开源的 agent 框架 Harness 在论文里描述了一个多 agent 模式，主 agent 创建队友，共享代码目录，通过信箱互相发消息，论文自己说还是初步实验。

Harness 我单独看了一下，它和我们不在一层。它是一个 agent 运行时，和 Claude Code、cursor-agent 是同一层，管的是一个 agent 怎么调模型、用工具；它的多 agent 模式也是一次会话里同一个框架内的分工，没有跨厂商互审，也不接 GitHub 的标签和 PR。它能替代的是流水线里的某个 agent，不是 runner。比如让它跑 DeepSeek 的模型，接一部分评审。

结论是：工作区隔离、issue 拆小、由另一个模型评审、人只在关键处把关，这些做法和资料里推荐的一致。我没找到现成的“按标签跑方案评审、实现、互审、自动合并”的开源流水线，所以暂时不换工具，继续在现有架构上改。

## 下一步

按先后：

1. **度量。** 记录每个 issue 跑了几轮、花了多少 token、我被叫出来几次。runner 已经记了用时和 token，补上后面两项，几乎不花额度。有了数据，才能回答“原则有没有让我少操心”。
2. **加第三家模型。** 先在 Mac 上手动试 codex-plugin-cc，看 Codex 审得怎么样；DeepSeek Harness 也是候选。好用的话，让 runner 把一部分评审交给第三家模型，减轻 Claude 额度的压力。
3. **runner 的形态。** 1170 行 bash 还撑得住。开 timer 之前，比较一下改成 GitHub Actions 按标签事件触发、在 ser8 上用 self-hosted runner 跑，会不会更好维护。
4. **看板前端。** 看 Vibe Kanban 一类工具能不能只当前端，流水线逻辑留在 runner 里。优先级最低。

## 参考

- [The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)（Addy Osmani）
- [9 Open-Source Agent Orchestrators for AI Coding](https://www.augmentcode.com/tools/open-source-agent-orchestrators)
- [Best Multi-Agent Coding Orchestrators in 2026](https://amux.io/blog/best-multi-agent-orchestrators-2026/)
- [OpenAI Codex plugin for Claude Code](https://www.mindstudio.ai/blog/openai-codex-plugin-claude-code-cross-provider-review-2)
- [DeepSeek open sources an agent harness where everything is a plugin](https://thenewstack.io/deepseek-harness-open-source-plugins/)
