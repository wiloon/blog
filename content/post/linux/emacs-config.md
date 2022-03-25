---
title: emacs 配置/config
author: "-"
date: 2011-04-16T02:28:41+00:00
url: /?p=41
categories:
  - Emacs

tags:
  - reprint
---
## emacs 配置/config
中文环境
  
之后,在~/.Xresources (如果没有的话,自己建一个) ,加入下面内容: 
  
Xft.antialias: 1
  
Xft.hinting: 1
  
Xft.hintstyle: hintfull
  
调用X Window系统中的字体,并且开启抗锯齿。

之后在~/.emacs下面加入

```bash
  
(custom-set-variables
   
;; custom-set-variables was added by Custom.
   
;; If you edit it by hand, you could mess it up, so be careful.
   
;; Your init file should contain only one such instance.
   
;; If there is more than one, they won't work right.
   
'(inhibit-startup-screen t))
  
(custom-set-faces
   
;; custom-set-faces was added by Custom.
   
;; If you edit it by hand, you could mess it up, so be careful.
   
;; Your init file should contain only one such instance.
   
;; If there is more than one, they won't work right.
   
)

; source: http://steve.yegge.googlepages.com/my-dot-emacs-file
  
(defun rename-file-and-buffer (new-name)
    
"Renames both current buffer and file it's visiting to NEW-NAME."
    
(interactive "sNew name: ")
    
(let ((name (buffer-name))
          
(filename (buffer-file-name)))
      
(if (not filename)
          
(message "Buffer '%s' is not visiting a file!" name)
        
(if (get-buffer new-name)
            
(message "A buffer named '%s' already exists!" new-name)
          
(progn
            
(rename-file filename new-name 1)
            
(rename-buffer new-name)
            
(set-visited-file-name new-name)
            
(set-buffer-modified-p nil))))))

(setq frame-title-format "emacs@%b")

; Set default window size
  
(setq default-frame-alist \`((height . 35) (width . 123)))

;; Set font
  
;;设置DejaVu Sans Mono为默认情况下的字体,字号为12号。
  
;;然后再设置一个字符集,设置字符集字体为WenQuanYi Micro Hei(文泉驿微米黑),当编码为非拉丁字母时,
  
;;系统自动会在/etc/fonts/cond.avail中寻找编码,比如汉字,就对应han,泰文就对应thai,等等.
  
(set-default-font "DejaVu Sans Mono-11")
  
(set-fontset-font (frame-parameter nil 'font)
            
'han '("WenQuanYi Micro Hei"))

;; the following function is to scroll the text one line down while keeping the cursor
  
(defun scroll-down-keep-cursor ()
  
(interactive)
  
(scroll-down 3))

;; set cursor as bar
  
(setq-default cursor-type \`bar)

;; hide tool bar
  
(tool-bar-mode 0)

;; hide menu bar
  
(menu-bar-mode 0)

;; hide scroll bar
  
(scroll-bar-mode 0)

;;enable select to clipboard
  
(setq x-select-enable-clipboard t)

;;允许使用C-z作为命令前缀
  
(define-prefix-command 'ctl-z-map)
  
(global-set-key (kbd "C-z") 'ctl-z-map) 

;;用C-z i快速打开~/.emacs文件。
  
(defun open-init-file ( )
    
(interactive)
    
(find-file "~/.emacs")) 

(global-set-key "\C-zi" 'open-init-file) 

;;启用ibuffer支持,增强\*buffer\*
  
(require \`ibuffer)
  
(global-set-key (kbd "C-x C-b") \`ibuffer)

;show line number
  
(global-linum-mode t)

;;auto backup
  
(setq
      
backup-by-copying t ;自动备份
      
backup-directory-alist
      
'(("." . "~/.saves")) ;自动备份在目录"~/.saves"下
      
delete-old-versions t ;自动删除旧的备份文件
      
kept-new-versions 6 ;保留最近的6个备份文件
      
kept-old-versions 2 ;保留最早的2个备份文件
      
version-control t) ;多次备份

;显示光标所在的行号列号
  
(setq column-number-mode t) 

```

http://murphytalk.github.io/posts/2005/03/03/gai-bian-emacschuang-kou-biao-ti-ge-shi/#.WJpliCFNzWU
  
http://ted.is-programmer.com/tag/emacs
  
http://kidneyball.iteye.com/blog/1014537
  
http://blog.163.com/zhang7410@126/blog/static/233564612009267442384