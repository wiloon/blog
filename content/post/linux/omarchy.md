---
title: Omarchy Linux
author: "-"
date: 2026-10-20T19:27:01+08:00
lastmod: 2026-10-20T19:27:01+08:00
url: omarchy
categories:
  - Linux
tags:
  - omarchy
  - arch-linux
  - hyprland
  - pacman
  - aur
  - ssh
  - ufw
  - remix
  - AI-assisted
---
## Omarchy 是什么

Omarchy 是 DHH（David Heinemeier Hansson）在 2025 年做的一套基于 Arch Linux + Hyprland 的预配置系统，前身是基于 Ubuntu 的 Omakub。底层还是 Arch，用 pacman 和 AUR；桌面用 Hyprland（Wayland 平铺式合成器），带一套可一键切换的主题系统，引导器用 Limine。官网 omarchy.org，代码在 GitHub `basecamp/omarchy`。

## 我的机器

| 机器 | 说明 |
| ---- | ---- |
| Dell XPS 13 9310 | Windows 11 + Omarchy 双系统，安装过程见 [Dual Boot Windows 11 and Omarchy on Dell XPS 13 9310](./windows-omarchy-dual-boot-xps-13-9310.md) |
| SER8（AMD CPU） | Omarchy 4.0.4，和另一套 Arch + KDE 双系统 |

## 版本与脚本位置

查看版本：

```bash
omarchy-version       # e.g. 4.0.4-1
```

Omarchy 的功能大多是一组 `omarchy-*` shell 脚本，也可以用总命令 `omarchy <子命令>` 调用，比如 `omarchy update`。脚本位置随版本不同：

- 4.x：由软件包安装，入口在 `/usr/bin`，其余在 `/usr/share/omarchy/bin`。
- 3.x：git 仓库克隆在 `~/.local/share/omarchy`，脚本在它的 `bin/` 下。

想知道某个功能具体做了什么，直接读脚本最快：

```bash
cat "$(command -v omarchy-update)"
ls /usr/share/omarchy/bin | grep -E 'update|pkg'
```

4.0.4 的桌面 shell 换成了 quickshell（`quickshell -n -p /usr/share/omarchy/shell`）。

## 系统更新与装软件

日常维护分两件事：升级整个系统，和装、卸单个软件。下面的脚本内容是在 SER8（Omarchy 4.0.4）上读到的。

### 升级系统：用 omarchy-update，不要直接 pacman -Syu

```bash
omarchy-update        # same as: omarchy update
omarchy-update -y     # unattended, no prompts
```

也可以从 Omarchy 菜单里点 Update。输出会记录到 `/tmp/omarchy-update.log`。

`omarchy-update` 本身也是调用 pacman 升级，只是在 `pacman -Syu` 前后加了几步。按 4.0.4 脚本里的顺序：

1. 检查磁盘剩余空间，然后让用户确认（加 `-y` 时跳过）。
1. 清理包缓存。这一步放在快照之前，因为缓存在被快照的子卷上，快照之后再清释放不出空间。
1. `omarchy-snapshot create`：用 snapper 建一个 btrfs 快照，升级出问题可以回滚。
1. 更新期间阻止机器休眠，再更新 keyring。
1. `omarchy-update-system-pkgs`：执行 `pacman -Syu --noconfirm --overwrite '/usr/share/omarchy/*'`。遇到文件冲突时交给专门的处理脚本，处理完重试一次。
1. `omarchy-migrate`：执行 Omarchy 各版本附带的迁移脚本（配置格式变化、组件替换等）。迁移脚本是按新装的包写的，所以包升级失败时脚本会停下，不会继续跑迁移。
1. 执行 post-update hook，升级 AUR 包和 mise，清理孤儿包。
1. 分析日志、显示状态，需要时提示重启（比如内核更新了）。

直接 `pacman -Syu` 只完成第 5 步的一部分，会漏掉：

- 升级前的快照。
- keyring 更新和文件冲突处理。
- `--overwrite '/usr/share/omarchy/*'`。`/usr/share/omarchy` 下如果有不属于任何包的文件，pacman 会中止升级。
- migrations。包升级了但配置没迁移，次数多了容易出现配置和组件版本对不上。

另外，无论用哪个工具，都不要做部分升级（`pacman -Sy <pkg>`），Arch 不支持这样用。

### 装、卸单个软件：菜单或 pacman/yay 都可以

`omarchy-update` 只升级已经装好的包，不装新包。装新软件有三种方式，效果一样：

- Omarchy 菜单 → Install → Package（官方仓库）或 AUR，可以边输入边搜索；卸载在菜单的 Remove 下面。
- Omarchy 自带的包装脚本：`omarchy-pkg-add`、`omarchy-pkg-aur-add`、`omarchy-pkg-remove`，另有 `omarchy-pkg-present` 和 `omarchy-pkg-missing` 用来检查某个包装了没有。
- 直接用 pacman 或 yay：

```bash
sudo pacman -S <pkg>      # install from official repos
yay -S <pkg>              # install from AUR
sudo pacman -Rns <pkg>    # remove with unneeded deps and config
pacman -Qs <keyword>      # search installed packages
pacman -Qo /path/to/file  # which package owns this file
```

查询、清缓存、排查依赖、降级这些事仍然用 pacman。

一句话：升级整个系统用 `omarchy-update`，装、卸、查用菜单或 pacman/yay。

### 更新时 SSH 被拒

在 SER8 上执行 `omarchy-update` 的过程中，已经连着的 SSH 会话不受影响，但新的 SSH 连接被重置了：

```text
kex_exchange_identification: read: Connection reset by peer
```

可能是这次更新升级了 openssh，而 sshd 还没重启：pacman 升级 openssh 后不会自动重启 sshd，新连接会失败，旧会话不受影响。这只是推测，没有核实。更新结束（或重启）后还是连不上的话，在本机执行：

```bash
sudo systemctl restart sshd
```

读脚本、`ps` 查看更新进度这类只读操作不会影响正在进行的更新：

```bash
ps -eo pid,etime,args | grep -E 'omarchy-update|pacman' | grep -v grep
```

## SSH 频繁连接被拒

SER8 用来跑 AI Agent，我会从 MacBook 频繁 ssh 上去，Ansible 也走 SSH。默认配置下经常连不上，原因有两层限制，报错也不同。

### 第一层：ufw 的 LIMIT 规则

用 `omarchy-setup-security-sshd` 配 SSH 时，Omarchy 会加一条 `ufw limit 22/tcp`：同一来源 IP 在 30 秒内新建 6 个以上连接，后面的就被拒绝。客户端看到的是：

```text
ssh: connect to host 192.168.50.15 port 22: Connection refused
```

解决办法是对局域网放行，并且这条规则要排在 LIMIT 前面，因为 ufw 按顺序匹配：

```bash
sudo ufw insert 1 allow from 192.168.50.0/24 to any port 22 proto tcp comment 'ssh-lan-no-limit'
sudo ufw status numbered    # the ALLOW must sit above "22/tcp LIMIT IN Anywhere"
```

局域网外的访问仍然受 LIMIT 限制。

### 第二层：sshd 的 PerSourcePenalties

OpenSSH 9.8 开始默认开启 `PerSourcePenalties`（SER8 上是 openssh 10.6）。sshd 会给每个来源 IP 记录"坏行为"并累计罚时：

| 行为 | 罚时 |
| ---- | ---- |
| 连上后没认证就断开（noauth） | 1 秒 |
| 认证失败（authfail） | 5 秒 |
| 握手超时（grace-exceeded） | 10 秒 |

累计达到 15 秒后，这个 IP 会被暂时拒绝，最长 600 秒。客户端看到的是：

```text
kex_exchange_identification: read: Connection reset by peer
```

另外 `MaxStartups` 默认 `10:30:100`：同时处于握手阶段的连接超过 10 个后，sshd 开始随机丢弃新连接。

查看当前生效值：

```bash
sudo sshd -T | grep -iE '^(maxstartups|persourcepenalt)'
```

加一个 drop-in，让局域网免罚，并放宽握手并发：

```bash
printf '%s\n' \
  '# LAN agents: no per-source penalties, more concurrent handshakes' \
  'PerSourcePenaltyExemptList 192.168.50.0/24' \
  'MaxStartups 50:30:200' |
  sudo tee /etc/ssh/sshd_config.d/20-lan-agents.conf
sudo sshd -t && sudo systemctl reload sshd    # reload keeps existing sessions
```

### 客户端：连接复用

在 Mac 的 `~/.ssh/config` 里给这台机器开 `ControlMaster`，多次 ssh 共用一条 TCP 连接，从源头减少新建连接：

```text
Host ser8
    HostName 192.168.50.15
    ControlMaster auto
    ControlPath ~/.ssh/cm-%r@%h:%p
    ControlPersist 10m
    ServerAliveInterval 30
```

`ServerAliveInterval` 让空闲会话定期发心跳，避免被路由器的 NAT 超时掐断。

```bash
ssh -O check ser8    # "Master running" means connections are being reused
ssh -O exit ser8     # drop a stale master, e.g. after the remote host rebooted
```

SER8 上这些配置由 Ansible 管理（`configure-ai-mode` playbook），Mac 的 `~/.ssh/config` 由 chezmoi 管理，不手动改。

## 待确认 / TODO

- `omarchy-update-pacman-guard` 的作用：`omarchy-update-system-pkgs` 调 pacman 时会设环境变量 `OMARCHY_UPDATE_PACMAN=1`，guard 可能是一个 pacman hook，用来拦截或提醒绕过 `omarchy-update` 的 `pacman -Syu`，还没读它的内容。
- 4.x 的 Omarchy 菜单快捷键和 Install 菜单的具体层级（3.x 是 `Super + Alt + Space`）。
- SER8 更新期间 SSH 被拒：当时 sshd 已在罚时（PerSourcePenalties）还是 openssh 升级后没重启，没有确认；更新后机器重启，sshd 正常。
