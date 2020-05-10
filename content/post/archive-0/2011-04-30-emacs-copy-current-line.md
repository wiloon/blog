---
title: emacs copy current line
author: wiloon
type: post
date: 2011-04-30T09:32:53+00:00
url: /?p=148
bot_views:
  - 4
categories:
  - Emacs

---
;;copy current line
  
(global-set-key (kbd &#8220;C-c C-w&#8221;) &#8216;copy-lines)
  
(defun copy-lines(&optional arg)
    
(interactive &#8220;p&#8221;)
    
(save-excursion
      
(beginning-of-line)
      
(set-mark (point))
      
(next-line arg)
      
(kill-ring-save (mark) (point))
      
)
    
)