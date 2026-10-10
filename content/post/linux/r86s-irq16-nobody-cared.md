---
title: "R86S IRQ 16 nobody cared：HD Audio 控制器引发的共享中断告警"
author: "-"
date: 2026-10-10T09:02:35+08:00
lastmod: 2026-10-10T10:00:00+08:00
url: r86s-irq16-nobody-cared
categories:
  - Linux
tags:
  - linux
  - kernel
  - proxmox
  - homelab
  - remix
  - AI-assisted
---

## 背景

homelab 里的 r86s（R86S 小主机，Celeron N5100，Jasper Lake 平台）跑 Proxmox VE，上面是 K8s 的两台 VM：k8s-50 和 k8s-51，拓扑见 [Homelab topology](../cloud/homelab-topology.md)。这台机器偶尔会整机卡死，所以每天 04:00 有一个定时任务自动 `apt full-upgrade` 加重启。

排查卡死问题时，在内核日志里看到了这样一段：

```text
kernel: irq 16: nobody cared (try booting with the "irqpoll" option)
kernel: CPU: 0 UID: 0 PID: 47 Comm: kworker/u16:1 Tainted: P           O        7.0.14-20-pve #1
kernel: Hardware name: BROUNION R86S/R86S, BIOS 5.19 04/12/2022
kernel: Workqueue: pm pm_runtime_work
...
kernel: handlers:
kernel: [<...>] idma64_irq [idma64]
kernel: [<...>] i2c_dw_isr
kernel: [<...>] i801_isr [i2c_i801]
kernel: [<...>] sdhci_irq [sdhci] threaded [<...>] sdhci_thread_irq [sdhci]
kernel: [<...>] azx_interrupt [snd_hda_codec]
kernel: Disabling IRQ #16
```

这篇记录这条告警是什么意思、根因是什么、影响什么，以及能用哪些 OS 或 BIOS 配置消除它。

## 环境

| 项目 | 值 |
| ---- | -- |
| 硬件 | BROUNION R86S，Intel Celeron N5100 |
| BIOS | American Megatrends 5.19（2022-04-12） |
| 系统 | Proxmox VE 9.2，内核 `7.0.14-22-pve` |
| 存储 | Samsung 970 EVO Plus 2TB（NVMe，PVE 系统盘和 VM 盘）；板载 128G eMMC（未使用） |

## 告警的含义

`irq 16: nobody cared` 来自内核中断子系统的伪中断检测（`kernel/irq/spurious.c` 里的 `note_interrupt()`）。

IRQ 16 是一条电平触发的共享中断线。中断来了，内核会依次调用挂在这条线上的所有处理函数，每个函数检查是不是自己的设备发的：是就返回 `IRQ_HANDLED`，不是就返回 `IRQ_NONE`。

如果一条线上 100,000 次中断里有 99,900 次没有任何处理函数认领，内核就认为这条线"卡住"了：某个设备一直拉着中断线，却没有驱动来清除它。这时内核会：

1. 打印 `nobody cared`，附上当前 CPU 的调用栈和这条线上的处理函数列表；
2. 禁用这条中断线（`Disabling IRQ #16`），防止中断风暴把 CPU 拖死；
3. 之后每 100ms 轮询一次这条线上的处理函数，作为兜底。

注意，打印出来的调用栈只是第 100,000 次中断到达时 CPU 正好在执行的代码，不一定和中断来源有关。r86s 上记录到的调用栈有空闲进程 `swapper/0`、KVM 的 vCPU 线程，也有 `pm_runtime_work`，要结合多次记录一起看。

## 排查

### 哪些设备共享 IRQ 16

```bash
grep -E '^ *16:' /proc/interrupts
# 16:  637379  0  0  0  IR-IO-APIC  16-fasteoi  idma64.0, i2c_designware.0, i801_smbus, mmc0, snd_hda_intel:card0
```

列出 legacy IRQ 是 16 的 PCI 设备：

```bash
for d in /sys/bus/pci/devices/*; do
  [ "$(cat $d/irq)" = 16 ] && lspci -s "$(basename $d)" -nn
done
```

| PCI 地址 | 设备 | 驱动 | 是否真的用 IRQ 16 |
| -------- | ---- | ---- | ----------------- |
| 00:15.0 | Serial IO I2C Host Controller | intel-lpss（idma64、i2c_designware） | 是 |
| 00:1a.0 | eMMC Controller | sdhci-pci（mmc0） | 是 |
| 00:1f.3 | HD Audio | snd_hda_intel | 是（MSI 被驱动关掉了，见下文） |
| 00:1f.4 | SMBus | i801_smbus | 是 |
| 00:04.0 | Dynamic Tuning service | 无 | 否 |
| 00:05.0 | IPU（摄像头） | 无（缺固件，probe 失败） | 否 |
| 01:00.0 | I211 网卡 | igb | 否，用 MSI-X，`DisINTx+` |
| 04:00.0 | NVMe SSD | nvme | 否，用 MSI-X，`DisINTx+` |

### 几乎每次开机都会出现

统计最近 20 次开机，18 次出现了 `irq 16: nobody cared`，出现时间从开机后十几分钟到二十个小时不等：

```bash
for b in $(journalctl --list-boots --no-pager | awk '{print $1}' | tail -20); do
  echo "boot $b: $(journalctl -b "$b" -k --no-pager | grep -c 'irq 16: nobody cared')"
done
```

而同一时间段里整机卡死只发生了两次。所以这条告警和卡死不是一一对应的。

### 声卡驱动的嫌疑

开机日志里 HD Audio 控制器有三行异常：

```text
snd_hda_intel 0000:00:1f.3: azx_get_response timeout, switching to polling mode: last cmd=0x000f0000
snd_hda_intel 0000:00:1f.3: No response from codec, disabling MSI: last cmd=0x000f0000
snd_hda_intel 0000:00:1f.3: Codec #0 probe error; disabling it...
```

HD Audio 控制器上可以挂多个 codec（音频编解码芯片），每个占一个地址。r86s 上：

- 地址 2 是 HDMI 音频 codec（`Intel Jasperlake HDMI`），能正常工作；
- 地址 0 是模拟音频 codec 的位置。R86S 没有 3.5mm 音频口，这里没有可用的 codec，但控制器报告这里有设备，驱动去探测时超时了。

驱动把超时当作中断投递有问题，于是关掉 MSI，退回到传统的 INTx 中断，也就是共享的 IRQ 16。

### 控制器在不停地休眠和唤醒

`snd_hda_intel` 默认开着运行时电源管理：`power_save=1`（空闲 1 秒就休眠），`power_save_controller=Y`（休眠时复位控制器）。每 0.5 秒采样一次控制器的运行时 PM 状态：

```bash
for i in $(seq 1 10); do
  printf '%s ' "$(cat /sys/bus/pci/devices/0000:00:1f.3/power/runtime_status)"
  sleep 0.5
done
# resuming resuming suspending resuming resuming resuming resuming suspending resuming resuming
```

开机 17,698 秒里，它真正处于 `suspended` 状态的时间累计只有 440 毫秒（`power/runtime_suspended_time`）。控制器一直在休眠和唤醒之间来回切换，每次切换都要停止或重新初始化控制器。

### 调用栈

有 3 次告警正好打断了内核里的电源管理任务（`pm_runtime_work`），调用栈都落在声卡驱动的休眠或唤醒路径上：

```text
# 2026-09-26 and 2026-10-08 04:20
RIP: 0010:snd_hdac_bus_stop_chip+0x45/0x100 [snd_hda_core]
 azx_stop_chip+0xe/0x20 [snd_hda_codec]
 __azx_shutdown_chip+0x17/0xc0 [snd_hda_intel]
 azx_runtime_suspend+0x5a/0xe0 [snd_hda_intel]
 pci_pm_runtime_suspend+0x6a/0x1b0

# 2026-10-08 10:45
RIP: 0010:hda_intel_init_chip+0xd0/0x2a0 [snd_hda_intel]
 __azx_runtime_resume+0x50/0x110 [snd_hda_intel]
 azx_runtime_resume+0x43/0xdc [snd_hda_intel]
 pci_pm_runtime_resume+0x97/0xf0
```

其余几次的调用栈是空闲进程或 KVM vCPU，说明不了来源。

## 根因

综合上面的证据，推断的过程如下：

1. 地址 0 的模拟 codec 探测超时，驱动关掉了 MSI，HD Audio 控制器改用共享的 IRQ 16。
2. 运行时电源管理让控制器反复休眠、唤醒、复位。
3. 在休眠或唤醒的切换过程中，控制器拉起了中断。HD Audio 控制器的中断处理函数 `azx_interrupt()` 有一个检查：设备不是 runtime active 状态时直接返回 `IRQ_NONE`。所以这时候的中断没有人认领。
4. 电平触发的中断线一直保持拉高，中断不停地重复触发，没人认领的次数很快达到阈值，内核禁用了 IRQ 16。告警前日志里出现的 `perf: interrupt took too long` 也说明当时 CPU0 正在被中断风暴占用。

这里还缺一个最直接的证据：IRQ 16 被禁用之后中断风暴就停了，事后用 `lspci -vvv` 查看各设备 Status 寄存器的 `INTx+` 位，已经看不到是谁拉着中断线。所以目前的结论是根据统计、调用栈和驱动行为推断出来的。要证实，可以按下文的方法消除 HD Audio 控制器之后观察几天，如果告警不再出现，就可以确认。

## 影响

IRQ 16 被禁用后，这条线上的设备收不到中断，只能靠内核每 100ms 轮询一次，功能还在，但响应变慢：

| 设备 | 在 r86s 上的用途 | 影响 |
| ---- | ---------------- | ---- |
| HD Audio | 无 | 无 |
| eMMC（mmcblk0，116G） | 未使用：没有分区，不在 LVM 里，也不是 swap | 无；如果以后要用，读写会非常慢 |
| I2C 控制器 / idma64 | 基本不用 | 无 |
| SMBus | 读取内存 SPD、部分传感器 | 可以忽略 |
| NVMe、I211 网卡 | PVE 系统盘、VM 存储、网络 | 不受影响，走 MSI-X |

对内核来说，涉及的是中断子系统：伪中断检测，以及禁用后的轮询兜底。中断风暴期间 IRQ 16 的中断全部落在 CPU0 上，会造成短暂的延迟尖峰，正好调度在 CPU0 上的 VM vCPU 会卡顿一下。线被禁用后就恢复正常了。

和整机卡死的关系：

- 告警几乎每天都有，卡死只有两次，没有对应关系；
- 两次卡死的日志都是突然中断的，没有 panic 也没有 oops，最后一条就是普通的 cron 日志；
- 所以目前看 IRQ 16 不是卡死的主因，卡死需要另外排查（见文末）。

## 解决方法

目标是让 HD Audio 控制器不再参与 IRQ 16，或者不再反复休眠和唤醒。按彻底程度从高到低列出：

| 方法 | 层级 | 效果 | 需要重启 | 代价 |
| ---- | ---- | ---- | -------- | ---- |
| 1. BIOS 里关闭 HD Audio | 固件 | 控制器从 PCI 总线上消失 | 是，要接显示器和键盘进 BIOS | 无 |
| 2. 屏蔽声卡驱动 | OS | 控制器不再被驱动使用 | 是 | 失去 HDMI 音频（r86s 上用不到） |
| 3. 关闭声卡的运行时电源管理 | OS | 控制器不再反复休眠和唤醒 | 是（模块参数）；用 sysfs 可以立即生效 | 控制器常驻 D0，多耗一点电 |
| 4. 只探测 HDMI codec | OS | 避免地址 0 超时，MSI 不被关掉 | 是 | 效果需要验证 |

### 方法 1：BIOS 里关闭 HD Audio

AMI Aptio 的 BIOS 一般在 Chipset → PCH-IO Configuration → HD Audio Configuration 里有 HD Audio 开关，改成 Disabled。R86S 的 BIOS 菜单我还没有实际进去确认过，具体位置以实物为准。

关闭后 `00:1f.3` 不会再出现在 `lspci` 里，驱动也不会加载，最彻底。缺点是需要接显示器和键盘进 BIOS 操作，而且以后升级或重置 BIOS 后可能恢复默认值。

### 方法 2：屏蔽声卡驱动（推荐）

在不进 BIOS 的情况下，这是最直接的办法：

```bash
cat > /etc/modprobe.d/blacklist-hda.conf <<'EOF'
# r86s has no analog audio; snd_hda_intel falls back to shared IRQ 16 and triggers "irq 16: nobody cared"
blacklist snd_hda_intel
# other drivers that can claim the same HDA controller (00:1f.3)
blacklist snd_sof_pci_intel_icl
blacklist snd_soc_avs
EOF
update-initramfs -u -k all
```

r86s 上这个 PCI 设备除了 `snd_hda_intel`，还有 SOF（`snd_sof_pci_intel_icl`）和 AVS（`snd_soc_avs`）两个驱动可能接管，所以一起屏蔽。`blacklist` 只阻止按设备别名自动加载，正常启动时就是这种方式，够用了。

重启后验证：

```bash
lspci -k -s 00:1f.3                    # no "Kernel driver in use" line
grep -E '^ *16:' /proc/interrupts      # snd_hda_intel no longer listed
journalctl -b -k | grep -c 'irq 16: nobody cared'   # expect 0
```

r86s 每天 04:00 会自动重启，配置写好之后不需要手动重启，第二天就生效。

### 方法 3：关闭声卡的运行时电源管理

如果想保留驱动，可以只关掉省电机制，让控制器一直保持工作状态：

```bash
cat > /etc/modprobe.d/hda-no-powersave.conf <<'EOF'
# keep the HDA controller in D0; runtime suspend/resume races with the shared IRQ 16
options snd_hda_intel power_save=0 power_save_controller=N
EOF
update-initramfs -u -k all
```

不重启的话，也可以通过 sysfs 立即关掉这个设备的运行时 PM。重启后会失效，适合用来做实验：

```bash
echo on > /sys/bus/pci/devices/0000:00:1f.3/power/control
cat /sys/bus/pci/devices/0000:00:1f.3/power/runtime_status   # expect "active"
```

这个方法只是去掉了触发条件，控制器仍然挂在共享的 IRQ 16 上。

### 方法 4：只探测 HDMI codec

`probe_mask` 参数可以限制驱动探测哪些 codec 地址。只探测地址 2（HDMI）的话，就不会出现地址 0 的超时，理论上驱动也就不会关掉 MSI，控制器能继续使用独占的 MSI 中断，不再占用 IRQ 16：

```bash
# bit 2 = codec address 2 (HDMI)
echo 'options snd_hda_intel probe_mask=4' > /etc/modprobe.d/hda-probe-mask.conf
update-initramfs -u -k all
```

这个方法我还没有验证过，需要重启后确认 `00:1f.3` 是否在使用 MSI（`lspci -vv -s 00:1f.3` 里 `MSI: Enable+`），以及 `/proc/interrupts` 里 IRQ 16 这一行还有没有 `snd_hda_intel`。

### 不推荐的做法

- `irqpoll` 或 `irqfixup` 内核参数：让内核在其他中断里顺带轮询所有处理函数，开销大，只是掩盖问题。
- `noirqdebug` 内核参数：会关掉伪中断检测本身。中断风暴不会再被内核拦下，反而可能一直占着 CPU0。

## 是不是 R86S 的通病

2026-10 在网上查了一圈（中英文，关键词包括 R86S、Jasper Lake、N5100/N5105，以及这组处理函数 `idma64` / `i2c_designware` / `sdhci` / `azx_interrupt`），没有找到 R86S 或 Jasper Lake 上 `irq 16: nobody cared` 的公开报告，所以不能说它是公认的 R86S 通病。

不过这个模式本身由来已久，在其他硬件上反复出现过：

- HD Audio 去探测一个不存在的 codec 槽位，超时后关掉 MSI，退回 INTx 共享中断，最后共享线被内核禁用。ALSA 维护者 Takashi Iwai 2006 年就分析过：HDA 硬件即使开着 MSI 也照样会发 INTx，驱动接不住，内核最终把这条线关掉（[LKML](https://lkml.indiana.edu/0610.2/0836.html)）。
- 2011 年 AMD E-450 上也有 `azx_interrupt` 挂在 IRQ 16 上被禁用的报告（[LKML](https://lkml.iu.edu/hypermail/linux/kernel/1111.3/02157.html)）。
- 内核 ALSA 文档说，访问不存在或不工作的 codec 槽位会卡住 HD-audio 总线，官方给的规避方法就是用 `probe_mask` 限制探测的槽位，也就是上文的方法 4。
- 有 Jasper Lake 用户的 HDA 控制器是被 SOF 驱动 `sof-audio-pci-intel-icl` 接管的（[Manjaro 论坛](https://forum.manjaro.org/t/jasper-lake-hd-audio-recognized-but-no-sound-as-usual/117082/9)），所以方法 2 要把 SOF 和 AVS 一起屏蔽。
- 网上常见的 `pci=nomsi` 不适合这里：它会让更多设备挤到共享中断线上，反而更糟。

我的推断是：同款 R86S 跑 Linux 大概率都会出现这条告警，只是它基本无害，很少有人去追。这只是推断，没有公开资料证实。

## 卡死问题的后续

IRQ 16 解决之后，整机卡死仍然需要单独排查。和 IRQ 16 不同，Jasper Lake（N5100/N5105/N6005）跑 Proxmox 随机卡死是有大量报告的平台问题：

- Proxmox 论坛长帖 [VM freezes irregularly](https://forum.proxmox.com/threads/vm-freezes-irregularly.111494/post-551842) 和 [VMs freezing randomly](https://forum.proxmox.com/threads/vms-freezing-randomly.113037/)，主要怀疑 CPU microcode 和 C-state。尝试过的办法有更新 microcode、更新 BIOS（新 BIOS 自带新 microcode）、`intel_idle.max_cstate=1`、换新内核，效果都因人而异，没有公认的彻底解决办法。
- R86S 专帖 [Issues on R86S](https://forum.proxmox.com/goto/post?id=533305)（2023-02，N6005）：起第二台 VM 就整个节点卡住，装了 `intel-microcode` 后看起来解决了，但帖子没有长期跟进。

r86s 上的 microcode 状态（2026-10-10 核对）：

```bash
grep -m1 microcode /proc/cpuinfo            # microcode : 0x24000026
journalctl -k -b | grep microcode           # Updated early from: 0x0000001d
dpkg -l intel-microcode                     # 3.20251111.1~deb13u1 (non-free-firmware)
```

- BIOS 5.19 自带的 microcode 是 `0x1d`，非常旧；
- `intel-microcode` 包 2025-10-09 就已经装上了，开机时早期加载（early load）把它更新到 `0x24000026`；
- Intel 官方仓库里 `06-9c-00`（Jasper Lake）最新的就是 `0x24000026`，日期 2023-09-26，到 2026-09 的历次 release 都没有再更新它。

也就是说，microcode 已经是最新的，卡死都是在最新 microcode 下发生的，论坛里"装 microcode 解决"的办法在这台机器上已经用过了。

BIOS 也走不通：这台的 BIOS Version 字段只有 `5.19`，和 AMI Aptio 内核版本（BIOS Revision）相同，没有厂商自己的版本号（另一台 GoWin 版 R86S 是 `JSP18422`，2023-05-14），问了生产厂家，没有更新的 BIOS。AMI 不直接向用户提供 BIOS，跨品牌刷 GoWin 的固件有变砖风险，暂时不考虑。

### 已采取的措施（2026-10-10）

先保证卡死后能自动恢复、能留下现场，再逐个变量地尝试修复：

| 措施 | 配置 | 作用 |
| ---- | ---- | ---- |
| 硬件看门狗 | `/etc/default/pve-ha-manager`：`WATCHDOG_MODULE=iTCO_wdt` | 原来是 `softdog`，内核卡死时它也跟着失效，卡死后分别过了约 10.5 小时和 4 小时才恢复。换成芯片组 TCO 看门狗，`watchdog-mux` 停止喂狗约 10 秒后硬件复位（原理见 [硬件看门狗](hardware-watchdog.md)） |
| lockup 自动 panic | `/etc/sysctl.d/90-lockup-panic.conf`：`kernel.softlockup_panic=1`、`kernel.hardlockup_panic=1`、`kernel.panic=10` | 内核检测到 lockup 就 panic，10 秒后重启 |
| EFI pstore | 默认已开（`efi_pstore` + `systemd-pstore`） | panic 时内核日志尾部存进 UEFI 变量，下次开机归档到 `/var/lib/systemd/pstore` |
| netconsole | r86s 上 `netconsole.service`（`modprobe netconsole netconsole=6666@192.168.50.5/vmbr0,6666@192.168.50.6/<n100 MAC>`）；n100 上 `netconsole-r86s.service`（socat 收 UDP 6666 写进 journald） | 卡死时日志来不及落盘，之前的卡死日志都是突然中断。netconsole 实时把内核日志发到 n100，用 `journalctl -t netconsole-r86s` 查看。写 journald 受其总量上限约束，加上单元自身限速，不会写满磁盘 |
| 控制台日志级别 | `kernel.printk = 5 4 1 7` | 原来是 3，只有 emerg/alert/crit 会发到 netconsole；改成 5 后 hung task、WARN 也能发出去 |
| 屏蔽声卡驱动 | 上文方法 2 | 消除 IRQ 16 告警和 CPU0 上的中断风暴 |

netconsole 绑在网桥 `vmbr0` 上时，一开始报错：

```text
netpoll: (null): fwpr103p0 doesn't support polling, aborting
```

网桥要求所有端口都支持 netpoll。VM 网卡设置了 `firewall=1` 时，PVE 会插入一层 `fwbr`/`fwpr`/`fwln`（veth），veth 不支持 netpoll。这台机器的 PVE 防火墙本来就没启用，所以把两台 VM 网卡的 `firewall` 改成 0（`qm set <vmid> --net0 ...,firewall=0`，运行中修改只会短暂断网），tap 直接挂在 `vmbr0` 上，netconsole 就正常了。

后续：观察两周左右。如果还有卡死，先看 n100 上的 netconsole 日志和 `/var/lib/systemd/pstore`，再单独试 `intel_idle.max_cstate=1`。

R86S 的硬件配置见 [Hardware](../Hardware/hardware.md#r86s)。
