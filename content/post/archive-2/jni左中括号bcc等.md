---
title: 'JNI左中括号[B[C[[C等'
author: "-"
date: 2017-06-02T02:54:06+00:00
url: /?p=10453
categories:
  - Inbox
tags:
  - reprint
---
## 'JNI左中括号[B[C[[C等'
http://blog.csdn.net/qinjuning/article/details/7599796

在Java存在两种数据类型:  基本类型 和 引用类型 。

    在JNI的世界里也存在类似的数据类型,与Java比较起来,其范围更具严格性,如下: 
    
        1、primitive types ----基本数据类型,如: int、 float 、char等基本类型
        2、reference types----引用类型,如: 类、实例、数组。
    
      特别需要注意: 数组 ------ 不管是对象数组还是基本类型数组,都作为reference types存在。
    
     1、primitive types (基本数据类型)映射参见下表:  
    
    
    
        这些基本数据类型都是可以在Native层直接使用的 。
    
      2、reference types (引用数据类型)映射参见下表
    
                        Java类型                      Native Type                                          描述
    
    
     注意:    
        1、引用数据类型则不能直接使用,需要根据JNI函数进行相应的转换后,才能使用
        2、多维数组(包括二维数组)都是引用类型,需要使用 jobjectArray 类型存取其值 ；
                 例如: 二维整型数组就是指向一位数组的数组,其声明使用方式如下: 
    

```java 

print?
  
//获得一维数组 的类引用,即jintArray类型
      
jclass intArrayClass = env->FindClass("[I");
      
//构造一个指向jintArray类一维数组的对象数组,该对象数组初始大小为dimion
      
jobjectArray obejctIntArray = env->NewObjectArray(dimion ,intArrayClass , NULL);
      
...//具体操作

另外,关于引用类型的一个继承关系如下,我们可以对具有父子关系的类型进行转换: 

类描述符

    类描述符是类的完整名称 (包名+类名) ,将原来的 . 分隔符换成 / 分隔符。
           例如: 在java代码中的java.lang.String类的类描述符就是java/lang/String
    
       其实,在实践中,我发现可以直接用该类型的域描述符取代,也是可以成功的。
              例如:         jclass intArrCls = env->FindClass("java/lang/String")
                等同于      jclass intArrCls = env->FindClass("Ljava/lang/String;")
    

数组类型的描述符则为,则为:  [ + 其类型的域描述符 (后文说明)
             
例如: 
                    
int [ ] 其描述符为[I
                    
float [ ] 其描述符为[F
                    
String [ ] 其描述符为[Ljava/lang/String;

域描述符

      1、基本类型的描述符已经被定义好了,如下表所示: 
    
    
    
    
    
     2、引用类型的描述符
    
         一般引用类型则为 L + 该类型类描述符 + ;   (注意,这儿的分号"；"只得是JNI的一部分,而不是我们汉语中的分段,下同)
                  例如: String类型的域描述符为 Ljava/lang/String;  
    
          对于数组,其为 :  [ + 其类型的域描述符 + ;
    
                  int[ ]     其描述符为[I
                  float[ ]   其描述符为[F
                  String[ ]  其描述符为[Ljava/lang/String;
                 Object[ ]类型的域描述符为[Ljava/lang/Object;
    
          多维数组则是 n个[ +该类型的域描述符 , N代表的是几维数组。例如: 
             int  [ ][ ] 其描述符为[[I
            float[ ][ ] 其描述符为[[F
    

方法描述符

       将参数类型的域描述符按照申明顺序放入一对括号中后跟返回值类型的域描述符,规则如下:  (参数的域描述符的叠加)返回
    

类型描述符。对于,没有返回值的,用V(表示void型)表示。举例如下: 

                 Java层方法                                               JNI函数签名
                String test ( )                                              Ljava/lang/String;
                int f (int i, Object object)                            (ILjava/lang/Object;)I
                void set (byte[ ] bytes)                                ([B)V
    
    
     在编程时,如果是利用javah工具的话,这些都不需要我们手动编写对应的类型转换,如果不能用javah工具,就只能手动的
    

进行类型转换了。