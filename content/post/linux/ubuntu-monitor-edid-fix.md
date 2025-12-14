---
author: "-"
date: "2025-12-12T16:00:00+08:00"
title: "Ubuntu 显示器分辨率问题修复：手动加载 EDID 固件"
url: ubuntu-monitor-edid-fix
categories:
  - Linux
tags:
  - Ubuntu
  - EDID
  - 显示器
  - 分辨率
  - remix
  - AI-assisted
---

## 问题描述

在使用 Ubuntu（特别是 AMD GPU + 多显示器环境）时，可能遇到显示器无法识别正确分辨率的问题：

- 显示器只能使用低分辨率（如 1024x768）
- `xrandr` 显示物理尺寸为 `0mm x 0mm`
- 内核日志出现 `EDID block 0 is all zeroes` 错误
- 休眠恢复后显示器被错误识别

## TL;DR 快速解决

```bash
# 1. 创建 EDID 固件目录
sudo mkdir -p /lib/firmware/edid

# 2. 生成 EDID 文件（以 1920x1200 显示器为例）
# 见下文 Python 脚本，生成后复制到 /lib/firmware/edid/

# 3. 配置 GRUB（替换 DP-X 为实际接口）
sudo vim /etc/default/grub
# 添加：drm.edid_firmware=DP-9:edid/dell_u2412m.bin

# 4. 更新并重启
sudo update-grub && sudo reboot
```

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

### 使用 ddcutil 验证硬件 EDID

```bash
# 安装 ddcutil
sudo apt install ddcutil

# 检测显示器（通过 DDC 协议直接读取硬件 EDID）
sudo ddcutil detect
```

如果 `ddcutil` 能正确读取显示器信息，但 `xrandr` 显示错误，说明内核缓存了错误的 EDID。

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
sudo apt-get install -y edid-decode

# 验证 EDID 文件
edid-decode /lib/firmware/edid/dell_u2412m.bin | grep -E "Checksum|1920x1200"
```

**重要**：确保输出中没有校验和错误。如果看到 `Checksum: 0xXX (should be 0xYY)` 这样的错误，说明 EDID 文件有问题，内核会拒绝加载。

### 步骤 5：配置 GRUB 加载 EDID 固件

```bash
# 备份 GRUB 配置
sudo cp /etc/default/grub /etc/default/grub.backup.$(date +%Y%m%d)

# 修改 GRUB 配置
# 注意：DisplayPort 接口编号可能在重启后变化，建议配置多个接口
sudo vim /etc/default/grub

# 添加 drm.edid_firmware 参数
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"

# 验证配置
grep "GRUB_CMDLINE_LINUX_DEFAULT" /etc/default/grub

# 更新 GRUB
sudo update-grub

# 重启系统
sudo reboot
```

### 步骤 6：重启后验证

```bash
# 检查内核日志
sudo dmesg | grep -i edid

# 查看显示器分辨率（应该能看到 1920x1200）
xrandr

# 检查物理尺寸（应该不再是 0mm x 0mm）
xrandr | grep -E "connected|mm"
```

## 多显示器场景

### 问题场景

当使用多个不同尺寸的显示器时（例如 24 寸 + 27 寸），如果为所有 DP 接口都配置了同一个 EDID 文件，可能会导致问题：

```bash
# 错误配置示例：所有接口都使用 24 寸显示器的 EDID
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"
```

**症状**：

- 系统启动时可能正常（因为硬件 EDID 读取成功）
- 休眠恢复后，27 寸显示器被识别为 24 寸
- `xrandr` 显示两个显示器物理尺寸相同
- 27 寸 4K 显示器无法使用正确的 3840x2160 分辨率

### 解决方案

**核心原则**：只为真正需要 EDID 固件的显示器配置，不要为能正常读取 EDID 的显示器配置固件。

```bash
# 编辑 GRUB 配置
sudo vim /etc/default/grub

# 修改前（错误）：所有接口都配置了 24 寸 EDID
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"

# 修改后（正确）：移除正常显示器的接口（如 DP-8）
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"

# 更新 GRUB 并重启
sudo update-grub
sudo reboot
```

### drm.edid_firmware 工作机制

内核处理 EDID 的逻辑：

```text
1. 尝试从硬件读取 EDID
2. 如果成功 → 使用硬件 EDID（忽略固件文件）
3. 如果失败 → 使用 drm.edid_firmware 指定的固件文件
```

**重要理解**：

- `drm.edid_firmware` 是**备用方案**，不是强制覆盖
- 只有当硬件 EDID 读取失败时，才会使用固件文件
- 为正常显示器配置错误的 EDID 固件，在硬件读取偶尔失败时会导致问题

## 故障排除

### 问题 1：找不到正确的显示器接口

**症状**：配置后问题依然存在

**解决方法**：

1. 运行 `xrandr` 查看所有显示器接口
2. 找到显示 `0mm x 0mm` 的接口（这是有问题的显示器）
3. 更新 GRUB 配置中的接口名称

```bash
# 假设正确的接口是 DP-9
sudo vim /etc/default/grub

# 修改为正确的接口名称
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-9:edid/dell_u2412m.bin"

# 更新并重启
sudo update-grub && sudo reboot
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
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"

sudo update-grub && sudo reboot
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

2. 验证校验和：

```bash
edid-decode /lib/firmware/edid/dell_u2412m.bin
# 检查输出中是否有校验和错误
```

3. 如果有错误，重新生成 EDID 文件（使用上面步骤 2 的 Python 脚本）

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

## 附录：EDID 背景知识

### 什么是 EDID？

**EDID (Extended Display Identification Data)** 是一种标准化的数据结构，用于显示器向计算机系统描述自己的能力和特性。可以将它理解为显示器的"身份证"。

**EDID 包含的信息**：

- **基本标识**：制造商 ID、产品型号、序列号、生产日期
- **显示能力**：支持的分辨率列表、刷新率、原生分辨率、色彩深度
- **物理特性**：屏幕物理尺寸（用于计算 DPI）、接口类型、Gamma 值

### 系统如何读取 EDID？

```text
显示器连接 → DDC 通信初始化 → EDID 数据传输 → GPU 驱动解析 → 自动配置显示
```

**通信协议**：

- **HDMI/DisplayPort**：使用 DDC 协议通过 AUX 通道传输
- **VGA**：通过 DDC1/DDC2B 协议，使用视频线缆中的专用引脚
- **DVI**：类似 HDMI，使用 DDC2B+ 协议

### EDID 读取失败的常见原因

1. **硬件故障**：显示器 EDID 芯片损坏、线缆质量差、接口接触不良
2. **驱动/固件问题**：GPU 驱动 bug、内核不兼容、显示器固件 bug
3. **时序问题**：显示器启动慢、热插拔检测故障、多显示器枚举冲突

### 关键知识点

1. **校验和的重要性**：EDID 文件必须有正确的校验和，否则内核会拒绝加载。校验和是前 127 字节的和取反后的低 8 位。

2. **文件大小要求**：
   - 基本 EDID：128 字节
   - 带扩展块：256 字节

3. **接口编号变化**：DisplayPort 接口编号可能在重启后变化，这是正常现象。

4. **运行时刷新限制**：内核的 EDID 缓存在运行时无法通过简单方法刷新，需要重启才会重新读取。

## 参考资料

- [Kernel EDID Firmware Documentation](https://www.kernel.org/doc/html/latest/admin-guide/edid.html)
- [EDID Wikipedia](https://en.wikipedia.org/wiki/Extended_Display_Identification_Data)
- [xrandr Manual](https://man.archlinux.org/man/xrandr.1)
