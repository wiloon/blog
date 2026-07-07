---
title: Git Worktree
author: "-"
date: 2026-07-05T21:05:21+08:00
lastmod: 2026-07-05T21:05:21+08:00
url: git/worktree
categories:
  - Tools
tags:
  - git
  - remix
  - AI-assisted
---

## 是什么

一个 Git 仓库（一份 `.git` 目录）可以同时关联多个"工作树"（working tree），每个工作树是磁盘上一个独立的目录，各自可以检出不同的分支。也就是说不用反复 `git checkout` 切换分支、不用为了同时看两个分支的代码而 `git clone` 出第二份仓库。

普通仓库只有一个工作树（主工作树，main worktree）；`git worktree` 可以在此基础上新增若干"链接工作树"（linked worktree），它们共享同一个 `.git` 对象库（commit、blob、tree 等），但有各自独立的工作区和索引（index）。

## 典型场景

- 紧急修 bug：正在 `feature-a` 分支开发到一半，不想 `stash`，直接开一个新工作树检出 `main` 改 hotfix，改完切回来继续原来的活。
- 同时对比多个分支的代码，或者在一个分支跑测试的同时在另一个分支继续写代码。
- CI / 构建场景：需要同时构建多个分支时，避免重复克隆仓库浪费磁盘和时间。
- review 别人的 PR：新建一个工作树检出对方分支，本地起服务验证，不影响自己当前的工作区。

## 常用命令

```bash
# git worktree add <path> [<branch>]
# path 是新工作树的目录（不能已存在），branch 是要检出的分支
# 新建一个工作树，并基于新分支 feature-x（自动创建）
git worktree add ../feature-x feature-x

# 基于已存在的分支创建工作树
git worktree add ../hotfix hotfix-branch

# -b <new-branch>：基于 commit-ish（这里是 main）新建分支并检出，一步完成
git worktree add -b hotfix-branch ../hotfix main

# 基于某个 commit/tag 创建一个游离状态（detached HEAD）的工作树
git worktree add ../review v1.2.0

# 查看当前仓库关联的所有工作树
git worktree list

# 删除一个工作树（目录和 Git 的关联记录一起清理）
git worktree remove ../feature-x

# 工作树目录被手动删掉了，用这个清理 Git 内部残留的记录
git worktree prune

# 防止某个工作树被 prune 误删（比如它在一个可能断线的移动硬盘上）
git worktree lock ../feature-x
git worktree unlock ../feature-x
```

## 注意事项

- **同一个分支不能同时被两个工作树检出**：`main` 分支已经在主工作树里检出了，就不能在另一个工作树里再检出一次 `main`，Git 会报错拒绝，这是为了避免同一分支在两处被修改造成冲突。
- **工作树目录是普通目录，删除前建议先 `git worktree remove`**：直接 `rm -rf` 目录后，Git 会认为这个工作树"丢了"，需要用 `git worktree prune` 清理记录，否则 `git worktree list` 里还会显示一个失效条目。
- **共享 `.git` 对象库**：多个工作树之间共享 commit 历史和暂存的对象，占用磁盘远小于多次 `clone`；但每个工作树有独立的索引和 `HEAD`，互不影响。
- 链接工作树内部会生成一个 `.git` 文件（不是目录），内容指向主仓库 `.git/worktrees/<name>` 下的元数据。

## 与其他方案的对比

| 方案                    | 磁盘占用               | 切换成本                           | 适用场景                                     |
| ----------------------- | ---------------------- | ---------------------------------- | -------------------------------------------- |
| `git checkout` 切换分支 | 最小                   | 需要保证工作区干净，可能要 `stash` | 单任务顺序切换                               |
| 多次 `git clone`        | 大（每份都是完整仓库） | 无需切换，各自独立                 | 长期并行、彼此完全隔离                       |
| `git worktree`          | 小（共享对象库）       | 无需切换，各自独立                 | 短期并行任务，如紧急修复、review、同时跑测试 |
