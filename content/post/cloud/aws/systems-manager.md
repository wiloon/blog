---
title: AWS Systems Manager（Run Command）
author: "-"
date: 2026-05-19T14:57:50+08:00
lastmod: 2026-05-19T14:57:50+08:00
url: aws-systems-manager
categories:
  - cloud
tags:
  - AI-assisted
  - aws
  - remix
  - ssm
  - systems-manager
---

## 概述

**AWS Systems Manager（简称 SSM）** 是 AWS 的**运维管理平台**：在 EC2、混合机上远程执行命令、打补丁、收集清单、免 SSH 登录等。

本文只聚焦备份场景里用到的一块：**Run Command（运行命令）**——通过 API 在实例上执行脚本，无需 SSH。

## 核心组件

| 组件                     | 说明                                                                   |
|--------------------------|------------------------------------------------------------------------|
| **SSM Agent**            | 装在 EC2 上的代理，接收并执行 Run Command（Amazon Linux 2023 通常已预装） |
| **Managed Instance**     | 已向 Systems Manager 注册的实例（Agent 在线 + IAM 权限正确）             |
| **Command document**     | 命令模板；常用内置文档 `AWS-RunShellScript`（跑 shell）                   |
| **SendCommand**          | API：对一台或多台实例下发命令                                             |
| **GetCommandInvocation** | API：查询某台实例上该次命令的执行结果                                      |

```text
调用方（Lambda / CLI / 控制台）
  → SendCommand（指定 InstanceId + Document + 命令）
  → SSM Agent 在 EC2 上执行
  → GetCommandInvocation 查看 Success / Failed / 输出
```

## 与 SSH 的对比

|        | **SSH**            | **SSM Run Command**               |
|--------|--------------------|-----------------------------------|
| 网络   | 通常要开放 22 端口 | 走 Agent 出站 HTTPS，**不必开 22** |
| 凭证   | SSH 密钥 / 密码    | **IAM** 授权谁可以 SendCommand    |
| 调用方 | 人要登录或脚本 ssh | Lambda、CLI、控制台均可             |
| 适合   | 交互式排错         | **自动化**、批量、审计              |

**Session Manager** 是同一产品族里的**交互式终端**（浏览器里连 shell）；Run Command 是**非交互、一次一条命令**。

## 前置条件（EC2）

1. 实例上 **SSM Agent 在运行**（`systemctl status amazon-ssm-agent`）
2. 实例有 **出站访问** `ssm.*.amazonaws.com` 等端点（公有子网或 NAT 即可）
3. EC2 **IAM Instance Profile** 至少包含托管策略 **`AmazonSSMManagedInstanceCore`**

没有第 3 条时，实例不会出现在 Fleet Manager / Run Command 目标列表里。

## 实践：Lambda 远程跑备份脚本

[EventBridge Scheduler](./eventbridge-scheduler.md) 触发 Lambda，Lambda 用 SSM 在东京 EC2 上执行 `enx-api-backup.sh`（详见 enx 项目 `DATABASE_BACKUP.md`）：

```text
Scheduler → Lambda enx-api-backup
              → ssm.send_command(AWS-RunShellScript, /usr/local/bin/enx-api-backup.sh)
              → 轮询 GetCommandInvocation 直到 Success / Failed
```

Lambda 侧 IAM 需要（资源缩放到目标实例）：

- `ssm:SendCommand`
- `ssm:GetCommandInvocation`

调用方**不需要** EC2 的 SSH 密钥。

### Python 示例（节选）

```python
ssm = boto3.client("ssm")
resp = ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName="AWS-RunShellScript",
    Parameters={"commands": ["/usr/local/bin/enx-api-backup.sh"]},
)
command_id = resp["Command"]["CommandId"]

inv = ssm.get_command_invocation(
    CommandId=command_id,
    InstanceId=instance_id,
)
# inv["Status"]  →  Pending | InProgress | Success | Failed | ...
```

## 常用 CLI

```bash
# 对单台实例执行命令
aws ssm send-command \
  --region ap-northeast-1 \
  --instance-ids i-xxxxxxxx \
  --document-name AWS-RunShellScript \
  --parameters 'commands=["echo hello"]'

# 查询执行结果（用上一条返回的 CommandId）
aws ssm get-command-invocation \
  --region ap-northeast-1 \
  --command-id "<command-id>" \
  --instance-id i-xxxxxxxx

# 列出可被 SSM 管理的实例
aws ssm describe-instance-information --region ap-northeast-1
```

## Systems Manager 其它能力（简表）

| 能力                | 用途                                |
|---------------------|-------------------------------------|
| **Session Manager** | 免 SSH 登录实例（审计、端口转发）      |
| **Parameter Store** | 存配置与密钥（Standard 参数有免费档） |
| **Patch Manager**   | 自动化补丁                          |
| **State Manager**   | 维持配置（类似定期 Ansible）          |

备份链路**没有用到** Session Manager；密钥类配置可优先考虑 Parameter Store，而不是写进代码库。

## 计费

在 **EC2 实例**上执行 Run Command **不额外按次收费**（仍照常付 EC2 费用）。Session Manager、Parameter Store 高级参数等另有定价，见 [Systems Manager 定价](https://aws.amazon.com/systems-manager/pricing/)。

## 参考

- [AWS Systems Manager 文档](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html)
- [Run Command 工作原理](https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command.html)
- [AWS-RunShellScript 文档](https://docs.aws.amazon.com/systems-manager/latest/userguide/documents-command-ssm-plugin-reference.html)
