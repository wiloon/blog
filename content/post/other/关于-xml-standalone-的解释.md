---
title: 关于 XML standalone 的解释
author: "-"
date: 2011-11-08T05:44:54+00:00
url: /?p=1462
categories:
  - Inbox
tags:
  - reprint
---
## 关于 XML standalone 的解释

  http://www.blogjava.net/javafuns/articles/257525.html

XML standalone 定义了外部定义的 DTD 文件的存在性. standalone element 有效值是 yes 和 no. 如下是一个例子:

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE s1 PUBLIC "http://www.ibm.com/example.dtd" "example.dtd">
<s1>.........</s1>

值 no 表示这个 XML 文档不是独立的而是依赖于外部所定义的一个 DTD.  值 yes 表示这个 XML 文档是自包含的(self-contained).