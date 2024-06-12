---
title: fcitx
author: "-"
date: 2022-07-09 20:57:51
url: fcitx
categories:
  - Desktop
tags:
  - reprint
---
## fcitx

## ubuntu 22.04 install fcitx5

检查系统中文环境
在 Ubuntu 设置中打开「区域与语言」—— 「管理已安装的语言」，然后会自动检查已安装语言是否完整。若不完整，根据提示安装即可。

最小安装
为使用 Fcitx 5，需要安装三部分基本内容：

Fcitx 5 主程序
中文输入法引擎
图形界面相关
按照这个思路，可以直接使用 apt 进行安装：

sudo apt install fcitx5 \
fcitx5-chinese-addons \
fcitx5-frontend-gtk4 fcitx5-frontend-gtk3 fcitx5-frontend-gtk2 \
fcitx5-frontend-qt5

配置
设置为默认输入法
使用 im-config 工具可以配置首选输入法，在任意命令行输入：

im-config

根据弹出窗口的提示，将首选输入法设置为 Fcitx 5 即可。

环境变量
需要为桌面会话设置环境变量，即将以下配置项写入某一配置文件中：

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
## 切换 全角半角符号, 逗号, 句号

ctrl + .

### 调整词顺序

ctrl+6

### 删除词

ctrl+7
```

### 五笔词库位置

```Bash
# fcitx5
/home/ywang6/.local/share/fcitx5/table/wbx.user.dict

# fcitx
/home/wiloon/.config/fcitx/table/wbx.mb
```

## 安装 fcitx

```bash
sudo pacman -S fcitx  kcm-fcitx fcitx-configtool fcitx-im fcitx-table-extra
# kcm-fcitx: 图形界面的配置程序: KDE 中的 kcm-fcitx
# fcitx-im: 输入法模块
# fcitx-table-extra: 输入法模块-五笔, 可能需要重启
# fcitx-configtool: gtk3 config tool, optional
```

### .zshrc

```bash
vim .zshrc
```

```bash
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
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
