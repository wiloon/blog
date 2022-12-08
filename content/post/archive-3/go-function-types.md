---
title: golang, function types, 函数类型
author: "-"
date: '2019-07-26T02:27:23+00:00'
url: go/function/types
categories:
  - Go
tags:
  - reprint
---
## golang, function types, 函数类型

### function types

A function type denotes the set of all functions with the same parameter and result types.

### 示例

```go
package main

import "fmt"

// function types
type Greeting func(name string) string

func say(g Greeting, n string) {
    fmt.Println(g(n))
}

func english(name string) string {
    return "Hello, " + name
}

func main() {
    say(english, "World")
}
```

输出Hello, World

say()函数要求传入一个Greeting类型，因为english函数的参数和返回值跟Greeting一样，参考接口的概念这里可以做类型转换。我们换个方式来实现上面的功能:

```go
package main

import "fmt"

// Greeting function types
type Greeting func(name string) string

func (g Greeting) say(n string) {
    fmt.Println(g(n))
}

func english(name string) string {
    return "Hello, " + name
}

func main() {
    g := Greeting(english)
    g.say("World")
}
```

同样输出Hello, World，只是给Greeting类型添加了say()方法。上面说了，函数类型是表示所有包含相同参数和返回类型的函数集合。我们在一开始先把func(name string) string这样的函数声明成Greeting类型，接着我们通过Greeting(english)将english函数转换成Greeting类型。通过这个转换以后，我们就可以借由变量g调用Greeting类型的say()方法。两段代码的差异就是go的类型系统添加方法和类C++语言添加类型方法的差异，具体讲解可以去查看《Go语言编程》第3章为类型添加方法这一节。

既然是函数集合，那么只有一个函数显然是不足以说明问题的。

```go
package main

import "fmt"

// Greeting function types
type Greeting func(name string) string

func (g Greeting) say(n string) {
    fmt.Println(g(n))
}

func english(name string) string {
    return "Hello, " + name
}

func french(name string) string {
    return "Bonjour, " + name
}

func main() {
    g := Greeting(english)
    g.say("World")
    g = Greeting(french)
    g.say("World")
}
```

输出

Hello, World
  
Bonjour, World
  
在其他语言里面，有些函数可以直接作为参数传递，有些是以函数指针进行传递，但是都没有办法像go这样可以给函数类型"增加"新方法。

回到Go: net/http的HandlerFunc类型，只要Martini的函数遵循文档中type HandlerFunc func(ResponseWriter, *Request)的要求，就可以转换成HandlerFunc类型，也就可以调用func (HandlerFunc)ServeHTTP函数。

---

<https://www.jianshu.com/p/fc4902159cf5>
