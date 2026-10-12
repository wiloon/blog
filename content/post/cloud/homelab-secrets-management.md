---
title: "Homelab Secrets Management: Bitwarden、rbw 与 OpenBao"
author: "-"
date: 2026-10-12T10:38:43+08:00
lastmod: 2026-10-12T15:32:33+08:00
url: homelab-secrets-management
categories:
  - Cloud
tags:
  - secrets
  - bitwarden
  - rbw
  - openbao
  - vault
  - k8s
  - homelab
  - remix
  - AI-assisted
---

我在整理 homelab 的配置仓库时发现，有不少密钥以明文形式进了 git：数据库密码、云服务的 API token、K8s Secret 的 manifest。还有一些放在 `~/.zshrc.local` 里，作为环境变量。这篇文章记录我比较几种方案之后选定的思路，以及其中涉及的概念。

最后选的组合是：**Bitwarden + rbw 管人在场的场景，OpenBao 管集群里的自动化**，没有用 SOPS。

## 先分清「存放」和「使用」

讨论密钥放在哪里时，容易把两件事混在一起：

```text
存放（数据源，长期）                    使用（临时）
git 里的密文 / Bitwarden / OpenBao  →   环境变量、内存、临时文件
```

- 使用的那一刻必然是明文，任何方案都绕不开，程序总得拿到真实值。能做的是让它**短暂、范围小**：只在一个子进程里，不长期落盘。
- 真正可以选择的是**存放**在哪里，而且不一定要是 git。

对照这个划分，原来的两个问题分别是：

| 做法 | 问题 |
| ---- | ---- |
| 明文进 git（即使是私有仓库） | 协作者授权、第三方 App 授权、CI 克隆、哪天转 public，都会把全部历史一起交出去 |
| 放在 `~/.zshrc.local` | 磁盘上是明文；shell 启动的**所有**子进程一直都能读到，包括各种 CLI、npm postinstall 脚本、AI agent |

## 分类原则：谁在用，有没有人在场

| 场景 | 存在哪里 | 怎么取 | 是否需要人在场 |
| ---- | ---- | ---- | ---- |
| 本地开发和运维（tofu、Ansible、脚本） | Bitwarden | `rbw get`，只注入单条命令 | 需要 |
| 集群自举密钥（集群启动时就必须存在的少数几个） | Bitwarden | 重建集群时，由人执行脚本创建 | 需要，只在重建时 |
| 集群里应用运行时用的密钥 | OpenBao | 程序用自己的身份去取；数据库用动态凭据 | 不需要 |

核心思路：**人在场就从 Bitwarden 取；没有人在场，就交给一个在线服务（OpenBao），程序用自己的身份去取。**

## Bitwarden + rbw：人在场的场景

### rbw 是什么

[rbw](https://github.com/doy/rbw) 是一个非官方的 Bitwarden 命令行客户端，用 Rust 写的，兼容官方服务和 Vaultwarden。它的工作方式类似 `ssh-agent`：

1. 执行 `rbw unlock`，输入一次主密码。
2. 后台的 `rbw-agent` 把解密后的密码库保存在**内存**里，超时后自动锁上。
3. `rbw get <name>` 把某一条打印到标准输出。

rbw 自己不往环境变量或文件里写任何东西。值最终落到哪里，由调用它的命令决定：

```bash
# Only this one process sees the variable
CLOUDFLARE_API_TOKEN="$(rbw get cloudflare-dns-token)" tofu apply
```

```yaml
# Ansible reads it directly, no env var at all
vars:
  cf_api_token: "{{ lookup('pipe', 'rbw get cloudflare-dns-token') }}"
```

官方的 `bw` CLI 也能做到这些，但每次都要处理 `BW_SESSION`，也比较慢，日常用 rbw 更顺手。

这样做以后，密钥不再长期存在于 git、`.env` 文件或 `.zshrc.local` 里。轮换只需要在 Bitwarden 里改一处，换机器时 Bitwarden 会自动同步。

### rbw 的风险边界

rbw 解锁期间，同一个用户下的**任何进程**都能执行 `rbw get`，读取库里的**任意一条**。两个缓解办法：

- 用 rbw 的 profile（`RBW_PROFILE`）登录一个**专门存基础设施密钥**的 Bitwarden 账号。银行、邮箱这些个人密码留在主账号里，rbw 接触不到。
- 把锁定超时 `lock_timeout` 设短一些。

即便如此，它也比 `.zshrc.local` 好：后者是长期明文，并且自动注入每一个进程。

另外，有些工具自带基于系统钥匙串的登录，比如 `gh auth login`。这种情况直接用工具自己的登录就行，不需要 rbw。

## OpenBao：集群里的自动化

集群里的程序（ArgoCD、CronJob、Pod）没有人在旁边输入主密码，所以 rbw 用不上，需要一个在线服务。

### Vault 和 OpenBao 是什么关系

- **HashiCorp Vault**：这个领域最有代表性的产品。2023 年 8 月，HashiCorp 把许可证从 MPL 2.0 改成了 BSL 1.1；2025 年 2 月 IBM 完成了对 HashiCorp 的收购。
- **OpenBao**：Vault 改许可证之后，社区基于最后一个 MPL 版本 fork 出来的项目，由 Linux Foundation 托管，许可证仍是 MPL 2.0。API 和 CLI 基本兼容 Vault，命令从 `vault` 换成 `bao`。

### 工作方式

```text
              ① 证明「我是谁」
  应用 / CI ────────────────────────► OpenBao
  (K8s Pod)    ServiceAccount token     │
                                        │ ② 认证方式（auth method）验证身份
                                        │ ③ 按策略（policy）决定能读哪些路径
                                        ▼
              ④ 拿到一个带 TTL 的 token，再用它读密钥
  应用 ◄──────────────────────────── 密钥 / 临时凭据
                                        │
                                        └─ ⑤ 每次访问都写审计日志
```

- **认证方式**：程序用平台已经给它的身份登录，比如 K8s 的 ServiceAccount token、GitHub Actions 的 OIDC。程序**不需要事先持有密码**。
- **策略**：按路径授权，比如某个应用只能读自己那一部分。
- **secrets engine**：
  - **KV**：存静态的键值对，带版本历史。
  - **动态凭据**：比如 database 引擎，应用来要数据库密码时，OpenBao 当场在 PostgreSQL 里建一个临时用户，到期后自动删除。每次拿到的账号都不一样，泄露了也很快失效。
  - **PKI**：充当内部 CA，签发短期证书。
  - **Transit**：加密即服务，应用自己不接触密钥。
- **审计日志**：谁、什么时候、读了哪个路径，全部有记录。

### 应用怎么拿到密钥

应用通常不需要改代码：

| 方式 | 说明 |
| ---- | ---- |
| External Secrets Operator / Vault Secrets Operator | 把密钥同步成 K8s Secret，Pod 照常引用 |
| Agent（sidecar 或 init container） | 负责认证，把密钥渲染成文件给应用读 |
| Secrets Store CSI Driver | 把密钥以卷的形式挂进 Pod |
| 直接调 API | 能用上动态凭据的续期，但要改代码 |

如果是 Job 或 CronJob，要用 init container 模式：常驻的 sidecar 不退出，Job 就永远不会结束。

### 适合先交给 OpenBao 的密钥

最适合入门的是**短时任务用的数据库密码**，比如每天跑一次的统计 CronJob：

- 能直接体验动态凭据，这是 SOPS 和 Bitwarden 都做不到的。
- 凭据只需要有效几十分钟，不用处理长连接续期。
- 出了问题影响很小。

## 封存与自动解封

### 为什么会有「封存」

OpenBao 存在磁盘上的数据都是加密的，钥匙分两层：

```text
磁盘上的数据  ←加密←  加密密钥  ←加密←  根密钥（root key）  ←谁来保护它？
```

根密钥不能明文放在磁盘上，否则偷走磁盘就拿到了一切。所以 OpenBao 启动时只有密文，必须有人把根密钥「交还」给它，才能开始工作，这个过程叫**解封（unseal）**。在此之前的状态叫 sealed。

### 根密钥由谁保护

| 方式 | 原理 | 重启后 |
| ---- | ---- | ---- |
| Shamir（默认） | 根密钥切成 N 片交给人保管，磁盘上不留 | 每次都要手动输入 K 片 |
| 云 KMS | 根密钥用云上的 KMS 密钥加密，那把 KMS 密钥永远不离开云厂商的硬件 | 自动 |
| HSM / PKCS#11 | 同上，换成本地硬件 | 自动 |
| Transit | 用**另一个** OpenBao 的 Transit 引擎加解密 | 自动，但那个实例本身仍需解封 |
| Static | 一把 32 字节的密钥直接通过环境变量或文件提供 | 自动 |

云 KMS 是生产环境的主流做法，因为它有两个家里没有的条件：

- 永远在线的硬件。
- 不靠密码的身份认证：云主机天生带着 IAM 身份。

这也说明了一个绕不开的事实：**任何自动解封，都要求某个地方无人值守地持有一把钥匙。** 自建 KMS 不能消除这个问题，只能把它挪到别处。

### Homelab 的做法：集群外的小 OpenBao 做 KMS

OpenBao 本身就能当 KMS 用。homelab 里可以这样做：

```text
集群外一台几乎不重启的 VM
  └─ 小 OpenBao，只开 Transit 引擎   ← 只有它需要手动解封，分片存在 Bitwarden
        ▲
        │ 自动解封
K8s 集群里的大 OpenBao              ← 节点重启、Pod 漂移都能自动恢复
```

**小 OpenBao 放进集群里是没有意义的。** 它本身需要手动解封，而集群里的 Pod 会因为节点升级、驱逐、重新调度而频繁重启。放进集群后，手动解封的次数一点没少，只是换了一个对象。另外，钥匙和数据会落在同一个集群、同一份备份里，「偷走备份也解不开」这一条也就不成立了。

### 这个结构的两类风险

| 风险 | 什么情况下发生 | 后果 |
| ---- | ---- | ---- |
| 可用性 | 小 OpenBao 挂着期间，大 OpenBao 恰好重启 | 大 OpenBao 暂时封存，小 OpenBao 恢复后自动解封。只有两边同时出问题才有影响 |
| 数据丢失 | 小 OpenBao 的磁盘坏了，而且**没有备份** | Transit key 永远丢失，大 OpenBao 的数据再也解不开 |

自动解封只在**启动那一刻**用到 KMS。所以小 OpenBao 挂了本身影响不大，真正要防的是钥匙丢失：

- 创建 Transit key 时允许导出，导出一份备份存进 Bitwarden。
- 小 OpenBao 的解封分片存在 Bitwarden。
- 大 OpenBao 定期做快照，存到集群外。

注意：用了自动解封之后，初始化时给的是 **recovery key**。它**不能**用来解封，只用于一些管理操作的授权，钥匙丢了它救不了。

### 起步时可以先用 Static seal

如果还没有一台足够稳定的独立机器，可以先用 Static seal，把动态凭据这些核心功能跑通，以后再迁移到 Transit。OpenBao 支持在不同的 seal 类型之间迁移。

| 方式 | 偷走磁盘或备份 | 整个集群被攻破 | 日常是否需要人工 |
| ---- | ---- | ---- | ---- |
| Shamir | 能防 | 能防（重启后封存） | 每次重启都要 |
| Transit（集群外） | 能防 | 部分能防 | 只在小机器重启时 |
| Static | 只要钥匙不在同一份备份里就能防 | 防不住 | 不需要 |

如果整个集群已经被攻破，攻击者可以直接读正在运行的 OpenBao 和已经同步出来的 K8s Secret。seal 方式主要防的是「磁盘或备份被拿走」。

## 自举密钥：OpenBao 管不了的那几个

有几个密钥必须在 OpenBao 启动**之前**就存在，比如：

- 大 OpenBao 连接小 OpenBao 用的 token
- GitOps 工具读取 git 仓库的 deploy key
- 私有镜像仓库的拉取凭据

它们和 OpenBao 之间存在循环依赖。我的处理方式是：存在 Bitwarden 里，**重建集群时由人执行一个脚本**，用 rbw 取值，再创建对应的 K8s Secret。集群重建本来就需要人参与，还要手动解封小 OpenBao，所以这一步不算额外负担。

代价是这几个 Secret 不声明在 git 里，要靠脚本和 RUNBOOK 保证重建时不会漏掉。

## 为什么没有用 SOPS

[SOPS](./sops.md) 的思路是把密钥加密后放进 git，它是 GitOps 圈子里很常见的方案。我比较后没有用它：

- 本地的场景都有人在场，rbw 直接从 Bitwarden 取就够了，不需要「git 里的密文」这一层。
- 集群里的场景交给 OpenBao；剩下的自举密钥数量很少，手动创建可以接受。
- 少维护一个工具，也少一把要保管的 age 私钥。

什么时候值得把它加回来：如果需要集群重建完全无人值守，或者结构化的密钥多到在 Bitwarden 里一条条维护很麻烦。SOPS 和现在的体系不冲突。

## Bitwarden 和 OpenBao 的关系

两者是**搭配**关系，不是替代关系：

| | Bitwarden（密码管理器） | OpenBao / Vault |
| ---- | ---- | ---- |
| 主要用户 | 人 | 程序 |
| 使用方式 | 浏览器自动填充、App、CLI | API，自动认证、自动续期 |
| 动态凭据、内部 CA | 没有 | 有 |
| 在本方案里的角色 | 信任根：解封分片、Transit key 备份、自举密钥、本地 token | 集群里的程序运行时用的密钥 |

容易混淆的一点：Bitwarden 另外还有一个 **Secrets Manager** 产品，是给程序用的，有机器账号，有免费档。它和 OpenBao 的 KV 部分有重叠，但没有动态凭据、PKI、Transit。另外，自建的 Vaultwarden 不支持 Secrets Manager。

### 收费与开源

| 产品 | 许可证 | 开源（OSI 定义） | 费用 |
| ---- | ---- | ---- | ---- |
| HashiCorp Vault Community | BSL 1.1 | 否，属于 source-available | 免费 |
| HashiCorp Vault Enterprise / HCP | 商业许可 | 否 | 收费 |
| OpenBao | MPL 2.0 | 是 | 免费 |
| Bitwarden | 主体为 GPL/AGPL | 主体是 | 个人免费版就够用，高级档位收费 |
| Vaultwarden | AGPL 3.0 | 是 | 免费，非官方的兼容服务端 |

## 参考

- [rbw](https://github.com/doy/rbw)
- [OpenBao](https://openbao.org/)
- [OpenBao seal configuration](https://openbao.org/docs/configuration/seal/)
- [OpenBao seal concepts](https://openbao.org/docs/concepts/seal/)
- [HashiCorp Vault 文档](https://developer.hashicorp.com/vault/docs)
- [Bitwarden Secrets Manager Plans](https://bitwarden.com/help/secrets-manager-plans/)
