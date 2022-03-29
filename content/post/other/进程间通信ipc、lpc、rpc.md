---
title: 进程间通信IPC、LPC、RPC
author: "-"
date: 2015-08-28T01:22:28+00:00
url: /?p=8175

categories:
  - inbox
tags:
  - reprint
---
## 进程间通信IPC、LPC、RPC
## 进程间通信 IPC、LPC、RPC

http://www.cnblogs.com/gsk99/archive/2010/12/13/1904541.html

进程间通信 (IPC,Inter-Process Communication) , 指至少两个进程或线程间传送数据或信号的一些技术或方法。进程是计算机系统分配资源的最小单位。每个进程都有自己的一部分独立的系统资源,彼此是隔离的。为了能使不同的进程互相访问资源并进行协调工作,才有了进程间通信。这些进程可以运行在同一计算机上或网络连接的不同计算机上。 进程间通信技术包括消息传递、同步、共享内存和远程过程调用。 IPC是一种标准的Unix通信机制。

有两种类型的进程间通信(IPC)。

本地过程调用(LPC)LPC用在多任务操作系统中,使得同时运行的任务能互相会话。这些任务共享内存空间使任务同步和互相发送信息。

远程过程调用(RPC)RPC类似于LPC,只是在网上工作。RPC开始是出现在Sun微系统公司和HP公司的运行UNIX操作系统的计算机中。

通过IPC和RPC,程序能利用其它程序或计算机处理的进程。客户机/服务器模式计算把远程过程调用与其它技术如消息传递一道,作为系统间通信的一种机制。客户机执行自己的任务,但靠服务器提供后端文件服务。RPC为客户机提供向后端服务器申请服务的通信机制。如果你把客户机/服务器应用程序想作是一个分离的程序,服务器能运行数据访问部分,因为它离数据最近,客户机能运行数据表 示和与用户交互的前端部分。这样,远程过程调用可看作是把分割的程序通过网络重组的部件。LPC有时也称耦合(Coupling)机制。

用这种方式分割程序,当用户要访问数据时就无需每次拷贝整个数据库或它的大部分程序到用户系统。其实,服务器只处理请求,甚至只执行一些数据计算,把得出的结果再发送给用户。因为当数据存放在一个地方时,数据库同步很容易实现,所以多个用户可同时访问相同的数据。


RPC:

Remote procedure call (RPC) is an Inter-process communication technology that allows a computer program to cause a subroutine or procedure to execute in another address space (commonly on another computer on a shared network) without the programmer explicitly coding the details for this remote interaction.

IPC:

Inter-process communication (IPC) is a set of techniques for the exchange of data among multiple threads in one or more processes. Processes may be running on one or more computers connected by a network.

RPCs are a form of inter-process communication (IPC)


>https://en.wikipedia.org/wiki/Remote_procedure_call
>https://en.wikipedia.org/wiki/Inter-process_communication