---
title: "redis bitmap"
author: "-"
date: "2021-07-06 05:56:41"
url: "redis-bitmap"
categories:
  - inbox
tags:
  - inbox
---
## "redis bitmap"

### BitMap
https://www.cnblogs.com/54chensongxia/p/13794391.html

BitMap#
BitMap 原本的含义是用一个比特位来映射某个元素的状态。由于一个比特位只能表示 0 和 1 两种状态，所以 BitMap 能映射的状态有限，但是使用比特位的优势是能大量的节省内存空间。

在 Redis 中，可以把 Bitmaps 想象成一个以比特位为单位的数组，数组的每个单元只能存储0和1，数组的下标在 Bitmaps 中叫做偏移量。

需要注意的是: BitMap 在 Redis 中并不是一个新的数据类型，其底层是 Redis 实现。

BitMap 相关命令#
# 设置值，其中value只能是 0 和 1
setbit key offset value

# 获取值
getbit key offset

# 获取指定范围内值为 1 的个数
# start 和 end 以字节为单位
bitcount key start end

# BitMap间的运算
# operations 位移操作符，枚举值
  AND 与运算 &
  OR 或运算 |
  XOR 异或 ^
  NOT 取反 ~
# result 计算的结果，会存储在该key中
# key1 … keyn 参与运算的key，可以有多个，空格分割，not运算只能一个key
# 当 BITOP 处理不同长度的字符串时，较短的那个字符串所缺少的部分会被看作 0。返回值是保存到 destkey 的字符串的长度 (以字节byte为单位) ，和输入 key 中最长的字符串长度相等。
bitop [operations] [result] [key1] [keyn…]

# 返回指定key中第一次出现指定value(0/1)的位置
bitpos [key] [value]

BitMap 占用的空间#
在弄清 BitMap 到底占用多大的空间之前，我们再来重申下: Redis 其实只支持 5 种数据类型，并没有 BitMap 这种类型，BitMap 底层是基于 Redis 的字符串类型实现的。

我们通过下面的命令来看下 BitMap 占用的空间大小: 

# 首先将偏移量是0的位置设为1
127.0.0.1:6379> setbit csx:key:1 0 1
(integer) 0
# 通过STRLEN命令，我们可以看到字符串的长度是1
127.0.0.1:6379> STRLEN csx:key:1
(integer) 1
# 将偏移量是1的位置设置为1
127.0.0.1:6379> setbit csx:key:1 1 1
(integer) 0
# 此时字符串的长度还是为1，以为一个字符串有8个比特位，不需要再开辟新的内存空间
127.0.0.1:6379> STRLEN csx:key:1
(integer) 1
# 将偏移量是8的位置设置成1
127.0.0.1:6379> setbit csx:key:1 8 1
(integer) 0
# 此时字符串的长度编程2，因为一个字节存不下9个比特位，需要再开辟一个字节的空间
127.0.0.1:6379> STRLEN csx:key:1
(integer) 2
通过上面的实验我们可以看出，BitMap 占用的空间，就是底层字符串占用的空间。假如 BitMap 偏移量的最大值是 OFFSET_MAX，那么它底层占用的空间就是: 

(OFFSET_MAX/8)+1 = 占用字节数
因为字符串内存只能以字节分配，所以上面的单位是字节。

但是需要注意，Redis 中字符串的最大长度是 512M，所以 BitMap 的 offset 值也是有上限的，其最大值是: 

8 * 1024 * 1024 * 512  =  2^32
由于 C语言中字符串的末尾都要存储一位分隔符，所以实际上 BitMap 的 offset 值上限是: 

(8 * 1024 * 1024 * 512) -1  =  2^32 - 1
使用场景#
1. 用户签到

很多网站都提供了签到功能，并且需要展示最近一个月的签到情况，这种情况可以使用 BitMap 来实现。
根据日期 offset =  (今天是一年中的第几天)  %  (今年的天数) ，key = 年份: 用户id。

如果需要将用户的详细签到信息入库的话，可以考虑使用一个一步线程来完成。

2. 统计活跃用户 (用户登陆情况) 

使用日期作为 key，然后用户 id 为 offset，如果当日活跃过就设置为1。具体怎么样才算活跃这个标准大家可以自己指定。

假如 20201009 活跃用户情况是:  [1，0，1，1，0]
20201010 活跃用户情况是 : [ 1，1，0，1，0 ]

统计连续两天活跃的用户总数: 

bitop and dest1 20201009 20201010 
# dest1 中值为1的offset，就是连续两天活跃用户的ID
bitcount dest1
统计20201009 ~ 20201010 活跃过的用户: 

bitop or dest2 20201009 20201010 
3. 统计用户是否在线

如果需要提供一个查询当前用户是否在线的接口，也可以考虑使用 BitMap 。即节约空间效率又高，只需要一个 key，然后用户 id 为 offset，如果在线就设置为 1，不在线就设置为 0。
