---
title: Java Scanner
author: "-"
date: 2017-03-30T05:12:14+00:00
url: /?p=9984
categories:
  - Inbox
tags:
  - reprint
---
## Java Scanner
<http://blog.csdn.net/carolzhang8406/article/details/6726589>
  
一、扫描控制台输入

这个例子是常常会用到,但是如果没有Scanner,你写写就知道多难受了。
  
当通过new Scanner(System.in)创建一个Scanner,控制台会一直等待输入,直到敲回车键结束,把所输入的内容传给Scanner,作为扫描对象。如果要获取输入的内容,则只需要调用Scanner的nextLine()方法即可。

/**
  
* 扫描控制台输入
  
*
  
* @author leizhimin 2009-7-24 11:24:47
  
*/
  
public class TestScanner {
  
public static void main(String[] args) {
  
Scanner s = new Scanner(System.in);
  
System.out.println("请输入字符串: ");
  
while (true) {
  
String line = s.nextLine();
  
if (line.equals("exit")) break;
  
System.out.println(">>>" + line);
  
}
  
}
  
}

请输入字符串:
  
>>>234
  
wer
  
>>>wer
  
bye
  
>>>bye
  
exit

Process finished with exit code 0

先写这里吧,有空再继续完善。

二、如果说Scanner使用简便,不如说Scanner的构造器支持多种方式,构建Scanner的对象很方便。

可以从字符串 (Readable) 、输入流、文件等等来直接构建Scanner对象,有了Scanner了,就可以逐段 (根据正则分隔式) 来扫描整个文本,并对扫描后的结果做想要的处理。

三、Scanner默认使用空格作为分割符来分隔文本,但允许你指定新的分隔符

使用默认的空格分隔符:
  
public static void main(String[] args) throws FileNotFoundException {
  
Scanner s = new Scanner("123 asdf sd 45 789 sdf asdfl,sdf.sdfl,asdf    ......asdfkl    las");
  
//                s.useDelimiter(" |,|\\.");
  
while (s.hasNext()) {
  
System.out.println(s.next());
  
}
  
}

asdf
  
sd
  
sdf
  
asdfl,sdf.sdfl,asdf
  
......asdfkl
  
las

Process finished with exit code 0

将注释行去掉,使用空格或逗号或点号作为分隔符,输出结果如下:
  
asdf
  
sd
  
sdf
  
asdfl
  
sdf
  
sdfl
  
asdf

asdfkl

las

Process finished with exit code 0

Scanning with regular expressions
  
In addition to scanning for predefined primitive types, you can also scan for your own user-defined patterns, which is helpful when scanning more complex data. This example scans threat data from a log like your firewall might produce:
  
//: strings/ThreatAnalyzer.java
  
import java.util.regex.*;
  
import java.util.*;
  
public class ThreatAnalyzer {
  
static String threatData =
  
"58.27.82.161@02/10/2005\n" +
  
"204.45.234.40@02/11/2005\n" +
  
"58.27.82.161@02/11/2005\n" +
  
"58.27.82.161@02/12/2005\n" +
  
"58.27.82.161@02/12/2005\n" +
  
"[Next log section with different data format]";
  
public static void main(String[] args) {
  
Scanner scanner = new Scanner(threatData);
  
String pattern = "(\\d+[.]\\d+[.]\\d+[.]\\d+)@" +
  
"(\\d{2}/\\d{2}/\\d{4})";
  
while(scanner.hasNext(pattern)) {
  
scanner.next(pattern);
  
MatchResult match = scanner.match();
  
String ip = match.group(1);
  
String date = match.group(2);
  
System.out.format("Threat on %s from %s\n", date,ip);
  
}
  
}
  
} /* Output:
  
Threat on 02/10/2005 from 58.27.82.161
  
Threat on 02/11/2005 from 204.45.234.40
  
Threat on 02/11/2005 from 58.27.82.161
  
Threat on 02/12/2005 from 58.27.82.161
  
Threat on 02/12/2005 from 58.27.82.161
  
*///:~
