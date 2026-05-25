---
title: Windows OpenSSH Server 远程登录
author: "-"
date: 2026-05-25T18:47:17+08:00
lastmod: 2026-05-25T19:34:14+08:00
url: openssh-server
categories:
  - Network
tags:
  - windows
  - openssh
  - ssh
  - remix
  - AI-assisted
---

在 Windows 10（1809 及以后）和 Windows 11 上，系统自带 **OpenSSH Server**，安装并启动 **sshd** 服务后，Linux 或其他机器即可用 `ssh` 登录本机。

与 [win11 ssh agent](/win11/ssh/agent) 的区别：

| 组件 | 作用 |
| ---- | ---- |
| OpenSSH **Client** | 本机作为客户端，`ssh user@host` 连别人 |
| OpenSSH **Authentication Agent** | 管理本机私钥（`ssh-add`） |
| OpenSSH **Server** | 本机作为服务端，让别人 `ssh` 进来 |

本文只讲 **Server**。

## 安装 OpenSSH Server（英文系统）

### 方法一：设置里搜索（推荐）

1. 打开 **Settings**（`Win + I`）
2. 顶部搜索框输入 **optional features**，进入 **Optional features** / **Manage optional features**
3. 点 **View features** 或 **Add an optional feature**
4. 搜索 **openssh**，勾选 **OpenSSH Server**，安装

也可从 **Settings → Apps → Installed apps → Optional features** 进入同一路径。

### 方法二：PowerShell（管理员）

查看是否已安装（**管理员 PowerShell**）：

```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
```

看输出里的 **`State`**，不要只看有没有一行：

| State | 含义 |
| ----- | ---- |
| `Installed` | 已安装 |
| `NotPresent` | 未安装（但系统支持，可执行下面的 `Add-WindowsCapability`） |
| 完全没有输出 | **不等于**「未安装」；常见原因：未用管理员运行、`-Online` 连 Windows Update 失败、系统版本过旧不含该可选功能。可改用 `Get-Service sshd` 或设置里的 Optional features 确认 |

未安装（`NotPresent`）时执行：

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

**进度条很慢是否正常：** 正常。`-Online` 会从 **Windows Update** 拉取可选功能包，耗时取决于网络、更新服务负载和磁盘速度；进度条长时间不动也常见，OpenSSH Server 体积不大，但等 **几分钟到十几分钟** 都可能有。只要未报错就先别中断；若超过约 20 分钟仍无结果，再检查网络、系统更新是否正常，或改用设置里的 **Optional features** 图形安装（本质也是同一来源）。

也可一次查看 Client / Server：

```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
```

## 启动服务并设为开机自启

**PowerShell（管理员）：**

```powershell
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic
```

**图形界面：** `Win + R` → `services.msc` → 找到 **OpenSSH SSH Server** → 启动，启动类型选 **Automatic**。

确认 22 端口在监听：

```powershell
Get-NetTCPConnection -LocalPort 22 -ErrorAction SilentlyContinue
```

或：

```cmd
netstat -an | findstr ":22"
```

## 防火墙

安装 Server 时通常会创建入站规则 **OpenSSH SSH Server (sshd)**。若没有，在管理员 PowerShell 中：

```powershell
New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH SSH Server (sshd)' `
  -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

## 从 Linux 连接

```bash
ssh Windows用户名@Windows的IP
```

- 用户名是登录 Windows 的账户名（不是显示名）。
- 首次连接确认主机指纹后，输入 **账户密码**（空密码账户一般无法 SSH；PIN 不能代替密码用于 SSH）。
- 本机与 Windows 需网络互通（同一局域网或路由/防火墙放行 22 端口）。

## 公钥登录（可选）

在 Linux 上：

```bash
ssh-copy-id Windows用户名@Windows的IP
```

或在 Windows 用户目录创建 `C:\Users\用户名\.ssh\authorized_keys`，写入公钥（一行一条）。

**管理员账户注意：** 若用户属于 **Administrators** 组，公钥应放在 `C:\ProgramData\ssh\administrators_authorized_keys`，且仅 **SYSTEM** 和 **Administrators** 拥有读写权限；放在用户目录下的 `authorized_keys` 会被忽略。

修改密钥或配置后重启服务：

```powershell
Restart-Service sshd
```

## 配置文件（可选）

主配置：`C:\ProgramData\ssh\sshd_config`

常用项示例：

```text
PasswordAuthentication yes
PubkeyAuthentication yes
```

保存后：

```powershell
Restart-Service sshd
```

## 常见问题

| 现象 | 处理 |
| ---- | ---- |
| 连接超时 | 核对 IP、网段、Windows 防火墙、路由器是否拦截 22 |
| Permission denied | 用户名或密码错误；管理员公钥是否放在 `administrators_authorized_keys` |
| 找不到 OpenSSH Server | 用 **Optional features** 或 `Add-WindowsCapability` 安装 |
| sshd 无法启动 | **Event Viewer** → Windows Logs → Application，查看 sshd 相关错误 |

## 相关

- 本机 SSH 客户端与 **ssh-agent**：[win11 ssh agent](/win11/ssh/agent)
- Microsoft 文档：[OpenSSH for Windows overview](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_overview)
