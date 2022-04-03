---
title: VIM 列编辑
author: "-"
date: 2018-12-25T01:58:57+00:00
url: /?p=13209
categories:
  - Uncategorized

tags:
  - reprint
---
## VIM 列编辑
VIM的列编辑操作

### 插入列
插入操作的话知识稍有区别。例如我们在每一行前都插入"() ": 

1. 光标定位到要操作的地方。
2. CTRL+v 进入"可视块" 模式, 选取这一列操作多少行。
3. SHIFT+i(I) 输入要插入的内容。
4. ESC 按两次, 会在每行的选定的区域出现插入的内容。

### 删除列
1. 光标定位到要操作的地方。
2. CTRL+v 进入"可视 块"模式,选取这一列操作多少行。
3. d 删除。
4. 

>https://www.cnblogs.com/xiaowant/articles/1992923.html