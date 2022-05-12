---
title: JAVA 随机数
author: "-"
date: 2012-05-25T07:56:45+00:00
url: /?p=3207
categories:
  - Java
tags:
  - reprint
---
## JAVA 随机数

在Java中，随机数的概念从广义上将，有三种。
  
1. 通过System.currentTimeMillis()来获取一个当前时间毫秒数的long型数字。
  
2. 通过Math.random()返回一个0到1之间的double值。
  
3. 通过Random类来产生一个随机数，这个是专业的Random工具类，功能强大。

int nextInt()
  
返回下一个伪随机数，它是此随机数生成器的序列中均匀分布的 int 值。
  
int nextInt(int n)
  
返回一个伪随机数，它是从此随机数生成器的序列中取出的、在 0 (包括) 和指定值 (不包括) 之间均匀分布的 int值。
  
在Java中我们可以使用java.util.Random类来产生一个随机数发生器。它有两种形式的构造函数，分别是Random()和Random(long seed)。Random()使用当前时间即System.currentTimeMillis()作为发生器的种子，Random(long seed)使用指定的seed作为发生器的种子。

随机数发生器(Random)对象产生以后，通过调用不同的method: nextInt()、nextLong()、nextFloat()、nextDouble()等获得不同类型随机数。

1>生成随机数

```java
   
Random random = new Random();
   
Random random = new Random(100);//指定种子数100

```

random调用不同的方法，获得随机数。
  
如果2个Random对象使用相同的种子 (比如都是100) ，并且以相同的顺序调用相同的函数，那它们返回值完全相同。如下面代码中两个Random对象的输出完全相同

```java
   
import java.util.*;
   
class TestRandom {
   
public static void main(String[] args) {
   
Random random1 = new Random(100);
   
System.out.println(random1.nextInt());
   
System.out.println(random1.nextFloat());
   
System.out.println(random1.nextBoolean());
   
Random random2 = new Random(100);
   
System.out.println(random2.nextInt());
   
System.out.println(random2.nextFloat());
   
System.out.println(random2.nextBoolean());
   
}
   
}

```

2>指定范围内的随机数
  
随机数控制在某个范围内,使用模数运算符%

```java
   
import java.util.*;
   
class TestRandom {
   
public static void main(String[] args) {
   
Random random = new Random();
   
for(int i = 0; i < 10;i++) {
   
System.out.println(Math.abs(random.nextInt())%10);
   
}
   
}
   
}

```

获得的随机数有正有负的，用Math.abs使获取数据范围为非负数

3>获取指定范围内的不重复随机数

```java
   
import java.util.*;
   
class TestRandom {
   
public static void main(String[] args) {
   
int[] intRet = new int[6];
   
int intRd = 0; //存放随机数
   
int count = 0; //记录生成的随机数个数
   
int flag = 0; //是否已经生成过标志
   
while(count<6){
   
Random rdm = new Random(System.currentTimeMillis());
   
intRd = Math.abs(rdm.nextInt())%32+1;
   
for(int i=0;i<count;i++){
   
if(intRet[i]==intRd){
   
flag = 1;
   
break;
   
}else{
   
flag = 0;
   
}
   
}
   
if(flag==0){
   
intRet[count] = intRd;
   
count++;
   
}
   
}
   
for(int t=0;t<6;t++){
   
System.out.println(t+"->"+intRet[t]);
   
}
   
}
   
}

```

Java随机数类Random介绍
  
Java实用工具类库中的类java.util.Random提供了产生各种类型随机数的方法。它可以产生int、long、float、double以 及Goussian等类型的随机数。这也是它与java.lang.Math中的方法Random()最大的不同之处，后者只产生double型的随机 数。
  
类Random中的方法十分简单，它只有两个构造方法和六个普通方法。
  
构造方法: 
  
(1)public Random()
  
(2)public Random(long seed)
  
Java产生随机数需要有一个基值seed，在第一种方法中基值缺省，则将系统时间作为seed。
  
普通方法: 
  
(1)public synonronized void setSeed(long seed)
  
该方法是设定基值seed。
  
(2)public int nextInt()
  
该方法是产生一个整型随机数。
  
(3)public long nextLong()
  
该方法是产生一个long型随机数。
  
(4)public float nextFloat()
  
该方法是产生一个Float型随机数。
  
(5)public double nextDouble()
  
该方法是产生一个Double型随机数。
  
(6)public synchronized double nextGoussian()
  
该方法是产生一个double型的Goussian随机数。
  
例2 RandomApp.java。

```java
   
//import java.lang.*;
   
import java.util.Random;

public class RandomApp{
   
public static void main(String args[]){
   
Random ran1=new Random();
   
Random ran2=new Random(12345);
   
//创建了两个类Random的对象。
   
System.out.println("The 1st set of random numbers:");
   
System.out.println(" Integer:"+ran1.nextInt());
   
System.out.println(" Long:"+ran1.nextLong());
   
System.out.println(" Float:"+ran1.nextFloat());
   
System.out.println(" Double:"+ran1.nextDouble());
   
System.out.println(" Gaussian:"+ran1.nextGaussian());
   
//产生各种类型的随机数
   
System.out.print("The 2nd set of random numbers:");
   
for(int i=0;i<5;i++){
   
System.out.println(ran2.nextInt()+" ");
   
if(i==2) System.out.println();
   
//产生同种类型的不同的随机数。
   
System.out.println();
   
}
   
}
   
}

Random random=new Random();
   
random.nextInt();

```

也可以有nextFloat等等,各种基本类型都有

Math.random也可以
  
比如说你想要0-10之间的随机数
  
你可以这样写
  
(int)(Math.random()*10);
  
JAVA产生指定范围的随机数》

《JAVA产生指定范围的随机数》
  
产生机制: 
  
产生Min-Max之间的数字
  
实现原理: 
  
Math.round(Math.random()*(Max-Min)+Min)

long Temp; //不能设定为int,必须设定为long
  
//产生1000到9999的随机数
  
Temp=Math.round(Math.random()*8999+1000);


http://blog.csdn.net/herrapfel/article/details/1885016

<http://lavasoft.blog.51cto.com/62575/113758/>