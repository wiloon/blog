---
title: redis list
author: "-"
date: 2015-12-01T02:32:24+00:00
url: /redis/list
categories:
  - redis
tags:
  - redis
---
## redis list

在 Redis 中, List 类型是按照插入顺序排序的字符串链表。和数据结构中的普通链表一样,我们可以在其头部(left)和尾部(right)添加新的元素。在插入时,如果该键并不存在,Redis将为该键创建一个新的链表。与此相反,如果链表中所有的元素均被移除,那么该键也将会被从数据库中删除。List中可以包含的最大元素数量是4294967295。
  
从元素插入和删除的效率视角来看,如果我们是在链表的两头插入或删除元素,这将会是非常高效的操作,即使链表中已经存储了百万条记录,该操作也可以在常量时间内完成。然而需要说明的是,如果元素插入或删除操作是作用于链表中间,那将会是非常低效的。

Redis 的列表经常被用作队列(queue),用于在不同程序之间有序地交换消息(message)。
  
一个程序(称之为生产者,producer)通过LPUSH命令将消息放入队列中,而另一个程序(称之为消费者,consumer)通过RPOP命令取出队列中等待时间最长的消息。

不幸的是,在这个过程中,一个消费者可能在获得一个消息之后崩溃,而未执行完成的消息也因此丢失。
  
使用RPOPLPUSH命令可以解决这个问题,因为它在返回一个消息之余,还将该消息添加到另一个列表当中,另外的这个列表可以用作消息的备份表: 假如一切正常,当消费者完成该消息的处理之后,可以用LREM命令将该消息从备份表删除。

另一方面,助手(helper)程序可以通过监视备份表,将超过一定处理时限的消息重新放入队列中去(负责处理该消息的消费者可能已经崩溃),这样就不会丢失任何消息了。

头元素和尾元素

头元素指的是列表左端/前端第一个元素,尾元素指的是列表右端/后端第一个元素。
  
举个例子,列表list包含三个元素: x, y, z,其中x是头元素,而z则是尾元素。

空列表

指不包含任何元素的列表,Redis将不存在的key也视为空列表。
  
一个列表最多可以包含 232 – 1 个元素 (4294967295, 每个列表超过40亿个元素)。

### 相关命令

### LPUSH

    LPUSH key value1 [value2]
    将一个或多个值插入到列表头部

### RPUSH

    RPUSH key value1 [value2]
    将一个或多个值value插入到列表key的表尾。

### LPOP key

移出并获取列表的第一个元素

### RPOP key

    RPOP key
    移除列表的最后一个元素,返回值为移除的元素。

### LLEN key

获取列表长度

### LRANGE key start stop

### LTRIM key start stop

对一个列表进行修剪(trim),就是说,让列表只保留指定区间内的元素,不在指定区间之内的元素都将被删除。

### BLPOP

    BLPOP key1 [key2 ] timeout
    移出并获取列表的第一个元素, 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。

### BRPOP key1 [key2 ] timeout

移出并获取列表的最后一个元素, 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。

### BRPOPLPUSH source destination timeout

从列表中弹出一个值,将弹出的元素插入到另外一个列表中并返回它； 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。

### RPOPLPUSH source destination

移除列表的最后一个元素,并将该元素添加到另一个列表并返回

### LINDEX key index

### LINSERT key BEFORE|AFTER pivot value

### LPUSHX key value

将值value插入到列表key的表头,当且仅当key存在并且是一个列表。    和LPUSH命令相反,当key不存在时,LPUSHX命令什么也不做。

RPUSHX key value

LSET key index value

BRPOP key1 [key2 …] timeout
  
阻塞式(blocking)弹出

它是RPOP命令的阻塞版本,当给定列表内没有任何元素可供弹出的时候,连接将被BRPOP命令阻塞,直到等待超时或发现可弹出元素为止。
  
当给定多个key参数时,按参数key的先后顺序依次检查各个列表,弹出第一个非空列表的尾部元素。
  
关于阻塞操作的更多信息,请查看BLPOP命令,BRPOP除了弹出元素的位置和BLPOP不同之外,其他表现一致。

时间复杂度:
  
O(1)
  
返回值:
  
假如在指定时间内没有任何元素被弹出,则返回一个nil和等待时长。
  
反之,返回一个含有两个元素的列表,第一个元素是被弹出元素所属的key,第二个元素是被弹出元素的值。
  
redis> LLEN course
  
(integer) 0

redis> RPUSH course algorithm001
  
(integer) 1
  
redis> RPUSH course c++101 # 尾部元素
  
(integer) 2

redis> BRPOP course 30
  
1) "course" # 弹出元素的key
  
2) "c++101" # 弹出元素的值
  
LPUSH key value [value …]

在key对应list的头部添加字符串元素

返回插入后链表中元素的数量。

O(1)
  
在指定Key所关联的List Value的头部插入参数中给出的所有Values。如果该Key不存在,该命令将在插入之前创建一个与该Key关联的空链表,之后再将数据从链表的头部插入。如果该键的Value不是链表类型,该命令将返回相关的错误信息。

### LPUSHX key value

插入后链表中元素的数量。
  
O(1)
  
仅有当参数中指定的Key存在时,该命令才会在其所关联的List Value的头部插入参数中给出的Value,否则将不会有任何操作发生。

### LRANGE key start stop

返回指定范围内元素的列表。
  
O(S+N)
  
时间复杂度中的S为start参数表示的偏移量,N表示元素的数量。该命令的参数start和end都是0-based。即0表示链表头部(leftmost)的第一个元素。其中start的值也可以为负值,-1将表示链表中的最后一个元素,即尾部元素,-2表示倒数第二个并以此类推。该命令在获取元素时,start和end位置上的元素也会被取出。如果start的值大于链表中元素的数量,空链表将会被返回。如果end的值大于元素的数量,该命令则获取从start(包括start)开始,链表中剩余的所有元素。

### LPOPkey

从list的头部删除元素,并返回删除元素:

返回链表头部的元素。
  
O(1)
  
返回并弹出指定Key关联的链表中的第一个元素,即头部元素,。如果该Key不存,返回nil。

### LLEN key

返回key对应list的长度:

返回链表中元素的数量。
  
O(1)
  
返回指定Key关联的链表中元素的数量,如果该Key不存在,则返回0。如果与该Key关联的Value的类型不是链表,则返回相关的错误信息。

### LREM key count value

从key对应list中删除count个和value相同的元素。

count>0时,按从头到尾的顺序删除

count<0时,按从尾到头的顺序删除

count=0时,删除全部

返回被删除的元素数量。
  
O(N)
  
时间复杂度中N表示链表中元素的数量。在指定Key关联的链表中,删除前count个值等于value的元素。如果count大于0,从头向尾遍历并删除,如果count小于0,则从尾向头遍历并删除。如果count等于0,则删除链表中所有等于value的元素。如果指定的Key不存在,则直接返回0。

### LSETkey index value

设置list中指定下标的元素值(下标从0开始):
  
O(N)
  
时间复杂度中N表示链表中元素的数量。但是设定头部或尾部的元素时,其时间复杂度为O(1)。设定链表中指定位置的值为新值,其中0表示第一个元素,即头部元素,-1表示尾部元素。如果索引值Index超出了链表中元素的数量范围,该命令将返回相关的错误信息。

### LINDEX key index

返回名称为key的list中index位置的元素:
  
O(N)
  
时间复杂度中N表示在找到该元素时需要遍历的元素数量。对于头部或尾部元素,其时间复杂度为O(1)。该命令将返回链表中指定位置(index)的元素,index是0-based,表示头部元素,如果index为-1,表示尾部元素。如果与该Key关联的不是链表,该命令将返回相关的错误信息。
  
返回请求的元素,如果index超出范围,则返回nil。

### LLTRIM key start stop

保留指定key 的值范围内的数据:
  
O(N)
  
N表示被删除的元素数量。该命令将仅保留指定范围内的元素,从而保证 list 中的元素数量相对恒定。start和stop参数都是 0-based,0表示头部元素。和其他命令一样,start和stop也可以为负值,-1表示尾部元素。如果start大于链表的尾部,或start大于stop,该命令不错报错,而是返回一个空的链表,与此同时该Key也将被删除。如果stop大于元素的数量,则保留从start开始剩余的所有元素。

LINSERT key BEFORE|AFTER pivot value
  
在key对应list的特定位置之前或之后添加字符串元素
  
O(N)
  
时间复杂度中N表示在找到该元素pivot之前需要遍历的元素数量。这样意味着如果pivot位于链表的头部或尾部时,该命令的时间复杂度为O(1)。该命令的功能是在pivot元素的前面或后面插入参数中的元素value。如果Key不存在,该命令将不执行任何操作。如果与Key关联的Value类型不是链表,相关的错误信息将被返回。
  
成功插入后链表中元素的数量,如果没有找到pivot,返回-1,如果key不存在,返回0。

RPOPLPUSH source destination
  
从第一个list的尾部移除元素并添加到第二个list的头部,最后返回被移除的元素值,整个操作是原子的.如果第一个list是空或者不存在返回nil:
  
O(1)
  
原子性的从与source键关联的链表尾部弹出一个元素,同时再将弹出的元素插入到与destination键关联的链表的头部。如果source键不存在,该命令将返回nil,同时不再做任何其它的操作了。如果source和destination是同一个键,则相当于原子性的将其关联链表中的尾部元素移到该链表的头部。
  
返回弹出和插入的元素。
  
命令RPOPLPUSH在一个原子时间内,执行以下两个动作:

将列表source中的最后一个元素(尾元素)弹出,并返回给客户端。
  
将source弹出的元素插入到列表destination,作为destination列表的的头元素。

举个例子,你有两个列表source和destination,source列表有元素a, b, c,destination列表有元素x, y, z,执行RPOPLPUSH source destination之后,source列表包含元素a, b,destination列表包含元素c, x, y, z ,并且元素c被返回。

如果source不存在,值nil被返回,并且不执行其他动作。

如果source和destination相同,则列表中的表尾元素被移动到表头,并返回该元素,可以把这种特殊情况视作列表的旋转(rotation)操作。

RPUSH key value [value …]
  
在key对应list的尾部添加字符串元素:
  
返回插入后链表中元素的数量。
  
O(1)
  
在指定Key所关联的List Value的尾部插入参数中给出的所有Values。如果该Key不存在,该命令将在插入之前创建一个与该Key关联的空链表,之后再将数据从链表的尾部插入。如果该键的Value不是链表类型,该命令将返回相关的错误信息。

仅有当参数中指定的Key存在时,该命令才会在其所关联的List Value的尾部插入参数中给出的Value,否则将不会有任何操作发生。
  
插入后链表中元素的数量。

RPOP key
  
从list的尾部删除元素,并返回删除元素:
  
O(1)
  
返回并弹出指定Key关联的链表中的最后一个元素,即尾部元素,。如果该Key不存,返回nil。
  
链表尾部的元素。

三、命令示例:

  1. LPUSH/LPUSHX/LRANGE:
  
    /> redis-cli #在Shell提示符下启动redis客户端工具。
  
    redis 127.0.0.1:6379> del mykey
  
    (integer) 1
  
    #mykey键并不存在,该命令会创建该键及与其关联的List,之后在将参数中的values从左到右依次插入。
  
    redis 127.0.0.1:6379> lpush mykey a b c d
  
    (integer) 4
  
    #取从位置0开始到位置2结束的3个元素。
  
    redis 127.0.0.1:6379> lrange mykey 0 2
  
    1) "d"
  
    2) "c"
  
    3) "b"
  
    #取链表中的全部元素,其中0表示第一个元素,-1表示最后一个元素。
  
    redis 127.0.0.1:6379> lrange mykey 0 -1
  
    1) "d"
  
    2) "c"
  
    3) "b"
  
    4) "a"
  
    #mykey2键此时并不存在,因此该命令将不会进行任何操作,其返回值为0。
  
    redis 127.0.0.1:6379> lpushx mykey2 e
  
    (integer) 0
  
    #可以看到mykey2没有关联任何List Value。
  
    redis 127.0.0.1:6379> lrange mykey2 0 -1
  
    (empty list or set)
  
    #mykey键此时已经存在,所以该命令插入成功,并返回链表中当前元素的数量。
  
    redis 127.0.0.1:6379> lpushx mykey e
  
    (integer) 5
  
    #获取该键的List Value的头部元素。
  
    redis 127.0.0.1:6379> lrange mykey 0 0
  
    1) "e" 

  2. LPOP/LLEN:
  
    redis 127.0.0.1:6379> lpush mykey a b c d
  
    (integer) 4
  
    redis 127.0.0.1:6379> lpop mykey
  
    "d"
  
    redis 127.0.0.1:6379> lpop mykey
  
    "c"
  
    #在执行lpop命令两次后,链表头部的两个元素已经被弹出,此时链表中元素的数量是2
  
    redis 127.0.0.1:6379> llen mykey
  
    (integer) 2

  3. LREM/LSET/LINDEX/LTRIM:
  
    #为后面的示例准备测试数据。
  
    redis 127.0.0.1:6379> lpush mykey a b c d a c
  
    (integer) 6
  
    #从头部(left)向尾部(right)变量链表,删除2个值等于a的元素,返回值为实际删除的数量。
  
    redis 127.0.0.1:6379> lrem mykey 2 a
  
    (integer) 2
  
    #看出删除后链表中的全部元素。
  
    redis 127.0.0.1:6379> lrange mykey 0 -1
  
    1) "c"
  
    2) "d"
  
    3) "c"
  
    4) "b"
  
    #获取索引值为1(头部的第二个元素)的元素值。
  
    redis 127.0.0.1:6379> lindex mykey 1
  
    "d"
  
    #将索引值为1(头部的第二个元素)的元素值设置为新值e。
  
    redis 127.0.0.1:6379> lset mykey 1 e
  
    OK
  
    #查看是否设置成功。
  
    redis 127.0.0.1:6379> lindex mykey 1
  
    "e"
  
    #索引值6超过了链表中元素的数量,该命令返回nil。
  
    redis 127.0.0.1:6379> lindex mykey 6
  
    (nil)
  
    #设置的索引值6超过了链表中元素的数量,设置失败,该命令返回错误信息。
  
    redis 127.0.0.1:6379> lset mykey 6 hh
  
    (error) ERR index out of range
  
    #仅保留索引值0到2之间的3个元素,注意第0个和第2个元素均被保留。
  
    redis 127.0.0.1:6379> ltrim mykey 0 2
  
    OK
  
    #查看trim后的结果。
  
    redis 127.0.0.1:6379> lrange mykey 0 -1
  
    1) "c"
  
    2) "e"
  
    3) "c"

  4. LINSERT:
  
    #删除该键便于后面的测试。
  
    redis 127.0.0.1:6379> del mykey
  
    (integer) 1
  
    #为后面的示例准备测试数据。
  
    redis 127.0.0.1:6379> lpush mykey a b c d e
  
    (integer) 5
  
    #在a的前面插入新元素a1。
  
    redis 127.0.0.1:6379> linsert mykey before a a1
  
    (integer) 6
  
    #查看是否插入成功,从结果看已经插入。注意lindex的index值是0-based。
  
    redis 127.0.0.1:6379> lindex mykey 0
  
    "e"
  
    #在e的后面插入新元素e2,从返回结果看已经插入成功。
  
    redis 127.0.0.1:6379> linsert mykey after e e2
  
    (integer) 7
  
    #再次查看是否插入成功。
  
    redis 127.0.0.1:6379> lindex mykey 1
  
    "e2"
  
    #在不存在的元素之前或之后插入新元素,该命令操作失败,并返回-1。
  
    redis 127.0.0.1:6379> linsert mykey after k a
  
    (integer) -1
  
    #为不存在的Key插入新元素,该命令操作失败,返回0。
  
    redis 127.0.0.1:6379> linsert mykey1 after a a2
  
    (integer) 0

  5. RPUSH/RPUSHX/RPOP/RPOPLPUSH:
  
    #删除该键,以便于后面的测试。
  
    redis 127.0.0.1:6379> del mykey
  
    (integer) 1
  
    #从链表的尾部插入参数中给出的values,插入顺序是从左到右依次插入。
  
    redis 127.0.0.1:6379> rpush mykey a b c d
  
    (integer) 4
  
    #通过lrange的可以获悉rpush在插入多值时的插入顺序。
  
    redis 127.0.0.1:6379> lrange mykey 0 -1
  
    1) "a"
  
    2) "b"
  
    3) "c"
  
    4) "d"
  
    #该键已经存在并且包含4个元素,rpushx命令将执行成功,并将元素e插入到链表的尾部。
  
    redis 127.0.0.1:6379> rpushx mykey e
  
    (integer) 5
  
    #通过lindex命令可以看出之前的rpushx命令确实执行成功,因为索引值为4的元素已经是新元素了。
  
    redis 127.0.0.1:6379> lindex mykey 4
  
    "e"
  
    #由于mykey2键并不存在,因此该命令不会插入数据,其返回值为0。
  
    redis 127.0.0.1:6379> rpushx mykey2 e
  
    (integer) 0
  
    #在执行rpoplpush命令前,先看一下mykey中链表的元素有哪些,注意他们的位置关系。
  
    redis 127.0.0.1:6379> lrange mykey 0 -1
  
    1) "a"
  
    2) "b"
  
    3) "c"
  
    4) "d"
  
    5) "e"
  
    #将mykey的尾部元素e弹出,同时再插入到mykey2的头部(原子性的完成这两步操作)。
  
    redis 127.0.0.1:6379> rpoplpush mykey mykey2
  
    "e"
  
    #通过lrange命令查看mykey在弹出尾部元素后的结果。
  
    redis 127.0.0.1:6379> lrange mykey 0 -1
  
    1) "a"
  
    2) "b"
  
    3) "c"
  
    4) "d"
  
    #通过lrange命令查看mykey2在插入元素后的结果。
  
    redis 127.0.0.1:6379> lrange mykey2 0 -1
  
    1) "e"
  
    #将source和destination设为同一键,将mykey中的尾部元素移到其头部。
  
    redis 127.0.0.1:6379> rpoplpush mykey mykey
  
    "d"
  
    #查看移动结果。
  
    redis 127.0.0.1:6379> lrange mykey 0 -1
  
    1) "d"
  
    2) "a"
  
    3) "b"
  
    4) "c"

四、链表结构的小技巧:

针对链表结构的Value,Redis在其官方文档中给出了一些实用技巧,如RPOPLPUSH命令,下面给出具体的解释。
  
Redis链表经常会被用于消息队列的服务,以完成多程序之间的消息交换。假设一个应用程序正在执行LPUSH操作向链表中添加新的元素,我们通常将这样的程序称之为"生产者(Producer)",而另外一个应用程序正在执行RPOP操作从链表中取出元素,我们称这样的程序为"消费者(Consumer)"。如果此时,消费者程序在取出消息元素后立刻崩溃,由于该消息已经被取出且没有被正常处理,那么我们就可以认为该消息已经丢失,由此可能会导致业务数据丢失,或业务状态的不一致等现象的发生。然而通过使用RPOPLPUSH命令,消费者程序在从主消息队列中取出消息之后再将其插入到备份队列中,直到消费者程序完成正常的处理逻辑后再将该消息从备份队列中删除。同时我们还可以提供一个守护进程,当发现备份队列中的消息过期时,可以重新将其再放回到主消息队列中,以便其它的消费者程序继续处理。

内部编码
列表类型的 内部编码 有两种:

2.1. ziplist (压缩列表)
当列表的元素个数 小于 list-max-ziplist-entries 配置 (默认 512 个) ,同时列表中 每个元素 的值都 小于  list-max-ziplist-value 配置时 (默认 64 字节) ,Redis 会选用 ziplist 来作为 列表 的 内部实现 来减少内存的使用。
 linkedlist (链表)
当 列表类型 无法满足 ziplist 的条件时, Redis 会使用 linkedlist 作为 列表 的 内部实现。

Redis3.2 版本提供了 quicklist 内部编码,简单地说它是以一个 ziplist 为 节点 的 linkedlist,它结合了 ziplist 和 linkedlist 两者的优势,为 列表类型 提供了一种更为优秀的 内部编码 实现,它的设计原理可以参考 Redis 的另一个作者 Matt Stancliff 的博客 redis-quicklist。

作者: 零壹技术栈
链接: <https://juejin.cn/post/6844903696120152071>
来源: 掘金
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

<http://www.cnblogs.com/stephen-liu74/archive/2012/02/14/2351859.html>

<http://tech.it168.com/a2011/0926/1251/000001251881_1.shtml>
