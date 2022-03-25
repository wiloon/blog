---
title: golang 位运算
author: "-"
date: 2019-11-06T03:02:17+00:00
url: /?p=15113
categories:
  - Uncategorized

tags:
  - reprint
---
## golang 位运算

```bash
&      位运算 AND
|      位运算 OR
^      位运算 XOR
&^     位清空 (AND NOT)
<<     左移
>>     右移
```

### 无符号右移
<https://blog.wiloon.com/?p=15522>

### & 操作符

假设给定数值 a，b
只有满足 a = b = 1 的情况下下
  
AND(a,b) = 1，否则为 0
  
所以AND的另外一个很好的效果是可以用于把一个整数进行清零。

```go

func main() {
    var x uint8 = 0xAC    // x = 10101100
    x = x & 0xF0          // x = 10100000
}
```

### | 操作符, OR
| 操作符对整数部分执行OR操作。回顾一下OR操作符的属性: 
给定数值 a, b
当 a = 1 或者 b = 1
OR(a,b) = 1
否则为 0
我们可以对一个给定的整数选择性地使用OR操作符设置各个位的值。例如，在下面的例子中，我们使用OR运算符 (从最低位到最高位 (MSB) ) 将第3位，第7位和第8位设置为1。

```go
 func main() {
    var a uint8 = 0
    a |= 196
    fmt.Printf("%b", a)
}
// prints 11000100
```

当我们使用位掩码的手段为给定的整数值设置任意位时，使用OR是非常有用的，例如: 
```go
 func main() {
    var a uint8 = 0
    a |= 196
    a |= 3
    fmt.Printf("%b", a)
}
// prints 11000111
```
https://lihaoquan.me/2018/1/1/bit-operator.html