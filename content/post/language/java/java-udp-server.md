---
title: java UDP
author: "-"
date: 2015-08-24T05:09:42+00:00
url: /?p=8148
categories:
  - Inbox
tags:
  - Java

---
## java UDP


一. UDP协议定义

UDP协议的全称是用户数据报，在网络中它与TCP协议一样用于处理数据包。在OSI模型中，在第四层——传输层，处于IP协议的上一层。UDP有不提供数据报分组、组装和不能对数据包的排序的缺点，也就是说，当报文发送之后，是无法得知其是否安全完整到达的。

二. 使用UDP的原因
  
它不属于连接型协议，因而具有资源消耗小，处理速度快的优点，所以通常音频、视频和普通数据在传送时使用UDP较多，因为它们即使偶尔丢失一两个数据包，也不会对接收结果产生太大影响。比如我们聊天用的ICQ和OICQ就是使用的UDP协议。在选择使用协议的时候，选择UDP必须要谨慎。在网络质量令人不十分满意的环境下，UDP协议数据包丢失会比较严重。

三. 在Java中使用UDP协议编程的相关类
  
1. InetAddress
  
用于描述和包装一个Internet IP地址。有如下方法返回实例: 
  
getLocalhost(): 返回封装本地地址的实例。

getAllByName(String host): 返回封装Host地址的InetAddress实例数组。

getByName(String host): 返回一个封装Host地址的实例。其中，Host可以是域名或者是一个合法的IP地址。
  
InetAddress.getByAddress(addr): 根据地址串返回InetAddress实例。
  
InetAddress.getByAddress(host, addr): 根据主机地符串和地址串返回InetAddress实例。

2. DatagramSocket
  
用于接收和发送UDP的Socket实例。该类有3个构造函数: 
  
DatagramSocket(): 通常用于客户端编程，它并没有特定监听的端口，仅仅使用一个临时的。程序会让操作系统分配一个可用的端口。
  
DatagramSocket(int port): 创建实例，并固定监听Port端口的报文。通常用于服务端

DatagramSocket(int port, InetAddress localAddr): 这是个非常有用的构建器，当一台机器拥有多于一个IP地址的时候，由它创建的实例仅仅接收来自LocalAddr的报文。
  
DatagramSocket具有的主要方法如下: 
  
1) receive(DatagramPacket d): 接收数据报文到d中。receive方法产生一个"阻塞"。"阻塞"是一个专业名词，它会产生一个内部循环，使程序暂停在这个地方，直到一个条件触发。

2) send(DatagramPacket dp): 发送报文dp到目的地。

3) setSoTimeout(int timeout): 设置超时时间，单位为毫秒。

4) close(): 关闭DatagramSocket。在应用程序退出的时候，通常会主动释放资源，关闭Socket，但是由于异常地退出可能造成资源无法回收。所以，应该在程序完成时，主动使用此方法关闭Socket，或在捕获到异常抛出后关闭Socket。

3. DatagramPacket
  
用于处理报文，它将Byte数组、目标地址、目标端口等数据包装成报文或者将报文拆卸成Byte数组。应用程序在产生数据包是应该注意，TCP/IP规定数据报文大小最多包含65507个，通常主机接收548个字节，但大多数平台能够支持8192字节大小的报文。DatagramPacket类的构建器共有4个: 
  
DatagramPacket(byte[] buf, int length): 将数据包中Length长的数据装进Buf数组，一般用来接收客户端发送的数据。
  
DatagramPacket(byte[] buf, int offset, int length): 将数据包中从Offset开始、Length长的数据装进Buf数组。
  
DatagramPacket(byte[] buf, int length, InetAddress clientAddress, int clientPort): 从Buf数组中，取出Length长的数据创建数据包对象，目标是clientAddress地址，clientPort端口,通常用来发送数据给客户端。

DatagramPacket(byte[] buf, int offset, int length, InetAddress clientAddress, int clientPort): 从Buf数组中，取出Offset开始的、Length长的数据创建数据包对象，目标是clientAddress地址，clientPort端口，通常用来发送数据给客户端。
  
主要的方法如下: 
  
1) getData(): 从实例中取得报文的Byte数组编码。
  
2) setDate(byte[] buf): 将byte数组放入要发送的报文中。

UDP是一种高速，无连接的数据交换方式，他的特点是，即使没有连接到 (也不许要连接) 接收方也可以封包发送，就像在一个多人使用的步话机环境中，你不知道你的信息是否被需要的人接受到，但是你的信息确实被传递然后消失了，有时候速度比数据完整性重要，在比如视频会议中，丢失几帧画面是可以接受的。但在需要数据安全接受的环境就不适用了。

发送步骤: 

  * 使用 DatagramSocket(int port) 建立socket (套间字) 服务。
  * 将数据打包到DatagramPacket中去
  * 通过socket服务发送  (send()方法) 
  * 关闭资源


  
    
      /**
    
    
       *UDPServer
    
    
       *@author Winty wintys@gmail.com
    
    
       *@version 2008-12-15
    
    
       */
    
    
      import java.io.*;
    
    
      import java.net.*;
    
    
    
    
      class UDPServer{
    
    
          public static void main(String[] args)throws IOException{
    
    
              DatagramSocket  server = new DatagramSocket(5050);
    
    
    
    
              byte[] recvBuf = new byte[100];
    
    
              DatagramPacket recvPacket
    
    
                  = new DatagramPacket(recvBuf , recvBuf.length);
    
    
    
    
              server.receive(recvPacket);
    
    
    
    
              String recvStr = new String(recvPacket.getData() ,  , recvPacket.getLength());
    
    
              System.out.println("Hello World!" + recvStr);
    
    
    
    
              int port = recvPacket.getPort();
    
    
              InetAddress addr = recvPacket.getAddress();
    
    
              String sendStr = "Hello ! I'm Server";
    
    
              byte[] sendBuf;
    
    
              sendBuf = sendStr.getBytes();
    
    
              DatagramPacket sendPacket
    
    
                  = new DatagramPacket(sendBuf , sendBuf.length , addr , port );
    
    
    
    
              server.send(sendPacket);
    
    
    
    
              server.close();
    
    
          }
    
    
      }
    
    
    
  



  
    
      /**
    
    
       *UDPClient
    
    
       *@author Winty wintys@gmail.com
    
    
       *@version 2008-12-15
    
    
       */
    
    
      import java.io.*;
    
    
      import java.net.*;
    
    
    
    
      class UDPClient{
    
    
          public static void main(String[] args)throws IOException{
    
    
              DatagramSocket client = new DatagramSocket();
    
    
    
    
              String sendStr = "Hello! I'm Client";
    
    
              byte[] sendBuf;
    
    
              sendBuf = sendStr.getBytes();
    
    
              InetAddress addr = InetAddress.getByName("127.0.0.1");
    
    
              int port = 5050;
    
    
              DatagramPacket sendPacket
    
    
                  = new DatagramPacket(sendBuf ,sendBuf.length , addr , port);
    
    
    
    
              client.send(sendPacket);
    
    
    
    
              byte[] recvBuf = new byte[100];
    
    
              DatagramPacket recvPacket
    
    
                  = new DatagramPacket(recvBuf , recvBuf.length);
    
    
              client.receive(recvPacket);
    
    
              String recvStr = new String(recvPacket.getData() ,  ,recvPacket.getLength());
    
    
              System.out.println("收到:" + recvStr);
    
    
    
    
              client.close();
    
    
          }
    
    
      }
    
  
  
  
  
    http://blog.csdn.net/wintys/article/details/3525643/
  
  
    http://blog.csdn.net/zzcchunter/article/details/6943740
  
