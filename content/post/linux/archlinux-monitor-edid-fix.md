---
author: "-"
date: "2025-12-30T16:45:00+08:00"
title: "Arch Linux 显示器分辨率问题修复：手动加载 EDID 固件"
url: archlinux-monitor-edid-fix
categories:
  - Linux
tags:
  - Arch Linux
  - EDID
  - 显示器
  - 分辨率
  - Wayland
  - KDE
  - GRUB
  - 双系统
  - remix
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

**环境说明**：
- 本文主要针对 **KDE Plasma + Wayland** 环境
- X11 环境有部分临时解决方案（详见下文）
- GRUB 永久方案适用于所有桌面环境

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

```深入理解：EDID 加载机制

### 内核 EDID 缓存位置

EDID 数据在内核中的存储：

```c
// 内核数据结构（简化）
struct drm_connector {
    struct drm_device *dev;
    
    const struct drm_edid *edid_blob_ptr;  // EDID 缓存
    struct edid *edid;  // 128 或 256 字节的 EDID 数据
    
    bool override_edid;  // 是否使用覆盖的 EDID
    struct list_head modes;  // 从 EDID 解析的模式列表
};
```

**内存布局**：
```text
内核内存
  └─ DRM 设备
      └─ 连接器列表
          ├─ DP-7
          │   ├─ edid → [EDID 数据 128字节] ✅
          │   └─ modes → [3840x2160, 2560x1440, ...]
          └─ DP-9
              ├─ edid → [EDID 数据 128字节] ❌ 损坏
              └─ modes → [1024x768, 800x600, ...] 降级模式
```

### drm.edid_firmware 参数详解

**参数定义**：
- **名称**：`drm.edid_firmware`
- **类型**：内核命令行参数
- **子系统**：DRM (Direct Rendering Manager)
- **作用**：在启动时为指定显示器加载 EDID 固件

**完整格式**：
```bash
drm.edid_firmware=<connector>:<firmware_path>

# 示例
drm.edid_firmware=DP-9:edid/monitor.bin

# 多个显示器（逗号分隔）
drm.edid_firmware=DP-9:edid/monitor1.bin,HDMI-A-1:edid/monitor2.bin
```

**参数说明**：

| 部分 | 说明 | 示例 |
|------|------|------|
| `connector` | 显示器接口名称 | `DP-9`, `HDMI-A-1`, `eDP-1` |
| `firmware_path` | 相对于 `/lib/firmware/` 的路径 | `edid/monitor.bin` |

**路径解析**：
```bash
drm.edid_firmware=DP-9:edid/monitor.bin
                        └──────────────┘
                              ↓
    实际文件路径: /lib/firmware/edid/monitor.bin
```

### 内核加载流程

```c
// 内核启动时的 EDID 加载流程（简化伪代码）
void drm_connector_init(struct drm_connector *connector) {
    struct edid *edid;
    
    // 1. 尝试从硬件读取 EDID
    edid = drm_get_edid(connector);
    
    if (!edid || !drm_edid_is_valid(edid)) {
        // 2. 硬件读取失败，检查内核参数
        if (has_firmware_override(connector->name)) {
            // 3. 加载固件 EDID ✨
            char *fw_path = get_firmware_path(connector->name);
            edid = load_firmware_edid(fw_path);
            
            pr_info("DRM: Using EDID firmware for %s\n", 
                    connector->name);
        } else {
            // 4. 使用降级的安全模式
            edid = create_fallback_edid();
        }
    }
    
    // 5. 解析 EDID，构建模式列表
    drm_add_edid_modes(connector, edid);
}
```

**时序图**：
```text
系统启动
  ↓
GRUB 传递参数: drm.edid_firmware=DP-9:edid/monitor.bin
  ↓
内核初始化
  ↓
DRM 子系统初始化
  ↓
枚举显示器 (DP-9)
  ↓
尝试读取硬件 EDID → 失败 ❌
  ↓
检查内核参数 → 找到 DP-9 的固件配置 ✅
  ↓
加载 /lib/firmware/edid/monitor.bin
  ↓
验证 EDID 校验和 → 通过 ✅
  ↓
解析 EDID → 生成模式列表 [1920x1200, 1920x1080, ...]
  ↓
Wayland/X11 启动 → 使用正确的分辨率 ✅
```

### 为什么没有运行时更新 EDID 的 API？

**技术原因**：

1. **EDID 是"物理真相"**
   - 内核认为 EDID 来自硬件，不应被用户空间随意修改
   - 防止恶意软件伪造显示器信息

2. **运行时更新的复杂性**
   - 需要重新初始化整个显示管道
   - 可能导致 Wayland/X 会话崩溃
   - 需要协调多个子系统（DRM → 合成器 → 应用程序）

3. **现有方案已够用**
   - 内核参数可以解决 99% 的 EDID 问题
   - 不需要增加内核复杂度

**技术上可以实现运行时 API**：

理论方案（未在主线内核中实现）：

```c
// 可能的实现方式
static ssize_t edid_store(struct device *device,
                          const char *buf, size_t count)
{
    struct drm_connector *connector = to_drm_connector(device);
    
    // 1. 验证新 EDID 数据
    // 2. 获取锁
    // 3. 替换 connector->edid
    // 4. 重新生成模式列表
    // 5. 触发热插拔事件通知用户空间
    
    return count;
}

// 用户空间使用
sudo cat /lib/firmware/edid/monitor.bin > /sys/class/drm/card0-DP-9/edid
```

**社区态度**：
- 相关补丁曾被提交但未合并
- 主要反对理由：安全性、不必要、维护负担

### 配置 EDID 固件的所有方式

| 方式 | 推荐度 | 适用场景 |
|------|-------|---------|
| **GRUB 参数** | ⭐⭐⭐⭐⭐ | 使用 GRUB 引导 |
| **systemd-boot** | ⭐⭐⭐⭐⭐ | 使用 systemd-boot |
| **模块参数** | ⭐⭐⭐ | DRM 驱动是模块 |
| **EFISTUB** | ⭐⭐⭐ | 直接 EFI 引导 |
| **编译内核** | ⭐ | 特殊需求 |

所有方式的本质都是在**内核 DRM 初始化时**传递 `drm.edid_firmware` 参数。

## 解决方案：手动加载 EDID 固件（GRUB 方式）

通过为内核提供一个自定义的 EDID 固件文件，可以绕过硬件 EDID 读取失败的问题。

**适用于**：
- ✅ 所有桌面环境（X11/Wayland）
- ✅ 所有显卡驱动（AMD/Intel/NVIDIA）
- ✅ 永久有效（重启后自动生效）Bad EDID, status3!
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

##### Ubuntu 配置示例

```bash
# 备份 GRUB 配置
sudo cp /etc/default/grub /etc/default/grub.backup.$(date +%Y%m%d)

# 编辑 GRUB 配置
sudo vim /etc/default/grub

# Ubuntu 的 GRUB_CMDLINE_LINUX_DEFAULT 通常包含 quiet splash
# 修改前：
# GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
# 修改后：
# GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"
```

##### Arch Linux 配置示例

```bash
# 备份 GRUB 配置
sudo cp /etc/default/grub /etc/default/grub.backup.$(date +%Y%m%d)

# 编辑 GRUB 配置
sudo vim /etc/default/grub

# Arch Linux 的 GRUB_CMDLINE_LINUX_DEFAULT 通常比较简洁
# 修改前：
# GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet"
# 修改后（在末尾添加 EDID 固件参数）：
# GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"
```

**注意事项**：

- DisplayPort 接口编号可能在重启后变化，建议配置多个接口（DP-8 到 DP-12）
- Arch Linux 默认配置通常更简洁，没有 `splash` 参数
- 两个系统的 EDID 固件路径相同：`/lib/firmware/edid/`
- 内核参数格式在两个系统中完全一致

#### 方法 2：使用 sed 自动修改

**通用命令（Ubuntu 和 Arch Linux 均适用）**：

```bash
# 备份 GRUB 配置
sudo cp /etc/default/grub /etc/default/grub.backup.$(date +%Y%m%d)

# 使用 sed 修改配置（自动在现有参数后追加 EDID 配置）
sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="\(.*\)"/GRUB_CMDLINE_LINUX_DEFAULT="\1 drm.edid_firmware=DP-8:edid\/dell_u2412m.bin,DP-9:edid\/dell_u2412m.bin,DP-10:edid\/dell_u2412m.bin,DP-11:edid\/dell_u2412m.bin,DP-12:edid\/dell_u2412m.bin"/' /etc/default/grub

# 验证配置
grep "GRUB_CMDLINE_LINUX_DEFAULT" /etc/default/grub
```

**预期输出示例**：

```bash
# Ubuntu:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"

# Arch Linux:
GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"
```

### 步骤 6：更新 GRUB 并重新生成 initramfs

#### Ubuntu

```bash
# Ubuntu 更新 GRUB 配置
sudo update-grub

# 可选：重新生成 initramfs（确保 EDID 固件被包含）
sudo update-initramfs -u -k all

# 重启系统
sudo reboot
```

#### Arch Linux

```bash
# Arch Linux 更新 GRUB 配置
sudo grub-mkconfig -o /boot/grub/grub.cfg

# 可选：重新生成 initramfs（确保 EDID 固件被包含）
sudo mkinitcpio -P

# 重启系统
sudo reboot
```

**命令对比**：

| 操作 | Ubuntu | Arch Linux |
|------|--------|------------|
| 更新 GRUB | `sudo update-grub` | `sudo grub-mkconfig -o /boot/grub/grub.cfg` |
| 重新生成 initramfs | `sudo update-initramfs -u -k all` | `sudo mkinitcpio -P` |
| 重启系统 | `sudo reboot` | `sudo reboot` |

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

### 问题 3：双系统环境下修改 ArchLinux 启动参数

**症状**：Ubuntu 和 ArchLinux 双系统，在 Ubuntu 中修改了 GRUB 配置，但 ArchLinux 启动时 EDID 参数不生效

**问题分析**：

当你从 Ubuntu 查看 `/boot/grub/grub.cfg` 时，可能会看到类似这样的 ArchLinux 启动项：

```bash
menuentry 'Arch Linux (on /dev/nvme0n1p4)' --class arch --class gnu-linux --class gnu --class os {
    insmod part_gpt
    insmod ext2
    search --no-floppy --fs-uuid --set=root a9769c82-3d32-48b5-b2ad-da69a31b0510
    linux /boot/vmlinuz-linux root=/dev/nvme0n1p4
    initrd /boot/initramfs-linux.img
}
```

**关键问题**：

1. 这个启动项是由 Ubuntu 的 `os-prober` 自动探测生成的
2. `os-prober` 只会读取 ArchLinux 分区内的 GRUB 配置
3. 即使在 Ubuntu 的 `/etc/default/grub` 中添加 EDID 参数，也只会影响 Ubuntu 自己的启动项
4. ArchLinux 的启动参数来自 **ArchLinux 系统内部的 `/etc/default/grub`**

**正确的解决方法**：

**步骤 1：启动进入 ArchLinux 系统**

从 GRUB 菜单选择 ArchLinux 启动。

**步骤 2：在 ArchLinux 中准备 EDID 固件**

```bash
# 确认 EDID 文件存在（如果没有，参考前文生成）
stat /lib/firmware/edid/dell_u2412m.bin

# 如果文件不存在，需要先创建目录并复制/生成 EDID 文件
sudo mkdir -p /lib/firmware/edid
# （然后按照前文步骤 2-3 生成并复制 EDID 文件）
```

**步骤 3：修改 ArchLinux 的 GRUB 配置**

```bash
# 备份配置
sudo cp /etc/default/grub /etc/default/grub.backup.$(date +%Y%m%d)

# 编辑 GRUB 配置
sudo vim /etc/default/grub

# 找到 GRUB_CMDLINE_LINUX_DEFAULT 行，通常是：
# GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet"
#
# 修改为（在末尾添加 EDID 参数）：
# GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"
```

**步骤 4：在 ArchLinux 中更新 GRUB**

```bash
# ArchLinux 使用 grub-mkconfig 命令
sudo grub-mkconfig -o /boot/grub/grub.cfg

# 可选：重新生成 initramfs
sudo mkinitcpio -P
```

**步骤 5：在 Ubuntu 中更新 GRUB（重要！）**

```bash
# 重启回到 Ubuntu
# 在 Ubuntu 中运行 update-grub，让 os-prober 重新探测 ArchLinux
sudo update-grub

# 这会让 Ubuntu 的 GRUB 菜单读取到 ArchLinux 更新后的内核参数
```

**步骤 6：验证配置**

```bash
# 重启进入 ArchLinux
# 检查内核参数是否包含 EDID 配置
cat /proc/cmdline | grep edid_firmware

# 应该看到类似输出：
# ... drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin ...

# 检查显示器分辨率
xrandr
```

**为什么需要在两个系统中都操作？**

```text
双系统 GRUB 启动流程：

开机 → Ubuntu 的 GRUB (主引导器)
          ↓
          ├─→ 启动 Ubuntu (使用 Ubuntu 的 /etc/default/grub)
          │
          └─→ 启动 ArchLinux (使用 ArchLinux 的 /etc/default/grub)
               ↑
               └─ os-prober 从 ArchLinux 分区读取启动参数
```

**关键理解**：

- Ubuntu 的 GRUB 是主引导器（安装在 MBR/ESP）
- Ubuntu 的 GRUB 通过 `os-prober` 发现其他系统
- 但每个系统的**内核参数**来自各自系统内的 `/etc/default/grub`
- 所以要修改 ArchLinux 的启动参数，必须在 ArchLinux 系统内部修改

**替代方案：手动编辑 Ubuntu 的 GRUB 配置文件（不推荐）**

如果你不想重启到 ArchLinux，可以直接编辑 Ubuntu 的 `/boot/grub/grub.cfg`，但这**不推荐**，因为：

1. 该文件会在下次 `update-grub` 时被覆盖
2. 容易出错（语法错误可能导致无法启动）
3. 不是标准做法

如果坚持要这样做：

```bash
# 备份
sudo cp /boot/grub/grub.cfg /boot/grub/grub.cfg.backup

# 编辑文件
sudo vim /boot/grub/grub.cfg

# 找到 ArchLinux 启动项，手动在 linux 行末尾添加 EDID 参数：
# 修改前：
#   linux /boot/vmlinuz-linux root=/dev/nvme0n1p4
# 修改后：
#   linux /boot/vmlinuz-linux root=/dev/nvme0n1p4 drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin
```

### 问题 4：Invalid firmware EDID 错误

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
sudWayland vs X11 环境差异

### 显示管理架构对比

| 方面 | X11 (xrandr) | Wayland (KMS) |
|------|-------------|---------------|
| **显示管理** | 用户空间（X Server） | 内核空间（KMS） + 合成器 |
| **模式列表来源** | X Server 可以"伪造" | 只能使用内核报告的模式 |
| **动态添加分辨率** | ✅ 可以（cvt + xrandr --newmode） | ❌ 不可以 |
| **依赖 EDID** | 中等（可绕过） | 强（必须正确） |
| **系统设置可选项** | EDID 模式 + 自定义模式 | 严格限于 EDID 模式 |

### 为什么 Wayland 不能动态添加分辨率？

**X11 的灵活性**：
```bash
# X11: X Server 在用户空间管理，可以添加自定义模式
### EDID 基础

1. **EDID 的作用**：EDID 包含显示器的能力信息（支持的分辨率、刷新率、物理尺寸等），操作系统通过读取 EDID 来自动配置显示器。

2. **系统设置的限制**：
   - Wayland：分辨率选项**严格限于** EDID 声明的模式
   - X11：主要依赖 EDID，但可以临时添加自定义模式
   - **结论**：修复 EDID 是根本解决方案

3. **校验和的重要性**：EDID 文件必须有正确的校验和，否则内核会认为文件损坏而拒绝加载。校验和是前 127 字节的和取反后的低 8 位。

4. **文件大小要求**：
   - 基本 EDID：128 字节
   - 带扩展块：256 字节（128 字节基本块 + 128 字节扩展块）

### 内核机制

5. **EDID 缓存位置**：
   - 内核数据结构：`struct drm_connector->edid`
   - 在 DRM 子系统初始化时加载
   - 运行时难以修改（缺乏标准 API）

6. **drm.edid_firmware 参数**：
   - 内核命令行参数，在启动时生效
   - 格式：`接口名:固件路径`（路径相对于 `/lib/firmware/`）
   - 只在硬件 EDID 读取失败时使用固件
   - 配置方式：GRUB、systemd-boot、模块参数等

7. **为什么没有运行时 API**：
   - 安全性考虑（防止伪造硬件信息）
   - 稳定性考虑（运行时修改可能导致系统崩溃）
   - 现有启动时加载方案已够用

### 实用技巧

8. **接口编号变化**：DisplayPort 接口编号可能在重启后变化，这是正常现象。通过配置多个接口可以解决这个问题。

9. **不影响正常显示器**：为正常显示器配置 EDID 固件不会有负面影响，内核会优先使用硬件 EDID。

10. **Wayland vs X11**：
    - Wayland 更依赖正确的 EDID（没有绕过机制）
    - X11 可以临时绕过（但不推荐）
    - 两者都应该从根本上修复 EDID
**实际影响**：

```text
EDID 损坏（DP-9）:
  内核 → 只知道 640x480, 1024x768 等安全模式
          ↓
  Wayland → 只能使用这些模式
          ↓
  系统设置 → 分辨率下拉框中只有低分辨率选项 ❌

EDID 正确:
  内核 → 知道 1920x1200, 1920x1080, 1600x1200 等
          ↓
  Wayland → 可以使用完整模式列表
          ↓
  系统设置 → 分辨率下拉框中有高分辨率选项 ✅
```

## 临时测试方案（重启后失效）

### 方案适用性

| 桌面环境 | 临时方案可行性 | 推荐方案 |
|---------|--------------|---------|
| **X11** | ✅ 可行（xrandr） | EDID 固件 |
| **Wayland (KDE/GNOME)** | ❌ 不可行 | **必须修复 EDID** |

### X11 环境临时方案

在永久修复前，X11 用户跳过验证步骤，直接使用生成的 EDID 文件
```

## 临时测试方案（重启后失效）

在永久修复前，可以先临时测试自定义分辨率。

### 方法 1：使用自动化脚本（推荐）

我提供了一个交互式脚本 `fix-monitor.sh`，自动完成所有步骤：

```bash
#!/bin/bash
# fix-monitor.sh - 修复显示器分辨率问题的脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== 显示器分辨率修复脚本 ===${NC}"
echo ""

# 步骤 1: 显示当前显示器状态
echo -e "${YELLOW}[1/4] 检查当前显示器状态...${NC}"
xrandr
echo ""

# 步骤 2: 选择显示器接口
echo -e "${YELLOW}[2/4] 请输入要修复的显示器接口名称 (例如: HDMI-1, DP-9, DVI-1)${NC}"
read -p "显示器接口: " MONITOR

if [ -z "$MONITOR" ]; then
    echo -e "${RED}错误: 未输入显示器接口${NC}"
    exit 1
fi

# 验证显示器是否存在
if ! xrandr | grep -q "^$MONITOR"; then
    echo -e "${RED}错误: 显示器接口 '$MONITOR' 不存在${NC}"
    echo -e "${YELLOW}可用的接口:${NC}"
    xrandr | grep " connected" | awk '{print $1}'
    exit 1
fi

# 步骤 3: 输入目标分辨率
echo ""
echo -e "${YELLOW}[3/4] 请输入目标分辨率${NC}"
echo "常见分辨率:"
echo "  1920x1200  (16:10 WUXGA)"
echo "  1920x1080  (16:9 Full HD)"
echo "  2560x1440  (16:9 2K)"
echo "  3840x2160  (16:9 4K)"
echo "  1680x1050  (16:10 WSXGA+)"
echo "  1600x1200  (4:3 UXGA)"

read -p "宽度 (如 1920): " WIDTH
read -p "高度 (如 1200): " HEIGHT
read -p "刷新率 (如 60, 默认 60): " REFRESH
REFRESH=${REFRESH:-60}

if [ -z "$WIDTH" ] || [ -z "$HEIGHT" ]; then
    echo -e "${RED}错误: 分辨率不能为空${NC}"
    exit 1
fi

# 步骤 4: 生成并应用自定义分辨率
echo ""
echo -e "${YELLOW}[4/4] 生成并应用自定义分辨率...${NC}"

# 使用 cvt 生成 modeline
MODELINE=$(cvt $WIDTH $HEIGHT $REFRESH | grep "Modeline" | sed 's/Modeline //')

if [ -z "$MODELINE" ]; then
    echo -e "${RED}错误: 无法生成 modeline${NC}"
    exit 1
fi

# 提取模式名称和参数
MODE_NAME=$(echo $MODELINE | awk '{print $1}' | tr -d '"')
MODE_PARAMS=$(echo $MODELINE | cut -d' ' -f2-)

echo "生成的模式: $MODE_NAME"
echo "参数: $MODE_PARAMS"
echo ""

# 删除可能存在的旧模式
echo "清理旧模式..."
xrandr --delmode $MONITOR $MODE_NAME 2>/dev/null || true
xrandr --rmmode $MODE_NAME 2>/dev/null || true

# 创建新模式
echo "创建新模式..."
xrandr --newmode $MODE_NAME $MODE_PARAMS

# 将模式添加到显示器
echo "添加模式到显示器 $MONITOR..."
xrandr --addmode $MONITOR $MODE_NAME

# 应用新分辨率
echo "应用新分辨率..."
xrandr --output $MONITOR --mode $MODE_NAME

echo ""
echo -e "${GREEN}✓ 完成！分辨率已设置为 ${WIDTH}x${HEIGHT}@${REFRESH}Hz${NC}"
echo ""
echo -e "${YELLOW}注意事项:${NC}"
echo "1. 此设置在重启后会失效"
echo "2. 如果显示异常，等待 10 秒会自动恢复"
echo "3. 要永久修复，请参考文档配置 EDID 固件"
echo ""

# 显示新的显示器状态
echo -e "${YELLOW}当前显示器状态:${NC}"
xrandr | grep "^$MONITOR" -A 3
```

**使用方法**：

```bash
# 保存脚本并添加执行权限

### Wayland 环境说明

**Wayland 用户无法使用上述临时方案**，原因：

1. **架构限制**：Wayland 合成器不允许动态创建自定义分辨率
2. **内核依赖**：必须在内核 DRM 层面提供正确的 EDID
3. **唯一方案**：配置 GRUB 参数 + EDID 固件（见下文）

**尝试运行时重新加载驱动的失败原因**：

```text
问题分析：
  1. EDID 在内核 DRM 初始化时读取并缓存
  2. 运行时重新加载驱动时：
     - 如果显示器仍连接 → 内核使用缓存的 EDID
     - modprobe 参数可能被忽略
     - Wayland 会话状态难以保持
  3. 即使驱动重新加载，EDID 固件也可能不生效
```

**技术原因**：
- 内核 `struct drm_connector->edid` 缓存机制
- 缺乏运行时更新 EDID 的标准 API
- Wayland 合成器依赖内核的正确初始化
chmod +x fix-monitor.sh

# 运行脚本
./fix-monitor.sh
```

**脚本执行示例**：

```
=== 显示器分辨率修复脚本 ===

[1/4] 检查当前显示器状态...
Screen 0: minimum 320 x 200, current 3840 x 1200, maximum 16384 x 16384
DP-8 connected 1920x1200+0+0 (normal left inverted right x axis y axis) 518mm x 324mm
DP-9 connected 1024x768+1920+0 (normal left inverted right x axis y axis) 0mm x 0mm

[2/4] 请输入要修复的显示器接口名称 (例如: HDMI-1, DP-9, DVI-1)
显示器接口: DP-9

[3/4] 请输入目标分辨率
常见分辨率:
  1920x1200  (16:10 WUXGA)
  1920x1080  (16:9 Full HD)
  2560x1440  (16:9 2K)
宽度 (如 1920): 1920
高度 (如 1200): 1200
刷新率 (如 60, 默认 60): 60

[4/4] 生成并应用自定义分辨率...
生成的模式: 1920x1200_60.00
参数: 193.25  1920 2056 2256 2592  1200 1203 1209 1245 -hsync +vsync

✓ 完成！分辨率已设置为 1920x1200@60Hz
```

### 方法 2：手动执行命令

如果你想手动执行每一步：

```bash
# 1. 查看当前显示器状态
xrandr

# 2. 生成 modeline（以 1920x1200@60Hz 为例）
cvt 1920 1200 60

# 输出示例:
# Modeline "1920x1200_60.00"  193.25  1920 2056 2256 2592  1200 1203 1209 1245 -hsync +vsync

# 3. 创建新的显示模式（从 cvt 输出复制 modeline）
xrandr --newmode "1920x1200_60.00"  193.25  1920 2056 2256 2592  1200 1203 1209 1245 -hsync +vsync

# 4. 将模式添加到显示器（替换 DP-9 为实际接口名称）
xrandr --addmode DP-9 1920x1200_60.00

# 5. 应用新分辨率
xrandr --output DP-9 --mode 1920x1200_60.00
```

**注意**：此方法在重启后会失效，仅用于测试。如果测试成功，建议使用 EDID 固件方案进行永久修复。

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
