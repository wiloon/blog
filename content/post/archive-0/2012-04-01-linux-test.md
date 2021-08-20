---
title: linux test
author: "-"
type: post
date: 2012-04-01T09:10:06+00:00
url: /?p=2717
categories:
  - Linux

---
<http://www.ibm.com/developerworks/cn/linux/l-bash-test.html>

内置命令 `test` 根据表达式_expr_ 求值的结果返回 0（真）或 1（假）。也可以使用方括号：`test  expr `和 [ _expr_ ] 是等价的。 可以用`$?` 检查返回值；可以使用 && 和 || 操作返回值；也可以用本技巧后面介绍的各种条件结构测试返回值。

<table summary="" width="50%" border="0" cellspacing="0" cellpadding="0">
  <tr valign="top">
    
      -d
    
    
    
      目录
    
  
  
  <tr valign="top">
    
      -e
    
    
    
      存在（也可以用 -a）
    
  
  
  <tr valign="top">
    
      -f
    
    
    
      普通文件
    
  
  
  <tr valign="top">
    
      -h
    
    
    
      符号连接（也可以用 -L）
    
  
  
  <tr valign="top">
    
      -p
    
    
    
      命名管道
    
  
  
  <tr valign="top">
    
      -r
    
    
    
      可读
    
  
  
  <tr valign="top">
    
      -s
    
    
    
      非空
    
  
  
  <tr valign="top">
    
      -S
    
    
    
      套接字
    
  
  
  <tr valign="top">
    
      -w
    
    
    
      可写
    
  
  
  <tr valign="top">
    
      -N
    
    
    
      从上次读取之后已经做过修改
    
  



可以用 `-eq`、 -`ne`、`-lt`、 -`le`、 -`gt` 或 -`ge` 比较算术值，它们分别表示等于、不等于、小于、小于等于、大于、大于等于。