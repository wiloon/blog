---
title: UUID
author: "-"
date: 2016-02-29T04:51:08+00:00
url: /?p=8753
categories:
  - Uncategorized

tags:
  - reprint
---
## UUID

UUID是什么?

UUID(Universally Unique Identifier)全局唯一标识符,是指在一台机器上生成的数字,它保证对在同一时空中的所有机器都是唯一的。按照开放软件基金会(OSF)制定的标准计算,用到了以太网卡地址、纳秒级时间、芯片ID码和许多可能的数字。由以下几部分的组合: 当前日期和时间(UUID的第一个部分与时间有关,如果你在生成一个UUID之后,过几秒又生成一个UUID,则第一个部分不同,其余相同),时钟序列,全局唯一的IEEE机器识别号 (如果有网卡,从网卡获得,没有网卡以其他方式获得) ,UUID的唯一缺陷在于生成的结果串会比较长。

A universally unique identifier (UUID) is an identifier standard used in software construction, standardized by the Open Software Foundation (OSF) as part of the Distributed Computing Environment (DCE). The intent of UUIDs is to enable distributed systems to uniquely identify information without significant central coordination. In this context the word unique should be taken to mean "practically unique" rather than "guaranteed unique". Since the identifiers have a finite size it is possible for two differing items to share the same identifier. The identifier size and generation process need to be selected so as to make this sufficiently improbable in practice. Anyone can create a UUID and use it to identify something with reasonable confidence that the same identifier will never be unintentionally created by anyone to identify something else. Information labeled with UUIDs can therefore be later combined into a single database without needing to resolve name conflicts.

A UUID is 128 bits long, and can guarantee uniqueness across space and time.  UUIDs were originally used in the Apollo Network Computing System and later in the Open Software Foundation's (OSF) Distributed Computing Environment (DCE), and then in Microsoft Windows platforms.

上面说的到在grub中写到的UUID的的好处是什么呢？

这样做和使用/dev/sda5这种直接引用分区的方法的一个优点就是,当硬盘中增加了新的分区,或者分区的顺序改变后,仍然能够保证系统加载分区到正确的加载点。

这对于swap分区尤为重要,如果硬盘分区顺序改变,而fstab对swap分区编号做响应的调整,是不是会把其他分区给作为swap哪？结果是很可怕的,这个分区上的数据恐怕就要不保了。通过在/dev/disk/uuid,这里的uuid列表实际上是一些symbol link文件,系统可以保证针对每一个分区生成一个唯一的编码,增加了系统的稳定性。
  
UUID具有以下涵义: 

经由一定的算法机器生成
  
为了保证UUID的唯一性,规范定义了包括网卡MAC地址、时间戳、名字空间 (Namespace) 、随机或伪随机数、时序等元素,以及从这些元素生成UUID的算法。UUID的复杂特性在保证了其唯一性的同时,意味着只能由计算机生成。

非人工指定,非人工识别
  
UUID是不能人工指定的,除非你冒着UUID重复的风险。UUID的复杂性决定了"一般人"不能直接从一个UUID知道哪个对象和它关联。

在特定的范围内重复的可能性极小
  
UUID的生成规范定义的算法主要目的就是要保证其唯一性。但这个唯一性是有限的,只在特定的范围内才能得到保证,这和UUID的类型有关 (参见UUID的版本) 。

UUID是16字节128位长的数字,通常以36字节的字符串表示,示例如下: 

3F2504E0-4F89-11D3-9A0C-0305E82C3301

其中的字母是16进制表示,大小写无关。
  
GUID (Globally Unique Identifier) 是UUID的别名；但在实际应用中,GUID通常是指微软实现的UUID。

UUID的版本

UUID具有多个版本,每个版本的算法不同,应用范围也不同。
  
首先是一个特例－－Nil UUID－－通常我们不会用到它,它是由全为0的数字组成,如下: 
  
00000000-0000-0000-0000-000000000000

UUID Version 1: 基于时间的UUID
  
基于时间的UUID通过计算当前时间戳、随机数和机器MAC地址得到。由于在算法中使用了MAC地址,这个版本的UUID可以保证在全球范围的唯一性。但与此同时,使用MAC地址会带来安全性问题,这就是这个版本UUID受到批评的地方。如果应用只是在局域网中使用,也可以使用退化的算法,以IP地址来代替MAC地址－－Java的UUID往往是这样实现的 (当然也考虑了获取MAC的难度) 。

UUID Version 2: DCE安全的UUID
  
DCE (Distributed Computing Environment) 安全的UUID和基于时间的UUID算法相同,但会把时间戳的前4位置换为POSIX的UID或GID。这个版本的UUID在实际中较少用到。

UUID Version 3: 基于名字的UUID (MD5) 
  
基于名字的UUID通过计算名字和名字空间的MD5散列值得到。这个版本的UUID保证了: 相同名字空间中不同名字生成的UUID的唯一性；不同名字空间中的UUID的唯一性；相同名字空间中相同名字的UUID重复生成是相同的。

UUID Version 4: 随机UUID
  
根据随机数,或者伪随机数生成UUID。这种UUID产生重复的概率是可以计算出来的,但随机的东西就像是买彩票: 你指望它发财是不可能的,但狗屎运通常会在不经意中到来。

UUID Version 5: 基于名字的UUID (SHA1) 
  
和版本3的UUID算法类似,只是散列值计算使用SHA1 (Secure Hash Algorithm 1) 算法。

UUID的应用

从UUID的不同版本可以看出,Version 1/2适合应用于分布式计算环境下,具有高度的唯一性；Version 3/5适合于一定范围内名字唯一,且需要或可能会重复生成UUID的环境下；至于Version 4,我个人的建议是最好不用 (虽然它是最简单最方便的) 。
  
通常我们建议使用UUID来标识对象或持久化数据,但以下情况最好不使用UUID: 
  
映射类型的对象。比如只有代码及名称的代码表。
  
人工维护的非系统生成对象。比如系统中的部分基础数据。
  
对于具有名称不可重复的自然特性的对象,最好使用Version 3/5的UUID。比如系统中的用户。如果用户的UUID是Version 1的,如果你不小心删除了再重建用户,你会发现人还是那个人,用户已经不是那个用户了。 (虽然标记为删除状态也是一种解决方案,但会带来实现上的复杂性。) 

UUID生成器

我没想着有人看完了这篇文章就去自己实现一个UUID生成器,所以前面的内容并不涉及算法的细节。下面是一些可用的Java UUID生成器: 
  
Java UUID Generator (JUG): 开源UUID生成器,LGPL协议,支持MAC地址。
  
UUID: 特殊的License,有源码。
  
Java 5以上版本中自带的UUID生成器: 好像只能生成Version 3/4的UUID。

此外,Hibernate中也有一个UUID生成器,但是,生成的不是任何一个 (规范) 版本的UUID,强烈不建议使用。

第一次看到UUID这个东西,是在Ubuntu系统中看到/boot/grub/grub.cfg中对kernel的配置: 
  
linux   /boot/vmlinuz-2.6.31-14-generic root=UUID=c74288db-c35e-4d7e-a1e8-82d6e8eff5cf
  
后来在分区表/etc/fstab中也有出现UUID。

获取设备的UUID的方法 (Linux系统中) :

1) # blkid /dev/sda1 (不是root用户需要sudo)
  
/dev/sda1: LABEL="/axs3" UUID="298d198d-aa60-48af-a9f4-638f8f274afa" SEC_TYPE="ext2" TYPE="ext3"

2) # tune2fs -l /dev/sda1 |grep 'UUID'
  
298d198d-aa60-48af-a9f4-638f8f274afa

3)# ls -l /dev/disk/by-uuid/ |grep sda1 |awk '{print $8}'
  
298d198d-aa60-48af-a9f4-638f8f274afa

4) #scsi_id -p 0x80/0x83 -s /block/sda1    应该只对SCSI设备有效。

5) # dumpe2fs /dev/sda1 |grep 'UUID'
  
dumpe2fs 1.39 (29-May-2006)
  
Filesystem UUID:       298d198d-aa60-48af-a9f4-638f8f274afa
  
这个命令不建议使用,要是分区比较大,耗时还是比较长的

6)# vol_id /dev/sda1 |grep 'UUID'
  
ID_FS_UUID=298d198d-aa60-48af-a9f4-638f8f274afa
  
ID_FS_UUID_ENC=298d198d-aa60-48af-a9f4-638f8f274afa
  
http://blog.chinaunix.net/uid-26495963-id-3150576.html

http://www.cnblogs.com/jdonson/archive/2009/07/22/1528466.html


http://blog.csdn.net/wangshubo1989/article/details/73993485

什么是uuid?

uuid是Universally Unique Identifier的缩写,即通用唯一识别码。

uuid的目的是让分布式系统中的所有元素,都能有唯一的辨识资讯,而不需要透过中央控制端来做辨识资讯的指定。如此一来,每个人都可以建立不与其它人冲突的 uuid。

A universally unique identifier (UUID) is a 128-bit number used to identify information in computer systems.

### Java
```java
    package com.mytest;
      
    import java.util.UUID;
      
    public class UTest {
          
    public static void main(String[] args) {
              
    UUID uuid = UUID.randomUUID();
              
    System.out.println(uuid);
      
    }}
```
### c++中生成uuid: 
```c
    #pragma comment(lib, "rpcrt4.lib")
      
    #include <windows.h>
      
    #include <iostream>

    using namespace std;

    int main()
      
    {
          
    UUID uuid;
          
    UuidCreate(&uuid);
          
    char _str;
          
    UuidToStringA(&uuid, (RPC_CSTR_)&str);
          
    cout<<str<<endl;
          
    RpcStringFreeA((RPC_CSTR*)&str);
          
    return 0;
      
    }
```

### golang uuid
```go
    "github.com/google/uuid"
      u := uuid.New().String()
```
github.com/satori/go.uuid

目前,golang中的uuid还没有纳入标准库,我们使用github上的开源库: 

go get -u github.com/satori/go.uuid

使用: 
```go
    package main

    import (
          
    "fmt"
          
    "github.com/satori/go.uuid"
      
    )

    func main() {
          
    // 创建
          
    u1 := uuid.NewV4()
          
    fmt.Printf("UUIDv4: %s\n", u1)

        // 解析
        u2, err := uuid.FromString("f5394eef-e576-4709-9e4b-a7c231bd34a4")
        if err != nil {
            fmt.Printf("Something gone wrong: %s", err)
            return
        }
        fmt.Printf("Successfully parsed: %s", u2)
        

    }
```
uuid在websocket中使用

这里就是一个简单的使用而已,在websocket中为每一个连接的客户端分配一个uuid。

golang中可以使用github.com/gorilla/websocket为我们提供的websocket开发包。

声明一个客户端结构体: 

type Client struct {
      
id string
      
socket *websocket.Conn
      
send chan []byte
  
}

使用: 

client := &Client{id: uuid.NewV4().String(), socket: conn, send: make(chan []byte)}





http://javag.iteye.com/blog/127753
  
UUID(Universally Unique Identifier)全局唯一标识符,是指在一台机器上生成的数字,它保证对在同一时空中的所有机器都是唯一的。按照开放软件基金会(OSF)制定的标准计算,用到了以太网卡地址、纳秒级时间、芯片ID码和许多可能的数字。由以下几部分的组合: 当前日期和时间(UUID的第一个部分与时间有关,如果你在生成一个UUID之后,过几秒又生成一个UUID,则第一个部分不同,其余相同),时钟序列,全局唯一的IEEE机器识别号 (如果有网卡,从网卡获得,没有网卡以其他方式获得) ,UUID的唯一缺陷在于生成的结果串会比较长。
  
在Java中生成UUID主要有以下几种方式:

JDK1.5
  
如果使用的JDK1.5的话,那么生成UUID变成了一件简单的事,以为JDK实现了UUID:
  
java.util.UUID,直接调用即可.
  
UUID uuid = UUID.randomUUID();
  
String s = UUID.randomUUID().toString();

UUID是由一个十六进制形式的数字组成,表现出来的形式例如
  
550E8400-E29B-11D4-A716-446655440000

//下面就是实现为数据库获取一个唯一的主键id的代码
  
public class UUIDGenerator {
      
public UUIDGenerator() {
      
}
      
/**
       
* 获得一个UUID
       
* @return String UUID
       
*/
      
public static String getUUID(){
          
String s = UUID.randomUUID().toString();
          
//去掉"-"符号
          
return s.substring(0,8)+s.substring(9,13)+s.substring(14,18)+s.substring(19,23)+s.substring(24);
      
}
      
/**
       
* 获得指定数目的UUID
       
* @param number int 需要获得的UUID数量
       
* @return String[] UUID数组
       
*/
      
public static String[] getUUID(int number){
          
if(number < 1){ return null; } String[] ss = new String[number]; for(int i=0;i<number;i++){ ss[i] = getUUID(); } return ss; } public static void main(String[] args){ String[] ss = getUUID(10); for(int i=0;i<ss.length;i++){ System.out.println(ss[i]); } } }


