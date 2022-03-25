---
title: java math
author: "-"
date: 2012-05-29T08:30:47+00:00
url: /?p=3289
categories:
  - Java

tags:
  - reprint
---
## java math
```java
// 取整 (/)  求余 (%) 
public class MathX {
    public static void main(String[] args) {
        System.out.println(5 / 3);
        System.out.println(5 / 3.0);
        System.out.println(5 % 3);
    }
}

//1
//1.6666666666666667
//2
```

### 幂指数值的运算

Math.pow(double a,double b)，返回的结果是a的b次方。

### 求整数的位数

```java
private static int getNumLenght(long num){
        num = num>0?num:-num;       
        if (num==0) {
            return 1;
        }
        return (int) Math.log10(num)+1;
    }

```

3075436Math.ceil(x):比x大的最小值。
  
Math.round(x): 四舍五入。
  
Math.floor(x):比x小的最大值。

java保留两位小数问题: 

方式一: 

四舍五入
  
double f = 111231.5585;
  
BigDecimal b = new BigDecimal(f);
  
double f1 = b.setScale(2, BigDecimal.ROUND_HALF_UP).doubleValue();
  
保留两位小数
  
—————————————————————

方式二: 

java.text.DecimalFormat df =new java.text.DecimalFormat("#.00");
  
df.format(你要格式化的数字);

例: new java.text.DecimalFormat("#.00").format(3.1415926)

#.00 表示两位小数 #.0000四位小数 以此类推…

方式三: 

double d = 3.1415926;

String result = String .format("%.2f");

%.2f %. 表示 小数点前任意位数 2 表示两位小数 格式后的结果为f 表示浮点型

方式四: 

NumberFormat ddf1=NumberFormat.getNumberInstance() ;

void setMaximumFractionDigits(int digits)
  
digits 显示的数字位数
  
为格式化对象设定小数点后的显示的最多位,显示的最后位是舍入的

import java.text.* ;
  
import java.math.* ;
  
class TT
  
{
  
public static void main(String args[])
  
{ double x=23.5455;
  
NumberFormat ddf1=NumberFormat.getNumberInstance() ;

ddf1.setMaximumFractionDigits(2);
  
String s= ddf1.format(x) ;
  
System.out.print(s);
  
}
  
}

———————————————————————————————————

有一篇: 

 (1) 、浮点数精确计算

胜利油田三流合一项目中一直存在一个问题，就是每次报表统计的物资金额和实际的金额要差那么几分钱，和实际金额不一致，让客户觉得总是不那么舒服，原因是因为我们使用java的浮点类型double来定义物资金额，并且在报表统计中我们经常要进行一些运算，但Java中浮点数 (double、float) 的计算是非精确计算，请看下面一个例子: 

System.out.println(0.05 + 0.01);

System.out.println(1.0 – 0.42);

System.out.println(4.015 * 100);

System.out.println(123.3 / 100);

你的期望输出是什么？可实际的输出确实这样的: 

0.060000000000000005

0.5800000000000001

401.49999999999994

1.2329999999999999

这个问题就非常严重了，如果你有123.3元要购买商品，而计算机却认为你只有123.29999999999999元，钱不够，计算机拒绝交易。

 (2) 、四舍五入

是否可以四舍五入呢？当然可以，习惯上我们本能就会这样考虑，但四舍五入意味着误差，商业运算中可能意味着错误，同时Java中也没有提供保留指定位数的四舍五入方法，只提供了一个Math.round(double d)和Math.round(float f)的方法，分别返回长整型和整型值。round方法不能设置保留几位小数，我们只能象这样 (保留两位) : 

public double round(double value){

return Math.round( value * 100 ) / 100.0;

}

但非常不幸的是，上面的代码并不能正常工作，给这个方法传入4.015它将返回4.01而不是4.02，如我们在上面看到的

4.015 * 100 = 401.49999999999994

因此如果我们要做到精确的四舍五入，这种方法不能满足我们的要求。

还有一种方式是使用java.text.DecimalFormat，但也存在问题，format采用的舍入模式是ROUND_HALF_DOWN (舍入模式在下面有介绍) ，比如说4.025保留两位小数会是4.02，因为.025距离"nearest neighbor" (.02和.03) 长度是相等，向下舍入就是.02，如果是4.0251那么保留两位小数就是4.03。

System.out.println(new java.text.DecimalFormat("0.00").format(4.025));

System.out.println(new java.text.DecimalFormat("0.00").format(4.0251));

输出是

4.02

4.03

 (3) 、浮点数输出 (科学记数法) 

Java浮点型数值在大于9999999.0就自动转化为科学记数法来表示，我们看下面的例子: 

System.out.println(999999999.04);

System.out.println(99999999.04);

System.out.println(10000000.01);

System.out.println(9999999.04);

输出的结果如下: 

9.9999999904E8

9.999999904E7

1.000000001E7

9999999.04

但有时我们可能不需要科学记数法的表示方法，需要转换为字符串，还不能直接用toString()等方法转换，很烦琐。

BigDecimal介绍

BigDecimal是Java提供的一个不变的、任意精度的有符号十进制数对象。它提供了四个构造器，有两个是用BigInteger构造，在这里我们不关心，我们重点看用double和String构造的两个构造器 (有关BigInteger详细介绍请查阅j2se API文档) 。

BigDecimal(double val)
  
Translates a double into a BigDecimal.

BigDecimal(String val)
  
Translates the String representation of a BigDecimal into a BigDecimal.

BigDecimal(double)是把一个double类型十进制数构造为一个BigDecimal对象实例。

BigDecimal(String)是把一个以String表示的BigDecimal对象构造为BigDecimal对象实例。

习惯上，对于浮点数我们都会定义为double或float，但BigDecimal API文档中对于BigDecimal(double)有这么一段话: 

Note: the results of this constructor can be somewhat unpredictable. One might assume that new BigDecimal(.1) is exactly equal to .1, but it is actually equal to .10000000000000000555111512312578 27021181583404541015625. This is so because .1 cannot be represented exactly as a double (or, for that matter, as a binary fraction of any finite length). Thus, the long value that is being passed in to the constructor is not exactly equal to .1, appearances notwithstanding.

The (String) constructor, on the other hand, is perfectly predictable: new BigDecimal(".1") is exactly equal to .1, as one would expect. Therefore, it is generally recommended that the (String) constructor be used in preference to this one

下面对这段话做简单解释: 

注意: 这个构造器的结果可能会有不可预知的结果。有人可能设想new BigDecimal(.1)等于.1是正确的，但它实际上是等于.1000000000000000055511151231257827021181583404541015625，这就是为什么.1不能用一个double精确表示的原因，因此，这个被放进构造器中的长值并不精确的等于.1，尽管外观看起来是相等的。

然而 (String) 构造器，则完全可预知的，new BigDecimal(".1")如同期望的那样精确的等于.1，因此， (String) 构造器是被优先推荐使用的。

看下面的结果: 

System.out.println(new BigDecimal(123456789.02).toString());

System.out.println(new BigDecimal("123456789.02").toString());

输出为: 

123456789.01999999582767486572265625

123456789.02

现在我们知道，如果需要精确计算，非要用String来够造BigDecimal不可！

实现方案

现在我们已经知道怎么解决这个问题了，原则上是使用BigDecimal (String) 构造器，我们建议，在商业应用开发中，涉及金额等浮点数计算的数据，全部定义为String，数据库中可定义为字符型字段，在需要使用这些数据进行运算的时候，使用BigDecimal (String) 构造BigDecimal对象进行运算，保证数据的精确计算。同时避免了科学记数法的出现。如果科学记数表示法在应用中不是一种负担的话，可以考虑定义为浮点类型。

这里我们提供了一个工具类，定义浮点数的加、减、乘、除和四舍五入等运算方法。以供参考。

源文件MathExtend.java: 

import java.math.BigDecimal;

public class MathExtend

{

//默认除法运算精度

private static final int DEFAULT_DIV_SCALE = 10;

/**

  * 提供精确的加法运算。 
  * @param v1

  * @param v2

  * @return 两个参数的和

*/

public static double add(double v1, double v2)

{

BigDecimal b1 = new BigDecimal(Double.toString(v1));

BigDecimal b2 = new BigDecimal(Double.toString(v2));

return b1.add(b2).doubleValue();

}

/**

  * 提供精确的加法运算 
  * @param v1

  * @param v2

  * @return 两个参数数学加和，以字符串格式返回

*/

public static String add(String v1, String v2)

{

BigDecimal b1 = new BigDecimal(v1);

BigDecimal b2 = new BigDecimal(v2);

return b1.add(b2).toString();

}

/**

  * 提供精确的减法运算。 
  * @param v1

  * @param v2

  * @return 两个参数的差

*/

public static double subtract(double v1, double v2)

{

BigDecimal b1 = new BigDecimal(Double.toString(v1));

BigDecimal b2 = new BigDecimal(Double.toString(v2));

return b1.subtract(b2).doubleValue();

}

/**

  * 提供精确的减法运算 
  * @param v1

  * @param v2

  * @return 两个参数数学差，以字符串格式返回

*/

public static String subtract(String v1, String v2)

{

BigDecimal b1 = new BigDecimal(v1);

BigDecimal b2 = new BigDecimal(v2);

return b1.subtract(b2).toString();

}

/**

  * 提供精确的乘法运算。 
  * @param v1

  * @param v2

  * @return 两个参数的积

*/

public static double multiply(double v1, double v2)

{

BigDecimal b1 = new BigDecimal(Double.toString(v1));

BigDecimal b2 = new BigDecimal(Double.toString(v2));

return b1.multiply(b2).doubleValue();

}

/**

  * 提供精确的乘法运算 
  * @param v1

  * @param v2

  * @return 两个参数的数学积，以字符串格式返回

*/

public static String multiply(String v1, String v2)

{

BigDecimal b1 = new BigDecimal(v1);

BigDecimal b2 = new BigDecimal(v2);

return b1.multiply(b2).toString();

}

/**

  * 提供 (相对) 精确的除法运算，当发生除不尽的情况时，精确到 
  * 小数点以后10位，以后的数字四舍五入,舍入模式采用ROUND_HALF_EVEN

  * @param v1

  * @param v2

  * @return 两个参数的商

*/

public static double divide(double v1, double v2)

{

return divide(v1, v2, DEFAULT_DIV_SCALE);

}

/**

  * 提供 (相对) 精确的除法运算。当发生除不尽的情况时，由scale参数指 
  * 定精度，以后的数字四舍五入。舍入模式采用ROUND_HALF_EVEN

  * @param v1

  * @param v2

  * @param scale 表示需要精确到小数点以后几位。

  * @return 两个参数的商

*/

public static double divide(double v1,double v2, int scale)

{

return divide(v1, v2, scale, BigDecimal.ROUND_HALF_EVEN);

}

/**

  * 提供 (相对) 精确的除法运算。当发生除不尽的情况时，由scale参数指 
  * 定精度，以后的数字四舍五入。舍入模式采用用户指定舍入模式

  * @param v1

  * @param v2

  * @param scale 表示需要精确到小数点以后几位

  * @param round_mode 表示用户指定的舍入模式

  * @return 两个参数的商

*/

public static double divide(double v1,double v2,int scale, int round_mode){

if(scale < 0)

{

throw new IllegalArgumentException("The scale must be a positive integer or zero");

}

BigDecimal b1 = new BigDecimal(Double.toString(v1));

BigDecimal b2 = new BigDecimal(Double.toString(v2));

return b1.divide(b2, scale, round_mode).doubleValue();

}

/**

  * 提供 (相对) 精确的除法运算，当发生除不尽的情况时，精确到 
  * 小数点以后10位，以后的数字四舍五入,舍入模式采用ROUND_HALF_EVEN

  * @param v1

  * @param v2

  * @return 两个参数的商，以字符串格式返回

*/

public static String divide(String v1, String v2)

{

return divide(v1, v2, DEFAULT_DIV_SCALE);

}

/**

  * 提供 (相对) 精确的除法运算。当发生除不尽的情况时，由scale参数指 
  * 定精度，以后的数字四舍五入。舍入模式采用ROUND_HALF_EVEN

  * @param v1

  * @param v2

  * @param scale 表示需要精确到小数点以后几位

  * @return 两个参数的商，以字符串格式返回

*/

public static String divide(String v1, String v2, int scale)

{

return divide(v1, v2, DEFAULT_DIV_SCALE, BigDecimal.ROUND_HALF_EVEN);

}

/**

  * 提供 (相对) 精确的除法运算。当发生除不尽的情况时，由scale参数指 
  * 定精度，以后的数字四舍五入。舍入模式采用用户指定舍入模式

  * @param v1

  * @param v2

  * @param scale 表示需要精确到小数点以后几位

  * @param round_mode 表示用户指定的舍入模式

  * @return 两个参数的商，以字符串格式返回

*/

public static String divide(String v1, String v2, int scale, int round_mode)

{

if(scale < 0)

{

throw new IllegalArgumentException("The scale must be a positive integer or zero");

}

BigDecimal b1 = new BigDecimal(v1);

BigDecimal b2 = new BigDecimal(v2);

return b1.divide(b2, scale, round_mode).toString();

}

/**

  * 提供精确的小数位四舍五入处理,舍入模式采用ROUND_HALF_EVEN 
  * @param v 需要四舍五入的数字

  * @param scale 小数点后保留几位

  * @return 四舍五入后的结果

*/

public static double round(double v,int scale)

{

return round(v, scale, BigDecimal.ROUND_HALF_EVEN);

}

/**

  * 提供精确的小数位四舍五入处理 
  * @param v 需要四舍五入的数字

  * @param scale 小数点后保留几位

  * @param round_mode 指定的舍入模式

  * @return 四舍五入后的结果

*/

public static double round(double v, int scale, int round_mode)

{

if(scale<0)

{

throw new IllegalArgumentException("The scale must be a positive integer or zero");

}

BigDecimal b = new BigDecimal(Double.toString(v));

return b.setScale(scale, round_mode).doubleValue();

}

/**

  * 提供精确的小数位四舍五入处理,舍入模式采用ROUND_HALF_EVEN 
  * @param v 需要四舍五入的数字

  * @param scale 小数点后保留几位

  * @return 四舍五入后的结果，以字符串格式返回

*/

public static String round(String v, int scale)

{

return round(v, scale, BigDecimal.ROUND_HALF_EVEN);

}

/**

  * 提供精确的小数位四舍五入处理 
  * @param v 需要四舍五入的数字

  * @param scale 小数点后保留几位

  * @param round_mode 指定的舍入模式

  * @return 四舍五入后的结果，以字符串格式返回

*/

public static String round(String v, int scale, int round_mode)

{

if(scale<0)

{

throw new IllegalArgumentException("The scale must be a positive integer or zero");

}

BigDecimal b = new BigDecimal(v);

return b.setScale(scale, round_mode).toString();

}

}

BigDecimal 舍入模式 (Rounding mode) 介绍: 

BigDecimal定义了一下舍入模式，只有在作除法运算或四舍五入时才用到舍入模式，下面简单介绍，详细请查阅J2se API文档

static int ROUND_CEILING
  
Rounding mode to round towards positive infinity.

向正无穷方向舍入

static int ROUND_DOWN
  
Rounding mode to round towards zero.

向零方向舍入

static int ROUND_FLOOR
  
Rounding mode to round towards negative infinity.

向负无穷方向舍入

static int ROUND_HALF_DOWN
  
Rounding mode to round towards "nearest neighbor" unless both neighbors are equidistant, in which case round down.

向 (距离) 最近的一边舍入，除非两边 (的距离) 是相等,如果是这样，向下舍入, 例如1.55 保留一位小数结果为1.5

static int ROUND_HALF_EVEN
  
Rounding mode to round towards the "nearest neighbor" unless both neighbors are equidistant, in which case, round towards the even neighbor.

向 (距离) 最近的一边舍入，除非两边 (的距离) 是相等,如果是这样，如果保留位数是奇数，使用ROUND_HALF_UP ，如果是偶数，使用ROUND_HALF_DOWN

static int ROUND_HALF_UP
  
Rounding mode to round towards "nearest neighbor" unless both neighbors are equidistant, in which case round up.

向 (距离) 最近的一边舍入，除非两边 (的距离) 是相等,如果是这样，向上舍入, 1.55保留一位小数结果为1.6

static int ROUND_UNNECESSARY
  
Rounding mode to assert that the requested operation has an exact result, hence no rounding is necessary.

计算结果是精确的，不需要舍入模式

static int ROUND_UP
  
Rounding mode to round away from zero.

向远离0的方向舍入

http://blog.csdn.net/yuhua3272004/article/details/