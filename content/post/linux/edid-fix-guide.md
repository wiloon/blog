# EDID 修复操作指南

## 当前状态（2025-12-31）

### ✅ 已完成的工作

1. **EDID 固件文件已准备好**
   - 位置：`/lib/firmware/edid/dell_u2412m.bin`
   - 大小：128 字节（标准大小）
   - 最后修改：2025-12-04

2. **确认了问题**
   ```bash
   # 内核日志显示 EDID 读取失败：
   [    4.253335] EDID block 0 is all zeroes
   [    4.253340] [drm:link_add_remote_sink [amdgpu]] *ERROR* Bad EDID, status3!
   ```

3. **确认了系统配置**
   - 双系统：Ubuntu + Arch Linux
   - Arch Linux 分区：`/dev/nvme0n1p4`
   - GRUB 由 Ubuntu 管理

### ❌ 尚未完成的工作

**内核参数未配置**
```bash
# 当前内核参数（缺少 drm.edid_firmware）：
BOOT_IMAGE=/boot/vmlinuz-linux root=/dev/nvme0n1p4
```

## 🚨 必须执行的操作

### 方案 A：在 Ubuntu 中修改 GRUB 配置（推荐）

根据文档"问题 3：双系统环境下修改 ArchLinux 启动参数"，需要：

1. **重启进入 Ubuntu 系统**

2. **确保 Ubuntu 也有 EDID 固件文件**
   ```bash
   # 在 Ubuntu 中执行：
   sudo mkdir -p /lib/firmware/edid
   
   # 从某处获取 dell_u2412m.bin 文件，或重新生成
   # （可以从 Arch 分区复制）
   sudo mount /dev/nvme0n1p4 /mnt
   sudo cp /mnt/lib/firmware/edid/dell_u2412m.bin /lib/firmware/edid/
   sudo umount /mnt
   ```

3. **修改 Ubuntu 的 GRUB 配置**
   ```bash
   # 在 Ubuntu 中执行：
   sudo cp /etc/default/grub /etc/default/grub.backup.$(date +%Y%m%d)
   
   sudo vim /etc/default/grub
   
   # 找到这一行（Ubuntu 默认）：
   # GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
   #
   # 修改为：
   # GRUB_CMDLINE_LINUX_DEFAULT="quiet splash drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin,DP-11:edid/dell_u2412m.bin,DP-12:edid/dell_u2412m.bin"
   ```

4. **更新 Ubuntu 的 GRUB**
   ```bash
   # 在 Ubuntu 中执行：
   sudo update-grub
   sudo update-initramfs -u -k all
   ```

5. **重启并验证**
   ```bash
   # 重启进入 Arch Linux
   sudo reboot
   
   # 在 Arch Linux 中验证：
   cat /proc/cmdline | grep edid_firmware
   sudo dmesg | grep -i edid
   ```

### 方案 B：直接编辑 Ubuntu 的 grub.cfg（不推荐，仅供参考）

**警告：此方法在 Ubuntu 下次 `update-grub` 时会被覆盖！**

```bash
# 在 Ubuntu 中执行：
sudo cp /boot/grub/grub.cfg /boot/grub/grub.cfg.backup.$(date +%Y%m%d)
sudo vim /boot/grub/grub.cfg

# 找到类似这样的 Arch Linux 启动项：
# menuentry 'Arch Linux (on /dev/nvme0n1p4)' ... {
#     ...
#     linux /boot/vmlinuz-linux root=/dev/nvme0n1p4
#     initrd /boot/initramfs-linux.img
# }
#
# 修改 linux 行，在末尾添加参数：
# linux /boot/vmlinuz-linux root=/dev/nvme0n1p4 drm.edid_firmware=DP-8:edid/dell_u2412m.bin,DP-9:edid/dell_u2412m.bin,DP-10:edid/dell_u2412m.bin
```

## 📋 需要确定的信息

### 显示器接口编号

由于 DisplayPort 接口编号可能变化，文档建议配置多个接口（DP-8 到 DP-12）。

你可以在下次启动时查看具体是哪个接口：
```bash
# 方法 1：如果是 X11
xrandr | grep "connected"

# 方法 2：检查内核日志
sudo dmesg | grep -i "drm\|edid" | grep -i "dp-"

# 方法 3：查看 sysfs
ls /sys/class/drm/
```

## 🔧 故障排除

### 如果配置后仍有问题

1. **检查内核参数是否生效**
   ```bash
   cat /proc/cmdline
   # 应该包含：drm.edid_firmware=...
   ```

2. **检查内核日志**
   ```bash
   sudo dmesg | grep -i edid
   # 应该看到类似：
   # [drm] Using EDID firmware for DP-9
   ```

3. **检查 EDID 文件**
   ```bash
   stat /lib/firmware/edid/dell_u2412m.bin
   # 大小应该是 128 或 256 字节
   ```

## � EDID 固件数据备份

### 十六进制数据

如果需要重新生成 EDID 固件文件，可以使用以下十六进制数据：

```hex
00 ff ff ff ff ff ff 00 10 ac 71 a0 4c 37 30 41
0c 16 01 03 80 34 20 78 ee ee 95 a3 54 4c 99 26
0f 50 54 a5 4b 00 d1 c0 a9 40 81 80 71 4f 01 01
01 01 01 01 01 01 28 3c 80 a0 70 b0 23 40 30 20
36 00 06 44 21 00 00 1a 00 00 00 ff 00 44 45 4c
4c 30 30 30 31 0a 20 20 20 20 00 00 00 fc 00 44
45 4c 4c 20 55 32 34 31 32 4d 0a 20 00 00 00 fd
00 38 4c 1e 53 11 00 0a 20 20 20 20 20 20 00 5e
```

### 生成 EDID 固件文件的方法

```bash
# 方法 1：从十六进制文本创建二进制文件
echo "00 ff ff ff ff ff ff 00 10 ac 71 a0 4c 37 30 41 \
0c 16 01 03 80 34 20 78 ee ee 95 a3 54 4c 99 26 \
0f 50 54 a5 4b 00 d1 c0 a9 40 81 80 71 4f 01 01 \
01 01 01 01 01 01 28 3c 80 a0 70 b0 23 40 30 20 \
36 00 06 44 21 00 00 1a 00 00 00 ff 00 44 45 4c \
4c 30 30 30 31 0a 20 20 20 20 00 00 00 fc 00 44 \
45 4c 4c 20 55 32 34 31 32 4d 0a 20 00 00 00 fd \
00 38 4c 1e 53 11 00 0a 20 20 20 20 20 20 00 5e" | \
xxd -r -p > dell_u2412m.bin

# 方法 2：如果有现有的 EDID 文件，可以从 Ubuntu 复制
sudo cp /lib/firmware/edid/dell_u2412m.bin /目标路径/
```

### EDID 解码信息（Dell U2412M）

```
Block 0, Base EDID:
  EDID Structure Version & Revision: 1.3
  Vendor & Product Identification:
    Manufacturer: DEL
    Model: 41073
    Serial Number: 1093678924
    Made in: week 12 of 2012
  Basic Display Parameters & Features:
    Digital display
    Maximum image size: 52 cm x 32 cm
    Gamma: 2.20
    DPMS levels: Standby Suspend Off
    RGB color display
    Default (sRGB) color space is primary color space
    First detailed timing is the preferred timing
  Color Characteristics:
    Red  : 0.6396, 0.3300
    Green: 0.2998, 0.5996
    Blue : 0.1503, 0.0595
    White: 0.3134, 0.3291
  Established Timings I & II:
    IBM     :   720x400    70.081663 Hz   9:5     31.467 kHz     28.320000 MHz
    DMT 0x04:   640x480    59.940476 Hz   4:3     31.469 kHz     25.175000 MHz
    DMT 0x06:   640x480    75.000000 Hz   4:3     37.500 kHz     31.500000 MHz
    DMT 0x09:   800x600    60.316541 Hz   4:3     37.879 kHz     40.000000 MHz
    DMT 0x0b:   800x600    75.000000 Hz   4:3     46.875 kHz     49.500000 MHz
    DMT 0x10:  1024x768    60.003840 Hz   4:3     48.363 kHz     65.000000 MHz
    DMT 0x12:  1024x768    75.028582 Hz   4:3     60.023 kHz     78.750000 MHz
    DMT 0x24:  1280x1024   75.024675 Hz   5:4     79.976 kHz    135.000000 MHz
  Standard Timings:
    DMT 0x52:  1920x1080   60.000000 Hz  16:9     67.500 kHz    148.500000 MHz
    DMT 0x33:  1600x1200   60.000000 Hz   4:3     75.000 kHz    162.000000 MHz
    DMT 0x23:  1280x1024   60.019740 Hz   5:4     63.981 kHz    108.000000 MHz
    DMT 0x15:  1152x864    75.000000 Hz   4:3     67.500 kHz    108.000000 MHz
  Detailed Timing Descriptors:
    DTD 1:  1920x1200   59.950171 Hz   8:5     74.038 kHz    154.000000 MHz (518 mm x 324 mm)
                 Hfront   48 Hsync  32 Hback   80 Hpol P
                 Vfront    3 Vsync   6 Vback   26 Vpol N
    Display Product Serial Number: 'DELL0001'
    Display Product Name: 'DELL U2412M'
    Display Range Limits:
      Monitor ranges (GTF): 56-76 Hz V, 30-83 kHz H, max dotclock 170 MHz
Checksum: 0x5e

关键信息：
- 显示器型号：DELL U2412M
- 原生分辨率：1920x1200 @ 60Hz
- 屏幕尺寸：518mm x 324mm (24 英寸)
- 文件大小：128 字节（标准 EDID Block 0）
```

## �📚 参考文档

详细说明请参考：
- `/home/wiloon/workspace/blog/content/post/linux/archlinux-monitor-edid-fix.md`
- 特别是"问题 3：双系统环境下修改 ArchLinux 启动参数"部分

## 📝 操作记录

- 2025-12-04：创建 EDID 固件文件 `/lib/firmware/edid/dell_u2412m.bin`
- 2025-12-31：确认问题，准备操作指南
- 2025-12-31：在 Ubuntu 中修改 GRUB 配置，添加内核参数
  - 备份 GRUB 配置：`/boot/grub/grub.cfg.backup.*`
  - 为 Arch Linux 启动项添加 `drm.edid_firmware` 参数
  - 发现实际 DisplayPort 接口为 DP-1 到 DP-9（当前配置为 DP-9 到 DP-12）
  - 添加 EDID 十六进制数据到文档作为备份参考
- 待完成：重启进入 Arch Linux 测试
