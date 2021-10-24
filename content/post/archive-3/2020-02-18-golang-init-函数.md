---
title: golang init 函数
author: "-"
type: post
date: 2020-02-18T05:01:48+00:00
url: /?p=15590
categories:
  - Uncategorized

---
## golang init 函数
init函数的作用: 

变量初始化
  
检查和修复程序状态
  
运行前注册，例如decoder，parser的注册
  
运行只需计算一次的模块，像sync.once的作用
  
其他

golang程序初始化先于main函数执行，由runtime进行初始化，初始化顺序如下: 

初始化导入的包（包的初始化顺序并不是按导入顺序（"从上到下") 执行的，runtime需要解析包依赖关系，没有依赖的包最先初始化，与变量初始化依赖关系类似，参见golang变量的初始化) ；
  
初始化包作用域的变量（该作用域的变量的初始化也并非按照"从上到下、从左到右"的顺序，runtime解析变量依赖关系，没有依赖的变量最先初始化，参见golang变量的初始化) ；
  
执行包的init函数；