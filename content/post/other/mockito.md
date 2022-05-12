---
title: Mockito
author: "-"
date: 2015-08-13T04:13:05.000+00:00
url: "/?p=8103"
categories: []
tags:
  - reprint
---
## Mockito

### 部分mock (partial mock)

部分mock是说一个类的方法有些是实际调用，有些是使用mockito的stubbing (桩实现) 。

### 为什么需要部分mock

当需要测试一个组合方法 (一个方法需要其它多个方法协作) 的时候，某个叶子方法 (只供别人调用，自己不依赖其它反复) 已经被测试过，我们其实不需要再次测试这个叶子方法，so，让叶子打桩实现返回结果，上层方法实际调用并测试。

mockito实现部分mock的两种方式: spy和 callRealMethod()

spy的原理是，如果不打桩默认都会执行真实的方法，如果打桩则返回桩实现。可以看出spy.size()通过桩实现返回了值100，而spy.get(0)则返回了实际值

```java
    List<String> list = new LinkedList<String>();  
    List<String> spy = spy(list);  
    when(spy.size()).thenReturn(100);  
    spy.add("one");  
    spy.add("two");  
    assertEquals(spy.get(0), "one");  
    assertEquals(100, spy.size());

    Channel channel = mock(Channel.class);
    when(channel.writeAndFlush(obj)).thenReturn(null);
```

```java
    // 重置 spy 对象，让 add(1,2) 调用真实方法，返回 3
        when(exampleService.add(1, 2)).thenCallRealMethod();
        Assert.assertEquals(3, exampleService.add(1, 2));
```

一、什么是mock测试，什么是mock对象？

一种替代方案就是使用mocks

从图中可以清晰的看出

mock对象就是在调试期间用来作为真实对象的替代品。

mock测试就是在测试过程中，对那些不容易构建的对象用一个虚拟对象来代替测试的方法就叫mock测试。

知道什么是mock测试后，那么我们就来认识一下mock框架—Mockito

二、什么是Mockito

除了有一个好记的名字外，Mockito尝试用不一样的方法做mocking测试，是简单轻量级能够替代EasyMock的框架。使用简单，测试代码可读性高，丰富的文档包含在javadoc中，直接在IDE中可查看文档，实例，说明。更多信息: [http://code.google.com/p/mockito/](http://code.google.com/p/mockito/)

三、Stub和Mock

相同点: Stub和Mock对象都是用来模拟外部依赖，使我们能控制。

不同点: 而stub完全是模拟一个外部依赖，用来提供测试时所需要的测试数据。而mock对象用来判断测试是否能通过，也就是用来验证测试中依赖对象间的交互能否达到预期。在mocking框架中mock对象可以同时作为stub和mock对象使用，两者并没有严格区别。 更多信息: [http://martinfowler.com/articles/mocksArentStubs.html](http://martinfowler.com/articles/mocksArentStubs.html)

四、mockito入门实例

Maven依赖: (没用maven管理的可以下载相关jar包导入classpath)

Xml代码

      <embed src="http://liuzhijun.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://liuzhijun.iteye.com/images/icon_star.png" alt="收藏代码" />

<dependencies>

<dependency>

<groupId>org.mockito</groupId>

<artifactId>mockito-all</artifactId>

<version>1.8.5</version>

<scope>test</scope>

</dependency>

</dependencies>

Java代码

      <embed src="http://liuzhijun.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://liuzhijun.iteye.com/images/icon_star.png" alt="收藏代码" />

import static org.mockito.Mockito.*;

import java.util.List;

import org.junit.Assert;

import org.junit.Test;

/**

*

* @author lzjun

* @version 0.1

* @date 2012-5-5

* {@link <http://weibo.com/u/1697702241>}

*

 */

public class SimpleTest {

    @Test


    public void simpleTest(){




        //创建mock对象，参数可以是类，也可以是接口


        List<String> list = mock(List.class);




        //设置方法的预期返回值


        when(list.get()).thenReturn("helloworld");




        String result = list.get();




        //验证方法调用(是否调用了get(0))


        verify(list).get();




        //junit测试


        Assert.assertEquals("helloworld", result);


    }

}

好了，五分钟差不多了，还想继续了解那就可以往下面看![](http://liuzhijun.iteye.com/images/smiles/icon_biggrin.gif)

创建mock对象不能对final，Anonymous ，primitive类进行mock。

可对方法设定返回异常

Java代码

      <embed src="http://liuzhijun.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://liuzhijun.iteye.com/images/icon_star.png" alt="收藏代码" />

when(list.get(1)).thenThrow(new RuntimeException("test excpetion"));

stubbing另一种语法(设置预期值的方法)，可读性不如前者

Java代码

      <embed src="http://liuzhijun.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://liuzhijun.iteye.com/images/icon_star.png" alt="收藏代码" />

doReturn("secondhello").when(list).get(1);

没有返回值的void方法与其设定(支持迭代风格，第一次调用donothing,第二次dothrow抛出runtime异常)

Java代码

      <embed src="http://liuzhijun.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://liuzhijun.iteye.com/images/icon_star.png" alt="收藏代码" />

doNothing().doThrow(new RuntimeException("void exception")).when(list).clear();

list.clear();

list.clear();

verify(list,times(2)).clear();

五、参数匹配器(Argument Matcher)

Matchers类内加你有很多参数匹配器  anyInt、anyString、anyMap…..Mockito类继承于Matchers,Stubbing时使用内建参数匹配器，下例:

Java代码

      <embed src="http://liuzhijun.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://liuzhijun.iteye.com/images/icon_star.png" alt="收藏代码" />

@Test

public void argumentMatcherTest(){

    List<String> list = mock(List.class);




    when(list.get(anyInt())).thenReturn("hello","world");




    String result = list.get()+list.get(1);




    verify(list,times(2)).get(anyInt());




    Assert.assertEquals("helloworld", result);

}

需要注意的是: 如果使用参数匹配器，那么所有的参数都要使用参数匹配器，不管是stubbing还是verify的时候都一样。

Java代码

      <embed src="http://liuzhijun.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://liuzhijun.iteye.com/images/icon_star.png" alt="收藏代码" />

@Test

public void argumentMatcherTest2(){

    Map<Integer,String> map = mock(Map.class);


    when(map.put(anyInt(),anyString())).thenReturn("hello");//anyString()替换成"hello"就会报错


    map.put(1, "world");


    verify(map).put(eq(1), eq("world")); //eq("world")替换成"world"也会报错

}

六、方法调用的验证(具体的调用次数、至少一次，一次也没有)

Java代码

      <embed src="http://liuzhijun.iteye.com/javascripts/syntaxhighlighter/clipboard_new.swf" type="application/x-shockwave-flash" width="14" height="15">
      </embed> 
      
      <img class="star" src="http://liuzhijun.iteye.com/images/icon_star.png" alt="收藏代码" />

@Test

public void verifyInvocate(){

    List<String> mockedList = mock(List.class);


    //using mock 


     mockedList.add("once");


     mockedList.add("twice");


     mockedList.add("twice");




     mockedList.add("three times");


     mockedList.add("three times");


     mockedList.add("three times");




     /**


      * 基本的验证方法


      * verify方法验证mock对象是否有没有调用mockedList.add("once")方法


      * 不关心其是否有返回值，如果没有调用测试失败。


      */


     verify(mockedList).add("once");


     verify(mockedList, times(1)).add("once");//默认调用一次,times(1)可以省略






     verify(mockedList, times(2)).add("twice");


     verify(mockedList, times(3)).add("three times");




     //never()等同于time(0),一次也没有调用


     verify(mockedList, times()).add("never happened");




     //atLeastOnece/atLeast()/atMost()


     verify(mockedList, atLeastOnce()).add("three times");


     verify(mockedList, atLeast(2)).add("twice");


     verify(mockedList, atMost(5)).add("three times");

}

一次写不完，慢慢分析。。。

参考:

[http://mockito.googlecode.com/svn/branches/1.6/javadoc/org/mockito/Mockito.html](http://mockito.googlecode.com/svn/branches/1.6/javadoc/org/mockito/Mockito.html)

[http://www.sizovpoint.com/2009/03/java-mock-frameworks-comparison.html](http://www.sizovpoint.com/2009/03/java-mock-frameworks-comparison.html)

[http://wenku.baidu.com/view/8def451a227916888486d73f.html](http://wenku.baidu.com/view/8def451a227916888486d73f.html)

[http://qiuguo0205.iteye.com/blog/1443344](http://qiuguo0205.iteye.com/blog/1443344)

<http://bijian1013.iteye.com/blog/1986068>

<http://blog.csdn.net/onlyqi/article/details/6396646>

<http://site.mockito.org/mockito/docs/current/org/mockito/Mockito.html>

ockito是一种mock工具/框架。我理解EasyMock有点过时了，Mockito是现在比较流行的。

什么是mock？说的直白一点，大家都知道unit test应该是尽可能独立的。对一个class的unit test不应该再和其他class有任何交互。

现在有一个类，扫描一个目录并将找到的文件都上传到FTP server。该类对于不同的FTP响应(找不到FTP server 或 上传成功，或上传失败)，有一些后续操作。

在写这个类的UT时，我们就必须虚构出来一个FTP对象。这样在UT中，这个虚构的对象能够代替真正的FTP，对被测试类的调用做出一定的响应。从而知道被测试类是否正确的调用了FTP并做出一些正确的期望的响应。从而达到测试的目的。

mock可以模拟各种各样的对象，从而代替真正的对象做出希望的响应。

关于mock的概念和EasyMock，可以参考:

Mock object and EasyMock framework

[http://blog.csdn.net/OnlyQi/archive/2011/04/26/6364885.aspx](http://blog.csdn.net/OnlyQi/archive/2011/04/26/6364885.aspx)

官网: [http://mockito.org/](http://mockito.org/)

一篇很好的入门文章:

<http://blog.csdn.net/huoshuxiao/archive/2010/12/30/6107835.aspx>

一些稍微复杂且实用一点的例子:

[http://gojko.net/2009/10/23/mockito-in-six-easy-examples/](http://gojko.net/2009/10/23/mockito-in-six-easy-examples/)

<http://liuzhijun.iteye.com/blog/1512780>
