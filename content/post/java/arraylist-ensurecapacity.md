---
title: ArrayList Capacity
author: "-"
date: 2012-08-20T06:00:23+00:00
url: ArrayList/capacity
categories:
  - Java
tags:
  - reprint
---
## ArrayList Capacity

<http://topic.csdn.net/t/20061223/10/5250896.html>
  
任何一个 ArrayList 对象都有一个 capacity 属性，用来指示该 ArrayList 的容量，用"容量"这个词容易引起像本贴楼主那样的误解，我觉得用"容纳能力"比较贴切。

我们知道ArrayList的内部是采用数组来存储元素的，由于java数组都是定长的，所以这个数组的大小一定是固定的，这个大小就是capacity。我们可以肯定capacity一定是大于或等于ArrayList的size，那么当size不断增加到了要超过capacity的时候，ArrayList就不得不重新创建新的capacity来容纳更多的元素，这时需要首先建立一个更长的数组，将原来的数组中的元素复制到新数组中，再删除原来的数组。可见当ArrayList越来越大时，这种操作的消耗也是越来越大的。

为了减少这种不必要的重建capacity的操作，当我们能肯定ArrayList大致有多大 (或者至少会有多大) 时，我们可以先让ArrayList把capacity设为我们期望的大小，以避免多余的数组重建。

假设ArrayList自动把capacity设为10，每次重建时将长度递增原来的三分之二，那么当我们需要大约存储50个元素到ArrayList中时，就会大约需要重建数组4次，分别是在增加第11、第17、第26、第39个元素的时候进行的。如果我们一开始就让ArrayList的capacity为50，那么不需要任何数组重建就能完成所有插入操作了。

java允许我们在构造ArrayList的同时指定capacity，如new   ArrayList(50)，也允许在以后将它设得更大，而增大capacity就是使用ensureCapacity()方法。注意: capacity只能比原来的更大，而不能比原来的更小，否则java会忽略该操作。ArrayList的初始默认capacity为10，所以给capacity指定小于10的整数是毫无意义的。

最后说说ArrayList的size，前面说过，size一定小于等于capactiy，而且更重要的是，访问超过size的位置将抛出异常，尽管这个位置可能没有超过capacity。ensureCapacity()只可能增加capacity，而不会对size有任何影响。要增加size，只能用add()方法。

<https://blog.csdn.net/vandavidchou/article/details/104306445>
