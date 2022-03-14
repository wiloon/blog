---
title: golang 包机制
author: "-"
date: 2017-03-09T00:03:22+00:00
url: /?p=9903
categories:
  - Uncategorized

tags:
  - reprint
---
## golang 包机制
http://blog.wuxu92.com/golang-package-usage/
  
我们都知道Golang中有package的概念。在go源码文件的第一行就是先声明包名: 

package main

这里的包名是一个标签,不是使用字符串。对于简答的项目可以直接使用main作为包名。

在go的开发中,我们会把所有的项目放到GOPATH/src目录下；与其他语言的项目不同,go的约定是 (当前用户) 所有的所有项目都是放到这个目录；所以这里面会有很多的项目。一般约定使用域名作为一级的目录,比如GOPATH/src/github.com这个目录存放所有从github获取的项目。

golang中的包全名是相对于GOPATH/src/的相对路径加源码文件中的package声明。源码的文件夹目录可以随意组织,可以有多层级目录,比如我打一个项目放在 GOPATH/src/wuxu.bit/example/alg/sort目录下。里面的一个源码文件sort.go如下: 

package sort

import "fmt"

func Sort(a []int) {
  
// do some sort things
  
// fmt.Println(...)
  
}

现在另外一个项目要使用这个排序方法,假设那个项目目录是GOPATH/src/wuxu/weather/目录下的main.go文件。那么要在main.go中import排序文件的包,这里要用完整的包名

package main

import (
  
sort "wuxu.bit/example/alg/sort"
  
"fmt"
  
)

func main() {
  
// can use sort.Sort here
  
}

上面使用了import包名的别名。

golang在引入包的时候还有一些tricks: 

import . "fmt" 这样在调用fmt包的导出方法时可以省略fmt
  
import _ "fmt" 这样引入该包但是不引入该包的导出函数,而是为了使用该导入操作的副作用: 调用包里面的init函数
  
golang的包机制现在还很简单,尤其还没有官方的包依赖解决方案,希望依赖解决能早日出来。