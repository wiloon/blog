---
title: linux CLI
author: "-"
date: 2011-04-03T02:45:32+00:00
url: /?p=5
categories:
  - Linux
tags:
  - reprint
---
## linux CLI
作为 Linuxer，必须具备一定的 CLI 操作能力。有时候用 CLI 会比用 GUI 会更方便快捷。  —-lcan  
http://lcan.info/2011/03/cli-software/#comment-53  

以下列出我所知道的一些常用 CLI 软件，仅供参考。

1. 中文终端。据我所知，目前主要有两个解决方案: **zhcon** 和 **fbterm**。两个我都用过，zhcon 较长时间不更新了，问题比较多。不小心加错参数，甚至可能会导致死机。所以我推荐 fbterm，这个还是很不错的，要使用的话，必须开启 framebuffer。虽然某些方面也有些瑕疵，不过就目前而言，应该算是一个比较好用的中文终端了。有人可能会问: "中文输入怎么解决？"嘿嘿，这个倒不用担心。比较简陋的有 fbterm_ucimf，另外还有基于 ibus 的 ibus-fbterm 可供选择。
2. 多窗口管理神器: **tmux**。功能和 screen 差不多，不过我感觉 tmux 更加强大、友好！可以横着切、竖着切窗口。让你充分利用你的屏幕！实乃远程管理、多任务控之必备神器啊！
3. 文件管理器: vim 风格的可以选 **ranger**，另外还有 **mc** 之类的。
4. 任务管理器: **htop**。这个可以理解为 top 的加强版。
5. 音乐播放器: **moc**。这个用来播放 mp3，wma，flac 等常见音频文件还是不错的，但是不支持 ape 和 cue。如果这类文件比较多的，那就只能另寻他方了。cmus 也不支持 ape。
6. 视频播放器: **mplayer**。说这个之前，我想咆哮几句: 是谁说 Linux 终端下只能用字符方式看视频啊！！！！是谁说在终端下看视频纯属找虐 啊！！！！！乃们这是误人子弟啊！！！！有木有听说过 framebuffer！！！！有木有！！！！有木有听说过 fbdev 输出！！！！！有木 有！！！！！！ 我以前被人误导，也一直认为在 tty 终端下只能以字符方式看视频，但是直到有一天，我无意中了解到了有 framebuffer 这个东西！！！！无意中看到 mplayer 的视频输出里有 fbdev！！！！于是在开启了 framebuffer 的 tty 下。 mplayer -vo fbdev2 "我要看的视频" 我看到了神马？！我看到了一个清晰的带颜色输出的视频，竟然和在图形界面下播放时的质量差不了多少！！！！有木有看到！！！有木有！！！！
7. PDF/图片查看器: **fbida**。fbida 里面包含了fbi，fbgs，ida，exiftran 四个应用。其中 fbi 可以用来查看图片 (FBI啊，名字就很牛X) ，fbgs 可以用来查看 PDF。前提嘛，估计各位看软件名就知道了，必 须开启 framebuffer。
8. 截图工具: **fbgrab**。不废话，看官方说明: fbgrab – takes screenshots using the framebuffer。在桌面环境下可以用scrot这个命令行软件截屏。
9.  IM 软件: **finch**。这个可以看成是 pidgin 的 CLI 版。
10. IRC 聊天: **irssi**。一个很强大的 IRC 客户端。
11. 邮件客户端: **mutt**。有关介绍请移步 wiki。这个我基本不用。
12. RSS 阅读器: **snownews**。
13. 屏幕录像: **recordmydesktop**。此软件可用于录制 GNOME、KDE 等桌面。

