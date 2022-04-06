---
title: ByteArrayInputStream ByteArrayOutputStream
author: "-"
date: 2014-04-04T01:58:59+00:00
url: /?p=6479
categories:
  - Uncategorized
tags:
  - Java

---
## ByteArrayInputStream ByteArrayOutputStream
http://blog.csdn.net/rcoder/article/details/6118313

bytejdkclassstream存储socket

第一次看到ByteArrayOutputStream的时候是在Nutch的部分源码，后来在涉及IO操作时频频发现这两个类的踪迹，觉得确实是很好用，所以把它们的用法总结一下。


ByteArrayOutputStream的用法


以下是JDK中的记载: 


public class ByteArrayOutputStream extends OutputStream


此类实现了一个输出流，其中的数据被写入一个 byte 数组。缓冲区会随着数据的不断写入而自动增长。可使用 toByteArray()和 toString()获取数据。


关闭 ByteArrayOutputStream 无效。此类中的方法在关闭此流后仍可被调用，而不会产生任何IOException。


我的个人理解是ByteArrayOutputStream是用来缓存数据的 (数据写入的目标 (output stream原义) ) ，向它的内部缓冲区写入数据，缓冲区自动增长，当写入完成时可以从中提取数据。由于这个原因，ByteArrayOutputStream常用于存储数据以用于一次写入。


实例: 


从文件中读取二进制数据，全部存储到ByteArrayOutputStream中。


FileInputStream fis=new FileInputStream("test");


BufferedInputStream bis=new BufferedInputStream(fis);


ByteArrayOutputStream baos=new ByteArrayOutputStream();


int c=bis.read();//读取bis流中的下一个字节


while(c!=-1){


baos.write(c);


c=bis.read();


}


bis.close();


byte retArr[]=baos.toByteArray();


ByteArrayInputStream的用法


相对而言，ByteArrayInputStream比较少见。先看JDK文档中的介绍: 


public class ByteArrayInputStreamextends InputStreamByteArrayInputStream 包含一个内部缓冲区，该缓冲区包含从流中读取的字节。内部计数器跟踪 read 方法要提供的下一个字节。


关闭 ByteArrayInputStream 无效。此类中的方法在关闭此流后仍可被调用，而不会产生任何 IOException。


构造函数: 


ByteArrayInputStream(byte[] buf)


注意它需要提供一个byte数组作为缓冲区。


与大部分Inputstream的语义类似，可以从它的缓冲区中读取数据，所以我们可以在它的外面包装另一层的inputstream以使用我们需要的读取方法。


个人认为一个比较好的用途是在网络中读取数据包，由于数据包一般是定长的，我们可以先分配一个够大的byte数组，比如byte buf[]=new byte[1024];


然后调用某个方法得到网络中的数据包，例如: 


Socket s=...;


DataInputStream dis=new DataInputStream(s.getInputStream());


dis.read(buf);//把所有数据存到buf中


ByteArrayInputStream bais=new ByteArrayInputStream(buf); //把刚才的部分视为输入流


DataInputStream dis_2=new DataInputStream(bais);


//现在可以使用dis_2的各种read方法，读取指定的字节


比如第一个字节是版本号，dis_2.readByte();


等等……


上面的示例的两次包装看上去有点多此一举，但使用ByteArrayInputStream的好处是关掉流之后它的数据仍然存在。