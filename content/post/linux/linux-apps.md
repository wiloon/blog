---
title: linux apps
author: "w10n"
date: 2026-04-03T09:04:50+08:00
url: linux/apps
categories:
  - Linux
tags:
  - original
  - remix
  - AI-assisted
---
## 必装软件（重装系统后优先安装）

| app       | source | notes          |
| --------- | ------ | -------------- |
| kitty     | pacman | terminal       |
| neovim    | pacman | 编辑器         |
| flameshot | pacman | 截图+标注      |
| bitwarden | pacman | 密码管理       |
| btop                 | pacman     | 颜值不错的 top 替代            |
| wechat           | aur    |            |
| visual-studio-code-bin          | aur    | VSCode 官方二进制版                                                        |

## 说明

- `pacman` — `sudo pacman -S`
- `aur` — `yay -S`
- `apt` — `sudo apt install`
- `go` — `go install`

## Browser

| app                | source | notes          |
| ------------------ | ------ | -------------- |
| chromium           | pacman | 开源版 Chrome  |
| google-chrome      | aur    |                |
| google-chrome-beta | aur    |                |
| google-chrome-dev  | aur    |                |

### ubuntu install chrome

```bash
curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

## Terminal

| app     | source | notes         |
| ------- | ------ | ------------- |
| hyper   | pacman | terminal      |
| termite | pacman | 支持32位色    |
| tmux    | pacman |               |

## Text Editor / Notes

| app          | source | notes                 |
| ------------ | ------ | --------------------- |
| mousepad     | pacman | 轻量文本编辑器        |
| typora       | aur    | markdown 编辑器       |
| obsidian     | pacman | 知识管理              |
| nixnote2-git | aur    | Evernote Linux 客户端 |

## Screenshot / Recording

| app                  | source     | notes                        |
| -------------------- | ---------- | ---------------------------- |
| spectacle            | pacman     | KDE 原生截图                 |
| simplescreenrecorder | pacman     | 录屏                         |
| gtk-recordmydesktop  | aur        | 录屏                         |
| shutter              | aur        | 截图，需配合 perl-goo-canvas |

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

| app         | source | notes              |
| ----------- | ------ | ------------------ |
| ark         | pacman | KDE 压缩包管理器   |
| file-roller | pacman | zip/7z/rar 支持    |
| zstd        | pacman | 多线程快速压缩工具 |
| rar/unrar   | apt    |                    |

## Media / Graphics

| app      | source | notes                 |
| -------- | ------ | --------------------- |
| digikam  | pacman | KDE 最佳图片管理      |
| gwenview | pacman | KDE 图片查看          |
| eog      | apt    | Eye of Gnome 图片查看 |
| inkscape | pacman | 矢量图形编辑，SVG     |
| audacity | pacman | 音频处理              |
| okular   | pacman | PDF reader            |
| gpick    | pacman | 颜色拾取工具          |

## Download

| app   | source | notes    |
| ----- | ------ | -------- |
| aria2 | pacman | 下载工具 |
| axel  | pacman | 下载工具 |

## Remote Desktop

| app      | source | notes              |
| -------- | ------ | ------------------ |
| remmina  | pacman | GTK 远程桌面客户端 |
| freerdp  | pacman | remmina RDP 支持包 |
| rdesktop | pacman |                    |

## Communication

| app              | source | notes      |
| ---------------- | ------ | ---------- |
| thunderbird      | apt    | 邮件客户端 |
| telegram-desktop | pacman |            |
| feishu           | aur    | 飞书       |
| dingtalk         | aur    | 钉钉       |
| zoom             | aur    |            |

## Office

| app               | source | notes            |
| ----------------- | ------ | ---------------- |
| libreoffice-fresh | pacman |                  |
| wps-office        | aur    | 需 ttf-wps-fonts |
| ttf-wps-fonts     | aur    | WPS 字体依赖     |

## Development Tools

| app                | source     | notes                                                |
| ------------------ | ---------- | ---------------------------------------------------- |
| git                | pacman/apt |                                                      |
| lazygit            | go         | `go install github.com/jesseduffield/lazygit@latest` |
| gitkraken          | aur        | Git GUI，Free for non-commercial                     |
| github-desktop-bin | aur        |                                                      |
| base-devel         | pacman     | 编译工具链                                           |
| cmake              | pacman     |                                                      |
| kotlin             | pacman     |                                                      |
| iperf3             | pacman     | 网络测试                                             |
| wireshark-qt       | pacman     |                                                      |
| lsof               | pacman     |                                                      |
| hexyl              | pacman     | 彩色 hex 编辑器                                      |
| lrzsz              | pacman     | zmodem                                               |
| binutils           | pacman     | 二进制文件处理工具集                                 |
| inetutils          | pacman     | telnet 等网络工具                                    |
| zeal               | pacman     | 离线文档                                             |
| platformio         | aur        | 物联网开发生态系统                                   |

## IDE

| app                             | source | notes                                                                      |
| ------------------------------- | ------ | -------------------------------------------------------------------------- |
| code                            | pacman | Visual Studio Code                                                         |
| vscodium-bin                    | aur    | VSCode 社区版（无遥测）                                                    |
| jetbrains-toolbox               | aur    | JetBrains 工具管理器                                                       |
| intellij-idea-community-edition | pacman | IDEA 社区版                                                                |
| intellij-idea-ultimate-edition  | aur    | `yay -S intellij-idea-ultimate-edition intellij-idea-ultimate-edition-jre` |
| goland                          | aur    | `yay -S goland goland-jre`                                                 |
| webstorm-jre                    | aur    | `yay -S webstorm webstorm-jre`                                             |
| clion                           | aur    | `yay -S clion clion-jre`                                                   |
| claude-code                     | aur    |                                                                            |

## Java

| app           | source | notes                   |
| ------------- | ------ | ----------------------- |
| jdk-openjdk   | pacman | Latest OpenJDK          |
| jdk8-openjdk  | pacman | OpenJDK 8               |
| openjdk8-src  | pacman | OpenJDK 8 源码          |
| openjdk-8-jdk | apt    | OpenJDK 8               |
| maven         | pacman |                         |
| gradle        | pacman |                         |
| graphviz      | pacman | PlantUML 依赖           |
| jd-gui-bin    | aur    | Java 反编译             |
| eclipse-mat   | aur    | Eclipse Memory Analyzer |

## Node.js / Rust

| app  | source | notes            |
| ---- | ------ | ---------------- |
| nvm  | pacman | Node.js 版本管理 |
| rust | pacman |                  |

## Database

| app                   | source | notes        |
| --------------------- | ------ | ------------ |
| redisinsight          | aur    | Redis GUI    |
| redis-desktop-manager | aur    | RDM          |
| sqlectron-gui         | pacman |              |
| heidisql              | aur    | MySQL 客户端 |
| tableplus             | aur    | MySQL client |
| datagrip              | —      | 官网下载     |

## Fonts

| app                                   | source | notes           |
| ------------------------------------- | ------ | --------------- |
| ttf-jetbrains-mono                    | pacman | JetBrains Mono  |
| adobe-source-code-pro-fonts           | pacman | Adobe 编程字体  |
| ttf-wqy-microhei                      | apt    | 文泉驿-微米黑   |
| ttf-wqy-zenhei                        | apt    | 文泉驿-正黑     |
| xfonts-wqy                            | apt    | 文泉驿-点阵宋体 |
| ttf-consolas-with-yahei-powerline-git | aur    | Consolas+雅黑   |

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

| name               | notes         |
| ------------------ | ------------- |
| netspeed widget    | 网络监控      |
| resources monitor  | CPU/内存监控  |
| Plasma Week Number | 显示周数      |

## Virtualization / Container

| app         | source | notes                |
| ----------- | ------ | -------------------- |
| docker      | pacman |                      |
| podman      | pacman |                      |
| podlet      | aur    |                      |
| kvm         | pacman |                      |
| wine        | pacman | 需开启 Multilib 仓库 |
| playonlinux | pacman | Wine 图形前端        |

## Utilities

| app                  | source | notes                   |
| -------------------- | ------ | ----------------------- |
| qalculate-gtk        | pacman | 全宇宙最好用的计算器    |
| rsibreak             | pacman | 番茄钟                  |
| gnome-shell-pomodoro | apt    | Pomodoro                |
| openvpn              | pacman |                         |
| pavucontrol          | apt    | Chrome 音频输出设置     |
| sl                   | pacman | 小火车                  |
| x11-apps             | apt    | xclock, xserver 测试用  |
| pamac-aur            | aur    | 图形界面的 pacman       |
| libiconv             | aur    | 编码转换                |
| Ventoy               | —      | 各种 ISO 安装盘引导工具 |

## References

- [Arch Linux List of Applications](https://wiki.archlinux.org/index.php/List_of_applications)
