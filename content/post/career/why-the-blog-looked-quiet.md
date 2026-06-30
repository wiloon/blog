---
title: "Why the Blog Looked Quiet 一次构建失败导致的「假性停更」"
author: "-"
date: 2026-06-30T14:46:12+08:00
lastmod: 2026-06-30T14:46:12+08:00
url: why-the-blog-looked-quiet
categories:
  - career
tags:
  - career
  - hugo
  - cloudflare
  - original
  - AI-assisted
---

本文是一条故障记录。

最近两天 wiloon.com 看起来像是“停更”，停在6月28号。但其实 blog 仓库是有更新的，也提交了，只是没能发布出来——博客有大约两天卡在一次构建失败上，而我自己一直不知道。

## 不是停更，是没发布出去

现象很简单：本地写好、`git push` 之后，wiloon.com 上看不到新内容。一开始我以为是 CDN 缓存或者部署延迟，没太在意。后来才发现是构建一直在失败——新提交根本没被发布出去。

## 怎么坏的

原因是文章标题里的一个冒号。

博客用 Hugo，文章开头的 front matter 是一段 YAML。我有几篇 Java/Spring 的文章标题是英中混写的，里面带了「冒号 + 空格」，比如：

```yaml
# breaks the build: ": " makes YAML parse it as a mapping
title: Spring WebFlux: 响应式 Web 框架
```

在 YAML 里，`: `（冒号加空格）是 key/value 的分隔符。没加引号时，解析器会把这一行当成一个嵌套映射来读，于是报错、Hugo 构建中止。一篇的 front matter 解析失败，整站就一个页面都不生成。

修复其实只要把整个标题值用引号包起来：

```yaml
# fixed: quote the whole value so the colon is just text
title: "Spring WebFlux: 响应式 Web 框架"
```

加上引号之后，构建立刻就恢复了。

## 本以为能只跳过出错的那篇

我一开始以为 Hugo 能配置成「只跳过解析失败的那篇、其它照常渲染」，查了一下资料，结果发现并不能：任何一篇坏掉，都会让整站构建中止，一个页面都不生成。`ignoreFiles` 也救不了——Hugo 是先解析完所有内容、再应用忽略规则，这点在 Hugo 仓库的 [issue #10303](https://github.com/gohugoio/hugo/issues/10303) 里有维护者确认过（标题就是“Hugo parses all content files, regardless of ignoreFiles status, and fails build if parsing fails”，并附了可复现的例子）。

我又了解了一下 fail-fast 是怎么回事，才弄明白它为什么有道理。它把整站当成一次编译产物，页面之间有列表、分类、交叉引用这些依赖，都要读每篇的 front matter。如果允许「跳过坏页、其它正常渲染」，结果可能是列表悄悄少一篇、分类计数不对、引用断裂，而构建却显示成功——这种「静默残缺」比直接报错更难发现。所以它选择 [fail-fast](../pattern/fail-fast.md)：一篇坏就当语法错误、整站停下，和编译器遇到语法错误就罢工是一个道理。代价就是这次的「一篇标题写错，全站都不更新」。

## 为什么我没第一时间发现

坏就坏在这次失败是「静默」的。

博客托管在 Cloudflare Pages，构建命令跑 `hugo`。Cloudflare Pages 有一个行为：当一次构建失败时，它会保留上一次成功的部署。也就是说，站点照常能访问、域名解析正常、页面也不报错——只是内容停在上一次成功构建的旧版本。

从外面看，wiloon.com 一切正常，没有 502、没有报错页。它只是不更新而已。我这边也没有任何提示，构建在后台默默失败了两天（大概是 6 月 28 日到 6 月 30 日），我才偶然发现新文档一直没上线。

对一个高频更新的站点，这种问题可能几分钟就被发现；但对一个更新本来就稀疏、读者也少的博客，「静默失败 + 保留旧版本」刚好凑成了一个很难察觉的组合——看起来就像我停更了。

## 事后做的两件事

修好构建只是把当下的问题解决了。我更在意的是下次怎么不再这样，于是做了两件事。

### 一是在博客的 AI docs 里加约束

我平时用 AI 辅助改博客，仓库里有一份给 AI 看的约定（`AGENTS.md`）。这次我把「标题含冒号要加引号」这条写进去了，并附了一条自查命令，用来扫出「带 `: ` 但没加引号」的标题：

```bash
# list titles that contain ": " but are not wrapped in quotes
rg -n --pcre2 '^title: (?!["\x27]).*: ' content/ -g '*.md'
```

这样无论是我自己还是 AI 改稿，写出会让构建挂掉的标题之前，规则和检查都摆在那里，提交前能先扫一遍。

### 二是给构建失败加邮件通知

光靠「别写错」不够，还得让万一真失败(其它异常)时我能第一时间知道，而不是再静默两天。

Cloudflare Pages 本身支持部署事件通知。我用 OpenTofu 把它写成了配置的一部分——加了一条通知策略，在生产环境部署失败时给我发邮件：

```hcl
# alert by email when a production deployment fails
resource "cloudflare_notification_policy" "pages_build_failed" {
  name       = "Pages production deployment failed"
  enabled    = true
  alert_type = "pages_event_alert"

  filters {
    environment = ["ENVIRONMENT_PRODUCTION"]
    event       = ["EVENT_DEPLOYMENT_FAILED"]
  }
}
```

以前构建失败时站点照常、毫无动静，只能靠自己偶然发现；现在下次一失败，我就会立刻收到一封邮件，能马上去处理，而不是让它静默卡在旧版本。

其实「怎么知道构建失败了」有好几个做法，我比较了三个：

- 邮件告警（最后选的这个）：不用多跑任何构建，失败了就收到邮件。代价是它在失败之后才提醒——问题已经发生、也已经推上去了，属于「快速知道」而不是「提前拦住」，但对这个低频更新的小博客够用了。
- 让 GitHub Actions 再编译一遍做检查：这其实是 AI 给我推荐的方案，理由是成本低、也方便——GitHub Actions 构建失败默认就会发邮件通知，不用我额外配。但它相当于在 Cloudflare 之外再跑一次构建，和 Cloudflare 的构建重复、白费算力，更要紧的是要我多维护一套 Actions 配置，平添维护成本，我不想为它多维护一条重复的流水线。
- 提交前在本地先编译一次：这是最早能拦住问题的做法，push 前就能发现。但我本地提交很频繁(平时查资料,学习新东西的时候会频繁提交)，本机性能又一般，编译一次要等挺久，「频繁本地构建 + 长时间等待」不是我想要的，所以哪怕它暴露得最早也放弃了。

最后没选 AI 推荐的 GitHub 那个，挑了邮件告警，是因为它在「不增加重复构建、不拖慢我提交节奏」的前提下，把「静默失败」解决了——让失败从「没人知道」变成「立刻知道」。它不是理论上最早暴露问题的那个，但在我现在的工作流里成本最低、也最省心。
