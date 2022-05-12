---
title: emacs 自动补全括号
author: "-"
date: 2011-04-23T12:00:20+00:00
url: /?p=113
categories:
  - Emacs
tags:$
  - reprint
---
## emacs 自动补全括号
;;; use groovy-mode when file ends in .groovy/.gradle or has #!/bin/groovy at start
  
(autoload 'groovy-mode "groovy-mode" "Groovy editing mode." t)
  
(add-to-list 'auto-mode-alist '(".groovy$" . groovy-mode))
  
(add-to-list 'interpreter-mode-alist '("groovy" . groovy-mode))
  
(add-to-list 'auto-mode-alist '(".gradle$" . groovy-mode))

;;auto pair
  
(defun code-mode-auto-pair ()
  
"autoPair"
  
(interactive)
  
(make-local-variable 'skeleton-pair-alist)
  
(setq skeleton-pair-alist '(
  
(?\` ?\` _ """)
  
(?( ? _ " )")
  
(?[ ? _ " ]")
  
(?{ n > _ n ?} >)
  
))
  
(setq skeleton-pair t)
  
(local-set-key (kbd "(") 'skeleton-pair-insert-maybe)
  
(local-set-key (kbd "{") 'skeleton-pair-insert-maybe)
  
(local-set-key (kbd "\`") 'skeleton-pair-insert-maybe)
  
(local-set-key (kbd "[") 'skeleton-pair-insert-maybe))
  
;;add hook to my groovy mode
  
(add-hook 'groovy-mode-hook 'code-mode-auto-pair)