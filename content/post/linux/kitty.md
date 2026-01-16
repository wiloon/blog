---
title: kitty
author: "-"
date: 2026-01-03T15:20:00+08:00
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

进入 history 模式可以像 Vim 一样浏览：qq

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

### 窗口布局调整

Kitty 默认的分割行为是：第一次分割后，后续窗口都会在下半屏继续分割。可以通过以下方式调整：

#### 快速切换布局（推荐）

- `Ctrl+Shift+L` - 在不同布局之间循环切换

#### 布局类型详解

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

**方法 2：切换布局时临时显示（推荐）✅**

创建一个智能的布局切换脚本，切换时显示 3 秒提示：

```conf
# 在 ~/.config/kitty/kitty.conf 中替换原来的布局切换快捷键
map ctrl+shift+l kitten hints --type=linenum --program=- "next_layout" && launch --type=overlay --hold sh -c 'layout=$(kitty @ ls | grep -o "\"layout\": \"[^\"]*\"" | head -1 | cut -d\" -f4); echo ""; echo "════════════════════"; echo "  当前布局: $layout"; echo "════════════════════"; sleep 2'
```

或者使用更简洁的方式：

```conf
# 切换布局并显示提示
map ctrl+shift+l combine : next_layout : launch --type=overlay --hold sh -c 'layout=$(kitty @ ls | grep -o "\"layout\": \"[^\"]*\"" | head -1 | cut -d\" -f4); printf "\n  📐 布局: \033[1;36m$layout\033[0m\n\n"; sleep 1.5'
```

**方法 3：快捷键查看当前布局**

```conf
# 按键显示当前布局信息
map ctrl+shift+alt+l launch --type=overlay --hold sh -c 'layout=$(kitty @ ls 2>/dev/null | grep -o "\"layout\": \"[^\"]*\"" | head -1 | cut -d\" -f4); echo ""; echo "════════════════════════════"; echo "  📐 当前布局: $layout"; echo "════════════════════════════"; echo ""; echo "可用布局:"; echo "  • tall  - 垂直分割"; echo "  • fat   - 水平分割"; echo "  • grid  - 网格布局"; echo "  • splits- 自由分割"; echo ""; echo "按回车继续..."; read'
```

**方法 4：命令行查询（无需配置）**

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

**推荐配置组合：**

```conf
# 方案 A：标签栏实时显示（最直观）
tab_bar_edge top
tab_bar_style powerline
tab_title_template "{title} [{layout_name}]"

# 方案 B：切换时显示提示（更简洁）
map ctrl+shift+l combine : next_layout : show_message --duration=1.5 "Layout switched"

# 可以同时使用两种方案
```

配置后：
- 按 `Ctrl+Shift+L` - 切换布局（标签栏实时显示当前布局）
- 按 `Ctrl+Shift+Alt+L` - 查看详细布局信息

#### 设置默认布局

在 `~/.config/kitty/kitty.conf` 中配置：

```conf
# 设置启用的布局和默认布局
enabled_layouts tall,fat,grid,splits

# 如果希望垂直/水平分割更符合预期，推荐使用 tall 布局
# enabled_layouts tall,splits

# 或者只使用 grid 布局（推荐，窗口平均分配）
# enabled_layouts grid
```

#### 自定义分割方向

```conf
# 垂直分割（左右分屏）- | for Vertical
# 使用 neighbor 确保新窗口出现在当前窗口旁边
map ctrl+shift+\ launch --location=vsplit --cwd=current

# 如果上面的方式不起作用，可以尝试使用 tall 布局：
# enabled_layouts tall,splits
# map ctrl+shift+\ launch --location=vsplit --cwd=current

# 水平分割（上下分屏）- - for Horizontal  
map ctrl+shift+- launch --location=hsplit --cwd=current
```

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
