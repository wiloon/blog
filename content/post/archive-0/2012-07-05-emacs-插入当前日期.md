---
title: emacs 插入当前日期
author: "-"
date: 2012-07-05T07:24:47+00:00
url: /?p=3749
categories:
  - Emacs

---
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