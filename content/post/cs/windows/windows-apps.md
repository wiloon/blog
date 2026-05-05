---
title: Windows apps
author: "-"
date: 2026-05-05T14:02:11+08:00
url: windows/apps
categories:
  - Desktop
tags:
  - remix
  - AI-assisted
---

## Windows Apps

跨平台常用软件统一维护于 [my apps](my-apps)，本文只记录 Windows 专属工具。

## 说明

- `winget` — `winget install <id>`
- `choco` — `choco install <name>`

## Essentials

跨平台工具见 [my apps](my-apps)，以下为 Windows 专属推荐：

| app | install | notes |
| --- | --- | --- |
| Windows Terminal | winget:Microsoft.WindowsTerminal | |
| PowerToys | winget:Microsoft.PowerToys | |
| WSL2 | — | `wsl --install` |
| T-Clock | — | 任务栏显示周数，[GitHub](https://github.com/White-Tiger/T-Clock/wiki) |

## Disk Analysis

| app | install | notes |
| --- | --- | --- |
| WizTree | — | 硬盘占用分析，商用收费 |
| SpaceSniffer | — | 硬盘占用分析，商用友好 |
| WinDirStat | — | |

## Partition

| app | install | notes |
| --- | --- | --- |
| MiniTool Partition Wizard | — | 磁盘分区工具 |

## Remote Desktop

| app | install | notes |
| --- | --- | --- |
| AnyDesk | winget:AnyDesk.AnyDesk | 远程桌面 |
| ToDesk | — | 远程桌面 |
| MobaXterm | — | SSH client + X server |
| WinSCP | winget:WinSCP.WinSCP | SFTP/SCP 客户端 |

## System Tools

| app | install | notes |
| --- | --- | --- |
| Process Hacker | choco:processhacker | 任务管理器替代 |
| Open Hardware Monitor | — | 监控温度/内存 |
| PowerToys | winget:Microsoft.PowerToys | |
| Windows Terminal | winget:Microsoft.WindowsTerminal | |
| taskmgr | — | `C:\Windows\System32\Taskmgr.exe` |

## X Server

| app | install | notes |
| --- | --- | --- |
| x410 | — | X server，Microsoft Store |
| VcXsrv | choco:vcxsrv | X server |

## Misc

| app | install | notes |
| --- | --- | --- |
| T-Clock | — | 任务栏时钟（显示周数），格式：`mm-dd HH:nn \nW Wi ddd` |
| rufus | choco:rufus | 创建启动盘，ISO to USB |
| WSL2 | — | `wsl --install` |

## winget packages

```bash
winget install Microsoft.WindowsTerminal
winget install Microsoft.PowerToys
winget install WinSCP.WinSCP
winget install Mozilla.Firefox
winget install Microsoft.PowerShell
winget install cURL.cURL
```

## choco packages

```bash
# 安装
choco install keepassxc
# 升级
choco upgrade keepassxc
```

| name | notes |
| --- | --- |
| keepassxc | |
| microsoft-windows-terminal | |
| winscp | |
| heidisql | MySQL 客户端 |
| redis-desktop-manager | |
| processhacker | |
| vcxsrv | X server |

## 录屏

- [v1tx 录屏工具推荐](https://www.v1tx.com/post/best-screen-recorder/)

## winget

```bash
winget install Microsoft.WindowsTerminal
```

- Microsoft.WindowsTerminal
- WinScp, WinSCP.WinSCP
- firefox, Mozilla.Firefox
- powershell, Microsoft.PowerShell
- curl, cURL.cURL
- Golang, GoLang.Go
- Tabby, Eugeny.Tabby
- nodejs, OpenJS.NodeJS

### choco

```bash
# 安装软件，重复执行只会检查是否安装不会升级版本
choco install keepassxc
# 升级软件到新版本
choco upgrade keepassxc
```

[https://blog.wiloon.com/?p=8340](https://blog.wiloon.com/?p=8340)  
[https://chocolatey.org/packages](https://chocolatey.org/packages)  

### chocolatey packages

| Name                       | 备注                  |
| -------------------------- | --------------------- |
| chocolatey                 | choco可以自己更新自己   |
| keepassxc                  |                       |
| microsoft-windows-terminal | 1.12.10393.0          |
| winscp                     |                       |
| vnote.portable             | 支持markdown和puml的文本编辑器 |
| vscode                     | Visual Studio Code    |
|notepadplusplus||
|puyyt||
|telegraf||
|redis-desktop-manager||
|heidisql||

### 录屏

[https://www.v1tx.com/post/best-screen-recorder/](https://www.v1tx.com/post/best-screen-recorder/)

- apps

| Name             | Comments |
| ---------------- | -------- |
| MobaXterm                 |ssh client|
| Open Hardware Monitor     | 监控,温度,内存 |
| WizTree | 硬盘占用分析 |
|Process Hacker|代替任务管理器|
|chrome||
|rufus|创建启动盘,iso to usb |
|foxmail||
|TortoiseSVN||
|powershell||
| gradle           |                    |
| notepad++        |                    |
| wlstty           |                    |
| docker desktop   |                    |
| eclipse          |                    |
| subclipse        |                    |
| alacritty        |                    |
| Windows Terminal |                    |
| wsl2             |                    |
|x410              | x server           |
|T-Clock           | 可以显示周数的任务栏时钟, 格式模板: "mm-dd HH:nn \nW Wi ddd", [https://github.com/White-Tiger/T-Clock/wiki](https://github.com/White-Tiger/T-Clock/wiki) |
|VcXsrc            | x server           |
|PowerToys||
|截图工具|搜索 截图工具|

MobaXterm

wps/liberoffice
  
xmind
  
picpick

base64tools
  
everything
  
fiddler
  
jd-gui
  
logdecode
  
navicat
  
putty
  
puttygen
  
puttyng
  
visualbox

avirnt

steam

cooledit
