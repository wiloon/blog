---
title: activity的android:name 设置问题
author: wiloon
type: post
date: 2014-07-28T08:50:05+00:00
url: /?p=6830
categories:
  - Uncategorized

---
<div class="cnblogs_code" style="color: #000000;">
  &lt;manifest xmlns:android="http://schemas.android.com/apk/res/android" 
<span style="color: #008080;"> 2</span>     <span style="color: #0000ff;">package</span>="com.example.android.apis"&gt; 
<span style="color: #008080;"> 3</span> 
<span style="color: #008080;"> 4</span> 
<span style="color: #008080;"> 5</span> &lt;activity android:name="<span style="color: #ff0000;">ApiDemos</span>"&gt; 
<span style="color: #008080;"> 6</span>             &lt;intent-filter&gt; 
<span style="color: #008080;"> 7</span>                 &lt;action android:name="android.intent.action.MAIN" /&gt; 
<span style="color: #008080;"> 8</span>                 &lt;category android:name="android.intent.category.DEFAULT" /&gt; 
<span style="color: #008080;"> 9</span>                 &lt;category android:name="android.intent.category.LAUNCHER" /&gt; 
<span style="color: #008080;">10</span>             &lt;/intent-filter&gt; 
<span style="color: #008080;">11</span> &lt;/activity&gt; 
<span style="color: #008080;">12</span> 
<span style="color: #008080;">13</span> 
<span style="color: #008080;">14</span> &lt;activity android:name="<span style="color: #ff0000;">.app.HelloWorld</span>" android:label="@string/activity_hello_world"&gt; 
<span style="color: #008080;">15</span>             &lt;intent-filter&gt; 
<span style="color: #008080;">16</span>                 &lt;action android:name="android.intent.action.MAIN" /&gt; 
<span style="color: #008080;">17</span>                 &lt;category android:name="android.intent.category.SAMPLE_CODE" /&gt; 
<span style="color: #008080;">18</span>             &lt;/intent-filter&gt; 
<span style="color: #008080;">19</span> &lt;/activity&gt;
  
  <div class="cnblogs_code_toolbar">
    <span class="cnblogs_code_copy"><a style="color: #4371a6;" title="复制代码"><img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" /></a></span>
  


<p style="color: #4b4b4b;">
  　　activity 组件的 android:name 属性采用类名的简写方式，查看文档类名的简写格式为<span style="color: #ff0000;"> ".ClassName"</span>, 但为什么<activity android:name="ApiDemos">里的android:anem="ApiDemos"，而不是android:anem=".ApiDemos"呢？ 而后面的所有Activity组件的android:name的值都是".ClassName"格式呢？google查询android:name属性值的说明，但未查到有类名前不加 "." 的说明!


<p style="color: #4b4b4b;">
  测试验证结果 "ApiDemos" 与 ".ApiDemos" 的写法都能正确运行程序。明明文档中说明的是 ".ClassName" 格式啊, 难道类名前有 "." 与没有 "." 是一样的？！于是把其它的Activity的android:name的值字符串中的第一个 "."去掉，再运行程序，却不行.


<p style="color: #4b4b4b;">
  　　反复的测试，发现了一个规则：


<p style="color: #4b4b4b;">
  　　如果manifest中指定了package属性，比如指定为"com.example.android.apis"，如果activity的实现类ApiDemos 也在这个package下，则android:name为实现的类名，这个类名前加不加点都没有关系，


<p style="color: #4b4b4b;">
  　　如果activity的实现类是在默认包的子包里面，则这个 "." 是必须有的，比如activity的实现是com.android.sample.app.DialogActivity，则android:name必须写成.app.DialogActivity或者com.android.sample.app.DialogActivity。如果只写app.DialogActivity，则会报错。


<p style="color: #4b4b4b;">
  　　不论Activity的子类是否在默认package下，还是在默认包的子包下，类名的简写方式统统采用“.ClassName”的方式，可避免类似问题！


<p style="color: #4b4b4b;">
  参考：


<p style="color: #4b4b4b;">
  　　<a style="color: #4371a6;" href="http://blog.csdn.net/fuxiaohui/article/details/9348677">http://blog.csdn.net/fuxiaohui/article/details/9348677</a>
