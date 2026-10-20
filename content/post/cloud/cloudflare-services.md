---
title: "Cloudflare Services: Cloudflare 服务一览、R2 对象存储与 Tunnel"
author: "-"
date: 2026-10-14T21:28:59+08:00
lastmod: 2026-10-20T06:41:47+08:00
url: cloudflare-services
categories:
  - cloud
tags:
  - cloudflare
  - r2
  - object-storage
  - cdn
  - opentofu
  - cloudflare-tunnel
  - homelab
  - remix
  - AI-assisted
---

Cloudflare 起家是 CDN 和 DNS，现在的产品线已经覆盖网络、安全、开发者平台和存储。这篇先按用途列一遍常用服务，再单独讲 R2 对象存储和 Tunnel。各服务的额度和价格会调整，以官方文档为准（本文核对于 2026-10）。

## 服务一览

### 网络与安全

| 服务 | 说明 |
| --- | --- |
| DNS | 权威 DNS，免费。域名的 NS 指到 Cloudflare 以后，其他服务才能接上 |
| CDN / 代理 | DNS 记录打开代理（橙色云朵）后，流量先经过 Cloudflare 边缘节点，静态内容在边缘缓存 |
| SSL/TLS | 边缘证书自动签发；回源可用 Origin CA 证书（只被 Cloudflare 信任，有效期最长 15 年），模式应选 Full (strict) |
| WAF / DDoS 防护 | 代理开着时自动生效，免费版有基础规则 |
| Turnstile | 人机验证，替代 reCAPTCHA，免费 |
| Registrar | 域名注册，按成本价续费，不加价 |

### 开发者平台

| 服务 | 说明 |
| --- | --- |
| Pages | 静态站点和前端项目托管，连 Git 仓库自动构建，见 [Hugo + Cloudflare Pages 搭建个人博客](../web/hugo-cloudflare-pages-blog-setup.md) |
| Workers | 边缘 Serverless 运行环境，见 [Cloudflare Workers](./cloudflare-workers.md) |
| KV | 全球分布的键值存储，读多写少，最终一致 |
| D1 | 基于 SQLite 的关系型数据库 |
| R2 | 对象存储，兼容 S3 API，没有出口流量费，见下文 |
| Durable Objects | 带强一致状态的单实例对象，适合协同编辑、计数、WebSocket |
| Queues | 消息队列 |
| Workers AI | 在边缘调用推理模型 |

KV、D1、R2、Durable Objects、Queues 都可以通过 binding 注入 Worker 使用。

### 其他

| 服务 | 说明 |
| --- | --- |
| Email Routing | 把 `name@你的域名` 转发到真实邮箱，只转发不存储，免费 |
| Web Analytics | 不用 Cookie 的访问统计，免费 |
| Tunnel | 内网服务不开公网端口，由 `cloudflared` 主动连到 Cloudflare 后对外提供访问，见下文 |
| Access | 在应用前面加一层身份认证（Zero Trust） |

这些服务大多能用 OpenTofu / Terraform 的 `cloudflare/cloudflare` provider 管理，Pages 的例子见 [Cloudflare Pages with OpenTofu](./cloudflare-pages-opentofu.md)。

## R2 对象存储

### R2 是什么

R2 是 Cloudflare 的对象存储，按桶（bucket）存文件（object），接口兼容 S3 API，现有的 S3 工具和 SDK 改一下 endpoint 就能用。

和 AWS S3 最大的区别是**没有出口流量费**：S3 按下载流量收费，放一个经常被下载的视频或安装包，流量费往往比存储费高得多；R2 只收存储费和请求次数费，下载多少都不另外收钱。

### 价格和免费额度

R2 把请求分成两类：

- **Class A**：写入和列举类操作，如 `PutObject`、`ListObjects`、分片上传
- **Class B**：读取类操作，如 `GetObject`、`HeadObject`

| 项目 | 免费额度（每月） | Standard | Infrequent Access |
| --- | --- | --- | --- |
| 存储 | 10 GB-month | $0.015 / GB-month | $0.01 / GB-month |
| Class A | 100 万次 | $4.50 / 百万次 | $9.00 / 百万次 |
| Class B | 1000 万次 | $0.36 / 百万次 | $0.90 / 百万次 |
| 取回数据 | 不需要额度：Standard 本来就不收 | 不收 | $0.01 / GB |
| 出口流量 | 不需要额度：本来就不收，也不限量 | 不收，不限量 | 不收，不限量 |

免费额度只适用于 Standard 存储类。对 Standard 来说，取回数据和出口流量都不收费，所以真正可能产生费用的只有超出免费额度的存储量和请求次数。Infrequent Access 适合很少读取的归档数据，最短计费 30 天，提前删除也按 30 天收费。

通过自定义域名访问时，命中 Cloudflare 缓存的请求不会回到 R2，也就不计 Class B 次数。

### 公开访问的两种方式

桶默认是私有的，只能用 API 密钥访问。要让浏览器直接下载，有两种方式：

| 方式 | 地址形式 | 说明 |
| --- | --- | --- |
| r2.dev 子域名 | `https://pub-<hash>.r2.dev/<key>` | 一键打开，有速率限制，不走缓存，只适合开发测试 |
| 自定义域名 | `https://media.example.com/<key>` | 域名必须托管在同一个 Cloudflare 账号下；走 Cloudflare CDN 缓存，可以配缓存和 WAF 规则，生产用这个 |

### 用 OpenTofu 创建桶和自定义域名

cloudflare provider 5.x 里对应 `cloudflare_r2_bucket` 和 `cloudflare_r2_custom_domain`：

```hcl
resource "cloudflare_r2_bucket" "media" {
  account_id = var.cloudflare_account_id
  name       = "example-media"
  # Location hint: where most readers are ("apac", "enam", "weur", ...)
  location = "apac"
}

# Public access at media.example.com, served through the Cloudflare cache.
# Cloudflare creates the DNS record for this domain itself.
resource "cloudflare_r2_custom_domain" "media" {
  account_id  = var.cloudflare_account_id
  bucket_name = cloudflare_r2_bucket.media.name
  zone_id     = var.zone_id
  domain      = "media.example.com"
  enabled     = true
  min_tls     = "1.2"
}
```

API Token 需要账号级的 **Workers R2 Storage: Edit** 权限，只有 Zone 权限的 token 会返回 403。

### 上传文件

用 wrangler（Cloudflare 官方 CLI）：

```bash
# Upload one object; --remote targets the real bucket, not the local emulator
wrangler r2 object put example-media/demo-v1.mp4 \
  --file demo.mp4 \
  --content-type video/mp4 \
  --cache-control "public, max-age=31536000, immutable" \
  --remote
```

或者用 AWS CLI 走 S3 兼容接口。先在 R2 页面创建 API Token，拿到 Access Key ID 和 Secret Access Key：

```bash
# R2 S3 endpoint is per account; region is always "auto"
aws s3 cp demo.mp4 s3://example-media/demo-v1.mp4 \
  --endpoint-url "https://<account_id>.r2.cloudflarestorage.com" \
  --region auto \
  --content-type video/mp4 \
  --cache-control "public, max-age=31536000, immutable"
```

`Content-Type` 和 `Cache-Control` 存在对象的元数据里，下载时原样返回，所以上传时就要设对。

### 适合放什么

- **网页里的视频、大图、安装包**：下载多、体积大，没有出口费的好处最明显
- **备份和归档**：配合 Infrequent Access 存储类
- **用户上传的文件**：后端生成预签名 URL（presigned URL），浏览器直接传到 R2，不经过自己的服务器

不适合放会被频繁小粒度修改的数据，那是数据库或 KV 的场景。

### 用法要点

- **文件名带版本号，缓存设成 immutable**。比如 `demo-v1.mp4`，更新时上传 `demo-v2.mp4` 并改引用地址，不用清缓存，也不会出现新旧版本混在缓存里
- **视频直接用 `<video>` 播放即可**。R2 支持 Range 请求，浏览器可以边下边播、拖动进度条
- **CORS 只在 JS 读取时需要**。`<video>`、`<img>` 直接引用不需要配 CORS；用 `fetch()` 读取或浏览器直传时，要给桶配 CORS 规则（`cloudflare_r2_bucket_cors`）
- **从 S3 迁移**：R2 提供 Super Slurper（一次性整体迁移）和 Sippy（访问时按需从 S3 拉取）

## Cloudflare Tunnel

### 解决什么问题

家里或公司内网的服务想让公网访问，传统做法是：路由器上做端口转发，再用 DDNS 把域名指向家里的出口 IP。这条路常常走不通，或者不想走：

- **没有公网 IP**：很多宽带是运营商级 NAT（CGNAT），端口转发根本没用
- **不想开入站端口**：开了端口，整个互联网都能扫到这台机器
- **出口 IP 会变、会暴露**：DDNS 有更新延迟，而且别人一查域名就知道你家的 IP

Tunnel 把方向反过来：内网里跑一个 `cloudflared` 进程，由它**主动向外**连到 Cloudflare。公网用户访问域名时，请求先到 Cloudflare 边缘节点，再顺着这条已经建好的连接送回内网。路由器上不用开任何入站端口，源站 IP 也不会暴露。免费版就能用。

### 工作原理

```text
browser ──HTTPS──> Cloudflare edge ──(existing tunnel)──> cloudflared ──> http://localhost:8080
                                       ^
                                       └─ cloudflared dialed out, port 7844
```

- `cloudflared` 启动后向 Cloudflare 的 7844 端口建立几条长连接（QUIC，走不通时退回基于 TCP 的 HTTP/2），分布在至少两个数据中心，单条断了不影响服务
- 每个 tunnel 有一个 UUID，域名用 CNAME 指向 `<UUID>.cfargotunnel.com`，必须打开代理（橙色云朵）
- `cloudflared` 的配置里写 ingress 规则：哪个主机名转发到内网哪个地址
- 内网这一侧只需要能出站，防火墙可以把入站全部关掉

### 配置示例

本地管理配置文件的方式：

```bash
# Log in once; writes cert.pem for this Cloudflare account
cloudflared tunnel login
# Create a named tunnel; prints its UUID and writes a credentials JSON
cloudflared tunnel create homelab
# Point a public hostname at the tunnel (creates the CNAME record)
cloudflared tunnel route dns homelab app.example.com
```

```yaml
# ~/.cloudflared/config.yml
tunnel: <UUID>
credentials-file: /home/user/.cloudflared/<UUID>.json
ingress:
  - hostname: app.example.com
    service: http://localhost:8080
  # Last rule must be a catch-all
  - service: http_status:404
```

```bash
cloudflared tunnel run homelab
```

也可以在 Zero Trust 控制台里创建 tunnel、配置主机名，本地只跑 `cloudflared tunnel run --token <token>`，配置都在 Cloudflare 那边（远程管理）。在 Kubernetes 里一般把 `cloudflared` 作为 Deployment 跑两个副本，ingress 规则指向集群内的 Service。

### 用法要点

- **公网访问只适合 HTTP(S)**。SSH、数据库这类 TCP 服务也能走 tunnel，但访问方同样要装 `cloudflared` 或 Cloudflare 的客户端，不能像网页那样直接打开
- **tunnel 只解决"能访问到"，不解决"谁能访问"**。只给自己用的后台，前面再加一层 Access（Zero Trust）做登录认证
- **给机器调用的入口不能用 Access 登录**。比如 GitHub webhook，GitHub 不会走 Access 的登录流程，只能靠请求签名校验（webhook secret 的 HMAC），再配合 WAF 规则只放行 GitHub 公布的 webhook IP 段
- **如果只是想让内网服务接收某个平台的事件，先看看能不能反过来"由内网主动去拉"**。比如 GitHub Actions 的自托管 runner 就是由 runner 主动连 GitHub 取任务，不需要任何入站入口，也就用不着 tunnel

## 参考

- [Cloudflare R2 文档](https://developers.cloudflare.com/r2/)
- [R2 Pricing](https://developers.cloudflare.com/r2/pricing/)
- [R2 Public buckets](https://developers.cloudflare.com/r2/buckets/public-buckets/)
- [cloudflare_r2_bucket（OpenTofu Registry）](https://search.opentofu.org/provider/cloudflare/cloudflare/latest/docs/resources/r2_bucket)
- [Cloudflare Tunnel 文档](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-20 | 新增 Cloudflare Tunnel 一节，标题加上 Tunnel | 原文只在服务一览里提了一句 |
