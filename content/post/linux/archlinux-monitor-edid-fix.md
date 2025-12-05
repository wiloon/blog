---
author: "-"
date: "2025-12-04T15:30:00+08:00"
title: "Arch Linux 显示器分辨率问题修复：手动加载 EDID 固件"
categories:
  - Linux
tags:
  - Arch Linux
  - EDID
  - 显示器
  - 分辨率
  - AI-assisted
---

## EDID 简介

### 什么是 EDID？

**EDID (Extended Display Identification Data)** 是一种标准化的数据结构，用于显示器向计算机系统描述自己的能力和特性。可以将它理解为显示器的"身份证"或"技术规格说明书"。

**EDID 包含的信息**：

1. **基本标识信息**：
   - 制造商 ID（如 Dell = "DEL", Samsung = "SAM"）
   - 产品型号代码和序列号
   - 生产日期（周数/年份）

1. **显示能力参数**：
   - 支持的分辨率列表（如 1920x1200, 1600x1200, 1280x1024）
   - 支持的刷新率（如 60Hz, 75Hz）
   - 原生（推荐）分辨率
   - 色彩深度和色域信息

1. **物理特性**：
   - 屏幕物理尺寸（以毫米为单位，用于计算正确的 DPI）
   - 显示接口类型（模拟/数字）
   - Gamma 值（2.2 是常见值）

### 系统如何读取 EDID？

**是的，操作系统从显示器读取 EDID 信息。** 这是一个自动化的初始化过程：

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. 物理连接                                                  │
│    显示器连接到主机（HDMI/DisplayPort/DVI/VGA）              │
│    硬件检测到连接                                             │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. DDC 通信初始化                                            │
│    主机 → 显示器：发起 DDC (Display Data Channel) 请求       │
│    使用 I2C 总线协议                                          │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. EDID 数据传输                                             │
│    显示器 → 主机：返回 EDID 数据（128 或 256 字节）          │
│    通过显示线缆内的专用数据通道                               │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. 内核处理                                                  │
│    GPU 驱动解析 EDID → 验证校验和 → 提取支持的模式          │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. 自动配置                                                  │
│    选择最佳分辨率（通常是原生分辨率）→ 配置显示输出          │
└─────────────────────────────────────────────────────────────┘
```

**通信协议细节**：

- **HDMI/DisplayPort**：使用 DDC 协议通过 AUX 通道或 HPD (Hot Plug Detect) 引脚传输
- **VGA**：通过 DDC1/DDC2B 协议，使用视频线缆中的第 12 和 15 引脚（SDA/SCL）
- **DVI**：类似 HDMI，使用 DDC2B+ 协议

整个过程**完全自动**，无需用户干预，通常在显示器连接后的几毫秒内完成。

### EDID 读取失败的后果

当 EDID 读取失败时（就像本文要解决的问题），系统会：

```bash
# 内核日志显示错误
[drm] EDID block 0 is all zeroes         # EDID 数据全为 0
[drm:amdgpu] *ERROR* Bad EDID, status3!  # 读取失败错误代码

# xrandr 显示受限状态
DP-9 connected 1024x768+0+0 (normal left inverted right x axis y axis) 0mm x 0mm
#              ↑ 低分辨率                                               ↑ 物理尺寸未知
```

**具体影响**：

- ❌ 系统不知道显示器支持的分辨率列表
- ❌ 回退到 VESA 安全模式（通常是 1024x768）
- ❌ 物理尺寸显示为 `0mm x 0mm`（导致 DPI 计算错误）
- ❌ 无法使用原生高分辨率（如 1920x1200）
- ❌ 刷新率可能不正确

### EDID 读取失败的常见原因

1. **硬件故障**：
   - 显示器内部 EDID 芯片损坏或老化
   - 显示线缆质量差（特别是廉价转接线）
   - 接口引脚接触不良或氧化

1. **驱动/固件问题**：
   - GPU 驱动 bug（AMD/NVIDIA 驱动的已知问题）
   - 内核版本与硬件不兼容
   - 显示器固件 bug

1. **时序问题**：
   - 显示器启动较慢，系统读取时还未准备好
   - DisplayPort 热插拔检测机制故障
   - 多显示器环境下的枚举冲突

### 手动加载 EDID 固件的原理

本文介绍的解决方案是通过内核参数提供一个"备用 EDID"：

```bash
# GRUB 配置
drm.edid_firmware=DP-9:edid/dell_u2412m.bin
#                  ↑         ↑
#                  接口名    EDID 固件文件路径（相对于 /lib/firmware/）
```

**工作流程**：

```text
内核启动 → 检测到 DP-9 显示器 → 尝试读取 EDID → 失败
                                                    ↓
                            检查 drm.edid_firmware 参数
                                                    ↓
                    加载 /lib/firmware/edid/dell_u2412m.bin
                                                    ↓
                    验证 EDID 校验和 → 解析数据 → 配置显示器
                                                    ↓
                            显示器正常工作（1920x1200）
```

**关键点**：

- 只有在硬件 EDID 读取**失败**时才使用固件文件
- 如果硬件 EDID 读取成功，内核会**忽略**固件参数
- 因此，为多个接口配置 EDID 固件不会影响正常显示器

## 问题描述

在使用 Arch Linux（特别是 AMD GPU + 多显示器环境）时，可能遇到某个显示器无法识别正确分辨率的问题，表现为上述 EDID 读取失败的症状。

## 诊断问题

### 检查显示器状态

```bash
# 查看当前显示器配置
xrandr

# 查看物理尺寸（有问题的显示器会显示 0mm x 0mm）
xrandr | grep -E "connected|mm"
```

### 检查内核日志

```bash
# 查看显卡信息
lspci | grep -i vga
lspci -k | grep -A 3 -i vga

# 检查内核日志中的 EDID 错误
sudo dmesg | grep -i "drm\|amdgpu\|edid" | tail -30
```

如果看到以下错误，说明 EDID 读取失败：

```text
EDID block 0 is all zeroes
[drm:link_add_remote_sink [amdgpu]] *ERROR* Bad EDID, status3!
```

## 解决方案：手动加载 EDID 固件

通过为内核提供一个自定义的 EDID 固件文件，可以绕过硬件 EDID 读取失败的问题。

### 步骤 1：创建 EDID 固件目录

```bash
sudo mkdir -p /lib/firmware/edid
```

### 步骤 2：生成 EDID 固件文件

以 Dell U2412M 显示器（1920x1200）为例，使用 Python 生成一个校验和正确的 EDID 文件：

```bash
python3 << 'PYTHON_EOF'
#!/usr/bin/env python3
# 生成一个有效的 1920x1200 @ 60Hz EDID

edid = bytearray(128)

# Header (0-7)
edid[0:8] = [0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00]

# Manufacturer ID: "DEL" (Dell) (8-9)
edid[8:10] = [0x10, 0xAC]

# Product code (10-11)
edid[10:12] = [0x71, 0xA0]

# Serial number (12-15)
edid[12:16] = [0x4C, 0x37, 0x30, 0x41]

# Week/year of manufacture (16-17)
edid[16:18] = [12, 22]  # Week 12, 2012+10=2022

# EDID version (18-19)
edid[18:20] = [1, 3]

# Video input definition (20)
edid[20] = 0x80  # Digital

# Screen size (21-22) - 52cm x 32cm
edid[21:23] = [0x34, 0x20]

# Gamma (23)
edid[23] = 0x78  # 2.20

# Features (24)
edid[24] = 0xEE

# Color characteristics (25-34)
edid[25:35] = [0xEE, 0x95, 0xA3, 0x54, 0x4C, 0x99, 0x26, 0x0F, 0x50, 0x54]

# Established timings (35-37)
edid[35:38] = [0xA5, 0x4B, 0x00]

# Standard timings (38-53)
edid[38:40] = [0xD1, 0xC0]  # 1920x1200 @ 60Hz
edid[40:42] = [0xA9, 0x40]  # 1600x1200 @ 60Hz
edid[42:44] = [0x81, 0x80]  # 1280x1024 @ 60Hz
edid[44:46] = [0x71, 0x4F]  # 1152x864 @ 75Hz
edid[46:54] = [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01]

# Detailed timing descriptor 1 (54-71) - 1920x1200 @ 60Hz
edid[54:72] = [
    0x28, 0x3C, 0x80, 0xA0, 0x70, 0xB0, 0x23, 0x40,
    0x30, 0x20, 0x36, 0x00, 0x06, 0x44, 0x21, 0x00,
    0x00, 0x1A
]

# Display product serial number (72-89)
edid[72:90] = [
    0x00, 0x00, 0x00, 0xFF, 0x00,
    ord('D'), ord('E'), ord('L'), ord('L'), ord('0'), ord('0'), ord('0'), ord('1'),
    0x0A, 0x20, 0x20, 0x20, 0x20
]

# Display product name (90-107)
edid[90:108] = [
    0x00, 0x00, 0x00, 0xFC, 0x00,
    ord('D'), ord('E'), ord('L'), ord('L'), ord(' '), 
    ord('U'), ord('2'), ord('4'), ord('1'), ord('2'), ord('M'),
    0x0A, 0x20
]

# Display range limits (108-125)
edid[108:126] = [
    0x00, 0x00, 0x00, 0xFD, 0x00,
    0x38, 0x4C, 0x1E, 0x53, 0x11, 0x00, 0x0A,
    0x20, 0x20, 0x20, 0x20, 0x20, 0x20
]

# Extension flag (126)
edid[126] = 0x00  # No extension blocks

# Calculate checksum (127)
checksum = (256 - (sum(edid[:127]) % 256)) % 256
edid[127] = checksum

# Write to file
with open('/tmp/dell_u2412m.bin', 'wb') as f:
    f.write(edid)

print(f"Generated EDID: {len(edid)} bytes, checksum: 0x{checksum:02x}")
PYTHON_EOF
```

### 步骤 3：安装 EDID 文件

```bash
# 复制到固件目录
sudo cp /tmp/dell_u2412m.bin /lib/firmware/edid/dell_u2412m.bin

# 验证文件
stat /lib/firmware/edid/dell_u2412m.bin
```

### 步骤 4：验证 EDID 文件（可选但推荐）

```bash
# 安装 EDID 验证工具
sudo pacman -S edid-decode-git  # 或从 AUR 安装

# 验证 EDID 文件
edid-decode /lib/firmware/edid/dell_u2412m.bin | grep -E "Checksum|1920x1200"
```

**重要**：确保输出中没有校验和错误。如果看到 `Checksum: 0xXX (should be 0xYY)` 这样的错误，说明 EDID 文件有问题，内核会拒绝加载。

### 步骤 5：配置 GRUB 加载 EDID 固件

#### 方法 1：直接编辑 GRUB 配置文件

```bash
# 备份 GRUB 配置
sudo cp /etc/default/grub /etc/default/grub.backup.$(date +%Y%m%d)

# 编辑 GRUB 配置
sudo vim /etc/default/grub

# 找到 GRUB_CMDLINE_LINUX_DEFAULT 行，在末尾添加 EDID 固件参数
# 修改前：
# GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
# 修改后（注意：DisplayPort 接口编号可能在重启后变化，建议配置多个接口）：
# GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"
```

#### 方法 2：使用 sed 自动修改

```bash
# 备份 GRUB 配置
sudo cp /etc/default/grub /etc/default/grub.backup.$(date +%Y%m%d)

# 使用 sed 修改配置
sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="\(.*\)"/GRUB_CMDLINE_LINUX_DEFAULT="\1 drm.edid_firmware=DP-8:edid\/dell_u2412m.bin,DP-9:edid\/dell_u2412m.bin,DP-10:edid\/dell_u2412m.bin,DP-11:edid\/dell_u2412m.bin,DP-12:edid\/dell_u2412m.bin"/' /etc/default/grub

# 验证配置
grep "GRUB_CMDLINE_LINUX_DEFAULT" /etc/default/grub
```

### 步骤 6：更新 GRUB 并重新生成 initramfs

```bash
# 更新 GRUB 配置（Arch Linux 使用 grub-mkconfig）
sudo grub-mkconfig -o /boot/grub/grub.cfg

# 可选：重新生成 initramfs（确保 EDID 固件被包含）
sudo mkinitcpio -P

# 重启系统
sudo reboot
```

### 步骤 7：重启后验证

```bash
# 检查内核日志
sudo dmesg | grep -i edid

# 查看显示器分辨率（应该能看到 1920x1200）
xrandr

# 检查物理尺寸（应该不再是 0mm x 0mm）
xrandr | grep -E "connected|mm"

# 验证内核参数是否生效
cat /proc/cmdline | grep edid_firmware
```

## Arch Linux 特有配置（可选）

### 通过 mkinitcpio 预加载 EDID 固件

如果需要在 early boot 阶段加载 EDID（例如使用 plymouth 或需要早期图形界面），可以配置 mkinitcpio：

```bash
# 编辑 mkinitcpio 配置
sudo vim /etc/mkinitcpio.conf

# 在 FILES 数组中添加 EDID 文件
FILES=(/lib/firmware/edid/dell_u2412m.bin)

# 重新生成 initramfs
sudo mkinitcpio -P
```

### 使用 systemd-boot 的配置

如果你使用 systemd-boot 而不是 GRUB：

```bash
# 编辑引导加载器条目
sudo vim /boot/loader/entries/arch.conf

# 在 options 行添加 EDID 固件参数
# 修改前：
# options root=/dev/sda2 rw quiet
# 修改后：
# options root=/dev/sda2 rw quiet drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin
```

## 故障排除

### 问题 1：找不到正确的显示器接口

**症状**：配置后问题依然存在

**解决方法**：

1. 运行 `xrandr` 查看所有显示器接口
1. 找到显示 `0mm x 0mm` 的接口（这是有问题的显示器）
1. 更新 GRUB 配置中的接口名称

```bash
# 假设正确的接口是 DP-9
sudo vim /etc/default/grub

# 修改为正确的接口名称
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-9:edid/dell_u2412m.bin"

# 更新并重启
sudo grub-mkconfig -o /boot/grub/grub.cfg && sudo reboot
```

### 问题 2：DisplayPort 接口编号重启后变化

**症状**：上次是 DP-10，重启后变成了 DP-9

**原因**：

- 内核检测显示器的顺序可能不同
- 显示器启动时序影响接口分配
- AMD GPU 驱动的接口枚举机制

**解决方法**：同时为多个可能的接口配置 EDID

```bash
sudo vim /etc/default/grub

# 涵盖所有可能的接口（DP-8 到 DP-12）
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"

sudo grub-mkconfig -o /boot/grub/grub.cfg && sudo reboot
```

**说明**：

- 同时配置多个接口不会影响正常显示器
- 内核对能正常读取 EDID 的显示器会优先使用其自身的 EDID
- EDID 固件仅在显示器 EDID 读取失败时才生效
- 不存在的接口会被内核自动忽略

### 问题 3：Invalid firmware EDID 错误

**症状**：内核日志显示

```text
[drm] *ERROR* Invalid firmware EDID "edid/dell_u2412m.bin"
```

**原因**：EDID 文件校验和错误或文件大小不正确

**解决方法**：

1. 验证文件大小：

```bash
stat /lib/firmware/edid/dell_u2412m.bin
# 应该是 128 字节（基本块）或 256 字节（带扩展块）
```

1. 验证校验和：

```bash
edid-decode /lib/firmware/edid/dell_u2412m.bin
# 检查输出中是否有校验和错误
```

1. 如果有错误，重新生成 EDID 文件（使用上面步骤 2 的 Python 脚本）

### 问题 4：需要为其他显示器型号生成 EDID

**方法 1：从工作的显示器提取 EDID**

如果你有一台相同型号的工作正常的显示器：

```bash
# 找到显示器的 EDID 文件
find /sys/class/drm -name edid -exec sh -c 'echo "=== {} ===" && cat {}' \;

# 复制到固件目录
sudo cp /sys/class/drm/card0-DP-X/edid /lib/firmware/edid/my_monitor.bin
```

**方法 2：使用 cvt 生成自定义分辨率**

```bash
# 生成 modeline
cvt 1920 1200 60

# 输出示例：
# Modeline "1920x1200_60.00"  193.25  1920 2056 2256 2592  1200 1203 1209 1245 -hsync +vsync

# 然后修改 Python 脚本中的 Detailed timing descriptor 部分
```

### 问题 5：AUR 软件包安装失败

如果 `edid-decode-git` 从 AUR 安装失败，可以尝试：

```bash
# 方法 1：使用 yay 或其他 AUR helper
yay -S edid-decode-git

# 方法 2：手动从官方仓库安装（如果可用）
sudo pacman -S edid-decode

# 方法 3：跳过验证步骤，直接使用生成的 EDID 文件
```

## 临时测试方案（重启后失效）

在永久修复前，可以先临时测试自定义分辨率：

```bash
# 生成 modeline
cvt 1920 1200 60

# 创建新的显示模式（从 cvt 输出复制 modeline）
xrandr --newmode "1920x1200_60.00"  193.25  1920 2056 2256 2592  1200 1203 1209 1245 -hsync +vsync

# 将模式添加到显示器（替换 DP-X 为实际接口名称）
xrandr --addmode DP-9 1920x1200_60.00

# 应用新分辨率
xrandr --output DP-9 --mode 1920x1200_60.00
```

**注意**：此方法在重启后会失效，仅用于测试。

## Arch Linux 与 Ubuntu 差异总结

| 项目 | Ubuntu | Arch Linux |
|------|--------|------------|
| 包管理器 | `apt-get install` | `pacman -S` |
| GRUB 更新 | `update-grub` | `grub-mkconfig -o /boot/grub/grub.cfg` |
| initramfs 工具 | `update-initramfs` | `mkinitcpio -P` |
| EDID 解码工具 | `edid-decode` (官方仓库) | `edid-decode-git` (AUR) |
| 固件目录 | `/lib/firmware/edid/` | `/lib/firmware/edid/` (相同) |
| 内核参数 | 相同 | 相同 |

## 关键知识点

1. **EDID 的作用**：EDID 包含显示器的能力信息（支持的分辨率、刷新率、物理尺寸等），操作系统通过读取 EDID 来自动配置显示器。

1. **校验和的重要性**：EDID 文件必须有正确的校验和，否则内核会认为文件损坏而拒绝加载。校验和是前 127 字节的和取反后的低 8 位。

1. **文件大小要求**：
   - 基本 EDID：128 字节
   - 带扩展块：256 字节（128 字节基本块 + 128 字节扩展块）

1. **接口编号变化**：DisplayPort 接口编号可能在重启后变化，这是正常现象。通过配置多个接口可以解决这个问题。

1. **不影响正常显示器**：为正常显示器配置 EDID 固件不会有负面影响，内核会优先使用硬件 EDID。

## 参考资料

- [Arch Wiki - Kernel Mode Setting](https://wiki.archlinux.org/title/Kernel_mode_setting)
- [Arch Wiki - EDID](https://wiki.archlinux.org/title/Kernel_parameters#EDID)
- [Kernel EDID Firmware Documentation](https://www.kernel.org/doc/html/latest/admin-guide/edid.html)
- [EDID Wikipedia](https://en.wikipedia.org/wiki/Extended_Display_Identification_Data)
- [xrandr Manual](https://man.archlinux.org/man/xrandr.1)
