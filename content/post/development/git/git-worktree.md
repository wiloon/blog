---
title: Git Worktree
author: "-"
date: 2026-07-05T21:05:21+08:00
lastmod: 2026-10-12T10:00:00+08:00
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

## 锁定（lock）

锁定是 Git 自带的功能，不是哪个工具额外加的。锁定的工作树会被 Git 保护起来，不会被清理掉、移动或删除。

### 为什么需要锁定

`git worktree prune` 会清理那些"目录已经不存在"的工作树记录，`git gc` 也会自动做这件事（过期时间由 `gc.worktreePruneExpire` 控制，默认 3 个月）。如果工作树放在移动硬盘或网络共享上，设备没挂载时目录看起来就"不存在"了，Git 会误以为它被删了，把 `.git/worktrees/<name>` 下的元数据清掉。下次挂上设备时，这个目录就和仓库断了联系。锁定就是为了防止这种误删。

### 锁定后哪些操作会被拦住

| 操作                     | 未锁定                         | 已锁定                           |
| ------------------------ | ------------------------------ | -------------------------------- |
| `git worktree prune`     | 目录丢失就清理记录             | 跳过，不清理                     |
| `git worktree remove`    | 工作区干净即可删，脏的要 `-f`  | 要 `-f -f`（两次 force）才能删   |
| `git worktree move`      | 可以移动                       | 要 `-f -f` 才能移动              |
| `git worktree add` 同路径 | 路径丢失时 `-f` 可覆盖         | 要 `-f -f`                       |

锁定**不会**限制在这个工作树里写代码、提交或推送，也不会锁住分支。它只保护工作树本身，不让它被清理、移动或删除。

### 命令

```bash
# 锁定，可以写上原因
git worktree lock --reason "on USB disk" ../feature-x

# 创建时直接锁定（比 add 之后再 lock 少一个竞态窗口）
git worktree add --lock --reason "long-running review" ../review pr-123

# 解锁
git worktree unlock ../feature-x

# 查看：list 里显示 locked，-v 或 --porcelain 会带上原因
git worktree list -v
```

### 锁定状态存在哪

锁定状态就是主仓库里的一个文件：`.git/worktrees/<name>/locked`。文件内容就是 `--reason` 写的原因，没写原因时文件是空的。`git worktree unlock` 做的事就是删掉这个文件。

```bash
$ cat .git/worktrees/docs-adr-056-enx-api-ko/locked
claude session docs-adr-056-enx-api-ko (pid 89635 start Mon Oct 12 02:52:29 2026)
```

### 实例：Claude Code 会自动锁定它创建的工作树

Claude Code 的 `EnterWorktree` 会在 `.claude/worktrees/` 下建工作树，并在会话期间把它锁定，原因里写着会话名和进程 PID（就是上面那个例子）。这样另一个会话或者手动跑的 `git worktree prune` / `remove` 就不会把正在使用的工作树删掉。

所以在 `git worktree list` 里看到 `locked`，通常说明有个会话还占着这个工作树。判断方法：

```bash
cat .git/worktrees/<name>/locked   # 看原因和 PID
ps -p <pid>                        # 进程还在 → 会话还开着，别动
```

如果进程已经不在了，锁就是残留的，可以先 `git worktree unlock` 再 `git worktree remove`。也可以不解锁，直接 `git worktree remove -f -f`。

## 与其他方案的对比

| 方案                    | 磁盘占用               | 切换成本                           | 适用场景                                     |
| ----------------------- | ---------------------- | ---------------------------------- | -------------------------------------------- |
| `git checkout` 切换分支 | 最小                   | 需要保证工作区干净，可能要 `stash` | 单任务顺序切换                               |
| 多次 `git clone`        | 大（每份都是完整仓库） | 无需切换，各自独立                 | 长期并行、彼此完全隔离                       |
| `git worktree`          | 小（共享对象库）       | 无需切换，各自独立                 | 短期并行任务，如紧急修复、review、同时跑测试 |
