---
title: "Ansible Vault: 加密 Ansible 仓库里的密钥"
author: "-"
date: 2026-10-20T05:44:47+08:00
lastmod: 2026-10-20T05:44:47+08:00
url: ansible-vault
categories:
  - Cloud
tags:
  - ansible
  - ansible-vault
  - secrets
  - remix
  - AI-assisted
---

## 解决什么问题

Ansible 仓库里迟早会出现密钥：数据库密码、API token、TLS 私钥。playbook 和变量文件要进 git，密钥如果跟着明文进去，所有能克隆仓库的人和程序就都拿到了它，而且会永远留在历史里。

Ansible Vault 是 Ansible 自带的加密功能（命令是 `ansible-vault`，不用另外安装）。它解决的是一件事：**让密钥以密文的形式和 playbook 放在同一个仓库里，运行 playbook 时自动解密。**

它和 HashiCorp Vault 没有关系，只是名字像。HashiCorp Vault（以及它的 fork OpenBao）是一个常驻的密钥服务；Ansible Vault 只是一个文件加密工具，没有服务端。

## 原理

加密后的文件是这样的：

```text
$ANSIBLE_VAULT;1.1;AES256
62313365396662343061393464336163383764373764613633653634306231386433626436623361
6134333665353966363534333632666535333761666131620a663537646436643839616531643561
...
```

- 第一行是头部：格式版本 `1.1`，算法 `AES256`。用了 vault ID（见下文）时版本是 `1.2`，头部末尾多一个标签。
- 加密过程：从 vault 密码用 PBKDF2-SHA256 加随机盐派生出密钥，用 AES-256（CTR 模式）加密内容，再用 HMAC-SHA256 防篡改，最后转成十六进制文本。
- 整个仓库通常只用一个 vault 密码。谁有这个密码，谁就能解开所有加密文件。

## 两种加密粒度

### 加密整个文件

```bash
# Create a new encrypted file and open it in $EDITOR
ansible-vault create group_vars/prod/vault.yml

# Encrypt an existing plaintext file in place
ansible-vault encrypt group_vars/prod/vault.yml

# Edit / view without leaving a plaintext copy on disk
ansible-vault edit group_vars/prod/vault.yml
ansible-vault view group_vars/prod/vault.yml

# Change the password
ansible-vault rekey group_vars/prod/vault.yml
```

### 只加密单个变量

```bash
ansible-vault encrypt_string 's3cr3t' --name 'db_password'
```

输出可以直接贴进普通的变量文件，文件其他部分仍是明文：

```yaml
db_user: app
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  3836613964...
```

整文件加密的缺点是 `git diff` 只能看到一整块密文变了，看不出改了哪个变量；单变量加密能看清结构，但密文不能用 `ansible-vault edit` 编辑，改值要重新生成。

### 常见的目录约定

Ansible 文档推荐把一组变量拆成两个文件：

```text
group_vars/prod/
├── vars.yml    # plaintext: db_password: "{{ vault_db_password }}"
└── vault.yml   # encrypted: vault_db_password: s3cr3t
```

所有密钥都用 `vault_` 前缀放进加密文件，明文文件里再引用一次。这样用 grep 能找到变量在哪里被用到，又不会暴露值。

## 运行时怎么提供密码

```bash
# Prompt for the password
ansible-playbook site.yml --ask-vault-pass

# Read it from a file
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

也可以在 `ansible.cfg` 里写 `vault_password_file = ...`，之后就不用每次加参数。

`--vault-password-file` 指向的如果是一个**可执行文件**，Ansible 会运行它，把标准输出当作密码。所以密码不必明文落盘，可以从密码管理器里取：

```bash
#!/bin/sh
# vault-pass.sh: print the vault password from Bitwarden
exec rbw get ansible-vault-password
```

一个仓库要分开管理多套密钥（比如 dev 和 prod 用不同密码）时，用 vault ID 给密码加标签：

```bash
ansible-vault encrypt --vault-id prod@prompt group_vars/prod/vault.yml
ansible-playbook site.yml --vault-id dev@~/.vault_dev --vault-id prod@prompt
```

## 局限

- **只有一把共享密码**：所有人、所有 CI 用同一个密码。有人离开团队就要 `rekey` 所有文件，而旧密码仍然能解开 git 历史里的旧版本。
- **密码本身放哪里，问题没有消失**：只是从「很多密钥」变成了「一个密码」。这个密码如果明文放在 `~/.vault_pass`，效果和明文差不多。
- **只服务 Ansible**：同一个密钥 OpenTofu、K8s 也要用的话，得另外再存一份。
- **没有审计和过期**：谁在什么时候解密了什么，没有记录；密钥也不会自动失效。

## 和其他方案对比

| 方案 | 密钥存在哪里 | 适合 |
| ---- | ---- | ---- |
| Ansible Vault | git 里的密文，一个共享密码 | 纯 Ansible 项目，小团队 |
| [SOPS](./sops.md) | git 里的密文，可以按人/按环境用不同的 age 或 KMS 密钥，只加密值、key 保持明文 | 多种工具共用的 GitOps 仓库 |
| 密码管理器 CLI（rbw） | 不进 git，运行时 `lookup('pipe', 'rbw get ...')` 取 | 人在场时执行的 playbook |
| OpenBao / Vault | 在线服务，按身份授权，有审计和动态凭据 | 无人值守的自动化 |

Ansible Vault 的优势是零依赖：装了 Ansible 就有，不用另外部署任何东西。SOPS 在它的基础上解决了「一把共享密码」和「diff 看不清」两个问题。

## 我的选择

我的 homelab 里，playbook 都是我自己在终端里执行的，属于「人在场」的场景，所以没有用 Ansible Vault，而是在 playbook 里直接从 Bitwarden 取：

```yaml
vars:
  cf_api_token: "{{ lookup('pipe', 'rbw get cloudflare-dns-token') }}"
```

这样 git 里连密文都没有，轮换只改 Bitwarden 里的一处。完整的取舍见 [Homelab Secrets Management](./homelab-secrets-management.md)。

如果哪天需要在 CI 里无人值守地跑 playbook，Ansible Vault 加一个从 CI secret 读密码的脚本，是最省事的过渡办法。
