---
title: BigDecimal
author: "-"
date: 2016-02-29T01:10:18+00:00
url: /?p=8751
categories:
  - Inbox
tags:
  - reprint
---
## BigDecimal

Java在java.math包中提供的API类BigDecimal,用来对超过16位有效位的数进行精确的运算。双精度浮点型变量double可以处理16位有效数。在实际应用中,需要对更大或者更小的数进行运算和处理。float和double只能用来做科学计算或者是工程计算,在商业计算中要用java.math.BigDecimal。BigDecimal所创建的是对象,我们不能使用传统的+、-、*、/等算术运算符直接对其对象进行数学运算,而必须调用其相对应的方法。方法中的参数也必须是BigDecimal的对象。构造器是类的特殊方法,专门用来创建对象,特别是带有参数的对象。

二、构造器描述
  
BigDecimal(int) 创建一个具有参数所指定整数值的对象。
  
BigDecimal(double) 创建一个具有参数所指定双精度值的对象。
  
BigDecimal(long) 创建一个具有参数所指定长整数值的对象。
  
BigDecimal(String) 创建一个具有参数所指定以字符串表示的数值的对象。

三、方法描述
  
add(BigDecimal) BigDecimal对象中的值相加,然后返回这个对象。
  
subtract(BigDecimal) BigDecimal对象中的值相减,然后返回这个对象。
  
multiply(BigDecimal) BigDecimal对象中的值相乘,然后返回这个对象。
  
divide(BigDecimal) BigDecimal对象中的值相除,然后返回这个对象。
  
toString() 将BigDecimal对象的数值转换成字符串。
  
doubleValue() 将BigDecimal对象中的值以双精度数返回。
  
floatValue() 将BigDecimal对象中的值以单精度数返回。
  
longValue() 将BigDecimal对象中的值以长整数返回。
  
intValue() 将BigDecimal对象中的值以整数返回。

四、格式化
  
由于NumberFormat类的format()方法可以使用BigDecimal对象作为其参数,可以利用BigDecimal对超出16位有效数字的货币值,百分值,以及一般数值进行格式化控制。

以利用BigDecimal对货币和百分比格式化为例。首先,创建BigDecimal对象,进行BigDecimal的算术运算后,分别建立对货币和百分比格式化的引用,最后利用BigDecimal对象作为format()方法的参数,输出其格式化的货币值和百分比。
  
public static void main(String[] args) {
  
NumberFormat currency = NumberFormat.getCurrencyInstance(); //建立货币格式化引用
  
NumberFormat percent = NumberFormat.getPercentInstance(); //建立百分比格式化引用
  
percent.setMaximumFractionDigits(3); //百分比小数点最多3位

BigDecimal loanAmount = new BigDecimal("15000.48"); //贷款金额
  
BigDecimal interestRate = new BigDecimal("0.008"); //利率
  
BigDecimal interest = loanAmount.multiply(interestRate); //相乘

System.out.println("贷款金额:\t" + currency.format(loanAmount));
  
System.out.println("利率:\t" + percent.format(interestRate));
  
System.out.println("利息:\t" + currency.format(interest));
  
}

运行结果如下:

贷款金额: ￥15,000.48
  
利率: 0.8%
  
利息: ￥120.00
  
五、BigDecimal比较
  
BigDecimal是通过使用compareTo(BigDecimal)来比较的,具体比较情况如下:
  
public static void main(String[] args) {
  
BigDecimal a = new BigDecimal("1");
  
BigDecimal b = new BigDecimal("2");
  
BigDecimal c = new BigDecimal("1");
  
int result1 = a.compareTo(b);
  
int result2 = a.compareTo(c);
  
int result3 = b.compareTo(a);
  
System.out.println(result1);
  
System.out.println(result2);
  
System.out.println(result3);

}

打印结果是: -1、0、1,即左边比右边数大,返回1,相等返回0,比右边小返回-1。
  
注意不能使用equals方法来比较大小。

使用BigDecimal的坏处是性能比double和float差,在处理庞大,复杂的运算时尤为明显,因根据实际需求决定使用哪种类型。

int r=big_decimal.compareTo(BigDecimal.Zero); //和0,Zero比较
  
if(r==0) //等于
  
if(r==1) //大于
  
if(r==-1) //小于
  
或者
  
if(big_decimal.equals(BigDecimal.Zero)) //是否等于0

[https://zhidao.baidu.com/question/296052164.html](https://zhidao.baidu.com/question/296052164.html)
  
[http://www.cnblogs.com/linjiqin/p/3413894.html](http://www.cnblogs.com/linjiqin/p/3413894.html)
