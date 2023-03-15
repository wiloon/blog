---
title: linux 剪贴板
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=15817
categories:
  - inbox
tags:
  - reprint
---
## linux 剪贴板

在 X 系统里面，从一个窗口复制一段文字到另一个窗口，有两套机制，分别是 Selections 和 cut buffers。

常用的 copy & paste 是利用的 cut buffers 机制;另外用鼠标选中一段文字，然后在另一个窗口按鼠标中键实现复制，利用的是 selections 机制。selection 又可以分为 master 和 slave selection。

当用鼠标选中一段文件，这段文字就自动被复制到 master selection。然后在另一个地方按鼠标中键，就自动把 master selection 的内容粘贴出来。

当你想复制少量文字的时候，两种方法都是很方便的。但是当复制大段文字的时候就挺麻烦。另外就是你可能会频繁的执行一些复制粘贴工作，不停的用鼠标选中文字，然后再粘贴。这是对手指的折磨。

我忍受不了这种折磨，所以发现了 xclip， 方便的管理 X selections 里面内容的工具。

比如如下命令就把文件 /etc/passwd 的内容复制到 X master selections 里面了。

xclip -i /etc/passwd

<https://www.x.org/releases/X11R7.7/doc/xorg-docs/icccm/icccm.html>

<http://blog.acgtyrant.com/Linux-%E5%89%AA%E8%B4%B4%E6%9D%BF%E3%83%BB%E7%BB%88%E9%98%B6.html>
我用 Linux 好多年，依然没真正理清 Linux 下剪贴板的用法，因为很多程序的复制粘贴行为都不一样，何况Ｘ还有两种剪贴板，再加上我经常跨机编辑，即 termite+ssh+tmux+neovim，这么多程序叠加在一起，就一直不知道到底怎么复制粘贴好。这不，今天我要在远程主机 yy 上通过 NeoVim 选中里面的内容，复制到另一个远程主机 103 的 NeoVim 上，乱按快捷键一通也没解决。于是终于彻底下定决心搞清 Linux 以及众多程序的剪贴板原理，在此整理并归档研究结论。

原理
<https://wiki.archlinux.org/index.php/Clipboard>

X Window 中的剪贴板

按这两篇的说法，所谓两种剪贴板 Clipboard 和 Primary selection 都是Ｘ的功能。区别是前者用 Windows 那样的复制粘贴键 ctrl+c/ctrl+v，后者只需选中内容，就可以在别的地方用鼠标中键粘贴。还有 shift+insert 能起到 ctrl+v 的作用，但这键太冷门了就不记了。

此外其实这两个剪贴板都是异步的——只有在粘贴时，才会真正触发复制！我实践发现，哪怕在 Gedit 主动用 ctrl+c 复制后，关掉 Gedit，在 Google Chrome 的地址栏就粘贴不出来任何东西了。 于是 ArchWiki 建议改用剪贴板管理器来解决。此外为了措辞上的方便，下文假设复制粘贴是同步的，比如「复制东西进剪贴板」。

选中也不一定可以复制，除了依云提到的，我还发现 Google Chrome 按 alt+d 选中地址栏的 URL，不能复制；但鼠标双击地址栏全选，能复制。

简化原则
为了解决如此复杂的剪贴板问题，我需要设定一些简化原则，减轻记忆负担。

只用 clipboard！从此以后就当 Linux 只存在一种剪贴板。自然不用记住选中却无法复制的例外情况了。primary，不存在。

尽可能地让所有程序的复制粘贴键接近 vim-binding。

程序
开始整理并归档御用程序如何使用剪贴板的解决方案。

御用剪贴板交互命令・xclip
除了用程序本身的复制粘贴键、鼠标选中复制与中键粘贴行为，其实也有现成的命令，能在 Shell 里与Ｘ剪贴板互动。最常见的有两个命令:  ‘xclip’ vs. ‘xsel’

由于 xsel 已经两年没更新了，而且 GitHub 官方帮助又钦定 xclip，再加上 xclip 比 xsel 顺耳许多了。我决定 xclip 作为御用剪贴板交互命令。

xclip 默认复制进 primary，坑。

御用虚拟终端・Termite
<https://wiki.archlinux.org/index.php/Termite>

Termite 像 Vim，有两种模式: Insert 和 Selection。

Insert 模式下，可以直接用鼠标选中内容，但它的行为和 Vim 不一样: 仍然处于 Insert 模式！用户可以一边选中内容，一边输入内容。由于虚拟终端和 Shell 紧密相关，不能直接用 ctrl+c/ctrl+v，只能用 ctrl+shift+c/ctrl+shift+v 代替复制粘贴。

按 ctrl+shift+space 可以进入 selection 模式，行为和 Vim 一样，不赘述。

复制会复制到Ｘ剪贴板，我测试了下发现包括 clipboard.

由于我习惯用 Tmux，Termite 的复制粘贴功能其实不重要，无需记忆。不过，我发现 Termite 的 ctrl+shift+v 在 Tmux 一样有效 ！

御用网络传输协议・SSH
既然剪贴板由Ｘ负责，那么我们需要 SSH 能够转发远程主机上的Ｘ程序到本地上，从而让远程主机能与本地的剪贴板互动。信任远程主机的话，alias ssh='ssh -Y' 即可。

实践证明，我 SSH 到远程主机并开启 Tmux 后，我可以把 clipboard 的东西通过 Termite 的 ctrl+shifht+v 粘贴进该 Tmux Session 的某 pane 里。

御用终端多路复用器・Tmux
由于 Termite 的复制粘贴直接作用于整个虚拟终端的界面上，不分 Tmux 里的 pane，于是需要掌握 Tmux 下能在 pane 复制粘贴行为。

Tmux 也有两种模式。一是常规模式，即用户在 pane 里的行为和单个虚拟终端一样；另一是 copy-mode，为能够在 pane 下滚动历史或复制而服务，其又有两种 binding，一是 Emacs 另一是 Vim，默认用 Emacs binding。

我习惯 vim-like 步骤与行为，自然要重新设置为 Vim Binding:  set-window-option -g mode-keys vi。

此外 Tmux 2.4 有重新定义 Key Binding 语法，本文不考虑 Tmux 2.4 之前的旧 Key Binding 语法。

Tmux 原本进入 copy-mode 的默认 key binding 为 prefix+[，太蠢，为保持与 Vim Binding 一致，可以直接修改:  bind-key Escape copy-mode # enter copy mode (prefix Escape)，模仿在 Vim 从 Insert 模式退出，进入 Normal 模式的行为。

再继续改造 key bindings:

bind-key -T copy-mode-vi 'v' send-keys -X begin-selection
bind-key -T copy-mode-vi 'V' send-keys -X select-line
bind-key -T copy-mode-vi 'r' send-keys -X rectangle-toggle
bind-key -T copy-mode-vi 'y' send-keys -X copy-pipe-and-cancel "xclip -in -selection clipboard"
需要注意的是 Tmux copy mode 不支持 Vim Visual 模式 ctrl+v 那样的 block selection，但是可以通过 r 改变 v 的 selection 行为，即从跨行 selection 和 block selection 之间转换。y 则是粘贴进 clipboard 了。

更进一步地像 Vim 那样能滚动浏览 pane 的历史:

# scroll like vim

bind-key -T copy-mode-vi f send-keys page-down
bind-key -T copy-mode-vi b send-keys page-up
bind-key -T copy-mode-vi d send-keys halfpage-down
bind-key -T copy-mode-vi u send-keys halfpage-up
其实本来还可以加 bind-key p run "xclip -o -sel clip | tmux load-buffer - ; tmux paste-buffer"，不过还是 ctrl+shift+v 粘贴更方便，就不加了。

御用文本编辑器・NeoVim
Vim 要有开启 clipboard 编译选项，才支持剪贴板 (大概) 。据说 Arch Linux 的 vim 就没开启！只能改装 gvim 包了。

好在 NeoVim 支持，但需要额外的依赖，help clipboard 指出:

The presence of a working clipboard tool implicitly enables the '+' and '*'
registers. Nvim looks for these clipboard tools, in order of priority:

- |g:clipboard|
- pbcopy/pbpaste (macOS)
- xsel (if $DISPLAY is set)
- xclip (if $DISPLAY is set)
- lemonade (for SSH) <https://github.com/pocke/lemonade>
- doitclient (for SSH) <http://www.chiark.greenend.org.uk/~sgtatham/doit/>
- win32yank (Windows)
- tmux (if $TMUX is set)
显然装 xclip 就行了。

Vim 默认 VISUAL 选中内容不会复制进 primary，这样正好，毕竟 Vim 重在编辑。可以通过 shift+"+y 复制进 clipboard。

至于到底怎么复制粘贴，看 How to make vim paste from (and copy to) system’s clipboard? 就够了。

最后，如何在 SSH 到远程主机再 Tmux 后再开 NeoVim，如何复制粘贴到本地？简单，ssh -Y，本地和远程主机都装 xclip，跟平常一样复制粘贴。

御用剪贴板管理器・Flicx Clipboard
参见 Fcitx Clipboard，在其插件的高级设置里可以把 primary text 关掉。作为剪贴板管理器已经足够好用了。

Written with StackEdit.

## xclip
<https://linuxtoy.org/archives/xclip.html>

在 X 系统里面,从一个窗口复制一段文字到另一个窗口,有两套机制,分别是 Selections 和 cut
  
buffers。

常用的 copy & paste 是利用的 cut
  
buffers 机制;另外用鼠标选中一段文字,然后在另一个窗口按鼠标中键实现复制,利用的是 selections
  
机制。selection 又可以分为 master 和 slave selection。

当用鼠标选中一段文件,这段文字就自动被复制到 master
  
selection。然后在另一个地方按鼠标中键,就自动把 master
  
selection 的内容粘贴出来。

当你想复制少量文字的时候,两种方法都是很方便的。但是当复制大段文字的时候就挺麻烦。另外就是你可能会频繁的执行一些复制粘贴工作,不停的用鼠标选中文字,然后再粘贴。这是对手指的折磨。

我忍受不了这种折磨,所以发现了 xclip, 方便的管理 X selections
  
里面内容的工具。

比如如下命令就把文件 /etc/passwd 的内容复制到 X master
  
selections 里面了。

xclip -i /etc/passwd

然后到别的地方就能复制出来,利用鼠标中键。或者是更舒服的 shift+insert。
  
我现在最常用的方法是通过键盘绑定来管理 X master
  
selections 的内容。比如 alt+F1 就能把我的 ~/f1 的内容复制到 X master
  
selections,alt+F2 复制 ~/f2 的内容。这样就能把你需要经常用到的内容方便的进行复制粘贴。比如常用的密码啥的。
