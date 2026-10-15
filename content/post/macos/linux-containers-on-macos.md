---
title: "Linux Containers on macOS: Colima, Apple container, OrbStack"
author: "-"
date: 2026-10-15T17:40:55+08:00
lastmod: 2026-10-15T17:40:55+08:00
url: linux-containers-on-macos
categories:
  - macOS
  - Cloud
tags:
  - macos
  - container
  - colima
  - lima
  - containerd
  - orbstack
  - remix
  - AI-assisted
---

macOS 内核不能直接跑 Linux 容器，所有方案都是先起一个 Linux 虚拟机，再在里面跑容器运行时。区别在于虚拟机怎么起、几个容器共用一台虚拟机、对外提供什么 CLI。

## 分层

| 层级 | 例子 | 作用 |
| ---- | ---- | ---- |
| 容器运行时 | containerd、Docker Engine | 拉镜像、起容器，跑在 Linux 里 |
| Mac 上的 Linux 环境 | Colima（基于 Lima）、Apple container、OrbStack、Docker Desktop | 在 macOS 上提供 Linux 虚拟机，并把 CLI 暴露给宿主 |
| CLI | nerdctl、docker、container | 用户敲的命令 |

containerd 和 Colima 不是同一类东西：containerd 是引擎，Colima 负责给 containerd 准备一台 Linux 虚拟机。

## Colima

- 基于 Lima，所有容器共用一台 Linux 虚拟机
- 运行时可选 `docker` 或 `containerd`，选 containerd 时用 `nerdctl`，和 Linux 服务器上的用法一致
- 支持 compose（`nerdctl compose` 或 `docker compose`），可选内置 k3s
- MIT 协议，商用免费，只有 CLI

```bash
brew install colima

# native arm64 VM, use Rosetta for amd64 images
colima start --arch aarch64 --vm-type vz --vz-rosetta --runtime containerd

colima nerdctl -- run --rm hello-world
colima list
colima stop
```

注意 `--arch x86_64` 会让整台虚拟机走模拟，在 Apple Silicon 上很慢。需要 amd64 镜像时，用 arm64 虚拟机加 `--platform linux/amd64` 构建即可。

卸载：

```bash
colima delete default -f
brew uninstall colima lima lima-additional-guestagents
rm -rf ~/.colima ~/Library/Caches/colima
```

## Apple container

苹果官方开源的工具，详见 [macos container](../other/macos-container.md)。

- 每个容器一台独立的轻量虚拟机，隔离性好
- 只支持 Apple Silicon，需要较新的 macOS
- 2026-06 发布 1.0
- 截至 2026-10 不支持 compose，官方没有给出时间表；第三方 `apple-compose` 不支持 `build:`，也没有重启策略
- 没有内置 Kubernetes，没有 GUI
- 社区跑分中容器启动约 0.9s，Colima 约 0.3s，OrbStack 约 0.4s；容器间网络吞吐也落后

卸载（Homebrew 和 pkg 两种安装方式可能同时存在）：

```bash
container system stop
brew uninstall container
# pkg install; -d also deletes user data
sudo /usr/local/bin/uninstall-container.sh -d
rm -rf ~/Library/Application\ Support/com.apple.container
```

## OrbStack

- 性能和文件共享（bind mount）表现最好，有 GUI
- 个人非商业使用免费，商用要付费

## 怎么选

| 场景 | 选择 |
| ---- | ---- |
| 免费、只用 CLI、需要 compose，或想和 Linux 服务器上的 nerdctl 保持一致 | Colima + containerd |
| 预算允许，追求速度和体验 | OrbStack |
| 只跑单个容器，看重隔离，愿意跟进苹果的路线 | Apple container |
| 有可用的 Linux 主机 | 不在 Mac 上跑容器，直接在 Linux 主机上跑 |

我最后选了最后一种：homelab 里有多台 Linux 主机，Mac 上的 Colima 和 Apple container 都卸载了，腾出约 9G 磁盘空间。

需要完整 Linux 桌面而不只是容器时，见 [macOS Virtual Machines](./macos-virtual-machines.md)。

## 参考

- [apple/container](https://github.com/apple/container)
- [Colima](https://github.com/abiosoft/colima)
- [macOS container benchmarks](https://github.com/zot24/macos-container-benchmarks)
- [Apple container vs OrbStack vs Colima](https://codingprotocols.com/toolkit/comparisons/apple-container-vs-orbstack-vs-colima)
- [Apple Ships Stable 1.0 of its Native Container Tool](https://cloudnativenow.com/features/apple-ships-stable-1-0-of-its-native-container-tool-for-macos/)
