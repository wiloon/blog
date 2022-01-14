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
