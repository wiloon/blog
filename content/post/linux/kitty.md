---
title: kitty
author: "-"
date: 2025-11-13T08:30:00+08:00
url: kitty
categories:
  - Linux
tags:
  - reprint
  - remix
  - AI-assisted
---
## kitty

kitty 是一个 GPU based terminal

https://sw.kovidgoyal.net/kitty/

## 快捷键

https://www.escapelife.site/posts/8e342b57.html

### 配置管理
- `Ctrl+Shift+F2` - 打开配置文件
- `Ctrl+Shift+F5` - 重新加载配置
- `Ctrl+Shift+F6` - 显示当前配置

### 窗口分割与管理
- `Ctrl+Shift+Enter` - 新建窗口（在当前窗口下方创建新窗口，水平分割）
- `Ctrl+Shift+W` - 关闭当前窗口
- `Ctrl+Shift+]` - 切换到下一个窗口
- `Ctrl+Shift+[` - 切换到上一个窗口
- `Ctrl+Shift+R` - 调整窗口大小模式
- `Ctrl+Shift+L` - 切换窗口布局（tall/fat/grid/horizontal/vertical/splits/stack）

### 标签页管理
- `Ctrl+Shift+T` - 新建标签
- `Ctrl+Shift+W` - 关闭标签（当只有一个窗口时）
- `Ctrl+Shift+Q` - 退出 kitty
- `Ctrl+Shift+Right` - 切换到下一个标签页
- `Ctrl+Shift+Left` - 切换到上一个标签页

## ubuntu install

```Bash
sudo apt update
sudo apt install kitty -y
kitty
```

## 配置文件

~/.config/kitty/kitty.conf

## 字体配置

### 安装推荐字体

```bash
# 安装 JetBrains Mono
sudo apt install fonts-jetbrains-mono
```

### 配置字体

编辑 `~/.config/kitty/kitty.conf`：

```conf
font_family      JetBrains Mono
bold_font        auto
italic_font      auto
bold_italic_font auto
font_size        12.0

# 禁用连字效果（如果不需要）
disable_ligatures always
```

## 主题配置

### 方式一：使用主题仓库（推荐）

**1. 克隆主题仓库**

```bash
git clone --depth 1 https://github.com/dexpota/kitty-themes.git ~/.config/kitty/kitty-themes
```

**2. 在配置文件中引用主题**

编辑 `~/.config/kitty/kitty.conf`，添加：

```conf
# 使用 Dracula 主题
include ./kitty-themes/themes/Dracula.conf
```

**3. 查看所有可用主题**

```bash
ls ~/.config/kitty/kitty-themes/themes/
```

**4. 切换主题**

只需修改 `include` 那一行，例如：

```conf
# Dracula 主题
include ./kitty-themes/themes/Dracula.conf

# Tokyo Night 主题
# include ./kitty-themes/themes/Tokyo_Night.conf
```

修改后按 `Ctrl+Shift+F5` 重新加载配置。

### 热门主题推荐

- **Dracula** - 深紫色背景，护眼，最流行的暗色主题
- **Tokyo Night** - 深蓝紫色调，柔和不刺眼
- **Nord** - 冷色调蓝灰背景，低对比度
- **Gruvbox** - 复古暖色调，舒适护眼
- **One Dark** - Atom 编辑器经典主题
- **Monokai Pro** - Sublime Text 经典配色
- **Catppuccin** - 柔和的粉彩色调
