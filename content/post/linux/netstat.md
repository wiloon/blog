---
title: netstat 命令
author: "-"
date: 2026-04-23T06:15:22+08:00
url: netstat
categories:
  - Linux
tags:
  - remix
  - AI-assisted
---

`netstat` 用于查看网络连接、路由表、接口统计等信息。在较新的 Linux 发行版中，推荐使用 `ss` 命令替代。

## 常用命令

```bash
# 查看所有 TCP 监听端口及对应进程
netstat -ntlp

# 过滤特定端口
netstat -tulpn | grep 9100
```

## 常用选项

| 选项 | 说明 |
| --- | --- |
| `-n` | 以 IP 地址代替主机名显示 |
| `-t` | 显示 TCP 协议的连接情况 |
| `-u` | 显示 UDP 协议的连接情况 |
| `-l` | 只显示监听状态的 Socket |
| `-p` | 显示使用该 Socket 的程序名称和 PID |
| `-a` | 显示所有 Socket（包括监听和非监听） |

## 安装

`netstat` 包含在 `net-tools` 包中：

```bash
# RHEL/CentOS
yum install net-tools

# Debian/Ubuntu
apt install net-tools
```
