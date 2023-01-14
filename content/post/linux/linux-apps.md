---
title: linux apps
author: "w10n"
date: 2022-04-04 17:43:03
url: linux/apps
categories:
  - Linux
tags:
  - remix
---
## linux apps

## pacman

- ncdu, 磁盘空间占用分析/清理
- bitwarden, password management
- btop, 另外一个 top 实现, 颜值还不错

## AUR

- joplin-desktop

## application list

<https://wiki.archlinux.org/index.php/List_of_applications>

```bash
# apps
sudo pacman -S code go jdk-openjdk openjdk-src \
maven gradle openvpn nftables zstd chromium \
git jdk8-openjdk openjdk8-src kotlin docker

# kde
sudo pacman -S powerdevil kmix kscreen ark
```

## archlinux pacman

| name                  | comments                                                                                |
| :-------------------- | :-------------------------------------------------------------------------------------- |
| thunderbird           | 邮件客户端|
| obsidian              | 知识管理 |
| flameshot             | 截图工具 screenshot                                                                     |
| netdata               | 系统资源监控                                                                            |
| qalculate-gtk         | 全宇宙最好用的计算器                                                                    |
| neofetch              | 系统信息显示命令行脚本, Neofetch 和 ScreenFetch 或者 Linux_Logo 很像，但是它可以高度定制          |
| screenfetch           | 打印发行版的 logo                                                                            |
| keepassxc             |                                                                                         |
| sqlectron-gui         |                                                                                         |
| hyper                 |                                                                                         |
| code                  | visual studio code, vscode                                                              |
| rsibreak              | 番茄钟                                                                                   |
| libreoffice-fresh     |                                                                                         |
| ark                   | kde dolphin extract zip,gz                                                              |
| wine                  | 需要开启 Multilib 仓库                                                                    |
| simplescreenrecorder  | 录屏                                                                                    |
| openvpn               |                                                                                         |
| rdesktop              |                                                                                         |
| pulseaudio            |                                                                                         |
| hexyl                 | 彩色hex编辑器                                                                           |
| nftables              |                                                                                         |
| zeitgeist             |                                                                                         |
| catfish               |                                                                                         |
| thunar-archive-plugin | thunar 右键解压文件                                                                     |
| file-roller           | zip 7z rar support                                                                      |
| zstd                  | 多线程，速度比较快的压缩工具, archlinux在用                                             |
| digikam               | : KDE 环境下最好的选择                                                                  |
| chromium              | 开源版chrome                                                                            |
| kvm                   |                                                                                         |
| kotlin                |                                                                                         |
| docker                |                                                                                         |
| hdparm                | 磁盘参数查看工具                                                                        |
| Deluge                | bt client docker                                                                        |
| aria2                 | 下载工具                                                                                |
| axel                  | 下载工具                                                                                |
| inetutils             | telnet client                                                                           |
| zeal                  | 离线文档                                                                                |
| wireshark-qt          | Wireshark                                                                               |
| lsof                  |                                                                                         |
| playonlinux           | Wine软件兼容层的图形前端，允许Linux安装基于Windows的应用程序                            |
| podman                |                                                                                         |
| v2ray                 |                                                                                         |
| nethogs               |                                                                                         |
| ttf-jetbrains-mono    | jetbrain的mono字体                                                                      |
| gpick                 | 颜色拾取工具                                                                            |
| telegram-desktop      | telegram                                                                                |
| apper                 | pacman GUI                                                                              |
| dstat                 | 查看系统性能的工具 dstat -cdlmnpsy                                                      |
| sl                    | 小火车                                                                                  |
| inkscape              | 矢量图形创建和编辑程序,svg                                                              |
| lrzsz                 | zmodem                                                                                  |
| remmina               | GTK 编写的远程桌面客户端                                                                |
| freerdp               | remmina 的RDP 支持包                                                                     |
| pycharm               |                                                                      |
|cmake||
|linux-lts|lts 内核|
|filelight|图形化的磁盘空间管理工具|
|okular|pdf reader|
|audacity|一款免费的音频处理软件。它是在linux下发展起来的，一款遵循GNU协议的免费软件。有着傻瓜式的操作界面和专业的音频处理效果。|
|python-pip||

## pacman, development

| name                            | comments          |
| :------------------------------ | :---------------- |
| graphviz                        | plantuml依赖的包, /opt/local/bin/dot              |
| jdk-openjdk                     | latest openjdk    |
| jdk8-openjdk                    | openjdk 8         |
| openjdk8-src                    | openjdk 8 source  |
| intellij-idea-community-edition | IDEA社区版        |
| maven                           |                   |
| gradle                          |                   |
| gradle-src                      |                   |
| git                             |                   |
| rust                            | rust-lang         |
| iperf3                          | 网络测试工具      |
| termite                         | 支持32位色的终端  |
| neovim                          | 用户体验更好的vim |
| adobe-source-code-pro-fonts     | adobe 的编程字体  |
| tmux                            |                   |

## AUR table

| name                                  | comments                                                                 |
| :------------------------------------ | :-------------------------------------------------------------           |
| intellij-idea-ultimate-edition        | yay -S intellij-idea-ultimate-edition intellij-idea-ultimate-edition-jre |
| telegraf-bin                          |                                                                          |
| goland                                | yay -S goland goland-jre, 两个一起安装                                     |
| webstorm-jre                          | yay -S webstorm webstorm-jre                                             |
| clion                                 | yay -S clion clion-jre                                                   |
| google-chrome                         |                                                                          |
| deepin-wine-wechat                    | 微信,<https://github.com/countstarlight/deepin-wine-wechat-arch>          |
| google-chrome-beta                    |                                                                          |
| redis-desktop-manager                 | rdm                                                                      |
| wps-office                            | 依赖                                                                      |
| ttf-wps-fonts                         | wps字体                                                                   |
| nixnote2-git                          | evernote linux 客户端                                                     |
| gitkraken                             | git GUI clinet, Free for non-commercial use                              |
| github-desktop-bin                    | MIT Linense                                                              |
| heidisql                              | MySQL客户端                                                               |
| jd-gui-bin                            | java反编译                                                                |
| eclipse-mat                           | Eclipse Memory Analyzer (MAT)                                            |
| dingtalk                              | 钉钉                                                                      |
| menulibre                             | xfce的系统菜单管理工具                                                      |
| ttf-consolas-with-yahei-powerline-git | Consolas-with-Yahei字体                                                   |
| zoom                                  |                                                                |
| shutter                               |                                                                |
| perl-goo-canvas                       | shutter 的画线插件                                             |
| google-chrome-dev                     |                                                                |
| intellij-idea-community-edition-jre   | idea with jre                                                  |
| tableplus                             | MySQL client                                                   |
| procmon                               | 微软的进程监控工具                                             |
| platformio                            | 物联网开发的开源生态系统                                       |
| slurm                                 | 网络监控                                                       |
| joplin-desktop                        |                                                                |
| typora                                | markdown 编辑器，joplin 外部编辑器                             |
| feishu                                | 飞书                                                           |
|libiconv |编码转换|
|hardinfo-git|HardInfo是一个Linux系统信息查看软件。它可以显示有关的硬件，软件，并进行简单的性能基准测试。|
| vscodium-bin|vscode 社区版|
|gtk-recordmydesktop|录屏|

## KDE

| name          | comments             |
| ------------- | -------------------- |
| powerdevil    | 电源管理，休眠按钮   |
| kmix          | 音量调节             |
| ark           | 压缩包管理器         |
| gwenview      | 图片查看             |
| kscreen       | kde 多显示器管理工具 |
| kcolorchooser | 颜色拾取             |

## KDE widget

| name               | comments                   |
| ------------------ | -------------------------- |
| netspeed widget    | 网络监控                   |
| resources monitor  | CPU, 内存 监控             |
| Plasma Week Number | 显示周数                   |
| rsibreak           | 蕃茄钟, install via pacman |

## ubuntu

| Name             | Comments                                                    |
| ---------------- | ----------------------------------------------------------- |
| openjdk-8-jdk    |                                                             |
| openjdk-8-source |                                                             |
| git-svn          |                                                             |
| nautilus         | ubuntu默认的文件管理器                                      |
| ttf-wqy-microhei | 文泉驿-微米黑                                               |
| ttf-wqy-zenhei   | 文泉驿-正黑                                                 |
| xfonts-wqy       | 文泉驿-点阵宋体                                             |
| keepassxc        |                                                             |
| eog              | Eye of Gnome, 图片查看                                      |
| neofetch         | 发行版logo                                                  |
| tree             | 以树型结构显示文件目录结构, tree -L N 子文件夹显示到第 N 层 |
| x11-apps         | xclock, xserver 测试用                                      |
| rar ||
| unrar ||

### ubuntu install chrome

```bash
curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

### xfce4

file-roller

### tar

| Name   | Comments              |
| ------ | --------------------- |
| Ventoy | 各种iso安装盘引导工具 |
| jetbrains-toolbox ||

### openwrt

| Name    | Comments |
| ------- | -------- |
| drill   |          |
| openwrt |          |

## other

| Name    | Comments |
| ------- | -------- |
| datagrip   |          |
| Joplin | Joplin.AppImage         |

## raspberry pi

omxplayer
