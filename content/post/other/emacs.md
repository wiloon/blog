---
title: emacs
author: "-"
date: 2012-06-21T01:14:06+00:00
url: emacs
categories:
  - editor
tags:
  - reprint
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

<https://www.emacswiki.org/emacs/YamlMode>
  
<https://github.com/yoshiki/yaml-mode>

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

## emacs nXML

download nXML from <http://www.thaiopensource.com/nxml-mode/>

To get things automatically loaded each time you start Emacs, add
(load "~/nxml-mode-200YMMDD/rng-auto.el")

To use nxml-mode automatically for files with an extension of xml,

xsl, rng or xhtml, add
(setq auto-mode-alist
        (cons '("\.\(xml\|xsl\|rng\|xhtml\)\'" . nxml-mode)
          auto-mode-alist))

## 'emacs  删除空行'

flush-lines命令

flush-lines删除匹配正则表达式的指定行

m-x flush-lines
  
用正则: ^$

### emacs 刷新, 重新载入文件

;;设置快捷键 F5

(global-set-key [f5] 'revert-buffer)

(global-set-key [C-f5] 'revert-buffer-with-coding-system)

;;按Y或空格确认
(fset 'yes-or-no-p 'y-or-n-p)

## emacs 插入空行

;insert line
  
(global-set-key (kbd "S-<return>") '(lambda()(interactive)(move-end-of-line 1)(newline)))
  
(global-set-key (kbd "C-S-<return>") '(lambda()(interactive)(move-beginning-of-line 1)(newline)(previous-line)))

<http://www.gnu.org/software/emacs/manual/html_node/emacs/Moving-Point.html>

## emacs在替换字符串的时候输入回车/换行

`C-Q C-J`

**Using carriage returns in query-replace / replace-string**

    Use C-Q C-J (control-Q control-J) each time you want to include a carriage return. e.g. to double-space everything
  
  
    M-x replace-string RET C-Q C-J RET C-Q C-J C-Q C-J RET
  
  
    Or to put "bloogie " at the beginning of every line
  
  
    M-x replace-string RET C-Q C-J RET C-Q C-J b l o o g i e SPACE RET
  
## Emacs中以十六进制查看文件
  
    打开文件后，用指令: 
  

  
    m-x hexl-mode
  