---
title: DEBIAN下切换xdm与gdm 默认进入gnome 或Xfce
author: wiloon
type: post
date: 2013-11-09T06:43:47+00:00
url: /?p=5913
categories:
  - Uncategorized

---
昨天装好了Xfce，忽然想到要装就要全套，把那个xdm也装上吧。很简单：aptitude install xdm 很快就装好了，然后出来一个对话框，选择默认的登录管理器，当然这会儿选xdm了。
  
重启（好像这个习惯不好），然后看到了xdm，那叫一个简约。登录，晕，怎么到gnome里了？
  
不知道了，问下google大神，这样，很简单的：vim ~/.xession ,输入startxfce4,保存，退出。OK。再重启，登录，直接进入Xfce了。
  
切换gdm和xdm命令：sudo dpkg-reconfigure xdm(gdm)



<http://ml0675.blog.163.com/blog/static/1714502020110311403867/>