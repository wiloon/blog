---
title: redis cluster哈希槽数量
author: w1100n
type: post
date: 2019-12-23T10:44:56+00:00
url: /?p=15242
categories:
  - Uncategorized

---
16348=16k，用bitmap来压缩心跳包的话，就相当于使用2_8_10=2KB大小的心跳包。而如果用crc16算法(redis使用这个而不是用哈希一致性算法)来确定哈希槽的分配。他的最大值是是2的16次方。用上面的算法换算需要8KB的心跳包来传输，作者自己认为这样不划算。而一个redis节点一般不会有超过1000个master(这个是作者自己说的),用16k来划分是比较合适的

https://www.zhihu.com/question/54817522
   
https://github.com/antirez/redis/issues/2576