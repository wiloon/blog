---
title: shell 判断文件存在
author: "-"
date: 2011-05-01T07:10:06+00:00
url: /?p=164
categories:
  - shell
tags:
  - reprint
---
## shell 判断文件存在
myPath="/var/log/httpd/"
  
myFile="/var /log/httpd/access.log"

# -d 参数判断$myPath是否存在
  
if [ ! -d "$myPath"]; then
  
mkdir "$myPath"
  
fi

# -f 参数判断$myFile是否存在
  
if [ ! -f "$myFile" ]; then
  
touch "$myFile"
  
fi

"[" 后面要有空格
  
"]"前面要有空格
  
另外使用变量时，如: 
  
mv $myFile $...
  
myFile 路径中不能有"~"

@_@