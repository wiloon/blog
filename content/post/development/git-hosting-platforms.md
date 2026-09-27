---
title: "Git Hosting Platforms: GitHub, GitLab, Gitea, Forgejo, Codeberg 对比"
author: "-"
date: 2026-09-27T08:30:43+08:00
lastmod: 2026-09-27T08:30:43+08:00
url: git-hosting-platforms
categories:
  - development
tags:
  - git
  - github
  - gitea
  - forgejo
  - codeberg
  - remix
  - AI-assisted
---

## 先分清两层：Git 和平台

GitHub、Gitea、Forgejo、Codeberg 底层用的都是标准 Git。它们之间的区别不在版本控制，而在包在 Git 外面的那层平台：

- 版本控制层：Git 负责提交历史、分支、合并，服务器上存的是普通的 Git bare 仓库。本地的 `git clone`、`git push`、`git pull` 在哪个平台上都一样。
- 平台层：提供 Web 界面、用户和权限、Issue、Pull Request、Wiki、Release、CI 集成等。这些 Git 本身没有，是各平台自己实现的。

另外，这几个名字不是同一类东西：

| 名字 | 类型 | 说明 |
| --- | --- | --- |
| GitHub | 托管服务（闭源） | 微软旗下，2018 年被收购 |
| GitLab | 平台软件 + 托管服务 | 有开源社区版，可自建；也有 gitlab.com |
| Gogs | 平台软件（开源） | Go 编写的轻量 Git 服务，Gitea 的前身 |
| Gitea | 平台软件（开源） | 2016 年从 Gogs 分叉，可自建 |
| Forgejo | 平台软件（开源） | 2022 年从 Gitea 分叉，可自建 |
| Codeberg | 托管服务（非营利） | 运行 Forgejo 的公共实例，codeberg.org |

## 分叉关系：Gogs → Gitea → Forgejo

- Gogs：早期的 Go 语言自建 Git 服务，单个二进制就能跑，资源占用小。但基本由一位维护者主导，合并社区贡献慢。
- Gitea：2016 年社区从 Gogs 分叉出来，采用社区治理，功能迭代快，后来成了自建 Git 服务的主流选择之一。
- Forgejo：2022 年 Gitea 的域名和商标被转到新成立的营利公司 Gitea Ltd，部分社区成员担心项目被商业公司控制，于是分叉出 Forgejo。Forgejo 由非营利组织 Codeberg e.V. 托管，一开始是 Gitea 的“软分叉”（持续同步上游），2024 年起变成硬分叉，不再跟随 Gitea 代码。

所以 Gitea 和 Forgejo 目前的界面和用法仍然很像，但功能细节已经开始分化。Forgejo 的一个重点方向是联邦化（ForgeFed 协议），目标是不同实例之间能互相关注、提 Issue、提 PR。

## Codeberg 是什么

Codeberg 是德国柏林的非营利注册协会 Codeberg e.V. 运营的公共代码托管平台，2019 年前后上线，靠捐款和会费维持。它运行的就是 Forgejo，可以理解为“由社区运营、跑开源软件的 GitHub”。

主要特点：

- 免费，无广告、无追踪，服务器在德国，受 GDPR 约束
- 只面向自由/开源项目，私有仓库只允许小规模、个人用途
- 提供 Codeberg Pages（静态站点）、Woodpecker CI（需申请）、Forgejo Actions（语法兼容 GitHub Actions）、Weblate 翻译平台
- 明确反对拿托管的代码训练 AI
- 规模小，历史上遇到过 DDoS 攻击和宕机

已有一些知名项目迁到了 Codeberg，比如 Zig 编程语言在 2025 年从 GitHub 迁了过去。

## Codeberg 与 GitHub 对比

| 维度 | Codeberg | GitHub |
| --- | --- | --- |
| 所有者 | 非营利协会，会员共同治理 | 微软，商业公司 |
| 平台软件 | Forgejo，开源，可自建 | 闭源 |
| 收费 | 免费，靠捐款 | 免费版 + 付费版 |
| 项目范围 | 只面向自由/开源项目 | 不限，包括商业私有项目 |
| 私有仓库 | 限小规模个人用途 | 不限 |
| CI | Woodpecker CI、Forgejo Actions，资源有限 | GitHub Actions，免费额度大，Marketplace 生态丰富 |
| 静态站点 | Codeberg Pages | GitHub Pages |
| AI | 无 Copilot，反对用托管代码训练 AI | Copilot 深度集成 |
| 数据所在地 | 德国（GDPR） | 美国 |
| 生态 | 小，第三方集成少 | 事实标准，第三方服务优先支持 |
| 稳定性 | 规模小，偶有宕机 | 总体稳定，有商业 SLA |

## 怎么选

- 开源项目、在意平台中立和隐私、不想被大公司锁定：Codeberg。
- 需要私有仓库、大量 CI 资源、Copilot，或者要和第三方服务深度集成、希望项目曝光度高：GitHub。
- 想自己托管（homelab、公司内网）：Gitea 或 Forgejo，单个二进制或一个容器即可运行，资源占用远小于 GitLab。更看重社区治理选 Forgejo，想要商业支持选 Gitea。
- 需要一体化 DevOps（CI/CD、容器仓库、安全扫描全都要）且不在乎资源：GitLab。

需要注意第三方服务的支持范围。比如 Cloudflare Pages 的 Git 集成只支持 GitHub 和 GitLab，用 Codeberg 时常见的做法是 Codeberg 作主仓库，再推送镜像到 GitHub（Forgejo 自带仓库推送镜像功能）。

## 在平台之间迁移

因为底层都是 Git，代码和提交历史可以原样迁移，只需改 remote 地址：

```bash
# point origin to the new platform and push everything
git remote set-url origin https://codeberg.org/<user>/<repo>.git
git push -u origin --all
git push origin --tags
```

Issue、PR、Wiki、Release 属于平台层数据，不在 Git 仓库里。Gitea 和 Forgejo 的“新建迁移”功能可以从 GitHub、GitLab、Gitea 等平台导入这些数据。

## 参考

- [Codeberg](https://codeberg.org/)
- [Forgejo](https://forgejo.org/)
- [Forgejo: Comparison with Gitea](https://forgejo.org/compare-to-gitea/)
- [Gitea](https://about.gitea.com/)
- [Codeberg Docs](https://docs.codeberg.org/)
