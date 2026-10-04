---
title: "Cloudflare Workers: 边缘 Serverless 运行环境"
author: "-"
date: 2026-10-04T07:46:21+08:00
lastmod: 2026-10-04T07:46:21+08:00
url: cloudflare-workers
categories:
  - cloud
tags:
  - cloudflare
  - serverless
  - javascript
  - remix
  - AI-assisted
---

## Cloudflare Workers 是什么

Cloudflare Workers 是 Cloudflare 提供的 Serverless 运行环境：把一段 JavaScript / TypeScript（也支持 Python 和编译成 WebAssembly 的 Rust、Go 等）部署到 Cloudflare 全球的边缘节点上，请求打到离用户最近的节点时直接在那里执行代码并返回响应，不需要自己管服务器。

和 AWS Lambda 这类传统 FaaS 相比，主要区别在运行时：

| 对比项   | Cloudflare Workers                     | 传统 FaaS（如 Lambda）         |
| -------- | -------------------------------------- | ------------------------------ |
| 隔离方式 | V8 Isolate，多个 Worker 共享一个进程   | 容器 / microVM                 |
| 冷启动   | 毫秒级，基本可忽略                     | 百毫秒到秒级                   |
| 部署位置 | 全球所有边缘节点                       | 选定的一个或几个 region        |
| 运行时   | 类浏览器的 Web 标准 API（fetch、Request、Response 等），部分兼容 Node.js API | 完整的 Node.js / Python 等运行时 |
| 限制     | CPU 时间、内存（128 MB）、包体积有限制 | 限制相对宽松                   |

V8 Isolate 是 Chrome 的 JS 引擎里用来隔离不同页面的机制，开销比容器小很多，所以冷启动快、单机能跑大量 Worker；代价是不能运行任意二进制，也不能使用依赖原生模块的 npm 包。

## 典型用途

- 在 CDN 层改写请求和响应：加 header、重定向、A/B 测试、按地区返回不同内容
- 轻量 API 后端：配合存储服务直接写业务逻辑
- 鉴权网关：在请求到达源站之前校验 token
- 定时任务：Cron Triggers 按 cron 表达式触发 Worker
- 给静态站点补动态能力：Cloudflare Pages 的 Functions 底层就是 Workers

## 配套存储和服务

Worker 本身无状态，需要状态时用 Cloudflare 的配套服务，通过 binding 注入到 `env` 里使用：

| 服务            | 说明                                             |
| --------------- | ------------------------------------------------ |
| KV              | 全球分布的键值存储，读多写少，最终一致           |
| D1              | 基于 SQLite 的关系型数据库                       |
| R2              | 对象存储，兼容 S3 API，无出口流量费              |
| Durable Objects | 带强一致状态的单实例对象，适合协同、计数、WebSocket |
| Queues          | 消息队列                                         |
| Workers AI      | 在边缘调用推理模型                               |

## 一个最小的 Worker

用官方脚手架创建项目：

```bash
npm create cloudflare@latest hello-worker
cd hello-worker
```

`src/index.js`：

```javascript
export default {
  // Called for every HTTP request routed to this Worker
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/hello") {
      return new Response("hello from the edge\n");
    }
    // Request metadata provided by Cloudflare, e.g. country code
    return Response.json({ path: url.pathname, country: request.cf?.country });
  },
};
```

配置文件 `wrangler.toml`（新版本脚手架也可能生成 `wrangler.jsonc`，字段相同）：

```toml
name = "hello-worker"
main = "src/index.js"
compatibility_date = "2026-10-01"

# Bind a KV namespace, available as env.MY_KV in code
# [[kv_namespaces]]
# binding = "MY_KV"
# id = "<namespace-id>"
```

本地开发和部署都用 Wrangler CLI：

```bash
# Run locally with the workerd runtime
npx wrangler dev

# Log in and deploy to Cloudflare
npx wrangler login
npx wrangler deploy
```

部署完成后默认得到一个 `hello-worker.<子域>.workers.dev` 的地址，也可以在后台或配置里给 Worker 绑定自己域名下的路由（routes）或自定义域名。

## 和 Cloudflare Pages 的关系

Cloudflare 后台里 Workers 和 Pages 放在同一个「Workers & Pages」入口下：

- Pages 偏向静态站点托管，连 Git 仓库自动构建，本博客就部署在 Pages 上（见 [Hugo + Cloudflare Pages 搭建博客](../web/hugo-cloudflare-pages-blog-setup.md)）
- Pages Functions 是在 Pages 项目里写的 Workers 代码
- Workers 现在也支持 Static Assets，可以直接托管静态文件，Cloudflare 官方的方向是逐步把新项目引导到 Workers 上

如果只是纯静态站点，Pages 足够；需要较多服务端逻辑或要用 Durable Objects、Queues 等能力时，直接用 Workers 更顺手。用 IaC 管理 Pages 项目的写法见 [Cloudflare Pages with OpenTofu](./cloudflare-pages-opentofu.md)。

## 免费额度和限制

免费计划（以官方文档为准，额度会调整）：

- 每天 10 万次请求
- 每次请求 CPU 时间 10 ms（付费计划默认 30 s，可调）
- 单个 Worker 压缩后体积 3 MB（付费 10 MB）

注意这里限制的是 CPU 时间，等待 `fetch` 子请求、等待数据库返回的时间不计入，所以做转发、聚合类工作时 10 ms 通常够用。

## 其他厂商的类似产品

### AWS

AWS 有两个类似的产品，都挂在 CloudFront 下面：

| 产品                 | 运行位置                                  | 特点                                                                                                                                            |
| -------------------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| CloudFront Functions | 全部 CloudFront 边缘节点                  | 轻量 JS，执行时间在亚毫秒级，不能访问网络，也不能读写请求体；只适合改 header、重定向、URL 重写、简单校验 token；可配合 CloudFront KeyValueStore 存少量数据 |
| Lambda@Edge          | CloudFront 区域边缘缓存（比边缘节点少）   | 本质是 Lambda，支持 Node.js 和 Python，能发网络请求、处理请求体；冷启动和价格都比 Workers 高，部署要从 us-east-1 复制出去                       |

Workers 一个产品同时覆盖了这两者的场景。AWS 拆成「极轻量」和「完整 Lambda」两档，两者都不是 V8 Isolate 模式。普通 Lambda 只跑在选定的 region，不算边缘计算。

### 其他厂商

| 厂商         | 产品                                    | 说明                                                                                                         |
| ------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Fastly       | Compute（原 Compute@Edge）              | 基于 WebAssembly，支持 Rust、JS、Go，冷启动也很快，是 Workers 最直接的对标                                   |
| Akamai       | EdgeWorkers                             | JS，跑在 Akamai 的 CDN 节点上                                                                                |
| Vercel       | Edge Middleware / Edge Functions        | 基于 V8 Isolate，和 Next.js 结合紧密；Vercel 近来更推 Node 运行时（Fluid compute）                           |
| Netlify      | Edge Functions                          | 基于 Deno                                                                                                    |
| Deno         | Deno Deploy                             | V8 Isolate，模式和 Workers 很像                                                                              |
| Google Cloud | 无直接对应                              | Cloud Run、Cloud Functions 都是 region 级；Media CDN 和 Cloud Load Balancing 的 Service Extensions 支持 Wasm 插件，可在边缘改请求，但能力有限 |
| Azure        | 无直接对应                              | Azure Functions 是 region 级；Front Door 只有规则引擎，不能跑通用代码                                        |
| 阿里云       | ESA 边缘函数（前身 DCDN EdgeRoutine）   | JS，跑在阿里云边缘节点                                                                                       |
| 腾讯云       | EdgeOne 边缘函数                        | JS，接口风格和 Workers 接近                                                                                  |

### 怎么选

- 已经在用 CloudFront，只做简单的请求改写：CloudFront Functions；需要更多能力再上 Lambda@Edge
- 想要全球部署、冷启动可忽略、还带存储（KV / D1 / R2）的完整方案：目前 Cloudflare Workers 最完整，Fastly Compute、Deno Deploy 也是这个方向
- 面向中国大陆用户：国外这些产品在大陆没有节点或需要备案，一般用阿里云 ESA 或腾讯云 EdgeOne

各家产品和限额变化较快，以官方文档为准。

## 参考

- [Cloudflare Workers 文档](https://developers.cloudflare.com/workers/)
- [Wrangler 文档](https://developers.cloudflare.com/workers/wrangler/)
- [Workers 限制说明](https://developers.cloudflare.com/workers/platform/limits/)
- [CloudFront Functions 与 Lambda@Edge 对比](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/edge-functions-choosing.html)
- [Fastly Compute](https://www.fastly.com/documentation/guides/compute/)
