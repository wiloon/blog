---
title: Go map set
author: "-"
date: 2016-11-23T07:14:53+00:00
url: go/map
categories:
  - Go
tags:
  - reprint
  - Map
---
## go map

- map 是由 key-value 对组成的；key 只会出现一次。
- Map 是一种无序的键值对的集合
- map 是 mutable 的, 可以对其进行修改,map 不是线程安全的.
- 从map中读取一个不存在的key的时候，返回0值
- Go 语言的 map 用的是哈希查找表(Hash table)，并且使用链表解决哈希冲突。

Go 语言中 map 是一种特殊的数据结构，一种元素对（pair）的无序集合，pair 对应一个 key（索引）和一个 value（值），所以这个结构也称为关联数组或字典，这是一种能够快速寻找值的理想结构，给定 key，就可以迅速找到对应的 value。

map 这种数据结构在其他编程语言中也称为字典（Python）、hash 和 HashTable 等。

维基百科里这样定义 map：

In computer science, an associative array, map, symbol table, or dictionary is an abstract data type composed of a collection of (key, value) pairs, such that each possible key appears at most once in the collection.

和 map 相关的操作主要是：

- 增加一个 k-v 对 —— Add or insert；
- 删除一个 k-v 对 —— Remove or delete；
- 修改某个 k 对应的 v —— Reassign；
- 查询某个 k 对应的 v —— Lookup；

为什么要用 map
从 Go 语言官方博客摘录一段话：

One of the most useful data structures in computer science is the hash table. Many hash table implementations exist with varying properties, but in general they offer fast lookups, adds, and deletes. Go provides a built-in map type that implements a hash table.
hash table 是计算机数据结构中一个最重要的设计。大部分 hash table 都实现了快速查找、添加、删除的功能。Go 语言内置的 map 实现了上述所有功能。

```go
/* 声明变量，默认 map 是 nil */
var map_variable map[key_data_type]value_data_type

/* 使用 make 函数 */
map_variable := make(map[key_data_type]value_data_type)

```

### 直接创建

```go
m2 := make(map[string]string)
// 然后赋值
m2["a"] = "aa"
m2["b"] = "bb"

// 删除
delete(m2, "a")
```

#### 初始化 + 赋值

```go
m3 := map[string]string{
    "a": "aa",
    "b": "bb",
}
```

#### 查找键值是否存在

```go
if v, ok := m1["a"]; ok {
    fmt.Println(v)
} else {
    fmt.Println("Key Not Found")
}
```

#### 遍历 map

```go
for k, v := range m1 {
    fmt.Println(k, v)
}
```

### map 清空

清空 map 中的所有元素
  
有意思的是, Go语言中并没有为 map 提供任何清空所有元素的函数、方法,清空 map 的唯一办法就是重新 make 一个新的 map, 不用担心垃圾回收的效率, Go语言中的并行垃圾回收效率比写一个清空函数要高效的多。

### gods > TreeMap

gods > treemap

## go set

golang 没有内置 Set 类型  
这个 gods 项目 现了各种数据类型, 其中就有set
  
[https://github.com/emirpasic/gods#hashset](https://github.com/emirpasic/gods#hashset)

```go
package main

import "github.com/emirpasic/gods/sets/hashset"

func main() {
    set := hashset.New()   // empty
    set.Add(1)             // 1
    set.Add(2, 2, 3, 4, 5) // 3, 1, 2, 4, 5 (random order, duplicates ignored)
    set.Remove(4)          // 5, 3, 2, 1 (random order)
    set.Remove(2, 3)       // 1, 5 (random order)
    set.Contains(1)        // true
    set.Contains(1, 5)     // true
    set.Contains(1, 6)     // false
    _ = set.Values()       // []int{5,1} (random order)
    set.Clear()            // empty
    set.Empty()            // true
    set.Size()             // 0
}
```

或者可以实现。
  
golang set: [https://studygolang.com/articles/8231](https://studygolang.com/articles/8231)

```go

# create map
serials:= make(map[string]uint8)
```

check if a map contains a key

```go

if val, ok := dict["foo"]; ok {
    //do something here
}
```

```go

package main

import "fmt"

func main() {
x := make(map[string][]string)

x["key"] = append(x["key"], "value")
x["key"] = append(x["key"], "value1")

fmt.Println(x["key"][0])
fmt.Println(x["key"][1])
}

```

### 遍历

```go
for k, v := range m { 
 fmt.Printf("k=%v, v=%v\n", k, v) 
 } 
```

基本语法
  
定义hashmap变量
  
由于go语言是一个强类型的语言,因此hashmap也是有类型的,具体体现在key和value都必须指定类型,比如声明一个key为string,value也是string的map,
  
需要这样做

var m map[string]string // 声明一个hashmap,还不能直接使用,必须使用make来初始化
  
m = make(map[string]string) // 初始化一个map
  
m = make(map[string]string, 3) // 初始化一个map并附带一个可选的初始bucket (非准确值,只是有提示意义)

m := map[string]string{} // 声明并初始化

m := make(map[string]string) // 使用make来初始化
  
大部分类型都能做key,某些类型是不能的,共同的特点是: 不能使用==来比较,包括: slice, map, function

get,set,delete
  
m := map[string]int
  
m["a"] = 1

fmt.Println(m["a"]) // 输出 1

// 如果访问一个不存在的key,返回类型默认值
  
fmt.Println(m["b"]) // 输出0

// 测试key是否存在
  
v, ok := m["b"]
  
if ok {
  
...
  
}

// 删除一个key
  
delete(m, "a")
  
迭代器
  
// 只迭代key
  
for k := range m {
  
...
  
}

// 同时迭代key-value
  
for k, v := range m {
  
...
  
}
  
在迭代的过程中是可以对map进行删除和更新操作的,规则如下:

迭代是无序的,跟插入是的顺序无关
  
迭代的过程中删除一个key,无论遍历还是没有遍历过都不会再遍历到
  
迭代的过程中添加一个key,不确定是否能遍历到
  
未初始化的map也可以迭代
  
其他
  
map的value是不可取地址的,意味着 &m["a"]这样的语法是非法的
  
len和cap分别可以获取当前map的kv个数和总容量

### Getting a slice of keys from a map

[https://stackoverflow.com/questions/21362950/getting-a-slice-of-keys-from-a-map](https://stackoverflow.com/questions/21362950/getting-a-slice-of-keys-from-a-map)
  
there is not a simpler/nicer way.

```go
package main

func main() {
    mymap := make(map[int]string)
    keys := make([]int, 0, len(mymap))
    for k := range mymap {
        keys = append(keys, k)
    }
}
```

文/icexin (简书作者)
  
原文链接: [http://www.jianshu.com/p/32b839e99289](http://www.jianshu.com/p/32b839e99289)
  
著作权归作者所有,转载请联系作者获得授权,并标注"简书作者"。
  
[http://www.jianshu.com/p/32b839e99289](http://www.jianshu.com/p/32b839e99289)

## 检测单向链表是否有环

```go
type Node struct {
    Next  *Node
    Value interface{}
}
var first *Node

func main(){
visited := make(map[*Node]bool)
    for n := first; n != nil; n = n.Next {
        if visited[n] {
            fmt.Println("cycle detected")
            break
        }
        visited[n] = true
        fmt.Println(n.Value)
    }
}
```

[https://www.jianshu.com/p/ba7852fbcc80](https://www.jianshu.com/p/ba7852fbcc80)

[https://segmentfault.com/a/1190000023879178](https://segmentfault.com/a/1190000023879178)

## go source code

```b
src/runtime/map.go
```

```go
// A header for a Go map.
type hmap struct {
    // 元素个数，调用 len(map) 时，直接返回此值
    count     int
    flags     uint8
    // buckets 的对数 log_2
    B         uint8
    // overflow 的 bucket 近似数
    noverflow uint16
    // 计算 key 的哈希的时候会传入哈希函数
    hash0     uint32
    // 指向 buckets 数组，大小为 2^B
    // 如果元素个数为0，就为 nil
    buckets    unsafe.Pointer
    // 扩容的时候，buckets 长度会是 oldbuckets 的两倍
    oldbuckets unsafe.Pointer
    // 指示扩容进度，小于此地址的 buckets 迁移完成
    nevacuate  uintptr
    extra *mapextra // optional fields
}
```

[[go-pointer#unsafe Pointer]]

[https://segmentfault.com/a/1190000023879178](https://segmentfault.com/a/1190000023879178)
