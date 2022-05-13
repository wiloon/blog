---
title: golang log
author: "-"
date: 2012-01-08T08:02:25+00:00
url: /?p=2118
categories:
  - Java
  - Web
tags:
  - reprint
---
## golang log

seelog
  
<https://github.com/cihub/seelog>

log, glog, logrus

<https://sites.google.com/site/kjellhedstrom2/g2log-efficient-background-io-processign-with-c11/g2log-vs-google-s-glog-performance-comparison>
  
<https://logmatic.io/blog/our-guide-to-a-golang-logs-world/>
  
<https://www.goinggo.net/2013/11/using-log-package-in-go.html>
  
<http://legendtkl.com/2016/03/11/go-log/>

log
  
首先是golang自带的package log。使用godoc查看，godoc -http=:8001，然后就可以在localhost:8001/pkg/log就可以查看了。

最重要的是SetOutput这个函数，原型是func SetOutput(w io.Writer),决定了log应该输出到什么地方，默认是标准输出。下面是把log输出到文件的一个简单代码示例。

package main

import (

"log"

"os"
  
)

func main() {

f, err := os.OpenFile("logfile.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)

if err != nil {

log.Fatalf("file open error : %v", err)

}

defer f.Close()

log.SetOutput(f)

log.Println("This is a test log entry")
  
}
  
我们此时打开文件logfile.log，会看到文件内容如下。

2016/03/11 17:54:10 This is a test log entry
  
有时候我们并不需要前面的日期以及时间信息，比如做自动化测试的时候比对log肯定不希望有时间信息。那应该怎么办呢？这时候就该SetFlags()出场了。

package main

import (

"log"

"os"
  
)

func main() {

f, err := os.OpenFile("logfile.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)

if err != nil {

log.Fatalf("file open error : %v", err)

}

defer f.Close()

log.SetOutput(f)

log.SetFlags(0)

log.Println("This is a test log entry")
  
}
  
SetFlags(flag int)函数可以用来自定义log的输出格式，flag可选如下任意个标志的或操作的组合。

const (

Ldate = 1 << iota // the date: 2009/01/23

Ltime // the time: 01:23:23

Lmicroseconds // microsecond resolution: 01:23:23.123123. assumes Ltime.

Llongfile // full file name and line number: /a/b/c/d.go:23

Lshortfile // final file name element and line number: d.go:23. overrides Llongfile

LstdFlags = Ldate | Ltime // initial values for the standard logger
  
)
  
iota的语法就不细说了，这里Ldate，Ltime，Lmicroseconds分别表示右起第一二三位。

自定义log形式还可以使用SetPrefix(prefix string)可以在我们的log最前面添加特定的prefix。除此之外剩下的API，比如Fatal，Fatalf，Panic等都相当于先输出log，然后调用Exit()或者panic函数。

logger
  
logger是log的一个简单封装，使用logger可以使记log更加的便捷。一个简单的示例如下。

package main

import (

"log"

"os"
  
)

func main() {

logger := log.New(os.Stdout, "DEBUG", log.Ldata | log.Ltime)

logger.Println("This is a DEBUG LOG")
  
}
  
运行上述go程序，将在终端得到如下结果:

DEBUG: 2016/03/11 22:21:19 This is a DEBUG LOG
  
我们简单看一下log.New()函数原型。

func New(out io.Writer, prefix string, flag int) *Logger
  
os.Stdout表示标准输出，如果你想记录到文件中，将os.Open()或者os.OpenFile()的返回值传入即可。"DEBUG"即为每条log的前缀，最后的flag就为上述的flag。相比于上面的代码片段，下面的代码更加的实用。

package main

import (

"io"

"io/ioutil"

"log"

"os"
  
)

var (

Info *log.Logger

Warning *log.Logger

Error *log.Logger
  
)

func Init(

infoHandle io.Writer,

warningHandle io.Writer,

errorHandle io.Writer) {

    Info = log.New(infoHandle,
        "INFO: ",
        log.Ldate|log.Ltime|log.Lshortfile)
    
    Warning = log.New(warningHandle,
        "WARNING: ",
        log.Ldate|log.Ltime|log.Lshortfile)
    
    Error = log.New(errorHandle,
        "ERROR: ",
        log.Ldate|log.Ltime|log.Lshortfile)

}

func main() {

Init(ioutil.Discard, os.Stdout, os.Stdout, os.Stderr)

    Info.Println("Special Information")
    Warning.Println("There is something you need to know about")
    Error.Println("Something has failed")

}
