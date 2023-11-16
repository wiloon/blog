---
title: golang sleep
author: "-"
date: 2017-07-27T06:30:10+00:00
url: /?p=10934
categories:
  - Inbox
tags:
  - reprint
---
## golang sleep

[http://xiaorui.cc/2016/03/23/golang%E9%9A%8F%E6%9C%BAtime-sleep%E7%9A%84duration%E9%97%AE%E9%A2%98/](http://xiaorui.cc/2016/03/23/golang%E9%9A%8F%E6%9C%BAtime-sleep%E7%9A%84duration%E9%97%AE%E9%A2%98/)

golang随机time.sleep的Duration问题

2016-3-23 Golang rfyiamcool 5,894 views
  
碰到一个Golang time.Sleep()的问题,这golang的time.sleep的功能貌似要比python ruby都要精细些,python的等待只是time.sleep()而已,而golang可以time.Sleep(10 * time.Second) 毫秒、秒分时等不同日期来搞… 大事不干,净整些没用的…

该文章写的有些乱,欢迎来喷 ! 另外文章后续不断更新中,请到原文地址查看更新[http://xiaorui.cc/?p=3034](http://xiaorui.cc/?p=3034)

重现一下问题,用math/rannd得到10以内的随机数,然后time.sleep()等待…

num := rand.Int31n(10)
  
time.sleep(num * time.Second)
  
num := rand.Int31n(10)
  
time.sleep(num * time.Second)
  
会遇到下面的问题:

# xiaorui.cc

# command-line-arguments

./lock.go:88: invalid operation: int(DefaultTimeout) * time.Second (mismatched types int and time.Duration)
  
# xiaorui.cc

# command-line-arguments

./lock.go:88: invalid operation: int(DefaultTimeout) * time.Second (mismatched types int and time.Duration)

解决的方法:

time.Sleep(time.Duration(num) * time.Second)
  
time.Sleep(time.Duration(num) * time.Second)
  
期初原因以为是rand随机数有问题,简单看了rand的函数说明感觉没问题！ 下面是产生的原因:

func Sleep(d Duration)

Sleep pauses the current goroutine for at least the duration d. A negative or zero duration causes Sleep to return immediately.
  
func Sleep(d Duration)

Sleep pauses the current goroutine for at least the duration d. A negative or zero duration causes Sleep to return immediately.
  
int32 and time.Duration are different types. You need to convert the int32 to a time.Duration, such as time.Sleep(time.Duration(rand.Int31n(1000)) * time.Millisecond).

下面是个完整的golang随机数,然后time.sleep()的例子:

package main

import (

"fmt"

"math/rand"

"time"
  
)

func main() {

rand.Seed(time.Now().UnixNano())

for i := 0; i < 10; i++ {

x := rand.Intn(10)

fmt.Println(x)

time.Sleep(time.Duration(x) * time.Second)

}
  
}
  
package main

import (

"fmt"

"math/rand"

"time"
  
)

func main() {

rand.Seed(time.Now().UnixNano())

for i := 0; i < 10; i++ {

x := rand.Intn(10)

fmt.Println(x)

time.Sleep(time.Duration(x) * time.Second)

}
  
}
  
Golang的time.sleep虽然可以直接用数字,但不能是float浮点型.

time.Sleep(1 * time.Second) //可以
  
time.Sleep(1.1 * time.Second) //BUG
  
time.Sleep(time.Duration(yourTime) * time.Second) //可以
  
time.Sleep(1 * time.Second) //可以
  
time.Sleep(1.1 * time.Second) //BUG
  
time.Sleep(time.Duration(yourTime) * time.Second) //可以
  
提示的错误是, constant 1.1 truncated to integer 。至于原因到这里看 [https://golang.org/pkg/time/#Duration](https://golang.org/pkg/time/#Duration)

END.
