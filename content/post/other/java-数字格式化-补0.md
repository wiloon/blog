---
title: java 数字格式化 补0
author: "-"
date: 2012-06-26T09:22:33+00:00
url: /?p=3674
categories:
  - Java
tags:
  - reprint
---
## java 数字格式化 补0
DecimalFormat df = new DecimalFormat("0000000");
  
System.out.println(df.format(1));

output: 0000001