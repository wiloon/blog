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

## 📚 参考文档

详细说明请参考：
- `/home/wiloon/workspace/blog/content/post/linux/archlinux-monitor-edid-fix.md`
- 特别是"问题 3：双系统环境下修改 ArchLinux 启动参数"部分

## 📝 操作记录

- 2025-12-31：确认问题，准备操作指南
- 待完成：在 Ubuntu 中修改 GRUB 配置
