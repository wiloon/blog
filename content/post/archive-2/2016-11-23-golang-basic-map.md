---
title: golang map set
author: wiloon
type: post
date: 2016-11-23T07:14:53+00:00
url: /?p=9419
categories:
  - Uncategorized

---
### map 清空

清空 map 中的所有元素
  
有意思的是，Go语言中并没有为 map 提供任何清空所有元素的函数、方法，清空 map 的唯一办法就是重新 make 一个新的 map，不用担心垃圾回收的效率，Go语言中的并行垃圾回收效率比写一个清空函数要高效的多。

### set

golang没有内置Set类型
  
这个gods项目 实现了各种数据类型，其中就有set
  
https://github.com/emirpasic/gods#hashset

或者可以实现。
  
golang set: https://studygolang.com/articles/8231

```golang 
# create map
serials:= make(map[string]uint8)
```

check if a map contains a key

```golang 
if val, ok := dict["foo"]; ok {
    //do something here
}
```

```golang &lt;br />package main

import "fmt"

func main() {
x := make(map[string][]string)

x["key"] = append(x["key"], "value")
x["key"] = append(x["key"], "value1")

fmt.Println(x["key"][0])
fmt.Println(x["key"][1])
}

```

遍历

```golang for k, v := range m { 
 fmt.Printf("k=%v, v=%v\n", k, v) 
 } 
```

基本语法
  
定义hashmap变量
  
由于go语言是一个强类型的语言，因此hashmap也是有类型的，具体体现在key和value都必须指定类型，比如声明一个key为string，value也是string的map，
  
需要这样做

var m map[string]string // 声明一个hashmap，还不能直接使用，必须使用make来初始化
  
m = make(map[string]string) // 初始化一个map
  
m = make(map[string]string, 3) // 初始化一个map并附带一个可选的初始bucket（非准确值，只是有提示意义）

m := map[string]string{} // 声明并初始化

m := make(map[string]string) // 使用make来初始化
  
大部分类型都能做key，某些类型是不能的，共同的特点是：不能使用==来比较，包括: slice, map, function

get,set,delete
  
m := map[string]int
  
m["a&#8221;] = 1

fmt.Println(m["a&#8221;]) // 输出 1

// 如果访问一个不存在的key，返回类型默认值
  
fmt.Println(m["b&#8221;]) // 输出0

// 测试key是否存在
  
v, ok := m["b&#8221;]
  
if ok {
  
&#8230;
  
}

// 删除一个key
  
delete(m, "a&#8221;)
  
迭代器
  
// 只迭代key
  
for k := range m {
  
&#8230;
  
}

// 同时迭代key-value
  
for k, v := range m {
  
&#8230;
  
}
  
在迭代的过程中是可以对map进行删除和更新操作的，规则如下：

迭代是无序的，跟插入是的顺序无关
  
迭代的过程中删除一个key，无论遍历还是没有遍历过都不会再遍历到
  
迭代的过程中添加一个key，不确定是否能遍历到
  
未初始化的map也可以迭代
  
其他
  
map的value是不可取地址的，意味着 &m["a&#8221;]这样的语法是非法的
  
len和cap分别可以获取当前map的kv个数和总容量

### Getting a slice of keys from a map

https://stackoverflow.com/questions/21362950/getting-a-slice-of-keys-from-a-map
  
there is not a simpler/nicer way.

```golang package main

func main() {
    mymap := make(map[int]string)
    keys := make([]int, 0, len(mymap))
    for k := range mymap {
        keys = append(keys, k)
    }
}
```

文／icexin（简书作者）
  
原文链接：http://www.jianshu.com/p/32b839e99289
  
著作权归作者所有，转载请联系作者获得授权，并标注“简书作者”。
  
http://www.jianshu.com/p/32b839e99289

 