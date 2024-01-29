---
title: "c, file, open, fopen"
author: "-"
date: "2021-06-29 21:00:52" 
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "c, file, open, fopen"
## ""


fopen 是 C 标准库函数,用于处理作为流对象的文件的打开。与本质上是系统调用的 open 函数不同,fopen 将 FILE 指针对象与给定的文件相关联。它需要两个参数；第一个参数代表要打开的文件的路径名,第二个参数是打开文件的模式。

open 函数本质上是一个低级的系统服务,即使使用 fopen 也会被调用。需要注意的是,系统调用通常是用 C 库的封装函数提供给最终用户的,但其特点和性能用例与 C stio 库中的函数不同。如: open 在创建新文件时,第二个参数取类型为 int,第三个参数可选,指定文件模式位。



https://www.delftstack.com/zh/howto/c/open-vs-fopen-in-c/

