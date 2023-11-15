---
title: "golang的类型转换, 强转、断言、“向上造型“"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "golang 的类型转换, 强转、断言、“向上造型“"

Golang的类型转换-三种转型(强转、断言、“向上造型“)

无数_mirage 2021-02-04 16:05:12  216  收藏
文章标签:  golang go 接口
版权
golang没有类似于java中的隐式类型转换
golang中的类型转换分为强制类型转换、类型断言、以及“向上造型”
向上造型这个词是取的Java中的定义,没有复杂的含义,表示将子类转为父类。在golang中达到同样的目的只需要.父结构体即可

package main

import "fmt"

// 隐式类型转换和强转
func t1(){
    var a float32 = 5.6
    var b int = 10
    //fmt.Println (a * b) // -- 隐式类型转换,编译报错,不支持
    fmt.Println(a * float32(b)) // -- 强转
}

type Base interface {
    hello()
}

type P interface {
    hi()
}
type S1 struct {
}

func (s1 *S1) hi() {
    fmt.Println("s1-hi")
}

func (s1 *S1) hello()  {
    fmt.Println("s1-hello")
}
type S2 struct {
}

func (s2 S2) hi() {
    fmt.Println("s2-hi")
}

type Son struct {
    S1
}

func (son *Son) hi() {
    fmt.Println("son-hi")
}

// 类型断言。注意由指针和非指针实现的方法,断言时的写法不同
// TODO .(T) 用来类型断言,返回参数1为断言之后的类型值,如果失败则是nil,参数2为是否断言成功
//         如果类型本身就是断言的类型,则断言成功,会转换成这个类型并返回
// 可以断言的情况: 
// 1.由接口断言到结构体
// 2.由父接口断言到子接口
func t2() {
    // 1.由接口断言到结构体
    var p1 P = &S1{} // 指针实现的方法hi
    p1.(*S1).hi()

    var p2 P = S2{} // 非指针实现的方法hi
    p2.(S2).hi()

    // 2.由父接口断言到子接口
    var base Base = &S1{}
    base.(P).hi()
}

// “向上造型”(java中这么叫,即转为父类)
func t3() {
    son := Son{}
    son.hi()
    // 因为golang中继承的语义是将父结构嵌入(即匿名字段)到子结构,所以只需要调用嵌入的父结构体即可
    son.S1.hi()
}
func main() {
    //t1()
    t2()
    t3()
}
————————————————
版权声明: 本文为CSDN博主「无数_mirage」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/qq_43413788/article/details/113651012