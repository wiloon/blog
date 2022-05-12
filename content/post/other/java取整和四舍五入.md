---
title: java取整和四舍五入
author: "-"
date: 2012-09-30T07:24:48+00:00
url: /?p=4356
categories:
  - Java
tags:$
  - reprint
---
## java取整和四舍五入
```java
  
Math.round
  
Math.round(-1.1): -1
  
Math.round(-1.5): -1
  
Math.round(-1.6): -2
  
Math.round(0.1): 0
  
Math.round(0.5): 1
  
Math.round(0.6): 1
  
Math.round(1.1): 1
  
Math.round(1.5): 2
  
Math.round(1.6): 2

round 方法，我们通常会说这个方法表示"四舍五入"，但是当参数为负数时，就不太好理解。
  
所以也有以下形式
  
即将原来的数字加上0.5后再向下取整。
  
Math.round(x) = Math.floor(x + 0.5)
  
```

import java.math.BigDecimal;
  
import java.text.DecimalFormat;

public class TestGetInt{

public static void main(String[] args){

double i=2, j=2.1, k=2.5, m=2.9;

System.out.println("舍掉小数取整:Math.floor(2)=" + (int)Math.floor(i));

System.out.println("舍掉小数取整:Math.floor(2.1)=" + (int)Math.floor(j));

System.out.println("舍掉小数取整:Math.floor(2.5)=" + (int)Math.floor(k));

System.out.println("舍掉小数取整:Math.floor(2.9)=" + (int)Math.floor(m));

/* 这段被注释的代码不能正确的实现四舍五入取整

System.out.println("四舍五入取整:Math.rint(2)=" + (int)Math.rint(i));

System.out.println("四舍五入取整:Math.rint(2.1)=" + (int)Math.rint(j));

System.out.println("四舍五入取整:Math.rint(2.5)=" + (int)Math.rint(k));

System.out.println("四舍五入取整:Math.rint(2.9)=" + (int)Math.rint(m));

System.out.println("四舍五入取整:(2)=" + new DecimalFormat("0").format(i));

System.out.println("四舍五入取整:(2.1)=" + new DecimalFormat("0").format(i));

System.out.println("四舍五入取整:(2.5)=" + new DecimalFormat("0").format(i));

System.out.println("四舍五入取整:(2.9)=" + new DecimalFormat("0").format(i));

*/

System.out.println("四舍五入取整:(2)=" + new BigDecimal("2").setScale(0, BigDecimal.ROUND_HALF_UP));

System.out.println("四舍五入取整:(2.1)=" + new BigDecimal("2.1").setScale(0, BigDecimal.ROUND_HALF_UP));

System.out.println("四舍五入取整:(2.5)=" + new BigDecimal("2.5").setScale(0, BigDecimal.ROUND_HALF_UP));

System.out.println("四舍五入取整:(2.9)=" + new BigDecimal("2.9").setScale(0, BigDecimal.ROUND_HALF_UP));

System.out.println("凑整:Math.ceil(2)=" + (int)Math.ceil(i));

System.out.println("凑整:Math.ceil(2.1)=" + (int)Math.ceil(j));

System.out.println("凑整:Math.ceil(2.5)=" + (int)Math.ceil(k));

System.out.println("凑整:Math.ceil(2.9)=" + (int)Math.ceil(m));

System.out.println("舍掉小数取整:Math.floor(-2)=" + (int)Math.floor(-i));

System.out.println("舍掉小数取整:Math.floor(-2.1)=" + (int)Math.floor(-j));

System.out.println("舍掉小数取整:Math.floor(-2.5)=" + (int)Math.floor(-k));

System.out.println("舍掉小数取整:Math.floor(-2.9)=" + (int)Math.floor(-m));

System.out.println("四舍五入取整:(-2)=" + new BigDecimal("-2").setScale(0, BigDecimal.ROUND_HALF_UP));

System.out.println("四舍五入取整:(-2.1)=" + new BigDecimal("-2.1").setScale(0, BigDecimal.ROUND_HALF_UP));

System.out.println("四舍五入取整:(-2.5)=" + new BigDecimal("-2.5").setScale(0, BigDecimal.ROUND_HALF_UP));

System.out.println("四舍五入取整:(-2.9)=" + new BigDecimal("-2.9").setScale(0, BigDecimal.ROUND_HALF_UP));

System.out.println("凑整:Math.ceil(-2)=" + (int)Math.ceil(-i));

System.out.println("凑整:Math.ceil(-2.1)=" + (int)Math.ceil(-j));

System.out.println("凑整:Math.ceil(-2.5)=" + (int)Math.ceil(-k));

System.out.println("凑整:Math.ceil(-2.9)=" + (int)Math.ceil(-m));

}

}

//_____________________________

舍掉小?取整:Math.floor(2)=2

舍掉小?取整:Math.floor(2.1)=2

舍掉小?取整:Math.floor(2.5)=2

舍掉小?取整:Math.floor(2.9)=2

四舍五入取整:(2)=2

四舍五入取整:(2.1)=2

四舍五入取整:(2.5)=3

四舍五入取整:(2.9)=3

?整:Math.ceil(2)=2

?整:Math.ceil(2.1)=3

?整:Math.ceil(2.5)=3

?整:Math.ceil(2.9)=3

舍掉小?取整:Math.floor(-2)=-2

舍掉小?取整:Math.floor(-2.1)=-3

舍掉小?取整:Math.floor(-2.5)=-3

舍掉小?取整:Math.floor(-2.9)=-3

四舍五入取整:(-2)=-2

四舍五入取整:(-2.1)=-2

四舍五入取整:(-2.5)=-3

四舍五入取整:(-2.9)=-3

?整:Math.ceil(-2)=-2

?整:Math.ceil(-2.1)=-2

?整:Math.ceil(-2.5)=-2

?整:Math.ceil(-2.9)=-2

===================================================

BigDecimal b = new BigDecimal(9.655 );

//double f1 = b.setScale(2, BigDecimal.ROUND_HALF_UP).doubleValue();

double f1 = b.setScale(2, BigDecimal.ROUND_HALF_UP).doubleValue();

System.out.println("f1=" + f1);//f1=9.65

BigDecimal mData = new BigDecimal("9.655").setScale(2, BigDecimal.ROUND_HALF_UP);

System.out.println("mData=" + mData);//mData=9.66

public BigDecimal(double val)

将 double 转换为 BigDecimal，后者是 double 的二进制浮点值准确的十进制表示形式。返回的 BigDecimal 的标度是使 (10scale × val) 为整数的最小值。

注: 

此构造方法的结果有一定的不可预知性。有人可能认为在 Java 中写入 new BigDecimal(0.1) 所创建的 BigDecimal 正好等于 0.1 (非标度值 1，其标度为 1) ，但是它实际上等于 0.1000000000000000055511151231257827021181583404541015625。这是因为 0.1 无法准确地表示为 double (或者说对于该情况，不能表示为任何有限长度的二进制小数) 。这样，传入 到构造方法的值不会正好等于 0.1 (虽然表面上等于该值) 。

另一方面，String 构造方法是完全可预知的: 写入 new BigDecimal("0.1") 将创建一个 BigDecimal，它正好 等于预期的 0.1。因此，比较而言，通常建议优先使用 String 构造方法。

当 double 必须用作 BigDecimal 的源时，请注意，此构造方法提供了一个准确转换；它不提供与以下操作相同的结果: 先使用 Double.toString(double) 方法，然后使用 BigDecimal(String) 构造方法，将 double 转换为 String。要获取该结果，请使用 static valueOf(double) 方法。