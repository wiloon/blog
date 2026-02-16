---
title: "给开源项目提交 Pull Request 完整指南"
author: "-"
date: 2026-02-01T11:10:47+08:00
url: git-pull-request
categories:
  - Development
tags:
  - git
  - GitHub
  - 开源
  - AI-assisted
---

## 概述

给开源项目贡献代码是参与开源社区的重要方式。本文记录了从 Fork 仓库到提交 Pull Request (PR) 的完整流程。

## 前置准备

### Fork 仓库

1. 在 GitHub 上打开你想贡献的开源项目
2. 点击右上角的 **Fork** 按钮
3. 将仓库 Fork 到你自己的账号下

### 克隆你的 Fork

```bash
git clone https://github.com/你的账号/仓库名.git
cd 仓库名
```

## 配置上游仓库

### 添加上游仓库（只需做一次）

```bash
git remote add upstream https://github.com/官方账号/官方仓库.git
```

### 验证 remote 配置

```bash
git remote -v
```

输出应该类似：

```text
origin    https://github.com/你的账号/仓库名.git (fetch)
origin    https://github.com/你的账号/仓库名.git (push)
upstream  https://github.com/官方账号/官方仓库.git (fetch)
upstream  https://github.com/官方账号/官方仓库.git (push)
```

## 同步上游代码

在开始新功能开发前，确保你的本地代码与上游保持同步：

```bash
# 拉取上游最新代码
git fetch upstream

# 切换到 main 分支
git checkout main

# 合并上游的 main
git merge upstream/main

# 推送到你的 fork
git push origin main
```

## 创建功能分支

**不要直接在 main 分支上开发**，应该创建新的功能分支：

```bash
# 基于最新的 main 创建功能分支
git checkout -b feature/你的功能名称
```

分支命名建议：

- `feature/功能描述` - 新功能
- `fix/问题描述` - Bug 修复
- `docs/文档描述` - 文档更新

## 开发与提交

### 进行代码修改

完成你的代码修改后，检查变更：

```bash
git status
git diff
```

### 提交代码

```bash
git add .
git commit -m "feat: 简洁描述你的修改"
```

Commit message 建议遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

### 推送到你的 Fork

```bash
git push origin feature/你的功能名称
```

## 创建 Pull Request

1. 打开你的 Fork 仓库页面
2. GitHub 会提示你刚推送的分支，点击 **Compare & pull request**
3. 或者点击 **Pull requests** → **New pull request**
4. 填写 PR 标题和描述
5. 点击 **Create pull request**

### PR 描述模板

```markdown
## 变更说明

简要描述这个 PR 做了什么

## 变更类型

- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 代码重构

## 测试

描述如何测试这些变更

## 相关 Issue

关联的 Issue 编号（如：Fixes #123）
```

## 处理 Review 反馈

如果维护者要求修改：

```bash
# 在同一分支上继续修改
git add .
git commit -m "fix: 根据 review 反馈修改"
git push origin feature/你的功能名称
```

新的提交会自动出现在 PR 中。

## 解决冲突

如果 PR 显示有冲突：

```bash
# 更新上游代码
git fetch upstream
git checkout feature/你的功能名称

# 变基到最新的 upstream/main
git rebase upstream/main

# 解决冲突后
git add .
git rebase --continue

# 强制推送（因为 rebase 改变了历史）
git push origin feature/你的功能名称 --force
```

## 完整流程总结

```bash
# 1. 一次性配置
git remote add upstream https://github.com/官方账号/官方仓库.git

# 2. 同步上游（每次开发前）
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# 3. 创建功能分支
git checkout -b feature/新功能

# 4. 开发并提交
git add .
git commit -m "feat: 描述"
git push origin feature/新功能

# 5. 在 GitHub 上创建 PR

# 6. 根据反馈修改后推送
git push origin feature/新功能

# 7. PR 合并后清理
git checkout main
git branch -d feature/新功能
```

## 常用命令速查

| 操作 | 命令 |
|------|------|
| 查看远程仓库 | `git remote -v` |
| 拉取上游更新 | `git fetch upstream` |
| 查看所有分支 | `git branch -a` |
| 删除本地分支 | `git branch -d 分支名` |
| 删除远程分支 | `git push origin --delete 分支名` |
| 查看提交历史 | `git log --oneline` |
| 撤销最近提交 | `git reset --soft HEAD~1` |
