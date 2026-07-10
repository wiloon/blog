---
title: Hugo + Cloudflare Pages 搭建个人博客
author: "-"
date: 2026-07-09T23:44:19+08:00
lastmod: 2026-07-09T23:44:19+08:00
url: hugo-cloudflare-pages-blog-setup
categories:
  - web
tags:
  - hugo
  - cloudflare
  - dns
  - cdn
  - github
  - remix
  - AI-assisted
---

本文记录这个博客的搭建方式，从买域名到发布一个静态站点。技术选型和步骤与本站的实现保持一致。

## 这套技术栈长什么样

一句话概览：用 Hugo 把 Markdown 编译成静态页面，源码在 GitHub，Cloudflare Pages 连接 GitHub 仓库并在 Cloudflare 侧构建、托管，域名解析和 CDN 也在 Cloudflare。

各部分的分工：

| 组件             | 作用                                                    |
| ---------------- | ------------------------------------------------------- |
| Hugo             | 静态站点生成器，把 `content/` 下的 Markdown 编译成 HTML |
| GitHub           | 存放源码，作为部署的触发源                              |
| Cloudflare Pages | 连接 GitHub 仓库，执行 `hugo --minify` 构建并托管产物   |
| Cloudflare DNS   | 域名解析，把自定义域名指向 Pages 项目                   |
| Cloudflare CDN   | 边缘缓存与加速，Pages 默认自带                          |

整个流程没有用 GitHub Actions，也没有容器化构建，构建这一步完全由 Cloudflare Pages 在它自己的环境里完成。基础站点的构建命令就是一句 `hugo --minify`；本站为了顺带生成搜索索引，把它包成了一个很短的脚本（见下文进阶模块），思路一样。

## 基础模块

这一部分从 0 到「能访问」。

### 买域名

域名可以在任意注册商购买，我最早是在 GoDaddy 买的。以 GoDaddy 为例：

1. 打开 [godaddy.com](https://www.godaddy.com/)，在搜索框里输入想要的域名，看是否可注册。
2. 选一个后缀（`.com`、`.dev` 等），加入购物车，结账。注意第一年常有促销价，续费价通常更高，下单前看清续费价格。
3. 结账时可关掉 GoDaddy 自家的一堆增值服务（邮箱、隐私保护等），后面把 DNS 切到 Cloudflare 后这些大多用不上。

Cloudflare 自己也能直接注册域名（Cloudflare Registrar，按批发价、免费 WHOIS 隐私保护），但支持的后缀有限。如果想要的后缀在它的列表里，直接在 Cloudflare 买、省去后面改 Nameserver 的步骤也可以；后缀不在列表里就按上面的思路在别的注册商买，再把 DNS 切过来。

### 把 DNS 切到 Cloudflare

在别处买的域名，要把解析交给 Cloudflare，做法是修改域名的 Nameserver。

1. 注册并登录 [Cloudflare](https://dash.cloudflare.com/)，点 Add a site，输入自己的域名。
2. 选免费计划（Free）。Cloudflare 会扫描现有 DNS 记录并列出来，确认无误后继续。
3. Cloudflare 会给出两个它分配的 Nameserver，形如 `xxx.ns.cloudflare.com`。
4. 回到 GoDaddy 的域名管理页，找到 Nameservers 设置，改成 Cloudflare 给的这两个。
5. 保存后等待生效，通常几分钟到几小时。Cloudflare 上域名状态变成 Active 就表示接管成功。

之后这个域名的所有解析记录都在 Cloudflare 后台管理。

### 本地安装 Hugo 并选主题

Hugo 是单个二进制文件，安装很简单。注意要装 extended 版本（支持 SCSS，很多主题需要）。

```bash
# macOS
brew install hugo

# Arch Linux
sudo pacman -S hugo

# 其他平台可从 GitHub Releases 下载 hugo_extended 二进制
hugo version
```

新建一个站点骨架并初始化 git：

```bash
hugo new site myblog
cd myblog
git init
```

主题的安装方式各不相同，通用做法是把主题作为 git submodule 放到 `themes/` 目录下，再在配置里指定。这里以 PaperMod 为例（本站用的就是它）：

```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

然后在站点配置里指定主题。Hugo 支持 `hugo.toml` / `config.toml` 等文件，本站用的是 `config.toml`：

```toml
baseURL = "https://example.com/"
languageCode = "en"
title = "My Blog"
theme = "PaperMod"
```

换其他主题时，步骤类似：读一遍主题仓库的 README，按它说的方式装（submodule 或 Hugo Modules），把 `theme` 改成对应名字，再把主题示例里的配置项抄进自己的配置文件。

### 写第一篇文章并本地预览

用 Hugo 命令生成一篇文章：

```bash
hugo new content/post/hello-world.md
```

打开 `content/post/hello-world.md`，会看到一段 front matter。把 `draft` 改成 `false`，正文随便写点内容：

```markdown
---
title: "Hello World"
date: 2026-07-09T10:00:00+08:00
draft: false
---

Hello World!
```

本地预览用 Hugo 自带的开发服务器：

```bash
hugo server -D
```

`-D` 表示同时渲染草稿。命令跑起来后，浏览器打开 `http://localhost:1313/` 就能看到站点，改动文件会自动刷新。确认页面正常后按 `Ctrl+C` 停掉。

### 在 GitHub 建仓库并推送

在 GitHub 上新建一个空仓库（可以是 public 也可以是 private，Cloudflare Pages 两种都支持授权）。然后把本地代码推上去：

```bash
git add .
git commit -m "init blog"
git branch -M main
git remote add origin git@github.com:yourname/blog.git
git push -u origin main
```

因为主题是 submodule，`git push` 会把 `.gitmodules` 一起推上去，Cloudflare 构建时会自动拉取子模块。

### 用 Cloudflare Pages 连接仓库并构建

1. 进入 Cloudflare 后台，左侧选 Workers & Pages，点 Create，切到 Pages 标签，选 Connect to Git。
2. 授权 Cloudflare 访问 GitHub，选中刚才那个仓库。
3. 在构建设置里：
   - Framework preset 选 Hugo（选了它会自动填好下面两项）。
   - Build command 填 `hugo --minify`。
   - Build output directory 填 `public`。
4. 展开环境变量，加一个 `HUGO_VERSION`，值填本地 `hugo version` 输出的版本号（例如 `0.159.1`）。不指定的话 Cloudflare 会用一个较旧的默认版本，容易和本地构建结果不一致。
5. 点 Save and Deploy。Cloudflare 会拉取仓库、跑 `hugo --minify`、把 `public` 目录部署上去。

首次部署成功后，会分配一个 `xxx.pages.dev` 的临时域名，打开就能看到站点。之后每次 `git push` 到 `main`，Cloudflare 都会自动重新构建部署。

### 绑定自定义域名

1. 在这个 Pages 项目里打开 Custom domains，点 Set up a custom domain，填自己的域名（例如 `wiloon.com`）。
2. 因为域名的 DNS 已经在 Cloudflare 托管，它会自动添加对应的 CNAME 记录并签发证书，不用手动配。
3. 等状态变成 Active，用自己的域名访问就能打开博客，HTTPS 和 CDN 都是默认开好的。

到这里，一个能访问、能持续写文章的博客就搭好了：写完新文章 `git push`，几十秒后线上就更新了。

## 进阶模块

基础站点跑起来后，可以按需接入下面这些能力。每一项本站都有单独一篇文章讲具体接入方式，这里只做概览。

### 全文搜索（Pagefind）

静态站没有后端，站内搜索要么把全文索引塞进浏览器（Fuse.js，文章一多首访就慢），要么用 Pagefind——构建时生成分片索引，搜索时按查询按需加载，extended 版本还支持中文分词。本站文档量较大，用的是 Pagefind。因为 Pagefind 要在 Hugo 之后再跑一步，本站把 Cloudflare 的构建命令从裸 `hugo --minify` 换成了一个小脚本 `build.sh`（先 `hugo --minify` 再跑 Pagefind 生成索引）。接入细节见 [Hugo Static Site Search](./hugo-static-site-search.md)。

### 评论系统（Giscus）

Giscus 基于 GitHub Discussions，评论数据完全存在 GitHub，不需要额外数据库或第三方平台，很适合 Cloudflare Pages 这类静态托管。它把每个页面映射到一个 Discussion，页面里嵌一段 `<script>` 就能加载评论组件。接入细节见 [Giscus 评论系统](../development/giscus.md)。

### 访问统计（Umami + Cloudflare Web Analytics）

Hugo + PaperMod 默认没有访问统计。本站同时接了两套：Umami（无 cookie、隐私友好，数据在 Umami 服务器）和 Cloudflare Web Analytics（和 Cloudflare 基础设施集成，数据在 Cloudflare），两者不冲突，可对比数据。接入细节见 [网站访问统计](../cs/web-analytics.md)。

### 用 OpenTofu 管理 Pages 项目（IaC）

前面绑域名、配构建、加环境变量这些都是在 Cloudflare 后台点出来的。想把这些配置变成可版本化、可复现的代码，可以用 OpenTofu（Terraform 的开源分支）以声明式的方式管理 Pages 项目、自定义域名和 DNS 记录。具体的 Provider 配置和资源写法见 [用 OpenTofu 管理 Cloudflare Pages](../cloud/cloudflare-pages-opentofu.md)。

## 源码参考

本站源码是 GitHub 上的公开仓库 [github.com/wiloon/blog](https://github.com/wiloon/blog)，上面这套配置（Hugo 配置、PaperMod submodule、Cloudflare Pages 构建设置对应的目录结构）都能直接翻到，搭建时可以对照参考。
