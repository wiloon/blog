---
title: golang struct/结构体
author: "-"
date: 2017-10-10T14:52:35+00:00
url: go-struct
categories:
  - golang

---
```golang
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
person:= struct {//匿名结构
        name string
        age int
    }{name:"匿名",age:1}
    f.Println("person:",person)
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

https://github.com/jemygraw/TechDoc/blob/master/Go%E8%BD%BB%E6%9D%BE%E5%AD%A6/go_tutorial_8_struct_interface.md
  
https://blog.csdn.net/books1958/article/details/22720033