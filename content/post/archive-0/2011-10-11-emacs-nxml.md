---
title: emacs nXML
author: wiloon
type: post
date: 2011-10-11T10:41:36+00:00
url: /?p=1018
views:
  - 8
bot_views:
  - 14
categories:
  - Emacs

---
download nXML from <a href="http://www.thaiopensource.com/nxml-mode/">http://www.thaiopensource.com/nxml-mode/</a>

To get things automatically loaded each time you start Emacs, add
(load "~/nxml-mode-200YMMDD/rng-auto.el")

To use nxml-mode automatically for files with an extension of xml,

xsl, rng or xhtml, add
(setq auto-mode-alist
        (cons '("\.\(xml\|xsl\|rng\|xhtml\)\'" . nxml-mode)
	      auto-mode-alist))