---
title: 'golang 获取interface{} 的数据类型'
author: "-"
type: post
date: 2020-02-11T05:42:52+00:00
url: /?p=15516
categories:
  - Uncategorized

---
# 'golang 获取interface{} 的数据类型'
https://blog.csdn.net/xia_xing/article/details/49423771

interface{} 可以接受任何类型的对象值
  
获取interface{}队形的数据类型，可以使用断言，或者 switch type 来实现

// Assertion project main.go
  
package main

import (
      
"fmt"
  
)

type Bag struct {
      
Key string
  
}

type Bag2 struct {
      
Key int
  
}

func main() {
      
var b1 interface{}
      
var b2 interface{}

    b1 = Bag{Key: "1"}
    b2 = Bag2{Key: 0}
    //获取interface{}中存放的数据类型
    //方法一: 
    { //判断是否是Bag类型  若不是则置0
        b, ok := b1.(Bag)
        fmt.Println("Bag类型   : ", ok, "数据", b)
    }
    { //判断是否是Bag2类型  若不是则置0
        b, ok := b2.(Bag2)
        fmt.Println("Bag2类型: ", ok, "数据", b)
    }
    //方法二: 
    switch v := b1.(type) { //v表示b1 接口转换成Bag对象的值
    case Bag:
        fmt.Println("b1.(type):", "Bag", v)
    case Bag2:
        fmt.Println("b1.(type):", "Bag2", v)
    default:
        fmt.Println("b1.(type):", "other", v)
    }
    

}
  
断言: 一般使用于已知interface中的对象的数据类型，调用后自动将接口转换成相应的对象，语法结构 接口对象(obj),存放的数据类型(string) ,v,ok := obj.(string)，若是相应的对象ok则为真，v为相应对象及数据。

switch type:  已知或者未知的对象数据类型均可，b1.(type)必须配合switch来使用，不能单独执行此语句。
  
switch v:= b1.(type){//b1为interface对象 ，v为相应对象及数据
  
case Bag: //类型为Bag时执行
  
fmt.Println("b1.(type):", "Bag", v)
  
case Bag2://类型为Bag2时执行
  
fmt.Println("b1.(type):", "Bag2", v)
  
default://类型为其他类型时执行
  
fmt.Println("b1.(type):", "other", v)
  
}
  
————————————————
  
版权声明: 本文为CSDN博主「夏星笑语」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/xia_xing/article/details/49423771