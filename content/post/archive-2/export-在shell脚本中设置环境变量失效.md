---
title: export 在shell脚本中设置环境变量失效
author: "-"
date: 2017-12-20T09:04:09+00:00
url: /?p=11646
categories:
  - Uncategorized

tags:
  - reprint
---
## export 在shell 脚本中设置环境变量失效 placeholder
shell 脚本中设定的路径和环境变量只对改shell和其子shell有效。 对其父shell和其它shell无效。

解决方法: 

source filename.sh

http://blog.csdn.net/nemo2011/article/details/8472326