---
title: 'java  float,double,decimal'
author: "-"
date: 2011-07-03T12:17:33+00:00
url: /?p=321
categories:
  - Java

tags:
  - reprint
---
## 'java  float,double,decimal'

decimal:数字型，128bit，不存在精度损失，常用于银行帐目计算。 (28个有效位) 

float f = 345.98756f;//结果显示为345.9876，只显示7个有效位，对最后一位数四舍五入。

double d=345.975423578631442d;//结果显示为345.975423578631，只显示15个有效位，对最后一位四舍五入。

注: float和double的相乘操作，数字溢出不会报错，会有精度的损失。

decimal dd=345.545454879.....//可以支持28位，对最后一位四舍五入。

注: 当对decimal类型进行操作时，数值会因溢出而报错。

由于对float或double 的使用不当，可能会出现精度丢失的问题。问题大概情况可以通过如下代码理解:

      public class FloatDoubleTest {
      public static void main(String[] args) {
      float f = 20014999;
      double d = f;
      double d2 = 20014999;
      System.out.println("f=" + f);
      System.out.println("d=" + d);
      System.out.println("d2=" + d2);
      }
      }


得到的结果如下: 

f=2.0015E7

d=2.0015E7

d2=2.0014999E7

从输出结果可以看出double 可以正确的表示20014999 ，而float 没有办法表示20014999 ，得到的只是一个近似值。这样的结果很让人讶异。20014999 这么小的数字在float下没办法表示。于是带着这个问 题，做了一次关于float和double学习，做个简单分享，希望有助于大家对java 浮 点数的理解。

**关于** **java** **的** **float** **和** **double**

Java 语言支持两种基本的浮点类型:  float 和 double 。java 的浮点类型都依据 IEEE 754 标准。IEEE 754 定义了32 位和 64 位双精度两种浮点二进制小数标准。

IEEE 754 用科学记数法以底数为 2 的小数来表示浮点数。32 位浮点数用 1 位表示数字的符号，用 8 位来表示指数，用 23 位来表示尾数，即小数部分。作为有符号整数的指数可以有正负之分。小数部分用二进制 (底数 2) 小数来表示。对于64 位双精度浮点数，用 1 位表示数字的符号，用 11 位表示指数，52 位表示尾数。如下两个图来表示: 

float(32位):

<img src="http://hi.csdn.net/attachment/201002/27/186734_1267278529L3Cf.jpg" alt="float" width="429" height="57" />

double(64位):

<img src="http://hi.csdn.net/attachment/201002/27/186734_1267278529IBy1.jpg" alt="double" width="576" height="57" />

都是分为三个部分: 

(1) 一 个单独的符号位s 直接编码符号s 。

(2)k 位 的幂指数E ，**移 码表示** 。

(3)n 位 的小数，**原码表示** 。

**那么 20014999 为什么用 float 没有办法正确表示？**

结合float和double的表示方法，通过分析 20014999 的二进制表示就可以知道答案了。

以下程序可以得出 20014999 在 double 和 float 下的二进制表示方式。

  
    
      public class FloatDoubleTest3 {
    
    
      public static void main(String[] args) {
    
    
      double d = 8;
    
    
      long l = Double.doubleToLongBits(d);
    
    
      System.out.println(Long.toBinaryString(l));
    
    
      float f = 8;
    
    
      int i = Float.floatToIntBits(f);
    
    
      System.out.println(Integer.toBinaryString(i));
    
    
      }
    
    
      }
    
  


输出结果如下: 

Double:100000101110011000101100111100101110000000000000000000000000000

Float:1001011100110001011001111001100

对于输出结果分析如下。对于都不 double 的二进制左边补上符号位 0 刚好可以得到 64 位的二进制数。根据double的表 示法，分为符号数、幂指数和尾数三个部分如下: 

0 10000010111 0011000101100111100101110000000000000000000000000000

对于 float 左边补上符 号位 0 刚好可以得到 32 位的二进制数。 根据float的表示法， 也分为 符号数、幂指数和尾数三个部分如下 : 

0 10010111 00110001011001111001100

绿色部分是符号位，红色部分是幂指数，蓝色部分是尾数。

对比可以得出:**符号位都是** **0 ，幂指数为移码表示,两者刚好也相等。唯一不同的是尾数。**

在 double 的尾数 为:  **001100010110011110010111** 0000000000000000000000000000 ，省略后面的零，至少需要24位才能正确表示 。

而在 float 下面尾数 为:  00110001011001111001100 ，共 23 位。

为什么会这样？原因很明显，因为 float尾数 最多只能表示 23 位，所以 24 位的 001100010110011110010111 在 float 下面经过四舍五入变成了 23 位的 00110001011001111001100 。所以 20014999 在 float 下面变成了 20015000 。
  
也就是说 20014999 虽然是在float的表示范围之内，但 在 IEEE 754 的 float 表示法精度长度没有办法表示出 20014999 ，而只能通过四舍五入得到一个近似值。


**总结: **

**浮点运算很少是精确的，只要是超过精度能表示的范围就会产生误差。往往产生误差不是 因为数的大小，而是因为数的精度。因此，产生的结果接近但不等于想要的结果。尤其在使用 float 和 double 作精确运 算的时候要特别小心。
  
可以考虑采用一些替代方案来实现。如通过 String 结合 BigDecimal 或 者通过使用 long 类型来转换。**

<http://blog.csdn.net/abing37/article/details/5332798>

http://blog.csdn.net/u014232091/article/details/23792649