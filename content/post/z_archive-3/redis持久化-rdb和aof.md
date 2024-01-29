---
title: Redis 持久化 RDB 和 AOF
author: "-"
date: 2019-12-23T08:00:59+00:00
url: redis-rdb-aof
categories:
  - inbox
tags:
  - reprint
---
## Redis 持久化 RDB 和 AOF

Redis本身的机制是 AOF 持久化开启且存在AOF文件时，优先加载AOF文件；AOF 关闭或者AOF文件不存在时，加载RDB文件；加载AOF/RDB文件城后，Redis启动成功；AOF/RDB文件存在错误时，Redis启动失败并打印错误信息

### RDB快照持久化

RDB 持久化是通过快照的方式，即在指定的时间间隔内将内存中的数据集快照写入磁盘。在创建快照之后，用户可以备份该快照，可以将快照复制到其他服务器以创建相同数据的服务器副本，或者在重启服务器后恢复数据。RDB是Redis默认的持久化方式
快照持久化
RDB持久化会生成RDB文件，该文件是一个压缩过的二进制文件，可以通过该文件还原快照时的数据库状态，即生成该RDB文件时的服务器数据。RDB文件默认为当前工作目录下的dump.rdb，可以根据配置文件中的dbfilename和dir设置RDB的文件名和文件位置

```bash
# 设置 dump 的文件名
dbfilename dump.rdb

# 工作目录
# 例如上面的 dbfilename 只指定了文件名，
# 但是它会写入到这个目录下。这个配置项一定是个目录，而不能是文件名。
dir ./
```

### 触发快照的时机

执行 save 和 bgsave 命令
配置文件设置 `save <seconds> <changes>`规则，自动间隔性执行bgsave命令
主从复制时，从库全量复制同步主库数据，主库会执行bgsave
执行 flushall 命令清空服务器数据
执行 shutdown 命令关闭 Redis 时，会执行 save命令

### save 和bgsave命令

执行save 和bgsave命令，可以手动触发快照，生成RDB文件，两者的区别如下
使用save 命令会阻塞Redis服务器进程，服务器进程在RDB文件创建完成之前是不能处理任何的命令请求

而使用bgsave 命令不同的是，basave命令会fork一个子进程，然后该子进程会负责创建RDB文件，而服务器进程会继续处理命令请求

fork() 是由操作系统提供的函数，作用是创建当前进程的一个副本作为子进程

fork 一个子进程，子进程会把数据集先写入临时文件，写入成功之后，再替换之前的RDB文件，用二进制压缩存储，这样可以保证RDB文件始终存储的是完整的持久化内容

自动间隔触发
在配置文件中设置 `save <seconds> <changes>` 规则，可以自动间隔性执行bgsave命令

```bash
# SNAPSHOTTING  ################################
#
# Save the DB on disk:
#
#   save <seconds> <changes>
#
#   Will save the DB if both the given number of seconds and the given
#   number of write operations against the DB occurred.
#
#   In the example below the behaviour will be to save:
#   after 900 sec (15 min) if at least 1 key changed
#   after 300 sec (5 min) if at least 10 keys changed
#   after 60 sec if at least 10000 keys changed
#
#   Note: you can disable saving completely by commenting out all "save" lines.
#
#   It is also possible to remove all the previously configured save
#   points by adding a save directive with a single empty string argument
#   like in the following example:
#
#   save ""

save 900 1
save 300 10
save 60 10000
# save <seconds> <changes>表示在seconds秒内，至少有changes次变化，就会自动触发gbsave命令

save 900 1  # 当时间到900秒时，如果至少有1个key发生变化，就会自动触发bgsave命令创建快照
save 300 10  # 当时间到300秒时，如果至少有10个key发生变化，就会自动触发bgsave命令创建快照
save 60 10000    # 当时间到60秒时，如果至少有10000个key发生变化，就会自动触发bgsave命令创建快照
```

### RDB

RDB 持久化
执行 rdb 持久化时, Redis 会fork 出一个子进程, 子进程将内存中数据写入到一个紧凑的文件中, 因此它保存的是某个时间点的完整数据。

子进程创建后，父子进程共享数据段，父进程继续提供读写服务，写脏的页面数据会逐渐和子进程分离开来。

如有需要，可以保存最近24小时的每小时备份文件，以及每个月每天的备份文件，便于遇到问题时恢复。

Redis 启动时会从 rdb 文件中恢复数据到内存， 因此恢复数据时只需将redis 关闭后，将备份的rdb文件替换当前的rdb文件，再启动Redis即可。

#### 优点

rdb文件体积比较小， 适合备份及传输
性能会比 aof 好 (aof 需要写入日志到文件中)
rdb 恢复比 aof 要更快

#### 缺点

服务器故障时会丢失最后一次备份之后的数据
Redis 保存rdb时， fork子进程的这个操作期间, Redis服务会停止响应(一般是毫秒级)，但如果数据量大且cpu时间紧张，则停止响应的时间可能长达1秒

### AOF 持久化 (Append Only File)

与 RDB 持久化通过保存数据库中的键值对来记录数据库状态不同，AOF持久化是通过保存Redis所执行的写命令来记录数据库状态的。

redis 默认情况是关闭AOF的，所以要使用就要先通过以下方式打开:
第一种方式:
打开 redis.conf  修改以下参数:

appendonly  yes        (默认no,关闭)表示是否开启AOF持久化:  

appendfilename “appendonly.aof”   AOF持久化配置文件的名称: **

默认情况下redis安装目录会生成 appendonly.aof文件，如果没有则执行以下方式
第二种方式:
在cmd通过redis-cli连接到服务器的命令界面里
输入
config set appendonly yes
config set save “” (可选)

执行的第一条命令开启了 AOF 功能:  Redis 会阻塞直到初始 AOF 文件创建完成为止， 之后 Redis 会继续处理命令请求， 并开始将写入命令追加到 AOF 文件末尾。

执行的第二条命令用于关闭 RDB 功能。 这一步是可选的， 如果你愿意的话， 也可以同时使用 RDB 和 AOF 这两种持久化功能。 (如果RDB和AOF同时开启，则AOF优先加载)

AOF如何实现持久化
AOF持久化功能的实现可以分为命令追加、文件写入、文件同步三个步骤。

命令追加:

当AOF持久化功能打开时，服务器在执行完一个写命令之后，会以协议格式将被执行的写命令追加到服务器状态的aof_buf缓冲区的末尾。

AOF文件的写入与同步:

每当服务器常规任务函数被执行、 或者事件处理器被执行时， aof.c/flushAppendOnlyFile 函数都会被调用， 这个函数执行以下两个工作:

WRITE: 根据条件，将 aof_buf 中的缓存写入到 AOF 文件。

SAVE: 根据条件，调用 fsync 或 fdatasync 函数，将 AOF 文件保存到磁盘中。

两个步骤都需要根据一定的条件来执行， 而这些条件由 AOF 所使用的保存模式来决定， 以下小节就来介绍 AOF 所使用的三种保存模式， 以及在这些模式下， 步骤 WRITE 和 SAVE 的调用条件。

Redis 目前支持三种 AOF 保存模式，它们分别是:

AOF_FSYNC_NO : 不保存。

AOF_FSYNC_EVERYSEC : 每一秒钟保存一次。

AOF_FSYNC_ALWAYS : 每执行一个命令保存一次。

不保存 (AOF_FSYNC_NO)

在这种模式下， 每次调用 flushAppendOnlyFile 函数， WRITE 都会被执行， 但 SAVE 会被略过。

在这种模式下， SAVE 只会在以下任意一种情况中被执行:

Redis 被关闭

AOF 功能被关闭

系统的写缓存被刷新 (可能是缓存已经被写满，或者定期保存操作被执行)

这三种情况下的 SAVE 操作都会引起 Redis 主进程阻塞。

每一秒钟保存一次 (AOF_FSYNC_EVERYSEC)

在这种模式中， SAVE 原则上每隔一秒钟就会执行一次， 因为 SAVE 操作是由后台子线程调用的， 所以它不会引起服务器主进程阻塞。

注意， 在上一句的说明里面使用了词语“原则上”， 在实际运行中， 程序在这种模式下对 fsync 或 fdatasync 的调用并不是每秒一次， 它和调用 flushAppendOnlyFile 函数时 Redis 所处的状态有关。

每当 flushAppendOnlyFile 函数被调用时， 可能会出现以下四种情况:

子线程正在执行 SAVE ，并且:

这个 SAVE 的执行时间未超过 2 秒，那么程序直接返回，并不执行 WRITE 或新的 SAVE 。

这个 SAVE 已经执行超过 2 秒，那么程序执行 WRITE ，但不执行新的 SAVE 。注意，因为这时 WRITE 的写入必须等待子线程先完成 (旧的)  SAVE ，因此这里 WRITE 会比平时阻塞更长时间。

子线程没有在执行 SAVE ，并且:

上次成功执行 SAVE 距今不超过 1 秒，那么程序执行 WRITE ，但不执行 SAVE 。

上次成功执行 SAVE 距今已经超过 1 秒，那么程序执行 WRITE 和 SAVE 。

可以用流程图表示这四种情况:

根据以上说明可以知道， 在“每一秒钟保存一次”模式下， 如果在情况 1 中发生故障停机， 那么用户最多损失小于 2 秒内所产生的所有数据。

如果在情况 2 中发生故障停机， 那么用户损失的数据是可以超过 2 秒的。

Redis 官网上所说的， AOF 在“每一秒钟保存一次”时发生故障， 只丢失 1 秒钟数据的说法， 实际上并不准确。

每执行一个命令保存一次 (AOF_FSYNC_ALWAYS)

在这种模式下，每次执行完一个命令之后， WRITE 和 SAVE 都会被执行。

另外，因为 SAVE 是由 Redis 主进程执行的，所以在 SAVE 执行期间，主进程会被阻塞，不能接受命令请求。

AOF 保存模式对性能和安全性的影响

在上一个小节， 我们简短地描述了三种 AOF 保存模式的工作方式， 现在， 是时候研究一下这三个模式在安全性和性能方面的区别了。

对于三种 AOF 保存模式， 它们对服务器主进程的阻塞情况如下:

不保存 (AOF_FSYNC_NO) : 写入和保存都由主进程执行，两个操作都会阻塞主进程。

每一秒钟保存一次 (AOF_FSYNC_EVERYSEC) : 写入操作由主进程执行，阻塞主进程。保存操作由子线程执行，不直接阻塞主进程，但保存操作完成的快慢会影响写入操作的阻塞时长。

每执行一个命令保存一次 (AOF_FSYNC_ALWAYS) : 和模式 1 一样。

因为阻塞操作会让 Redis 主进程无法持续处理请求， 所以一般说来， 阻塞操作执行得越少、完成得越快， Redis 的性能就越好。

模式 1 的保存操作只会在AOF 关闭或 Redis 关闭时执行， 或者由操作系统触发， 在一般情况下， 这种模式只需要为写入阻塞， 因此它的写入性能要比后面两种模式要高， 当然， 这种性能的提高是以降低安全性为代价的:  在这种模式下， 如果运行的中途发生停机， 那么丢失数据的数量由操作系统的缓存冲洗策略决定。

模式 2 在性能方面要优于模式 3 ， 并且在通常情况下， 这种模式最多丢失不多于 2 秒的数据， 所以它的安全性要高于模式 1 ， 这是一种兼顾性能和安全性的保存方案。

模式 3 的安全性是最高的， 但性能也是最差的， 因为服务器必须阻塞直到命令信息被写入并保存到磁盘之后， 才能继续处理请求。

综合起来，三种 AOF 模式的操作特性可以总结如下:

image.png

AOF 文件的读取和数据还原
AOF 文件保存了 Redis 的数据库状态， 而文件里面包含的都是符合 Redis 通讯协议格式的命令文本。

这也就是说， 只要根据 AOF 文件里的协议， 重新执行一遍里面指示的所有命令， 就可以还原 Redis 的数据库状态了。

Redis 读取 AOF 文件并还原数据库的详细步骤如下:

1.创建一个不带网络连接的伪客户端 (fake client) 。

2.读取 AOF 所保存的文本，并根据内容还原出命令、命令的参数以及命令的个数。

3.根据命令、命令的参数和命令的个数，使用伪客户端执行该命令。

4.执行 2 和 3 ，直到 AOF 文件中的所有命令执行完毕。

完成第 4 步之后， AOF 文件所保存的数据库就会被完整地还原出来。

注意， 因为 Redis 的命令只能在客户端的上下文中被执行， 而 AOF 还原时所使用的命令来自于 AOF 文件， 而不是网络， 所以程序使用了一个没有网络连接的伪客户端来执行命令。 伪客户端执行命令的效果， 和带网络连接的客户端执行命令的效果， 完全一样。

### AOF重写

因为AOF持久化是通过保存被执行的写命令来记录数据库状态的，所以随着服务器运行时间的流逝，AOF文件中的内容越来越多，文件体积越来越大，如果不加以控制，会对redis服务器甚至宿主计算器造成影响。

所谓的“重写”其实是一个有歧义的词语， 实际上， AOF 重写并不需要对原有的 AOF 文件进行任何写入和读取， 它针对的是数据库中键的当前值。

考虑这样一个情况， 如果服务器对键 list 执行了以下四条命令:

RPUSH list 1 2 3 4// [1, 2, 3, 4]

RPOP list // [1, 2, 3]

LPOP list // [2, 3]

LPUSH list 1 // [1, 2, 3]

那么当前列表键 list 在数据库中的值就为 [1, 2, 3] 。

如果我们要保存这个列表的当前状态， 并且尽量减少所使用的命令数， 那么最简单的方式不是去 AOF 文件上分析前面执行的四条命令， 而是直接读取 list 键在数据库的当前值， 然后用一条 RPUSH 1 2 3 命令来代替前面的四条命令。

再考虑这样一个例子， 如果服务器对集合键 animal 执行了以下命令:

SADD animal cat// {cat}

SADD animal dog panda tiger// {cat, dog, panda, tiger}

SREManimal cat// {dog, panda, tiger}

SADD animal cat lion// {cat, lion, dog, panda, tiger}

那么使用一条 SADD animal cat lion dog panda tiger 命令， 就可以还原 animal 集合的状态， 这比之前的四条命令调用要大大减少。

除了列表和集合之外， 字符串、有序集、哈希表等键也可以用类似的方法来保存状态， 并且保存这些状态所使用的命令数量， 比起之前建立这些键的状态所使用命令的数量要大大减少。

AOF重写程序aof_rewrite函数可以很好完成创建一个新AOF文件的任务，但是这个函数会进行大量写入操作，会长时间阻塞，所以Redis将AOF重写程序放到子进程里执行，这样做达到两个目的:

·子进程AOF重写期间，服务器进程可以继续处理命令请求。

·子进程带有数据库进程的数据副本，使用子进程而不是线程，可以避免使用锁的情况下保证数据安全。

不过，使用子进程也有一个问题需要解决，就是AOF重写期间如果有新的写命令进来，不能漏掉，那样会数据不一致。

于是Redis服务器设置了一个AOF重写缓冲区

最后流程变为:

1.执行客户端发来的命令

2.将执行的写命令追加到AOF缓冲区

3.将执行后的写命令追加到AOF重写缓冲区

这样一来可以保证:

·AOF缓冲区的内容会定期被写入和同步到AOF文件，对现有AOF文件的处理工作会照常进行。

·从创建子进程开始，服务器执行的所有写命令会被记录到AOF重写缓冲区里面

当子进程完成AOF重写工作之后，它会向父进程发送一个信号，父进程收到信号后，会调用一个信号处理函数，并执行以下工作:

1.将AOF重写缓冲区中的所有内容写入新的AOF文件中，这时新AOF文件锁保存的数据库状态和服务器当前状态一致

2.对新的AOF文件进行改名，原子性操作地覆盖现有的AOF文件，完成新旧AOF文件的替换。

这个信号函数执行完毕以后，父进程就可以继续像往常一样接受命令请求了，在整个AOF后台重写过程中，只有信号处理函数执行时会对服务器进程造成阻塞，其他时候都可以继续处理请求，这样AOF重写对服务器性能造成的影响降到了最低。

以上就是AOF后台重写，也即是BGREWRITEAOF命令的实现原理。

#### AOF的缺点

- 体积大: 对于相同的数据集来说，AOF文件的体积通常要大于 RDB文件的体积。
- 性能差: 根据所使用的Fsync策略，AOF的速度可能会慢于 RDB。在一般情况下，每秒Fsync的性能依然非常高，而关闭 Fsync可以让 AOF的速度和 RDB一样快，即使在高负荷之下也是如此。不过在处理巨大的写入载入时，RDB可以提供更有保证的最大延迟时间(Latency)。

AOF 其实就是将客户端每一次操作记录追加到指定的aof (日志) 文件中，在aof文件体积多大时可以自动在后台重写aof文件 (期间不影响正常服务，中途磁盘写满或停机等导致失败也不会丢失数据)

aof 持久化的fsync策略支持:

不执行 fsync: 由操作系统保证数据同步到磁盘(linux 默认30秒)， 速度最快
每秒1次: 最多丢失最近1s的数据 (推荐)
每条命令: 绝对保证数据持久化 (影响性能)
fsync: 同步内存中所有已修改的文件数据到储存设备
aof 文件是一个只追加的文件, 若写入了不完整的命令(磁盘满, 停机...)时, 可用自带的 redis-check-aof 工具轻易修复问题: 执行redis-check-aof --fix

aof文件过大时会触发自动重写, 重写后的新aof文件包含了恢复当前数据集所需的最少的命令集合.

客户端多次对同一个键 incr 时, 操作N次则会写入N条, 但实际上只需一条 set 命令就可以保存该值, 重建就是生成足够重建当前数据集的最少命令。
Redis 重写aof操作同样是通过 fork 子进程来处理的.
Redis 运行时打开 aof:

redis-cli> CONFIG SET appendonly yes
仅当前实例生命周期内有效
优点
充分保证数据的持久化，正确的配置一般最多丢失1秒的数据
aof 文件内容是以Redis协议格式保存， 易读
缺点
aof 文件通常大于 rdb 文件
速度会慢于rdb, 具体得看具体fsyn策略
重新启动redis时会极低的概率会导致无法将数据集恢复成保存时的原样(概率极低, 但确实出现过)

```bash
############### rdb ###############
save 600 1
save 300 20000
save 60 80000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump_7000.rdb
# redis不会自动 创建此目录
dir /data/redisdata
```

关于Redis说点什么，目前都是使用Redis作为数据缓存，缓存的目标主要是那些需要经常访问的数据，或计算复杂而耗时的数据。缓存的效果就是减少了数据库读的次数，减少了复杂数据的计算次数，从而提高了服务器的性能。

一、redis持久化--两种方式
  
1. redis提供了两种持久化的方式，分别是RDB (Redis DataBase) 和AOF (Append Only File) 。

2. RDB，简而言之，就是在不同的时间点，将redis存储的数据生成快照并存储到磁盘等介质上；

3. AOF，则是换了一个角度来实现持久化，那就是将redis执行过的所有写指令记录下来，在下次redis重新启动时，只要把这些写指令从前到后再重复执行一遍，就可以实现数据恢复了。

4. 其实RDB和AOF两种方式也可以同时使用，在这种情况下，如果redis重启的话，则会优先采用AOF方式来进行数据恢复，这是因为AOF方式的数据恢复完整度更高。

5. 如果你没有数据持久化的需求，也完全可以关闭RDB和AOF方式，这样的话，redis将变成一个纯内存数据库，就像memcache一样。

二、redis持久化--RDB
  
1. RDB方式，是将redis某一时刻的数据持久化到磁盘中，是一种快照式的持久化方法。

2. redis在进行数据持久化的过程中，会先将数据写入到一个临时文件中，待持久化过程都结束了，才会用这个临时文件替换上次持久化好的文件。正是这种特性，让我们可以随时来进行备份，因为快照文件总是完整可用的。

3. 对于RDB方式，redis会单独创建 (fork) 一个子进程来进行持久化，而主进程是不会进行任何IO操作的，这样就确保了redis极高的性能。

4. 如果需要进行大规模数据的恢复，且对于数据恢复的完整性不是非常敏感，那RDB方式要比AOF方式更加的高效。

5. 虽然RDB有不少优点，但它的缺点也是不容忽视的。如果你对数据的完整性非常敏感，那么RDB方式就不太适合你，因为即使你每5分钟都持久化一次，当redis故障时，仍然会有近5分钟的数据丢失。所以，redis还提供了另一种持久化方式，那就是AOF。

三、redis持久化--AOF
  
1. AOF，英文是Append Only File，即只允许追加不允许改写的文件。

2. 如前面介绍的，AOF方式是将执行过的写指令记录下来，在数据恢复时按照从前到后的顺序再将指令都执行一遍，就这么简单。

3. 我们通过配置redis.conf中的appendonly yes就可以打开AOF功能。如果有写操作 (如SET等) ，redis就会被追加到AOF文件的末尾。

4. 默认的AOF持久化策略是每秒钟fsync一次 (fsync是指把缓存中的写指令记录到磁盘中) ，因为在这种情况下，redis仍然可以保持很好的处理性能，即使redis故障，也只会丢失最近1秒钟的数据。

5如果在追加日志时，恰好遇到磁盘空间满、inode满或断电等情况导致日志写入不完整，也没有关系，redis提供了redis-check-aof工具，可以用来进行日志修复。

6. 因为采用了追加方式，如果不做任何处理的话，AOF文件会变得越来越大，为此，redis提供了AOF文件重写 (rewrite) 机制，即当AOF文件的大小超过所设定的阈值时，redis就会启动AOF文件的内容压缩，只保留可以恢复数据的最小指令集。举个例子或许更形象，假如我们调用了100次INCR指令，在AOF文件中就要存储100条指令，但这明显是很低效的，完全可以把这100条指令合并成一条SET指令，这就是重写机制的原理。

7. 在进行AOF重写时，仍然是采用先写临时文件，全部完成后再替换的流程，所以断电、磁盘满等问题都不会影响AOF文件的可用性，这点大家可以放心。

8. AOF方式的另一个好处，我们通过一个"场景再现"来说明。某同学在操作redis时，不小心执行了FLUSHALL，导致redis内存中的数据全部被清空了，这是很悲剧的事情。不过这也不是世界末日，只要redis配置了AOF持久化方式，且AOF文件还没有被重写 (rewrite) ，我们就可以用最快的速度暂停redis并编辑AOF文件，将最后一行的FLUSHALL命令删除，然后重启redis，就可以恢复redis的所有数据到FLUSHALL之前的状态了。是不是很神奇，这就是AOF持久化方式的好处之一。但是如果AOF文件已经被重写了，那就无法通过这种方法来恢复数据了。

9. 虽然优点多多，但AOF方式也同样存在缺陷，比如在同样数据规模的情况下，AOF文件要比RDB文件的体积大。而且，AOF方式的恢复速度也要慢于RDB方式。

如果你直接执行BGREWRITEAOF命令，那么redis会生成一个全新的AOF文件，其中便包括了可以恢复现有数据的最少的命令集。

10. 如果运气比较差，AOF文件出现了被写坏的情况，也不必过分担忧，redis并不会贸然加载这个有问题的AOF文件，而是报错退出。这时可以通过以下步骤来修复出错的文件:

1.备份被写坏的AOF文件
  
2.运行redis-check-aof –fix进行修复
  
3.用diff -u来看下两个文件的差异，确认问题点
  
4.重启redis，加载修复后的AOF文件

四、redis持久化--AOF重写
  
1. AOF重写的内部运行原理，我们有必要了解一下。

2. 在重写即将开始之际，redis会创建 (fork) 一个"重写子进程"，这个子进程会首先读取现有的AOF文件，并将其包含的指令进行分析压缩并写入到一个临时文件中。

3. 与此同时，主工作进程会将新接收到的写指令一边累积到内存缓冲区中，一边继续写入到原有的AOF文件中，这样做是保证原有的AOF文件的可用性，避免在重写过程中出现意外。

4. 当"重写子进程"完成重写工作后，它会给父进程发一个信号，父进程收到信号后就会将内存中缓存的写指令追加到新AOF文件中。

5. 当追加结束后，redis就会用新AOF文件来代替旧AOF文件，之后再有新的写指令，就都会追加到新的AOF文件中了。

五、redis持久化--如何选择RDB和AOF
  
1. 对于我们应该选择RDB还是AOF，官方的建议是两个同时使用。这样可以提供更可靠的持久化方案。

2. redis的备份和还原，可以借助第三方的工具redis-dump。

六、Redis的两种持久化方式也有明显的缺点
  
1. RDB需要定时持久化，风险是可能会丢两次持久之间的数据，量可能很大。

2. AOF每秒fsync一次指令硬盘，如果硬盘IO慢，会阻塞父进程；风险是会丢失1秒多的数据；在Rewrite过程中，主进程把指令存到mem-buffer中，最后写盘时会阻塞主进程。

3. 这两个缺点是个很大的痛点。为了解决这些痛点，GitHub的两位工程师 Bryana Knight 和 Miguel Fernández 日前写了一篇 文章 ，讲述了将持久数据从Redis迁出的经验:

[http://www.open-open.com/lib/view/open1487736984424.html](http://www.open-open.com/lib/view/open1487736984424.html)
  
### AOF持久化

AOF (Append-Only-File) 持久化即记录所有变更数据库状态的指令，以append的形式追加保存到AOF文件中。在服务器下次启动时，就可以通过载入和执行AOF文件中保存的命令，来还原服务器关闭前的数据库状态。

redis.conf中AOF持久化配置如下

## 默认关闭AOF，若要开启将no改为yes

appendonly no

append文件的名字

appendfilename "appendonly.aof"

每隔一秒将缓存区内容写入文件 默认开启的写入方式

appendfsync everysec

当AOF文件大小的增长率大于该配置项时自动开启重写 (这里指超过原大小的100%)

auto-aof-rewrite-percentage 100

当AOF文件大小大于该配置项时自动开启重写

auto-aof-rewrite-min-size 64mb
AOF持久化的实现包括3个步骤:

命令追加: 将命令追加到AOF缓冲区
文件写入: 缓冲区内容写到AOF文件
文件保存: AOF文件保存到磁盘
其中后两步的频率通过appendfsync来配置，appendfsync的选项包括

always， 每执行一个命令就保存一次，安全性最高，最多只丢失一个命令的数据，但是性能也最低 (频繁的磁盘IO)
everysec，每一秒保存一次，推荐使用，在安全性与性能之间折中，最多丢失一秒的数据
no， 依赖操作系统来执行 (一般大概30s一次的样子) ，安全性最低，性能最高，丢失操作系统最后一次对AOF文件触发SAVE操作之后的数据
AOF通过保存命令来持久化，随着时间的推移，AOF文件会越来越大，Redis通过AOF文件重写来解决AOF文件不断增大的问题 (可以减少文件的磁盘占有量，加快数据恢复的速度) ，原理如下:

调用fork，创建一个子进程

子进程读取当前数据库的状态来“重写”一个新的AOF文件 (这里虽然叫“重写”，但实际并没有对旧文件进行任何读取，而是根据数据库的当前状态来形成指令)

主进程持续将新的变动同时写到AOF重写缓冲区与原来的AOF缓冲区中

主进程获取到子进程重写AOF完成的信号，调用信号处理函数将AOF重写缓冲区内容写入新的AOF文件中，并对新文件进行重命名，原子地覆盖原有AOF文件，完成新旧文件的替换

AOF的重写也分为手动触发与自动触发

手动触发:  直接调用bgrewriteaof命令
自动触发:  根据auto-aof-rewrite-min-size和auto-aof-rewrite-percentage参数确定自动触发时机。其中auto-aof-rewrite-min-size表示运行AOF重写时文件最小体积，默认为64MB。auto-aof-rewrite-percentage表示当前AOF文件大小 (aof_current_size) 和上一次重写后AOF文件大小 (aof_base_size) 的比值。自动触发时机为 aof_current_size > auto-aof-rewrite-min-size && (aof_current_size - aof_base_size) /aof_base_size> = auto-aof-rewrite-percentage

---

版权声明: 本文为CSDN博主「ljheee」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: [https://blog.csdn.net/ljheee/article/details/76284082](https://blog.csdn.net/ljheee/article/details/76284082)

[https://zhuanlan.zhihu.com/p/98497789](https://zhuanlan.zhihu.com/p/98497789)

[https://segmentfault.com/a/1190000022792882](https://segmentfault.com/a/1190000022792882)

作者: TurboSnail
链接: [https://juejin.cn/post/6844903939339452430](https://juejin.cn/post/6844903939339452430)
来源: 掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
