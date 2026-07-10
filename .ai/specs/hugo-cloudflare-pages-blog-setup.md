# Spec: Hugo + Cloudflare Pages 搭建个人博客

| 字段     | 值                                                     |
| -------- | ------------------------------------------------------ |
| 状态     | draft-written                                          |
| 交付物   | `content/post/web/hugo-cloudflare-pages-blog-setup.md` |
| Hugo url | `hugo-cloudflare-pages-blog-setup`                     |
| 标题     | Hugo + Cloudflare Pages 搭建个人博客                   |
| 分类     | web                                                    |

---

## 1. 目的

帮助没用过 Hugo / Cloudflare Pages 的朋友，从买域名到发布一个带搜索、评论、访问统计、IaC 管理的博客，跟着本文从零操作一遍。技术选型与实现步骤与本博客的真实实现保持一致。

## 2. 读者

有 GitHub 使用经验，没有域名、没用过 Hugo 和 Cloudflare Pages 的朋友。

## 3. 核心信息

- 域名可以在任意注册商购买（以 GoDaddy 为例），DNS 切到 Cloudflare；一句话提及 Cloudflare Registrar 也能直接买域名，但支持后缀有限
- Hugo 主题安装讲通用步骤，用 PaperMod 举例
- 部署方式与本博客一致：Cloudflare Pages 直接连接 GitHub 仓库，在 Cloudflare 侧构建（`hugo --minify`），**不**经过 GitHub Actions，**不**使用 Containerfile/容器
- 本地预览用最简单的 `hugo server`，不引入 nerdctl / go-task
- 文中域名、仓库名等示例可直接引用本博客真实信息
- 文末说明本博客源码是 GitHub 公开仓库（`github.com/wiloon/blog`），可供参考

## 4. 建议结构（母文 + 子文 hub）

**母文**（本 Spec 交付物）`content/post/web/hugo-cloudflare-pages-blog-setup.md`：

1. 前言：这套技术栈长什么样（一句话概览：Hugo + GitHub + Cloudflare Pages/DNS/CDN）
2. 基础模块（从 0 到能访问、能发文章）
   - 买域名（GoDaddy 示例）
   - DNS 切到 Cloudflare（改 Nameserver）
   - 本地安装 Hugo + 选主题（PaperMod 示例）
   - 写第一篇文章、`hugo server` 本地预览
   - GitHub 建仓库并推送
   - Cloudflare Pages 连接仓库、设置构建命令与产物目录
   - 绑定自定义域名
3. 进阶模块总览（每项 2-3 句概览 + 链接子文）
   - 全文搜索（Pagefind）→ [hugo-static-site-search.md](../../content/post/web/hugo-static-site-search.md)
   - 评论系统（Giscus）→ [giscus.md](../../content/post/development/giscus.md)
   - 访问统计（Umami + Cloudflare Web Analytics）→ [web-analytics.md](../../content/post/cs/web-analytics.md)
   - IaC 管理 Cloudflare Pages 项目（OpenTofu）→ 需新建子文（本站现有 `content/post/cloud/opentofu.md` 是 AWS VPC/EC2 通用入门，不是 Cloudflare Pages 场景），见 §B Round 3
4. 结尾：本博客源码开源在 GitHub（`github.com/wiloon/blog`），可直接参考

---

## 验收清单

- [ ] 标题、url、分类与 Spec 表一致
- [ ] 正文从 `##` 起，无 `#`（MD025）
- [ ] 标签（SDD）：`original`、`AI-assisted` + 内容标签（如 `hugo`、`cloudflare`、`dns`）；无 `remix`、`reprint`
- [ ] 读者跟着教程从零到能访问自己的博客（域名 → DNS → Hugo → 部署 → CDN）
- [ ] 每个关键步骤给出可执行命令或截图说明，不是纯概念介绍
- [ ] 进阶模块三项（搜索/评论/统计）分别正确链接到已有子文
- [ ] OpenTofu 进阶模块的处理方式按 §B Round 3 结论执行

---

## A. 原始素材

> **AI 禁止修改本章节任何内容。**

### 2026-07-09

这个 blog 的源码是 markdown 文档，使用 hugo 编译成了静态页面，然后部署是在 cloudflare 的 cloudflare page，使用了 cloudflare 的 cdn，域名最早是在 godaddy 买的，dns 用的 cloudflare。

今天跟一个朋友聊天，他也想搭一个这样的 blog，我想写一个教程类的文章，让他跟着这个教程做就能把自己的 blog 搭起来。

---

## B. AI 审阅 · 问答

> **规则：**
>
> - AI 只在此处末尾追加新 Round，**不修改已有 Round 的任何内容**
> - 每轮结束时 AI 判断信息是否充分，若充分则写"建议进入 ready-to-write"，**状态由作者手动更新**
> - 作者在"作者回答"下填写，完成后通知 AI 继续下一轮或输出正文

### Round 1

**Q:** 读者的起点是什么？是完全没有域名、没有 GitHub 账号的新手，还是已经有域名、只是不知道怎么接 Hugo + Cloudflare Pages？

**A:**
github有使用经验，但是没有域名，没有使用过 hugo, cloudflare pages.
**Q:** 域名部分是否要讲"在 GoDaddy 购买域名"这一步，还是只讲"域名已有，把 DNS 换成 Cloudflare"？（读者朋友可能已经有域名，或用别的注册商）

**A:**
在 cloudflare 可以买域名吗？或者你建议在哪里买域名？
**Q:** Hugo 主题是否要指定用本博客同款 PaperMod，还是让读者自选主题、只讲通用步骤？

**A:**
主题只讲通用步骤，PaperMod 作为示例。
**Q:** 部署方式是否只讲 Cloudflare Pages 直连 GitHub 仓库自动构建，还是也要提本仓库用的 `build.sh` / Containerfile 这种自定义构建脚本？（读者大概率不需要这么复杂，可能只需要最简单路径）

**A:**
本blog 不是用 github构建的，是在cloudflare构建的，实际上没有用 containerfile,这个文章尽量讲的跟我这个 blog 的实现是一致的。
**Q:** 是否需要包含评论系统、访问统计（Umami）、搜索（Pagefind）等本博客有的进阶功能，还是教程只到"能访问、能发文章"为止？

**A:**
把这个blog用到的所有的技术栈都 写进去，但是要分模块，先讲基础的，然后讲进阶的。
**Q:** 教程里出现的域名、仓库名等示例，是用占位符（如 `yourdomain.com`）还是可以直接引用本博客的真实域名作为示例说明？

**A:**
可以引用
---

### Round 2

**Q1（回答你的域名问题）：** Cloudflare 确实可以直接注册新域名（Cloudflare Registrar），按批发价、免费 WHOIS 隐私保护，但支持的后缀有限，且新手第一次通常还没有 Cloudflare 账号里已有域名的概念。本博客实际走的是「GoDaddy（或其他任意注册商）买域名 → 域名的 Nameserver 改指到 Cloudflare」这条路，更通用、适合大多数常见后缀。建议教程按**本博客真实路径**写：域名可以在任意注册商购买（以 GoDaddy 为例），DNS 换到 Cloudflare；同时用一句话提一下"Cloudflare Registrar 也可以直接买，但后缀有限"作为备选。这样处理可以吗？

**A:**
可以
**Q2（模块划分确认）：** 按你说的"先基础后进阶"，我梳理了本博客实际用到的技术栈，草拟分组如下，请确认或调整：

- **基础模块**（从 0 到能访问、能发文章）：域名购买 → DNS 切到 Cloudflare → 本地装 Hugo + 选主题（以 PaperMod 为例）→ 写第一篇文章 → GitHub 建仓库 → Cloudflare Pages 连接仓库并设置构建命令（`hugo --minify`，产物目录 `public`）→ 绑定自定义域名
- **进阶模块**：Pagefind 全文搜索、Giscus 评论（基于 GitHub Discussions）、访问统计（Umami + Cloudflare Web Analytics）、Page Bundle 图片管理
- **可选 / 不建议写入**（本博客有但对新手意义不大，除非你想要）：`Taskfile.yml`/go-task 本地命令封装、`Containerfile`/nerdctl 容器化本地预览、OpenTofu 管理 Cloudflare Pages 项目（IaC）

这个分组可以吗？"可选"部分要不要也写（哪怕简短提一句"进阶到这个程度可以了解一下"）？

**A:**
“OpenTofu 管理 Cloudflare Pages 项目（IaC）” 这个要写
**Q3（篇幅与拆分）：** 把基础 + 进阶全部技术栈写进一篇，预估篇幅会明显超过 800 行（单篇偏长的经验阈值）。是否按 hub 模式拆成"母文 + 子文"，例如：母文《Hugo + Cloudflare Pages 搭建个人博客》讲基础模块并总览进阶模块，进阶的每个技术点（搜索/评论/统计）各链接到本博客已有的对应文章（[hugo-static-site-search.md](../../content/post/web/hugo-static-site-search.md)、[giscus.md](../../content/post/development/giscus.md)、[web-analytics.md](../../content/post/cs/web-analytics.md)）？还是希望这篇是一篇独立自足的教程，不依赖跳转到其他文章？

**A:**
使用母文，子文结构
**Q4（本地预览工具）：** 教程里演示"本地预览效果"这一步，用最简单的 `hugo server` 命令，还是也要讲本博客实际用的 `task preview`（封装了 nerdctl 容器）？新手大概率没有 nerdctl/go-task 环境，简单版可能更友好。

**A:**
写简单版本
最后再写一下本 blog 的源码是在 github上的公开仓库，可以参考。

---

### Round 3

**Q（OpenTofu 子文的处理方式）：** 你要写"OpenTofu 管理 Cloudflare Pages 项目"这个进阶模块，但本博客目前没有对应文章——现有 [opentofu.md](../../content/post/cloud/opentofu.md) 讲的是 AWS VPC/EC2 通用入门，不是 Cloudflare Pages 场景。有两种处理方式：

1. **这次一起做**：本 Spec 顺带新开一篇子文 Spec（如 `content/post/cloud/cloudflare-pages-opentofu.md`），母文和子文一起产出。
2. **母文先发，子文后补**：母文里进阶概览段落先简要写清楚"用 OpenTofu 管理 Cloudflare Pages 项目"的思路和示例代码片段（不单独成文、不需要新 Spec），把它当成母文的一个小节而不是链接子文；以后想扩展再拆出来。

你倾向哪种？如果选 1，子文的 url / 分类按你意见定，还是按我提议的 `cloudflare-pages-opentofu`（分类 `cloud`）？

**A:**
opentofu的文档需要拆分吗？ 比如拆分出一个基础文档（跟aws,cloudflare都 无关 的）再关联其它文档opentofu管理aws, opentofu管理 cloudflare, 还是保持现有的？

---

### Round 4

**Q（回答你关于拆分 opentofu.md 的问题）：** 不建议现在拆。原因：

1. **`opentofu.md` 已发布，且已被 5 篇文章引用**（`aws-lambda.md`、`cloudwatch.md`、`eventbridge-scheduler.md`、`sns.md`、`sqs.md` 都链接它作为"OpenTofu 通用概念"出处）。拆成"基础 + AWS + Cloudflare"三篇，意味着要改 url、改这 5 篇的内链，是一次独立的重构任务，和"写一篇教程文章"这个目标不是一回事，风险和工作量都不小。
2. 现有 `opentofu.md` 里 Provider / Resource / Data Source 这些概念本来就是通用的（不特定于 AWS），只是标题和 url 带了 `aws-vpc-ec2`——**内容其实已经具备"基础概念"的部分**，不拆也能被新文章引用。
3. 按 [doc-length-and-split.md](../doc-length-and-split.md) 的原则，拆分要"作者确认后再执行"，且通常是因为**单篇过长或明显混杂多主题**才拆；现在的动机是"想新增一个 Cloudflare 场景"，不是"现有文章太长/太杂"，不满足拆分触发条件。

**建议做法**：保持 `opentofu.md` 不动，新建一篇 `content/post/cloud/cloudflare-pages-opentofu.md`（分类 `cloud`），开头一两句概念性内容直接链接回 `opentofu.md`（"Provider / Resource 等基础概念见 xxx"），正文只讲 Cloudflare Provider 管理 Pages 项目、自定义域名、DNS 记录的具体做法。这样不用动现有文章和它的 5 处引用，新文章也不会重复造轮子。

这个方案可以吗？如果可以，我就按这个来写子文 Spec；如果你还是想现在就拆分 `opentofu.md`，我们可以另开一个独立的重构 Spec 来做（不在这篇教程 Spec 里）。

**A:**
按你的建议做
---

## C. 批注

---

## 变更记录

| 日期       | 变更 |
| ---------- | ---- |
| 2026-07-09 | 初版 |
