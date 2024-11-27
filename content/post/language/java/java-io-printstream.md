---
title: java io PrintStream
author: "-"
date: 2017-02-04T04:32:31+00:00
url: /?p=9705
categories:
  - Inbox
tags:
  - reprint
---
## java io PrintStream
http://www.cnblogs.com/skywang12345/p/io_16.html


本章介绍PrintStream以及 它与DataOutputStream的区别。我们先对PrintStream有个大致认识,然后再深入学习它的源码,最后通过示例加深对它的了解。

转载请注明出处: http://www.cnblogs.com/skywang12345/p/io_16.html

PrintStream 介绍
  
PrintStream 是打印输出流,它继承于FilterOutputStream。
  
PrintStream 是用来装饰其它输出流。它能为其他输出流添加了功能,使它们能够方便地打印各种数据值表示形式。
  
与其他输出流不同,PrintStream 永远不会抛出 IOException；它产生的IOException会被自身的函数所捕获并设置错误标记, 用户可以通过 checkError() 返回错误标记,从而查看PrintStream内部是否产生了IOException。
  
另外,PrintStream 提供了自动flush 和 字符集设置功能。所谓自动flush,就是往PrintStream写入的数据会立刻调用flush()函数。
  
PrintStream 函数列表
  
/*
  
* 构造函数
  
*/
  
// 将"输出流out"作为PrintStream的输出流,不会自动flush,并且采用默认字符集
  
// 所谓"自动flush",就是每次执行print(), println(), write()函数,都会调用flush()函数；
  
// 而"不自动flush",则需要我们手动调用flush()接口。
  
PrintStream(OutputStream out)
  
// 将"输出流out"作为PrintStream的输出流,自动flush,并且采用默认字符集。
  
PrintStream(OutputStream out, boolean autoFlush)
  
// 将"输出流out"作为PrintStream的输出流,自动flush,采用charsetName字符集。
  
PrintStream(OutputStream out, boolean autoFlush, String charsetName)
  
// 创建file对应的FileOutputStream,然后将该FileOutputStream作为PrintStream的输出流,不自动flush,采用默认字符集。
  
PrintStream(File file)
  
// 创建file对应的FileOutputStream,然后将该FileOutputStream作为PrintStream的输出流,不自动flush,采用charsetName字符集。
  
PrintStream(File file, String charsetName)
  
// 创建fileName对应的FileOutputStream,然后将该FileOutputStream作为PrintStream的输出流,不自动flush,采用默认字符集。
  
PrintStream(String fileName)
  
// 创建fileName对应的FileOutputStream,然后将该FileOutputStream作为PrintStream的输出流,不自动flush,采用charsetName字符集。
  
PrintStream(String fileName, String charsetName)

// 将"字符c"追加到"PrintStream输出流中"
  
PrintStream append(char c)
  
// 将"字符序列从start(包括)到end(不包括)的全部字符"追加到"PrintStream输出流中"
  
PrintStream append(CharSequence charSequence, int start, int end)
  
// 将"字符序列的全部字符"追加到"PrintStream输出流中"
  
PrintStream append(CharSequence charSequence)
  
// flush"PrintStream输出流缓冲中的数据",并检查错误
  
boolean checkError()
  
// 关闭"PrintStream输出流"
  
synchronized void close()
  
// flush"PrintStream输出流缓冲中的数据"。
  
// 例如,PrintStream装饰的是FileOutputStream,则调用flush时会将数据写入到文件中
  
synchronized void flush()
  
// 根据"Locale值(区域属性)"来格式化数据
  
PrintStream format(Locale l, String format, Object... args)
  
// 根据"默认的Locale值(区域属性)"来格式化数据
  
PrintStream format(String format, Object... args)
  
// 将"float数据f对应的字符串"写入到"PrintStream输出流"中,print实际调用的是write函数
  
void print(float f)
  
// 将"double数据d对应的字符串"写入到"PrintStream输出流"中,print实际调用的是write函数
  
void print(double d)
  
// 将"字符串数据str"写入到"PrintStream输出流"中,print实际调用的是write函数
  
synchronized void print(String str)
  
// 将"对象o对应的字符串"写入到"PrintStream输出流"中,print实际调用的是write函数
  
void print(Object o)
  
// 将"字符c对应的字符串"写入到"PrintStream输出流"中,print实际调用的是write函数
  
void print(char c)
  
// 将"字符数组chars对应的字符串"写入到"PrintStream输出流"中,print实际调用的是write函数
  
void print(char[] chars)
  
// 将"long型数据l对应的字符串"写入到"PrintStream输出流"中,print实际调用的是write函数
  
void print(long l)
  
// 将"int数据i对应的字符串"写入到"PrintStream输出流"中,print实际调用的是write函数
  
void print(int i)
  
// 将"boolean数据b对应的字符串"写入到"PrintStream输出流"中,print实际调用的是write函数
  
void print(boolean b)
  
// 将"数据args"根据"Locale值(区域属性)"按照format格式化,并写入到"PrintStream输出流"中
  
PrintStream printf(Locale l, String format, Object... args)
  
// 将"数据args"根据"默认Locale值(区域属性)"按照format格式化,并写入到"PrintStream输出流"中
  
PrintStream printf(String format, Object... args)
  
// 将"换行符"写入到"PrintStream输出流"中,println实际调用的是write函数
  
void println()
  
// 将"float数据对应的字符串+换行符"写入到"PrintStream输出流"中,println实际调用的是write函数
  
void println(float f)
  
// 将"int数据对应的字符串+换行符"写入到"PrintStream输出流"中,println实际调用的是write函数
  
void println(int i)
  
// 将"long数据对应的字符串+换行符"写入到"PrintStream输出流"中,println实际调用的是write函数
  
void println(long l)
  
// 将"对象o对应的字符串+换行符"写入到"PrintStream输出流"中,println实际调用的是write函数
  
void println(Object o)
  
// 将"字符数组chars对应的字符串+换行符"写入到"PrintStream输出流"中,println实际调用的是write函数
  
void println(char[] chars)
  
// 将"字符串str+换行符"写入到"PrintStream输出流"中,println实际调用的是write函数
  
synchronized void println(String str)
  
// 将"字符c对应的字符串+换行符"写入到"PrintStream输出流"中,println实际调用的是write函数
  
void println(char c)
  
// 将"double数据对应的字符串+换行符"写入到"PrintStream输出流"中,println实际调用的是write函数
  
void println(double d)
  
// 将"boolean数据对应的字符串+换行符"写入到"PrintStream输出流"中,println实际调用的是write函数
  
void println(boolean b)
  
// 将数据oneByte写入到"PrintStream输出流"中。oneByte虽然是int类型,但实际只会写入一个字节
  
synchronized void write(int oneByte)
  
// 将"buffer中从offset开始的length个字节"写入到"PrintStream输出流"中。
  
void write(byte[] buffer, int offset, int length)

注意: print()和println()都是将其中参数转换成字符串之后,再写入到输入流。
  
例如,

print(0x61);
  
等价于

write(String.valueOf(0x61));
  
上面语句是将字符串"97"写入到输出流。0x61对应十进制数是97。

write(0x61)
  
上面语句是将字符'a'写入到输出流。因为0x61对应的ASCII码的字母'a'。

查看下面的代码,我们能对这些函数有更清晰的认识！


PrintStream 源码分析(基于jdk1.7.40)
  
View Code
  
说明: 
  
PrintStream的源码比较简单,请上文的注释进行阅读。若有不明白的地方,建议先看看后面的PrintStream使用示例；待搞清它的作用和用法之后,再来阅读源码。


PrintStream和DataOutputStream异同点
  
相同点: 都是继承与FileOutputStream,用于包装其它输出流。

不同点: 

(01) PrintStream和DataOutputStream 都可以将数据格式化输出；但它们在"输出字符串"时的编码不同。

PrintStream是输出时采用的是用户指定的编码(创建PrintStream时指定的),若没有指定,则采用系统默认的字符编码。而DataOutputStream则采用的是UTF-8。
  
关于UTF-8的字符编码可以参考"字符编码(ASCII,Unicode和UTF-8) 和 大小端"
  
关于DataOutputStream的更多内容,可以参考"java io系列15之 DataOutputStream(数据输出流)的认知、源码和示例"

(02) 它们的写入数据时的异常处理机制不同。

DataOutputStream在通过write()向"输出流"中写入数据时,若产生IOException,会抛出。
  
而PrintStream在通过write()向"输出流"中写入数据时,若产生IOException,则会在write()中进行捕获处理；并设置trouble标记(用于表示产生了异常)为true。用户可以通过checkError()返回trouble值,从而检查输出流中是否产生了异常。

(03) 构造函数不同

DataOutputStream的构造函数只有一个: DataOutputStream(OutputStream out)。即它只支持以输出流out作为"DataOutputStream的输出流"。
  
而PrintStream的构造函数有许多: 和DataOutputStream一样,支持以输出流out作为"PrintStream输出流"的构造函数；还支持以"File对象"或者"String类型的文件名对象"的构造函数。
  
而且,在PrintStream的构造函数中,能"指定字符集"和"是否支持自动flush()操作"。

(04) 目的不同

DataOutputStream的作用是装饰其它的输出流,它和DataInputStream配合使用: 允许应用程序以与机器无关的方式从底层输入流中读写java数据类型。
  
而PrintStream的作用虽然也是装饰其他输出流,但是它的目的不是以与机器无关的方式从底层读写java数据类型；而是为其它输出流提供打印各种数据值表示形式,使其它输出流能方便的通过print(), println()或printf()等输出各种格式的数据。


示例代码
  
关于PrintStream中API的详细用法,参考示例代码(PrintStreamTest.java): 
  
1 import java.io.PrintStream;
  
2 import java.io.File;
  
3 import java.io.FileOutputStream;
  
4 import java.io.IOException;
  
6 /**
  
7 * PrintStream 的示例程序
  
8 *
  
9 * @author skywang
  
10 */
  
11 public class PrintStreamTest {
  
13 public static void main(String[] args) {
  
15 // 下面3个函数的作用都是一样: 都是将字母"abcde"写入到文件"file.txt"中。
  
16 // 任选一个执行即可！
  
17 testPrintStreamConstrutor1() ;
  
18 //testPrintStreamConstrutor2() ;
  
19 //testPrintStreamConstrutor3() ;
  
21 // 测试write(), print(), println(), printf()等接口。
  
22 testPrintStreamAPIS() ;
  
23 }
  
25 /**
  
26 * PrintStream(OutputStream out) 的测试函数
  
27 *
  
28 * 函数的作用,就是将字母"abcde"写入到文件"file.txt"中
  
29 */
  
30 private static void testPrintStreamConstrutor1() {
  
31 // 0x61对应ASCII码的字母'a',0x62对应ASCII码的字母'b', ...
  
32 final byte[] arr={0x61, 0x62, 0x63, 0x64, 0x65 }; // abced
  
33 try {
  
34 // 创建文件"file.txt"的File对象
  
35 File file = new File("file.txt");
  
36 // 创建文件对应FileOutputStream
  
37 PrintStream out = new PrintStream(
  
38 new FileOutputStream(file));
  
39 // 将"字节数组arr"全部写入到输出流中
  
40 out.write(arr);
  
41 // 关闭输出流
  
42 out.close();
  
43 } catch (IOException e) {
  
44 e.printStackTrace();
  
45 }
  
46 }
  
48 /**
  
49 * PrintStream(File file) 的测试函数
  
50 *
  
51 * 函数的作用,就是将字母"abcde"写入到文件"file.txt"中
  
52 */
  
53 private static void testPrintStreamConstrutor2() {
  
54 final byte[] arr={0x61, 0x62, 0x63, 0x64, 0x65 };
  
55 try {
  
56 File file = new File("file.txt");
  
57 PrintStream out = new PrintStream(file);
  
58 out.write(arr);
  
59 out.close();
  
60 } catch (IOException e) {
  
61 e.printStackTrace();
  
62 }
  
63 }
  
65 /**
  
66 * PrintStream(String fileName) 的测试函数
  
67 *
  
68 * 函数的作用,就是将字母"abcde"写入到文件"file.txt"中
  
69 */
  
70 private static void testPrintStreamConstrutor3() {
  
71 final byte[] arr={0x61, 0x62, 0x63, 0x64, 0x65 };
  
72 try {
  
73 PrintStream out = new PrintStream("file.txt");
  
74 out.write(arr);
  
75 out.close();
  
76 } catch (IOException e) {
  
77 e.printStackTrace();
  
78 }
  
79 }
  
81 /**
  
82 * 测试write(), print(), println(), printf()等接口。
  
83 */
  
84 private static void testPrintStreamAPIS() {
  
85 // 0x61对应ASCII码的字母'a',0x62对应ASCII码的字母'b', ...
  
86 final byte[] arr={0x61, 0x62, 0x63, 0x64, 0x65 }; // abced
  
87 try {
  
88 // 创建文件对应FileOutputStream
  
89 PrintStream out = new PrintStream("other.txt");
  
91 // 将字符串"hello PrintStream"+回车符,写入到输出流中
  
92 out.println("hello PrintStream");
  
93 // 将0x41写入到输出流中
  
94 // 0x41对应ASCII码的字母'A',也就是写入字符'A'
  
95 out.write(0x41);
  
96 // 将字符串"65"写入到输出流中。
  
97 // out.print(0x41); 等价于 out.write(String.valueOf(0x41));
  
98 out.print(0x41);
  
99 // 将字符'B'追加到输出流中
  
100 out.append('B');
  
102 // 将"CDE is 5" + 回车 写入到输出流中
  
103 String str = "CDE";
  
104 int num = 5;
  
105 out.printf("%s is %d\n", str, num);
  
107 out.close();
  
108 } catch (IOException e) {
  
109 e.printStackTrace();
  
110 }
  
111 }
  
112 }

运行上面的代码,会在源码所在目录生成两个文件"file.txt"和"other.txt"。
  
file.txt的内容如下: 

abcde
  
other.txt的内容如下: 

hello PrintStream
  
A65BCDE is 5