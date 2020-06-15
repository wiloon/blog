---
title: chmod
author: wiloon
type: post
date: 2011-04-24T08:34:50+00:00
url: /?p=119
views:
  - 1
bot_views:
  - 5
categories:
  - Linux

---
```bash
chmod a+x 1.sh
chmod og+rwx 1.sh
```

格式: \[ugoa&#8230;\]\[+-=\]\[rwxX&#8230;\]\[,&#8230;\]
  
u 拥有者
  
g 与拥有者同组的
  
o 其它用户
  
a 三者都是

chmod -R a+rw folderName

-R 对目录下和所有文件和子目录进行相同的权限变更