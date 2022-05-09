---
title: java 自定义异常, customized exception
author: "-"
date: 2014-05-22T11:04:57+00:00
url: /?p=6653
categories:
  - Inbox
tags:
  - Java

---
## java 自定义异常, customized exception

编写自定义异常类的模式
  
编写自定义异常类实际上是继承一个API标准异常类,用新定义的异常处理信息覆盖原有信息的过程。常用的编写自定义异常类的模式如下:

public class CustomException extends Exception { //或者继承任何标准异常类
  
public CustomException() {} //用来创建无参数对象
  
public CustomException(String message) { //用来创建指定参数对象
  
super(message); //调用超类构造器
  
}
  
}

当然也可选用Throwable作为超类。其中无参数构造器为创建缺省参数对象提供了方便。第二个构造器将在创建这个异常对象时提供描述这个异常信息的字符串,通过调用超类构造器向上传递给超类,对超类中的toString()方法中返回的原有信息进行覆盖。
  
来讨论一个具体例子。假设程序中需要验证用户输入的表示年龄的数据必须是正整数值。我们可以按照以上模式编写这个自定义异常类如下:

public class NegativeAgeException extends Exception {
  
//或者: extends Throwable
  
public NegativeAgeException() {}
  
public NegativeAgeException(String message) {
  
super(message);
  
}
  
}

下面是应用这个自定义异常类的例子:

//完整程序存在本书配套资源目录为Ch11中名为NegativeAgeExceptionTest.java
  
...
  
try{
  
String ageString = JOptionPane.showInputDialog("Enter your age: ");

if (Integer.parseInt(ageString) < 0)
  
throw new NegativeAgeException("Please enter a positive age");
  
else
  
JOptionPane.showMessageDialog(null, ageString, "Age", 1);
  
}
  
catch(NegativeAgeException e){
  
System.out.println(e);
  
}
  
...

或者,可以创建一个缺省对象,然后在catch中打印具体信息,如:

throw new NegativeAgeException();
  
...
  
catch (NegativeAgeException e) {
  
System.out.println("Please enter a positive age");

将产生与第一个例子相同的效果。
  
11.7.2 自定义异常处理
  
无论是利用标准API异常类来处理特殊的异常,或者编写自定义的异常类来达到同样目的,问题的关键是:
  
1. 当这个异常发生时,如何及时捕获这个异常。
  
2. 捕获这个异常后,如何产生精确的异常处理信息。
  
毋庸置疑,我们不可能期待JVM自动抛出一个自定义异常,也不能够期待JVM会自动处理一个自定义异常。发现异常、抛出异常以及处理异常的工作必须靠编程人员在代码中利用异常处理机制自己完成。
  
一般情况下,发现和抛出一个自定义异常通过在try程序块中利用if和throw语句完成,即:

try {
  
...
  
if (someExceptionConditon == true) {
  
throw new CustomException("A custom exception xxx occurred. Please
  
check your entry...")
  
...
  
}
  
catch (CustomException e) {
  
...
  
}

而打印异常处理信息可以在抛出时包括在构造器的参数中,或者包括在处理这个异常的catch中。
  
另外应该注意在自定义异常发生之前,有可能产生标准异常的情况。例如,在一个需要验证年龄必须是正整数值的程序中,利用自定义异常类,如NegativeAgeException,验证输入的年龄是否正整数,即:

try {
  
...
  
if (Integer.parseInt(ageString) < 0)
  
throw NegativeAgeException("Please enter a positive age");
  
else
  
...
  
}
  
catch (NumberFormatException e) {
  
System.out.println(e);
  
}
  
catch (NegativeAgeException e) {
  
System.out.println(e);
  
}
  
...

注意在这个代码中,如果ageString是非法整数字符串,如"25ab",系统将首先抛出NumberFormatException,而不会执行throw NegativeAgeException("Please enter a positive age")。所以应该在catch中加入对NumberFormatException的处理,如以上代码所示。

本文出自 "海外咖啡豆 - 高永强的.." 博客,请务必保留此出处<http://yqgao.blog.51cto.com/773490/174767>

<http://yqgao.blog.51cto.com/773490/174767>
