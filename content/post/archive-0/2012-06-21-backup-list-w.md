---
title: emacs yaml plugin
author: "-"
type: post
date: 2012-06-21T01:14:06+00:00
url: /?p=3551
categories:
  - Linux

---
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