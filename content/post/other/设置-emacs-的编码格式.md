---
title: 设置 Emacs 的编码格式
author: "-"
date: 2011-12-27T03:09:34+00:00
url: /?p=2033
categories:
  - Emacs
tags:
  - reprint
---
## 设置 Emacs 的编码格式

  
    查看一下 Emacs 读取文件用的编码格式。 M-x describe-coding-system
  
  
    把 Emacs 的默认编码设置为 UTF-8。
  
  
    在 .emacs 文件里放入下面这段代码: 
  
  
    [lisp]
 ;;set the default text coding system
 (setq default-buffer-file-coding-system 'utf-8)
 [/lisp]
 可是即使我加了上面这条语句，为什么 Emacs 依然显示 org 文件为乱码呢？
  
  
    原来上面这一行，只是适用于写文件的情况。当你读取一个文件的时候，可能依然会显示出乱码，因为 Emacs 读文件也是按照一定的编码规律来解读文件的。我们再用命令 M-x describe-coding-system 仔细观察一下结果里面的内容，是不是有类似下面这样一段: 
  
    Priority order for recognizing coding systems when reading files:
    1. iso-latin-1 (alias: iso-8859-1 latin-1)
    2. utf-8 (alias: mule-utf-8)
    3. iso-2022-7bit
    4. iso-2022-7bit-lock (alias: iso-2022-int-1)
    5. iso-2022-8bit-ss2
    6. emacs-mule
    7. raw-text
    8. iso-2022-jp (alias: junet)
    9. in-is13194-devanagari (alias: devanagari)
    10. chinese-iso-8bit (alias: cn-gb-2312 euc-china euc-cn cn-gb gb2312)
    11. utf-8-auto
    12. utf-8-with-signature
    13. utf-16
    14. utf-16be-with-signature (alias: utf-16-be)
    15. utf-16le-with-signature (alias: utf-16-le)
    16. utf-16be
    17. utf-16le
    18. japanese-shift-jis (alias: shift_jis sjis cp932)
    19. undecided
  
  
    这就是 Emacs 在读文件时候的解码顺序！如果你的文件是以英文开头，自然会套用第一种方法。这个时候，我们还需要调整一下这个编码的先后次序。用命令 M-x prefer-coding-system 就可以调整这些顺序。调整完顺序，再打开 org 文件看一看，终于恢复原貌了。
  
  
    如果你只是用命令 M-x prefer-coding-system 来设置，下次重启 Emacs 的时候，这个设置就会自动清除。如果需要每次都采用这个设置，可以把下面这行扔到 .emacs 里指定优先用 utf-8 来解码: 
  
  (prefer-coding-system 'utf-8)
  
 
      另外一种解决乱码的办法，就是用命令 C-x <RET> r ( M-x revert-buffer-with-coding-system) 来用指定的编码重新读入这个文件。
 
  
  
    另外，碰到文件编码混乱的时候，最重要的一点，看到乱码的文件，不要随便保存。有关 Emacs 编码格式的详情可以看看官方文档。
  
  
    原创文章，如转载请注明: 转载自细节之锤 [ http://blog.WaterLin.org/ ]
  
