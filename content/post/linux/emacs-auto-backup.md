---
title: emacs auto backup
author: "-"
date: 2011-04-23T09:05:52+00:00
url: /?p=106
categories:
  - Emacs
tags:$
  - reprint
---
## emacs auto backup
(setq backup-directory-alist '(("" . "~/backup/emacs/backup")))
  
(setq-default make-backup-file t)
  
(setq make-backup-file t)

(setq make-backup-files t)
  
(setq version-control t)
  
(setq kept-old-versions 2)
  
(setq kept-new-versions 10)
  
(setq delete-old-versions t)