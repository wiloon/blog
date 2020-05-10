---
title: The Go Programming Language
author: wiloon
type: post
date: 2016-03-04T04:53:20+00:00
url: /?p=8776
categories:
  - Uncategorized
tags:
  - Golang

---
Go 语言虽然是静态编译型语言，但是它却拥有脚本化的语法，支持多种编程范式(函数式和面向对象)。

### hello world

<pre><code class="language-go line-numbers">package main
import "fmt"
func main() {
fmt.Println("hello world")
}
</code></pre>

<pre><code class="language-bash line-numbers">go run hello-world.go
go build hello-world.go
./hello-world
</code></pre>

http://studygolang.com/articles/1941
  
https://gobyexample.com/hello-world