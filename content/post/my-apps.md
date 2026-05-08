---
title: my apps
author: "-"
date: 2026-05-05T14:02:11+08:00
url: my-apps
categories:
  - Desktop
tags:
  - apps
  - original
  - AI-assisted
---

## My Apps

跨平台常用软件统一列表。各平台专属工具见：

- [Linux Apps](linux/apps)
- [macOS Apps](macos/apps)
- [Windows Apps](windows/apps)

## 说明

列值为包名，可直接用于安装命令：

- `pacman` 列：`sudo pacman -S <name>`
- `aur` 列：`yay -S <name>`
- `brew` 列：`brew install <name>`
- `cask` 列：`brew install --cask <name>`
- `win` 列：`winget install <id>`
- `—` 表示该平台不支持或不常用

## Essentials

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| chezmoi | chezmoi | — | chezmoi | — | twpayne.chezmoi | dotfiles 管理 |
| kitty | kitty | — | — | kitty | — | terminal |
| neovim | neovim | — | neovim | — | Neovim.Neovim | 编辑器 |
| bitwarden | bitwarden | — | — | bitwarden | Bitwarden.Bitwarden | 密码管理 |
| flameshot | flameshot | — | — | flameshot | Flameshot.Flameshot | 截图+标注 |
| btop | btop | — | btop | — | — | top 替代 |
| wechat | — | wechat | — | wechat | Tencent.WeChat | |
| vscode | — | visual-studio-code-bin | — | visual-studio-code | Microsoft.VisualStudioCode | |

## Browser

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| chromium | chromium | — | chromium | — | Hibbiki.Chromium | 开源版 Chrome |
| google-chrome | — | google-chrome | — | google-chrome | Google.Chrome | |
| google-chrome-beta | — | google-chrome-beta | — | google-chrome@beta | Google.Chrome.Beta | |

## Terminal

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| kitty | kitty | — | — | kitty | — | |
| tmux | tmux | — | tmux | — | — | |
| hyper | hyper | — | — | hyper | Hyper.Hyper | |

## Text Editor / Notes

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| neovim | neovim | — | neovim | — | Neovim.Neovim | |
| typora | — | typora | — | typora | Typora.Typora | Markdown 编辑器 |
| obsidian | obsidian | — | — | obsidian | Obsidian.Obsidian | 知识管理 |

## Screenshot

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| flameshot | flameshot | — | — | flameshot | Flameshot.Flameshot | 截图+标注 |

## System Monitor

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| btop | btop | — | btop | — | — | |
| ncdu | ncdu | — | ncdu | — | — | 磁盘空间分析 |

## Development Tools

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| git | git | — | git | — | Git.Git | |
| lazygit | — | — | lazygit | — | JesseDuffield.lazygit | `go install github.com/jesseduffield/lazygit@latest` |
| gitkraken | — | gitkraken | — | gitkraken | Axosoft.GitKraken | Git GUI |
| github-desktop | — | github-desktop-bin | — | github | GitHub.GitHubDesktop | |
| cmake | cmake | — | cmake | — | Kitware.CMake | |
| iperf3 | iperf3 | — | iperf3 | — | ESnet.iPerf3 | 网络测试 |
| wireshark | wireshark-qt | — | — | wireshark | WiresharkFoundation.Wireshark | |
| zeal | zeal | — | — | zeal | OlegKalnin.Zeal | 离线文档 |
| chezmoi | chezmoi | — | chezmoi | — | twpayne.chezmoi | dotfiles 管理 |
| platformio | — | platformio | platformio | — | — | 物联网开发 |

## IDE

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| vscode | — | visual-studio-code-bin | — | visual-studio-code | Microsoft.VisualStudioCode | |
| vscodium | — | vscodium-bin | — | vscodium | VSCodium.VSCodium | 无遥测版 |
| jetbrains-toolbox | — | jetbrains-toolbox | — | jetbrains-toolbox | JetBrains.Toolbox | |
| intellij-idea-ce | intellij-idea-community-edition | — | — | intellij-idea-ce | JetBrains.IntelliJIDEA.Community | |
| intellij-idea-ult | — | intellij-idea-ultimate-edition | — | intellij-idea | JetBrains.IntelliJIDEA.Ultimate | |
| goland | — | goland | — | goland | JetBrains.GoLand | |
| webstorm | — | webstorm | — | webstorm | JetBrains.WebStorm | |
| clion | — | clion | — | clion | JetBrains.CLion | |
| datagrip | — | — | — | datagrip | JetBrains.DataGrip | |
| claude-code | — | claude-code | — | — | — | macOS: `npm i -g @anthropic-ai/claude-code` |

## Java

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| jdk (latest) | jdk-openjdk | — | openjdk | — | Microsoft.OpenJDK.21 | |
| jdk8 | jdk8-openjdk | — | openjdk@8 | — | Microsoft.OpenJDK.8 | |
| maven | maven | — | maven | — | Apache.Maven | |
| gradle | gradle | — | gradle | — | Gradle.Gradle | |
| graphviz | graphviz | — | graphviz | — | Graphviz.Graphviz | PlantUML 依赖 |
| jd-gui | — | jd-gui-bin | — | jd-gui | — | Java 反编译 |
| eclipse-mat | — | eclipse-mat | — | mat | — | Eclipse Memory Analyzer |

## Go / Node.js / Rust

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| go | go | — | go | — | GoLang.Go | |
| nvm | nvm | — | nvm | — | — | Node.js 版本管理 |
| rust | rust | — | rustup | — | Rustlang.Rustup | |

## Database

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| redisinsight | — | redisinsight | — | redisinsight | Redis.RedisInsight | Redis GUI |
| tableplus | — | tableplus | — | tableplus | — | DB 客户端 |
| heidisql | — | heidisql | — | — | HeidiSQL.HeidiSQL | MySQL 客户端 |

## Communication

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| telegram | telegram-desktop | — | — | telegram | Telegram.TelegramDesktop | |
| wechat | — | wechat | — | wechat | Tencent.WeChat | |
| feishu | — | feishu | — | feishu | ByteDance.Feishu | 飞书 |
| dingtalk | — | dingtalk | — | dingtalk | Alibaba.DingTalk | |
| zoom | — | zoom | — | zoom | Zoom.Zoom | |
| thunderbird | thunderbird | — | — | thunderbird | Mozilla.Thunderbird | 邮件客户端 |

## Office

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| libreoffice | libreoffice-fresh | — | — | libreoffice | TheDocumentFoundation.LibreOffice | |
| wps-office | — | wps-office | — | wpsoffice | — | |

## Media / Graphics

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| inkscape | inkscape | — | — | inkscape | Inkscape.Inkscape | 矢量图形 SVG |
| audacity | audacity | — | — | audacity | Audacity.Audacity | 音频处理 |

## Archive / Compression

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| zstd | zstd | — | zstd | — | Facebook.Zstandard | 多线程快速压缩 |

## Download

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| aria2 | aria2 | — | aria2 | — | aria2.aria2 | |
| axel | axel | — | axel | — | — | |

## VPN

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| openvpn | openvpn | — | — | tunnelblick | OpenVPNTechnologies.OpenVPN | macOS 用 Tunnelblick GUI |

## Virtualization / Container

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| docker | docker | — | — | docker | Docker.DockerDesktop | |
| podman | podman | — | podman | — | RedHat.Podman | |

## Fonts

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| JetBrains Mono | ttf-jetbrains-mono | — | font-jetbrains-mono | — | JBRAINS.JetBrainsMono | |
| Source Code Pro | adobe-source-code-pro-fonts | — | font-source-code-pro | — | — | Adobe 编程字体 |

## Utilities

| app | pacman | aur | brew | cask | win | notes |
| --- | --- | --- | --- | --- | --- | --- |
| keepassxc | keepassxc | — | — | keepassxc | KeePassXCTeam.KeePassXC | 密码管理 |
| qalculate | qalculate-gtk | — | qalculate-gtk | — | — | 全宇宙最好用的计算器 |
