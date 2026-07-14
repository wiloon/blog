---
title: "GitHub Personal Access Token：Classic vs Fine-grained"
author: "-"
date: 2026-07-13T09:00:00+08:00
lastmod: 2026-07-13T09:00:00+08:00
url: github-pat-classic-vs-fine-grained
categories:
  - development
tags:
  - github
  - security
  - opentofu
  - AI-assisted
---

GitHub 的 Personal Access Token（PAT）有两套互相独立、并列的机制：Classic 和 Fine-grained。两者各自有独立的设置页面和独立的 token 值，**互不共享权限、互不影响**——改了一个的 scope，对另一个没有任何作用。

## 对比

| | Classic token (`ghp_...`) | Fine-grained token (`github_pat_...`) |
| --- | --- | --- |
| 权限粒度 | 粗粒度，按 scope 打勾（`repo`、`admin:org`、`workflow` ...），一个 scope 覆盖你有权限的**所有**仓库/组织 | 细粒度，创建时指定 Resource owner（个人账号或某个具体组织），再选具体仓库（全部/指定几个），每个仓库单独授予 Contents / Administration / Issues 等权限 |
| 作用范围 | 只要本人对某组织/仓库有权限，token 默认就能操作（除非组织手动 Restrict） | 天生绑死在创建时选的 Resource owner，只能代表操作那一个账号或组织下的资源 |
| 安全性 | 权限范围大，一旦泄露风险高 | 权限可以缩得很小，泄露影响面小，GitHub 官方推荐新场景一律用这个 |
| 过期时间 | 早期可选"永不过期" | 设计上引导必须设置过期时间 |
| 组织侧控制 | 只有"全允许 / 全禁止"的粗暴开关（组织 Settings → Personal access tokens → Tokens (classic)） | 组织可以看到每一个申请访问本组织资源的 fine-grained token，逐个 Approve / Deny / 撤销，可审计 |

## Fine-grained 要解决的问题

Classic token 加 scope 解决不了几个结构性问题，这也是 GitHub 推出 fine-grained token 的原因：

1. **无法限定到具体仓库/组织**——`repo` scope 一勾，能读写所有有权限的仓库，没法只给某一个仓库授权。
2. **权限类别捆绑得太死**——`repo` 一个 scope 打包了代码读写、Issues、PR、部署状态、安全告警等一堆能力，没法只开"读 Issues"这种更细的权限。
3. **组织没有审计/审批机制**——组织对 classic token 只能整体允许或禁止，看不到具体是哪些 token、谁的、权限多大。fine-grained 补上了逐个审批、可追责这一块。
4. **没有强制过期**——泄露的永久 token 是长期风险。

## 踩坑记录：fine-grained token 操作组织仓库报 403

用 OpenTofu（`integrations/github` provider）在新建的 GitHub organization 下创建仓库时报错：

```
POST https://api.github.com/orgs/xxx/repos: 403 You need admin access to the organization before adding a repository to it.
```

排查过程：

1. 一开始以为是 classic token 缺 `admin:org` scope，去 classic token 设置里加上，问题依旧。
2. 用 `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user` 查看 token 前缀，发现环境变量 `GITHUB_TOKEN` 实际存的是 `github_pat_...` 开头的 **fine-grained token**，跟改过权限的 classic token 根本不是同一个。
3. fine-grained token 创建时 Resource owner 选的是个人账号，不是目标组织，所以对组织仓库没有 Administration 权限。

**解决方向：** 保留 fine-grained token，需要重新配置——去 <https://github.com/settings/personal-access-tokens>，Resource owner 选目标组织，并授予 Repository permissions → Administration: Read and write（组织只有一个 owner 时通常无需额外审批，自动生效）。

## 结论

排查 token 权限问题时，第一步先确认环境变量里到底存的是哪个 token（看前缀 `ghp_` 还是 `github_pat_`），再去对应的设置页面调整 scope/permission，避免像这次一样改错了 token 白忙一场。
