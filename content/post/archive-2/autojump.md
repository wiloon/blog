---
title: autojump
author: "-"
date: 2017-02-22T15:26:40+00:00
url: /?p=9866
categories:
  - Inbox
tags:
  - reprint
---
## autojump
https://linux.cn/article-3401-1.html

在命令行中切换目录是最常用的操作,不过很少有比一遍又一遍重复"cd ls cd ls cd ls ……"更令人沮丧的事情了。如果你不是百分百确定你想要进入的下一个目录的名字,那么你不得不使用ls来确认,然后使用cd来进入你想要进的那一个。所幸的是,现在大量的终端和shell语言提供了强大的自动补全功能来处理该问题。但是,你仍然需要一直疯狂地敲击TAB键来干这事。如果你和我一样懒惰,你一定会对autojump感到惊喜。

autojump是一个命令行工具,它允许你可以直接跳转到你喜爱的目录,而不用管你现在身在何处。


oh-my-zsh 自带的插件_z_,和 autojump 实现的功能是一样的,但是不用额外安装,直接在plugins=()里启用就可以了。