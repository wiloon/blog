---
title: wsl native docker windows vscode hack
author: "-"
date: 2025-06-26 15:15:24
url: wsl-docker-win-vscode
categories:
  - Linux
tags:
  - reprint
  - remix

---
## wsl native docker windows vscode hack

wsl archlinux install containerd nerdctl

nerdctl 和 containerd 使用 Unix socket一般在 /run/containerd/containerd.sock

在 WSL 里启动 socat 监听 containerd.socket，转发到 Windows 命名管道

```bash
sudo mkdir -p /mnt/wsl/shared-containerd
sudo ln -sf /run/containerd/containerd.sock /mnt/wsl/shared-containerd/containerd.sock

socat UNIX-LISTEN:/mnt/wsl/shared-containerd/containerd.sock,fork EXEC:"/mnt/c/workspace/apps/npiperelay.exe -ei -ep -s //./pipe/containerd_engine"
```
