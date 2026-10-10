---
title: "硬件看门狗：主板上的倒计时复位电路"
author: "-"
date: 2026-10-10T11:00:00+08:00
lastmod: 2026-10-10T12:00:00+08:00
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
- 定时器的时钟源被固件关掉了，倒计时根本不走。r86s 就是这种情况，而且驱动加载、sysfs 状态都看不出任何异常（见下文"实测"）；
- 所以启用之后一定要实际测一次。

**TCO** 是 Total Cost of Ownership 的缩写，是 Intel 当年为降低企业 PC 运维成本推出的一组芯片组功能，看门狗定时器是其中之一。Intel 的 TCO 定时器是两段式的：第一次超时只置状态位（可以触发 SMI），第二次超时才复位整机。`iTCO_wdt` 驱动会处理这个细节，对用户来说就是设一个超时时间。

### r86s 上的 TCO 看门狗

```text
iTCO_wdt iTCO_wdt: Found a Intel PCH TCO device (Version=6, TCOBASE=0x0400)
iTCO_wdt iTCO_wdt: initialized. heartbeat=30 sec (nowayout=0)
```

没有报 `NO_REBOOT` 错误，说明 BIOS 没锁"不复位"位。它一直都在 PCH 里，只是之前没人用。不过后来实测发现，光这样还不够。

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

## 实测：一只不会叫的狗

硬件看门狗"能加载"不代表"真能复位"。测试方法是让 `watchdog-mux` 停止喂狗：

```bash
# WARNING: hard-resets the host in ~10s; VMs go down without a clean shutdown
kill -STOP $(pidof watchdog-mux)
```

`SIGSTOP` 让进程暂停而不退出，`/dev/watchdog` 一直开着却没人喂狗，约 10 秒后机器应该直接复位。测试前先把 VM 正常关机，免得它们被硬复位。

### 第一次测试：没有复位

2026-10-10 11:04:18 执行，`watchdog-mux` 确实停住了（`ps` 状态 `T`），也没有其他进程打开 `/dev/watchdog`，但等了两分钟机器都没有复位。sysfs 里的 `timeleft` 一直停在 9，不往下走。

于是直接读芯片组寄存器。TCO 寄存器在 I/O 端口 `TCOBASE=0x400`，ACPI 寄存器在 `0x1800`（见 `/proc/ioports`），可以用 Python 读 `/dev/port`：

```python
import os
p = os.open("/dev/port", os.O_RDONLY)
def io(addr, n):
    os.lseek(p, addr, 0)
    return int.from_bytes(os.read(p, n), "little")
print(hex(io(0x400, 2)), hex(io(0x408, 2)), hex(io(0x1808, 4)))
```

| 寄存器 | 读数 | 含义 |
| ------ | ---- | ---- |
| `TCO_RLD`（`0x400`），TCO 当前计数 | 一直是 `0x10` | 倒计时停住了。`0x10` = 16 个 tick × 0.6 秒 ≈ 10 秒，是刚喂过狗的初始值 |
| `TCO1_CNT`（`0x408`） | `0x1000` | 暂停位（bit 11）和 v6 的 `NO_REBOOT` 位（bit 0）都是 0，TCO 本身的配置没问题 |
| ACPI PM 定时器（`0x1808`） | 一直是 `0x375c4b` | 本来是一个不停跳动的 3.58MHz 计数器，现在完全不动 |

ACPI PM 定时器不走是关键：**TCO 定时器就是用 ACPI 定时器的时钟来计数的**。再看电源管理控制器（PMC）的 MMIO 寄存器 `ACPI_TMR_CTL`（`PWRMBASE 0xfe000000 + 0x18FC`）：

```python
import os, mmap
f = os.open("/dev/mem", os.O_RDONLY | os.O_SYNC)
m = mmap.mmap(f, 0x1000, mmap.MAP_SHARED, mmap.PROT_READ, offset=0xfe001000)
print(hex(int.from_bytes(m[0x8fc:0x900], "little")))   # 0x2
```

读出来是 `0x2`，bit 1 `ACPI_TIM_DIS` = 1，**ACPI 定时器被关掉了**。所以 TCO 计数器永远停在初始值，看门狗永远不会到点。驱动正常加载，sysfs 显示 `active`，`watchdog-mux` 也在正常喂狗，表面上一切正常，实际上就是一只不会叫的狗。

Intel 新平台的固件里有"关闭 ACPI 定时器以省电"的选项（coreboot 和 FSP 都有对应配置），代价就是 TCO 看门狗也跟着停。

### 是谁关的

- 开机时内核成功注册了 `acpi_pm` 时钟源，而内核注册前会检查这个定时器在不在走，说明那时它还在走，是开机过程中稍后才被关掉的；
- 内核 2024 年给 `intel_pmc_core` 加过"休眠时关闭 ACPI 定时器"的功能，但只在系统休眠时生效。实测把这一位清零后卸载、重新加载 `intel_pmc_core`，这一位仍然是 0，不是它关的；
- 清零后它一直保持为 0，系统运行期间没有再被关掉。

结论是开机过程中由固件（ACPI 或 SMM 代码）关掉的一次性动作。具体是哪一步，要更细的开机追踪才能定位，意义不大，直接在开机后把它改回去就行。

### 修复和第二次测试

把 `ACPI_TIM_DIS` 清零：

```python
m = mmap.mmap(f, 0x1000, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=0xfe001000)
v = int.from_bytes(m[0x8fc:0x900], "little")
m[0x8fc:0x900] = (v & ~0x2).to_bytes(4, "little")
```

清零后 PM 定时器开始跳，`TCO_RLD` 也从 `0x10` 降到了 `0xf`。再测一次：

| 时间 | 事件 |
| ---- | ---- |
| 11:17:18 | `kill -STOP watchdog-mux` |
| 11:17:19 到 11:17:28 | `timeleft` 从 9 一秒一秒倒数到 0 |
| 约 11:17:29 | 硬复位，SSH 断开 |
| 11:17:58 | 重新开机，两台 VM（`onboot: 1`）自动起来 |

上一次启动的日志停在 11:17:18，没有任何关机过程，这正是硬件复位的特征。

### 让它每次开机都生效

复位重启后 `ACPI_TMR_CTL` 又变回了 `0x2`，所以要在开机后自动清零。做成一个 systemd timer：开机 30 秒后运行一次，之后每 5 分钟检查一次。脚本把这一位清零，再读两次 PM 定时器，确认它在走：

```python
#!/usr/bin/python3
import os, mmap, sys, syslog, time

PWRM_PAGE, OFF, DIS = 0xfe001000, 0x8fc, 0x2      # ACPI_TMR_CTL = PWRMBASE + 0x18FC
PM_TMR = 0x1808

f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
m = mmap.mmap(f, 0x1000, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=PWRM_PAGE)
v = int.from_bytes(m[OFF:OFF + 4], "little")
if v & DIS:
    m[OFF:OFF + 4] = (v & ~DIS).to_bytes(4, "little")
    syslog.syslog(syslog.LOG_WARNING, f"ACPI_TIM_DIS was set (ACPI_TMR_CTL={v:#x}), cleared")

p = os.open("/dev/port", os.O_RDONLY)
def pm_tmr():
    os.lseek(p, PM_TMR, 0)
    return int.from_bytes(os.read(p, 4), "little")
a = pm_tmr(); time.sleep(0.01); b = pm_tmr()
if a == b:
    syslog.syslog(syslog.LOG_ERR, f"ACPI PM timer still stopped ({a:#x}); iTCO watchdog will not fire")
    sys.exit(1)
```

每 5 分钟检查一次，是为了防止固件在运行时又把它关掉，真关了也能自动恢复并留下日志（`journalctl -t acpi-timer-enable`）。开机后到第一次运行之间约 30 秒，看门狗是失效的，这个窗口很短，可以接受。

`PWRMBASE`、寄存器偏移这些地址是 Jasper Lake 平台的，换别的平台要查对应的数据手册或 coreboot 源码。内核要允许 `/dev/mem` 访问这段 MMIO：PVE 内核是 `CONFIG_STRICT_DEVMEM=y`，但没有开 `CONFIG_IO_STRICT_DEVMEM`，这段区域也没有被驱动占用，所以可以访问。

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
| 硬件看门狗 | `WATCHDOG_MODULE=iTCO_wdt`，加上开机后清除 `ACPI_TIM_DIS` 的 `acpi-timer-enable` | 检测不到的整机卡死：`watchdog-mux` 停止喂狗，约 10 秒后 PCH 直接复位（已实测） |

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
- 观察期过后，如果真实的卡死也被看门狗正常拉起来了（`kill -STOP` 测试已经通过，但真实卡死可能是另一种形态），可以把定时任务改成每周一次升级加重启，减少 K8s 节点（k8s-51 是 control plane）每天被重启的扰动。

## 2026-10-10 排查记录

r86s 这一天做的事情，按顺序：

| 步骤 | 做了什么 | 发现或结果 |
| ---- | -------- | ---------- |
| 1. IRQ 16 告警 | 分析 `irq 16: nobody cared`，屏蔽声卡驱动 | 声卡探测空 codec 超时、退回共享 IRQ 16、运行时电源管理反复休眠唤醒引发中断风暴；告警基本无害，不是卡死主因（详见 [R86S IRQ 16 nobody cared](r86s-irq16-nobody-cared.md)） |
| 2. 查网上资料 | IRQ 16 和 Jasper Lake 卡死 | IRQ 16 在 R86S 上没有公开报告；Jasper Lake 跑 Proxmox 随机卡死是有大量报告的平台问题，常见建议是更新 microcode 和 BIOS |
| 3. microcode | 查当前版本 | 已是 Intel 发布的最新版 `0x24000026`，`intel-microcode` 包 2025-10 就装了，卡死都发生在最新 microcode 下 |
| 4. BIOS | 查版本、问厂家 | BIOS 5.19（2022-04-12），Version 字段没有厂商版本号；厂家没有新 BIOS；AMI 不直接给用户 BIOS，跨品牌刷有变砖风险，暂不刷 |
| 5. 卡死时的日志 | 统计最近 25 次开机 | 3 周内卡死 4 次；soft/hard lockup、hung task 日志一条都没有，卡死瞬间日志根本没落盘 |
| 6. lockup 自动 panic | `softlockup_panic=1`、`hardlockup_panic=1`、`panic=10`、`printk=5` | 能检测到的 lockup 会 panic 并重启；EFI pstore 本来就开着，panic 现场会存进 UEFI 变量 |
| 7. netconsole | r86s 发、n100 收（socat 写进 journald） | 绑在 `vmbr0` 上时报 `fwpr103p0 doesn't support polling`：VM 网卡 `firewall=1` 插入的 veth 不支持 netpoll。PVE 防火墙本来没开，把两台 VM 网卡改成 `firewall=0` 后正常 |
| 8. 硬件看门狗 | `WATCHDOG_MODULE=iTCO_wdt` | 驱动正常加载、sysfs 显示 active |
| 9. 测试看门狗 | `kill -STOP watchdog-mux` | 第一次没有复位：固件开机时设置了 `ACPI_TIM_DIS`，TCO 计数器不走 |
| 10. 修复 | 清除 `ACPI_TIM_DIS`，做成开机后和每 5 分钟运行的 systemd timer | 第二次测试，停止喂狗约 10 秒后硬复位，VM 自动恢复 |

还没解决的：卡死的根因。接下来观察两周左右，如果再卡死，先看 n100 上的 netconsole 日志（`journalctl -t netconsole-r86s`）和 r86s 上的 `/var/lib/systemd/pstore`，再单独试 `intel_idle.max_cstate=1`。

上面这些服务器配置都收进了 w10n-config 仓库的 `infra/homelab/pve-r86s-stability/`，用 Ansible 部署（`task deploy`），`task status` 查看看门狗、ACPI 定时器、IRQ 16 和 netconsole 的状态。

## 参考

- Linux 内核文档：[The Linux Watchdog driver API](https://docs.kernel.org/watchdog/watchdog-api.html)
- Linux 内核文档：[Softlockup detector and hardlockup detector](https://docs.kernel.org/admin-guide/lockup-watchdogs.html)
- Proxmox VE 文档：[High Availability - Fencing](https://pve.proxmox.com/wiki/High_Availability#ha_manager_fencing)
- [R86S IRQ 16 nobody cared](r86s-irq16-nobody-cared.md)
