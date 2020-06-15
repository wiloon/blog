---
title: Windows 安装 Emacs
author: wiloon
type: post
date: 2013-09-04T12:27:37+00:00
url: /?p=5794
categories:
  - Emacs

---


Emacs平台很强大，已经不只是一个编辑器这么简单了，它被移植到Windows平台下使得非Unix用户也有幸接触到并使用它。

之前我写了一个Windows7下的Emacs的一点说明，简单说了一下如何在Windows下安装emacs，不过，那不是最佳方式。



因为，按Windows7系统本身的HOME目录配置的话，C:Users<username>AppDataRoaming 这个HOME目录太深了，而且默认状态下AppData目录是隐藏的，最最关键的是：如果系统盘一旦出问题，之前的.emacs配置文件和.el的扩展都得重新配置和下载。



还有另外两咱方法，更改HOME目录：一是添加HOME系统环境变量，这个有个很大的弊端，如果系统里同时还安装有java sdk、Cygwin等，那就可想而知了，这些软件“找不到北的”；二是添加 HKEY\_LOCAL\_MACHINESOFTWAREGNUEmacsHOME=%emacs_dir% 注册表项，好是好，你得重启系统啊。。。



本文给大家介绍一个个人认为最佳的方式：



首先，我们再来看看emacs的简单安装吧，http://ftp.gnu.org/pub/gnu/emacs/windows/emacs-23.2-bin-i386.zip 这里下载emacs-23.2最新版，并解压到一个磁盘根目录，我这里放在了d:下，解压后，得到 d:emacs-23.2，进入d:emacs-23.2bin目录，执行 addpm.exe 在开始菜单中加入 emacs 的启动项。



启动emacs，在 Option 菜单中随便更改一下设置，如 取消 Case-Insensitive Search，之后，点 Save Options。这一步不是多余的哦，因为默认情况下emacs不会在一启动的时候就生成 .emacs 配置文件和 .emacs.d目录的。这步生成的 .emacs 目录还是在 C:Users<username>AppDataRoaming 下，因为我们并没有做别的设置移动它嘛~



下面就进入关键步骤了，打开 C:Users<username>AppDataRoaming.emacs 配置文件，修改内容为

(load-file "D:/apps/emacs-24.5/.emacs")

复制代码

这个配置意思很明显了，emacs在启动的时候会加载 C:Users<username>AppDataRoaming.emacs 这个配置文件，而该文件又加载另一个 D:/emacs-23.2/.emacs 配置文件。这样，自然就成功实现了配置的转移喽~好了，从现在起就不用进入 C:Users<username>AppDataRoaming.emacs 这个冗的路径喽！



上一步，我们把emacs的配置文件用 (load-file &#8230;) 配置已经指向到 D:/emacs-23.2/.emacs 了，那两个就拷贝一个 .emacs 文件放到 D:/emacs-23.2/ 里吧（Windows下好像不能建立以 . 开头的文件吧）。然后，打开D:/emacs-23.2/.emacs，在开头添加如下配置：

(setenv "HOME" "D:/emacs-23.2")

(setenv "PATH" "D:/emacs-23.2")

;;set the default file path

(setq default-directory "~/")



恩，是的，这里重新给 HOME PATH 等定义了新的路径~~~写到这里大家该明白了，就是把配置转移了一下而已。



好了，现在就可以了把 D:/emacs-23.2 当成emacs的 HOME了，配置可以参考这个帖子：http://club.topsage.com/thread-2252500-1-1.html，里面用的两个简单的扩展，由于指定了 load-path 为 ~/.emacs.d/elisp

(setq load-path (cons "~/.emacs.d/elisp" load-path))



也就是 D:/emacs-23.2/.emacs.d/elisp，把两个文件放进去就ok了呗~！



<完>



转载请注明出处：http://club.topsage.com/thread-2253070-1-1.html