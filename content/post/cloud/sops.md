---
title: "SOPS: Secrets OPerationS 简介"
author: "-"
date: 2026-10-12T15:32:33+08:00
lastmod: 2026-10-12T15:32:33+08:00
url: sops
categories:
  - Cloud
tags:
  - sops
  - age
  - secrets
  - gitops
  - remix
  - AI-assisted
---

## SOPS 是什么

SOPS（Secrets OPerationS）是一个命令行工具，用 Go 写的。它最初由 Mozilla 开发，2023 年迁到 [getsops/sops](https://github.com/getsops/sops)，现在是 CNCF 项目。

它只做一件事：**加密和解密结构化文件**，支持 YAML、JSON、ENV（dotenv）、INI 和二进制文件。典型用法是把密钥加密后提交到 git，这样 git 里只有密文。

它**不是**常驻服务，也不负责存储。密文就是普通文件，解密由你在需要的时候显式调用。

## 原理

### 信封加密

1. 每个文件随机生成一把 data key，用 AES256-GCM 加密文件里的值。
2. 再用一把或多把 master key 加密这把 data key，结果写进文件末尾的 `sops:` 元数据段。

master key 可以是 age、PGP、AWS/GCP/Azure 的 KMS、HashiCorp Vault（或 OpenBao）的 Transit 等。同一个文件可以同时加密给多把 master key，任意一把都能解开。

### 只加密值，不加密键

```yaml
stringData:
  POSTGRES_PASSWORD: ENC[AES256_GCM,data:3mZ0...,iv:...,tag:...,type:str]
sops:
  age:
    - recipient: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
      enc: |
        -----BEGIN AGE ENCRYPTED FILE-----
        ...
  mac: ENC[AES256_GCM,data:...,type:str]
```

- `git diff` 能看出改的是哪个字段，review 时不用解密也能看懂结构。
- 非敏感字段（比如 K8s 的 `metadata`）可以保持明文。
- 文件带 MAC，密文被篡改时解密会报错。

## age

[age](https://age-encryption.org/) 是一个小巧的文件加密工具，可以看作 PGP 的现代替代品，SOPS 官方也建议优先用它。

- 公钥（`age1...`）可以公开，写进仓库的 `.sops.yaml`，**加密**只需要公钥。
- 私钥（`AGE-SECRET-KEY-1...`）只有它能**解密**，绝对不能进 git。

SOPS 默认从以下位置读取私钥：

- Linux：`~/.config/sops/age/keys.txt`
- macOS：`~/Library/Application Support/sops/age/keys.txt`
- 设置了 `$XDG_CONFIG_HOME` 时，两者都改为 `$XDG_CONFIG_HOME/sops/age/keys.txt`

也可以用 `SOPS_AGE_KEY_FILE`、`SOPS_AGE_KEY`，或 `SOPS_AGE_KEY_CMD`（用一条命令输出私钥，比如从密码管理器取）来覆盖。

## 基本用法

```yaml
# .sops.yaml at repo root
creation_rules:
  - path_regex: \.sops\.ya?ml$
    encrypted_regex: ^(data|stringData)$
    age: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
```

```bash
# Encrypt in place
sops encrypt -i secret.sops.yaml

# Edit decrypted content in $EDITOR, re-encrypt on save
sops edit secret.sops.yaml

# Print plaintext
sops decrypt secret.sops.yaml

# Run a command with values injected only into its environment
sops exec-env secrets.sops.env 'tofu apply'

# Re-encrypt data key after recipients changed
sops updatekeys secret.sops.yaml
```

`exec-env` 解密后只把变量放进子进程的环境，不写磁盘。`exec-file` 通过 FIFO 把明文以文件的形式交给程序。

## 什么时候解密

SOPS **不会**在应用读取时自动解密，应用本身也不知道 SOPS 的存在。解密发生在应用启动前，由各种集成负责：

| 场景 | 谁来解密 |
| ---- | ---- |
| 本地命令 | `sops exec-env` / `exec-file`，或 direnv 的 `.envrc` 调用 `sops decrypt` |
| Ansible | `community.sops` 插件 |
| OpenTofu / Terraform | `carlpett/sops` provider（注意：解密后的值会进 state） |
| K8s + ArgoCD | [KSOPS](https://github.com/viaduct-ai/kustomize-sops)，在渲染 manifest 时解密 |
| K8s + Flux | Flux 内置支持 |

## 优缺点

优点：

- 密钥和代码一起版本化、一起 review。
- 不依赖任何在线服务，离线也能用。
- 一套工具同时覆盖 K8s、Ansible、tofu、本地脚本。

缺点：

- 密文永远留在 git 历史里。age 私钥一旦泄露，所有历史版本都能被解开，只能逐个轮换真实凭据。
- 权限粒度粗：持有私钥就能读全部。
- 没有审计，也没有动态凭据。
- 加密不能替代轮换：以前以明文进过 git 的密钥，迁移到 SOPS 之后仍要去控制台换掉。

## 和其他方案比较

| 方案 | 适合 |
| ---- | ---- |
| SOPS | 个人、小团队、GitOps；希望密钥和代码放在一起 |
| Sealed Secrets | 只有 K8s Secret 的场景 |
| ansible-vault | 纯 Ansible 项目 |
| 密码管理器 CLI（比如 Bitwarden 的 rbw） | 人在场的本地场景，密钥完全不进 git |
| OpenBao / Vault | 需要审计、动态凭据、集中轮换的自动化场景 |

我的 homelab 最后没有用 SOPS，而是选了 Bitwarden + rbw + OpenBao，取舍见 [Homelab Secrets Management](./homelab-secrets-management.md)。

## 参考

- [SOPS 文档](https://getsops.io/docs/)
- [SOPS age 用法](https://getsops.io/docs/usage/identities/age/)
- [age](https://age-encryption.org/)
- [KSOPS](https://github.com/viaduct-ai/kustomize-sops)
