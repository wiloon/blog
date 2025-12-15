#!/bin/bash
# setup-edid.sh - 自动配置 EDID 固件的脚本
# 会自动完成所有步骤，包括 GRUB 配置

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}=== EDID 固件自动配置脚本 ===${NC}"
echo ""

# 检查 root 权限
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}错误: 需要 root 权限运行此脚本${NC}"
    echo "请使用: sudo $0"
    exit 1
fi

# 步骤 1: 询问显示器信息
echo -e "${YELLOW}[1/6] 收集显示器信息${NC}"
echo ""
echo "请输入要修复的显示器信息:"
read -p "显示器接口名称 (如 DP-11): " MONITOR
read -p "目标分辨率宽度 (如 1920): " WIDTH
read -p "目标分辨率高度 (如 1200): " HEIGHT
read -p "刷新率 (默认 60): " REFRESH
REFRESH=${REFRESH:-60}

if [ -z "$MONITOR" ] || [ -z "$WIDTH" ] || [ -z "$HEIGHT" ]; then
    echo -e "${RED}错误: 必填信息不能为空${NC}"
    exit 1
fi

EDID_FILENAME="custom_${WIDTH}x${HEIGHT}.bin"

echo ""
echo "配置摘要:"
echo "  显示器: $MONITOR"
echo "  分辨率: ${WIDTH}x${HEIGHT}@${REFRESH}Hz"
echo "  EDID 文件: $EDID_FILENAME"
echo ""
read -p "确认继续? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "已取消"
    exit 0
fi

# 步骤 2: 创建 EDID 固件目录
echo ""
echo -e "${YELLOW}[2/6] 创建固件目录${NC}"
mkdir -p /lib/firmware/edid
echo -e "${GREEN}✓ 目录已创建: /lib/firmware/edid/${NC}"

# 步骤 3: 生成 EDID 文件
echo ""
echo -e "${YELLOW}[3/6] 生成 EDID 固件文件${NC}"

python3 << PYTHON_EOF
#!/usr/bin/env python3
import sys

# 配置参数
width = $WIDTH
height = $HEIGHT
refresh = $REFRESH

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
edid[16:18] = [12, 22]

# EDID version (18-19)
edid[18:20] = [1, 3]

# Video input definition (20)
edid[20] = 0x80  # Digital

# Screen size (21-22) - 估算基于分辨率
screen_width_cm = int(width * 0.027)
screen_height_cm = int(height * 0.027)
edid[21:23] = [screen_width_cm, screen_height_cm]

# Gamma (23)
edid[23] = 0x78  # 2.20

# Features (24)
edid[24] = 0xEE

# Color characteristics (25-34)
edid[25:35] = [0xEE, 0x95, 0xA3, 0x54, 0x4C, 0x99, 0x26, 0x0F, 0x50, 0x54]

# Established timings (35-37)
edid[35:38] = [0xA5, 0x4B, 0x00]

# Standard timings (38-53) - 设置主要分辨率
# 标准时序编码: (水平分辨率/8-31) | ((宽高比<<6) | (刷新率-60))
def encode_standard_timing(w, h, r):
    ar_map = {
        (16, 10): 0,
        (4, 3): 1,
        (5, 4): 2,
        (16, 9): 3
    }
    ratio = (16, 10) if h * 16 == w * 10 else (16, 9) if h * 16 == w * 9 else (4, 3)
    ar_code = ar_map.get(ratio, 0)
    return [(w // 8 - 31), ((ar_code << 6) | (r - 60))]

timing = encode_standard_timing(width, height, refresh)
edid[38:40] = timing
edid[40:54] = [0x01, 0x01] * 7

# Detailed timing descriptor 1 (54-71) - 主分辨率
# 这是一个简化的时序，实际应该用 cvt 计算
pixel_clock = int((width * height * refresh * 1.05) / 10000)  # 简化计算
edid[54:56] = [pixel_clock & 0xFF, (pixel_clock >> 8) & 0xFF]

h_active_low = width & 0xFF
h_blank = int(width * 0.25)
h_blank_low = h_blank & 0xFF
edid[56] = h_active_low
edid[57] = h_blank_low
edid[58] = ((width >> 8) & 0x0F) << 4 | ((h_blank >> 8) & 0x0F)

v_active_low = height & 0xFF
v_blank = int(height * 0.05)
v_blank_low = v_blank & 0xFF
edid[59] = v_active_low
edid[60] = v_blank_low
edid[61] = ((height >> 8) & 0x0F) << 4 | ((v_blank >> 8) & 0x0F)

# 其余时序参数
edid[62:72] = [0x30, 0x20, 0x36, 0x00, 0x06, 0x44, 0x21, 0x00, 0x00, 0x1A]

# Display product serial number (72-89)
edid[72:90] = [
    0x00, 0x00, 0x00, 0xFF, 0x00,
    ord('C'), ord('U'), ord('S'), ord('T'), ord('O'), ord('M'), ord('0'), ord('1'),
    0x0A, 0x20, 0x20, 0x20, 0x20
]

# Display product name (90-107)
name = f"{width}x{height}".ljust(13)[:13]
edid[90:108] = [
    0x00, 0x00, 0x00, 0xFC, 0x00,
] + [ord(c) for c in name] + [0x0A]

# Display range limits (108-125)
edid[108:126] = [
    0x00, 0x00, 0x00, 0xFD, 0x00,
    0x38, 0x4C, 0x1E, 0x53, 0x11, 0x00, 0x0A,
    0x20, 0x20, 0x20, 0x20, 0x20, 0x20
]

# Extension flag (126)
edid[126] = 0x00

# Calculate checksum (127)
checksum = (256 - (sum(edid[:127]) % 256)) % 256
edid[127] = checksum

# Write to file
with open('/lib/firmware/edid/$EDID_FILENAME', 'wb') as f:
    f.write(edid)

print(f"✓ EDID 文件已生成: {len(edid)} 字节")
print(f"  校验和: 0x{checksum:02x}")
print(f"  分辨率: {width}x{height}@{refresh}Hz")
PYTHON_EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ EDID 文件生成成功${NC}"
    ls -lh /lib/firmware/edid/$EDID_FILENAME
else
    echo -e "${RED}错误: EDID 文件生成失败${NC}"
    exit 1
fi

# 步骤 4: 备份 GRUB 配置
echo ""
echo -e "${YELLOW}[4/6] 备份 GRUB 配置${NC}"
BACKUP_FILE="/etc/default/grub.backup.$(date +%Y%m%d_%H%M%S)"
cp /etc/default/grub "$BACKUP_FILE"
echo -e "${GREEN}✓ 备份已创建: $BACKUP_FILE${NC}"

# 步骤 5: 修改 GRUB 配置
echo ""
echo -e "${YELLOW}[5/6] 修改 GRUB 配置${NC}"

# 检查是否已经配置过 EDID 固件
if grep -q "drm.edid_firmware=" /etc/default/grub; then
    echo -e "${YELLOW}检测到已有 EDID 固件配置${NC}"
    echo "当前配置:"
    grep "GRUB_CMDLINE_LINUX_DEFAULT" /etc/default/grub
    echo ""
    read -p "是否追加新的 EDID 配置? (y/n): " ADD_MORE
    if [ "$ADD_MORE" = "y" ]; then
        # 在现有配置后追加
        sed -i "s/drm.edid_firmware=\([^ \"]*\)/drm.edid_firmware=\1,$MONITOR:edid\/$EDID_FILENAME/" /etc/default/grub
    else
        echo "跳过 GRUB 修改"
    fi
else
    # 首次添加 EDID 配置
    sed -i "s/GRUB_CMDLINE_LINUX_DEFAULT=\"\(.*\)\"/GRUB_CMDLINE_LINUX_DEFAULT=\"\1 drm.edid_firmware=$MONITOR:edid\/$EDID_FILENAME\"/" /etc/default/grub
fi

echo ""
echo "修改后的配置:"
grep "GRUB_CMDLINE_LINUX_DEFAULT" /etc/default/grub
echo -e "${GREEN}✓ GRUB 配置已更新${NC}"

# 步骤 6: 更新 GRUB
echo ""
echo -e "${YELLOW}[6/6] 更新 GRUB${NC}"
grub-mkconfig -o /boot/grub/grub.cfg
echo -e "${GREEN}✓ GRUB 配置已重新生成${NC}"

# 完成
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ 配置完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "配置摘要:"
echo "  • EDID 文件: /lib/firmware/edid/$EDID_FILENAME"
echo "  • 显示器: $MONITOR"
echo "  • 分辨率: ${WIDTH}x${HEIGHT}@${REFRESH}Hz"
echo "  • GRUB 备份: $BACKUP_FILE"
echo ""
echo -e "${YELLOW}下一步:${NC}"
echo "  1. 检查配置是否正确:"
echo "     cat /proc/cmdline"
echo "  2. 重启系统:"
echo "     sudo reboot"
echo "  3. 重启后验证:"
echo "     sudo dmesg | grep -i edid"
echo ""
echo -e "${BLUE}如果需要恢复 GRUB 配置:${NC}"
echo "  sudo cp $BACKUP_FILE /etc/default/grub"
echo "  sudo grub-mkconfig -o /boot/grub/grub.cfg"
echo ""
