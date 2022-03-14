---
title: CGI
author: "-"
date: 2017-12-16T05:15:10+00:00
url: /?p=11592
categories:
  - Uncategorized

tags:
  - reprint
---
## CGI
CGI: 全拼(Common Gateway Interface)是能让web服务器和CGI脚本共同处理客户的请求的协议。Web服务器把请求转成CGI脚本,CGI脚本执行回复Web服务器,Web服务回复给客户端。

CGI fork一个新的进程来执行,读取参数,处理数据,然后就结束生命期。

FastCGI采用tcp链接,不用fork新的进程,因为程序启动的时候就已经开启了,等待数据的到来,处理数据。

CGI的一些知识点
  
2012-12-24 11:31 by 轩脉刃, 4325 阅读, 3 评论, 收藏, 编辑
  
CGI(Common Gateway Interface)是能让web服务器和CGI脚本共同处理客户的请求的协议。它的协议定义文档是http://www.ietf.org/rfc/rfc3875。

其中Web服务器负责管理连接,数据传输,网络交互等。至于CGI脚本就负责管理具体的业务逻辑。

Web服务器的功能是将客户端请求 (HTTP Request) 转换成CGI脚本请求,然后执行脚本,接着将CGI脚本回复转换为客户端的回复 (HTTP Response) 。

CGI的脚本请求有两部分: 请求元数据 (request meta-variables) 和相关的消息体 (message-body) 。

请求元数据
  
包含: 

                               "AUTH_TYPE" | "CONTENT_LENGTH" |
                           "CONTENT_TYPE" | "GATEWAY_INTERFACE" |
                           "PATH_INFO" | "PATH_TRANSLATED" |
                           "QUERY_STRING" | "REMOTE_ADDR" |
                           "REMOTE_HOST" | "REMOTE_IDENT" |
                           "REMOTE_USER" | "REQUEST_METHOD" |
                           "SCRIPT_NAME" | "SERVER_NAME" |
                           "SERVER_PORT" | "SERVER_PROTOCOL" |
                           "SERVER_SOFTWARE" | scheme |
                           protocol-var-name | extension-var-name
    

下面一个一个看: 

AUTH_TYPE是唯一标识了用户的认证方式,比如basic,Digest等
  
CONTENT_LENGTH是请求消息体的长度
  
CONTENT_TYPE是标识消息体的格式
  
GATEWAY_INTERFACE标识使用的CGI的版本,比如CGI/1.1
  
PATH_INFO说明了解释CGI脚本的地址
  
PATH_TRANSLATED就是可以被访问的cgi的路径,它对应CGI脚本的路径,比如
  
http://somehost.com/cgi-bin/somescript/this%2eis%2epath%3binfo
  
对应的PATH_INFO就是/this.is.the.path;info
  
QUERY_STRING 请求参数 (GET的参数就是放在这个里面的) 
  
REMOTE_ADDR标识客户端的ip地址
  
REMOTE_HOST标识的是客户端的域名
  
REMOTE_IDENT是发出请求的使用者标示,大多数服务端选择忽略这个属性
  
REMOTE_USER是使用者的合法名称
  
REQUEST_METHOD是请求方法,包括GET/POST/PUT/DELETE等
  
SCRIPT_NAME是脚本程序的虚拟路径,比如是/test/test.php
  
SERVER_NAME是WEB服务器的域名
  
SERVER_PORT是WEB服务器端口名
  
SERVER_PROTOCOL是WEB服务器与客户端的交互请求协议
  
SERVER_SOFTWARE发送给客户端的response的Web服务器的标识,比如nginx/1.0.6

请求消息体
  
就是直接将客户端的请求消息体转发,将消息体放在stdin中传递给script的

相关知识点
  
参数传递
  
下面的问题就是web服务器获取了http请求后,由于http请求是有分GET和POST等方法的。参数怎么传递给可执行程序呢？
  
比如GET方法,CGI程序就会从环境变量QUERY_STRING中获取数据。
  
POST呢？Web服务器会通过stdin (标准输入) 想CGI中传送数据的。而传送的数据长度就是放在CONTENT_LENGTH中的。
  
对应于HTTP请求,QUERY_STRING存放http的GET参数,stdin存放HTTP的BODY参数

现在流行的nginx+php的方法就是使用nginx(web服务器)将请求变成cgi请求到php-cgi上,然后php-cgi进程执行php,将返回值变成cgi response返回给nginx。nginx再将它变成http回复返回给客户端。

但是这里有个问题,cgi是单进程的,一个进程的生命期就只是请求进来,处理,返回回复这几个阶段。但是web服务器都是需要接受多个web请求的,这里就需要在后端开启多个cgi了。一般的cgi服务器都会设置允许开启多少个cgi的数量的。

这里要明确一点,cgi是有分服务端和客户端的区别的,cgi客户端是放在web服务器一侧,像nginx,apache这样的web服务器就已经是实现了这个客户端。服务器端需要另外重启。像nginx+cgi+php这样的配合就需要启动php-cgi服务,当然你也可以想到这样的服务一定是以deamon的形式在后台运行,然后会fork出很多个cgi进程。

复用
  
当然有人会问,cgi进程不能复用是个问题,为什么不呢,fastcgi出现就是解决了这个问题。它的一个进程可以处理多个请求。这样速度当然就升上去了。然后还有一种cgi是scgi (simple cgi) ,scgi和fastcgi相似,只能说它定义的协议更简单 (所以才叫做simple) 。scgi的客户端是c写的,服务端是perl写的。

就最常见的nginx+cgi+php来说,要明确一点php中$_SERVER中获取的信息实际都是从cgi中获取的,当然这个和nginx中获取的客户端信息是一致的。另外由于cgi是有客户端和服务端的区别的,因此很容易想到cgi客户端需要使用tcp与客户端连接,每个连接当然需要占用一个端口,因此还是会有端口限制的。所以从这个角度上说,并不是cgi开的越多越好 (当然6w的端口限制是远远够的了) 。

安全
  
关于开启的cgi安全问题,曾经鸟哥就爆出了一个bug: http://www.laruence.com/2010/05/20/1495.html
  
有兴趣的读者可以看看。

还有cgi服务器不是在监听端口吗？怎么防止外网的请求执行cgi呢？我们一般的办法就是直接绑定在127.0.0.1的ip地址上,保证只有本机才能访问
  
参考文档: 
  
http://www.lyinfo.net.cn/webclass/cgi/default.htm
  
http://blog.csdn.net/ablo_zhou/article/details/3634954
  
http://www.ietf.org/rfc/rfc3875

http://www.infoq.com/cn/articles/golang-standard-library-part02

http://www.cnblogs.com/yjf512/archive/2012/12/24/2830730.html