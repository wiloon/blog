---
title: 过滤字符串中的 Emoji 表情
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=6737
categories:
  - Uncategorized
tags:
  - Java

---
## 过滤字符串中的 Emoji 表情
http://doombyte.com/blog/2013/03/20/filter-emoji-emotion-in-string/

iOS 5.0之前,苹果都是采用3个字节来承接emoji表情,Java的普通char可以支持显示。但iOS 5.0之后, 苹果升级了系统自带的emoji表情输入法,用的Unicode 6标准来统一,是采用4个bytes来承接一个 emoji表情。如果不做处理的话,这种表情直接存储到MySQL5.5以下的数据库是会报错的。
