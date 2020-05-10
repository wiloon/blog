---
title: 'clean arch  linux'
author: wiloon
type: post
date: 2018-06-09T14:32:13+00:00
url: /?p=12288
categories:
  - Uncategorized

---
[code lang=shell]
  
sudo pacman -R $(pacman -Qtdq)

pacman -Scc
  
rm -rf ~/.cache
  
sudo pacman -S rmlint # remove duplicate file
  
sudo pacman -S ncdu
  
sudo pacman -S filelight
  
[/code]

https://www.youtube.com/watch?v=3OoMvyHYWDY