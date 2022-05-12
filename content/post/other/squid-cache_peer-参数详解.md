---
title: squid cache_peer 参数详解
author: "-"
date: 2012-01-18T09:29:04+00:00
url: /?p=2155
categories:
  - Linux
  - Network
tags:
  - reprint
---
## squid cache_peer 参数详解
通过squid.conf配置文件中的cache_peer选项来配置代理服务器阵列，通过其他的选项来控制选择代理伙伴的方法。Cache_peer的使用格式如下: 
  
cache_peer hostname type http_port icp_port
  
共有5个选项可以配置: 
  
1. hostname:指被请求的同级子代理服务器或父代理服务器。可以用主机名或ip地址表示；
  
2. type: 指明hostname的类型，是同级子代理服务器还是父代理服务器，也即parent (父)  还是 sibling (子) ；
  
3. http_port: hostname的监听端口；
  
4. icp_port: hostname上的ICP监听端口，对于不支持ICP协议的可指定7；
  
5. options: 可以包含一个或多个关键字。
  
Options可能的关键字有: 
  
1． proxy-only: 指明从peer得到的数据在本地不进行缓存，缺省地，squid是要缓存这部分数据的；
  
2． weight=n: 用于你有多个peer的情况，这时如果多于一个以上的peer拥有你请求的数据时，squid通过计算每个peer的ICP响应时间来 决定其weight的值，然后squid向其中拥有最大weight的peer发出ICP请求。也即weight值越大，其优先级越高。当然你也可以手工 指定其weight值；
  
3． no-query: 不向该peer发送ICP请求。如果该peer不可用时，可以使用该选项；
  
4． Default: 有点象路由表中的缺省路由，该peer将被用作最后的尝试手段。当你只有一个父代理服务器并且其不支持ICP协议时，可以使用default和no-query选项让所有请求都发送到该父代理服务器；
  
5．login=user:password: 当你的父代理服务器要求用户认证时可以使用该选项来进行认证。