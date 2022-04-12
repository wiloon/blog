---
title: kde idea 图标消失
author: "-"
date: 2019-02-20T05:39:48+00:00
url: /?p=13648
categories:
  - Uncategorized

tags:
  - reprint
---
## kde idea 图标消失

Open folder /home/USERNAME/.local/share/applications/
  
Find jetbrains-idea.desktop.
  
Right mouse click on it, then select Properties
  
Open Application tab
  
Next to the Command section click Browse... button and select idea.sh file in /pathToIntelliJ/bin folder. (In my case the path was already correct, but it seems that selection the file again rewrite something and Icon works ok now).
  
Click OK.

<https://stackoverflow.com/questions/43706663/intellij-idea-lost-icon-after-launch>
