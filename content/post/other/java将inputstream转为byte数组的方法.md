---
title: java IO, InputStream, OutputStream
author: "-"
date: 2013-01-16T04:31:49+00:00
url: /?p=5029
categories:
  - Java
tags:$
  - reprint
---
## java IO, InputStream, OutputStream

InputStream和OutStream是java.io包中面向字节操作的两个顶层抽象类，所有关于java同步IO字节流的操作都是基于这两个的。

什么是流？
《O'Reilly-Java Io》中是这么解释的: 

A stream is an ordered sequence of bytes of undetermined length. Input streams move bytes
of data into a Java program from some generally external source. Output streams move bytes
of data from Java to some generally external target. (In special cases streams can also move
bytes from one part of a Java program to another.)

流是一个不确定长度的有序字节序列。输入流从外部资源将数据字节移动到Java程序中。输出流从Java程序中将数据字节移动到外部目标。 (特殊的情况也可以将字节从java程序中一部分移动到另一部分) 

流从哪里来？
通常流来自于: 
1. 网络
2. 文件
3. java内部程序

InputStream (输入流) : 
InputStream作为java中用于读取流中字节的顶层抽象类，定义了一些方法: 
public abstract int read() throws IOException
public int read(byte b[], int off, int len) throws IOException
public int read(byte b[]) throws IOException {
        return read(b, 0, b.length);
}
有三个read方法用来读取字节: 
1. 第一个抽象方法交由子类来实现，读取一个无符号字节，由于java本身没有无符号字节的基本类型，所以用int作为返回值。当返回-1时表示到了流的结尾，这也是需要返回int的原因之一 (因为带符号的byte有可能是-1) 

2. 
作用:  从流中读取字节数组，通常一个一个字节的读效率相当低下，可指定数组中开始的偏移位置off，长度len
参数:  保存字节的字节数组、偏移量、长度。
返回值:  实际读到的字节数 (-1为末尾) 
默认的实现依赖于第一个抽象方法，就是循环调用读取一个无符号字节。所以效率不是很高，通常会有的子类以更高效的方式来重写。

3. 
作用:  从流中读取字节数组，通常一个一个字节的读效率相当低下。
参数:  保存字节的字节数组
返回值:  实际读到的字节数 (-1为末尾) 
默认的实现依赖于第二个方法，仅仅是用read(b,0,b.length)来实现，重写这个方法的子类相对较少。

public int available() throws IOException
作用:  从流中立刻能够获取到的字节数。
返回值:  能够读取到的字节数 (没有会返回0，到流的末尾也会返回0) 

public long skip(long bytesToSkip) throws IOException
作用:  从流中跳过一定字节不读，通常跳过比读取后不处理快 (比如文件流，只是指针的移动) 。
参数:  期望跳过的字节数
返回值: 实际跳过的字节数 (遇到末尾返回-1) 

public void close() throws IOException
作用:  用完流之后，关闭流，但并不是所有的流都需要关闭，比如说System.in。

关闭流的最佳实践: 
1. 在finally中关闭

.
    InputStream in = null;
    try {
        in = new ...;
        ...
    } catch(IOException e) {
        ...
    } finally {
        try {
            if (in != null) {
                in.close();
            }
        } catch(IOException e) {
    
        }
    }
2. java7支持try-with-resources方式关闭流，实现了java.lang.AutoCloseable接口的对象支持用这种方式

.
    try (InputStream in = new ....){
        ...
    } catch(IOException e) {
        ...
    }
标记和重置: 
public synchronized void mark(int readLimit)
public synchronized void reset() throws IOException
public boolean markSupported()
有时候你读取一些字节后希望返回到之前的位置重新读，这几个方法就是用来做这件事。

public boolean markSupported()
作用:  判断当前流是否支持标记
返回值:  当前流是否支持标记
如果当前流不支持标记，执行reset()方法将抛出一个IOException异常，而mark () 方法不会做任何操作

public synchronized void mark(int readLimit)
作用:  将读取的位置标记在当前位置。
参数:  最大可阅读超过标记位置的字节数 (只要没有阅读超过readLimit字节数，就可以重置回去) 
在同一时刻，只能有一个标记，再设置会覆盖
java.io中只有BufferedInputStream和ByteArrayInputStream支持标记。但是其他的过滤流连接到这两个上也支持标记。

OutputStream (输出流) : 
OutputStream作为java中用于向流中写字节的顶层抽象类，定义了一些方法: 
public abstract void write(int b) throws IOException
public void write(byte[] data, int offset, int length) throws IOException
public void write(byte[] data) throws IOException
有三个write方法用来向流中写字节: 

1. 第一个是抽象方法交由子类实现，向流中写入一个无符号字节 (0-255) ，如果超过255只会取低八位的字节。

2. 作用:  向流中写入字节数组，可以指定数组中起始的偏移位置和长度。
参数:  写入的字符数组、起始的偏移位置、长度
默认的实现是循环调用第一个方法一个一个写入，但是效率极其低下，子类一般会有更高效的方式

3. 作用:  向流中写入字节数组
参数:  写入的字符数组
默认的实现是调用第二个write()方法write(b, 0, b.length);

public void flush() throws IOException
作用:  许多输出流增加一个缓冲区来提升性能，当缓冲区写满之后才会发送数据，而flush()方法可以强制清空缓冲区发送数据，如果不刷新则有可能导致数据丢失。通常PrintStream的println()方法会自动flush()

public void close() throws IOException
作用:  当用完输出流之后，将流关闭，关闭的同时也会flush()

无处不在的IOException:
IOException是受检异常，在程序中必须被声明。
IOException存在的意义是因为操作系统中的‘输入’和‘输出’是不可靠的，操作系统层级发生的异常是不受程序控制。

子类
java.io包中常用的子类: 

图
其它包中还有一些类。

作者: Draft灬h
链接: https://www.jianshu.com/p/375ee4a42c34
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
