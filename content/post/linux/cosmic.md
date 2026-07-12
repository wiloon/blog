---
author: "-"
date: 2026-07-12T00:00:00+08:00
lastmod: 2026-07-12T00:00:00+08:00
title: COSMIC 桌面环境与 cosmic-greeter
url: cosmic
categories:
  - Desktop
tags:
  - original
  - linux
  - archlinux
  - AI-assisted
---

## 什么是 COSMIC

COSMIC（"Computer Operating System Main Interface Components"）是 System76（Pop!_OS 的厂商）用 **Rust + iced** 从零重写的新一代桌面环境，用来替代 Pop!_OS 之前基于 GNOME Shell 深度定制的 Pop Shell。

- Compositor：`cosmic-comp`，基于 Smithay（Rust 的 Wayland compositor 库），只支持 **Wayland**，不支持 X11。
- UI 工具包：`iced`（Rust 原生 GUI 库），不依赖 GTK 或 Qt。
- 特点：内置类似平铺窗口管理器的窗口平铺/浮动切换，风格上介于 GNOME 的简洁与传统桌面（面板 + 应用列表 + 系统托盘）之间。
- 现状（2026-07）：Arch `extra` 仓库已提供稳定打包（当前 `1.2.0-1`），可通过包组 `cosmic` 一次性安装。

## KDE Plasma 对比 COSMIC

| 维度 | KDE Plasma | COSMIC |
| --- | --- | --- |
| 实现语言/工具包 | C++ / Qt + QML | Rust / iced |
| 显示协议 | X11 + Wayland 双支持 | 仅 Wayland（`cosmic-comp` 基于 Smithay） |
| 项目历史 | 1996 年至今，成熟度极高 | 2022 年立项，2024~2025 年逐步稳定，仍在快速迭代 |
| 窗口管理风格 | 浮动窗口为主，插件式支持平铺（如 KWin 脚本、Bismuth） | 原生内置平铺/浮动切换，无需插件 |
| 可定制程度 | 极高：几乎每个组件（面板、快捷键、主题、特效）都可深度配置 | 目前较克制，配置项比 Plasma 少很多，走"够用即可"路线 |
| 默认发行版 | Kubuntu、openSUSE、Arch 等（无绑定） | Pop!_OS（System76 主推，未来默认桌面） |
| 资源占用 | 中等，特效多时略高 | 更轻量，Rust 实现 + 无 Qt/GTK 依赖 |
| 应用生态 | 庞大（KDE Applications 套件：Dolphin、Kate、Okular、Konsole 等） | 尚在建设中（`cosmic-files`、`cosmic-terminal`、`cosmic-text-editor` 等基础应用刚起步） |
| 主题/外观定制 | 支持第三方主题、图标包、Global Theme 一键换肤 | 目前主题选择有限，风格由官方统一把控（类似 GNOME 的"少即是多"哲学） |
| 登录界面集成 | SDDM（KWallet 自动解锁等深度集成） | `cosmic-greeter`（greetd），风格与桌面统一，但生态集成不如 SDDM 成熟 |
| 适合人群 | 想要高度自定义、功能全面、多年验证的稳定桌面 | 想尝鲜 Rust 生态新桌面、偏好简洁一致设计、愿意接受少数功能还不完善 |

一句话总结：**Plasma 是"功能全面、可深度定制"的成熟老牌桌面；COSMIC 是"简洁统一、技术栈新颖"的年轻桌面**，目前更适合尝鲜和轻量使用，还不建议完全替代 Plasma 作为主力日常桌面。

## 核心组件一览

| 包 | 作用 |
| --- | --- |
| `cosmic-session` | 会话管理器，登录后拉起整个 COSMIC 会话；同时向系统注册 Wayland session 文件（供 SDDM/GDM/greetd 等登录管理器识别） |
| `cosmic-comp` | Wayland compositor（窗口管理 + 合成渲染） |
| `cosmic-panel` / `cosmic-applets` | 顶部面板与各类小挂件（音量、网络、电量等） |
| `cosmic-launcher` | 应用启动器（类似 Spotlight / krunner） |
| `cosmic-files` | 文件管理器 |
| `cosmic-settings` / `cosmic-settings-daemon` | 系统设置界面与后台设置服务 |
| `cosmic-store` | 应用商店（前端对接 Flatpak 等） |
| `cosmic-terminal` | 自带终端模拟器 |
| `xdg-desktop-portal-cosmic` | XDG Desktop Portal 后端，供沙盒应用（Flatpak）调用文件选择、截图等系统能力 |
| `cosmic-greeter` | 登录界面（greeter），见下节 |

## cosmic-greeter 是什么，解决了什么问题

### 背景：greetd 与「greeter」的分层设计

登录管理器传统上是一个整体（比如 SDDM、GDM 各自把"认证 + 画登录界面 + 拉起会话"绑在一起）。**greetd** 是另一种思路：它把"认证 + 拉起会话"这个核心逻辑做成一个极简、与桌面无关的 systemd 服务，本身**不提供任何图形界面**；具体登录界面是可插拔的 "greeter" 程序，可以自由更换：

- `tuigreet` — 纯终端风格的极简 greeter
- `regreet` — GTK 实现，界面接近 GNOME 风格
- `cosmic-greeter` — 用 COSMIC 自家的 iced UI 实现，视觉风格与 COSMIC 桌面完全统一（同款圆角、字体、配色）

### cosmic-greeter 解决的问题

COSMIC 项目（面向 Pop!_OS 默认发行版）希望**登录界面的视觉/交互体验和桌面本身一致**，而不是依赖：

- SDDM —— 来自 KDE 生态，Qt/QML 实现，主题体系和 COSMIC 不通用；
- GDM —— 来自 GNOME 生态，与 GNOME Shell 强耦合。

于是 COSMIC 团队基于 greetd + 自研 iced 界面，做了 `cosmic-greeter`：一个专门为 COSMIC 桌面设计的登录界面，同时也会扫描 `/usr/share/wayland-sessions/` 和 `/usr/share/xsessions/`，列出系统里所有已安装的会话（不仅限于 COSMIC），供用户在登录时选择。

### 与 SDDM 的关系：互斥的"登录管理器"

`cosmic-greeter`（配合 `greetd.service`）和 `SDDM`（`sddm.service`）**做的是同一件事**——认证用户 + 展示会话选择器 + 拉起选中的会话，只是实现生态不同：

| | 登录管理器（daemon） | 界面实现 | 生态 |
| --- | --- | --- | --- |
| 传统方案 | `sddm.service` | SDDM 自带 QML 主题 | KDE / Qt |
| COSMIC 方案 | `greetd.service` | `cosmic-greeter`（可换成 tuigreet/regreet） | greetd 协议 / iced |

**同一时刻只能 enable 一个**（`sddm` 或 `greetd`），两者都监听 seat/tty，同时启用会冲突。

### 对"KDE + COSMIC 共存"场景的意义

如果只是想在**已有 SDDM** 的系统上试用 COSMIC 桌面本体，并不需要 `cosmic-greeter`：`cosmic-session` 安装后会在 `/usr/share/wayland-sessions/` 注册一个 `cosmic.desktop`，SDDM 会自动识别并在登录界面的会话选择器里列出它，和 Plasma 一样可选。

只有当你想**连登录界面本身也换成 COSMIC 风格**（放弃 SDDM）时，才需要装 `cosmic-greeter` 并启用 `greetd.service`（同时 disable `sddm.service`）。

## 现在 KDE 靠 SDDM 启动，能换成 cosmic-greeter 吗？cosmic-greeter 能拉起 KDE 吗？

**能换，也能拉起 KDE。** 原因在于 `cosmic-greeter` 只是 greetd 的一个"皮肤"，它和 SDDM 一样，只是按标准位置扫描系统里已安装的会话：

- `/usr/share/xsessions/*.desktop`（X11 会话，比如 KDE 的 `plasmax11.desktop`）
- `/usr/share/wayland-sessions/*.desktop`（Wayland 会话，比如 `plasma.desktop`、`cosmic.desktop`）

这些 `.desktop` 文件里的 `Exec=` 通常指向发行版通用的启动脚本（如 `startplasma-x11` / `startplasma-wayland`），不绑定任何特定登录管理器。因此只要 KDE Plasma 的会话文件还在，无论换成 SDDM、GDM 还是 greetd + cosmic-greeter，都能在会话选择器里看到并选中 "Plasma"，和选 "COSMIC" 是同一套机制。

**迁移方式**（如果决定换）：

1. 安装 `greetd` + `cosmic-greeter`
2. 配置 `/etc/greetd/config.toml`，把 `default_session.command` 指向 `cosmic-greeter`
3. `systemctl disable --now sddm.service`
4. `systemctl enable --now greetd.service`

**需要注意的坑**（换之前建议了解）：

- **KWallet 自动解锁**：SDDM 对 KDE 生态有专门集成，登录密码可以通过 PAM（`pam_kwallet5`）自动解锁 KWallet；greetd 是通用协议，是否能顺带把密码传给 `pam_kwallet5` 取决于 greetd 的 PAM 配置是否正确串联，社区里常见反馈是**需要额外手动配置 PAM stack**，不像 SDDM 那样开箱即用，否则登录 KDE 后 KWallet 仍会弹窗要求再输一次密码。
- **成熟度**：SDDM 是 KDE 生态用了多年的默认方案，配置项、主题生态、故障排查资料都更丰富；greetd + cosmic-greeter 相对新，遇到问题时可参考的资料较少。
- **回退容易**：`greetd.service` 和 `sddm.service` 都是普通 systemd 服务，disable 一个、enable 另一个即可切回，不会破坏 KDE 或 COSMIC 本身的安装。

结论：**技术上完全可行**，cosmic-greeter 不是"只能启动 COSMIC"的专属登录界面；但如果只是想让 SDDM 的登录界面里多一个 COSMIC 选项（而不是连登录界面都换掉），**没有必要换**，装 `cosmic-session` 让 SDDM 识别新会话即可，风险更小。

## 参考

- [Arch Wiki: COSMIC (desktop environment)](https://wiki.archlinux.org/title/COSMIC_(desktop_environment))
- [greetd (GitHub)](https://github.com/kennylevinsen/greetd)
- [COSMIC Epoch (GitHub, system76/cosmic-epoch)](https://github.com/pop-os/cosmic-epoch)
