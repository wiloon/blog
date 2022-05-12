---
title: emacs 启动 窗口最大化
author: "-"
date: 2011-08-18T02:49:36+00:00
url: /?p=434
categories:
  - Emacs
tags:$
  - reprint
---
## emacs 启动 窗口最大化
(defun fullscreen (&optional f)
  (interactive)
  (x-send-client-message nil 0 nil "_NET_WM_STATE" 32
                 '(2 "_NET_WM_STATE_MAXIMIZED_VERT" 0))
  (x-send-client-message nil 0 nil "_NET_WM_STATE" 32
                 '(2 "_NET_WM_STATE_MAXIMIZED_HORZ" 0)))
(add-hook 'window-setup-hook 'fullscreen)