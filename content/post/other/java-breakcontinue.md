---
title: java, break/continue
author: "-"
date: 2012-07-08T08:31:15+00:00
url: /?p=3807
categories:
  - Java
tags:
  - reprint
---
## java, break/continue
使用break 退出循环 可以使用break 语句直接强行退出循环，忽略循环体中任何其他语句和循环条件测试。在循环中遇到break语句时，循环被终止，程序控制在循环后面语句重新开始。例如 如果for 循环被设计为从 0执行到99，然后输出0到99这些数字，但是当i等于10时，break语句终止程序。所以程序只会输出0到10。 在一系列嵌套循环中使用break 语句时，它将仅仅终止最里面循环。

而continue则停止执行当前的反复，然后退回循环起始和，开始新的反复。continue 用于跳过循环体中的一部分语句，也就是不执行这部分语句

return语句用来明确地从一个方法返回。也就是，return 语句使程序控制返回到调用它方法。因此，将它分类为跳转语句。尽管对return 语句详细讨论在第 7 章开始，这里对其作简要地介绍。在一个方法任何时间，return 语句可被用来使正在执行分支程序返回到调用它方法。下面例子说明这一点。下例中，由于是Java 运行系统调用main() ，因此，return语句使程序执行返回到Java 运行系统。


[http://java.chinaitlab.com/base/799194.html](http://java.chinaitlab.com/base/799194.html)