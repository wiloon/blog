---
title: IEEE754
author: "-"
date: 2011-07-02T13:08:01+00:00
url: /?p=263
categories:
  - inbox
tags:
  - reprint
---
## IEEE754
IEEE754代码
  
标准表示法
  
为便于软件的移植，浮点数的表示格式应该有统一标准 (定义) 。1985年IEEE (Institute of Electrical and Electronics Engineers) 提出了IEEE754标准。该标准规定基数为2，阶码E用移码表示，尾数M用原码表示，根据原码的规格化方法，最高数字位总是1，该标准将这个1缺省存储，使得尾数表示范围比实际存储的多一位。

类型 存储位数

偏移值

数符(s) 阶码(E) 尾数(M) 总位数 十六进制 十进制
  
短实数(Single,Float) 1位 8位 23位 32位 0x7FH +127
  
长实数(Double) 1位 11 位 52位 64位 0x3FFH +1023
  
临时实数(延伸双精确度,不常用) 1位 15位 64位 80位 0x3FFFH +16383