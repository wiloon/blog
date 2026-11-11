---
title: "Docker Image Digest: 镜像指纹与版本号的区别"
author: "-"
date: 2026-11-09T10:36:53+08:00
lastmod: 2026-11-09T10:36:53+08:00
url: image-digest
categories:
  - cloud
tags:
  - docker
  - container
  - renovate
  - remix
  - AI-assisted
---

## Digest 是版本号的第四位吗

在看 Renovate 的依赖更新 PR 时，我遇到了三种更新类型：minor、patch 和 digest。前两种能对应版本号的位置，digest 是否就是第四位？

不是。major、minor、patch 属于语义化版本号；digest 是镜像内容的哈希指纹，两者描述的是不同的东西。

以 `1.27.3` 为例：

| 部分 | 名称 | 含义 |
| --- | --- | --- |
| `1` | major | 主版本 |
| `27` | minor | 次版本 |
| `3` | patch | 补丁版本 |

Docker 镜像的 tag 可以采用这种版本号，也可以是 `latest`、`stable` 或其他字符串。tag 本身不保证遵循语义化版本规范。

## Tag 是标签，digest 是指纹

下面是两种镜像引用方式：

```text
golang:1.27.3
golang@sha256:e519d3b0a5b285e5aa53ab9eef02bc6bbb9cb04608389b743a136a9ce75f0d1e
```

第一行通过 tag `1.27.3` 查找镜像。第二行通过 digest 精确指定镜像内容，其中 `sha256` 是哈希算法，冒号后面是哈希值。

tag 是一个可移动的引用：维护者可以让同一个 tag 指向后来重新构建的镜像。digest 则绑定特定内容，不能在保持 digest 不变的情况下把它替换成另一份内容。

更准确地说，仓库引用中的 digest 通常是镜像 manifest 的哈希；对于多平台镜像，也可能是引用多个平台 manifest 的 image index 的哈希。它不是简单地对某个镜像压缩包文件计算哈希。

因此，固定 tag 不等于固定镜像内容。按 digest 拉取时，只要对应内容仍可从仓库获取，就能取得该 digest 指定的内容。[Docker 官方说明](https://docs.docker.com/dhi/explore/security-concepts/digests/)

## 为什么 Go 版本不变，digest 仍然会更新

镜像里除了 Go，还可能包含操作系统文件、系统库和其他工具。

例如，镜像维护者保持 Go `1.27.3` 不变，但更新底层操作系统的安全补丁并重新构建，再将 `golang:1.27.3` 指向新镜像。这时：

- Go 版本仍是 `1.27.3`。
- tag 仍是 `golang:1.27.3`。
- 镜像内容变了，digest 随之改变。

这是一种可能的更新原因，不能仅凭 digest 变化就判断具体改了哪些内容；实际原因还需要查看上游构建记录。

对于多平台镜像，某个平台的镜像或 index 内容发生变化，也可能导致顶层 digest 改变，并不一定意味着所有平台的运行内容都发生了变化。

## Renovate 的 digest 更新在做什么

项目使用 digest 固定构建镜像后，上游移动 tag 不会自动改变项目使用的镜像。Renovate 可以跟踪该 tag 对应的 digest，并通过 PR 更新项目里固定的值。

例如，PR 显示：

```text
Update type: digest
2920bb1... → e519d3b...
```

这里的短字符串是 digest 的缩写，实际配置使用完整的 SHA-256 值。它表示更换固定的镜像内容，不表示版本号从第三位增加到了第四位。

固定 digest 让更新成为一次显式、可审查的配置变更。是否自动合并这类 PR，是另一项 Renovate 策略；digest 更新本身并不保证没有兼容性影响。

## 查看与使用 digest

查看 tag 当前对应的 digest 和平台信息：

```bash
docker buildx imagetools inspect golang:1.27.3
```

按指定 digest 拉取镜像，以下命令中的 `<digest>` 需要替换为完整的哈希值：

```bash
docker pull golang@sha256:<digest>
```

本地已拉取镜像的仓库 digest 可以用下面的命令查看。列表里的 `IMAGE ID` 与仓库 digest 不是同一个概念：

```bash
docker image ls --digests
```

固定 digest 解决的是内容一致性问题，不等于证明镜像来自可信发布者，也不代表镜像没有漏洞。

## 参考

- [Docker: Image digests](https://docs.docker.com/dhi/explore/security-concepts/digests/)
- [Semantic Versioning 2.0.0](https://semver.org/)
