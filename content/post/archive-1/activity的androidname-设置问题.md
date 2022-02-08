---
title: activity的android,name 设置问题
author: "-"
date: 2014-07-28T08:50:05+00:00
url: /?p=6830
categories:
  - Uncategorized

tags:
  - reprint
---
## activity的android,name 设置问题

  <manifest xmlns:android="http://schemas.android.com/apk/res/android" 
 2     package="com.example.android.apis"> 
 3 
 4 
 5  
 6             <intent-filter> 
 7                  
 8                 <category android:name="android.intent.category.DEFAULT" /> 
 9                 <category android:name="android.intent.category.LAUNCHER" /> 
10             </intent-filter> 
11 </activity> 
12 
13 
14  
15             <intent-filter> 
16                  
17                 <category android:name="android.intent.category.SAMPLE_CODE" /> 
18             </intent-filter> 
19 </activity>
  
  
    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  


  activity 组件的 android:name 属性采用类名的简写方式，查看文档类名的简写格式为 ".ClassName", 但为什么里的android:anem="ApiDemos"，而不是android:anem=".ApiDemos"呢？ 而后面的所有Activity组件的android:name的值都是".ClassName"格式呢？google查询android:name属性值的说明，但未查到有类名前不加 "." 的说明!


  测试验证结果 "ApiDemos" 与 ".ApiDemos" 的写法都能正确运行程序。明明文档中说明的是 ".ClassName" 格式啊, 难道类名前有 "." 与没有 "." 是一样的？！于是把其它的Activity的android:name的值字符串中的第一个 "."去掉，再运行程序，却不行.


  反复的测试，发现了一个规则: 


  如果manifest中指定了package属性，比如指定为"com.example.android.apis"，如果activity的实现类ApiDemos 也在这个package下，则android:name为实现的类名，这个类名前加不加点都没有关系，


  如果activity的实现类是在默认包的子包里面，则这个 "." 是必须有的，比如activity的实现是com.android.sample.app.DialogActivity，则android:name必须写成.app.DialogActivity或者com.android.sample.app.DialogActivity。如果只写app.DialogActivity，则会报错。


  不论Activity的子类是否在默认package下，还是在默认包的子包下，类名的简写方式统统采用".ClassName"的方式，可避免类似问题！


  参考: 


  http://blog.csdn.net/fuxiaohui/article/details/9348677
