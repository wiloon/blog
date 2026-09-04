---
title: Dual Boot Windows 11 and Omarchy on Dell XPS 13 9310
author: "-"
date: 2026-09-04T14:15:01+08:00
lastmod: 2026-09-04T14:15:01+08:00
url: windows-omarchy-dual-boot-xps-13-9310
categories:
  - Linux
tags:
  - dual-boot
  - windows
  - arch-linux
  - omarchy
  - hyprland
  - uefi
  - ssh
  - sudo
  - remix
  - AI-assisted
---
## 目标与前提

在一台 Dell XPS 13 9310 上装 Windows 11（最新版）和 Omarchy 双系统。

关于 Omarchy：它是 DHH（David Heinemeier Hansson）在 2025 年做的一套基于 Arch Linux + Hyprland 的预配置系统，前身是基于 Ubuntu 的 Omakub。底层还是 Arch，用 pacman 和 AUR；桌面用 Hyprland（Wayland 平铺式合成器），配好了 Waybar、walker、终端、hyprlock 等，并带一套可一键切换的主题系统。引导器用 Limine。官网 omarchy.org，代码在 GitHub `basecamp/omarchy`。

本文是一份安装顺序的初稿，实际操作前请再核对当前版本的官方文档（`basecamp/omarchy` 仓库 `manual/50-dual-boot-install.md`）。

## 推荐顺序

先调 BIOS，再装 Windows，最后装 Omarchy。

Windows 每次安装都会重写 EFI 引导项，先装 Linux 会被覆盖；反过来 Omarchy 的 Limine 引导器能扫描并接管已存在的 Windows。所以顺序是固定的：Windows 在前，Omarchy 在后。

同类流程可参考本站已有的 [dual boot windows and ubuntu](./dual-boot.md)。

## 阶段 0：准备

- 备份数据。
- 在 Windows 里更新 BIOS 到最新版本（或用 Dell 的更新 U 盘）。9310 早期 BIOS 对 NVMe 和电源管理有已知问题。
- 记快捷键：开机按 `F2` 进 BIOS 设置，按 `F12` 进一次性启动菜单。

## 阶段 1：先改 BIOS

这一步要在装 Windows 之前完成。

1. SATA/NVMe Operation：从 `RAID On` 改为 `AHCI`。

   XPS 13 9310 出厂默认是 Intel RST 的 RAID 模式，Linux 安装器看不到这块 NVMe 盘。如果先装了 Windows 再改，Windows 会启动失败，需要用安全模式修复一次。清装场景下现在就改成 AHCI 最省事。

1. 关闭 Secure Boot（必要时连 TPM 一起关）。

   Omarchy 官方文档明确要求关闭 Secure Boot 和/或 TPM 才能安装。可以后期用 `sbctl` 自己签名再开回来，但步骤繁琐，先关掉。

1. 可选：关闭 Fast Boot，启动检测设为 Thorough。

   这里的 Fast Boot 是 BIOS 自检加速选项（跳过部分硬件初始化），和阶段 3 的 Windows「快速启动」是两回事。Minimal 模式下有时 U 盘引导识别不到、装完 Linux 看不到新启动项，改成 Thorough 能避免；全部装好后可再改回。

如果这台机器上已有需要保留的 Windows，改 AHCI 或关 Secure Boot 都会触发 BitLocker 恢复码提示。先到 `https://account.microsoft.com/devices/recoverykey` 存好恢复码，或先关闭 BitLocker。

## 阶段 2：装 Windows 11

- 用微软官方 Media Creation Tool 制作安装 U 盘。
- 到分区界面时不要让它占满整块盘：删掉旧分区后，只给 Windows 建一个需要的大小（例如总容量的 50%～60%），其余留成未分配空间给 Omarchy。
- 装完进系统，装齐 Dell 驱动，跑完 Windows Update。

## 阶段 3：Windows 装完后的收尾

1. 关闭 BitLocker / 设备加密（必做，不是可选）。

   路径：设置 → 隐私和安全性 → 设备加密，关闭并等待解密完成。Omarchy 的 free-space 安装与 BitLocker 不兼容：它只加密自己那个分区，而 BitLocker 锁的是整块盘，安装器检测到会直接报错。

1. 关闭快速启动。

   控制面板 → 电源选项 → 选择电源按钮的功能 → 取消勾选「启用快速启动」。否则 Windows 处于半休眠状态，双系统共享分区会损坏，时钟也会乱。

1. 用「磁盘管理」压缩 C 盘，留出给 Omarchy 的未分配空间（如果阶段 2 没留）。

   开始菜单搜「磁盘管理」→ 选中 Windows 主分区 → 右键「压缩卷」→ 输入要压缩出的大小。这块空间就是将来 Omarchy 的全部容量（含它自己的 boot 分区）。压缩完能看到一段「未分配」空间。

## 阶段 4：装 Omarchy

官方 ISO 安装器支持两种模式，选对模式就不会动到 Windows：

- **Full-disk install**：接管并擦除整块盘。不要选。
- **Free space install**：装进阶段 3 空出来的未分配空间，保留 Windows。选这个。

它仍然默认对自己的分区做 LUKS 加密（只加密这一个分区，不是整盘），体验上和全盘装没差别。想装成不加密的，在磁盘格式化确认那一步按 `Ctrl + C` 切换。

步骤：

1. 到 omarchy.org 下载 Omarchy ISO，用 balenaEtcher（Windows / macOS）或 caligula（Linux）写入 U 盘。
1. `F12` 从 U 盘引导（Secure Boot / TPM 已在阶段 1 关闭）。
1. 回答配置问题（键盘、时区、用户名、密码等）并确认。
1. 选择目标磁盘，然后选 **Free space install**。
1. 确认无误，等待安装完成，通常几分钟。

装完引导器变成 Limine，默认只有 Omarchy。运行 `limine-scan`，按提示把 Windows Boot Manager 加进 Limine 配置，之后开机就能看到 Omarchy 和 Windows 两个选项。

如果想完全自己掌控分区，也可以按 Arch Wiki 手动装 Arch（手动分区保留 Windows），再运行 Omarchy 的安装脚本糊上桌面环境。多数情况下没必要。

### 关于开机解锁密码与键盘

分区加密后，开机输入解锁密码这一步（和进 BIOS 一样）**不能用蓝牙键盘**。XPS 13 的内置键盘没问题；如果平时接蓝牙外接键盘，解锁时改用内置键盘或有线 / 2.4G 键盘。

## 阶段 5：收尾

时钟：Windows 用本地时间，Linux 默认用 UTC，双系统会差 8 小时。在 Linux 里执行下面的命令让 Linux 也把 RTC 当本地时间。背景见 [解决 archlinux 和 windows 双系统启动时间不准的问题](../cs/解决-archlinux-和-windows-双系统启动时间不准的问题.md)。

```bash
# make Linux also treat the RTC as local time
timedatectl set-local-rtc 1 --adjust-system-clock
```

默认启动项：Limine 已是默认引导器；如果 BIOS 启动顺序里 Windows Boot Manager 排在前面，用 BIOS 启动菜单或 `efibootmgr` 把 Limine（Omarchy）调到前面。

固件更新：

```bash
# check and apply firmware updates via LVFS
fwupdmgr refresh
fwupdmgr get-updates
fwupdmgr update
```

XPS 13 9310 的硬件（AX201 网卡、指纹、雷电、核显）在近几年的内核上开箱可用，不需要额外驱动。

## 阶段 6：SSH 远程访问

Omarchy 用 `omarchy-setup-security-sshd` 一条命令配好 SSH：装 openssh、`systemctl enable --now sshd`、在 ufw 里放开 22 端口（rate limit）、把公钥写进 `~/.ssh/authorized_keys`，最后**关闭密码登录**（只认密钥）。

`~/.ssh` 目录不存在是正常的，脚本会自己建。

### 交互式配置

```bash
omarchy-setup-security-sshd
```

按提示选 **Grab key from GitHub**，输入自己的 GitHub 用户名即可。GitHub 把每个账号的公钥放在公开地址 `https://github.com/<username>.keys`，免登录就能拉，脚本内部就是 `curl` 这个地址。只会暴露公钥，私钥始终在本机。

较新版本支持 `--gh-keys <user>` / `--key="ssh-ed25519 ..."` 参数跳过菜单；4.0.2 的 ISO 还没有，用交互式或下面的手动方式。

### 手动配置（与版本无关）

```bash
sudo pacman -S --needed openssh
sudo systemctl enable --now sshd
sudo ufw limit 22/tcp
mkdir -p ~/.ssh && chmod 700 ~/.ssh
curl -fsSL https://github.com/<username>.keys > ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

注意：手动方式不会写 `PasswordAuthentication no`。要关密码登录，加一个 drop-in：

```bash
# key-only login
printf 'PasswordAuthentication no\nKbdInteractiveAuthentication no\n' | sudo tee /etc/ssh/sshd_config.d/10-omarchy-hardening.conf
sudo sshd -t && sudo systemctl reload sshd
```

### 连接

在 Omarchy 上查 IP，然后从客户端连：

```bash
ip -brief addr        # find the LAN IP
sudo ufw status       # confirm 22 is allowed
systemctl is-active sshd
```

```bash
ssh <username>@<ip>
```

连不上时先看错误：`Connection refused` 是 sshd 没起或端口没放开；`Operation timed out` 多半 IP 不对或 ufw 没放行；`Permission denied (publickey)` 是公钥没进 `authorized_keys`。`ufw limit` 会在 30 秒内同一 IP 连 6 次以上时临时封禁，反复重试失败就等一分钟。

## 阶段 7：免密 sudo

Omarchy 自带的 `omarchy-sudo-passwordless` 是**临时**开关：默认 15 分钟后由 systemd 定时器自动撤销，重启也失效。适合临时给 AI agent 用，不适合长期。

长期免密要自己放一个 sudoers 片段，用 `visudo` 编辑（带语法检查，写错不会锁死 sudo）：

```bash
sudo visudo -f /etc/sudoers.d/99-<username>-nopasswd
```

内容一行：

```text
<username> ALL=(ALL:ALL) NOPASSWD: ALL
```

一步到位的写法：

```bash
echo "<username> ALL=(ALL:ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/99-<username>-nopasswd
sudo chmod 440 /etc/sudoers.d/99-<username>-nopasswd
sudo visudo -c        # validate all sudoers files
```

验证：

```bash
sudo -k               # drop cached credentials
sudo -n whoami        # should print root with no prompt
```

两个注意点：

- **文件名不要用 `99-omarchy-nopasswd-<username>`**。`omarchy-sudo-passwordless` 用的就是这个名字，且它有「文件在但定时器没了就删」的清理逻辑，会把永久文件删掉。用 `99-<username>-nopasswd` 之类避开。
- 配合密钥登录 + 关闭密码登录后，拿到私钥的人等于直接 root，自行权衡。撤销就 `sudo rm /etc/sudoers.d/99-<username>-nopasswd`。

## 待确认 / TODO

- Free space install 对已有 Windows ESP 的处理：是复用还是新建 boot 分区，实际装完再确认。
- `limine-scan` 添加 Windows 后的启动项显示效果。
- Secure Boot 保持开启 + `sbctl` 签名的完整流程（如果后续想开 Secure Boot）。
- XPS 13 9310 在 Hyprland 下的缩放、外接显示器、休眠表现。
