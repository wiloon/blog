---
title: "systemd linger: 注销后保持用户服务运行"
author: "-"
date: 2026-10-17T07:47:57+08:00
lastmod: 2026-10-17T07:47:57+08:00
url: systemd-linger
categories:
  - Linux
tags:
  - systemd
  - loginctl
  - linger
  - remix
  - AI-assisted
---

linger 是 systemd-logind 的一个按用户设置的开关。打开后，这个用户的 systemd 用户实例（`user@UID.service`）在开机时就启动，并且在用户所有会话都退出后也继续运行。它解决的问题是：用 `systemctl --user` 管理的服务，默认只在用户登录期间存在。

## 默认行为（没有 linger）

每个用户有一个自己的 systemd 实例 `user@UID.service`，`systemctl --user` 操作的就是它。默认情况下：

- 用户第一次登录（SSH、图形界面、TTY 都算）时，logind 启动 `user@UID.service`，同时创建 `/run/user/UID`（即 `XDG_RUNTIME_DIR`）
- 用户最后一个会话结束后（默认再等 `UserStopDelaySec=10s`），logind 停掉 `user@UID.service`，删除 `/run/user/UID`
- 机器重启后，用户不登录，`user@UID.service` 就不会启动

结果是：`systemctl --user enable` 的服务，在用户登出后会被停掉，重启后要等用户登录才会起来；用户级的 timer 在没人登录时也不会触发。

## 打开 linger 之后

- 开机时就启动 `user@UID.service`，不等登录
- 所有会话退出后，`user@UID.service` 和 `/run/user/UID` 继续保留
- 用户级服务、timer、socket 像系统服务一样常驻

linger 只决定用户实例的生命周期，对系统级服务（`/etc/systemd/system` 下的 unit）没有影响。

## 命令

```bash
# enable linger for the current user (needs sudo or polkit auth)
sudo loginctl enable-linger $USER

# disable it
sudo loginctl disable-linger $USER

# check: Linger=yes / no
loginctl show-user $USER -p Linger

# logind keeps one empty marker file per lingering user
ls /var/lib/systemd/linger/
```

`/var/lib/systemd/linger/<user>` 这个空文件就是全部的持久化状态，`enable-linger` 创建它，`disable-linger` 删掉它。做配置管理时（比如 Ansible），可以用这个文件判断是否已经打开：

```yaml
- name: Enable linger
  command: loginctl enable-linger {{ ansible_user }}
  args:
    creates: /var/lib/systemd/linger/{{ ansible_user }}
  become: yes
```

## 和 KillUserProcesses 的关系

`/etc/systemd/logind.conf` 里的 `KillUserProcesses` 控制的是另一件事：会话结束时，要不要杀掉这个会话里启动的进程（比如在 SSH 里直接起的 `tmux`、`nohup` 进程）。

| | 会话里直接起的进程 | `systemctl --user` 服务 |
| --- | --- | --- |
| `KillUserProcesses=no`（大多数发行版的默认值，Arch 也是） | 登出后继续运行 | 没有 linger 时随用户实例停掉；有 linger 时继续运行 |
| `KillUserProcesses=yes` | 登出后被杀，linger 也保不住 | 同上 |

所以：

- 想让进程在登出后、重启后都在，正确做法是把它写成用户级 service，再打开 linger
- 在 `KillUserProcesses=yes` 的机器上，临时进程可以用 `systemd-run --user --scope <cmd>` 跑在用户实例下面，脱离会话；这同样依赖 linger，否则用户实例一停，进程也跟着停

```bash
# check the effective value (commented line = compiled-in default)
systemd-analyze cat-config systemd/logind.conf | grep KillUserProcesses
```

## 常见用途

- rootless 容器：rootless containerd / nerdctl、podman 的守护进程都是用户级服务，不开 linger，登出后容器就没了，见 [nerdctl](../cloud/nerdctl.md)
- 长期运行的用户级服务：syncthing、个人同步脚本、用户级 timer 定时任务
- 24 小时跑 AI Agent 的主机：agent 写成 `systemctl --user` 服务，配合 linger，SSH 断开或机器重启后都能自己起来

我在 homelab 的 SER8 上就是这样配的：桌面是 Omarchy，平时 SSH 进去跑 agent，打开 linger 之后 SSH 断开，用户级服务照样运行。

## 参考

- `man loginctl`（`enable-linger` 一节）
- `man logind.conf`（`KillUserProcesses`、`UserStopDelaySec`）
- [systemd, systemctl](systemd.md)
