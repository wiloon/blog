---
title: "failover, failfast, failback, failsafe"
author: "-"
date: "2021-07-06 06:44:36"
url: "failover"
categories:
  - inbox
tags:
  - inbox
---
## "failover, failfast, failback, failsafe"

### failover: 失效转移/故障转移

故障转移（fail-over）

Fail-Over 的含义为“失效转移”，是一种备份操作模式，当主要组件异常时，其功能转移到备份组件。其要点在于有主有备，且主故障时备可启用，并设置为主。如MySQL的双Master模式，当正在使用的Master出现故障时，可以拿备Master做主使用

通俗地说，即当A无法为客户服务时，系统能够自动地切换，使B能够及时地顶上继续为客户提供服务，且客户感觉不到这个为他提供服务的对象已经更换。

这里的A和B可以存在于各种领域，但一般fail-over特指计算机领域的数据库、应用服务、硬件设备等的失效转移。

### failfast: 快速失败

从字面含义看就是“快速失败”，尽可能的发现系统中的错误，使系统能够按照事先设定好的错误的流程执行，对应的方式是“fault-tolerant (错误容忍) ”。以JAVA集合 (Collection) 的快速失败为例，当多个线程对同一个集合的内容进行操作时，就可能会产生fail-fast事件。例如: 当某一个线程A通过iterator去遍历某集合的过程中，若该集合的内容被其他线程所改变了；那么线程A访问集合时，就会抛出ConcurrentModificationException异常 (发现错误执行设定好的错误的流程) ，产生fail-fast事件。

### failback: 失效自动恢复

Fail-over 之后的自动恢复，在簇网络系统 (有两台或多台服务器互联的网络) 中，由于要某台服务器进行维修，需要网络资源和服务暂时重定向到备用系统。在此之后将网络资源和服务器恢复为由原始主机提供的过程，称为自动恢复

### failsafe: 失效安全

Fail-Safe的含义为“失效安全”，即使在故障的情况下也不会造成伤害或者尽量减少伤害。维基百科上一个形象的例子是红绿灯的“冲突监测模块”当监测到错误或者冲突的信号时会将十字路口的红绿灯变为闪烁错误模式，而不是全部显示为绿灯。

————————————————
版权声明: 本文为CSDN博主「青鱼入云」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: [https://blog.csdn.net/u011305680/article/details/79730646](https://blog.csdn.net/u011305680/article/details/79730646)
>[https://blog.csdn.net/u013699827/article/details/73251649](https://blog.csdn.net/u013699827/article/details/73251649)
