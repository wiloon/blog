---
title: "GitHub CODEOWNERS：自动分配 PR Reviewer"
author: "-"
date: 2026-07-17T11:32:36+08:00
lastmod: 2026-07-17T11:32:36+08:00
url: github-codeowners
categories:
  - development
tags:
  - github
  - git
  - codeowners
  - remix
  - AI-assisted
---

## 概述

`CODEOWNERS` 是 GitHub 的一个约定文件：声明仓库里哪些路径由哪些人/团队"负责"。当 PR 改动了某个路径下的文件，GitHub 会**自动把对应的 owner 加进 PR 的 Reviewers 列表**。配合分支保护规则里的 "Require review from Code Owners"，还可以强制要求这些 owner 必须 approve，PR 才能合并。

它解决的问题：团队变大之后，"这段代码改了应该找谁 review" 不再是靠口头约定或者人肉记忆，而是写进仓库、可版本管理、对所有协作者可见的规则。

## 文件位置

GitHub 按以下顺序查找，只会使用**第一个找到的**：

1. 仓库根目录：`CODEOWNERS`
2. `.github/CODEOWNERS`
3. `docs/CODEOWNERS`

文件名区分大小写，没有扩展名，也不支持在多个位置同时生效。

## 基本语法

语法风格类似 `.gitignore`：一行一个路径 pattern，后面跟一个或多个 owner。

```text
# 默认 owner，匹配仓库里所有文件
*                       @wiloon

# 某个目录下的文件由指定团队负责
/infra/                @starlabrys/engineering

# 具体文件可以指定多个 owner，任意一个 approve 都算数
/docs/architecture.md  @wiloon @some-teammate

# 用邮箱也可以（必须是该用户在 GitHub 账号上验证过的邮箱）
*.sql                  db-owner@example.com
```

Owner 可以是：

- `@username`：单个 GitHub 用户
- `@org/team-slug`：某个组织下的团队
- `email@example.com`：用户在 GitHub 上验证过的邮箱

## 匹配规则：后面的 pattern 优先级更高

和 `.gitignore` 不同，`.gitignore` 靠 `!` 取消忽略；`CODEOWNERS` 没有取消符号，而是**文件里越靠后的匹配行优先级越高**——如果一个文件同时匹配多条 pattern，以最后一条为准。

```text
*.js                @frontend-team
/apps/legacy/*.js    @legacy-owner
```

`/apps/legacy/utils.js` 匹配了两行，但因为第二行在后面、更靠后，最终 owner 是 `@legacy-owner`，不是 `@frontend-team`。

想让某个子路径"没有 owner"（不继承上面更宽泛的规则），给它单独一行、后面不写任何 owner：

```text
/apps/            @app-team
/apps/config.yaml
```

`config.yaml` 这一行没有 owner，即使上面 `/apps/` 整体归 `@app-team`，这个文件也不会自动请求 review。

## 生效的前提条件（容易踩的坑）

CODEOWNERS 写对了语法，不代表一定会生效，常见的坑：

1. **Owner 必须对仓库有 write 权限**。个人用户要么是仓库的 collaborator，要么通过 team 拥有权限；团队被写进 CODEOWNERS 前，必须先把这个团队关联到仓库并授予至少 Write 权限（比如用 Terraform `github_team_repository` 或者网页 Settings → Collaborators and teams）。没有 write 权限的用户/团队写进 CODEOWNERS 不会报错，但也不会被自动请求 review。
2. **团队可见性不能是 secret**。要用 `@org/team-slug` 语法自动请求某个团队 review，这个团队至少要是 visible（不能是 secret），否则无法被作为 reviewer 请求。
3. **个人 owner 必须已经接受了协作者邀请**。刚发出邀请、对方还没 accept 的账号不会被自动加进 Reviewers。
4. **只有改动匹配路径的 PR 才会触发**。PR 如果完全没碰到某个 owner 名下的路径，这个 owner 不会出现在 Reviewers 里。
5. **文件本身需要通过语法检查**。仓库 Insights → 有专门的 CODEOWNERS 校验入口，语法错误的行会被 GitHub 忽略并在 PR 里提示。

## 配合分支保护规则

CODEOWNERS 单独存在时，只是"自动加 reviewer"，并不会阻止合并。要让它变成强制门槛，需要在分支保护规则（Settings → Branches → 对应分支 → Branch protection rule）里同时打开两项：

- **Require a pull request before merging**（先决条件，没有这项后面的都不会生效）
- **Require review from Code Owners**（勾选后，只要 PR 改动了 CODEOWNERS 里声明的路径，对应 owner 必须 approve，PR 才能合并）

这两项通常还会搭配 "Require approvals"（设置一个全局最低 approve 人数），两者是叠加关系：全局最低人数保证"至少有人看过"，Code Owners 规则保证"该看的人看过"。

## 一个典型组合：内部协作者 + Owner 兜底

一种常见的团队组织仓库场景：

```text
# CODEOWNERS
*    @org-name/engineering
```

- 团队里的协作者对仓库有 Write 权限，可以直接建分支、开 PR，不需要 fork
- 分支保护规则要求 PR 必须有 Code Owners review 才能合并
- 仓库 owner（通常也是团队里权限最高的人）可以把自己也放进 CODEOWNERS，或者依赖分支保护规则里 "Restrict who can dismiss pull request reviews" / 管理员豁免（`enforce_admins` 相关设置）来决定 owner 自己是否也要被这条规则约束

`enforce_admins`（Terraform GitHub provider 里 `github_branch_protection` 资源的字段）为 `true` 时，仓库管理员/owner 也必须遵守所有分支保护规则（包括必须走 PR、必须有人 approve）；为 `false` 时，管理员/owner 可以绕过这些限制，直接 push 或者不经审批合并 PR。这个开关决定的是"规则对谁生效"，和 CODEOWNERS 是否触发是两回事。

## 小结

- CODEOWNERS 解决的是"改了这段代码该找谁 review"的自动化，本身不是强制门槛
- 要变成强制门槛，必须配合分支保护里的 "Require pull request" + "Require review from Code Owners"
- 团队作为 owner 前，先确认团队对仓库有 Write 权限、且不是 secret 团队，否则规则形同虚设
- 越靠后的 pattern 优先级越高，这点和 `.gitignore` 的思路不一样，容易踩坑
