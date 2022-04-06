---
title: golang date time, 日期, 时间
author: "-"
date: 2017-07-31T01:27:35+00:00
url: /?p=10959

categories:
  - inbox
tags:
  - reprint
---
## golang date time, 日期, 时间

### 创建一个指定时间的日期对象

```go
start := time.Date(2021, 1, 7, 12, 0, 0, 0, time.Local)
```

### 比较

先把当前时间格式化成相同格式的字符串, 然后使用time的Before, After, Equal 方法即可.

```go
time1 := "2015-03-20 08:50:29"
time2 := "2015-03-21 09:04:25"
//先把时间字符串格式化成相同的时间类型
t1, err := time.Parse("2006-01-02 15:04:05", time1)
t2, err := time.Parse("2006-01-02 15:04:05", time2)
if err == nil && t1.Before(t2) {
    //处理逻辑
    fmt.Println("true")
}
```

#### duration 比较

```go
func minDuration(a, b time.Duration) time.Duration {
    if a <= b { return a }
    return b
}
```

### layout

```bash
# 时区
2006-01-02T15:04:05Z07:00
2006-01-02T15:04:05Z
Mon, 2 Jan 2006 15:04:05 MST
20060102150405.000
# 毫秒
2006-02-01 15:04:05.000
```

### unix nano > time

```go
unixnano:=int64(1570603226000000000)
t:=time.Unix(0,unixnano)
fmt.Println(t)
```

### 毫秒, get microsecond, mill second

```go
time.Now().UnixNano() / int64(time.Millisecond)
```

```go
func main() {
    fmt.Printf("时间戳 (秒) : %v;\n", time.Now().Unix())
    fmt.Printf("时间戳 (纳秒) : %v;\n",time.Now().UnixNano())
    fmt.Printf("时间戳 (毫秒) : %v;\n",time.Now().UnixNano() / 1e6)
    fmt.Printf("时间戳 (纳秒转换为秒) : %v;\n",time.Now().UnixNano() / 1e9)
}
```

### days between two dates

```go
func main() {
    // The leap year 2016 had 366 days.
    t1 := Date(2016, 1, 1)
    t2 := Date(2017, 1, 1)
    days := t2.Sub(t1).Hours() / 24
    fmt.Println(days) // 366
}

func Date(year, month, day int) time.Time {
    return time.Date(year, time.Month(month), day, 0, 0, 0, 0, time.UTC)
}
```

### date > string

```go
// 格式化日期 - RFC3339
time.Now().Format("2006-01-02T15:04:05Z07:00")
time.Now().Format("2006-01-02-15-04-05")
time.Now().Format("2006-01-02 15:04:05")
```

```go
    format:="2006-01-02 15:04:05"
    fmt.Println(time.Now().Format(format))

// 一天前
    d, _ := time.ParseDuration("-24h")
    d1 := now.Add(d)
    fmt.Println(d1)
```

### string > date

在windows下,time.Parse()的时区和time.Format()的时区是一致的。
  
但是在linux环境下,time.Parse()的默认时区是UTC,time.Format()的时区默认是本地, 使用ParseInLocation 解决时区问题

```go
tm2, _ := time.Parse("01/02/2006", "02/08/2015")
localTime, err := time.ParseInLocation("2006-01-02 15:04:05", "2017-12-03 22:01:02", time.Local)
```

### 时区

```go
 now := time.Now()
    local1, err1 := time.LoadLocation("") //等同于"UTC"
    if err1 != nil {
        fmt.Println(err1)
    }
    local2, err2 := time.LoadLocation("Local")//服务器上设置的时区
    if err2 != nil {
        fmt.Println(err2)
    }
    local3, err3 := time.LoadLocation("America/Los_Angeles")
    if err3 != nil {
        fmt.Println(err3)
    }

    fmt.Println(now.In(local1))
    fmt.Println(now.In(local2))
    fmt.Println(now.In(local3))
    //output:
    //2016-12-04 07:39:06.270473069 +0000 UTC
    //2016-12-04 15:39:06.270473069 +0800 CST
    //2016-12-03 23:39:06.270473069 -0800 PST
```

### 时间计算

```go
h, _ := time.ParseDuration("-1h")
start := time.Now().Add(h)
```

https://github.com/jemygraw/TechDoc/blob/master/Go%E7%A4%BA%E4%BE%8B%E5%AD%A6/Go%20%E6%97%B6%E9%97%B4%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%92%8C%E8%A7%A3%E6%9E%90.markdown

Go 时间格式化和解析

Go使用模式匹配的方式来支持日期格式化和解析。

package main

import "fmt"
  
import "time"

func main() {

p := fmt.Println

    // Format 函数使用一种基于示例的模式匹配方式,
    // 它使用已经格式化的时间模式来决定所给定参数
    // 的输出格式
    p(t.Format("3:04PM"))
    p(t.Format("Mon Jan _2 15:04:05 2006"))
    p(t.Format("2006-01-02T15:04:05.999999-07:00"))
    
    // 对于纯数字表示的时间来讲,你也可以使用标准
    // 的格式化字符串的方式来格式化时间
    fmt.Printf("%d-%02d-%02dT%02d:%02d:%02d-00:00\n",
        t.Year(), t.Month(), t.Day(),
        t.Hour(), t.Minute(), t.Second())
    
    // 时间解析也是采用一样的基于示例的方式
    withNanos := "2006-01-02T15:04:05.999999999-07:00"
    t1, e := time.Parse(
        withNanos,
        "2012-11-01T22:08:41.117442+00:00")
    p(t1)
    kitchen := "3:04PM"
    t2, e := time.Parse(kitchen, "8:41PM")
    p(t2)
    
    // Parse将返回一个错误,如果所输入的时间格式不对的话
    ansic := "Mon Jan _2 15:04:05 2006"
    _, e = time.Parse(ansic, "8:41PM")
    p(e)
    
    // 你可以使用一些预定义的格式来格式化或解析时间
    p(t.Format(time.Kitchen))

}
  
运行结果

2014-03-03T22:39:31+08:00
  
10:39PM
  
Mon Mar 3 22:39:31 2014
  
2014-03-03T22:39:31.647077+08:00
  
2014-03-03T22:39:31-00:00
  
2012-11-01 22:08:41.117442 +0000 +0000
  
0000-01-01 20:41:00 +0000 UTC
  
parsing time "8:41PM" as "Mon Jan _2 15:04:05 2006": cannot parse "8:41PM" as "Mon"
  
10:39PM

### 字符串毫秒转时间格式

```go
package main

import (
    "fmt"
    "strconv"
    "time"
)

func main() {
    fmt.Println(msToTime("1489582166978"))
}

func msToTime(ms string) (time.Time, error) {
    msInt, err := strconv.ParseInt(ms, 10, 64)
    if err != nil {
        return time.Time{}, err
    }

    tm := time.Unix(0, msInt*int64(time.Millisecond))

    fmt.Println(tm.Format("2006-02-01 15:04:05.000"))

    return tm, nil
}

```

### RFC3339

RFC3339 比 ISO 8601 有一个很一个明显的限制,这里提一下: ISO允许24点,而 RFC3339 为了减少混淆,限制小时必须在0至23之间。23:59过1分钟,是第二天的0:00。
标准时间
本地时间只包括当前的时间,不包含任何时区信息。同一时刻,东八区的本地时间比零时区的本地时间快了8个小时。在不同时区之间交换时间数据,除了用纯数字的时间戳,还有一种更方便人类阅读的表示方式: 标准时间的偏移量表示方法。

RFC3339详细定义了互联网上日期/时间的偏移量表示:

2017-12-08T00:00:00.00Z
这个代表了UTC时间的2017年12月08日零时

2017-12-08T00:08:00.00+08:00
这个代表了同一时刻的,东八区北京时间 (CST) 表示的方法

上面两个时间的时间戳是等价的。两个的区别,就是在本地时间后面增加了时区信息。Z表示零时区。+08:00表示UTC时间增加8小时。

这种表示方式容易让人疑惑的点是从标准时间换算UTC时间。以CST转换UTC为例,没有看文档的情况下,根据 +08:00 的结尾,很容易根据直觉在本地时间再加上8小时。正确的计算方法是本地时间减去多增加的8小时。+08:00减去8小时才是UTC时间,-08:00加上8小时才是UTC时间。

https://blog.csdn.net/CodyGuo/article/details/53009451
  
https://www.kancloud.cn/itfanr/go-by-example/81698
  
https://yourbasic.org/golang/days-between-dates/
  
https://programming.guide/go/format-parse-string-time-date-example.html
  
https://www.jianshu.com/p/92d9344425a7

https://zhuanlan.zhihu.com/p/31829454
