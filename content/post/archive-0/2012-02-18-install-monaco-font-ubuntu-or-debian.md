---
title: Install Monaco font Ubuntu (or Debian)
author: wiloon
type: post
date: 2012-02-18T10:56:44+00:00
url: /?p=2345
categories:
  - Font

---
[shell]
  
sudo mkdir /usr/share/fonts/truetype/custom
  
sudo mv Monaco_Linux.ttf /usr/share/ts/truetype/custom/
  
sudo fc-cache -f -v
  
[/shell]