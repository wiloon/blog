---
title: golang JSON
author: "-"
date: 2012-04-25T08:50:44+00:00
url: go/json
categories:
  - Go
tags:
  - reprint
---
## golang JSON

## go json string 格式化

```bash
var str bytes.Buffer
_ = json.Indent(&str, []byte(data), "", "    ")
fmt.Println("formated: ", str.String())
```

### time.Time 序列化

<https://www.cnblogs.com/chenqionghe/p/13409556.html>

```go
json.Marshal(struct {
    *User
    Password bool `json:"password,omitempty"`
}{
    User: user,
})
```

```go
json.Marshal()
// 序列化 + 格式化
resp2, _ := json.MarshalIndent(s, "", "    ")
json.Unmarshal()
```

### struct json tag

<https://colobu.com/2017/06/21/json-tricks-in-Go/>

```go
type Result struct {
    Count      int       `json:"count"`
    Data       MyStruct  `json:"data,omitempty"`
}

func main() {
    out := shellExec(shell)
    var result Result
    json.Unmarshal([]byte(out), &result)
    fmt.Println(result.Count)
}

```

### gjson

<https://github.com/tidwall/gjson>

<http://www.cnblogs.com/fengbohello/p/4665883.html>

本文介绍如何使用 Go 语言自带的库把对象转换为JSON格式，并在channel中进行传输后，并把JSON格式的信息转换回对象。

1. Go 语言的 JSON 库
  
Go语言自带的JSON转换库为 encoding/json
  
1.1) 其中把对象转换为JSON的方法 (函数) 为 json.Marshal()，其函数原型如下
  
func Marshal(v interface{}) ([]byte, error)

也就是说，这个函数接收任意类型的数据 v，并转换为字节数组类型，返回值就是我们想要的JSON数据和一个错误代码。当转换成功的时候，这个错误代码为nil

在进行对象转换为 JSON 的过程中，会遵循如下几条规则:

• 布尔型转换为 JSON 后仍是布尔型， 如true -> true

• 浮点型和整数型转换后为JSON里面的常规数字，如 1.23 -> 1.23

• 字符串将以UTF-8编码转化输出为Unicode字符集的字符串，特殊字符比如<将会被转义为\u003c

• 数组和切片被转换为JSON 里面的数组，[]byte类会被转换为base64编码后的字符串，slice的零值被转换为null

• 结构体会转化为JSON对象，并且只有结构体里边以大写字母开头的可被导出的字段才会被转化输出，而这些可导出的字段会作为JSON对象的字符串索引

• 转化一个map 类型的数据结构时，该数据的类型必须是 map[string]T (T 可以是encoding/json 包支持的任意数据类型)

1.2) 把 JSON 转换回对象的方法 (函数) 为 json.Unmarshal()，其函数原型如下

func Unmarshal(data [] byte, v interface{}) error

这个函数会把传入的 data 作为一个JSON来进行解析，解析后的数据存储在参数 v 中。这个参数 v 也是任意类型的参数 (但一定是一个类型的指针) ，原因是我们在是以此函数进行JSON 解析的时候，这个函数不知道这个传入参数的具体类型，所以它需要接收所有的类型。

那么，在进行解析的时候，如果JSON 和 对象的结构不对口会发生什么呢，这就需要解析函数json.Unmarshal()遵循以下规则

• json.Unmarshal() 函数会根据一个约定的顺序查找目标结构中的字段，如果找到一个即发生匹配。那什么是找到了呢？关于"找到了"又有如下的规则: 假设一个JSON对象有个名为"Foo"的索引，要将"Foo"所对应的值填充到目标结构体的目标字段上，json.Unmarshal() 将会遵循如下顺序进行查找匹配

§ 一个包含Foo 标签的字段

§ 一个名为Foo 的字段

§ 一个名为Foo 或者Foo 或者除了首字母其他字母不区分大小写的名为Foo 的字段。 这些字段在类型声明中必须都是以大写字母开头、可被导出的字段。

注意: 如果JSON中的字段在Go目标类型中不存在，json.Unmarshal() 函数在解码过程中会丢弃该字段。

• 当JSON 的结构是未知的时候，会遵循如下规则:

§ JSON中的布尔值将会转换为Go中的bool类型

§ 数值会被转换为Go中的float64类型

§ 字符串转换后还是string类型

§ JSON数组会转换为[]interface{} 类型

§ JSON对象会转换为map[string]interface{}类型

§ null值会转换为nil

注意: 在Go的标准库encoding/json包中，允许使用map[string]interface{}和[]interface{} 类型的值来分别存放未知结构的JSON对象或数组

代码实例

假设我们有如下一个类 (结构体) student 及其一个实例对象st:

复制代码
  
type Student struct {

Name string

Age int

Guake bool

Classes []string

Price float32
  
}

st := &Student {

"Xiao Ming",

16,

true,

[]string{"Math", "English", "Chinese"},

9.99,
  
}

现在我们需要把这个类的一个对象转换为JSON格式，并且传输给远方的朋友，那么我们就可以这么做:

b, err := json.Marshal(st)
  
这样就转换好了。是不是很简单！转换回来就更简单了，比如我们有一个新的student对象，就叫stb，那么我们可以这样转换回来:

stb := &Student{}
  
err = json.Unmarshal([]byte(strData), &stb)
  
这样就转换回来了，是不是很简单！

下面是完整代码及运行结果:

$ cat gojson.go

复制代码

1 package main

2

3 import (

4 "fmt"

5 "encoding/json"

6 )

7

8 type Student struct {

9 Name string
  
10 Age int
  
11 Guake bool
  
12 Classes []string
  
13 Price float32
  
14 }
  
16 func (s * Student)ShowStu() {
  
17 fmt.Println("show Student :")
  
18 fmt.Println("\tName\t:", s.Name)
  
19 fmt.Println("\tAge\t:", s.Age)
  
20 fmt.Println("\tGuake\t:", s.Guake)
  
21 fmt.Println("\tPrice\t:", s.Price)
  
22 fmt.Printf("\tClasses\t: ")
  
23 for _, a := range s.Classes {
  
24 fmt.Printf("%s ", a)
  
25 }
  
26 fmt.Println("")
  
27 }
  
29 func main() {
  
30 st := &Student {
  
31 "Xiao Ming",
  
32 16,
  
33 true,
  
34 []string{"Math", "English", "Chinese"},
  
35 9.99,
  
36 }
  
37 fmt.Println("before JSON encoding :")
  
38 st.ShowStu()
  
40 b, err := json.Marshal(st)
  
41 if err != nil {
  
42 fmt.Println("encoding faild")
  
43 } else {
  
44 fmt.Println("encoded data : ")
  
45 fmt.Println(b)
  
46 fmt.Println(string(b))
  
47 }
  
48 ch := make(chan string, 1)
  
49 go func(c chan string, str string){
  
50 c <- str
  
51 }(ch, string(b))
  
52 strData := <-ch
  
53 fmt.Println("-----------")
  
54 stb := &Student{}
  
55 stb.ShowStu()
  
56 err = json.Unmarshal([]byte(strData), &stb)
  
57 if err != nil {
  
58 fmt.Println("Unmarshal faild")
  
59 } else {
  
60 fmt.Println("Unmarshal success")
  
61 stb.ShowStu()
  
62 }
  
63 }
  
复制代码
  
运行结果:

复制代码
  
$ go run gojson.go
  
before JSON encoding :
  
show Student :

Name : Xiao Ming

Age : 16

Guake : true

Price : 9.99

Classes : Math English Chinese
  
encoded data :

```json
{"Name":"Xiao Ming","Age":16,"Guake":true,"Classes":["Math","English","Chinese"],"Price":9.99}
```

show Student :

Name :

Age : 0

Guake : false

Price : 0

Classes :
  
Unmarshal success
  
show Student :

Name : Xiao Ming

Age : 16

Guake : true

Price : 9.99

Classes : Math English Chinese

<http://colobu.com/2017/06/21/json-tricks-in-Go/#%E4%B8%B4%E6%97%B6%E6%94%B9%E5%90%8Dstruct%E7%9A%84%E5%AD%97%E6%AE%B5>

## Golang 从 Json 串中快速取出需要的字段

### GJSON

<https://github.com/tidwall/gjson>

### gojsonq

<https://github.com/thedevsaddam/gojsonq>
