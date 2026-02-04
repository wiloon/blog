---
title: Fork 项目同步与提交 PR 的完整流程
author: "-"
date: 2026-02-02T18:56:44+08:00
url: git-fork-sync-and-pr
categories:
  - development
tags:
  - git
  - github
  - opensource
  - remix
  - AI-assisted
---

## 概述

在参与开源项目开发时，通常的工作流程是：Fork 主仓库 → 在自己的仓库开发 → 保持与主仓库同步 → 提交 Pull Request。本文记录这个完整的操作流程。

## 前置准备

### 添加上游仓库

首次 fork 项目后，需要添加原始仓库（上游仓库）作为远程仓库：

```bash
# 添加上游仓库
git remote add upstream <原始仓库的 git 地址>igin    https://github.com/your-username/project.git (fetch)
origin    https://github.com/your-username/project.git (push)
upstream  https://github.com/original-owner/project.git (fetch)
upstream  https://github.com/original-owner/project.git (push)
```

- **origin**: 你的 fork 仓库
- **upstream**: 原始仓库（上游）

## 保持本地主分支同步

在开发新功能前，或定期需要将上游仓库的最新变更同步到本地：

### 1. 获取上游仓库的最新变更

```bash
git fetch upstream
```

这会下载上游仓库的所有分支和提交，但不会合并到本地。

### 2. 切换到本地主分支

```bash
git checkout main
# 或者
git switch main
```

### 3. 检查当前状态

```bash
git status
```

确保工作区是干净的，没有未提交的更改。

### 4. 合并上游主分支

```bash
git merge upstream/main
```

**为什么 main 分支用 merge 而不是 rebase？**

- **main 分支不应该有自己的提交** - 所有开发都在功能分支进行
- 如果 main 分支是干净的（没有本地提交），`merge` 会自动执行 **fast-forward**，结果和 rebase 一样
- `merge` 不会改写历史，不需要强制推送，更安全
- 操作更简单，出错风险更低
- 如果 main 分支意外有本地提交，merge 会保留完整历史，便于发现问题

**注意：** rebase 主要用于功能分支的整理，下面会详细说明。

### 5. 推送到你的远程仓库

```bash
git push origin main
```

将同步后的主分支推送到你的 fork 仓库（不需要 `--force`）。

## 开发功能分支

### 1. 创建并切换到功能分支

```bash
# 从最新的 main 分支创建功能分支
git checkout -b feature/your-feature-name
# 或者
git switch -c feature/your-feature-name
```

### 2. 进行开发

在功能分支上进行代码开发、测试、提交。

```bash
git add .
git commit -m "feat: add new feature"
```

### 3. 保持功能分支与主分支同步

在开发过程中，主分支可能已经更新，需要定期同步：

```bash
# 切换回主分支
git switch main

# 同步上游变更（重复前面的步骤）
git fetch upstream
git merge upstream/main
git push origin main

# 切换回功能分支
git switch feature/your-feature-name

# 将主分支的最新变更 rebase 到功能分支
git rebase main
```

### 4. 解决冲突（如果有）

如果 rebase 过程中出现冲突：

```bash
# 1. 手动编辑冲突文件
# 2. 标记冲突已解决
git add <冲突文件>

# 3. 继续 rebase
git rebase --continue

# 如果想放弃 rebase
git rebase --abort
```

### 5. 推送功能分支

由于使用了 rebase，需要强制推送（如果之前已经推送过该分支）：

```bash
git push --force-with-lease origin feature/your-feature-name
```

**为什么使用 `--force-with-lease` 而不是 `-f`？**

- `--force-with-lease` 是更安全的强制推送方式
- 它会检查远程分支是否被其他人修改过
- 如果远程有新的提交（不在你的本地），推送会失败，避免覆盖他人的工作
- `-f` 会无条件覆盖远程分支，可能导致数据丢失

## 提交 Pull Request

### 1. 推送功能分支后

在 GitHub 页面访问你的 fork 仓库，会看到提示创建 Pull Request 的按钮。

### 2. 创建 PR

- 选择源分支：`your-username/project:feature/your-feature-name`
- 选择目标分支：`original-owner/project:main`
- 填写 PR 标题和描述
- 提交 PR

### 3. 代码审查和修改

如果维护者要求修改：

```bash
# 在功能分支上继续修改
git add .
git commit -m "fix: address review comments"

# 推送更新
git push origin feature/your-feature-name
```

PR 会自动更新。

### 4. PR 合并后清理

当 PR 被合并后：

```bash
# 同步主分支
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# 删除本地功能分支
git branch -d feature/your-feature-name

# 删除远程功能分支
git push origin --delete feature/your-feature-name
```

## 完整命令速查

### 首次设置

```bash
git remote add upstream <上游仓库地址>
git remote -v
```

### 同步主分支

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 开发和提交

```bash
# 创建功能分支
git switch -c feature/your-feature-name

# 开发提交
git add .
git commit -m "feat: your changes"

# 同步主分支变更到功能分支
git switch main
git fetch upstream
git merge upstream/main
git push origin main

git switch feature/your-feature-name
git rebase main

# 推送功能分支
git push --force-with-lease origin feature/your-feature-name
```

## 常见问题

### 1. main 分支为什么用 merge 不用 rebase？

- **main 分支应该保持干净**：不应该有自己的本地提交，只是 upstream 的镜像
- **merge 更安全**：如果 main 是干净的会自动 fast-forward（和 rebase 效果一样）
- **不需要 force push**：merge 不改写历史，普通 push 即可
- **风险更低**：即使操作失误也不会丢失提交

### 2. 功能分支什么时候用 rebase？

- **整理提交历史**：将功能分支的多个提交整理成清晰的线性历史
- **同步主分支更新**：将 main 的最新变更合并到功能分支（`git rebase main`）
- **保持提交清晰**：避免不必要的合并提交，便于代码审查

### 3. 什么时候用 merge？

- **同步 main 分支**：`git merge upstream/main`（本文推荐做法）
- **协作分支**：多人共同开发一个功能分支时
- **保留完整历史**：当你想保留所有分支信息时
- **PR 合并**：将功能分支合并到主分支（通常由 PR 自动处理）

### 4. 如果忘记同步主分支就开始开发了怎么办？

可以在功能分支上直接 rebase 上游主分支：

```bash
git fetch upstream
git rebase upstream/main
```

这样可以跳过 main 分支，直接将功能分支变基到最新的上游 main 上。

## 最佳实践

1. **经常同步**：定期同步上游仓库，避免分叉太久导致大量冲突
2. **小步提交**：提交要小而频繁，便于代码审查和问题定位
3. **描述清晰**：提交信息和 PR 描述要清晰明确
4. **遵守规范**：遵循项目的贡献指南和代码规范
5. **测试充分**：提交 PR 前确保代码通过所有测试
6. **及时响应**：关注 PR 的反馈，及时回应和修改

## 参考资料

- [GitHub Fork & Pull Request 工作流](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
- [Git Rebase 文档](https://git-scm.com/docs/git-rebase)
- [理解 git push --force-with-lease](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-leaseltrefnamegt)
