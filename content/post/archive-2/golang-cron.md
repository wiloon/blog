---
title: golang cron
author: "-"
date: 2018-03-16T05:57:12+00:00
url: /?p=11990

categories:
  - inbox
tags:
  - reprint
---
## golang cron
https://www.jianshu.com/p/626acb9549b1

cron 表达式的基本格式
  
用过 linux 的应该对 cron 有所了解。linux 中可以通过 crontab -e 来配置定时任务。不过,linux 中的 cron 只能精确到分钟。而我们这里要讨论的 Go 实现的 cron 可以精确到秒,除了这点比较大的区别外,cron 表达式的基本语法是类似的。 (如果使用过 Java 中的 Quartz,对 cron 表达式应该比较了解,而且它和这里我们将要讨论的 Go 版 cron 很像,也都精确到秒) 

cron(计划任务),顾名思义,按照约定的时间,定时的执行特定的任务 (job) 。cron 表达式 表达了这种约定。

cron 表达式代表了一个时间集合,使用 6 个空格分隔的字段表示。
  
字段名 是否必须 允许的值 允许的特定字符
  
秒(Seconds) 是 0-59 * / , -
  
分(Minutes) 是 0-59 * / , -
  
时(Hours) 是 0-23 * / , -
  
日(Day of month) 是 1-31 * / , – ?
  
月(Month) 是 1-12 or JAN-DEC * / , -
  
星期(Day of week) 否 0-6 or SUM-SAT * / , – ?
  
注: 
  
1) 月(Month)和星期(Day of week)字段的值不区分大小写,如: SUN、Sun 和 sun 是一样的。
  
2) 星期 (Day of week)字段如果没提供,相当于是 *
  
2. 特殊字符说明
  
1) 星号(*)
  
表示 cron 表达式能匹配该字段的所有值。如在第5个字段使用星号(month),表示每个月

2) 斜线(/)
  
表示增长间隔,如第1个字段(minutes) 值是 3-59/15,表示每小时的第3分钟开始执行一次,之后每隔 15 分钟执行一次 (即 3、18、33、48 这些时间点执行) ,这里也可以表示为: 3/15

3) 逗号(,)
  
用于枚举值,如第6个字段值是 MON,WED,FRI,表示 星期一、三、五 执行

4) 连字号(-)
  
表示一个范围,如第3个字段的值为 9-17 表示 9am 到 5pm 直接每个小时 (包括9和17) 

5) 问号(?)
  
只用于日(Day of month)和星期(Day of week),\表示不指定值,可以用于代替 *
  
3. 示例
  
最简单crontab任务
  
package main

import (
      
"github.com/robfig/cron"
      
"log"
  
)

func main() {
      
i := 0
      
c := cron.New()
      
spec := "*/5 \* \* \* * ?"
      
c.AddFunc(spec, func() {
          
i++
          
log.Println("cron running:", i)
      
})
      
c.Start()

    select{}
    

}
  
启动后输出如下: 

2017/07/06 18:28:30 cron running: 1
  
2017/07/06 18:28:35 cron running: 2
  
2017/07/06 18:28:40 cron running: 3
  
2017/07/06 18:28:45 cron running: 4
  
2017/07/06 18:28:50 cron running: 5
  
...
  
多个定时crontab任务
  
package main

import (
      
"github.com/robfig/cron"
      
"log"
      
"fmt"
  
)

type TestJob struct {
  
}

func (this TestJob)Run() {
      
fmt.Println("testJob1...")
  
}

type Test2Job struct {
  
}

func (this Test2Job)Run() {
      
fmt.Println("testJob2...")
  
}

//启动多个任务
  
func main() {
      
i := 0
      
c := cron.New()

    //AddFunc
    spec := "*/5 * * * * ?"
    c.AddFunc(spec, func() {
        i++
        log.Println("cron running:", i)
    })
    
    //AddJob方法
    c.AddJob(spec, TestJob{})
    c.AddJob(spec, Test2Job{})
    
    //启动计划任务
    c.Start()
    
    //关闭着计划任务, 但是不能关闭已经在执行中的任务.
    defer c.Stop()
    
    select{}
    

}
  
go run crontab/crontab-2.go
  
启动后输出如下: 
  
testJob1...
  
2017/07/07 18:46:40 cron running: 1
  
testJob2...
  
2017/07/07 18:46:45 cron running: 2
  
testJob1...
  
testJob2...
  
2017/07/07 18:46:50 cron running: 3
  
testJob1...
  
testJob2...
  
2017/07/07 18:46:55 cron running: 4
  
testJob1...
  
testJob2...
  
testJob2...
  
testJob1...
  
2017/07/07 18:47:00 cron running: 5
  
...
  
可结合toml yaml 配置需要定时执行的任务
  
...
  
参考
  
http://ju.outofmemory.cn/entry/65356

作者: 水滴穿石
  
链接: https://www.jianshu.com/p/626acb9549b1
  
來源: 简书
  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。