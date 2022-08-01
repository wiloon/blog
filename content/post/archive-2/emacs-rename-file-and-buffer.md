---
title: emacs rename file and buffer
author: "-"
date: 2017-07-05T04:26:54+00:00
url: /?p=10783
categories:
  - Inbox
tags:
  - reprint
---
## emacs rename file and buffer

<https://stackoverflow.com/questions/384284/how-do-i-rename-an-open-file-in-emacs>

;; source: <http://steve.yegge.googlepages.com/my-dot-emacs-file>
  
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
