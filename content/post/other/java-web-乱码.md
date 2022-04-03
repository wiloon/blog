---
title: Java web 乱码
author: "-"
date: 2012-06-03T10:34:29+00:00
url: /?p=3371
categories:
  - Java
  - Web

tags:
  - reprint
---
## Java web 乱码
http://www.jb51.net/web/12714.html
  
 (一) get提交
  
1.首先说下客户端 (浏览器) 的form表单用get方法是如何将数据编码后提交给服务器端的吧。

对于get方法来说，都是把数据串联在请求的url后面作为参数，如: http://localhost:8080/servlet?msg=abc
  
 (很常见的一个乱码问题就要出现了，如果url中出现中文或其它特殊字符的话，如: http://localhost:8080 /servlet?msg=杭州，服务器端容易得到乱码) ，url拼接完成后，浏览器会对url进行URL encode，然后发送给服务器，URL encode的过程就是把部分url做为字符，按照某种编码方式 (如: utf-8,gbk等) 编码成二进制的字节码，然后每个字节用一个包含3个字符的字符串 "%xy" 表示，其中xy为该字节的两位十六进制表示形式。我这里说的可能不清楚，具体介绍可以看下java.net.URLEncoder。了解了 URL encode的过程，我们能看到2个很重要的问题，第一: 需要URL encode的字符一般都是非ASCII的字符 (笼统的讲) ，再通俗的讲就是除了英文字母以外的文字 (如: 中文，日文等) 都要进行URL encode，所以对于我们来说，都是英文字母的url不会出现服务器得到乱码问题，出现乱码都是url里面带了中文或特殊字符造成的；第二: URL encode到底按照那种编码方式对字符编码？这里就是浏览器的事情了，而且不同的浏览器有不同的做法，中文版的浏览器一般会默认的使用GBK，通过设置浏览器也可以使用UTF-8，可能不同的用户就有不同的浏览器设置，也就造成不同的编码方式，所以很多网站的做法都是先把url里面的中文或特殊字符用 javascript做URL encode，然后再拼接url提交数据，也就是替浏览器做了URL encode，好处就是网站可以统一get方法提交数据的编码方式。 完成了URL encode，那么现在的url就成了ASCII范围内的字符了，然后以iso-8859-1的编码方式转换成二进制随着请求头一起发送出去。这里想多说几句的是，对于get方法来说，没有请求实体，含有数据的url都在请求头里面，之所以用URL encode，我个人觉的原因是: 对于请求头来说最终都是要用iso-8859-1编码方式编码成二进制的101010.....的纯数据在互联网上传送，如果直接将含有中文等特殊字符做iso-8859-1编码会丢失信息，所以先做URL encode是有必要的。
  
2。服务器端 (tomcat) 是如何将数据获取到进行解码的。
  
第一步是先把数据用iso-8859-1进行解码，对于get方法来说，tomcat获取数据的是ASCII范围内的请求头字符，其中的请求url里面带有参数数据，如果参数中有中文等特殊字符，那么目前还是URL encode后的%XY状态，先停下，我们先说下开发人员一般获取数据的过程。通常大家都是request.getParameter("name")获取参数数据，我们在request对象获得的数据都是经过解码过的，而解码过程中程序里是无法指定，这里要说下，有很多新手说用 request.setCharacterEncoding("字符集")可以指定解码方式，其实是不可以的，看servlet的官方API说明有对此方法的解释: Overrides the name of the character encoding used in the body of this request. This method must be called prior to reading request parameters or reading input using getReader().可以看出对于get方法他是无能为力的。那么到底用什么编码方式解码数据的呢，这是tomcat的事情了，默认缺省用的是 iso-8859-1,这样我们就能找到为什么get请求带中文参数为什么在服务器端得到乱码了，原因是在客户端一般都是用UTF-8或GBK对数据 URL encode，这里用iso-8859-1方式URL decoder显然不行，在程序里我们可以直接

```java
  
new String(request.getParameter("name")
  
.getBytes("iso-8859-1"),"客户端指定的URLencode编码方式")

```

还原回字节码，然后用正确的方式解码数据，网上的文章通常是在tomcat里面做个配置

```xml

<Connector port="8080" protocol="HTTP/1.1" maxThreads="150"
  
connectionTimeout="20000" redirectPort="8443"
  
URIEncoding="GBK"/>

```

这样是让tomcat在获取数据后用指定的方式URL decoder.

 (一) post提交
  
1.客户端 (浏览器) 的表单(form)用post方法是如何将数据编码后提交给服务器端的。
  
在post方法里所要传送的数据也要URL encode，那么他是用什么编码方式的呢？
  
在form所在的html文件里如果有段<meta http-equiv="Content-Type" content="text/html; charset=字符集 (GBK，utf-8等) "/>，那么post就会用此处指定的编码方式编码。一般大家都认为这段代码是为了让浏览器知道用什么字符集来对网页解释，所以网站都会把它放在html代码的最前端，尽量不出现乱码，其实它还有个作用就是指定form表单的post方法提交数据的 URL encode编码方式。从这里可以看出对于get方法来说，浏览器对数据的URL encode的编码方式是有浏览器设置来决定， (可以用js做统一指定) ，而post方法，开发人员可以指定。
  
2。服务器端 (tomcat) 是如何将数据获取到进行解码的。
  
如果用tomcat默认缺省设置，也没做过滤器等编码设置，那么他也是用iso-8859-1解码的，但是request.setCharacterEncoding("字符集")可以派上用场。

我发现上面说的tomcat所做的事情前提都是在请求头里没有指定编码方式，如果请求头里指定了编码方式将按照这种方式编码。
  
有2篇文章推荐下，地址分别是
  
>http://www.cnblogs.com/yencain/articles/1321386.html；
  
表单用post方法提交数据时乱码问题: http://wanghuan8086.javaeye.com/blog/173869

用post很重要的在form所在的html文件里如果有段<meta http-equiv="Content-Type" content="text/html; charset=字符集 (GBK，utf-8等) "/>