---
title: emacs 插件安装
author: "-"
date: 2011-04-23T08:34:58+00:00
url: /?p=98
categories:
  - Emacs

tags:
  - reprint
---
## emacs 插件安装
```bash
  
#edis .emacs
  
(add-to-list 'load-path "/home/wiloon/.emacs.d/lisp")

;;; use groovy-mode when file ends in .groovy or has #!/bin/groovy at start
  
(autoload 'groovy-mode "groovy-mode" "Groovy editing mode." t)

;;files end with .groovy , open as groovy mode

(add-to-list 'auto-mode-alist '(".groovy$" . groovy-mode))

(add-to-list 'interpreter-mode-alist '("groovy" . groovy-mode))

```