---
title: kitty
author: "-"
date: 2025-11-24T20:00:00+08:00
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

## 清空控制台历史输出

### 方法一：使用 clear 命令（推荐）

```bash
clear
# 或
Ctrl+L  # 快捷键，清空当前屏幕显示
```

**注意**：`clear` 或 `Ctrl+L` 只是清空当前屏幕显示，**不会删除滚动缓冲区**的历史内容，按 `Ctrl+Shift+H` 仍能看到之前的输出。

### 方法二：完全清空包括滚动缓冲区

```bash
# 清空屏幕并清除滚动缓冲区
printf '\033[2J\033[3J\033[1;1H'

# 或使用 Kitty 专用命令
clear && printf '\033[2J'
```

### 方法三：使用 Kitty 远程控制（最彻底）

```bash
# 清空当前窗口的滚动缓冲区
kitty @ scroll-window reset

# 如果需要在配置文件中设置快捷键
# 在 ~/.config/kitty/kitty.conf 中添加：
# map ctrl+shift+k scroll_end
# map ctrl+shift+delete clear_terminal reset active
```

### 快捷键配置（推荐）

在 `~/.config/kitty/kitty.conf` 中添加：

```conf
# Linux
map ctrl+shift+delete clear_terminal reset active

# macOS
map cmd+k clear_terminal reset active
```

配置后：
- **Linux**: `Ctrl+Shift+Delete` - 完全清空终端和滚动缓冲区
- **macOS**: `Cmd+K` - 完全清空终端和滚动缓冲区

### 三种清空方式对比

| 方式 | 命令/快捷键 | 清空屏幕 | 清空滚动缓冲区 |
|------|------------|---------|---------------|
| 标准 clear | `clear` 或 `Ctrl+L` | ✅ | ❌ |
| 完全清空 | `printf '\033[2J\033[3J\033[1;1H'` | ✅ | ✅ |
| Kitty 快捷键 | `Ctrl+Shift+Delete` (需配置) | ✅ | ✅ |

## 滚动查看历史输出

Kitty 没有滚动条，但可以用快捷键或鼠标滚动查看历史输出：

### 快速跳转到顶部/底部

**Linux 快捷键：**
- `Ctrl+Shift+Home` - 跳转到滚动缓冲区的**第一行**（最早的输出）
- `Ctrl+Shift+End` - 跳转到滚动缓冲区的**最后一行**（最新的输出）
- `Ctrl+Shift+H` - 进入 history 浏览模式，然后按 `g` 跳到顶部，按 `G` 跳到底部

**macOS 快捷键：**
- `Cmd+Home` - 跳转到滚动缓冲区的第一行
- `Cmd+End` - 跳转到滚动缓冲区的最后一行

### 滚动浏览

**鼠标操作：**
- 鼠标滚轮上下滚动
- `Shift+鼠标滚轮` - 加速滚动

**键盘操作（Linux）：**
- `Ctrl+Shift+Up` - 向上滚动一行
- `Ctrl+Shift+Down` - 向下滚动一行
- `Ctrl+Shift+Page Up` - 向上翻页
- `Ctrl+Shift+Page Down` - 向下翻页

**键盘操作（macOS）：**
- `Cmd+Up` - 向上滚动
- `Cmd+Down` - 向下滚动
- `Cmd+Page Up` - 向上翻页
- `Cmd+Page Down` - 向下翻页

### History 浏览模式（推荐）

进入 history 模式可以像 Vim 一样浏览：

1. 按 `Ctrl+Shift+H` 进入浏览模式
2. 使用 Vim 风格的快捷键：
   - `g` - 跳转到第一行（顶部）
   - `G` - 跳转到最后一行（底部）
   - `j`/`k` - 逐行上下移动
   - `Ctrl+F` / `Ctrl+B` - 向前/向后翻页
   - `d`/`u` - 向下/向上翻半页
3. 按 `q` 或 `Esc` 退出浏览模式

**最快方式：`Ctrl+Shift+H` 然后按 `g` 直接跳到第一行！**

## 搜索终端文字

在 Kitty 中可以搜索终端显示的文字内容（包括滚动缓冲区）：

### macOS 快捷键

- `Cmd+F` - 打开搜索栏
- `Cmd+G` - 查找下一个匹配
- `Cmd+Shift+G` - 查找上一个匹配
- `Esc` - 关闭搜索栏

### Linux 快捷键

- `Ctrl+Shift+H` - 打开 scrollback history 浏览模式（使用 less/vim 风格）
- `Esc` 或 `q` - 退出 history 浏览模式

**History 浏览模式说明**：

`Ctrl+Shift+H` 会打开**滚动历史浏览模式**，这是一个类似 `less` 的全屏浏览器：

- 窗口标题显示 "history"
- 使用 **Vim/less 风格的操作**：
  - `/` - 输入搜索关键词（会在底部显示冒号 `:` 或 `/`）
  - `n` - 跳转到下一个匹配
  - `N` - 跳转到上一个匹配
  - `j`/`k` - 上下滚动
  - `g`/`G` - 跳转到开头/结尾
  - `q` 或 `Esc` - 退出浏览模式
- 这个模式用于浏览和搜索终端的历史输出
- 搜索时输入的文字会在底部冒号后显示

**这就是 Kitty 的搜索功能！**

Kitty 默认使用 Vim/less 风格的搜索，没有图形化搜索框。如果你习惯了这种方式，这就是最直接的搜索方法。

**想要更好的搜索体验？使用 fzf**：

如果想要交互式的模糊搜索界面，可以配置 fzf：

```conf
# 在 ~/.config/kitty/kitty.conf 中添加
# 使用 Ctrl+Shift+F 打开 fzf 模糊搜索（需要先安装 fzf）
map ctrl+shift+f launch --type=overlay --stdin-source=@screen_scrollback fzf --no-sort --no-mouse --exact -i --tac
```

### 搜索功能特性

- 支持正则表达式搜索
- 实时高亮所有匹配项
- 支持大小写敏感/不敏感切换
- 可搜索滚动缓冲区中的历史内容
- 搜索时会自动滚动到匹配位置

### 配置搜索相关快捷键

可以在 `~/.config/kitty/kitty.conf` 中自定义搜索快捷键：

```conf
# macOS
map cmd+f launch --type=overlay --stdin-source=@screen_scrollback /bin/sh -c 'fzf --no-sort --no-mouse --exact -i'

# Linux
map ctrl+shift+f launch --type=overlay --stdin-source=@screen_scrollback /bin/sh -c 'fzf --no-sort --no-mouse --exact -i'
```

### 配合 fzf 使用（高级）

如果安装了 `fzf`，可以实现更强大的搜索功能：

```bash
# 安装 fzf
# macOS
brew install fzf

# Linux
sudo apt install fzf
```

配置使用 fzf 搜索滚动缓冲区：

```conf
# 使用 fzf 搜索滚动缓冲区
map ctrl+shift+f launch --type=overlay --stdin-source=@screen_scrollback fzf --no-sort --no-mouse --exact -i --tac
```

这样可以实现模糊搜索、多选、预览等高级功能。

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

### 窗口位置调整

窗口移动功能需要在配置文件中手动配置。编辑 `~/.config/kitty/kitty.conf` 添加：

```conf
# 移动窗口位置
map ctrl+shift+up move_window up
map ctrl+shift+down move_window down
map ctrl+shift+left move_window left
map ctrl+shift+right move_window right

# 修改标签页切换快捷键（避免与窗口移动冲突）
map ctrl+shift+page_up previous_tab
map ctrl+shift+page_down next_tab
```

配置后按 `Ctrl+Shift+F5` 重新加载配置，然后就可以使用：
- `Ctrl+Shift+Up` - 将当前窗口向上移动
- `Ctrl+Shift+Down` - 将当前窗口向下移动  
- `Ctrl+Shift+Left` - 将当前窗口向左移动
- `Ctrl+Shift+Right` - 将当前窗口向右移动

### 标签页管理
- `Ctrl+Shift+T` - 新建标签
- `Ctrl+Shift+W` - 关闭标签（当只有一个窗口时）
- `Ctrl+Shift+Q` - 退出 kitty
- `Ctrl+Shift+PageDown` - 切换到下一个标签页（避免与窗口移动冲突）
- `Ctrl+Shift+PageUp` - 切换到上一个标签页（避免与窗口移动冲突）

## ubuntu install

```Bash
sudo apt update
sudo apt install kitty -y
kitty
```

## 配置文件

~/.config/kitty/kitty.conf

### 配置滚动缓冲区大小

控制 Kitty 保存的历史输出行数，在 `~/.config/kitty/kitty.conf` 中配置：

```conf
# 设置滚动缓冲区行数（默认值：10000）
scrollback_lines 10000

# 常用配置示例：
# scrollback_lines 20000   # 保存 2 万行
# scrollback_lines 50000   # 保存 5 万行
# scrollback_lines 100000  # 保存 10 万行
# scrollback_lines 0       # 禁用滚动缓冲区（不推荐）
# scrollback_lines -1      # 无限制（慎用，可能占用大量内存）
```

**配置说明：**

- **默认值**：10000 行（约 10MB 内存）
- **推荐值**：10000-50000 行（适合日常使用）
- **大值影响**：设置过大会占用更多内存
- **特殊值**：
  - `0` - 禁用历史记录（不推荐）
  - `-1` - 无限制（会持续占用内存，慎用）

**生效方式：**

配置后按 `Ctrl+Shift+F5`（Linux）或 `Cmd+Shift+R`（macOS）重新加载配置。

**查看当前配置：**

```bash
# 在 Kitty 中运行
kitty @ get-config scrollback_lines
```

**内存占用估算：**

- 10000 行 ≈ 10MB
- 50000 行 ≈ 50MB  
- 100000 行 ≈ 100MB

根据你的使用场景和内存情况选择合适的值。

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
