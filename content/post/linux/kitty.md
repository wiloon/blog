---
title: kitty
author: "-"
date: 2025-11-15T14:30:00+08:00
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

## 安装 Kitty

```bash
# macOS
brew install kitty

# Linux (Debian/Ubuntu)
sudo apt update
sudo apt install kitty -y
kitty
```

### 2. 安装 JetBrains Mono 字体

推荐编程字体 JetBrains Mono：

```bash
brew install --cask font-jetbrains-mono
```

### 3. 配置 Kitty 使用 JetBrains Mono 字体

编辑配置文件 `~/.config/kitty/kitty.conf`，添加如下内容：

```conf
font_family      JetBrains Mono
bold_font        JetBrains Mono Bold
italic_font      JetBrains Mono Italic
bold_italic_font JetBrains Mono Bold Italic
font_size        14.0
disable_ligatures never
```

### 4. 安装主题（Tokyo Night 推荐）

```bash
git clone --depth 1 https://github.com/dexpota/kitty-themes.git ~/.config/kitty/kitty-themes
ln -sf ~/.config/kitty/kitty-themes/themes/Tokyo_Night.conf ~/.config/kitty/theme.conf
```

在 `kitty.conf` 末尾添加：

```conf
include ./theme.conf
```

### 5. 主流快捷键配置（macOS 优化）

```conf
# 复制粘贴
map cmd+c copy_to_clipboard
map cmd+v paste_from_clipboard
# 新建/关闭窗口
map cmd+n new_os_window
map cmd+w close_window
# 新建/关闭标签页
map cmd+t new_tab
map shift+cmd+w close_tab
# 垂直/水平分屏
map cmd+d launch --location=vsplit --cwd=current
map cmd+shift+d launch --location=hsplit --cwd=current
# 字体大小调整
map cmd+equal change_font_size all +1.0
map cmd+minus change_font_size all -1.0
map cmd+0 change_font_size all 0
# 其他快捷键详见配置文件
```

### 6. 重新加载配置

在 Kitty 中按 `Ctrl+Shift+F5` 或 `Cmd+Shift+R` 重新加载配置。

---

## 快捷键

### macOS 快捷键

```conf
# 复制粘贴
map cmd+c copy_to_clipboard
map cmd+v paste_from_clipboard
# 新建/关闭窗口
map cmd+n new_os_window
map cmd+w close_window
# 新建/关闭标签页
map cmd+t new_tab
map shift+cmd+w close_tab
# 垂直/水平分屏
map cmd+d launch --location=vsplit --cwd=current
map cmd+shift+d launch --location=hsplit --cwd=current
# 字体大小调整
map cmd+equal change_font_size all +1.0
map cmd+minus change_font_size all -1.0
map cmd+0 change_font_size all 0
# 其他快捷键详见配置文件
```

#### 配置管理
- `Cmd+,` - 编辑配置文件
- `Cmd+Shift+,` - 重新加载配置
- `Cmd+Shift+/` - 显示滚动历史
- `Cmd+Shift+F11` - 切换全屏

#### 窗口分割与管理
- `Cmd+Shift+Enter` - 新建窗口（在当前窗口下方创建新窗口，水平分割）
- `Cmd+Shift+W` - 关闭当前窗口
- `Cmd+]` / `Cmd+[` - 切换窗口
- `Cmd+Shift+]` / `Cmd+Shift+[` - 移动窗口
- `Cmd+Shift+R` - 重新加载配置

#### 标签页管理
- `Cmd+T` - 新建标签
- `Shift+Cmd+W` - 关闭标签
- `Cmd+1~9` - 切换到指定标签页
- `Ctrl+Tab` / `Ctrl+Shift+Tab` - 切换标签页

---

### Linux 快捷键

#### 配置管理
- `Ctrl+Shift+F2` - 打开配置文件
- `Ctrl+Shift+F5` - 重新加载配置
- `Ctrl+Shift+F6` - 显示当前配置

#### 窗口分割与管理
- `Ctrl+Shift+Enter` - 新建窗口（在当前窗口下方创建新窗口，水平分割）
- `Ctrl+Shift+W` - 关闭当前窗口
- `Ctrl+Shift+]` - 切换到下一个窗口
- `Ctrl+Shift+[` - 切换到上一个窗口
- `Ctrl+Shift+R` - 调整窗口大小模式
- `Ctrl+Shift+L` - 切换窗口布局（tall/fat/grid/horizontal/vertical/splits/stack）

#### 标签页管理
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

## macOS Terminal vs Kitty 对比

### 性能

**macOS Terminal**

- 传统的 CPU 渲染方式
- 大量文本输出时可能出现卡顿
- 滚动性能一般

**Kitty**

- GPU 加速渲染 (基于 OpenGL)
- 处理大量文本输出时性能优异
- 滚动流畅，延迟低
- 特别适合日志查看、编译输出等场景

### 功能特性

**macOS Terminal**

- 基础功能完善
- 与 macOS 系统深度集成
- 支持标签页、分屏
- 有限的自定义选项
- 不支持图片显示
- 不支持多窗口平铺

**Kitty**

- 丰富的配置选项
- 内置窗口管理器 (支持平铺布局)
- 支持图片显示 (icat)
- 支持 ligature (连字)
- Unicode 支持更好
- 可扩展的 kitten 系统
- 支持远程控制
- 支持会话管理

### 外观定制

**macOS Terminal**

- 预设主题有限
- 颜色、字体配置通过图形界面
- 自定义选项较少

**Kitty**

- 完全可定制的配置文件
- 丰富的主题生态
- 支持字体后备 (font fallback)
- 支持半透明、模糊背景
- 更精细的颜色控制

### 兼容性

**macOS Terminal**

- macOS 原生应用
- 与系统完美集成
- 支持所有 macOS 特性
- Spotlight 搜索集成

**Kitty**

- 跨平台 (Linux, macOS, BSD)
- 需要额外安装
- 部分 macOS 特性不支持
- 配置可跨平台共享

### 资源占用

**macOS Terminal**

- 内存占用较低
- CPU 使用适中
- 不依赖 GPU

**Kitty**

- 需要 GPU 支持
- 内存占用稍高
- 对现代硬件更友好
- 通过 GPU 加速降低 CPU 负载

### 快捷键与操作

**macOS Terminal**

- 遵循 macOS 标准快捷键
- Cmd+T 新标签页
- Cmd+D 分屏
- 有限的自定义

**Kitty**

- 完全可自定义快捷键
- 默认使用 Ctrl+Shift 组合
- 支持复杂的键盘映射
- 窗口管理快捷键丰富

### 适用场景

**选择 macOS Terminal 如果你：**

- 只需要基础终端功能
- 喜欢系统原生体验
- 不需要高性能要求
- 追求简单易用

**选择 Kitty 如果你：**

- 需要处理大量文本输出
- 追求极致性能和流畅度
- 需要高度自定义
- 使用多平台，希望配置统一
- 需要高级功能 (图片显示、窗口平铺等)
- 喜欢折腾配置文件

### 总结

macOS Terminal 是一个稳定可靠的终端，适合日常使用和系统集成场景。Kitty 则是面向高级用户和性能追求者的现代化终端模拟器，通过 GPU 加速提供更好的性能和更丰富的功能。

如果你对终端性能和可定制性有较高要求，Kitty 是更好的选择；如果你只需要一个简单好用的终端，macOS 原生 Terminal 完全够用。

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
