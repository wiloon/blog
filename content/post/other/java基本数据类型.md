---
title: java 基本数据类型， primitive type
author: "-"
date: 2012-09-19T08:44:40+00:00
url: java/primitive
categories:
  - Java
tags:$
  - reprint
---
## java 基本数据类型， primitive type
Java语言提供了八种基本类型: 六种数字类型 (四个整数型，两个浮点型) ，一种字符类型，一种布尔型。
  
1. 整数: 包括 int, short, byte, long
2. 浮点型: float, double
3. 字符: char
4. 布尔: boolean

java.lang.String 类是final类型的，因此不可以继承这个类、不能修改这个类。为了提高效率节省空间，应该用StringBuffer类

 (1个字节是8个bit)  
整数型: byte (1字节) 、short (2字节) 、int (4字节) 、long (8字节)  浮点型: float (4字节) 、double (8字节)  布尔型: boolean (1字节)  字符型: char (2字节) 

### boolean: 

boolean数据类型表示一位的信息；
  
只有两个取值: true和false；
  
这种类型只作为一种标志来记录true/false情况；
  
默认值是false；
  
例子: boolean one = true。

### byte
8位有符号整数
  
byte是一个字节保存的，有8个位.
  
byte取值的范围: -128—127
  
8位的第一个位是符号位,
  
0000 0001代表的是数字1
  
1000 0000代表的就是-1
  
正数最大为0111 1111，是数字127
  
负数最大为1111 1111，是数字-128
  
在java中采用的是补码的形式.

### short
short数据类型是16位、有符号的以二进制补码表示的整数
  
最小值是-32768 (-2^15) ；
  
最大值是32767 (2^15 - 1) ；
  
Short数据类型也可以像byte那样节省空间。一个short变量是int型变量所占空间的二分之一；
  
默认值是0；
  
例子: short s = 1000，short r = -20000。

### char
16位Unicode字符
  
char类型是一个单一的16位Unicode字符；
  
最小值是'\u0000' (即为0) ；
  
最大值是'\uffff' (即为65,535) ；
  
char数据类型可以储存任何字符；
  
例子: char letter = 'A'。

### int
32位有符号整数
  
int数据类型是32位、有符号的以二进制补码表示的整数；
  
最小值是-2,147,483,648 (-2^31) ；
  
最大值是2,147,485,647 (2^31 – 1) ；
  
一般地整型变量默认为int类型；
  
默认值是0；
  
例子: int a = 100000, int b = -200000。

### float
节数为4  
32bit, 32位浮点数(floating-point)
  
数值范围为-3.4E38~3.4E38 (7个有效位) 

float数据类型是单精度、32位、符合IEEE 754标准的浮点数；
  
float在储存大型浮点数组的时候可节省内存空间；
  
默认值是0.0f；
  
浮点数不能用来表示精确的值，如货币；
  
例子: float f1 = 234.5f。

不声明时，默认为double，要声明float该写为
   
    float PI=3.14f;
    或者float PI =  (float) 3.14;

### long
64位有符号整数
  
long数据类型是64位、有符号的以二进制补码表示的整数；
  
最小值是-9,223,372,036,854,775,808 (-2^63) ；
  
最大值是9,223,372,036,854,775,807 (2^63 -1) ；
  
这种类型主要使用在需要比较大整数的系统上；
  
默认值是0L；
  
例子:  long a = 100000L，int b = -200000L。

### double
节数为8  
64位浮点数
  
double数据类型是双精度、64位、符合IEEE 754标准的浮点数；  
64bit数值范围-1.7E308~1.7E308 (15个有效位)   
双精度实型  

浮点数的默认类型为double类型；
  
double类型同样不能表示精确的值，如货币；
  
默认值是0.0f；

例子: double d1 = 123.4。
  
数值范围-1.7E308~1.7E308 (15个有效位) 
  
String是char[]的封装类型
  
char和string是有编码的

Java 遵循 unicode 4.0 标准，内部的 character 以 utf-16 作为 encoding。unicode 4.0 标准包含从 U+0000-U+FFFF 的基本多语言平面和 U+10000-U+10FFFF 的扩展平面的文字，这是 code point。Java 的 char 类型是 16 bit ，单个 char 只支持基本平面内的文字，扩展平面的文字由一对 char 表示。

String.getBytes() 按照指定的 encoding 返回字符串，一般中文系统的默认编码是 utf-8 (linux, mac) 或者 gbk/gb18030 (windows)。只要是基本平面内的文字，utf-8码的中文都是3字节的，而 gbk/gbk18030 是2字节的

都是浮点型但是表示范围是不一样的，转换的时候当然会提示精度损失，虽然这个数字在两个类型中都是不溢出的。

---

http://blog.csdn.net/yulei_qq/article/details/8992664