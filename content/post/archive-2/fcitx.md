---
title: fcitx
author: "-"
date: 2017-01-12T04:50:30.000+00:00
url: fcitx
categories:
  - Desktop
tags:
  - reprint
---
## fcitx
## 繁体简体转换快捷键

    addon里找 繁体简体转换，修改快捷键

### 配置文件
    vim ~/.config/fcitx/config
### 在线造词
(词组最长为10个汉字)
在中文输入方式下按CTRL+8,则利用将刚刚输入的内容造词,默认为最近输入法两个字,可以用左右方向键的增加或减少词组中的字数,回车确认。
输入法提供了两种在线造词方法(词组最长为 10 个汉字):
1. 在中文输入方式下按 CTRL_8,则利用将刚刚输入的内容造词,默认为最近输
入法两个字,可以用左右方向键的增加或减少词组中的字数。
1. 自动组词:将需要造的词按单字连续输入后,再按它的组词规则连续输入编码 ,
   程序会提示用户这个新词。如果此时按空格或它前面的序号则将这个新词输入到用
   户程序中,您可以设置这个新词是否进入词库。如果不想录入该词,继续进行下一
   次输入即可(fcitx 只能记录最近 2048 个输入的字)。
   如果想删除词库中的词,先让该词显示中输入条上,按 CTRL_7,并按提示操作即可;
   或是当程序提示有该词组时,按 CTRL_DEL 删除。

### 调整词顺序

ctrl+6

### 删除词

ctrl+7

### 五笔词库位置

/home/wiloon/.config/fcitx/table/wbx.mb

## 安装 fcitx

```bash
sudo pacman -S fcitx  kcm-fcitx fcitx-configtool fcitx-im fcitx-table-extra
# kcm-fcitx: 图形界面的配置程序: KDE 中的 kcm-fcitx
# fcitx-im: 输入法模块
# fcitx-table-extra: 输入法模块-五笔, 可能需要重启
# fcitx-configtool: gtk3 config tool, optional
```

### vim .zshrc

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

        sudo rm /usr/bin/emacs.raw
        sudo mv /usr/bin/emacs /usr/bin/emacs.raw

        #since emacs is unavailabe now
        sudo vi /usr/bin/emacs

        #new /usr/bin/emacs file content
        #! /bin/bash
        export LC_CTYPE=zh_CN.utf-8;
        /usr/bin/emacs.raw "$@"

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

### deepin版微信输入中文

[https://beekc.top/2019/01/26/deepin-wine-input-chinese/](https://beekc.top/2019/01/26/deepin-wine-input-chinese/ "https://beekc.top/2019/01/26/deepin-wine-input-chinese/")

/opt/deepinwine/apps/Deepin-WeChat/run.sh

    export GTK_IM_MODULE=fcitx
    export QT_IM_MODULE=fcitx
    export XMODIFIERS="@im=fcitx"

https://blog.csdn.net/qq_18649781/article/details/87476043

https://blog.hellojukay.cn/2019/08/09/20190810/

https://bbs.archlinuxcn.org/viewtopic.php?id=2052

>https://zhuanlan.zhihu.com/p/51957263

http://forum.ubuntu.org.cn/viewtopic.php?f=68&t=395616

https://blog.csdn.net/rznice/article/details/79840261

https://registerboy.pixnet.net/blog/post/12180583