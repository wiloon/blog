#!/bin/bash
# fix-monitor.sh - 修复显示器分辨率问题的脚本 (Wayland 版本)
# 适用于 EDID 读取失败导致分辨率异常的情况
# 支持 KDE Wayland (kscreen-doctor) 和 wlroots 系 (wlr-randr)

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== 显示器分辨率修复脚本 (Wayland) ===${NC}"
echo ""

# 检测 Wayland 会话类型
echo -e "${YELLOW}检测显示服务器类型...${NC}"
SESSION_TYPE=$(loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}' | head -1) -p Type --value 2>/dev/null || echo "unknown")

if [ "$SESSION_TYPE" != "wayland" ]; then
    echo -e "${YELLOW}警告: 未检测到 Wayland 会话 (当前: $SESSION_TYPE)${NC}"
    echo "如果你在使用 X11，请使用 xrandr 版本的脚本"
    read -p "继续运行? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ]; then
        exit 0
    fi
fi

# 检测 Wayland 合成器
COMPOSITOR=""
if pgrep -x "kwin_wayland" > /dev/null; then
    COMPOSITOR="KDE"
    TOOL="kscreen-doctor"
elif pgrep -x "sway" > /dev/null; then
    COMPOSITOR="Sway"
    TOOL="wlr-randr"
elif pgrep -x "hyprland" > /dev/null; then
    COMPOSITOR="Hyprland"
    TOOL="wlr-randr"
elif pgrep -x "gnome-shell" > /dev/null; then
    COMPOSITOR="GNOME"
    TOOL="gnome-randr"
else
    COMPOSITOR="Unknown"
    TOOL="wlr-randr"
fi

echo -e "${GREEN}✓ 检测到: $COMPOSITOR Wayland${NC}"
echo -e "${BLUE}使用工具: $TOOL${NC}"
echo ""

# 检查依赖工具
echo -e "${YELLOW}检查依赖工具...${NC}"
MISSING_TOOL=false

if [ "$TOOL" = "kscreen-doctor" ]; then
    if ! command -v kscreen-doctor &> /dev/null; then
        echo -e "${RED}错误: 未找到 kscreen-doctor${NC}"
        echo "KDE Wayland 应该自带此工具，请检查安装"
        echo "  sudo pacman -S kscreen"
        MISSING_TOOL=true
    fi
elif [ "$TOOL" = "wlr-randr" ]; then
    if ! command -v wlr-randr &> /dev/null; then
        echo -e "${RED}错误: 未找到 wlr-randr${NC}"
        echo "请安装:"
        echo "  sudo pacman -S wlr-randr"
        MISSING_TOOL=true
    fi
elif [ "$TOOL" = "gnome-randr" ]; then
    if ! command -v gnome-randr &> /dev/null; then
        echo -e "${RED}错误: 未找到 gnome-randr${NC}"
        echo "请安装:"
        echo "  yay -S gnome-randr"
        MISSING_TOOL=true
    fi
fi

if [ "$MISSING_TOOL" = true ]; then
    exit 1
fi

echo -e "${GREEN}✓ 依赖检查通过${NC}"
echo ""

# 步骤 1: 显示当前显示器状态
echo -e "${YELLOW}[1/4] 检查当前显示器状态...${NC}"
echo ""

if [ "$TOOL" = "kscreen-doctor" ]; then
    kscreen-doctor -o
elif [ "$TOOL" = "wlr-randr" ]; then
    wlr-randr
elif [ "$TOOL" = "gnome-randr" ]; then
    gnome-randr
fi

echo ""

# 步骤 2: 选择显示器
echo -e "${YELLOW}[2/4] 请输入要修复的显示器名称${NC}"

if [ "$TOOL" = "kscreen-doctor" ]; then
    echo "输入格式示例: DP-9, HDMI-A-1, eDP-1"
    echo "提示: 从上面输出的 'Output:' 后复制完整名称（如 'Output: 2 DP-9 ...', 输入 'DP-9'）"
elif [ "$TOOL" = "wlr-randr" ]; then
    echo "输入格式示例: DP-9, HDMI-A-1"
fi

read -p "显示器名称: " MONITOR

if [ -z "$MONITOR" ]; then
    echo -e "${RED}错误: 未输入显示器名称${NC}"
    exit 1
fi

# 步骤 3: 获取可用分辨率或输入自定义分辨率
echo ""
echo -e "${YELLOW}[3/4] 选择分辨率${NC}"

if [ "$TOOL" = "kscreen-doctor" ]; then
    echo ""
    echo "该显示器支持的分辨率:"
    MODES_OUTPUT=$(kscreen-doctor -o | grep -A 50 "Output: .* $MONITOR" | grep "Modes:")
    echo "$MODES_OUTPUT"
    
    # 提取所有模式并格式化显示
    echo ""
    echo "可用模式列表:"
    echo "$MODES_OUTPUT" | sed 's/.*Modes: *//' | tr -d '  ' | sed 's/[0-9]*://g' | tr ' ' '\n' | grep -E '^[0-9]+x[0-9]+@' | sort -u | nl
    echo ""
    
    # 检测是否可能是 EDID 问题
    MAX_RES=$(echo "$MODES_OUTPUT" | grep -oE '[0-9]+x[0-9]+' | awk -F'x' '{print $1*$2, $0}' | sort -rn | head -1 | awk '{print $2}')
    MAX_WIDTH=$(echo $MAX_RES | cut -d'x' -f1)
    
    if [ "$MAX_WIDTH" -lt 1920 ]; then
        echo -e "${RED}⚠️  警告: EDID 读取可能失败！${NC}"
        echo -e "${YELLOW}检测到最大分辨率只有 $MAX_RES，这通常表示显示器 EDID 信息丢失。${NC}"
        echo ""
        echo "在 Wayland (KDE) 环境下的限制:"
        echo "  • Wayland 只能使用显示器报告的分辨率模式"
        echo "  • 不能像 X11 那样动态创建自定义分辨率"
        echo "  • 必须修复 EDID 问题才能获得正确的分辨率列表"
        echo ""
        echo -e "${GREEN}推荐解决方案:${NC}"
        echo "  1. 配置内核 EDID 固件（永久方案，参考文档）"
        echo "  2. 临时切换到 X11 会话使用 xrandr（临时方案）"
        echo ""
        read -p "是否继续尝试从现有模式中选择? (y/n): " CONTINUE
        if [ "$CONTINUE" != "y" ]; then
            echo ""
            echo -e "${BLUE}建议步骤:${NC}"
            echo "1. 按照文档配置 EDID 固件（/lib/firmware/edid/）"
            echo "2. 修改 GRUB 参数: drm.edid_firmware=DP-11:edid/your_monitor.bin"
            echo "3. 更新 GRUB 并重启"
            echo ""
            echo "详细文档: /home/wiloon/workspace/blog/content/post/linux/archlinux-monitor-edid-fix.md"
            exit 0
        fi
    fi
    
    echo ""
    read -p "输入完整模式 (从上面列表复制，如 1920x1200@60.00): " MODE
    if [ -z "$MODE" ]; then
        echo -e "${RED}错误: 模式不能为空${NC}"
        exit 1
    fi
    
    # 验证模式是否存在
    if ! echo "$MODES_OUTPUT" | grep -q "$MODE"; then
        echo -e "${RED}错误: 模式 '$MODE' 在该显示器的支持列表中不存在${NC}"
        echo -e "${YELLOW}请从上面的列表中选择一个可用的模式${NC}"
        exit 1
    fi
elif [ "$TOOL" = "wlr-randr" ]; then
    echo ""
    echo "常见分辨率:"
    echo "  1920x1200  (16:10 WUXGA)"
    echo "  1920x1080  (16:9 Full HD)"
    echo "  2560x1440  (16:9 2K)"
    echo "  3840x2160  (16:9 4K)"
    echo ""
    
    # 显示该显示器可用模式
    echo "该显示器支持的模式:"
    wlr-randr | grep -A 30 "^$MONITOR" | grep "px" | head -10
    echo ""
    
    read -p "输入模式 (如 1920x1200@60.000000Hz): " MODE
    if [ -z "$MODE" ]; then
        echo -e "${RED}错误: 模式不能为空${NC}"
        exit 1
    fi
fi

# 步骤 4: 应用分辨率
echo ""
echo -e "${YELLOW}[4/4] 应用新分辨率...${NC}"

if [ "$TOOL" = "kscreen-doctor" ]; then
    echo "执行命令: kscreen-doctor output.$MONITOR.mode.$MODE"
    kscreen-doctor output.$MONITOR.mode.$MODE
    
elif [ "$TOOL" = "wlr-randr" ]; then
    echo "执行命令: wlr-randr --output $MONITOR --mode $MODE"
    wlr-randr --output $MONITOR --mode $MODE
fi

echo ""
echo -e "${GREEN}✓ 完成！分辨率已设置${NC}"
echo ""
echo -e "${YELLOW}注意事项:${NC}"
echo "1. 此设置在重启后可能失效（取决于桌面环境配置）"
echo "2. 如果显示异常，系统可能会自动恢复"
echo "3. KDE 会自动保存显示配置到 ~/.local/share/kscreen/"
echo "4. 要永久修复，建议配置 EDID 固件（参考文档）"
echo ""

# 显示当前状态
echo -e "${YELLOW}当前显示器状态:${NC}"
if [ "$TOOL" = "kscreen-doctor" ]; then
    kscreen-doctor -o | grep -A 5 "$MONITOR"
elif [ "$TOOL" = "wlr-randr" ]; then
    wlr-randr | grep -A 10 "^$MONITOR"
fi
