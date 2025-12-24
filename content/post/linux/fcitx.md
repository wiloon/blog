---
title: fcitx
author: "-"
date: 2025-12-22T14:30:00+08:00
url: fcitx
categories:
  - Desktop
tags:
  - reprint
  - remix
  - AI-assisted
---
## fcitx

https://wiki.archlinux.org/title/Fcitx5

## archlinux KDE 安装 fcitx

https://blog.csdn.net/GaaraZ/article/details/128618441

https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland#KDE_Plasma

```bash
# include 1) fcitx5  2) fcitx5-configtool  3) fcitx5-gtk  4) fcitx5-qt
sudo pacman -S fcitx5-im
sudo pacman -S fcitx5-chinese-addons

# disable fcitx5 desktop file after install fcitx5 in kde
sudo mv /etc/xdg/autostart/org.fcitx.Fcitx5.desktop/org.fcitx.Fcitx5.desktop /etc/xdg/autostart/org.fcitx.Fcitx5.desktop/org.fcitx.Fcitx5.desktop.bak

#---
sudo pacman -S  fcitx-table-extra
# kcm-fcitx5 包的实际内容是 fcitx5-configtool
# fcitx-table-extra: 输入法模块-五笔, 可能需要重启
# fcitx-configtool: gtk3 config tool, optional
```

chrome

application launcher> right click chrome> command line arguments: --ozone-platform=wayland

### .zshrc

```bash
vim .zshrc
```

```bash
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
```

## ubuntu 24.04 install fcitx5

检查系统中文环境
在 Ubuntu 设置中打开「区域与语言 (Region & Language)」—— 「管理已安装的语言」 (Manage Installed Languages)，然后会自动检查已安装语言是否完整。若不完整，根据提示安装即可。

最小安装
为使用 Fcitx 5，需要安装三部分基本内容：

1. Fcitx 5 主程序
2. 中文输入法引擎
3. 图形界面相关

用 apt 进行安装：

```bash
sudo apt install fcitx5 \
fcitx5-chinese-addons \
fcitx5-frontend-gtk4 fcitx5-frontend-gtk3 fcitx5-frontend-gtk2 \
fcitx5-frontend-qt5
```

配置
设置为默认输入法
使用 im-config 工具可以配置首选输入法，在任意命令行输入：

```bash
im-config
```

根据弹出窗口的提示，将首选输入法设置为 Fcitx 5 即可。

环境变量
xorg 需要为桌面会话设置环境变量，即将以下配置项写入某一配置文件中：

```Bash
export XMODIFIERS=@im=fcitx
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
```

如果使用 zsh 作为 shell，则建议写入至 ~/.zshrc ，这样只对当前用户生效，而不影响其他用户。

另一个可以写入此配置的文件为系统级的 /etc/profile 。

开机自启动
安装 Fcitx 5 后并没有自动添加到开机自启动中，每次开机后需要手动在应用程序中找到并启动，非常繁琐。

解决方案非常简单，在 Tweaks（sudo apt install gnome-tweaks）中将 Fcitx 5 添加到「开机启动程序」列表中即可。

```bash
sudo apt install gnome-tweaks
```

### wubi 

restart computer before config wubi input method
run fcitx5 config
取消勾选 “only show current language”
在右侧窗口里选择 wubi 加到左边的空格
点击  apply


Fcitx 配置
Fcitx 5 提供了一个基于 Qt 的强大易用的 GUI 配置工具，可以对输入法功能进行配置。有多种启动该配置工具的方法：

在应用程序列表中打开「Fcitx 配置」
在 Fcitx 托盘上右键打开「设置」
命令行命令 fcitx5-configtool
根据个人偏好进行设置即可。需要注意的是「输入法」标签页下，应将「键盘 - 英语」放在首位，拼音（或其他中文输入法）放在后面的位置。

取消勾选 only show current language

在简体中文中选择 wubi 加入左边窗格

自定义主题
Fcitx 5 默认的外观比较朴素，用户可以根据喜好使用自定义主题。

第一种方式为使用经典用户界面，可以在 GitHub 搜索主题，然后在 Fcitx5 configtool —— 「附加组件」 —— 「经典用户界面」中设置即可。

第二种方式为使用 Kim面板，一种基于 DBus 接口的用户界面。此处安装了 Input Method Panel 这个 GNOME 扩展，黑色的风格与正在使用的 GNOME 主题 Orchis-dark 非常搭配。

https://extensions.gnome.org/extension/261/kimpanel/

## 繁体简体转换快捷键

addon 里找 繁体简体转换，修改快捷键

### 配置文件

```bash
vim ~/.config/fcitx/config
```

## fcitx5 造词方法

fcitx5 提供了多种造词方式，适用于不同场景。

### 方法一：快捷键造词（推荐）

在 Ubuntu 24.04 的 fcitx5 中，使用快捷键造词最为方便：

1. **输入要造词的内容**：先用单字或词组输入你想要造词的内容
1. **按 Ctrl+8**：输入完成后，按下 `Ctrl+8` 快捷键
1. **调整词组长度**：
   - 默认选择最近输入的 2 个字
   - 使用 `←` 左方向键：**增加**字数（最多 10 个字）
   - 使用 `→` 右方向键：**减少**字数
1. **确认造词**：按 `Enter` 回车确认，新词会自动添加到用户词库

**示例**：
```text
输入："人工智能技术"（单字输入）
按 Ctrl+8 → 默认选中"术"
按 ← 扩展 → 选中"技术"
继续按 ← → 选中"能技术"
继续按 ← → 选中"智能技术"
继续按 ← → 选中"工智能技术"
继续按 ← → 选中"人工智能技术"
按 Enter 确认
```

### 方法二：自动组词

fcitx5 支持智能自动组词功能：

1. **连续输入单字**：按单字方式输入需要造词的内容
1. **输入组词编码**：连续输入该词组的拼音/五笔编码
1. **系统提示新词**：fcitx5 会自动识别并提示这是一个新词
1. **选择是否加入词库**：
   - 按 `空格` 或对应的 `序号` 键：将新词输入到程序中，并可选择加入词库
   - 继续输入其他内容：放弃该词

**注意**：fcitx5 只能记录最近 2048 个输入的字符。

### 删除自造词

如果需要删除词库中的自造词：

**方法 1：候选词列表删除**
1. 输入编码让该词显示在候选列表中
1. 按 `Ctrl+7` 进入删除模式
1. 按提示操作完成删除

**方法 2：快速删除**
1. 当词组显示在候选列表时
1. 直接按 `Ctrl+Delete` 即可删除

### 词库文件位置

用户自定义词库文件存储位置：

```bash
# fcitx5 用户词库（二进制格式）
~/.local/share/fcitx5/table/wbx.user.dict  # 五笔
~/.local/share/fcitx5/pinyin/user.dict     # 拼音

# fcitx4 旧版词库（如果从 fcitx4 迁移）
~/.config/fcitx/table/wbx.mb
```

**注意**：词库文件是二进制格式，直接编辑可能导致损坏，建议使用 fcitx5 提供的工具进行管理。

## 其他常用快捷键

```bash
# 切换全角/半角符号（逗号、句号等）
Ctrl + .

# 删除词组
Ctrl + 7

# 快速删除当前候选词
Ctrl + Delete
```

**关于调整词组顺序：**

在 Ubuntu 24.04 的 fcitx5 中，旧版的 `Ctrl+6` 调整词顺序快捷键**已不可用**：

1. **验证结果**（五笔用户）：
   - 打开 `fcitx5-configtool` → **Addons** 标签页
   - 找到 **Table** 插件 → 点击配置按钮
   - 可用的快捷键只有：
     - `Ctrl+8`: Modify Dictionary（造词）
     - `Ctrl+7`: Forget Word（删除词）
     - `Ctrl+Alt+E`: Look up Pinyin（查询拼音）
   - **没有** "Reorder candidate list" 选项

2. **推荐方案**：
   - **依赖自动调整**：fcitx5 会根据使用频率自动调整词组顺序，高频词自动提前
   - **删除重建法**：
     1. 用 `Ctrl+7` 删除低优先级的旧词
     2. 用 `Ctrl+8` 重新造词，新词会获得更高优先级
   - **多次使用**：持续选择使用某个词，系统会逐渐提升其排名

### 在线造词

(词组最长为10个汉字)
在中文输入方式下按 CTRL+8, 则利用将刚刚输入的内容造词, 默认为最近输入法两个字, 可以用左右方向键的增加或减少词组中的字数, 回车确认。
输入法提供了两种在线造词方法(词组最长为 10 个汉字):

1. 在中文输入方式下按 CTRL_8,则利用将刚刚输入的内容造词,默认为最近输
入法两个字,可以用左右方向键的增加或减少词组中的字数。
2. 自动组词:将需要造的词按单字连续输入后,再按它的组词规则连续输入编码 ,
   程序会提示用户这个新词。如果此时按空格或它前面的序号则将这个新词输入到用
   户程序中,您可以设置这个新词是否进入词库。如果不想录入该词,继续进行下一
   次输入即可(fcitx 只能记录最近 2048 个输入的字)。
   如果想删除词库中的词,先让该词显示中输入条上,按 CTRL_7,并按提示操作即可;
   或是当程序提示有该词组时,按 CTRL_DEL 删除。

## 快捷键

```bash
## 切换 全角半角符号, 逗号, 句号, 不需要改配置永久禁用全角符号, 切换即可

ctrl + .

### 调整词顺序

ctrl+6

### 删除词

ctrl+7
```

### 五笔词库位置

词库是一个二进制文件，包含了词组和编码的映射关系。.dict 的结构是 fcitx5-table 的内部格式

```Bash
# fcitx5
~/.local/share/fcitx5/table/wbx.user.dict

# fcitx
~/.config/fcitx/table/wbx.mb
```

#### .mb

```bash
git clone https://github.com/fcitx/fcitx5-table-extra.git
cd fcitx5-table-extra/tools
mkdir build && cd build
cmake ..
make
sudo make install
```

### start fcitx

fcitx 安装之后自己会设置开机启动, 这里临时手动启动一下看看配置有没有问题
    fcitx

### 切换输入法

默认快捷键 ctrl + space

### 解决 emacs 中文输入问题

```bash
sudo rm /usr/bin/emacs.raw
sudo mv /usr/bin/emacs /usr/bin/emacs.raw

#since emacs is unavailabe now
sudo vi /usr/bin/emacs

#new /usr/bin/emacs file content
#! /bin/bash
export LC_CTYPE=zh_CN.utf-8;
/usr/bin/emacs.raw "$@"
```

### .zshrc

vim .zshrc
export XIM="fcitx"
export XIM_PROGRAM="fcitx"
export XMODIFIERS="@im=fcitx"
export GTK_IM_MODULE="fcitx"
export QT_IM_MODULE="fcitx"
export LC_CTYPE=zh_CN.UTF-8

### Fcitx 配置工具

```bash
fcitx-configtool
```

### 修改剪贴板快捷键

Input Method – System Settings Module -> Addon Config -> Clipboard

### 修改简繁切换快捷键

Input Method Configuration -> Addon -> Simplified Chinese To Traditional Chinese

### 删除词组

ctrl-7

### deepin 版微信输入中文

[https://beekc.top/2019/01/26/deepin-wine-input-chinese/](https://beekc.top/2019/01/26/deepin-wine-input-chinese/ "https://beekc.top/2019/01/26/deepin-wine-input-chinese/")

/opt/deepinwine/apps/Deepin-WeChat/run.sh

```bash
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS="@im=fcitx"
```

[https://blog.csdn.net/qq_18649781/article/details/87476043](https://blog.csdn.net/qq_18649781/article/details/87476043)

[https://blog.hellojukay.cn/2019/08/09/20190810/](https://blog.hellojukay.cn/2019/08/09/20190810/)

[https://bbs.archlinuxcn.org/viewtopic.php?id=2052](https://bbs.archlinuxcn.org/viewtopic.php?id=2052)

[https://zhuanlan.zhihu.com/p/51957263](https://zhuanlan.zhihu.com/p/51957263)

[http://forum.ubuntu.org.cn/viewtopic.php?f=68&t=395616](http://forum.ubuntu.org.cn/viewtopic.php?f=68&t=395616)

[https://blog.csdn.net/rznice/article/details/79840261](https://blog.csdn.net/rznice/article/details/79840261)

[https://registerboy.pixnet.net/blog/post/12180583](https://registerboy.pixnet.net/blog/post/12180583)


## ubuntu install fcitx5

```Bash
sudo apt install fcitx5 \
fcitx5-chinese-addons \
fcitx5-frontend-gtk4 fcitx5-frontend-gtk3 fcitx5-frontend-gtk2 \
fcitx5-frontend-qt5
```

settings> region& language> manage installed languages

https://zhuanlan.zhihu.com/p/508797663

## fcitx wayland chrome

https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland#Chromium_.2F_Electron
