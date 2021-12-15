---
title: pentaho pdi hello world
author: "-"
date: 2015-01-08T03:05:04+00:00
url: /?p=7201
categories:
  - Uncategorized
tags:
  - Pentaho

---
## pentaho pdi hello world
create db schema named pentaho0

edit pentaho pdi start up script comment out java 64bit related line，  这一行会死循环，没调查为什么，注掉。

edit generated db initial sql , replace all boolean to char(1), since the MySQL does not support boolean in lower version

admin password (2be98afc86aa7f2e4cb79ce71da9fa6d4) is admin.