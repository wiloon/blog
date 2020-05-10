---
title: httpclient4乱码问题
author: wiloon
type: post
date: 2014-05-26T09:16:52+00:00
url: /?p=6662
categories:
  - Uncategorized
tags:
  - Java

---
http://my.oschina.net/u/179805/blog/93659

今天在开发调用第三方接口的时候，使用HTTPCLIENT4调用后返回的结果中中文都是乱码，蛋疼的乱码问题又来了！我一开始使用的是：

1
  
String result = new String(EntityUtils.toString(entity,&#8221;UTF-8&#8243;));
  
获取返回值的，结果是乱码，咨询了第三方公司后，他们表示他们的返回的结果已经是UTF-8编码,
  
于是我直接使用：

1
  
String result = new String(EntityUtils.toString(entity)）;
  
悲剧的是返回值还是乱码！
  
后来我试了试：

1
  
ByteArrayOutputStream baos = new ByteArrayOutputStream();
  
2
  
while((len = is.read(b)) != -1){
  
3
  
baos.write(b, 0, len);
  
4
  
}
  
5
  
System.out.println(&#8220;baos=&#8221;+new String(baos.toByteArray()));
  
这次不乱了，查看了下EntityUtils.toString源码，发现如果不指定编码，EntityUtils默认会使用ISO\_8859\_1进行编码，所以如果服务端直接返回 是UTF-8编码的值可以进行如下转码：

1
  
String result = new String(EntityUtils.toString(entity).getBytes(&#8220;ISO\_8859\_1&#8243;),&#8221;UTF-8&#8221;);
  
这样可以直接使用EntityUtils.toString方法了！