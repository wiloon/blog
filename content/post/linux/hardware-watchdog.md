---
title: "硬件看门狗：主板上的倒计时复位电路"
author: "-"
date: 2026-10-10T11:00:00+08:00
lastmod: 2026-10-10T11:00:00+08:00
url: hardware-watchdog
categories:
  - Linux
tags:
  - linux
  - kernel
  - hardware
  - proxmox
  - homelab
  - remix
  - AI-assisted
---

## 背景

homelab 里的 r86s（R86S 小主机，Celeron N5100，跑 Proxmox VE）偶尔整机卡死。卡死后机器既不会自己恢复，也不会留下日志，前几次分别过了约 10.5 小时和 4 小时才被人发现并重启。排查过程见 [R86S IRQ 16 nobody cared](r86s-irq16-nobody-cared.md)。

在修不了根因（BIOS 没有更新、microcode 已是最新）的情况下，第一件要做的事是让机器卡死后能自动恢复，这就是硬件看门狗的用途。这篇记录硬件看门狗是什么、Linux 和 Proxmox 怎么用它，以及它在 r86s 这次排查里起的作用。

## 看门狗是什么

看门狗（watchdog timer，WDT）是一个独立于 CPU 运行的倒计时器：

1. 软件启动看门狗，设一个超时时间，比如 10 秒；
2. 软件定期"喂狗"（kick / pet），每次喂狗把倒计时重置回 10 秒；
3. 如果软件卡死、没人喂狗，倒计时走到 0，看门狗就直接拉复位信号，把整台机器重启。

关键在于**独立**：倒计时由芯片组里的电路自己走，不依赖 CPU 执行任何指令。CPU 死锁、内核卡死、关了中断，它都照样倒数，照样复位。这一点是软件手段做不到的。

这个思路最早来自嵌入式和工控领域：无人值守的设备死机了没人去按电源键，必须自己恢复。单片机几乎都内置看门狗。

## 硬件看门狗在哪里

它通常不是一块单独的板卡或模块，而是集成在芯片里的一小块电路。x86 机器上常见的几种：

| 位置 | 例子 | Linux 驱动 |
| ---- | ---- | ---------- |
| Intel 芯片组（ICH/PCH）里的 TCO 定时器 | 从 1999 年的 ICH 一直到现在的 PCH，包括 Jasper Lake | `iTCO_wdt` |
| AMD 芯片组（FCH）里的 TCO 定时器 | 大部分 AMD 平台 | `sp5100_tco` |
| 主板上的 Super I/O 芯片 | ITE IT87xx、Nuvoton NCT67xx、Fintek F718xx | `it87_wdt`、`w83627hf_wdt`、`f71808e_wdt` |
| 服务器的 BMC | IPMI 看门狗 | `ipmi_watchdog` |
| ARM SoC | 树莓派的 BCM2835 | `bcm2835_wdt` |

所以"几乎所有 x86 主板都有"是成立的，至少芯片组里会有一个 TCO 定时器。但"有"不等于"能用"：

- BIOS 可以设置并锁定 TCO 的 `NO_REBOOT` 位，这时定时器照样倒数，到点却不复位，驱动加载时会报 `unable to reset NO_REBOOT flag`；
- 有些板子的复位线路接得不对，超时后什么也不发生；
- 所以启用之后最好实际测一次（见文末）。

**TCO** 是 Total Cost of Ownership 的缩写，是 Intel 当年为降低企业 PC 运维成本推出的一组芯片组功能，看门狗定时器是其中之一。Intel 的 TCO 定时器是两段式的：第一次超时只置状态位（可以触发 SMI），第二次超时才复位整机。`iTCO_wdt` 驱动会处理这个细节，对用户来说就是设一个超时时间。

### r86s 上的 TCO 看门狗

```text
iTCO_wdt iTCO_wdt: Found a Intel PCH TCO device (Version=6, TCOBASE=0x0400)
iTCO_wdt iTCO_wdt: initialized. heartbeat=30 sec (nowayout=0)
```

没有报 `NO_REBOOT` 错误，说明 BIOS 没锁。它一直都在 PCH 里，只是之前没人用。

## Linux 里的看门狗

### 统一接口：/dev/watchdog

Linux 内核把所有看门狗驱动统一成一个字符设备 `/dev/watchdog`（主设备号 10，次设备号 130），多个看门狗时还有 `/dev/watchdog0`、`/dev/watchdog1`……

- 打开设备：看门狗开始倒数；
- 往里写任何内容，或者调用 `WDIOC_KEEPALIVE` ioctl：喂狗；
- 写一个字符 `V` 再关闭（magic close）：停止看门狗。如果没写 `V` 就关闭，或者进程崩溃了，看门狗继续倒数，到点复位。这正是我们想要的：喂狗的进程死了，机器就重启；
- `nowayout` 模式下，看门狗一旦启动就无法停止。

在 sysfs 里能看到状态：

```bash
cat /sys/class/watchdog/watchdog0/identity   # iTCO_wdt
cat /sys/class/watchdog/watchdog0/timeout    # 10
cat /sys/class/watchdog/watchdog0/timeleft   # 9（倒计时剩余秒数）
cat /sys/class/watchdog/watchdog0/state      # active
```

### softdog：纯软件的"看门狗"

内核还有一个 `softdog` 驱动，接口和硬件看门狗完全一样，但倒计时是内核里的一个定时器。它能发现"用户态的喂狗进程挂了"，但内核本身卡死时，定时器也跟着停，就复位不了机器了。

### 内核的 lockup 检测器：另一种 watchdog

内核里还有一组也叫 watchdog 的东西，容易混淆，它们是**检测器**，不是复位电路：

| 检测器 | 检测什么 | 原理 |
| ------ | -------- | ---- |
| soft lockup detector | 某个 CPU 长时间（默认 20 秒）在内核态不让出调度 | 每个 CPU 上跑一个高优先级的 watchdog 内核线程，长时间得不到运行就报警 |
| hard lockup detector（NMI watchdog） | 某个 CPU 长时间（默认 10 秒）关着中断不响应 | 用性能计数器定时产生 NMI（不可屏蔽中断），在 NMI 里检查时钟中断还在不在走 |
| hung task detector | 进程长时间（默认 120 秒）处于 D 状态 | 内核线程 `khungtaskd` 定期扫描 |

它们默认只打印告警。设置 `kernel.softlockup_panic=1`、`kernel.hardlockup_panic=1` 后，检测到 lockup 就 panic，再配合 `kernel.panic=10`，panic 10 秒后自动重启。

但它们都依赖内核和 CPU 还能执行代码。如果整个 CPU 或芯片组卡死，NMI 都送不进去，这些检测器也就失效了。这时只能靠硬件看门狗。

### 三层保护的关系

| 故障 | lockup 检测器 + panic | softdog | 硬件看门狗 |
| ---- | --------------------- | ------- | ---------- |
| 喂狗进程卡死，内核正常 | 无效 | 能复位 | 能复位 |
| 内核某个 CPU 死锁，其他 CPU 正常 | 能 panic 重启，还能留下调用栈 | 不一定 | 能复位 |
| 内核整体卡死，中断全停 | NMI 还能进就有效，否则无效 | 无效 | 能复位 |
| CPU 或芯片组硬件层面卡死 | 无效 | 无效 | 能复位 |

越往右越可靠，但能留下的信息越少：panic 能打印调用栈，硬件看门狗复位就是直接拉复位线，什么也不留。所以通常是几层一起用：能 panic 就 panic，留下现场；panic 不了就靠硬件看门狗兜底。

## Proxmox VE 的 watchdog-mux

Proxmox 默认就在用看门狗，管理它的是 `watchdog-mux` 服务：

- 它打开 `/dev/watchdog`，每秒喂一次狗，超时时间设为 10 秒；
- 它本身也是一个"复用器"：HA 管理器（`pve-ha-lrm`、`pve-ha-crm`）连到 `watchdog-mux` 上喂它。启用了 HA 的节点如果和集群失联，HA 管理器会故意停止喂狗，让节点被看门狗复位，这就是 HA 的 fencing（隔离）。没有启用 HA 时，`watchdog-mux` 就只是自己喂狗；
- 用哪个看门狗由 `/etc/default/pve-ha-manager` 里的 `WATCHDOG_MODULE` 决定，**默认是 `softdog`**；
- PVE 的内核包把所有硬件看门狗驱动都放进了黑名单（`/lib/modprobe.d/blacklist_pve-kernel-*.conf`），防止它们被自动加载、抢占 `/dev/watchdog`。指定了 `WATCHDOG_MODULE` 后，由 `watchdog-mux` 在启动时加载对应模块。

PVE 默认用 softdog，是因为它在所有机器上都能工作，而硬件看门狗在某些板子上的行为不可靠。代价就是内核卡死时它管不了。

### 在 r86s 上启用 iTCO

```bash
# /etc/default/pve-ha-manager
WATCHDOG_MODULE=iTCO_wdt
```

重启后：

```bash
cat /sys/class/watchdog/watchdog0/identity   # iTCO_wdt（原来是 Software Watchdog）
cat /sys/class/watchdog/watchdog0/timeout    # 10
ls -l /proc/$(pidof watchdog-mux)/fd | grep watchdog   # 3 -> /dev/watchdog
```

注意一个坑：`/etc/default/pve-ha-manager` 原文件末尾没有换行，直接 `echo ... >>` 追加会把新行拼到最后一行注释后面，变成注释，配置不生效。

## 在 r86s 这次排查中的作用

### 之前：卡死后没有任何东西能把机器拉起来

- 看门狗是 `softdog`，内核卡死时它也跟着停了；
- lockup 检测器开着，但只告警不 panic，而且告警写不到盘上；
- 每天 04:00 的定时重启是从另一台机器 SSH 过来触发的，机器卡死时 SSH 连不上，也没用；
- 结果就是卡死后一直挂着，直到有人发现、手动断电重启：两次分别挂了约 10.5 小时和 4 小时，上面两台 K8s VM 也跟着停摆。

### 现在：几层保护

| 层次 | 配置 | 卡死后的结果 |
| ---- | ---- | ------------ |
| netconsole | 内核日志实时发到 n100 | 卡死前最后的内核日志留在 n100 上 |
| lockup 检测 + panic | `softlockup_panic=1`、`hardlockup_panic=1`、`panic=10` | 能检测到的 lockup：panic，调用栈发到 netconsole、存进 EFI pstore，10 秒后重启 |
| 硬件看门狗 | `WATCHDOG_MODULE=iTCO_wdt` | 检测不到的整机卡死：`watchdog-mux` 停止喂狗，约 10 秒后 PCH 直接复位 |

硬件看门狗是最后一道兜底，作用是把卡死后的停机时间从几个小时缩短到一两分钟（10 秒超时，加上 BIOS 自检和系统启动）。

它**不解决根因**。机器还是会卡死，只是能自己恢复了。根因还得靠 netconsole 和 pstore 抓到的日志去查。另外，看门狗复位和断电一样，是不正常关机：VM 来不及关机，磁盘缓存里还没写回的数据会丢失。所以它是兜底，不能代替正常的 `reboot`。

## 有了看门狗，还需要每天定时重启吗

r86s 每天 04:00 跑一次 `apt full-upgrade` 加 `reboot`，当初加它就是因为这台机器不稳定。有了硬件看门狗之后，它是不是就可以去掉了？要分开看它的两个作用：

1. **升级系统**：这个和看门狗无关，内核和 microcode 升级都需要重启才能生效，总得有个升级重启的机制，只是不一定要每天。
2. **预防卡死**：每天重启能不能减少卡死，取决于卡死和运行时长有没有关系。从记录看，卡死发生在开机后几个小时到十几个小时不等，每天重启并没有阻止卡死；而硬件看门狗管的是卡死之后的恢复，这两件事不冲突。

而且看门狗只覆盖"整机卡死、`watchdog-mux` 不再喂狗"这一种情况。下面这些它管不了：

- 部分卡死：比如某台 VM 卡住、网卡没流量、存储 I/O 卡住，但内核和 `watchdog-mux` 都还在跑，照样喂狗；
- 性能慢慢变差、内存泄漏之类的问题。

结论：

- 观察期（约两周）内先**保留**每天重启。这期间要验证看门狗、netconsole、声卡屏蔽是否有效，此时改掉定时重启等于多了一个变量（运行时长），出了问题分不清原因；
- 观察期过后，如果确认看门狗能正常把卡死的机器拉起来，可以把定时任务改成每周一次升级加重启，减少 K8s 节点（k8s-51 是 control plane）每天被重启的扰动。

## 测试看门狗

硬件看门狗"能加载"不代表"真能复位"，最好实际测一次。方法是让 `watchdog-mux` 停止喂狗：

```bash
# WARNING: hard-resets the host in ~10s; VMs go down without a clean shutdown
kill -STOP $(pidof watchdog-mux)
```

`SIGSTOP` 让进程暂停而不退出，`/dev/watchdog` 一直开着却没人喂狗，约 10 秒后机器应该直接复位。重启后看 `journalctl --list-boots`，上一次启动的日志应该是突然中断的，没有关机过程。

测试前先把 VM 关掉，或者确认能接受它们被硬复位。

## 参考

- Linux 内核文档：[The Linux Watchdog driver API](https://docs.kernel.org/watchdog/watchdog-api.html)
- Linux 内核文档：[Softlockup detector and hardlockup detector](https://docs.kernel.org/admin-guide/lockup-watchdogs.html)
- Proxmox VE 文档：[High Availability - Fencing](https://pve.proxmox.com/wiki/High_Availability#ha_manager_fencing)
- [R86S IRQ 16 nobody cared](r86s-irq16-nobody-cared.md)
