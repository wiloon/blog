---
title: http GET POST 长度
author: "-"
date: 2015-10-13T11:05:48+00:00
url: /?p=8402
categories:
  - Uncategorized

tags:
  - reprint
---
## http GET POST 长度
http://blog.csdn.net/blueling51/article/details/6935901

1.    Get方法长度限制

Http Get方法提交的数据大小长度并没有限制,HTTP协议规范没有对URL长度进行限制。这个限制是特定的浏览器及服务器对它的限制。

如: IE对URL长度的限制是2083字节(2K+35)。

下面就是对各种浏览器和服务器的最大处理能力做一些说明.

Microsoft Internet Explorer (Browser)

IE浏览器对URL的最大限制为2083个字符,如果超过这个数字,提交按钮没有任何反应。
  
Firefox (Browser)

对于Firefox浏览器URL的长度限制为65,536个字符。

Safari (Browser)

URL最大长度限制为 80,000个字符。

Opera (Browser)

URL最大长度限制为190,000个字符。

Google (chrome)

URL最大长度限制为8182个字符。

Apache (Server)

能接受最大url长度为8,192个字符。

Microsoft Internet Information Server(IIS)

能接受最大url的长度为16,384个字符。

通过上面的数据可知,为了让所有的用户都能正常浏览, URL最好不要超过IE的最大长度限制(2083个字符) ,当然,如果URL不直接提供给用户,而是提供给程序调用,这时的长度就只受Web服务器影响了。

注: 对于中文的传递,最终会为urlencode后的编码形式进行传递,如果浏览器的编码为UTF8的话,一个汉字最终编码后的字符长度为9个字符。

因此如果使用的 GET 方法,最大长度等于URL最大长度减去实际路径中的字符数。

2.    POST方法长度限制

理论上讲,POST是没有大小限制的。HTTP协议规范也没有进行大小限制,起限制作用的是服务器的处理程序的处理能力。

如: 在Tomcat下取消POST大小的限制 (Tomcat默认2M) ；

打开tomcat目录下的conf目录,打开server.xml 文件,修改

<Connector

debug="0"

acceptCount="100"

connectionTimeout="20000"

disableUploadTimeout="true"

port="8080"

redirectPort="8443"

enableLookups="false"

minSpareThreads="25"

maxSpareThreads="75"

maxThreads="150"

maxPostSize="0"

URIEncoding="GBK"



</Connector>

增加红色字体部分 maxPostSize="0" (设为0是取消POST的大小限制)