---
title: Java RandomAccessFile, MappedByteBuffer, mmap
author: "-"
date: 2014-11-12T07:42:50+00:00
url: /?p=7007
tags:
  - Java
  - mmap
categories:
  - inbox
---
## Java RandomAccessFile, MappedByteBuffer, mmap

RandomAccessFile

RandomAccessFile是用来访问那些保存数据记录的文件的,你就可以用 seek() 方法来访问记录,并进行读写了。这些记录的大小不必相同；但是其大小和位置必须是可知的。但是该类仅限于操作文件。

RandomAccessFile不属于InputStream和OutputStream类系的。实际上,除了实现DataInput和DataOutput接口之外(DataInputStream和DataOutputStream也实现了这两个接口),它和这两个类系毫不相干,甚至不使用InputStream和OutputStream类中已经存在的任何功能；它是一个完全独立的类,所有方法(绝大多数都只属于它自己)都是从零开始写的。这可能是因为RandomAccessFile能在文件里面前后移动,所以它的行为与其它的I/O类有些根本性的不同。总而言之,它是一个直接继承Object的,独立的类。

基本上,RandomAccessFile的工作方式是,把DataInputStream和DataOutputStream结合起来,再加上它自己的一些方法,比如定位用的getFilePointer( ),在文件里移动用的seek( ),以及判断文件大小的length( )、skipBytes()跳过多少字节数。此外,它的构造函数还要一个表示以只读方式("r"),还是以读写方式("rw")打开文件的参数 (和C的fopen( )一模一样)。它不支持只写文件。

只有RandomAccessFile才有seek搜寻方法,而这个方法也只适用于文件。BufferedInputStream有一个mark( )方法,你可以用它来设定标记(把结果保存在一个内部变量里),然后再调用reset( )返回这个位置,但是它的功能太弱了,而且也不怎么实用。

RandomAccessFile的绝大多数功能,但不是全部,已经被JDK 1.4的nio的"内存映射文件(memory-mapped files)"给取代了,你该考虑一下是不是用"内存映射文件"来代替RandomAccessFile了。

import java.io.IOException;
  
import java.io.RandomAccessFile;
  
public class TestRandomAccessFile {

public static void main(String[] args) throws IOException {

RandomAccessFile rf = new RandomAccessFile("rtest.dat", "rw");

for (int i = 0; i < 10; i++) {

//写入基本类型double数据

rf.writeDouble(i * 1.414);

}

rf.close();

rf = new RandomAccessFile("rtest.dat", "rw");

//直接将文件指针移到第5个double数据后面

rf.seek(5 * 8);

//覆盖第6个double数据

rf.writeDouble(47.0001);

rf.close();

rf = new RandomAccessFile("rtest.dat", "r");

for (int i = 0; i < 10; i++) {

System.out.println("Value " + i + ": " + rf.readDouble());

}

rf.close();

}
  
}

### 内存映射文件, mmap, FileChannel

内存映射文件能让你创建和修改那些因为太大而无法放入内存的文件。有了内存映射文件, 你就可以认为文件已经全部读进了内存, 然后把它当成一个非常大的数组来访问。这种解决办法能大大简化修改文件的代码。
  
fileChannel.map(FileChannel.MapMode mode, long position, long size) 将此通道的文件区域直接映射到内存中。注意, 你必须指明, 它是从文件的哪个位置开始映射的, 映射的范围又有多大；也就是说,它还可以映射一个大文件的某个小片断。
  
MappedByteBuffer是ByteBuffer的子类,因此它具备了ByteBuffer的所有方法,但新添了force()将缓冲区的内容强制刷新到存储设备中去、load()将存储设备中的数据加载到内存中、isLoaded()位置内存中的数据是否与存储设置上同步。这里只简单地演示了一下put()和get()方法,除此之外,你还可以使用asCharBuffer( )之类的方法得到相应基本类型数据的缓冲视图后,可以方便的读写基本类型数据。

import java.io.RandomAccessFile;
  
import java.nio.MappedByteBuffer;
  
import java.nio.channels.FileChannel;
  
public class LargeMappedFiles {

static int length = 0x8000000; // 128 Mb

public static void main(String[] args) throws Exception {

// 为了以可读可写的方式打开文件,这里使用RandomAccessFile来创建文件。

FileChannel fc = new RandomAccessFile("test.dat", "rw").getChannel();

//注意,文件通道的可读可写要建立在文件流本身可读写的基础之上

MappedByteBuffer out = fc.map(FileChannel.MapMode.READ_WRITE, 0, length);

//写128M的内容

for (int i = 0; i < length; i++) {

out.put((byte) 'x');

}

System.out.println("Finished writing");

//读取文件中间6个字节内容

for (int i = length / 2; i < length / 2 + 6; i++) {

System.out.print((char) out.get(i));

}

fc.close();

}
  
}

尽管映射写似乎要用到FileOutputStream,但是映射文件中的所有输出 必须使用RandomAccessFile,但如果只需要读时可以使用FileInputStream,写映射文件时一定要使用随机访问文件,可能写时要读的原因吧。

该程序创建了一个128Mb的文件,如果一次性读到内存可能导致内存溢出,但这里访问好像只是一瞬间的事,这是因为,真正调入内存的只是其中的一小部分,其余部分则被放在交换文件上。这样你就可以很方便地修改超大型的文件了(最大可以到2 GB)。注意,Java是调用操作系统的"文件映射机制"来提升性能的。

RandomAccessFile类的应用:

/*

* 程序功能: 演示了RandomAccessFile类的操作,同时实现了一个文件复制操作。

_/
  
package com.lwj.demo;
  
import java.io._;
  
public class RandomAccessFileDemo {

public static void main(String[] args) throws Exception {

RandomAccessFile file = new RandomAccessFile("file", "rw");

// 以下向file文件中写数据

file.writeInt(20);// 占4个字节

file.writeDouble(8.236598);// 占8个字节

file.writeUTF("这是一个UTF字符串");// 这个长度写在当前文件指针的前两个字节处,可用readShort()读取

file.writeBoolean(true);// 占1个字节

file.writeShort(395);// 占2个字节

file.writeLong(2325451l);// 占8个字节

file.writeUTF("又是一个UTF字符串");

file.writeFloat(35.5f);// 占4个字节

file.writeChar('a');// 占2个字节

file.seek(0);// 把文件指针位置设置到文件起始处

// 以下从file文件中读数据,要注意文件指针的位置

System.out.println("——————从file文件指定位置读数据——————");

System.out.println(file.readInt());

System.out.println(file.readDouble());

System.out.println(file.readUTF());

file.skipBytes(3);// 将文件指针跳过3个字节,本例中即跳过了一个boolean值和short值。

System.out.println(file.readLong());

file.skipBytes(file.readShort()); // 跳过文件中"又是一个UTF字符串"所占字节,注意readShort()方法会移动文件指针,所以不用加2。

System.out.println(file.readFloat());

//以下演示文件复制操作

System.out.println("——————文件复制 (从file到fileCopy) ——————");

file.seek(0);

RandomAccessFile fileCopy=new RandomAccessFile("fileCopy","rw");

int len=(int)file.length();//取得文件长度 (字节数)

byte[] b=new byte[len];

file.readFully(b);

fileCopy.write(b);

System.out.println("复制完成！");

}
  
}
  
RandomAccessFile 插入写示例:

/**

*

* @param skip 跳过多少过字节进行插入数据

* @param str 要插入的字符串

* @param fileName 文件路径

*/
  
public static void beiju(long skip, String str, String fileName){

try {

RandomAccessFile raf = new RandomAccessFile(fileName,"rw");

if(skip < 0 || skip > raf.length()){

System.out.println("跳过字节数无效");

return;

}

byte[] b = str.getBytes();

raf.setLength(raf.length() + b.length);

for(long i = raf.length() – 1; i > b.length + skip – 1; i–){

raf.seek(i – b.length);

byte temp = raf.readByte();

raf.seek(i);

raf.writeByte(temp);

}

raf.seek(skip);

raf.write(b);

raf.close();

} catch (Exception e) {

e.printStackTrace();

}
  
}

利用RandomAccessFile实现文件的多线程下载,即多线程下载一个文件时,将文件分成几块,每块用不同的线程进行下载。下面是一个利用多线程在写文件时的例子,其中预先分配文件所需要的空间,然后在所分配的空间中进行分块,然后写入:

import java.io.FileNotFoundException;
  
import java.io.IOException;
  
import java.io.RandomAccessFile;
  
/**

* 测试利用多线程进行文件的写操作

_/
  
public class Test {

public static void main(String[] args) throws Exception {

// 预分配文件所占的磁盘空间,磁盘中会创建一个指定大小的文件

RandomAccessFile raf = new RandomAccessFile("D://abc.txt", "rw");

raf.setLength(1024_1024); // 预分配 1M 的文件空间

raf.close();

// 所要写入的文件内容

String s1 = "第一个字符串";

String s2 = "第二个字符串";

String s3 = "第三个字符串";

String s4 = "第四个字符串";

String s5 = "第五个字符串";

// 利用多线程同时写入一个文件

new FileWriteThread(1024_1,s1.getBytes()).start(); // 从文件的1024字节之后开始写入数据

new FileWriteThread(1024_2,s2.getBytes()).start(); // 从文件的2048字节之后开始写入数据

new FileWriteThread(1024_3,s3.getBytes()).start(); // 从文件的3072字节之后开始写入数据

new FileWriteThread(1024_4,s4.getBytes()).start(); // 从文件的4096字节之后开始写入数据

new FileWriteThread(1024*5,s5.getBytes()).start(); // 从文件的5120字节之后开始写入数据

}

// 利用线程在文件的指定位置写入指定数据

static class FileWriteThread extends Thread{

private int skip;

private byte[] content;

public FileWriteThread(int skip,byte[] content){

this.skip = skip;

this.content = content;

}

public void run(){

RandomAccessFile raf = null;

try {

raf = new RandomAccessFile("D://abc.txt", "rw");

raf.seek(skip);

raf.write(content);

} catch (FileNotFoundException e) {

e.printStackTrace();

} catch (IOException e) {

// TODO Auto-generated catch block

e.printStackTrace();

} finally {

try {

raf.close();

} catch (Exception e) {

}

}

}

}
  
}

>[http://www.ibm.com/developerworks/cn/java/l-javaio/](http://www.ibm.com/developerworks/cn/java/l-javaio/)
  
[http://blog.csdn.net/napolunyishi/article/details/18214929](http://blog.csdn.net/napolunyishi/article/details/18214929)
  
[http://blog.csdn.net/akon_vm/article/details/7429245](http://blog.csdn.net/akon_vm/article/details/7429245)
  
[http://blog.csdn.net/kabini/article/details/4286737](http://blog.csdn.net/kabini/article/details/4286737)
