---
title: Java反编译, jad, jd-gui
author: "-"
date: 2014-04-11T06:46:31+00:00
url: /?p=6518

categories:
  - inbox
tags:
  - reprint
---
## Java反编译, jad, jd-gui
### Jadclipse
JadClipse是Jad的Eclipse插件
### jad
jad是一款使用非常广泛地Java反编译工具，上面这款Jadclipse就是基于jad的反编译插件，JAD 文件包含 MIDlet 套件的标题信息，例如开发应用程序的公司、应用程序名称和大小。

官方网站: http://varaneckas.com/jad/
### JD-GUI
JD-GUI 是一个用 C++ 开发的 Java 反编译工具，由 Pavel Kouznetsov开发，支持Windows、Linux和苹果Mac Os三个平台。而且提供了Eclipse平台下的插件JD-Eclipse。JD-GUI不需要安装，直接点击运行，可以反编译jar,class文件。

官方网站: http://jd.benow.ca/

### jdec
http://jdec.sourceforge.net/

### uuDeJava
http://www.uuware.com/uudejava_cn.htm
### Minjava
### Java Decompiler
http://jd.benow.ca/

工具使用jad(还有joda,jd等工具)


1. 使用jad反编译class文件，jad可以配置到eclipse中当做插件，直接下载jad的eclipse插件jar包，放在eclipse的plugin目录下即可。把下载的jad.exe放在JAVA_HOME的bin下。然后eclipse中点击class文件即可查看到源码。


2. 使用其他工具，FrontEnd Plus集成了jad的java反编译工具，支持多个文件的反编译，也支持各种选项。


矫正反编译代码错误和奇怪代码


1. 异常错误


反编译之后出入类似如下代码: 


DocumentException e;


e;


e.printStackTrace();


break MISSING_BLOCK_LABEL_67;


e;


e.printStackTrace();


break MISSING_BLOCK_LABEL_67;


e;


e.printStackTrace();


break MISSING_BLOCK_LABEL_67;


e;


这种处理方式就是异常处理，反编译之后出现的这种情况，修改的时候使用try catch即可，其实完全可以将这块删除之后，然后eclipse会自动提示需要添加异常处理的模块，自动try catch即可。


2. 语句标号 (goto) 


这种情况常见于条件语句，即转化为if，else语句即可，这种比较容易判断。


i = 0;


goto _L1


_L3:


i++;


_L1:


if(i < 4) goto _L3; else goto _L2


_L2:


g.dispose();


上面的代码实际上就是如下的代码: 


i=0;


if(i < 4){


i++;


}else{


g.dispose();


}


3. jvm代码信息错误


String rand = backStr[random.nextInt(backStr.length)];


this;


sRand;


JVM INSTR new #203 <Class StringBuilder>;


JVM INSTR dup_x1 ;


JVM INSTR swap ;


String.valueOf();


StringBuilder();


rand;


append();


toString();


sRand;


这种错误代码，也是很常见的，比如上面的代码中，rand 是局部设定的变量，而存在一个类变量sRand，上面的代码可以使用如下的代码替换掉错误。


this.sRand += rand;


当然，对这段代码进行分析一下即可看出，分析的时候需要结合下面4中讲解的字符串拼接翻译器代码，从这段混乱的代码中可以看到，有this和sRand，这种可以看出是操作了this的sRand变量，下面的jvm instr是创建了一个stringBuilder的的变量，实际这个变量是保存了this的sRand字符串。最后是append了一个rand变量，然后把这个变量又赋值给了this的sRand。


4. 字符串拼接的代码


(new StringBuilder(String.valueOf(prefix))).append(file).toString();


上面的这种代码，实际代码如下: 


prefix + file


所有字符串拼接都是转为StringBuilder使用append拼接之后然后toString。


5. continue关键字


这种常常会隐含逻辑错误，但是编译并不报错，这种问题最难发现。这种的反编译一般伴随着大段的循环代码，然后反编译之后会将循环代码或者if代码转成goto语句 (参见2) ，然后在某个情况之下不需要继续执行，便使用continue截断代码执行路径。代码出现如下情况。


continue; /* Loop/switch isn't completed */


这样的代码出现的时候，并没有报语法的错误，我遇到这种情况之后，程序运行之后结果出错，最后将程序中的这个反编译问题找了出来，将continue修改成break语句正常了。这样的问题常常会出现在while循环中，可能反编译出来的程序丢失了while循环，变成了if语句，常常是迭代器循环的时候，非常容易出现这种情况。


6. 迭代器循环


迭代器循环反编译之后常出险两种情况，一种容易引起逻辑上的错误，一种没有逻辑和语法上的错误，只不过不是原来代码的写法而已。


iter = datalist.iterator();


goto _L1


if(iter.hasNext()) goto _L3; else goto _L2


上面的代码可以利用类型2来翻译出来，但是这里会有个地方需要修改，那就是if必须换成while，而else中是一些异常处理而已。这里常见的隐含问题在于，在代码片段L3中，常常含有break，continue等跳转语句，一定要分析清楚，不然很容易出现难以排查的逻辑错误，使得反编译出来的代码运行结果不正确。


还原之后的代码如下: 


try {


Iterator iter = datalist.iterator();


while(iter.hasNext()){


}


}catch (Exception e) {


e.printStackTrace();


}


还有一种没有错误的译法如下: 


for(Iterator iterrisk = tRiskLIst.iterator(); iterrisk.hasNext();)


{


}


这种译法没有错误，只不过是看着不习惯而已，原程序程序通常如下: 


Iterator iterrisk = tRiskLIst.iterator();


while(iterrisk.hasNext()){


}


本文永久地址http://blog.sina.com.cn/s/blog_4a2100f801014iwy.html