---
title: kitty
author: "-"
date: 2026-01-30T11:30:06+08:00
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

## 远程控制（Remote Control）

Kitty 支持通过命令行远程控制终端，可以实现自动化窗口管理、发送命令等功能。

### 启用远程控制

在 `~/.config/kitty/kitty.conf` 中添加：

```conf
# Unix Socket 方式（推荐，可从任何终端控制）
allow_remote_control socket-only
listen_on unix:/tmp/kitty.sock
```

**注意**：使用 Unix Socket 方式时，Kitty 会在 socket 文件名后自动添加进程 ID，例如：
- 配置：`listen_on unix:/tmp/kitty.sock`
- 实际文件：`/tmp/kitty.sock-387363`（387363 是进程 ID）

### 基本使用示例

```bash
# 查找当前 Kitty 的 socket 文件
ls -t /tmp/kitty.sock-* | head -1

# Hello World 示例：在终端打印 "hello world"
kitty @ --to unix:/tmp/kitty.sock-387363 send-text "echo hello world\n"

# 自动查找 socket 的通用命令
kitty @ --to unix:$(ls -t /tmp/kitty.sock-* | head -1) send-text "echo hello world\n"
```

### 常用远程控制命令

```bash
# 列出所有窗口和标签页
kitty @ --to unix:$(ls -t /tmp/kitty.sock-* | head -1) ls

# 创建新窗口
kitty @ --to unix:$(ls -t /tmp/kitty.sock-* | head -1) launch

# 切换布局
kitty @ --to unix:$(ls -t /tmp/kitty.sock-* | head -1) goto-layout tall

# 发送命令到当前窗口
kitty @ --to unix:$(ls -t /tmp/kitty.sock-* | head -1) send-text "ls -la\n"
```

### 远程控制的应用场景

- **自动化开发环境**：一键启动多个项目窗口
- **IDE 集成**：从编辑器发送代码到终端执行
- **脚本自动化**：批量管理窗口和标签页
- **会话管理**：保存和恢复工作环境

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

- **Linux**: `Ctrl+Shift+Delete` - 完全清空终端和滚动缓冲区
- **macOS**: `Cmd+K` - 完全清空终端和滚动缓冲区

完整配置参见下文的 **Linux 完整配置** 和 **macOS 配置说明** 部分

### 三种清空方式对比

| 方式 | 命令/快捷键 | 清空屏幕 | 清空滚动缓冲区 |
|------|------------|---------|---------------|
| 标准 clear | `clear` 或 `Ctrl+L` | ✅ | ❌ |
| 完全清空 | `printf '\033[2J\033[3J\033[1;1H'` | ✅ | ✅ |
| Kitty 快捷键 | `Ctrl+Shift+Delete` (需配置) | ✅ | ✅ |

## 滚动查看历史输出

Kitty 没有滚动条，但可以用快捷键或鼠标滚动查看历史输出：

- **鼠标滚轮** - 上下滚动，按住 Shift 加速
- **快速跳转** - Home/End 键跳到顶部/底部
- **History 浏览模式** - `Ctrl+Shift+H`（Linux）或 `Cmd+H`（macOS）进入 Vim 风格浏览

完整快捷键配置参见下文的 **Linux 完整配置** 和 **macOS 配置说明** 部分

### History 浏览模式（推荐）

进入 history 模式可以像 Vim 一样浏览：

- 使用 Vim 风格的快捷键：`g`/`G` 跳转开头/结尾，`j`/`k` 上下移动，`/` 搜索
- 按 `q` 或 `Esc` 退出浏览模式

**提示**：最快查看历史记录的方式是进入 history 模式然后按 `g` 直接跳到第一行！

## 搜索终端文字

在 Kitty 中可以搜索终端显示的文字内容（包括滚动缓冲区）：

### 搜索方式

**Vim/less 风格搜索（内置）**：
- 进入 history 浏览模式，按 `/` 输入搜索关键词
- 按 `n` 跳转到下一个匹配，`N` 上一个匹配
- Kitty 默认使用这种方式，无需图形化搜索框

**fzf 模糊搜索（推荐）**：
- 需要先安装 fzf：`sudo apt install fzf`（Linux）或 `brew install fzf`（macOS）
- 提供交互式模糊搜索界面、实时预览、多选等高级功能
- 配置方法参见下文的 **Linux 完整配置** 部分

### 搜索功能特性

- 支持正则表达式搜索
- 实时高亮所有匹配项
- 支持大小写敏感/不敏感切换
- 可搜索滚动缓冲区中的历史内容
- 搜索时会自动滚动到匹配位置

完整搜索快捷键配置参见下文的 **Linux 完整配置** 和 **macOS 配置说明** 部分

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
- `Cmd+D` - 垂直分割（左右分屏）
- `Cmd+Shift+D` - 水平分割（上下分屏）
- `Cmd+Shift+W` - 关闭当前窗口
- `Cmd+]` / `Cmd+[` - 切换窗口
- `Cmd+Shift+]` / `Cmd+Shift+[` - 移动窗口
- `Cmd+Shift+R` - 重新加载配置

#### 标签页管理
- `Cmd+T` - 新建标签
- `Shift+Cmd+W` - 关闭标签
- `Cmd+1~9` - 切换到指定标签页
- `Ctrl+Tab` / `Ctrl+Shift+Tab` - 切换标签页

### macOS 窗口分割快捷键故障排查

如果在 macOS 中窗口分割快捷键不工作，可能的原因和解决方案：

#### 问题 1：系统快捷键冲突

**检查方法：**
1. 打开"系统设置" → "键盘" → "键盘快捷键"
2. 检查"应用快捷键"和其他系统快捷键是否占用了 `Cmd+D` 或 `Cmd+Shift+D`

**解决方案：**
```conf
# 方案 1：在 kitty.conf 中更改为不冲突的快捷键
map cmd+\ launch --location=vsplit --cwd=current
map cmd+- launch --location=hsplit --cwd=current

# 方案 2：使用 Ctrl 组合键
map ctrl+shift+\ launch --location=vsplit --cwd=current
map ctrl+shift+- launch --location=hsplit --cwd=current
```

#### 问题 2：快捷键未配置或被覆盖

**检查配置文件：**
```bash
# 查看配置文件
cat ~/.config/kitty/kitty.conf | grep -E "(map.*split|map.*launch)"

# 确认配置文件路径
kitty --debug-config | grep "Loaded config"
```

**完整配置示例：**
```conf
# ~/.config/kitty/kitty.conf

# 启用布局（推荐使用 tall 或 splits）
enabled_layouts tall,fat,grid,splits

# 垂直分割（左右分屏）
map cmd+d launch --location=vsplit --cwd=current
map cmd+\ launch --location=vsplit --cwd=current

# 水平分割（上下分屏）  
map cmd+shift+d launch --location=hsplit --cwd=current
map cmd+- launch --location=hsplit --cwd=current

# 窗口导航
map cmd+[ previous_window
map cmd+] next_window
map cmd+shift+w close_window

# 窗口移动
map cmd+shift+up move_window up
map cmd+shift+down move_window down
map cmd+shift+left move_window left
map cmd+shift+right move_window right
```

#### 问题 3：权限问题

**验证 Kitty 权限：**
```bash
# 检查 Kitty 是否有辅助功能权限（可能影响某些快捷键）
# macOS 系统设置 → 隐私与安全性 → 辅助功能 → 确认 Kitty 在列表中并已启用
```

#### 问题 4：快捷键测试

**测试快捷键是否生效：**
```bash
# 在终端中直接测试命令
kitty @ launch --location=vsplit --cwd=current
kitty @ launch --location=hsplit --cwd=current

# 如果命令有效但快捷键无效，说明是快捷键配置问题
```

#### 问题 5：配置文件语法错误

**检查配置文件语法：**
```bash
# Kitty 会在启动时显示配置错误
kitty --debug-config

# 或查看日志
tail -f ~/.local/share/kitty/kitty.log
```

#### 快速修复步骤

1. **备份现有配置：**
```bash
cp ~/.config/kitty/kitty.conf ~/.config/kitty/kitty.conf.backup
```

2. **添加或修改分割快捷键：**
```bash
# 编辑配置文件
nano ~/.config/kitty/kitty.conf

# 添加以下内容（如果不存在）
enabled_layouts tall,splits
map cmd+d launch --location=vsplit --cwd=current
map cmd+shift+d launch --location=hsplit --cwd=current
```

3. **重新加载配置：**
- 按 `Cmd+Shift+R` 或
- 重启 Kitty

4. **测试快捷键：**
- 按 `Cmd+D` 应该垂直分割窗口
- 按 `Cmd+Shift+D` 应该水平分割窗口

#### 替代方案

如果快捷键仍然不工作，可以使用命令行：
```bash
# 在终端中直接输入
kitty @ launch --location=vsplit --cwd=current  # 垂直分割
kitty @ launch --location=hsplit --cwd=current  # 水平分割
```

或创建 shell 别名：
```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加
alias ksplit-v='kitty @ launch --location=vsplit --cwd=current'
alias ksplit-h='kitty @ launch --location=hsplit --cwd=current'
```

### Linux 完整配置

完整的 Kitty 配置文件，包含所有基础设置和快捷键：

```conf
# ============================================
# Kitty Configuration - Linux Version
# ~/.config/kitty/kitty.conf
# ============================================

# -------------------- Remote Control --------------------
allow_remote_control socket-only
listen_on unix:/tmp/kitty.sock

# -------------------- Layout --------------------
enabled_layouts tall,fat,grid,splits,stack

# -------------------- Font --------------------
font_family      Cascadia Code
bold_font        auto
italic_font      auto
bold_italic_font auto
font_size        12.0
disable_ligatures always

# -------------------- Cursor --------------------
cursor_shape block
cursor_blink_interval 0

# -------------------- Window --------------------
remember_window_size  yes
initial_window_width  1200
initial_window_height 800

# -------------------- Performance --------------------
repaint_delay 10
input_delay 3
sync_to_monitor yes

# -------------------- Tab Bar Style --------------------
tab_bar_edge top
tab_bar_style powerline
tab_powerline_style slanted
tab_bar_min_tabs 1
tab_title_template "{fmt.fg.red}{bell_symbol}{activity_symbol}{fmt.fg.tab}{title} [{layout_name}]"

# -------------------- Scrollback Buffer --------------------
scrollback_lines 30000

# -------------------- Theme --------------------
include ./kitty-themes/themes/Tokyo_Night.conf

# ============================================
# Keyboard Shortcuts
# ============================================

# -------------------- Config Management --------------------
map ctrl+shift+f2 load_config_file     # Open config file
map ctrl+shift+f5 load_config_file     # Reload config
map ctrl+shift+f6 debug_config         # Show current config

# -------------------- Window Split --------------------
map ctrl+shift+enter launch --cwd=current                 # New window
map ctrl+shift+\ launch --location=vsplit --cwd=current   # Vertical split (side by side)
map ctrl+shift+- launch --location=hsplit --cwd=current   # Horizontal split (top/bottom)

# -------------------- Window Management --------------------
map ctrl+shift+w close_window          # Close current window
map ctrl+shift+x close_window          # Close current window (alternative)
map alt+w close_window                 # Close current window (Alt+W)
map ctrl+shift+] next_window           # Switch to next window
map ctrl+shift+[ previous_window       # Switch to previous window
map ctrl+shift+r start_resizing_window # Enter window resize mode

# -------------------- Window Move --------------------
map ctrl+shift+up move_window up       # Move current window up
map ctrl+shift+down move_window down   # Move current window down
map ctrl+shift+left move_window left   # Move current window left
map ctrl+shift+right move_window right # Move current window right

# -------------------- Layout Switch --------------------
map ctrl+shift+l next_layout           # Cycle through layouts
map ctrl+shift+h goto_layout fat       # Switch to fat layout (horizontal)
map ctrl+shift+g goto_layout grid      # Switch to grid layout
map ctrl+shift+s goto_layout splits    # Switch to splits layout (free split)
map ctrl+shift+a goto_layout stack     # Switch to stack layout (fullscreen single)

# -------------------- Tab Management --------------------
map ctrl+shift+t new_tab               # New tab
map ctrl+shift+q quit                  # Quit kitty
map ctrl+shift+page_up previous_tab    # Switch to previous tab
map ctrl+shift+page_down next_tab      # Switch to next tab

# -------------------- Search & History --------------------
map ctrl+shift+/ show_scrollback       # Open history browser (/ is search in vim)
map ctrl+shift+f launch --type=overlay --stdin-source=@screen_scrollback fzf --no-sort --no-mouse --exact -i --tac  # fzf fuzzy search
map ctrl+shift+home scroll_home        # Jump to first line
map ctrl+shift+end scroll_end          # Jump to last line
map ctrl+alt+page_up scroll_page_up    # Page up (ctrl+alt to avoid tab switch conflict)
map ctrl+alt+page_down scroll_page_down  # Page down (ctrl+alt to avoid tab switch conflict)

# -------------------- Clear Terminal --------------------
map ctrl+shift+delete clear_terminal reset active  # Clear terminal and scrollback buffer
```

**快捷键记忆法：**

- **tall 布局** → 默认布局，用 `Ctrl+Shift+L` 循环回来（无需单独快捷键）
- `H` → **H**orizontal/Fat（水平分割，上下布局）
- `G` → **G**rid（网格布局）
- `S` → **S**plits（自由分割）
- `A` → st**A**ck（全屏单窗口）
- `F` → **F**uzzy/Find 搜索（fzf 模糊搜索历史输出）

### macOS 配置说明

macOS 下的快捷键配置与 Linux 基本相同，主要区别是：

1. **将 `ctrl` 替换为 `cmd`**：大部分快捷键只需将 `ctrl+shift` 改为 `cmd+shift` 即可
2. **额外的 macOS 特有快捷键**：

```conf
# ============================================
# Kitty 配置文件 - macOS 版本
# ~/.config/kitty/kitty.conf
# ============================================

# macOS 特有快捷键（其余快捷键将 ctrl 替换为 cmd 即可）

# -------------------- 复制粘贴 --------------------
map cmd+c copy_to_clipboard            # 复制
map cmd+v paste_from_clipboard         # 粘贴

# -------------------- 窗口管理（macOS 特有）--------------------
map cmd+n new_os_window                # 新建操作系统窗口

# -------------------- 配置管理 --------------------
map cmd+, load_config_file             # 编辑配置文件
map cmd+shift+f11 toggle_fullscreen    # 切换全屏

# -------------------- 标签页快速切换 --------------------
map cmd+1 goto_tab 1                   # 切换到标签页 1-9
map cmd+2 goto_tab 2
# ... (cmd+3 到 cmd+9 类推)

# -------------------- 字体大小调整 --------------------
map cmd+equal change_font_size all +1.0    # 增大字体
map cmd+minus change_font_size all -1.0    # 减小字体
map cmd+0 change_font_size all 0           # 重置字体大小

# -------------------- 清空终端（macOS 惯例）--------------------
map cmd+k clear_terminal reset active  # 完全清空终端（macOS 使用 cmd+k 而非 ctrl+shift+delete）

# -------------------- 其他快捷键 --------------------
# 所有 Linux 配置中的 ctrl+shift 快捷键，在 macOS 下都改为 cmd+shift
# 例如：
#   ctrl+shift+l → cmd+shift+l  （循环切换布局）
#   ctrl+shift+h → cmd+shift+h  （切换到 fat 布局）
#   ctrl+shift+g → cmd+shift+g  （切换到 grid 布局）
#   ctrl+shift+a → cmd+shift+a  （切换到 stack 布局）
#   ctrl+shift+f → cmd+f        （fzf 搜索）
# ... 其余类推

# -------------------- 布局配置 --------------------
enabled_layouts tall,fat,grid,splits,stack
```

---

## 窗口布局调整

Kitty 默认的分割行为是：第一次分割后，后续窗口都会在下半屏继续分割。可以通过切换布局来调整窗口排列方式。

**快捷键**：完整的布局切换快捷键配置参见上文的 **快捷键** 章节（Linux 完整配置和 macOS 配置说明）。

### 布局类型详解

| 布局名称 | 视觉特征 | 适用场景 | 窗口行为 |
|---------|---------|---------|---------|
| **tall** | 主窗口在左侧占据整个高度，其他窗口在右侧垂直堆叠 | 编辑器+多个终端 | 第一个窗口占左侧，后续窗口在右侧垂直排列 |
| **fat** | 主窗口在上方占据整个宽度，其他窗口在下方水平排列 | 浏览器+多个工具窗口 | 第一个窗口占上方，后续窗口在下方水平排列 |
| **grid** | 所有窗口平均分配空间，形成网格 | 多任务监控、日志查看 | 所有窗口大小相同，自动网格排列 |
| **horizontal** | 所有窗口水平排列成一行 | 并排比较、同时查看多个文件 | 窗口从左到右排列，平均分配宽度 |
| **vertical** | 所有窗口垂直排列成一列 | 长文本查看、流式日志 | 窗口从上到下排列，平均分配高度 |
| **splits** | 自由分割，窗口位置由 Kitty 决定 | 灵活的临时布局 | 新窗口位置不可预测，根据空间自动调整 |
| **stack** | 只显示一个窗口，其他窗口隐藏 | 专注单任务、演示 | 类似标签页，窗口全屏显示 |

**布局选择建议：**

- **垂直分割场景**（左右分屏）→ 使用 `tall` 布局
- **水平分割场景**（上下分屏）→ 使用 `fat` 布局
- **多任务监控**（4 个以上窗口）→ 使用 `grid` 布局
- **专注工作**（减少干扰）→ 使用 `stack` 布局
- **灵活调整**（临时需求）→ 使用 `splits` 布局

**提示**：如果你希望 `Ctrl+Shift+\` 总是在当前窗口右侧创建新窗口，应该使用 `tall` 布局而不是 `splits`

#### 查看当前布局

**方法 1：启用标签栏显示布局（最推荐）✅**

在 `~/.config/kitty/kitty.conf` 中添加配置，让标签栏自动显示当前布局：

```conf
# 启用标签栏（即使只有一个标签页也显示）
tab_bar_edge top
tab_bar_style powerline

# 自定义标签栏格式，显示布局名称
tab_title_template "{fmt.fg.red}{bell_symbol}{activity_symbol}{fmt.fg.tab}{title} [{layout_name}]"
```

配置后，标签栏会实时显示当前布局名称，例如：
- `~ [tall]` - 当前是 tall 布局
- `~ [fat]` - 当前是 fat 布局（水平分割）
- `~ [grid]` - 当前是 grid 布局

**方法 2：命令行查询（无需配置）**

```bash
# 查询当前布局
kitty @ ls | grep -o '"layout": "[^"]*"' | head -1 | cut -d'"' -f4

# 创建 shell 函数（在 ~/.zshrc 中添加）
show-layout() {
    local layout=$(kitty @ ls 2>/dev/null | grep -o '"layout": "[^"]*"' | head -1 | cut -d'"' -f4)
    if [[ -n "$layout" ]]; then
        echo "📐 当前布局: $layout"
    else
        echo "无法获取布局信息"
    fi
}
```

#### 设置默认布局

在 `~/.config/kitty/kitty.conf` 中配置：

```conf
# 设置启用的布局和默认布局
enabled_layouts tall,fat,grid,splits,stack

# 如果希望垂直/水平分割更符合预期，推荐使用 tall 布局
# enabled_layouts tall,splits

# 或者只使用 grid 布局（推荐，窗口平均分配）
# enabled_layouts grid
```

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
