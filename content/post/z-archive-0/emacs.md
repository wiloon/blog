---
title: emacs
author: "-"
date: 2012-06-21T01:14:06+00:00
url: emacs
categories:
  - editor

---
## emacs
## emacs yaml plugin
```bash
  
(add-to-list 'load-path "/home/wiloon/.emacs.d/lisp")

(require 'yaml-mode)
  
(add-to-list 'auto-mode-alist '("\\.yml\\'" . yaml-mode))

(add-hook 'yaml-mode-hook
          
(lambda ()
        
(define-key yaml-mode-map "\C-m" 'newline-and-indent)))

```

https://www.emacswiki.org/emacs/YamlMode
  
https://github.com/yoshiki/yaml-mode


## emacs git
Remove git from the list of backends handled by vc-mode:

    (delete 'Git vc-handled-backends) 

or remove **all** source control hooks:

    (setq vc-handled-backends ())

## emacs keys
符号 C- 意思是按住 Ctrol 键
  
M- 意指 Meta 键 (键盘上若无Meta 键，则可以ALT ESC 键来取而代之)
  
DEL 意指退格键 (不是 删除(Delete) key)
  
RET 意指回车键
  
SPC 意指空格键
  
ESC 意指Escape键
  
TAB 意指Tab键

像 "C-M-" (or "M-C") 这样连在一起的意味着同时按住 Control 和 Meta 键不放.

C-x C-h                     列出全部命令
  
C-x ESC ESC            重复执行上一条命令

nXML

M-; 注释一行


### Emacs里统计某个词出现的次数
 
1) M-x count-matches 统计该表达式在buffer中出现的次数。
  
2) M-x occur 统计该表达式在buffer中出现的次数，显示在哪些地方出现了这个表达式.

## emacs version
    M-x emacs-version

## emacs groovy mode
<http://groovy.codehaus.org/Emacs+Groovy+Mode>

## 'Emacs, How to Define Keyboard Shortcuts'
(global-set-key (kbd "C-c o") 'COMMAND);test

## emacs 换行
在替换里面 c-q c-j表示换行

## emacs 插入当前日期
C-c m d

```bash

(defun my-insert-date ()

(interactive)
   
(insert "#")
   
;(insert (user-full-name))
   
;(insert "@")
   
(insert (format-time-string "%Y/%m/%d %H:%M:%S" (current-time))))
   
(global-set-key (kbd "C-c m d") 'my-insert-date)

```



