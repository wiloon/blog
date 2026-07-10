---
title: "Cloudflare Pages with OpenTofu: 用 IaC 管理 Pages 项目"
author: "-"
date: 2026-07-09T23:44:19+08:00
lastmod: 2026-07-09T23:44:19+08:00
url: cloudflare-pages-opentofu
categories:
  - cloud
tags:
  - opentofu
  - cloudflare
  - IaC
  - original
  - AI-assisted
---

在 Cloudflare 后台点几下就能建好一个 Pages 项目、绑好域名。想把这些配置变成可版本化、可复现的代码，就用 OpenTofu 来管理。本文只讲 Cloudflare 场景的具体写法，Provider、Resource、State 这些基础概念见 [OpenTofu 入门](./opentofu.md)。

## 目标

用 OpenTofu 声明式地管理三样东西：

- 一个连接 GitHub 仓库的 Cloudflare Pages 项目（含构建命令、产物目录、环境变量）
- 项目绑定的自定义域名
- 指向 Pages 的 DNS 记录

## 准备

需要两个 Cloudflare 侧的标识和一个 API Token：

| 变量       | 从哪来                                                                 |
| ---------- | ---------------------------------------------------------------------- |
| Account ID | Cloudflare 后台任意页面右侧栏，或 Workers & Pages 概览页               |
| Zone ID    | 域名的 Overview 页面右侧栏                                             |
| API Token  | My Profile → API Tokens → Create Token，授予 Pages 编辑和 DNS 编辑权限 |

Token 属于机密，不要写进代码，用环境变量注入：

```bash
export TF_VAR_cloudflare_api_token="your-token-here"
```

## Provider 配置

```hcl
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4"
    }
  }
}

variable "cloudflare_api_token" {
  type      = string
  sensitive = true
}

variable "account_id" {
  type = string
}

variable "zone_id" {
  type = string
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}
```

## Pages 项目

`cloudflare_pages_project` 对应后台的一个 Pages 项目，`source` 块声明连接哪个 GitHub 仓库，`build_config` 对应构建命令和产物目录，`deployment_configs` 里可以设环境变量（例如 `HUGO_VERSION`）。

```hcl
resource "cloudflare_pages_project" "blog" {
  account_id        = var.account_id
  name              = "blog"
  production_branch = "main"

  source {
    type = "github"
    config {
      owner             = "wiloon"
      repo_name         = "blog"
      production_branch = "main"
    }
  }

  build_config {
    build_command   = "hugo --minify"
    destination_dir = "public"
  }

  deployment_configs {
    production {
      # keep Cloudflare's Hugo in sync with local
      environment_variables = {
        HUGO_VERSION = "0.159.1"
      }
    }
  }
}
```

## 自定义域名与 DNS 记录

`cloudflare_pages_domain` 把域名挂到 Pages 项目上，`cloudflare_record` 添加指向项目 `pages.dev` 子域的 CNAME 记录，`proxied = true` 让流量走 Cloudflare 的 CDN。

```hcl
resource "cloudflare_pages_domain" "blog" {
  account_id   = var.account_id
  project_name = cloudflare_pages_project.blog.name
  domain       = "wiloon.com"
}

resource "cloudflare_record" "blog" {
  zone_id = var.zone_id
  name    = "@"
  type    = "CNAME"
  content = cloudflare_pages_project.blog.subdomain
  proxied = true
}
```

## 应用

```bash
tofu init
tofu plan
tofu apply
```

`tofu plan` 会列出将要创建的资源，确认无误后 `tofu apply` 执行。之后这套 Pages 配置就由 state 文件追踪，改配置改代码、重新 `apply` 即可，不用再回后台手点。

## 说明

Cloudflare Provider 的资源名和字段在不同大版本间会有调整（例如 v5 对部分资源做了重命名），实际使用时以所锁定版本的 [官方文档](https://registry.terraform.io/providers/cloudflare/cloudflare/latest/docs) 为准。上面的示例基于 v4。
