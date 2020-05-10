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
<pre>download nXML from <a href="http://www.thaiopensource.com/nxml-mode/">http://www.thaiopensource.com/nxml-mode/</a></pre>

<pre>To get things automatically loaded each time you start Emacs, add
(load "~/nxml-mode-200YMMDD/rng-auto.el")</pre>

<pre>To use nxml-mode automatically for files with an extension of xml,</pre>

<pre>xsl, rng or xhtml, add
(setq auto-mode-alist
        (cons '("\.\(xml\|xsl\|rng\|xhtml\)\'" . nxml-mode)
	      auto-mode-alist))</pre>