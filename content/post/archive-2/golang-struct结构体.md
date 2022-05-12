---
title: golang struct/结构体
author: "-"
date: 2017-10-10T14:52:35+00:00
url: go-struct
categories:
  - Go
tags:
  - reprint
---
## golang struct/结构体

```go
//定义一个struct
type Student struct {
    id      int
    name    string
    address string
    age     int
}
```

### 匿名结构体

```go
//匿名结构
person := struct { 
    Name string
    Age  int
}{Name: "匿名", Age: 1}

jsonBytes, _ := json.Marshal(person)
fmt.Println("person:", string(jsonBytes))
```

```go
type foo struct {
    Field0 string `json:"field0"`
    Field1  struct {
        Field2 string `json:"field2"`
    } `json:"field1"`
    Field3 int `json:"field3"`
}
```

<https://github.com/jemygraw/TechDoc/blob/master/Go%E8%BD%BB%E6%9D%BE%E5%AD%A6/go_tutorial_8_struct_interface.md>
  
<https://blog.csdn.net/books1958/article/details/22720033>
