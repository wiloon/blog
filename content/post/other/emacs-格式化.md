---
title: emacs format, 格式化
author: "-"
date: 2011-09-21T07:08:09+00:00
url: /?p=822
categories:
  - Emacs

tags:
  - reprint
---
## emacs format, 格式化
http://www.blogjava.net/killme2008/archive/2011/07/26/355041.html

格式化源码是很常见的需求，emacs有个indent-region函数用于格式化选定的代码，前提是你处在某个非text mode下，如c-mode或者java-mode之类。如果要格式化整个文件，你需要先选定整个文件(C-x-h)，然后调用indent-region (或者 C-M-\ )。两个命令总是麻烦，我们可以定义个函数搞定这一切，并绑定在一个特定键上，实现一键格式化: 

```bash
  
;;格式化整个文件函数
  
(defun indent-whole ()
    
(interactive)
    
(indent-region (point-min) (point-max))
    
(message "format successfully"))
  
;;绑定到F7键
  
(global-set-key [f7] 'indent-whole)
  
```

    将这段代码添加到你的emacs配置文件 (~/.emacs)，重启emacs，以后格式化源码都可以用F7一键搞定。
    

1. 整理整个文件

M-x mark-whole-buffer 或者 C-x h //选中整个文件
  
M-x indent-region 或者 C-M- //格式化选中

2. 整理某个函数

M-x mark-defun 或者 C-M-h //选中函数
  
M-x indent-region 或者 C-M- //格式化