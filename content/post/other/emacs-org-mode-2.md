---
title: emacs org mode
author: "-"
date: 2012-02-17T02:32:36+00:00
url: /?p=2327
categories:
  - Emacs
tags:
  - reprint
---
## emacs org mode
Emacs 22 以后的版本已经集成了 org-mode，打开 .org 扩展的文件会自动进入 org 模式。

增减一个TODO项目的优先级 S-Up/Down

move subtree/list item up/down M-S-UP/DOWN
  
promote/demote heading M-LEFT/RIGHT
  
insert new TODO entry/checkbox item M-S-RET
  
insert TODO entry/ckbx after subtree C-S-RET

C-RET加入新的同级标识

M-left将当前项提升一级

M-right将当前项降低一级

M-S-left将当前分支提升一级

M-S-right将当前分支降低一级

M-S-up将当前分支向上移动

M-S-down将当前分支向下移动

C-c C-x C-k删除当前分支

C-c C-x M-w复制当前分支

C-c C-x C-y粘贴分支

C-c C-w移动当前分支

C-c *为当前分支加入内容

3.1 关于TODO ITEM的基本知识和操作

设置TODO项目所有标题只要以TODO开头，就会变成TODO 项目。例如: 
  
\*** TODO 付手机费
  
\*** TODO 开会
  
更改TODO项目的状态
  
C-c C-t Rotate the TODO state of the current item among
  
,-> (unmarked) -> TODO -> DONE -.
  
'-----------'
  
C-c C-t是在定义的状态中循环，而C-u C-c C-t可以指定一个状态。

S-Right 和 S-Left也可以在定义的状态中循环。

C-c / t (org-show-todo-tree) will redisplay the current document as a sparse tree which only shows TODO items. Alternatively, to show only DONE items, you can use C-c / T DONE.

to archive all done item c-c c-x c-s

http://www.cnblogs.com/holbrook/archive/2012/04/12/2444992.html
  
http://i.linuxtoy.org/docs/guide/ch32s02.html
  
http://emacser.com/org-mode.htm