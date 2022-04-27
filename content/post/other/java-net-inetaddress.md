---
title: java.net.InetAddress
author: "-"
date: 2015-08-05T05:08:35+00:00
url: /?p=8060
categories:
  - Uncategorized
tags:
  - Java

---
## java.net.InetAddress
http://www.cnblogs.com/hnrainll/archive/2012/01/09/2317515.html


1. java.net.InetAddress类的使用

1.1. 简介

IP地址是IP使用的32位 (IPv4) 或者128位 (IPv6) 位无符号数字，它是传输层协议TCP，UDP的基础。InetAddress是Java对IP地址的封装，在java.net中有许多类都使用到了InetAddress，包括ServerSocket，Socket，DatagramSocket等等。

InetAddress的实例对象包含以数字形式保存的IP地址，同时还可能包含主机名 (如果使用主机名来获取InetAddress的实例，或者使用数字来构造，并且启用了反向主机名解析的功能) 。InetAddress类提供了将主机名解析为IP地址 (或反之) 的方法。

InetAddress对域名进行解析是使用本地机器配置或者网络命名服务 (如域名系统 (Domain Name System，DNS) 和网络信息服务 (Network Information Service，NIS) ) 来实现。对于DNS来说，本地需要向DNS服务器发送查询的请求，然后服务器根据一系列的操作，返回对应的IP地址，为了提高效率，通常本地会缓存一些主机名与IP地址的映射，这样访问相同的地址，就不需要重复发送DNS请求了。在java.net.InetAddress类同样采用了这种策略。在默认情况下，会缓存一段有限时间的映射，对于主机名解析不成功的结果，会缓存非常短的时间 (10秒) 来提高性能。
  
1.2. InetAddress对象的获取

InetAddress的构造函数不是公开的 (public) ，所以需要通过它提供的静态方法来获取，有以下的方法: 

static InetAddress[] getAllByName(String host)

static InetAddress getByAddress(byte[] addr)

static InetAddress getByAddress(String host,byte[] addr)

static InetAddress getByName(String host)

static InetAddress getLocalHost()

在这些静态方法中，最为常用的应该是getByName(String host)方法，只需要传入目标主机的名字，InetAddress会尝试做连接DNS服务器，并且获取IP地址的操作。代码片段如下，注意我们假设以下的代码，都是默认导入了java.net中的包，在程序的开头加上import java.net.*，否则需要指定类的全名java.net.InetAddress。

InetAddress address=InetAddress.getByName("www.baidu.com");

注意到这些方法可能会抛出的异常。如果安全管理器不允许访问DNS服务器或禁止网络连接，SecurityException会抛出，如果找不到对应主机的IP地址，或者发生其他网络I/O错误，这些方法会抛出UnknowHostException。所以需要写如下的代码: 

try

{

InetAddress address=InetAddress.getByName("www.baidu.com");

System.out.println(address);

}

catch(UnknownHostException e)

{

e.printStackTrace();

}

下面是一则完整的例子: 

package org.dakiler.javanet.chapter1;
  
import java.net.InetAddress;
  
/**

* this example is used to show how to get InetAddress instance

* @author Dakiler

*/

public class Example1

{

public static void main(String args[])throws Exception

{

InetAddress address=InetAddress.getByName("www.baidu.com");

System.out.println(address);

System.out.println("--");

InetAddress[] addresses=InetAddress.getAllByName("www.baidu.com");

for(InetAddress addr:addresses)

{

System.out.println(addr);

}

}

}

运行结果如下: 

www.baidu.com/119.75.213.61

--

www.baidu.com/119.75.213.61

www.baidu.com/119.75.216.30

在这个例子中，我们使用到了getByName()以及getAllByName()两个方法，前者通过"www.baidu.com"来获取InetAddress的对象，并且输出到控制台。System.out.println(address); 默认调用了InetAddress.toString()方法，在结果中可以看到"www.baidu.com/119.75.213.61"的输出结果，其中119.75.213.61为百度网站的IP地址。

getAllByName()方法是根据主机名返回其可能的所有InetAddress对象，保存在一个数组中。在这个例子中，输出的结果中，www.baidu.com有两个ip地址分别为119.75.213.61以及119.75.216.30。

另外一个静态常用的静态方法是getLocalHost()，返回的是本地地址，如下例: 

package org.dakiler.javanet.chapter1;
  
import java.net.InetAddress;
  
public class Example2

{

public static void main(String args[])throws Exception

{

InetAddress address=InetAddress.getLocalHost();

System.out.println(address);

}

}

这个例子首先是根据InetAddress.getLocalHost()方法获取本地IP地址，然后通过System.out.println()打印出来，结果如下: 
  
dakiler/192.168.1.102
  
作者: Leo Chin
  
出处: http://www.cnblogs.com/hnrainll/
  
本博客文章,大多系网络中收集,转载请注明出处
  
相关标签: 嵌入式培训、嵌入式开发、嵌入式学习