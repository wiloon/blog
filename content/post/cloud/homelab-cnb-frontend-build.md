---
title: "Homelab CNB Frontend Build: 用 Cloud Native Buildpacks 构建前端镜像"
author: "-"
date: 2026-10-13T08:55:43+08:00
lastmod: 2026-10-13T08:55:43+08:00
url: homelab-cnb-frontend-build
categories:
  - cloud
tags:
  - buildpacks
  - cnb
  - tekton
  - k8s
  - nextjs
  - vite
  - homelab
  - remix
  - AI-assisted
---

## 这篇文档讲什么

Homelab 里两个前端 enx-ui（Next.js）和 rssx-ui（Vue + Vite）的镜像，现在都用 Cloud Native Buildpacks（CNB）构建，不再用 Dockerfile + Kaniko。本文按实际配置说明这套构建是怎么搭起来的：编译用哪个镜像、运行用哪个镜像、自己写的 buildpack 做了什么、Tekton 里怎么跑。

CNB 本身的概念（buildpack、builder、lifecycle、platform）见 [CNB: Cloud Native Buildpacks 与 Paketo](./cloud-native-buildpacks.md)；为什么会有 CNB、它和 Dockerfile 的取舍见 [Dockerfile/BuildKit vs CNB](./dockerfile-buildkit-vs-cnb.md)。这里只写 homelab 的落地。

## 为什么换掉 Kaniko

- Kaniko 上游（GoogleContainerTools/kaniko）2025-06 已归档，`executor:v1.23.0` 之后没有安全更新。
- enx-ui 用 Kaniko 构建一次约 5 分 20 秒，其中解压缓存的 `node_modules` 层 78 秒，每次新建并挂载 Longhorn RWX 卷约 40 秒。

备选里 BuildKit 需要常驻 `buildkitd`，rootless 模式也要放宽 seccomp/AppArmor；CNB 的 lifecycle 以普通用户运行，不需要特权，还支持 rebase。所以选了 CNB。2026-10 rssx 也迁过来之后，集群里已经没有 Kaniko 了。

## 三个组件：builder、buildpack、run image

CNB 构建出来的镜像，是把「构建产物」叠到「运行镜像」上。homelab 里这三样东西分别是：

| 组件 | 用的什么 | 作用 |
| --- | --- | --- |
| builder（编译阶段的镜像） | `heroku/builder:24` | 提供 Ubuntu 24.04 构建环境和 CNB lifecycle；构建步骤在这个镜像里跑 |
| buildpack | 仓库里自己写的（enx-ui：`cnb/nextjs-standalone`，rssx-ui：`cnb/vite-static`） | 装 Node、pnpm，跑构建，决定哪些东西进最终镜像 |
| run image（运行阶段的镜像） | `paketobuildpacks/ubuntu-noble-run-tiny` | 最终镜像的底座：Ubuntu 24.04、glibc，约 11 MB，没有 shell，用户 `1002:1001` |

编译阶段和运行阶段用的是两个不同的镜像，这一点和 Dockerfile 的多阶段构建（`FROM node AS builder` + `FROM nginx`）是同一个思路，区别是：

- Dockerfile 里两个阶段都由自己写；CNB 里 builder 和 run image 是两个现成的镜像，buildpack 只负责中间的构建逻辑。
- 最终镜像的层由 lifecycle 按 buildpack 声明的 layer 类型组装，不是靠 `COPY --from`。
- run image 和 builder 必须是同一个 Ubuntu 版本（这里都是 24.04 noble），否则构建期编译出的 glibc 二进制在运行期可能跑不起来。

### 为什么 builder 选 Heroku、却不用 Heroku 的 buildpack

`heroku/builder:24` 只用了两样东西：Ubuntu 24.04 的构建环境，和镜像里的 `/cnb/lifecycle/creator`。它自带的 Node buildpack 没用。

实测过直接用 Heroku 的 Node buildpack 构建 enx-ui：能成功，但镜像 565 MB，Kaniko 镜像只有 77 MB。原因是它按通用 Node 应用设计：

| 层 | 大小 | 说明 |
| --- | --- | --- |
| run image `heroku/heroku:24` | 166 MB | 完整 Ubuntu |
| pnpm 虚拟 store | 201 MB | standalone 输出里已经带了依赖，这层运行时是重复的 |
| app 层 | 97 MB | 整个项目目录，含源码 |
| Node.js | 70 MB | |
| pnpm | 29 MB | 运行时用不到 |

Paketo 官方不支持 pnpm；Google 的 builder 支持 pnpm，但同样是通用 Node buildpack 加 Ubuntu run image，体积问题一样。所以最后的做法是：借 Heroku builder 的构建环境，buildpack 自己写，run image 换成 Paketo 的 tiny 镜像。

run image 没选 alpine，是因为 alpine 用 musl：Node 和 `sharp` 之类的原生二进制要准备 glibc（构建期）和 musl（运行期）两套。tiny 镜像是 glibc，构建期和运行期一致。

## 自己写的 buildpack

一个 buildpack 最少只要三个文件：

```text
cnb/vite-static/
├── buildpack.toml   # id, version, buildpack API, target os/arch
└── bin/
    ├── detect       # exit 0 if this buildpack applies to the app
    └── build        # does the work, writes layers and launch.toml
```

`bin/build` 是普通的 bash 脚本。lifecycle 调用它时，当前目录是应用源码，`$CNB_LAYERS_DIR` 是写 layer 的目录。每个 layer 是一个子目录加一个同名 `.toml`，`.toml` 里的三个开关决定这层去哪：

| 开关 | 含义 |
| --- | --- |
| `build = true` | 后续构建步骤可见（加进 PATH 等） |
| `launch = true` | 进最终镜像 |
| `cache = true` | 存进缓存镜像，下次构建恢复 |

编译和运行分离，就是靠这三个开关做到的。以 rssx-ui 为例：

| layer | build | launch | cache | 内容 |
| --- | --- | --- | --- | --- |
| `node` | ✓ | | ✓ | 完整 Node.js（从 nodejs.org 下载，版本取 `.node-version`） |
| `pnpm` | ✓ | | ✓ | pnpm，版本取 `package.json` 的 `packageManager` |
| `store` | | | ✓ | pnpm content-addressable store，只做缓存 |
| `server` | | ✓ | ✓ | static-web-server 一个静态二进制，运行期唯一的程序 |

Node 和 pnpm 只在构建期存在，不进最终镜像；store 只做缓存；进镜像的 layer 只有 `server`。构建完成后，脚本把应用目录清空，只放回 `dist/` 的内容——源码和 `node_modules` 也不会进镜像。

## 依赖包为什么不会进运行时镜像

用 CNB 构建 Node 应用，如果不做特殊处理，依赖包会进最终镜像。上面 Heroku 实测的 565 MB 里，pnpm 虚拟 store（201 MB）、pnpm（29 MB）、带着源码和依赖的整个项目目录（97 MB）都在运行时镜像里。

原因在于：哪些东西进最终镜像，是 buildpack 决定的，不是 lifecycle 决定的。buildpack 给某个 layer 标了 `launch = true`，这层就会被导出到镜像；应用目录（app 层）在构建结束时是什么样，导出的就是什么样。Heroku 的 Node buildpack 面向通用 Node 应用，它无法假设运行时不需要 `node_modules`，所以依赖层标成了 launch，项目目录也原样保留。这不是 bug，是通用 buildpack 必须做的保守选择。

解决办法不是去改 Heroku 的 buildpack，而是不用它，换成自己写的 buildpack。具体靠下面四件事：

1. 替换掉 builder 自带的 buildpack。`creator` 的 `-buildpacks` 指向仓库里的 buildpack 目录，`-order` 指向只有这一个 buildpack 的 order 文件（见下文「构建脚本」）。builder 里的 Heroku buildpack 根本不参与检测和构建，Heroku builder 只剩下构建环境和 lifecycle 两个作用。
2. 依赖相关的 layer 都不标 launch。Node 和 pnpm 是 `build + cache`，pnpm store 是只 `cache`：这些层在构建期可用，下次构建能从缓存恢复，但不会出现在运行时镜像里。
3. 让构建产物自带运行所需的最小依赖。
   - Next.js 开启 `output: 'standalone'`：`next build` 会追踪（trace）服务端实际 import 了哪些文件，把用到的依赖单独复制到 `.next/standalone/node_modules`。没用到的包、devDependencies 都不在里面。
   - Vite 打包后的 `dist/` 只有静态文件，依赖已经打进 JS bundle，运行时不需要 `node_modules`。
4. 构建最后一步重写应用目录。`bin/build` 把应用目录清空，只放回 standalone 或 `dist/` 的内容。app 层导出时就只有这些，源码、完整的 `node_modules`、`.next/cache` 都留在构建环境里。

再加上 run image 换成约 11 MB 的 tiny 镜像，enx-ui 最终各层是：run image 10.8 MB、`node` 可执行文件 52.4 MB、standalone 15.3 MB、launcher 1.4 MB，合计 79.9 MB。

这和 Dockerfile 多阶段构建里「在 builder 阶段装依赖、只把产物 `COPY --from` 到运行阶段」是同一个思路，只是表达方式从 `COPY --from` 换成了 layer 的 launch 标记和对应用目录的整理。

enx-ui 的 `nextjs-standalone` 结构相同，区别在运行期：Next.js SSR 需要 Node，所以 launch layer 只放 `node` 这一个可执行文件，应用目录只留 `.next/standalone`、`.next/static` 和 `public`。实测镜像 79.9 MB，和原来 Containerfile 的 76.9 MB 基本持平。

### 启动命令：launch.toml

run image 没有 shell，启动命令必须是 exec 形式。buildpack 在 `$CNB_LAYERS_DIR/launch.toml` 里声明：

```toml
# rssx-ui: serve the Vite build with static-web-server
[[processes]]
type = "web"
command = ["static-web-server"]
args = ["--host", "0.0.0.0", "--port", "8080", "--root", ".", "--page-fallback", "./index.html", "--cache-control-headers", "false", "--health", "true"]
default = true
```

几个参数的来由：

- 端口 8080：run image 的用户不是 root，绑不了 80。Service 仍对外暴露 80，`targetPort` 指向 8080。
- `--page-fallback`：找不到的路径返回 `index.html`，相当于 nginx 的 `try_files $uri $uri/ /index.html`，Vue Router 的深链接靠它。
- `--cache-control-headers false`：static-web-server 默认给 `index.html` 加 `max-age=86400`，发布后浏览器会继续用一天前的页面。原来的 nginx 不加缓存头，这里保持一致。
- static-web-server 用的是 musl 静态链接版本（约 8 MB），在没有 shell 的 tiny 镜像上直接能跑。下载时按 sha256 校验。

### 实际踩到的坑

- lifecycle 恢复缓存时会重新序列化 layer 的 `.toml`，键前面多了缩进。用 `sed` 读缓存里的版本号时要容忍缩进，否则每次都判断为缓存未命中、重新下载 Node。
- Corepack 装的 pnpm 12 启动器会自己去拉平台二进制，从 Nexus npm 代理读不到 `integrity` 字段就失败。改成 `npm install -g pnpm@<version>`。
- 下载一定要设超时。有一次 nodejs.org 下载卡住，没设 `--max-time` 的 curl 把构建拖了 17 分钟。

## 构建脚本：直接调 lifecycle，不用 pack

本地常见的入口是 `pack build`，但 Tekton 里没有 pack。为了不让两处逻辑走样，每个前端仓库里只有一个 `cnb/build.sh`，它在 builder 镜像里直接调用 lifecycle：

```bash
# lay out the repo's buildpack the way the lifecycle expects, then:
CNB_PLATFORM_API=0.14 /cnb/lifecycle/creator \
  -app="$APP_DIR" \
  -layers="$WORK/layers" \
  -platform="$WORK/platform" \
  -buildpacks="$WORK/buildpacks" \
  -order="$WORK/order.toml" \
  -run-image="$RUN_IMAGE" \
  -cache-image="$CACHE_IMAGE" \
  -previous-image="$REPO:cnb-latest" -tag="$REPO:cnb-latest" \
  "$REPO:$COMMIT"
```

`creator` 一条命令跑完 detect、restore、build、export 几个阶段。几个参数的作用：

- `-order`：只有一组，只有仓库自己的 buildpack，builder 自带的都不参与。
- `-platform`：platform env 目录。npm 源就是写成 `env/npm_config_registry` 文件传给 buildpack 的。
- `-cache-image`：缓存（Node、pnpm、store）存在 registry 里的一个镜像，不需要 PVC。
- `-previous-image`：和上一次的镜像比较，没变的 launch layer 直接复用、不重新上传。

镜像版本固定在仓库里的一个文件 `cnb/images.conf`，按 digest 写，不写可变的 tag：

```bash
# heroku/builder:24 -- build environment and lifecycle only
RSSX_CNB_BUILDER_IMAGE=docker.io/heroku/builder@sha256:1186...
# paketobuildpacks/ubuntu-noble-run-tiny:latest -- no shell, ~11 MB
RSSX_CNB_RUN_IMAGE=docker.io/paketobuildpacks/ubuntu-noble-run-tiny@sha256:2314...
```

升级时只改这个文件：Node 改 `.node-version`，pnpm 改 `packageManager`，builder / run image 查新 digest 改 `images.conf`。

## Tekton 里怎么跑

w10n-config 仓库里有两个通用 Task，enx-ui 和 rssx-ui 共用：

| Task | 做什么 |
| --- | --- |
| `cnb-resolve-builder` | 浅克隆仓库，从 `images.conf` 读出 builder 镜像，作为 result 输出 |
| `cnb-build` | clone 和 build 两个 step 在同一个 Pod 里：clone 到 emptyDir，然后在 builder 镜像里执行 `<app>/cnb/build.sh` |

builder 要单独一个 Task 读出来，是因为 step 的镜像必须在 Pod 创建前就确定；后一个 Task 的 step 用 `image: $(params.BUILDER_IMAGE)` 引用前一个 Task 的 result。

```yaml
# pipeline-build-rssx-ui.yaml (excerpt)
- name: resolve-builder
  taskRef: {name: cnb-resolve-builder}
  params:
  - {name: IMAGES_CONF, value: rssx-ui/cnb/images.conf}
  - {name: KEY, value: RSSX_CNB_BUILDER_IMAGE}
- name: build-image
  taskRef: {name: cnb-build}
  params:
  - {name: APP_DIR, value: rssx-ui}
  - {name: BUILDER_IMAGE, value: $(tasks.resolve-builder.results.builder)}
  - {name: CACHE_IMAGE, value: nexus.nexus.svc.cluster.local:8086/rssx-ui-cnb-cache:latest}
  - {name: RUN_IMAGE_MIRROR, value: nexus.nexus.svc.cluster.local:8082}
```

和集群环境相关的几点：

- 源码在 emptyDir 上，不再为每次构建创建 Longhorn 卷。
- build step 以 CNB 用户（uid 1000）运行，不需要 privileged；clone step 以 root 运行，克隆完把源码 `chown` 给 uid 1000。
- lifecycle 是自己去 registry 拉 run image 的，节点上 containerd 配的镜像加速不起作用，所以 `RUN_IMAGE_MIRROR` 把 run image 引用里的 `docker.io` 换成集群内 Nexus 的 Docker Hub 代理。
- npm 源用集群内 Nexus 的 npm-group，走 HTTP：builder 镜像不信任内部 `*.wiloon.com` 的 CA。
- 构建完成后 `update-gitops-repo` 把新镜像 tag 写回 GitOps 仓库的 Deployment，Argo CD 同步上线。这一段和 Kaniko 时期一样，见 [enx-api 在 Homelab 的构建与部署](./enx-api-homelab-cicd.md)。

## 结果

| 项目 | 之前（Kaniko + Containerfile） | 现在（CNB） |
| --- | --- | --- |
| enx-ui 只改代码时的构建耗时 | 约 4 分 50 秒 | 约 3 分钟 |
| enx-ui 镜像大小 | 76.9 MB | 79.9 MB |
| rssx-ui 运行期 | nginx（alpine） | static-web-server，run-tiny |
| 是否需要 root / privileged | 构建需要 root | 不需要 |
| 构建定义在哪 | Containerfile + Pipeline 里的 Kaniko 参数 | 应用仓库里的 `cnb/`，Pipeline 只负责执行 |

## 代价

- buildpack 是自己维护的。下载 Node、安装 pnpm、整理产物这些原来写在 Dockerfile 里的步骤，现在写在 `bin/build` 里，CNB 特有的细节（layer TOML、缓存命中判断）也要自己处理。
- run image 没有 shell，不能 `kubectl exec ... sh` 进去排查，要用 `kubectl debug` 或者另起一个临时 Pod。
- 运行用户从 root 变成 1002，端口要用非特权端口；挂载了持久卷的应用要检查文件属主。

## 后端：ko

同一时期，Go 后端 enx-api 和 rssx-api 改用 [ko](https://ko.build/) 构建，Tekton 里对应 `ko-build` Task。ko 不走 CNB，直接把 `go build` 出来的二进制作为一层叠到基础镜像上，基础镜像用的是同系列的 `paketobuildpacks/ubuntu-noble-run-static`（没有 libc，只有 CA 证书和 tzdata）。和前端一样，Go、ko、基础镜像的版本都按 digest 固定在应用仓库的 `build/build.conf` 里。

## 相关文件

| 文件 | 说明 |
| --- | --- |
| `enx-ui/cnb/`、`rssx-ui/cnb/` | `build.sh`、`images.conf`、buildpack 目录 |
| w10n-config `infra/homelab/k8s/tekton/task-cnb-build.yaml` | `cnb-resolve-builder` 和 `cnb-build` 两个 Task |
| w10n-config `infra/homelab/k8s/tekton/pipeline-build-*-ui.yaml` | 前端的 Pipeline |
| enx `docs/architecture/adr-055-*.md` | 选型决策和实验数据 |

## 参考

- [Cloud Native Buildpacks: Buildpack API](https://buildpacks.io/docs/reference/spec/buildpack-api/)
- [Cloud Native Buildpacks: Platform API（lifecycle creator）](https://buildpacks.io/docs/reference/spec/platform-api/)
- [heroku/builder](https://github.com/heroku/cnb-builder-images)
- [Paketo noble tiny stack](https://github.com/paketo-buildpacks/noble-tiny-stack)
- [static-web-server](https://static-web-server.net/)
