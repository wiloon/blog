---
title: golang 排序
author: "-"
date: 2020-03-04T08:57:20+00:00
url: /?p=15683
categories:
  - Inbox
tags:
  - reprint
---
## golang 排序
Go 的排序思路和 C 和 C++ 有些差别。 C 默认是对数组进行排序， C++ 是对一个序列进行排序， Go 则更宽泛一些，待排序的可以是任何对象， 虽然很多情况下是一个 slice (分片， 类似于数组)，或是包含 slice 的一个对象。

排序(接口)的三个要素: 

待排序元素个数 n ；
  
第 i 和第 j 个元素的比较函数 cmp ；
  
第 i 和 第 j 个元素的交换 swap ；
  
乍一看条件 3 是多余的， c 和 c++ 都不提供 swap 。 c 的 qsort 的用法:  qsort(data, n, sizeof(int), cmp_int); data 是起始地址， n 是元素个数， sizeof(int) 是每个元素的大小， cmp_int 是一个比较两个 int 的函数。

c++ 的 sort 的用法:  sort(data, data+n, cmp_int); data 是第一个元素的位置， data+n 是最后一个元素的下一个位置， cmp_int 是比较函数。

基本类型排序(int、float64 和 string)
  
1. 升序排序
  
对于 int 、 float64 和 string 数组或是分片的排序， go 分别提供了 sort.Ints() 、 sort.Float64s() 和 sort.Strings() 函数， 默认都是从小到大排序。


    package main
    
    import (
        "fmt"
        "sort"
    )
    
    func main() {
        intList := [] int {2, 4, 3, 5, 7, 6, 9, 8, 1, 0}
        float8List := [] float64 {4.2, 5.9, 12.3, 10.0, 50.4, 99.9, 31.4, 27.81828, 3.14}
        stringList := [] string {"a", "c", "b", "d", "f", "i", "z", "x", "w", "y"}
      
        sort.Ints(intList)
        sort.Float64s(float8List)
        sort.Strings(stringList)
      
        fmt.Printf("%v\n%v\n%v\n", intList, float8List, stringList)
    
    }


https://itimetraveler.github.io/2016/09/07/%E3%80%90Go%E8%AF%AD%E8%A8%80%E3%80%91%E5%9F%BA%E6%9C%AC%E7%B1%BB%E5%9E%8B%E6%8E%92%E5%BA%8F%E5%92%8C%20slice%20%E6%8E%92%E5%BA%8F/