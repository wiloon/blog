---
author: "-"
date: "2020-08-02 19:10:49" 
title: "vlan"
categories:
  - inbox
tags:
  - reprint
---
## "vlan"

vlan范围: 0~4095
    0,4095 保留 仅限系统使用 用户不能查看和使用这些VLAN  
    1 正常 Cisco默认VLAN 用户能够使用该VLAN,但不能删除它  
    2-1001 正常 用于以太网的VLAN 用户可以创建、使用和删除这些VLAN  
    1002-1005 正常 用于 FDDI 和令牌环的 Cisco 默认 VLAN 用户不能删除这些 VLAN  
    1006-1024 保留 仅限系统使用 用户不能查看和使用这些VLAN  
    1025-4094 扩展 仅用于以太网VLAN  

|            |            |           |               |              |
|------------|------------|-----------|---------------|--------------|
|            | Tagged 数据帧 | Tagged数据帧 | Untagged数据帧   | Untagged数据帧  |  
|            | in         | out       | in            | out          |
| Tagged端口   | 原样接收       | 原样发送      | 按端口PVID打TAG标记 | 按照PVID打TAG标记 |
| Untagged端口 | 丢弃         | 去掉TAG标记   | 按端口PVID打TAG标记 | 原样发送         |

2 、所谓的Untagged Port和tagged Port不是讲述物理端口的状态,而是将是物理端口所拥有的某一个VID的状态,所以一个物理端口可以在某一个VID上是Untagged Port,在另一个VID上是tagged Port；

3 、一个物理端口只能拥有一个PVID,当一个物理端口拥有了一个PVID的时候,必定会拥有和PVID的TAG等同的VID,而且在这个VID上,这个物理端口必定是Untagged Port；
4. PVID的作用只是在交换机从外部接受到可以接受Untagged 数据帧的时候给数据帧添加TAG标记用的,在交换机内部转发数据的时候PVID不起任何作用；
5. 拥有和TAG标记一致的VID的物理端口,不论是否在这个VID上是Untagged Port或者tagged Port,都可以接受来自交换机内部的标记了这个TAG标记的tagged 数据帧；
6. 拥有和TAG标记一致的VID的物理端口,只有在这个VID上是tagged Port,才可以接受来自交换机外部的标记了这个TAG标记的tagged 数据帧；

[https://www.cnblogs.com/iiiiher/p/8067226.html](https://www.cnblogs.com/iiiiher/p/8067226.html)
