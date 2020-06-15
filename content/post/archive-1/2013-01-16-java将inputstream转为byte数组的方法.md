---
title: java InputStream
author: wiloon
type: post
date: 2013-01-16T04:31:49+00:00
url: /?p=5029
categories:
  - Java

---
首先请查看一下JavaAPI，可以看到InputStream读取流有三个方法，分别为read()，read(byte[] b),read(byte[] b, int off, int len)。其中read()方法是一次读取一个字节，鬼都知道效率是非常低的。所以最好是使用后面两个方法。
  
例如以下代码：
  
Java代码 收藏代码
  
/**
   
* 读取流
   
*
   
* @param inStream
   
* @return 字节数组
   
* @throws Exception
   
*/
  
public static byte[] readStream(InputStream inStream) throws Exception {
      
ByteArrayOutputStream outSteam = new ByteArrayOutputStream();
      
byte[] buffer = new byte[1024];
      
int len = -1;
      
while ((len = inStream.read(buffer)) != -1) {
          
outSteam.write(buffer, 0, len);
      
}
      
outSteam.close();
      
inStream.close();
      
return outSteam.toByteArray();
  
}

我们来测试一下：
  
Java代码 收藏代码
  
public static void main(String[] args) {
      
try {
          
File file = new File("C:&#92;ceshi.txt");
          
FileInputStream fin = new FileInputStream(file);
          
byte[] filebt = readStream(fin);
          
System.out.println(filebt.length);
      
} catch (Exception e) {
          
e.printStackTrace();
      
}
  
}
  
后台会打印这个文本的字节大小。看起来，这个是没有问题的。

关于InputStream类的available()方法
  
这个方法的意思是返回此输入流下一个方法调用可以不受阻塞地从此输入流读取（或跳过）的估计字节数。为什么需要这个方法？因为在一些网络应用中，数据流并不是一次性就能传递的，如果我们还是像上面那样去将这个流转换，会出问题的。我们来做一个例子，这是一个Socket编程的简单例子，具体Socket内容我会在后面文章中解释的。
  
首先编写两个类，一个用户初始化Socket服务，并且处理每个请求都有新的线程去处理，代码如下：
  
Java代码 收藏代码
  
package com.service;
  
import java.net.*;
  
public class DstService {
      
public static void main(String[] args) {
          
try {
              
// 启动监听端口 8001
              
ServerSocket ss = new ServerSocket(8001);
              
boolean bRunning = true;
              
while (bRunning) {
                  
// 接收请求
                  
Socket s = ss.accept();
                  
// 将请求指定一个线程去执行
                  
new Thread(new DstServiceImpl(s)).start();
              
}
          
} catch (Exception e) {
              
e.printStackTrace();
          
}
      
}
  
}
  
那么处理类我们也来看一下：
  
Java代码 收藏代码
  
package com.service;
  
import java.io.*;
  
import java.net.*;
  
import com.util.*;
  
public class DstServiceImpl implements Runnable {
      
Socket socket = null;
      
public DstServiceImpl(Socket s) {
          
this.socket = s;
      
}
      
public void run() {
          
try {
              
InputStream ips = socket.getInputStream();
              
OutputStream ops = socket.getOutputStream();
              
while (true) {
                  
byte[] bt = StreamTool.readStream(ips);
                  
String str = new String(bt);
                  
System.out.println("主机收到信息：" + str);
                  
String restr = "你好，主机已经收到信息！";
                  
ops.write(restr.getBytes());
                  
ops.flush();
              
}
          
} catch (Exception e) {
              
e.printStackTrace();
          
}
      
}
  
}
   
至于工具类，我就直接给代码了：
  
Java代码 收藏代码
  
package com.util;
  
import java.io.*;
  
public class StreamTool {
      
public static void main(String[] args) {
          
try {
              
File file = new File("C:&#92;ceshi.txt");
              
FileInputStream fin = new FileInputStream(file);
              
byte[] filebt = readStream(fin);
              
System.out.println(filebt.length);
          
} catch (Exception e) {
              
e.printStackTrace();
          
}
      
}
      
/**
       
* @功能 读取流
       
* @param inStream
       
* @return 字节数组
       
* @throws Exception
       
_/
      
public static byte[] readStream(InputStream inStream) throws Exception {
          
ByteArrayOutputStream outSteam = new ByteArrayOutputStream();
          
byte[] buffer = new byte[1024];
          
int len = -1;
          
while ((len = inStream.read(buffer)) != -1) {
              
outSteam.write(buffer, 0, len);
          
}
          
outSteam.close();
          
inStream.close();
          
return outSteam.toByteArray();
      
}
  
}
   
你可以直接运行这个类，会看到流被转换的效果。
  
我们来写一个Socket客户端测试一下：
  
Java代码 收藏代码
  
package com.client;
  
import java.io._;
  
import java.net.*;
  
import com.util.*;
  
public class DstClient {
      
public static void main(String[] args) {
          
try {
              
Socket socket = new Socket("127.0.0.1", 8001);
              
// 开启保持活动状态的套接字
              
socket.setKeepAlive(true);
              
// 设置读取超时时间
              
socket.setSoTimeout(30 * 1000);
              
OutputStream ops = socket.getOutputStream();
              
String mess = "你好，我是崔素强！";
              
ops.write(mess.getBytes());
              
InputStream ips = socket.getInputStream();
              
byte[] rebyte = StreamTool.readStream(ips);
              
String remess = new String(rebyte);
              
System.out.println("收到主机消息：" + remess);
              
socket.close();
          
} catch (Exception e) {
              
e.printStackTrace();
          
}
      
}
  
}
   
先运行DstService，然后运行客户端，看效果。会发现，控制台没有任何输出。经过调试发现，因为请求死在了
  
Java代码 收藏代码
  
while ((len = inStream.read(buffer)) != -1) {
  
这行代码上面。这就是在网络应用中会造成的后果。那么如何解决呢？有的人给出了如下代码：
  
Java代码 收藏代码
  
int count = in.available();
  
byte[] b = new byte[count];
  
in.read(b);
  
可是在进行网络操作时往往出错，因为你调用available()方法时，对发发送的数据可能还没有到达，你得到的count是0。需要做如下修改，是我们的读取流方法改成如下：
  
Java代码 收藏代码
  
/**
   
* @功能 读取流
   
* @param inStream
   
* @return 字节数组
   
* @throws Exception
   
*/
  
public static byte[] readStream(InputStream inStream) throws Exception {
      
int count = 0;
      
while (count == 0) {
          
count = inStream.available();
      
}
      
byte[] b = new byte[count];
      
inStream.read(b);
      
return b;
  
}
  
下面你在运行，会看到服务端和客户端都收到了消息。

关于InputStream.read(byte[] b)和InputStream.read(byte[] b,int off,int len)这两个方法都是用来从流里读取多个字节的，有经验的程序员就会发现，这两个方法经常 读取不到自己想要读取的个数的字节。比如第一个方法，程序员往往希望程序能读取到b.length个字节，而实际情况是，系统往往读取不了这么多。仔细阅读Java的API说明就发现了，这个方法 并不保证能读取这么多个字节，它只能保证最多读取这么多个字节(最少1个)。因此，如果要让程序读取count个字节，最好用以下代码：
  
Java代码 收藏代码
  
int count = 100;
  
byte[] b = new byte[count];
  
int readCount = 0; // 已经成功读取的字节的个数
  
while (readCount < count) {
      
readCount += inStream.read(b, readCount, count &#8211; readCount);
  
}
   
这样就能保证读取100个字节，除非中途遇到IO异常或者到了数据流的结尾情况！

[java]

ByteArrayOutputStream baos = new ByteArrayOutputStream();
  
int len = 0;
  
byte[] b = new byte[1024];
  
while ((len = is.read(b, 0, b.length)) != -1) {
  
baos.write(b, 0, len);
  
}
  
byte[] buffer =  baos.toByteArray();

[/java]

http://www.blogjava.net/anchor110/articles/343500.html
  
http://cuisuqiang.iteye.com/blog/1434416