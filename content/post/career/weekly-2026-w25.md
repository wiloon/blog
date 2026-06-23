---
title: 2026 W25
author: "-"
date: 2026-06-21T23:59:59+08:00
lastmod: 2026-06-23T10:55:35+08:00
url: weekly-2026-w25
categories:
  - career
tags:
  - weekly
  - resume
  - java
  - enx
  - original
  - AI-assisted
---

本周一（6 月 16 日）补写了 [2026 W24 周记](./weekly-2026-w24.md)。下面记 W25 自己的事。

## 投递邀请与简历准备

6 月 15 日收到一份投递简历的邀请。我打算这周主要修改简历和可能的面试准备，homelab 改造、公司刻章之类都先往后放。

写简历时沿用平时写代码、写 blog 用的 SDD 思路：先和 AI 写一份 spec，对照旧简历与新职位描述列出差异；再按差异到个人 profile 里挖过往项目的故事；回到 spec 标注每条差异可以引用哪些素材；最后让 AI 根据 spec 生成新一版简历。因为此前投过类似方向的岗位，很多段落可以复用，这个流程既有结构又省时间。6 月 17 日跟前同事聊 AI 用法时，才突然意识到 SDD 不只适用于代码和文章——简历同样适用。

挖素材的过程中，我把一些早年做过但没在简历里展开的项目重新整理成文，例如 [车联网平台第三方数据推送集成](./iot-third-party-data-push.md)。有些事只是做过、学过，和跟别人讲过一次之后，大脑里留下的关联是不一样的；输出过一遍，需要的时候更容易想起来。

PDF 导出是另一条线。以前用 VS Code / Cursor 的 Preview 在浏览器里打开再打印 PDF，软件更新后这条路走不通了。跟 AI 聊了几轮，第一次正经用排版工具链：Markdown 经 Pandoc + XeLaTeX 出 PDF，定制了 LaTeX 模板和一键脚本。流程稳定后另写了一篇技术记录：[Markdown to PDF: Pandoc + XeLaTeX 简历导出实践](../development/markdown-to-pdf-pandoc-xelatex.md)。

看职位描述时还记下一个概念 Speed over Perfection，顺手写进了 [agile 笔记](../cs/agile.md)。

## 梳理 Java 文档

简历主体定稿后，重心转到 blog 里攒了很久的 Java 笔记。这次投的是 Java 方向，正好借机把零散文章理顺：拆大篇、补版本脉络、把 JVM 和 HotSpot 分开写。日历上这几天和简历收尾有重叠，但主线已经换成「整理文档」。

周记里不展开具体技术点，只列几篇本周动过的代表文章，方便以后自己回溯：

- [Java 知识地图](../language/java/java-knowledge-map.md)（总览）
- [Java 版本史](../language/java/java-version-history.md)（版本脉络）
- [JVM](../language/java/jvm.md)（运行时）
- [GraalVM](../language/java/graalvm.md)（本周新拆的一篇）

## enx：Cognito 合入与 Java 后端方向

梳理文档的过程中，我越来越觉得光看文章不够，得有个项目动手练。enx 是个人用的 playground，正好打算加一个 Java 后端，和正在看的 Java 职位也能对齐。

在此之前，enx 仓库里有一条分叉很久的 Cognito / 邮箱注册分支。若直接开 Java 后端，以后合并会更麻烦。周末先花时间把这条分支测到可用，合进 main，再在 Homelab 里把 enx-api、enx-ui 的构建和部署跑通。部署细节见 [enx-api 在 Homelab 的构建与部署](../cloud/enx-api-homelab-cicd.md)。

合入并部署完成后，Java 后端的方向就定了下来：在 enx 里开新分支做实现。脚手架和 k8s 落地是 6 月 22 日之后的事，留到 W26 周记再写。

## Homelab 与其它

简历仍是本周主轴，但有几处零星维护：6 月 18 日在集群里加了 descheduler；内外网域名分离的方案写了一大版 spec，因这周时间紧先搁置；公司刻章也推到下周。一人公司相关的日常运营文档（跑步、时间分配之类）打算以后在 blog 上挂个链入口，这次还没动。

## 输出与记忆

SDD 用在简历上的这次经历，又印证了一件事：输入、操作和「组织语言说出来」会在记忆里留下不同的痕迹。我早就在用 SDD 写代码和 blog，却直到跟人聊完才想到简历也可以走同一套。以后还是得多记录、多跟人聊新工具和新概念，需要的时候才捞得起来。

但愿这个新机会能顺利。
