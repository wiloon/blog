---
title: Runtime freeMemory,totalMemory,maxMemory
author: "-"
date: 2017-03-31T01:24:08+00:00
url: /?p=9999
categories:
  - Uncategorized

tags:
  - reprint
---
## Runtime freeMemory,totalMemory,maxMemory
http://blog.csdn.net/zy_27_ok/article/details/8462385

最近在网上看到一些人讨论到Java.lang.Runtime类中的freeMemory(),totalMemory(),maxMemory ()这几个方法的一些题目,很多人感到很迷惑,为什么,在java程序刚刚启动起来的时候freeMemory()这个方法返回的只有一两兆字节,而随着 java程序往前运行,创建了不少的对象,freeMemory()这个方法的返回有时候不但没有减少,反而会增加。这些人对freeMemory()这 个方法的意义应该有一些误解,他们以为这个方法返回的是操纵系统的剩余可用内存,实在根本就不是这样的。这三个方法反映的都是java这个进程的内存情 况,跟操纵系统的内存根本没有关系。下面结合totalMemory(),maxMemory()一起来解释。
  
maxMemory()这个方法返回的是java虚拟机 (这个进程) 能构从操纵系统那里挖到的最大的内存,以字节为单位,假如在运行java程 序的时 候,没有添加-Xmx参数,那么就是64兆,也就是说maxMemory()返回的大约是64\*1024\*1024字节,这是java虚拟机默认情况下能 从操纵系统那里挖到的最大的内存。假如添加了-Xmx参数,将以这个参数后面的值为准,例如java -cp ClassPath -Xmx512m ClassName,那么最大内存就是512\*1024\*0124字节。
  
totalMemory()这个方法返回的是java虚拟机现在已经从操纵系统那里挖过来的内存大小,也就是java虚拟机这个进程当时所占用的 所有 内存。假如在运行java的时候没有添加-Xms参数,那么,在java程序运行的过程的,内存总是慢慢的从操纵系统那里挖的,基本上是用多少挖多少,直 挖到maxMemory()为止,所以totalMemory()是慢慢增大的。假如用了-Xms参数,程序在启动的时候就会无条件的从操纵系统中挖- Xms后面定义的内存数,然后在这些内存用的差未几的时候,再往挖。
  
freeMemory()是什么呢,刚才讲到假如在运行java的时候没有添加-Xms参数,那么,在java程序运行的过程的,内存总是慢慢的 从操 作系统那里挖的,基本上是用多少挖多少,但是java虚拟机100％的情况下是会稍微多挖一点的,这些挖过来而又没有用上的内存,实际上就是 freeMemory(),所以freeMemory()的值一般情况下都是很小的,但是假如你在运行java程序的时候使用了-Xms,这个时候由于程 序在启动的时候就会无条件的从操纵系统中挖-Xms后面定义的内存数,这个时候,挖过来的内存可能大部分没用上,所以这个时候freeMemory()可 能会有些大。
  
把下面的源代码编译以后,在class文件所在的目录里面,分别用java -cp . Untitled1 和java -cp . -Xms80m -Xmx80m Untitled1 运行,看看结果如何,有助于理解上面的阐述。

public?class?Untitled1?{??????
  
??public?Untitled1()?{}??????
  
??public?static?void?main(String[]?args)?{??
  
????System.out.println(Runtime.getRuntime().freeMemory());??
  
????System.out.println(Runtime.getRuntime().totalMemory());??
  
????System.out.println(Runtime.getRuntime().maxMemory());??
  
????long?t?=?System.currentTimeMillis();??
  
????try?{??
  
??????Thread.sleep(30000);??
  
????}?catch?(Exception?ee)?{??
  
??????ee.printStackTrace();??
  
????}??
  
????String[]?aaa?=?new?String[2000000];??
  
????System.out.println(Runtime.getRuntime().freeMemory());??
  
????System.out.println(Runtime.getRuntime().totalMemory());??
  
????System.out.println(Runtime.getRuntime().maxMemory());??
  
????try?{??
  
??????Thread.sleep(30000);??
  
????}?catch?(Exception?ee)?{??
  
??????ee.printStackTrace();??
  
????}??
  
????for?(int?i?=?0;?i?<?2000000;?i++)?{??
  
??????aaa[i]?=?new?String("aaa");??
  
????}??
  
????System.out.println(Runtime.getRuntime().freeMemory());??
  
????System.out.println(Runtime.getRuntime().totalMemory());??
  
????System.out.println(Runtime.getRuntime().maxMemory());??
  
????try?{??
  
??????Thread.sleep(30000);??
  
????}?catch?(Exception?ee)?{??
  
??????ee.printStackTrace();??
  
????}??
  
??}??
  
}?