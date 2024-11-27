---
title: memcache basic,command
author: "-"
date: 2018-01-05T09:00:17+00:00
url: memcache
categories:
  - Inbox
tags:
  - reprint
---
## memcache basic,command

### run as docker

```bash
podman run \
--name memcache \
-d \
-p 11211:11211 \
-v /etc/localtime:/etc/localtime:ro \
memcached -m 16
```

### connect

```bash
    telnet HOST PORT
```

### set

```bash
    set key flags exptime bytes [noreply]
    value

# 参数说明如下: 

key: 键值 key-value 结构中的 key,用于查找缓存值。
flags: 可以包括键值对的整型参数, 客户机使用它存储关于键值对的额外信息
exptime: 在缓存中保存键值对的时间长度 (以秒为单位,0 表示永远) 
bytes: 在缓存中存储的字节数
noreply (可选) :  该参数告知服务器不需要返回数据
value: 存储的值 (始终位于第二行)  (可直接理解为key-value结构中的value) 

### 示例
set foo 0 0 3
bar

#获取存储在 key(键) 中的 value(数据值) ,如果 key 不存在,则返回空。
get key

# 删除key
delete <key>

#输出各个slab中的item的数目和最老item的年龄(最后一次访问距离现在的秒数) .
stats items

# 根据<slab_id>输出相同的<slab_id>中的item信息。是输出的个数,当为0是输出所有的item。
stats cachedump <slab_id> 

#显示各个slab的信息,包括chunk的大小、数目、使用情况等。
stats slabs

```

Memcached 连接
  
我们可以通过 telnet 命令并指定主机ip和端口来连接 Memcached 服务。

语法
  
telnet HOST PORT
  
命令中的 HOST 和 PORT 为运行 Memcached 服务的 IP 和 端口。

实例
  
以下实例演示了如何连接到 Memcached 服务并执行简单的 set 和 get 命令。

本实例的 Memcached 服务运行的主机为 127.0.0.1 (本机)  、端口为 11211。

telnet 127.0.0.1 11211

Trying 127.0.0.1...

Connected to 127.0.0.1.

Escape character is '^]'.

set foo 0 0 3 保存命令

bar 数据

STORED 结果

get foo 取得命令

VALUE foo 0 3 数据

bar 数据

END 结束行

quit 退出

memcached go
  
[https://github.com/bradfitz/gomemcache](https://github.com/bradfitz/gomemcache)
  
[http://blog.51cto.com/151wqooo/1309088](http://blog.51cto.com/151wqooo/1309088)
