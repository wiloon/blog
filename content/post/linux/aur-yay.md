---
title: archlinux AUR Helper, paru, yay
author: "-"
date: 2026-01-01T08:30:00+08:00
lastmod: 2026-05-29T14:08:08+08:00
url: aur-helper-yay-paru
tags:
  - Linux
  - remix
  - AI-assisted
categories:
  - Linux
---

## archlinux AUR Helper

AUR（Arch User Repository）里的包不能直接用 `pacman -S` 安装，需要 **AUR helper** 来搜索、构建和更新。目前最常用的是 **paru** 和 **yay**，命令与 pacman 高度一致，且都能同时管理官方仓库与 AUR 包。

## paru

https://github.com/Morganamilo/paru

paru 是用 Rust 编写的 AUR 助手，由 yay 核心贡献者 Morganamilo 维护，常被视为「下一代 AUR helper」。它是 **pacman 的超集**：装/卸/更新官方包仍走 pacman，AUR 包由 paru 负责下载 PKGBUILD 并构建，日常只需记住 `paru` 一套命令即可。

### 名字由来

paru **不是** Pacman + AUR 的缩写（所以不是 `paur`）。作者说明它只是与 pacman、Arch、AUR、Rust 等相关的音节组合，**没有特定含义**；本想找一个好听的 3 字母名，未果后用了 4 字母的 paru。见 [GitHub Discussion #1279](https://github.com/Morganamilo/paru/discussions/1279)。

### paru 安装

paru 不在 Arch 官方仓库，不能 `pacman -S paru`。**首次安装不依赖 yay 或其它 AUR helper**，标准做法与 yay 一样：从 AUR 取 PKGBUILD，用 `makepkg` 构建后由 `pacman` 安装。

#### 推荐：paru 源码包（与当前 pacman 对齐）

AUR 的 `paru` 会在本机按当前 `libalpm` 编译，pacman 大版本升级后也能通过重装恢复。首次安装或升级 pacman 后优先用这个：

```bash
pacman -S --needed git base-devel rust
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si
```

（若未装 `rust`，`base-devel` 构建过程中会拉取；也可先 `pacman -S rust`。）

#### paru-bin（预编译，省事但有版本滞后风险）

`paru-bin` 从 GitHub Release 拉**已编好的**二进制，本机不编译 paru，但二进制固定链接某一版 `libalpm`（例如 `.so.15`）。系统已升到 pacman 7 / `libalpm.so.16` 时，**重装 `paru-bin` 仍无效**——装上的还是同一份旧二进制。此时应改装上面的 `paru` 源码包，或等 AUR 维护者发布适配新 libalpm 的 `paru-bin` 后再用。

仅在 pacman 与 Release 二进制版本一致时适合：

```bash
pacman -S --needed git base-devel
git clone https://aur.archlinux.org/paru-bin.git
cd paru-bin
makepkg -si
```

一行命令：

```bash
pacman -S --needed git base-devel && git clone https://aur.archlinux.org/paru-bin.git && cd paru-bin && makepkg -si
```

#### 用 curl 代替 git（可选）

不想装 git 时，可下载 AUR 快照再 `makepkg`，效果与 `git clone` 相同：

```bash
pacman -S --needed curl base-devel
curl -LO https://aur.archlinux.org/cgit/aur.git/snapshot/paru-bin.tar.gz
tar xf paru-bin.tar.gz
cd paru-bin
makepkg -si
```

#### 已有 AUR helper 时（可选）

系统里若已装 yay 等，可省一步：`yay -S paru-bin` 或 `yay -S paru`。这只是捷径，**不是**安装 paru 的前提。

#### makepkg 权限

若 `makepkg -si` 因 sudo 失败，可分两步：`makepkg` 构建后，再 `sudo pacman -U paru-*.pkg.tar.zst`。

首次使用 `-git` 包跟踪时，可执行一次 `paru --gendb`。

### paru 使用命令

```bash
# 搜索（官方源 + AUR，默认分区显示）
paru -Ss <package-name>

# 只搜 AUR
paru -Ss <package-name> -a

# 安装（官方包或 AUR 包均可）
paru -S <package-name>

# 全量更新（官方源 + AUR）
paru -Syu
# 或直接
paru

# 查看 Arch 新闻（大版本升级前有用）
paru --news
```

### 常见问题

**`libalpm.so.15: cannot open shared object file`**

`pacman -Syu` 正常，但 `paru` 报找不到 `libalpm.so.15`，说明系统已是 **pacman 7 / libalpm 16**（`ls /usr/lib/libalpm.so*` 可见 `.so.16`），而磁盘上的 paru 仍链接 **`.so.15`**。

常见原因：

1. 装的是 **`paru-bin`**：预编译包不会随你系统 pacman 变；`makepkg -si` 重装也只是再次装上同版本旧二进制，**不能**解决。
2. 装的是旧版 **`paru` 源码包** 且未按新 libalpm 重编。

处理：**卸掉 `paru-bin`，改从源码装 `paru`**（会按当前 libalpm 编译）：

```bash
pacman --version    # 确认已是 Pacman v7.x / libalpm v16.x
pacman -Rns paru-bin paru-bin-debug
pacman -S --needed git base-devel rust
cd /tmp && rm -rf paru
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si
paru --version
```

若 `paru` 源码包编译仍报 alpm 版本不支持，可改用跟踪上游的 **`paru-git`**（需与 `paru` / `paru-bin` 互斥，先卸载再装）：

```bash
pacman -Rns paru paru-bin paru-debug paru-bin-debug 2>/dev/null; true
git clone https://aur.archlinux.org/paru-git.git
cd paru-git
makepkg -si
```

参考：[paru #1454 Support for libalpm v16](https://github.com/Morganamilo/paru/issues/1454)（维护者说明 **`-bin` 无法由用户针对新 soname 重链**，须源码重编或等新 Release）。

日常若长期用 `paru-bin`，pacman 大版本升级后可能再次踩坑；升级 pacman 后优先检查 `paru --version` 是否还能运行。

**从 paru-bin 换到 paru 源码包时 debug 包冲突**

```
paru-debug: /usr/lib/debug/usr/bin/paru.debug exists in filesystem (owned by paru-bin-debug)
```

先卸载旧包再装，或只装主包、跳过 debug 包：

```bash
sudo pacman -Rns paru-bin paru-bin-debug
makepkg -si
# 或：makepkg 后只执行 sudo pacman -U paru-*.pkg.tar.zst（不要装 paru-debug）
```

## yay

https://github.com/Jguer/yay

yay 是一个 AUR 助手。它使用 Go 语言写成，宗旨是提供最少化用户输入的 pacman 界面、yaourt 式的搜索，而几乎没有任何依赖软件。

### yay 安装

```bash
pacman -S --needed git base-devel
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si

# 如果遇到 sudo 权限问题，可以分两步执行：
# 1. 构建包（普通用户）
makepkg
# 2. 安装包（需要 root 权限）
su -c "pacman -U yay-*.pkg.tar.zst"
# 或者
sudo pacman -U yay-*.pkg.tar.zst
```

一行命令：

```bash
pacman -S --needed git base-devel && git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si
```

#### Binary

若不想本地编译 yay，可使用 GitHub Actions 构建的二进制包：

```bash
pacman -S --needed git base-devel
git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
makepkg -si
```

Release 下载：<https://github.com/Jguer/yay/releases>

#### AUR mirror

默认的仓库 (aur.archlinux.org) 非常慢，可以走梯子加速，或者用国内的镜像。

执行以下命令修改 aururl：

```bash
yay --aururl "https://aur.archlinux.org" --save
```

**注意：清华镜像源已停止服务**

清华大学 AUR 镜像源 `aur.tuna.tsinghua.edu.cn` 已经停止服务。如果遇到以下错误：

```text
dial tcp: lookup aur.tuna.tsinghua.edu.cn: no such host
```

请切换回官方源：

```bash
yay --aururl "https://aur.archlinux.org" --save
```

**重要：如果执行上述命令后仍然报错**

如果执行 `--aururl` 命令后仍然尝试访问清华镜像源，说明配置文件中 `aurrpcurl` 字段仍然保留旧的镜像地址。需要手动编辑配置文件：

```bash
vim ~/.config/yay/config.json
# 或者
nano ~/.config/yay/config.json
```

找到 `aurrpcurl` 字段，确保其值为：

```json
"aurrpcurl": "https://aur.archlinux.org/rpc?",
```

或者使用 sed 命令快速修复：

```bash
sed -i 's|"aurrpcurl": "https://aur.tuna.tsinghua.edu.cn/rpc?"|"aurrpcurl": "https://aur.archlinux.org/rpc?"|' ~/.config/yay/config.json
```

修改的配置文件位于 `~/.config/yay/config.json`，可以通过以下命令查看修改过的配置：

```bash
yay -P -g
```

如果官方源访问较慢，建议使用代理或 VPN 加速访问。

### yay 使用命令

```bash
# 搜索
yay -Ss <package-name>

# 安装
yay -S <package-name>

# 全量更新
yay

# 查看已安装包
yay -Q

# 查询包内文件
yay -Ql
yay -Ql <package-name>
```

## paru vs yay

### 相同点

- 都是 AUR 助手，命令与 pacman 高度一致
- **都能同时管理官方仓库和 AUR 软件包**（`paru -Syu` / `yay -Syu` 一次更新全部）
- 都支持依赖解析、并行下载、`-git` 包 devel 跟踪
- 配置与缓存各自独立，迁移成本低（改命令前缀即可）

### 主要区别

| 特性 | paru | yay |
| ---- | ---- | --- |
| 编程语言 | Rust | Go |
| 开发状态 | 活跃维护 | 活跃维护 |
| 默认行为 | 更严格，安装 AUR 包前常提示查看 PKGBUILD | 更自动化，交互更少 |
| 搜索 `-Ss` | 官方源与 AUR **分区显示**；只搜 AUR 用 `-a` | 官方源与 AUR 结果**交错显示**，找包往往更直观 |
| 配置文件 | `~/.config/paru/paru.conf` | `~/.config/yay/config.json` |
| 特色功能 | `paru --news`、本地仓库、clean chroot 构建 | 历史久、文档多、批处理选项成熟 |
| 性能 | 大批量搜索/同步有时略快；默认审查 PKGBUILD 可能让流程感觉更慢 | 日常感知差异不大 |

### 能否并存

**可以。** paru 和 yay 可同时安装在系统里，分别执行 `paru` / `yay` 即可，不会自动互相替换。

注意：

- 不要把 `pacman` alias 成其中一个，容易误操作
- 两者对 `-git` 包的 devel 跟踪数据库分开维护，不建议长期交替做全量更新
- 实践上选一个做主力（负责无参全量更新和日常 AUR 管理），另一个可留着备用

### 命令对比

```bash
# 安装
paru -S package-name
yay -S package-name

# 搜索
paru -Ss keyword
yay -Ss keyword

# 全量更新
paru
yay

# 删除
paru -R package-name
yay -R package-name
```

### 如何选择

- **选 paru**：重视 PKGBUILD 审查、需要 Arch 新闻提醒、或要用 chroot / 本地仓库
- **选 yay**：想要更少步骤、类似 yaourt 的体验，或发行版已预装 yay

两者都是优秀的 AUR 助手；许多用户从 yay 迁移到 paru，但不必强行更换。

## Yaourt

Yaourt 已经不再维护。

- [清华 AUR 镜像说明（已停服）](https://mirrors.tuna.tsinghua.edu.cn/help/AUR/)
- [install yaourt（历史文章）](http://bashell.nodemedia.cn/archives/install-yaourt.html)
- [linux.cn 相关文章](https://linux.cn/article-9925-1.html)
