---
title: Java 流, Stream
author: lcf
date: 2012-09-25T06:38:01+00:00
url: /?p=4278
categories:
  - Java
tags:$
  - reprint
---
## Java 流, Stream
IO流的分类: 
  
1. 根据流的数据对象来分: 
  
高端流: 所有的内存中的流都是高端流，比如: InputStreamReader
  
低端流: 所有的外界设备中的流都是低端流，比如InputStream，OutputStream
  
如何区分: 所有的流对象的后缀中包含Reader或者Writer的都是高端流，反之，则基本上为低端流，不过也有例外，比如PrintStream就是高端流

2. 根据数据的流向来分: 
  
输出流: 是用来写数据的，是由程序 (内存) ->外界设备
  
输入流: 是用来读数据的，是由外界设备->程序 (内存) 
  
如何区分: 一般来说输入流带有Input，输出流带有Output

3. 根据流数据的格式来分: 
- 字节流: 处理声音或者图片等二进制的数据的流，比如InputStream
- 字符流: 处理文本数据 (如txt文件) 的流，比如InputStreamReader
  
如何区分: 可用高低端流来区分，所有的低端流都是字节流，所有的高端流都是字符流

4. 根据流数据的包装过程来分: 
  
原始流: 在实例化流的对象的过程中，不需要传入另外一个流作为自己构造方法的参数的流，称之为原始流。
  
包装流: 在实例化流的对象的过程中，需要传入另外一个流作为自己构造方法发参数的流，称之为包装流。
  
如何区分: 所以的低端流都是原始流，所以的高端流都是包装流

流是 Java 中最重要的基本概念之一。文件读写、网络收发、进程通信，几乎所有需要输入输出的地方，都要用到流。

流是做什么用的呢？就是做输入输出用的。为什么输入输出要用"流"这种方式呢？因为程序输入输出的基本单位是字节，输入就是获取一串字节，输出就是发送一串字节。但是很多情况下，程序不可能接收所有的字节之后再进行处理，而是接收一点处理一点。比方你下载魔兽世界，不可能全部下载到内存里再保存到硬盘上，而是下载一点就保存一点。这时，流这种方式就非常适合。

在 Java 中，每个流都是一个对象。流分为两种: 输入流(InputStream)和输出流(OutputStream)。对于输入流，你只要从流当中不停地把字节取出来就是了；而对于输出流，你只要把准备好的字节串传给它就行。

____________\__Java 程序____________
  
| |
  
外部系统 –|–(输入流)–> 处理逻辑 –(输出流)—|–> 外部系统
  
|_________________________________|

流对象是怎么获得的呢？不同的外部系统，获取流的方式也不同。例如，文件读写就要创建 FileInputStream/FileOutputStream 对象，而网络通信是通过 Socket 对象来获取输入输出流的。一般来说，如果一个类有 getInputStream() 或 getOutputStream() 这样的方法，就表明它是通过流对象来进行输入输出的。

InputStream 是输入流，下面是一个通过 InputStream 读取文件的例子: 

import java.io.File;
  
import java.io.FileInputStream;
  
import java.io.IOException;
  
import java.io.InputStream;
  
import java.io.FileNotFoundException;
  
import java.util.Arrays;

/**
   
* 通过流读取文件
   
*/
  
public class ReadFileDemo {

// 程序入口
   
public static void main(String[] args) {
   
String path = "c:/boot.ini";
   
File file = new File(path);

// 创建输入流
   
InputStream is;
   
try {
   
is = new FileInputStream(file);
   
} catch (FileNotFoundException e) {
   
System.err.println("文件 " + path + " 不存在。");
   
return;
   
}

// 开始读取
   
byte[] content = new byte[0]; // 保存读取出来的文件内容
   
byte[] buffer = new byte[10240]; // 定义缓存

try {
   
int eachTime = is.read(buffer); // 第一次读取。如果返回值为 -1 就表示没有内容可读了。
   
while (eachTime != -1) {
   
// 读取出来的内容放在 buffer 中，现在将其合并到 content。
   
content = concatByteArrays(content, buffer, eachTime);
   
eachTime = is.read(buffer); // 继续读取
   
}
   
} catch (IOException e) {
   
System.err.println("读取文件内容失败。");
   
e.printStackTrace();
   
} finally {
   
try {
   
is.close();
   
} catch (IOException e) {
   
// 这里的异常可以忽略不处理
   
}
   
}

// 输出文件内容
   
String contentStr = new String(content);
   
System.out.println(contentStr);
   
}

/**
   
* 合并两个字节串
   
*
   
* @param bytes1 字节串1
   
* @param bytes2 字节串2
   
* @param sizeOfBytes2 需要从 bytes2 中取出的长度
   
*
   
* @return bytes1 和 bytes2 中的前 sizeOfBytes2 个字节合并后的结果
   
*/
   
private static byte[] concatByteArrays(byte[] bytes1, byte[] bytes2, int sizeOfBytes2) {
   
byte[] result = Arrays.copyOf(bytes1, (bytes1.length + sizeOfBytes2));
   
System.arraycopy(bytes2, 0, result, bytes1.length, sizeOfBytes2);
   
return result;
   
}
  
}
  
虽然写得很啰嗦，但这确实是 InputStream 的基本用法。注意，这只是一个例子，说明如何从输入流中读取字节串。实际上，Java 提供更简单的方式来读取文本文件。以后将会介绍。

相比从流中读取，使用 OutputStream 输出则是非常简单的事情。下面是一个例子: 

import java.io.OutputStream;
  
import java.io.FileOutputStream;
  
import java.io.File;
  
import java.io.IOException;
  
import java.util.Date;

/**
   
* 将当前日期保存到文件
   
*/
  
public class SaveFileDemo {

public static void main(String[] args) throws IOException {
   
String path = "c:/now.txt";

File file = new File(path);
   
if (!file.exists() && !file.createNewFile()) {
   
System.err.println("无法创建文件。");
   
return;
   
}

OutputStream os = new FileOutputStream(file); // 创建输出流 (前提是文件存在) 
   
os.write(new Date().toString().getBytes()); // 将当前时间写入文件
   
os.close(); // 必须关闭流，内容才会写入文件。
   
System.out.println("文件写入完成。");
   
}
  
}
  
Java 还提供其它的流操作方式，但它们都是对 InputStream 和 OutputStream 进行扩展或包装。所以这两个类是基础，必须要理解它们的使用。

Java将数据于目的地及来源之间的流动抽象化为一个流(Stream)，而流当中流动的则是位数据。
  
14.2.1InputStream和OutputStream
  
计算机中实际上数据的流动是通过电路，而上面流动的则是电流，电流的电位有低位与高位，即数字的0与1位。从程序的观点来说，通常会将数据目的地(例如内存)与来源(例如文件)之间的数据流动抽象化为一个流(Stream)，而其中流动的则是位数据，如图14-1所示。

图14-1 数据的流动抽象化为流的概念
  
在Java SE中有两个类用来作流的抽象表示: java.io.InputStream与java.io.OutputStream。
  
InputStream 是所有表示位输入流的类之父类，它是一个抽象类，继承它的子类要重新定义其中所定义的抽象方法。InputStream是从装置来源地读取数据的抽象表示，例如System中的标准输入流in对象就是一个InputStream类型的实例。在Java程序开始之后，in流对象就会开启，目的是从标准输入装置中读取数据，这个装置通常是键盘或是用户定义的输入装置。
  
OutputStream 是所有表示位输出流的类之父类，它是一个抽象类。子类要重新定义其中所定义的抽象方法，OutputStream是用于将数据写入目的地的抽象表示。例如 System中的标准输出流对象out其类型是java.io.PrintStream，这个类是OutputStream的子类 (java.io.FilterOutputStream继承OutputStream， PrintStream再继承FilterOutputStream)。在程序开始之后，out流对象就会开启，可以通过out来将数据写至目的地装置，这个装置通常是屏幕显示或用户定义的输出装置。
  
范例14.4可以读取键盘输入流，in对象的read()方法一次读取一个字节的数据，读入的数据以int类型返回。所以在使用out对象将数据显示出来时，就是10进制方式。
  
ü 范例14.4 StreamDemo.java
  
package onlyfun.caterpillar;
  
import java.io.*;
  
public class StreamDemo {
      
public static void main(String[] args) {
          
try {
              
System.out.print("输入字符: ");
              
System.out.println("输入字符十进制表示: " +
                                      
System.in.read());
          
}
          
catch(IOException e) {
              
e.printStackTrace();
          
}
      
}
  
}
  
执行结果: 
  
输入字符: A
  
输入字符十进制表示: 65
  
字符A输入后由标准输入流in读取，A的位表示以十进制来看就是65，这是A字符的编码(查查ASCII编码表就知道了)。
  
一般来说，很少直接实现InputStream或OutputStream上的方法，因为这些方法比较低级，通常会实现它们的子类。这些子类上所定义的方法在进行输入/输出时更为方便。
  
14.2.2FileInputStream和FileOutputStream
  
java.io.FileInputStream 是InputStream的子类。从开头File名称上就可以知道，FileInputStream与从指定的文件中读取数据至目的地有关。而 java.io.FileOutputStream是OutputStream的子类，顾名思义，FileOutputStream主要与从来源地写入数据至指定的文件中有关。
  
当建立一个FileInputStream或FileOutputStream的实例时，必须指定文件位置及文件名称，实例被建立时文件的流就会开启；而不使用流时，必须关闭文件流，以释放与流相依的系统资源，完成文件读/写的动作。
  
FileInputStream可以使用 read()方法一次读入一个字节，并以int类型返回，或者是使用read()方法时读入至一个byte数组，byte数组的元素有多少个，就读入多少个字节。在将整个文件读取完成或写入完毕的过程中，这么一个byte数组通常被当作缓冲区，因为这么一个byte数组通常扮演承接数据的中间角色。
  
范例14.5是使用FileInputStream与FileOutputStream的一个例子。程序可以复制文件，它会先从来源文件读取数据至一个byte数组中，然后再将byte数组的数据写入目的文件。
  
ü 范例14.5 FileStreamDemo.java
  
package onlyfun.caterpillar;
  
import java.io.*;
  
public class FileStreamDemo {
      
public static void main(String[] args) {
          
try {
              
byte[] buffer = new byte[1024];
              
// 来源文件
              
FileInputStream fileInputStream =
                  
new FileInputStream(new File(args[0]));
              
// 目的文件
              
FileOutputStream fileOutputStream =
                  
new FileOutputStream(new File(args[1]));
              
// available()可取得未读取的数据长度
              
System.out.println("复制文件: " +
                      
fileInputStream.available() + "字节");

            while(true) {
                if(fileInputStream.available() < 1024) {
                    // 剩余的数据比1024字节少
                    // 一位一位读出再写入目的文件
                    int remain = -1;
                    while((remain = fileInputStream.read())
                                           != -1) {
                        fileOutputStream.write(remain);
                    }
                    break;
                }
                else {
                    // 从来源文件读取数据至缓冲区
                    fileInputStream.read(buffer);
                    // 将数组数据写入目的文件
                    fileOutputStream.write(buffer);
                }
            }
            // 关闭流
            fileInputStream.close();
            fileOutputStream.close();
            System.out.println("复制完成");
        }
        catch(ArrayIndexOutOfBoundsException e) {
            System.out.println(
                      "using: java FileStreamDemo src des");
            e.printStackTrace();
        }
        catch(IOException e) {
            e.printStackTrace();
        }
    }
    

}
  
程序中示范了两个read()方法，一个方法可以读入指定长度的数据至数组，另一个方法一次可以读入一个字节。每次读取之后，读取的光标都会往前进，如果读不到数据则返回–1，使用available()方法获得还有多少字节可以读取。除了使用File来建立FileInputStream、 FileOutputStream的实例之外，也可以直接使用字符串指定路径来建立。
  
// 来源文件FileInputStream fileInputStream = new FileInputStream(args[0]);// 目的文件FileOutputStream fileOutputStream = new FileOutputStream(args[1]);在不使用文件流时，记得使用close()方法自行关闭流，以释放与流相依的系统资源。一个执行的结果范例如下，它将FileDemo.java复制为FileDemo.txt: 
  
java onlyfun.caterpillar.FileStreamDemo FileDemo.java FileDemo.txt
  
复制文件: 1723字节
  
复制完成
  
FileOutputStream默认会以新建文件的方式来开启流。如果指定的文件名称已经存在，则原文件会被覆盖；如果想以附加的模式来写入文件，则可以在构建FileOutputStream实例时指定为附加模式。例如: 
  
FileOutputStream fileOutputStream = new FileOutputStream(args[1], true);构建方法的第二个append参数如果设置为true，在开启流时如果文件不存在则会新建一个文件，如果文件存在就直接开启流，并将写入的数据附加至文件末端。

虽然我一向不喜欢使用过长的范例来作程序示范(也不喜欢看很长的范例)，不过本章的范例与其他各章的比起来相对长了一些，我会在程序中多用注释解释程序的逻辑。因为解释输入/输出操作最好的方式，是呈现一个具实用性的范例，本章的范例除了练习的作用之外，日后需要某些输入/输出功能时，也可以来参考看看如何实现。
  
14.2.3BufferedInputStream和BufferedOutputStream
  
在介绍FileInputStream和 FileOutputStream的例子中，使用了一个byte数组来作为数据读入的缓冲区，以文件存取为例，硬盘存取的速度远低于内存中的数据存取速度。为了减少对硬盘的存取，通常从文件中一次读入一定长度的数据，而写入时也是一次写入一定长度的数据，这可以增加文件存取的效率。
  
java.io.BufferedInputStream 与java.io.BufferedOutputStream可以为InputStream、OutputStream类的对象增加缓冲区功能。构建 BufferedInputStream实例时，需要给定一个InputStream类型的实例，实现BufferedInputStream时，实际上最后是实现InputStream实例。同样地，在构建BufferedOutputStream时，也需要给定一个OutputStream实例，实现 BufferedOutputStream时，实际上最后是实现OutputStream实例。
  
BufferedInputStream的数据成员buf是一个位数组，默认为2048字节。当读取数据来源时，例如文件，BufferedInputStream会尽量将buf填满。当使用read ()方法时，实际上是先读取buf中的数据，而不是直接对数据来源作读取。当buf中的数据不足时，BufferedInputStream才会再实现给定的InputStream对象的read()方法，从指定的装置中提取数据，如图14-2所示。

图14-2 BufferedInputStream在内部有buf成员作为缓冲区
  
BufferedOutputStream的数据成员buf是一个位数组，默认为512字节。当使用write()方法写入数据时，实际上会先将数据写至buf中，当buf已满时才会实现给定的 OutputStream对象的write()方法，将buf数据写至目的地，而不是每次都对目的地作写入的动作。
  
下面将范例14.5做个改写，这次不用自行设置缓冲区，而使用BufferedInputStream和BufferedOutputStream让程序看来简单一些，也比较有效率。
  
ü 范例14.6 BufferedStreamDemo.java
  
package onlyfun.caterpillar;
  
import java.io.*;
  
public class BufferedStreamDemo {
      
public static void main(String[] args) {
          
try {
              
byte[] data = new byte[1];
              
File srcFile = new File(args[0]);
              
File desFile = new File(args[1]);
              
BufferedInputStream bufferedInputStream =
                  
new BufferedInputStream(
                           
new FileInputStream(srcFile));
              
BufferedOutputStream bufferedOutputStream =
                  
new BufferedOutputStream(
                           
new FileOutputStream(desFile));
              
System.out.println("复制文件: " +
                               
srcFile.length() + "字节");
              
while(bufferedInputStream.read(data) != -1) {
                  
bufferedOutputStream.write(data);
              
}

            // 将缓冲区中的数据全部写出
            bufferedOutputStream.flush();
            // 关闭流
            bufferedInputStream.close();
            bufferedOutputStream.close();
            System.out.println("复制完成");
        }
        catch(ArrayIndexOutOfBoundsException e) {
            System.out.println(
                    "using: java UseFileStream src des");
            e.printStackTrace();
        }
        catch(IOException e) {
            e.printStackTrace();
        }
    }
    

}
  
为了确保缓冲区中的数据一定被写出至目的地，建议最后执行flush()将缓冲区中的数据全部写出目的流中。这个范例的执行结果与范例14.5是相同的。
  
BufferedInputStream和 BufferedOutputStream并没有改变InputStream或 OutputStream的行为，读入或写出时的动作还是InputStream和OutputStream负责。 BufferedInputStream和BufferedOutputStream只是在操作对应的方法之前，动态地为它们加上一些额外功能(像缓冲区功能)，在这里是以文件存取流为例，实际上可以在其他流对象上也使用BufferedInputStream和BufferedOutputStream 功能。
  
http://book.51cto.com/art/200812/101093.htm
  
http://blog.csdn.net/YidingHe/article/details/4093892
  
http://www.cnblogs.com/chen-lhx/p/4992401.html