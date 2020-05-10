---
title: Fcitx
author: wiloon
type: post
date: 2017-01-12T04:50:30+00:00
url: /?p=9650
categories:
  - Uncategorized

---
### 在线造词

(词组最长为10个汉字)
  
在中文输入方式下按CTRL+8，则利用将刚刚输入的内容造词，默认为最近输入法两个字，可以用左右方向键的增加或减少词组中的字数,回车确认。

输入法提供了两种在线造词方法(词组最长为 10 个汉字):
       
1) 在中文输入方式下按 CTRL_8,则利用将刚刚输入的内容造词,默认为最近输
      
入法两个字,可以用左右方向键的增加或减少词组中的字数。
       
2) 自动组词:将需要造的词按单字连续输入后,再按它的组词规则连续输入编码 ,
      
程序会提示用户这个新词。如果此时按空格或它前面的序号则将这个新词输入到用
      
户程序中,您可以设置这个新词是否进入词库。如果不想录入该词,继续进行下一
      
次输入即可(fcitx 只能记录最近 2048 个输入的字)。
  
如果想删除词库中的词,先让该词显示中输入条上,按 CTRL_7,并按提示操作即可;
  
或是当程序提示有该词组时,按 CTRL_DEL 删除。

### 调整词顺序

ctrl+6

### 五笔词库位置

/home/user0/.config/fcitx/table/wbx.mb

### 安装fcitx

<pre><code class="language-bash line-numbers">sudo pacman -S fcitx

#图形界面的配置程序：KDE 中的 kcm-fcitx
sudo pacman -S  kcm-fcitx

# gtk3 config tool
sudo pacman -S fcitx-configtool

# 输入法模块
sudo pacman -S fcitx-im

#五笔
# 可能需要重启
sudo pacman -S fcitx-table-extra 

#edit .zshrc
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx

#start fcitx
fcitx

# 解决 emacs 中文输入问题
sudo rm /usr/bin/emacs.raw
sudo mv /usr/bin/emacs /usr/bin/emacs.raw

#since emacs is unavailabe now
sudo vi /usr/bin/emacs

#new /usr/bin/emacs file content
#! /bin/bash
export LC_CTYPE=zh_CN.utf-8;
/usr/bin/emacs.raw "$@"

</code></pre>

### .zshrc

<pre><code class="language-bash line-numbers">vim .zshrc

export XIM="fcitx"
export XIM_PROGRAM="fcitx"
export XMODIFIERS="@im=fcitx"
export GTK_IM_MODULE="fcitx"
export QT_IM_MODULE="fcitx"
export LC_CTYPE=zh_CN.UTF-8
</code></pre>

## Fcitx 配置工具

<pre><code class="language-bash line-numbers">fcitx-configtool
</code></pre>

### 修改剪贴板快捷键

Input Method &#8211; System Settings Module -> Addon Config -> Clipboard

### 修改简繁切换快捷键

Input Method Configuration -> Addon -> Simplified Chinese To Traditional Chinese

### 删除词组

ctrl-7

### fcitx 微信

https://github.com/countstarlight/deepin-wine-wechat-arch/issues/12
  
https://github.com/countstarlight/deepin-wine-tim-arch/issues/5
  
https://github.com/countstarlight/deepin-wine-wechat-arch/issues/13

<blockquote class="wp-embedded-content" data-secret="WTjsfTu5gR">
  <p>
    <a href="https://beekc.top/2019/01/26/deepin-wine-input-chinese/">deepin版微信输入中文</a>
  </p>
</blockquote>

<iframe title="《deepin版微信输入中文》—BEEKC" class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="https://beekc.top/2019/01/26/deepin-wine-input-chinese/embed/#?secret=WTjsfTu5gR" data-secret="WTjsfTu5gR" width="600" height="338" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>
  
https://blog.csdn.net/qq_18649781/article/details/87476043
  
https://blog.hellojukay.cn/2019/08/09/20190810/
  
https://bbs.archlinuxcn.org/viewtopic.php?id=2052

## https://zhuanlan.zhihu.com/p/51957263

http://forum.ubuntu.org.cn/viewtopic.php?f=68&t=395616
  
https://blog.csdn.net/rznice/article/details/79840261
  
https://registerboy.pixnet.net/blog/post/12180583