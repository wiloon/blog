---
title: emacs git
author: "-"
date: 2012-06-25T05:31:56+00:00
url: /?p=3667
categories:
  - VCS
tags:
  - emacs
  - Git

---
## emacs git
Remove git from the list of backends handled by vc-mode:

    (delete 'Git vc-handled-backends) 

or remove **all** source control hooks:

    (setq vc-handled-backends ())