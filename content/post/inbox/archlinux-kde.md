---
title: archlinux kde, config
author: "-"
date: 2025-12-03T18:30:00+08:00
url: kde
categories:
  - Linux
tags:
  - inbox
  - KDE
  - remix
  - AI-assisted
---
## 删除和重新安装 KDE

### 删除 KDE

```bash
# 连接到远程主机
ssh root@192.168.50.19

# 1. 停止并禁用 SDDM 显示管理器
systemctl stop sddm
systemctl disable sddm

# 2. 查看已安装的 KDE 相关包
pacman -Qq | grep -E 'plasma|kde'

# 3. 删除 KDE Plasma 桌面环境及相关包
# 删除 plasma 元包和所有依赖
sudo pacman -Rns plasma-desktop plasma-wayland-session

# 删除其他 KDE 应用（根据需要）
sudo pacman -Rns konsole dolphin kate kwalletmanager

# 删除 KDE 主题和附加组件
sudo pacman -Rns breeze-gtk breeze kde-gtk-config kdeplasma-addons

# 删除 SDDM（如果不再需要）
sudo pacman -Rns sddm

# 4. 清理孤立的依赖包
sudo pacman -Rns $(pacman -Qtdq)

# 5. 清理配置文件（可选）
# 删除系统级配置
rm -rf /etc/sddm.conf.d/
rm -rf /usr/share/sddm/

# 删除用户配置（谨慎操作，会删除个人设置）
rm -rf ~/.config/plasma*
rm -rf ~/.config/kde*
rm -rf ~/.local/share/plasma*
rm -rf ~/.local/share/kwalletd/
rm -rf ~/.kde4/

# 6. 清理缓存
rm -rf ~/.cache/plasma*
rm -rf ~/.cache/kde*
```

### 重新安装 KDE

```bash
# 1. 更新系统
sudo pacman -Syu

# 2. 安装 KDE Plasma 桌面（基础版本）
sudo pacman -S plasma-desktop

# 如果需要完整的 KDE Plasma 环境，可以安装：
# sudo pacman -S plasma

# 3. 安装常用的 KDE 应用
sudo pacman -S konsole dolphin kate

# 4. 安装 SDDM 显示管理器
sudo pacman -S sddm

# 5. 启用 SDDM
systemctl enable sddm
systemctl start sddm

# 6. 安装 Wayland 支持（可选）
sudo pacman -S plasma-wayland-session

# 7. 安装 GTK 主题支持（可选）
sudo pacman -S breeze-gtk breeze kde-gtk-config

# 8. 安装 KDE 附加组件（可选）
sudo pacman -S kdeplasma-addons

# 9. 安装钱包管理器（可选）
sudo pacman -S kwalletmanager

# 10. 重启系统
reboot
```

### 选择性安装 - X11 或 Wayland

#### 纯 Wayland 会话（推荐）

如果只想使用 Wayland 模式，仍需安装少量 X11 组件以支持 XWayland 兼容层：

```bash
# 安装 Wayland 会话支持
sudo pacman -S plasma-wayland-session

# 安装 XWayland 及必要组件（用于运行传统 X11 应用）
sudo pacman -S xorg-xwayland xorg-xrdb xorg-xlsclients

# 从命令行启动（测试用）
/usr/lib/plasma-dbus-run-session-if-needed /usr/bin/startplasma-wayland

# 登录时在 SDDM 选择 "Plasma (Wayland)" 会话
```

**说明**：
- `xorg-xwayland` - XWayland 服务器，让 Wayland 会话能运行传统 X11 应用
- `xorg-xrdb` - X 资源数据库工具
- `xorg-xlsclients` - 列出 X 客户端的工具
- **不需要**安装完整的 `xorg` 或 `xorg-server` 包

### 注意事项

1. **备份重要数据**：删除前建议备份 `~/.config` 和 `~/.local/share` 中的重要配置
2. **孤立包清理**：使用 `pacman -Qtdq` 前确认要删除的包，避免误删
3. **Wayland 推荐**：使用 Wayland 会话可获得更好的性能和现代化体验
4. **XWayland 必需**：即使是纯 Wayland 环境也需要 XWayland 组件来运行传统应用
5. **重启建议**：完成安装后重启系统以确保所有服务正常启动

## archlinux kde, config

```bash
# 虽然启动的是 Wayland 会话，KDE Plasma（以及大多数现代 Linux 桌面）仍会启用一层叫做 XWayland 的兼容层：
sudo pacman -S xorg-xrdb xorg-xlsclients

sudo pacman -S plasma-desktop
sudo pacman -S konsole dolphin kate

# start kde from CLI
/usr/lib/plasma-dbus-run-session-if-needed /usr/bin/startplasma-wayland
sudo pacman -S sddm
systemctl enable sddm
```

---------

```bash
sudo pacman -S xorg xorg-xinit
sudo pacman -S plasma-desktop
echo "exec startplasma-x11" > ~/.xinitrc

sudo pacman -S konsole dolphin kate
startx
sudo pacman -S sddm
sudo pacman -S breeze-gtk breeze kde-gtk-config
sudo pacman -S kdeplasma-addons

sudo pacman -S kwalletmanager
# start kwalletmanager and disactive kwallet
```

### 登录后启动kde

```bash
vim /home/wiloon/.zshrc
if [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  exec startx
fi
```

[https://wiki.archlinux.org/index.php/Xinit#Autostart_X_at_login][1]{.wp-editor-md-post-content-link}

sddm
  
[https://wiki.archlinux.org/index.php/Display_manager#Loading_the_display_manager](https://wiki.archlinux.org/index.php/Display_manager#Loading_the_display_manager)

 [1]: https://wiki.archlinux.org/index.php/Xinit#Autostart_X_at_login "https://wiki.archlinux.org/index.php/Xinit#Autostart_X_at_login"

### 锁屏界面的日期时间格式

[https://chubuntu.com/questions/28565/how-to-display-kde-lock-screen-time-in-24-hour-format.html](https://chubuntu.com/questions/28565/how-to-display-kde-lock-screen-time-in-24-hour-format.html)

```bash
vim  /usr/share/plasma/look-and-feel/org.kde.breeze.desktop/contents/components/Clock.qml
找到这一行: 

text: Qt.formatTime(timeSource.data["Local"]["DateTime"])
并将其更改为

text: Qt.formatTime(timeSource.data["Local"]["DateTime"], "hh:mm:ss")
对于ISO日期更改,请找到以下行: 

text: Qt.formatDate(timeSource.data["Local"]["DateTime"], Qt.DefaultLocaleLongDate);
并将其更改为

text: Qt.formatDate(timeSource.data["Local"]["DateTime"], "yyyy-MM-dd");
保存更改。

按Ctrl + Alt + L锁定屏幕并立即查看更改。
```

### kde 配置

#### 多显示器

 Right-click on the background of the second screen -> Add Panel -> Empty Panel
 add widgets: task manager

## Arch Linux, KDE, Wayland

```bash
pacman -S plasma-desktop plasma-wayland-session
dbus-run-session startplasma-wayland
```

## wayland rdp

```bash
pacman -S weston freerdp
weston --backend=rdp-backend.so --port=3389

```

## 编译 Weston

```bash
git clone git@gitlab.freedesktop.org:wayland/weston.git
pacman -S wayland-protocols cmake seatd
meson build/ --prefix=/root/tmp/foo
# Failed to load module: libicuuc.so.70, 等 weston 升版本
```

[https://man.archlinux.org/man/weston.1](https://man.archlinux.org/man/weston.1)

[https://gitlab.freedesktop.org/wayland/weston](https://gitlab.freedesktop.org/wayland/weston)
