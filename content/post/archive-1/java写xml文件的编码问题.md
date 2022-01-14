---
title: Java写xml文件的编码问题
author: "-"
date: 2014-05-26T09:15:02+00:00
url: /?p=6658
categories:
  - Uncategorized
tags:
  - Java

---
## Java写xml文件的编码问题
http://itindex.net/detail/49012-java-xml-%E6%96%87%E4%BB%B6

最近项目中需要生成xml格式的配置文件,用的是 javax.xml.transform.Transformer 类中提供的transform方法,在本地执行没问题,但是一旦把工程部署到Tomcat下运行,就会出现中文乱码的现象,纠结了许久,在大神的帮助下终于解决了。

有篇文章其实已经讲的很清楚了,链接如下: 

http://www.cnblogs.com/yunmou/archive/2013/02/19/2917646.html
  
但是按照他给的方法还是不行,问题就出在

OutputStreamWriter osw = new OutputStreamWriter(fos); // 注意。。。
  
这一行,作者虽然加了注意,但没说明怎么办,让我更加迷惑。
  
最后查了若干资料,发现确实是需要在这个地方进行注意。

最终代码如下: 

Source source = new DOMSource((Document) obj);

// Create a new Transformer that performs a copy of the Source to the Result.
  
TransformerFactory transFactory = TransformerFactory.newInstance();
  
Transformer transFormer = transFactory.newTransformer();
  
transFormer.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
  
transFormer.setOutputProperty(OutputKeys.METHOD, "xml");
  
transFormer.setOutputProperty(OutputKeys.INDENT, "no");

OutputStreamWriter outputStreamWriter = new OutputStreamWriter(
  
new FileOutputStream(path), "UTF-8");
  
Result xmlResult = new StreamResult(outputStreamWriter);

// Transform the XML Source to a Result.
  
transFormer.transform(source, xmlResult);

找到区别了吧,以后遇到此类问题都可以这样解决了,开心啊！