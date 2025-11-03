---
title: 自动装箱 拆箱
author: "-"
date: "2020-06-30 17:26:53"
url: java-wrapper
categories:
  - Java
tags:
  - Java
---
## 自动装箱 拆箱

Java作为面向对象语言，有人认为所看到的都是对象，事实上，在Java SE 5之前，基本类型默认并不是采用对象存在的如果您想要把基本类型作为对象来处理，就必须自行转换，不过，在Java SE 5之后，为基本数据类型提供了自动装箱和拆箱功能，使得将基本类型转换为对象变得极其便捷。

在这里来捋一捋java的基本数据类型，不理不要紧，一理才发现俺也掌握的不是那么明确，在这里俺也再次学习下
  
总计有八个，分别是
  
byte字节型 (一个字节) ，char字符型 (两个字节) ，short短整型 (两个字节) ，int整型 (四个字节) ，
  
long长整型 (八个字节) ，float浮点型 (四个字节) ，double 双精度浮点型 (八个字节) ，boolean型 (一个字节) 
  
在javase5之前，如果想要把基本数据类型作为对象来操作，就需要采用对应的对象，来把它们打包才行

现在虽然不用这样了，但其中也有一些要注意的地方，俺揪出来晒晒。

先说说类和对象，建立个概念吧先

类-可以认为是对象的设计图
  
对象-是按照设计图实现了的具体工具
  
先这么简单理解吧，如果真要扯开了说，那可是软件工程里面的一门专业课，我们有个概念就好
  
之所以要将基本类型数据打包成为对象，原因很简单，是因为对象可以携带更多的数据。

手动、自动装箱拆箱示例

Long，Integer，Double，Float,Boolean等等的类就是所谓的wrapper类，就跟wrapper这个单词所代表的意思一样，就是提供一个"包装，加壳"，把基本数据类型放在里面，来看代码，体会下先

public class WrapperDemo{
  
public staticvoid main(String[] args){
  
int data1=21;
  
int data2=24;
  
//打包成为对象
  
Integer data1Wrapper = new Integer(data1);
  
Integer data2Wrapper = new Integer(data2);
  
//原始数据直接除以3
  
System.out.println(data1/3);
  
//将数据打包，转换为double型，除以3
  
System.out.println(data1Wrapper.doubleValue()/3);
  
//比较
  
System.out.println(data1Wrapper.compareTo(data2Wrapper));
  
}

}

图1-1 WrapperDemo的运行结果

通过上面的代码和运行结果，看到了将基本数据类型打包成为对象带来的好处了吧，别着急，这还只是javase5之前的做法，在javase5之后就已经支持自动装箱和拆箱了，在这，就不再单独写代码出来了，只写几个能说明问题的语句就可以了，相信很容易理解的。

javase5之前，手动打包
  
Integer data1 = new Integer(10);
  
事项将基本类型数据转换为对象
  
javase5之后，支持自动打包
  
Integer data1 = 10；
  
便可以实现将基本类型的数据转换为对象
  
eg: 
  
在上面的代码中，可以采用，可以直接进行两个基本数据类型的比较
  
data1.compareTo (data2) ;
  
基本数据类型本身没有什么方法，当你运行之后会发现，它仍然可以正确运行，这就自动装箱和拆箱带来的好处
  
再来说说自动装箱拆箱

自动装箱和拆箱，从本质上讲，是编译器帮了我们的忙，这就是所谓的"编译器蜜糖"，既然这么好，是不是就可以放心的用了呢？

先别着急，喝口水，咱再接着唠

看看下面的情况，您是否了解

Integer i = null;//表明i没有参考至任何对象
  
int j = i ;//相当于 int j = i.intValue () 
  
这样的代码，编译时是可以通过的，因为它的语法是正确的，但在运行时，就会排除NullPointerException错误，这是由于i并没有参考至任何对象造成的
  
个人建议，如果您对装箱拆箱不是理解的很清楚，最好还是按部就班的一步一步的对它进行装包和拆包，这样，有的时候，可能会为你节省很多纠错的时间哦
  
还是自动装箱拆箱

public class BoxDemo{
  
public static void main(String[] args){
  
Integer data1 = 500;
  
Integer data2 = 500;
  
System.out.println(data1==data2);
  
}
  
}
  
在你看到接下来的运行结果前，您先猜猜看，运行的结果会是怎样的呢？true or false？
  
图1-2 BoxDemo运行结果

false？没错，它就是false，自动装箱时，对于值从-128-127之间的数，被装箱后，会被放在内存中进行重用，

如果超出了这个值的范围就不会被重用的，所以每次new出来的都是一个新的对象，结果自然会是false。

在这里，区别一个概念"=="和equals () 
  
"=="是比较两个对象是不是引用自同一个对象。
  
"equals () "是比较两个对象的内容。
  
这个一定得搞清楚，否则，在遇到问题的时候，可真是会让人抓狂的。
  
原文链接: http://blog.csdn.net/mlc0202/article/details/7393471



  
    
      
        
          java是一种面向对象语言,java中的类把方法与数据连接在一起,并构成了自包含式的处理单元.但在java中不能定义基本类型(primitive type),为了能将基本类型视为对象来处理,并能连接相关的方法,java为每个基本类型都提供了包装类,这样,我们便可以把这些基本类型转化为对象来处理了.这些包装类有:Boolean,Byte,Short,Character,Integer,Long,Float,Double,Void共9个(注意: Date不是，无其基本类型).
        
        
        
          一、 包装类(Wrapper Class)共同的方法
        
        
        
          值得说明的是,java是可以直接处理基本类型的,但是在有些情况下我们需要将其作为对象来处理,这时就需要将其转化为包装类了.所有的包装类(Wrapper Class)都有共同的方法,他们是:
        
        
        
          (1)带有基本值参数并创建包装类对象的构造函数.如可以利用Integer包装类创建对象,Integer obj=new Integer(145);
        
        
        
          (2)带有字符串参数并创建包装类对象的构造函数.如new Integer("-45.36");
        
        
        
          (3)可生成对象基本值的typeValue方法,如obj.intValue();
        
        
        
          (4)将字符串转换为基本值的 parseType方法,如Integer.parseInt(args[0]);
        
        
        
          (5)生成哈稀表代码的hashCode方法,如obj.hasCode();
        
        
        
          (6)对同一个类的两个对象进行比较的equals()方法,如obj1.eauqls(obj2);
        
        
        
          (7)生成字符串表示法的toString()方法,如obj.toString().
        
        
        
          
        
        
        
          转换关系: 
        
        
        
          基本类型-->包装器类
 Integer obj=new Integer(145);
        
        
        
          包装器类-->基本类型
 int num=obj.intValue();
        
        
        
          字符串-->包装器类
 Integer obj=new Integer("-45.36");
        
        
        
          包装器类-->字符串包装器类
        
        
        
          String str=obj.toString();
        
        
        
          字符串-->基本类型
 int num=Integer.parseInt("-45.36");
        
        
        
          基本类型-->字符串包装器类
        
        
        
          String str=String.valueOf(5);
 在一定的场合,运用java包装类来解决问题,能大大提高编程效率.
        
        
        
          
        
        
        
          二、JDK1.5的新特性: 自动装箱/拆箱(Autoboxing/unboxing)
        
        
        
          自动装箱/拆箱大大方便了基本类型数据和它们包装类地使用。
        
        
        
          自动装箱: 基本类型自动转为包装类.(int>>Integer)
        
        
        
          自动拆箱: 包装类自动转为基本类型.(Integer>>int)
        
        
        
          在JDK1.5之前，我们总是对集合不能存放基本类型而耿耿于怀，现在自动转换机制
 解决了我们的问题。
        
        
        
          inta=3;
 Collectionc=newArrayList();
 c.add(a);//自动转换成Integer.
        
        
        
          Integerb=newInteger(2);
 c.add(b+2);
        
        
        
          这里Integer先自动转换为int进行加法运算，然后int再次转换为Integer.
        
      
    
  


http://developer.51cto.com/art/201203/325314.htm