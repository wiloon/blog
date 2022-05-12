---
title: corba, ejb, webservice, rest分布式 区别
author: lcf
date: 2012-09-25T06:05:43+00:00
url: /?p=4273
categories:
  - Java
tags:
  - reprint
---
## corba, ejb, webservice, rest分布式 区别
Corba，还是EJB，都有一些共同点: 
  
1) 通过专有的网络协议通讯
  
2) 不能跨平台调用
  
3) 通过分布式对象调用来实现分布式架构，换句话来说就是，分布式架构是绑定在面向对象的机制上的 分布式对象架构的缺陷在EJB2时代被充分暴露了出来
  
web services有一些明显不同于Corba和EJB分布式对象架构的特征: 
  
1) 通过标准SOAP协议通讯，一般走HTTP通道
  
2) 能够跨平台调用
  
3) 通讯格式是xml文本，而不是二进制数据格式
  
4) 通过RPC机制来实现分布式调用，而不是通过面向对象机制实现分布式调用
  
REST也是一种分布式系统的架构风格，那么REST和上面这些分布式架构有哪些明显的区别呢？
  
1) REST走的是HTTP协议，并且充分利用或者说极端依赖HTTP协议
  
Corba和EJB是采用专有的二进制协议，SOAP可以但不依赖HTTP，并且仅仅使用HTTP POST。
  
2) REST是基于HTTP抽象资源的分布式调用，换句话来说，就是分布式调用是绑定在资源的操作上面的。
  
分布式架构       协议             调用方式
  
-------------------
  
Corba架构        专有二进制协议      对象的CRUD操作
  
EJB架构          专有二进制协议      对象的CRUD操作
  
Web Services     SOAP协议            RPC方式
  
REST             HTTP协议            对资源的CRUD操作

REST最大的特点是什么呢？REST是为通过HTTP协议来进行分布式调用量身定造的架构
  
REST是专门为分布式调用设计的架构，在REST里面，分布式是通过对资源的操作来实现的，不是像EJB那样通过对象的方法调用来实现的。资源是一种抽象的概念，资源被映射到相应的一套URL规则上面了。所以资源只和URL相关，而与具体实现无关，因此REST具有更好的解藕性。