---
title: python 遍历目录
author: "-"
date: 2012-11-17T08:01:00+00:00
url: /?p=4707
categories:
  - Development

---
## python 遍历目录
<http://www.cnblogs.com/vivilisa/archive/2009/03/01/1400968.html>

<http://laocao.blog.51cto.com/480714/525140>

[python]

#!/usr/bin/python
  
import os,sys
  
dir = '/home/wiloon/tmp'
  
list = os.listdir(dir)
  
print list

for line in list:
   
path = os.path.join(dir, line)
   
print path

[/python]