---
title: linux apps
author: wiloon
type: post
date: 2018-09-23T05:52:02+00:00
url: /?p=12667
categories:
  - Uncategorized

---
<pre><code class="language-bash line-numbers"># apps
sudo pacman -S code go jdk-openjdk openjdk-src \
maven gradle openvpn nftables zstd chromium \
git jdk8-openjdk openjdk8-src kotlin docker

# for PC
sudo pacman -S wine rdesktop pulseaudio

# kde
sudo pacman -S powerdevil kmix kscreen ark
</code></pre>

### pacman:

| name                  | comments                               |
|:--------------------- |:-------------------------------------- |
| screenfetch           | 发行版的logo                               |
| keepassxc             |                                        |
| sqlectron-gui         |                                        |
| hyper                 |                                        |
| code                  | visual studio code                     |
| rsibreak              | 番茄钟                                    |
| libreoffice-fresh     |                                        |
| ark                   | kde dolphin extract zip&#8230;         |
| spectacle             | kde screen shot                        |
| neofetch              |                                        |
| wine                  | 需要开启Multilib仓库                         |
| qalculate-gtk         | 全宇宙最好用的计算器                             |
| simplescreenrecorder  | 录屏                                     |
| openvpn               |                                        |
| rdesktop              |                                        |
| pulseaudio            |                                        |
| hexyl                 | 彩色hex编辑器                               |
| nftables              |                                        |
| google-chrome-dev     |                                        |
| google-chrome-beta    |                                        |
| zeitgeist             |                                        |
| catfish               |                                        |
| thunar-archive-plugin | thunar 右键解压文件                          |
| file-roller           | zip 7z rar support                     |
| zstd                  | 多线程，速度比较快的压缩工具, archlinux在用            |
| digikam               | ：KDE 环境下最好的选择                          |
| chromium              | 开源版chrome                              |
| kvm                   |                                        |
| kotlin                |                                        |
| docker                |                                        |
| hdparm                | 磁盘参数查看工具                               |
| Deluge                | bt client &#8211; docker               |
| aria2                 | 下载工具                                   |
| axel                  | 下载工具                                   |
| inetutils             | telnet client                          |
| zeal                  | 离线文档                                   |
| wireshark-qt          | Wireshark                              |
| lsof                  |                                        |
| playonlinux           | Wine软件兼容层的图形前端，允许Linux安装基于Windows的应用程序 |
| xfce4-screenshooter   | xfce的截图工具                              |
| podman                |                                        |
| v2ray                 |                                        |
| nethogs               |                                        |

### pacman, dev

| name                            | comments         |
|:------------------------------- |:---------------- |
| graphviz                        |                  |
| jdk-openjdk                     | latest openjdk   |
| jdk8-openjdk                    | openjdk 8        |
| openjdk8-src                    | openjdk 8 source |
| intellij-idea-community-edition | IDEA社区版          |
| maven                           |                  |
| gradle                          |                  |
| git                             |                  |
| rust                            | rust-lang        |

### AUR, yay:

| name                                  | comments                                                                                                 |
|:------------------------------------- |:-------------------------------------------------------------------------------------------------------- |
| redis-desktop-manager                 | rdm                                                                                                      |
| wps-office                            | 依赖                                                                                                       |
| ttf-wps-fonts                         | wps字体                                                                                                    |
| heidisql                              |                                                                                                          |
| nixnote2-git                          | evernote linux 客户端                                                                                       |
| gitkraken                             | git clinet, Free for non-commercial use                                                                  |
| github-desktop-bin                    | MIT Linense                                                                                              |
| heidisql                              | mysql客户端                                                                                                 |
| jd-gui-bin                            | java反编译                                                                                                  |
| eclipse-mat                           | Eclipse Memory Analyzer (MAT)                                                                            |
| dingtalk                              | 钉钉                                                                                                       |
| menulibre                             | xfce的系统菜单管理工具                                                                                            |
| deepin-wine-wechat                    | 微信, https://github.com/countstarlight/deepin-wine-wechat-arch                   |
| ttf-consolas-with-yahei-powerline-git | Consolas-with-Yahei字体                                                                                    |
| goland                                |                                                                                                          |
| zoom                                  |                                                                                                          |
| shutter                               |                                                                                                          |
| perl-goo-canvas                       | shutter 的画线插件                                                                                            |

### KDE

| name       | comments  |
| ---------- | --------- |
| powerdevil | 电源管理，休眠按钮 |
| kscreen    | 多显示器配置    |
| kmix       | 音量调节      |
| ark        | 压缩包管理器    |
| gwenview   | 图片查看      |

### KDE widget

| name               | comments   |
| ------------------ | ---------- |
| netspeed widget    | 网络监控       |
| resources monitor  | CPU, 内存 监控 |
| Plasma Week Number | 显示周数       |

## ubuntu

| Name          | Comments |
| ------------- | -------- |
| openjdk-8-jdk |          |

### xfce4

file-roller