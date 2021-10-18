---
title: emacs copy current line
author: "-"
type: post
date: 2011-04-30T09:32:53+00:00
url: /?p=148
bot_views:
  - 4
categories:
  - Emacs

---
# emacs copy current line
;;copy current line
  
(global-set-key (kbd "C-c C-w") 'copy-lines)
  
(defun copy-lines(&optional arg)
    
(interactive "p")
    
(save-excursion
      
(beginning-of-line)
      
(set-mark (point))
      
(next-line arg)
      
(kill-ring-save (mark) (point))
      
)
    
)