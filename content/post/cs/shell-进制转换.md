---
title: shell 进制转换
author: "-"
date: 2020-03-24T02:21:01+00:00
url: /?p=15812
categories:
  - shell
tags:
  - reprint
  - shell


---
## shell 进制转换
## 16进制转换成10进制
  
```bash
printf %d 0xF
echo $((16#F))
```
 
## 10进制转换成16进制
  
```bash
printf %x 15
echo "obase=16;15"|bc
```

三、10进制转换成8进制
  
printf %o 9
  
11

四、8进制转换成10进制
  
echo $((8#11))
  
9

五、同理二进制转换成10进制
  
echo $((2#111))
  
7

六、10进制转换成二进制
  
echo "obase=2;15"|bc
  
1111
  
https://blog.csdn.net/rheostat/article/details/8057405