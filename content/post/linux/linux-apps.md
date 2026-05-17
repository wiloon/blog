---
title: linux apps
author: "w10n"
date: 2026-05-05T14:02:11+08:00
url: linux/apps
categories:
  - Linux
tags:
  - original
  - AI-assisted
aliases:
  - /p4157/
---

## Linux Apps

跨平台常用软件统一维护于 [my apps](my-apps)，本文只记录 Linux 专属工具。

## 说明

- `pacman` — `sudo pacman -S`
- `aur` — `yay -S`
- `apt` — `sudo apt install`

## Essentials

跨平台工具详见 [my apps](my-apps)，以下是 Linux 上的安装命令速查：

| app | source | notes |
| --- | --- | --- |
| kitty | pacman | terminal |
| neovim | pacman | 编辑器 |
| flameshot | pacman | 截图+标注 |
| bitwarden | pacman | 密码管理 |
| btop | pacman | top 替代 |
| wechat | aur | |
| visual-studio-code-bin | aur | VSCode 官方二进制版 |

## Browser

### Ubuntu install Chrome

```bash
curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

## Terminal

| app     | source | notes      |
| ------- | ------ | ---------- |
| termite | pacman | 支持 32 位色 |

## Text Editor

| app          | source | notes          |
| ------------ | ------ | -------------- |
| mousepad     | pacman | 轻量文本编辑器 |
| nixnote2-git | aur    | Evernote Linux 客户端 |

## Screenshot / Recording

| app                  | source | notes                        |
| -------------------- | ------ | ---------------------------- |
| spectacle            | pacman | KDE 原生截图                 |
| simplescreenrecorder | pacman | 录屏                         |
| gtk-recordmydesktop  | aur    | 录屏                         |
| shutter              | aur    | 截图，需配合 perl-goo-canvas |

## System Monitor

| app                  | source     | notes                          |
| -------------------- | ---------- | ------------------------------ |
| ncdu                 | pacman/apt | 命令行磁盘空间分析             |
| netdata              | pacman     | 系统资源监控                   |
| indicator-sysmonitor | apt        | 任务栏系统资源监控             |
| nethogs              | pacman     | 网络流量监控                   |
| dstat                | pacman     | 查看系统性能 `dstat -cdlmnpsy` |
| slurm                | aur        | 网络监控                       |
| hardinfo-git         | aur        | 硬件信息查看                   |

## System Info

| app       | source     | notes                  |
| --------- | ---------- | ---------------------- |
| fastfetch | pacman     | 打印发行版 logo        |
| neofetch  | pacman/apt | 系统信息（已停止维护） |
| stress    | pacman     | 压力测试               |
| hdparm    | pacman     | 磁盘参数查看           |
| procmon   | aur        | 微软的进程监控工具     |

## File Management

| app       | source | notes                    |
| --------- | ------ | ------------------------ |
| filelight | pacman | 图形化磁盘空间管理       |
| baobab    | apt    | 硬盘占用分析工具         |
| catfish   | pacman | 文件搜索                 |
| tree      | apt    | 树形目录显示 `tree -L N` |
| nautilus  | apt    | Ubuntu 默认文件管理器    |

## Archive / Compression

| app         | source | notes            |
| ----------- | ------ | ---------------- |
| ark         | pacman | KDE 压缩包管理器 |
| file-roller | pacman | zip/7z/rar 支持  |
| rar/unrar   | apt    |                  |

## Media / Graphics

| app      | source | notes                 |
| -------- | ------ | --------------------- |
| digikam  | pacman | KDE 最佳图片管理      |
| gwenview | pacman | KDE 图片查看          |
| eog      | apt    | Eye of Gnome 图片查看 |
| okular   | pacman | PDF reader            |
| gpick    | pacman | 颜色拾取工具          |

## Remote Desktop

| app      | source | notes              |
| -------- | ------ | ------------------ |
| remmina  | pacman | GTK 远程桌面客户端 |
| freerdp  | pacman | remmina RDP 支持包 |
| rdesktop | pacman |                    |

## Development Tools

| app        | source | notes            |
| ---------- | ------ | ---------------- |
| base-devel | pacman | 编译工具链       |
| lsof       | pacman |                  |
| hexyl      | pacman | 彩色 hex 编辑器  |
| lrzsz      | pacman | zmodem           |
| binutils   | pacman | 二进制文件处理工具集 |
| inetutils  | pacman | telnet 等网络工具 |
| kotlin     | pacman |                  |

## Fonts

| app                                   | source | notes           |
| ------------------------------------- | ------ | --------------- |
| ttf-wqy-microhei                      | apt    | 文泉驿-微米黑   |
| ttf-wqy-zenhei                        | apt    | 文泉驿-正黑     |
| xfonts-wqy                            | apt    | 文泉驿-点阵宋体 |
| ttf-consolas-with-yahei-powerline-git | aur    | Consolas+雅黑   |
| ttf-wps-fonts                         | aur    | WPS 字体依赖    |

## KDE

```bash
sudo pacman -S powerdevil kmix kscreen ark gwenview kcolorchooser
```

| app           | source | notes              |
| ------------- | ------ | ------------------ |
| powerdevil    | pacman | 电源管理，休眠按钮 |
| kmix          | pacman | 音量调节           |
| kscreen       | pacman | 多显示器管理       |
| kcolorchooser | pacman | 颜色拾取           |

### KDE Widget

| name               | notes        |
| ------------------ | ------------ |
| netspeed widget    | 网络监控     |
| resources monitor  | CPU/内存监控 |
| Plasma Week Number | 显示周数     |

## Virtualization

| app         | source | notes                |
| ----------- | ------ | -------------------- |
| kvm         | pacman |                      |
| wine        | pacman | 需开启 Multilib 仓库 |
| playonlinux | pacman | Wine 图形前端        |
| podlet      | aur    | podman 辅助工具      |

## Utilities

| app                  | source | notes                   |
| -------------------- | ------ | ----------------------- |
| rsibreak             | pacman | 番茄钟                  |
| gnome-shell-pomodoro | apt    | Pomodoro                |
| pavucontrol          | apt    | Chrome 音频输出设置     |
| sl                   | pacman | 小火车                  |
| x11-apps             | apt    | xclock, xserver 测试用  |
| pamac-aur            | aur    | 图形界面的 pacman       |
| libiconv             | aur    | 编码转换                |
| Ventoy               | —      | 各种 ISO 安装盘引导工具 |

## References

- [Arch Linux List of Applications](https://wiki.archlinux.org/index.php/List_of_applications)
