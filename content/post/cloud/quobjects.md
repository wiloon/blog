---
title: "QuObjects: 威联通 NAS 上的 S3 兼容对象存储"
author: "-"
date: 2026-11-25T14:45:57+08:00
lastmod: 2026-11-25T14:45:57+08:00
url: quobjects
categories:
  - cloud
tags:
  - qnap
  - nas
  - s3
  - object-storage
  - backup
  - longhorn
  - homelab
  - remix
  - AI-assisted
---

## QuObjects 是什么

QuObjects 是威联通（QNAP）官方的应用，在 App Center 里安装。装好后，NAS 会多出一个兼容 Amazon S3 协议的对象存储服务：客户端用 S3 API（Access Key + Secret Key 签名的 HTTP 请求）读写 bucket 和对象，不需要挂载目录。

所以凡是支持 S3 的程序，把 endpoint 指向 NAS 就能用，比如 Longhorn、Velero、restic、rclone、Veeam、Litestream。官方说它通过了 Veeam 的 "Ready Object with Immutability" 认证。

除了 S3，它也支持 OpenStack Swift 协议。

## 和 NFS、SMB 的区别

同一台 NAS 可以同时提供 NFS、SMB 和 S3（QuObjects），三者适合的场景不同：

| | NFS | SMB/CIFS | S3（QuObjects） |
| --- | --- | --- | --- |
| 客户端看到的 | 挂载的目录 | 挂载的目录 / 网络盘 | bucket 和对象，经 HTTP API 读写 |
| 鉴权 | 默认 `AUTH_SYS`：只看客户端 IP，uid 由客户端自报；真鉴权要 Kerberos | 用户名和密码 | Access Key 签名每个请求 |
| 防误删 / 勒索 | 无 | 依赖 NAS 快照 | 版本控制、Object Lock（WORM） |
| POSIX 语义 | 完整 | 大部分 | 没有：不能部分改写、不能重命名 |
| 上云 / 异地 | 难 | 难 | 换 endpoint 即可，rclone 直接同步 |
| 典型用途 | Linux 间共享目录、K8s NFS 存储类 | 桌面电脑、Time Machine、家庭共享 | 备份、归档、程序存数据 |

一句话：NFS 给 Linux 共享目录，SMB 给人用，S3 给程序存数据。

NFS 这一点容易误解：NAS 网页登录的用户名密码只管 SMB 和网页，管不到 NFS。导出规则写成 `*` 时，局域网里任何设备都能挂载并读写。

## 系统要求

以下来自官方产品页和教程（见文末参考）：

| 项目 | 要求 |
| --- | --- |
| CPU | 所有 x86（Intel / AMD）机型；ARM 只支持 TS-x32 系列和 TS-1635AX |
| 系统 | QTS 5.0.0 及以上、QuTS hero h5.0.0 及以上、QuTScloud c5.0.0 及以上 |
| 内存 | 官方建议 8 GB 或以上（没写最低值） |
| 默认端口 | 8010，可选 HTTP 或 HTTPS |

教程里另有一句「QuTS hero 只支持 QuObjects 2.3 及更早版本」，和产品页的说法对不上，装之前在 App Center 里看实际能装的版本为准。

我家里的是 TS-453Bmini：Celeron J3455（x86）、16 GB 内存、QTS 5.2.11，三项都满足要求。

## 主要功能

- Bucket：创建、删除、列出、HEAD、CORS。
- 对象：上传、下载、复制、删除、批量删除、预签名 URL。
- 分片上传：Initiate / UploadPart / Complete / ListParts / ListUploads。
- 路径风格（path-style）和虚拟主机风格的请求都支持。
- 版本控制：同一对象保留多个版本，可按天数或版本数设置保留。
- Object Lock（WORM）：对象在规定期限内不能删除或覆盖；开启 Object Lock 时会自动开启版本控制。

官方教程列出的 S3 API 清单里，没有出现 lifecycle、bucket policy、tagging、ACL 等接口。这些是否支持要装上后实测。

### 不可变性和底层文件系统

Object Lock 的强度和 NAS 的系统有关。官方对比表：

| | QuTS hero | QTS |
| --- | --- | --- |
| 对象存储底层 | ZFS | ext4 |
| 对象不可变的实现 | ZFS WORM | Linux `chattr` |
| 经 S3 协议访问时的不可变性 | 高 | 高 |
| 经其他协议访问时的不可变性 | 高 | 中 |

也就是说，在 QTS 上，S3 客户端删不掉被锁的对象；但如果有人通过 SMB 或 SSH 直接碰底层文件，防护会弱一些。

### 限制

| 项目 | 上限 |
| --- | --- |
| bucket 数、每个 bucket 的对象数 | 不限 |
| 单个对象 | QTS 16 TiB；QuTS hero 48.8 TiB |
| 单次 PUT | 1 TiB |
| 分片 | 最多 10,000 片，每片 5 MiB ~ 5 GiB |

## 用户和 Access Key

QuObjects 不单独维护用户库，它用的是 NAS 的本地用户或域用户：

1. 在 QuObjects 的 User Management 里点 Add User，选 NAS 上已有的用户。
1. 给这个用户生成 Access Key，一个用户可以有多个 key。
1. 从 QuObjects 里移除用户后，它的访问立即失效。

有一个坑：在 NAS 系统里删除用户，并不会让它在 QuObjects 里的 key 失效，得在 QuObjects 里也移除。

给程序用时，建议每个用途一个专用 NAS 用户（比如 `longhorn`），只给它需要的 bucket，key 定期轮换。

## 用作 Longhorn 备份目标

Longhorn 的备份格式是「块数据 + 元数据文件」，本来就按对象存储设计，S3 也是它文档里的默认例子。接 QuObjects 大致是：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: longhorn-backup-s3
  namespace: longhorn-system
stringData:
  AWS_ACCESS_KEY_ID: "<access-key>"
  AWS_SECRET_ACCESS_KEY: "<secret-key>"
  # QuObjects endpoint on the NAS
  AWS_ENDPOINTS: "https://192.168.50.227:8010"
  # Only needed when the NAS uses a self-signed certificate
  AWS_CERT: |
    -----BEGIN CERTIFICATE-----
    ...
```

然后把 Longhorn 的 backup target 设为 `s3://longhorn-backup@us-east-1/`（region 随便填，QuObjects 不看），credential secret 填 `longhorn-backup-s3`。Secret 不要明文进 git，用 SealedSecret 或 SOPS。

开 Object Lock 时要注意：Longhorn 会按保留数量删除旧备份，锁定期内的删除会被拒绝。两者怎么配合要先实测，可以先只开版本控制，Object Lock 放到验证之后。

## 能用 OpenTofu 管吗

能管一部分。OpenTofu 的 AWS provider 可以把 S3 endpoint 指向任何兼容服务：

```hcl
provider "aws" {
  alias  = "qnap"
  region = "us-east-1" # ignored by QuObjects

  endpoints {
    s3 = "https://192.168.50.227:8010"
  }

  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
}

resource "aws_s3_bucket" "longhorn" {
  provider = aws.qnap
  bucket   = "longhorn-backup"
}
```

| 能进 OpenTofu | 进不了 |
| --- | --- |
| bucket；版本控制、Object Lock 配置（看 QuObjects 是否实现对应 API） | QuObjects 的用户和 Access Key：没有 IAM 那样的 API，只能在网页上建 |
| | QuObjects 应用本身的安装和设置 |

风险：AWS provider 读取 `aws_s3_bucket` 时会顺带调用 ACL、CORS、website、logging、replication、tagging 等一串子接口。兼容 S3 的服务常有几个没实现，`tofu plan` 会报 `NotImplemented`。上面那份官方 API 清单里就缺了不少，所以能不能顺利跑通要实测。跑不通的话，bucket 在网页上手动建，写进文档也可以，毕竟它建完基本不会再动。

## 社区反馈

搜了 Veeam、Proxmox、QNAP 社区论坛和 GitHub 的讨论（2022–2025 年），整体结论是：能用，但不是开箱即用的 AWS 级兼容，常见问题集中在下面几类。

| 问题 | 说明 |
| --- | --- |
| 必须用 path-style | Proxmox Backup Server 列 bucket 报 400，开 path-style 后解决 |
| 自签证书 | 默认是 NAS 自签证书，校验证书的客户端走 HTTPS 会失败；换 Let's Encrypt 证书或给客户端配 CA |
| 版本回归 | QuObjects 2.5.539 改了对 AWS S3 新校验和标准的处理，有用户每次上传都报 400，回退到 2.5.513 解决；Velero 的 AWS 插件也受影响 |
| 签名版本 | 早期版本底层是 Swift，不支持 AWS Signature V4，Velero 内置的 restic 用不了（2022 年的 issue） |
| 请求限流 | 有用户用 Velero 时 bucket 里空目录越积越多，过期扫描触发 `Too Many Requests`，最后换成了 MinIO |
| Veeam | 官方认证，但 Veeam 的兼容列表注明要升级到 2.4.1785 以上，修了若干问题 |

也有正面的例子：有人用 restic 加 Let's Encrypt 证书把 QuObjects 当备份仓库，用得没问题，并说明它免费。

对 Longhorn 来说，要留意的是限流和版本回归：Longhorn 备份会把卷切成很多 2 MiB 的小块对象，请求数多。升级 QuObjects 前最好先跑一次备份和恢复验证。

## 待验证

- App Center 里能装的 QuObjects 版本。
- HTTPS 证书怎么配（自签还是导入）。
- AWS provider 对 QuObjects 的兼容性。
- Longhorn 的保留策略和 Object Lock 能否共存。

## 参考

- [QuObjects 产品页](https://www.qnap.com/en/software/quobjects)
- [QuObjects 设置教程](https://www.qnap.com/vi-vn/how-to/tutorial/con_show.php?cid=136)
- [QuObjects 2.5.539 upload problem](https://community.qnap.com/t/quobjects-2-5-539-upload-problem/5911)
- [Proxmox: PBS on QuObjects](https://forum.proxmox.com/threads/trying-to-set-up-pbs-to-use-s3-on-quobjects-app-qnap.176670/)
- [QuObjects S3 and Duplicati](https://community.qnap.com/t/quobjects-s3-and-duplicati-local-network/7193)
- [Velero issue #5587: Signature V4](https://github.com/vmware-tanzu/velero/issues/5587)
- [QuObject directory automatic deletion](https://forum.qnap.com/viewtopic.php?t=162122&p=794518)
- [Veeam: QNAP QuObjects](https://www.veeam.com/sys1242)
- [Pull Backup with Restic to a QNAP NAS S3 store](https://harald.hoyer.xyz/restic/)
- [NFS](./nfs.md)、[Samba](./samba.md)、[Litestream](./litestream.md)
- [Hardware：QNAP TS453Bmini](../hardware/hardware.md#qnap-ts453bmini)
