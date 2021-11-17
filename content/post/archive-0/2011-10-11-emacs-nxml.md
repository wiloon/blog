---
title: emacs nXML
author: "-"
date: 2011-10-11T10:41:36+00:00
url: /?p=1018
views:
  - 8
categories:
  - Emacs

---
## emacs nXML
download nXML from http://www.thaiopensource.com/nxml-mode/

To get things automatically loaded each time you start Emacs, add
(load "~/nxml-mode-200YMMDD/rng-auto.el")

To use nxml-mode automatically for files with an extension of xml,

xsl, rng or xhtml, add
(setq auto-mode-alist
        (cons '("\.\(xml\|xsl\|rng\|xhtml\)\'" . nxml-mode)
	      auto-mode-alist))