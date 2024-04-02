---
title: golang 类/type
author: "-"
date: 2017-02-17T01:22:13+00:00
url: /?p=9825
categories:
  - Inbox
tags:
  - reprint
---
## golang 类/type
```java
  
//类定义
  
type Mutex struct {
        
state int32
        
sema uint32
    
}

//扩展已定义类型
   
type Num int32
      
func (num Num) IsBigger(otherNum Num) bool {
          
return num > otherNum
      
}

//类方法
  
type Once struct {
      
m Mutex
      
done uint32
  
}

func (o *Once) Do(f func()) {
      
if atomic.LoadUint32(&o.done) == 1 {
          
return
      
}
      
// Slow-path.
      
o.m.Lock()
      
defer o.m.Unlock()
      
if o.done == 0 {
          
defer atomic.StoreUint32(&o.done, 1)
          
f()
      
}
  
}

```

类声明
  
type Poem struct {
      
Title string
      
Author string
      
intro string
  
}
  
这样就声明了一个类,其中没有public、protected、private的的声明。golang用另外一种做法来实现属性的访问权限: 属性的开头字母是大写的则在其它包中可以被访问,否则只能在本包中访问。类的声明和方法亦是如此。

类方法声明
  
func (poem *Poem) publish() {
      
fmt.Println("poem publish")
  
}
  
或者
  
func (poem Poem) publish() {
      
fmt.Println("poem publish")
  
}

实例化对象
  
实例化对象有好几种方式
  
poem := &Poem{}
  
poem.Author = "Heine"
  
poem2 := &Poem{Author: "Heine"}
  
poem3 := new(Poem)
  
poem3.Author = "Heine"
  
poem4 := Poem{}
  
poem4.Author = "Heine"
  
poem5 := Poem{Author: "Heine"}

http://kangkona.github.io/oo-in-golang
  
http://www.01happy.com/golang-oop/
  
https://code.tutsplus.com/zh-hans/tutorials/lets-go-object-oriented-programming-in-golang-cms-26540
  
http://hackthology.com/golangzhong-de-mian-xiang-dui-xiang-ji-cheng.html
  
http://hackthology.com/golangzhong-de-mian-xiang-dui-xiang-ji-cheng.html