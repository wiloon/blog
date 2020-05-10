---
title: android.intent.action.MAIN 与 android.intent.category.LAUNCHER
author: wiloon
type: post
date: 2014-04-14T08:06:08+00:00
url: /?p=6547
categories:
  - Uncategorized

---
先看看网路上的说法：

android.intent.action.MAIN决定应用程序最先启动的

Activity android.intent.category.LAUNCHER决定应用程序是否显示在程序列表里

通过实验后，发现有问题？

MAIN 与 LAUNCHER 并不是单纯的各管各的事情；

个人认为正确的说法是

我测试的结果是，如果一个应用没有LAUNCHER则该apk仍能安装到设备上，但是在桌面中图标中看不到。如果给那个Activity 设定了LAUNCHER，且同时设定了Main,则这个Activity就可出现在程序图标中；如果没有Main，则不知启动哪个Activity，故也不会有图标出现。可见，Main指的是，点击图标后启动哪个Activity。当然，Main可以给多个Activity设定，但只设定Main不设定LAUNCHER，仍然无法进入activity。

可见，Main和LAUNCHER同时设定才有意义，如果多个activity同时设定，则会出现两个图标，分别先进入不同的activity.如下图：Lift\_cycles 01 与 Lift\_cycles 02

\[html\]\[/html\] view plaincopy

<activity android:name=&#8221;.Life_CyclesActivity&#8221;

android:label=&#8221;Lift_cycles 01&#8243;>

<intent-filter>

<action android:name=&#8221;android.intent.action.MAIN&#8221; />

<category android:name=&#8221;android.intent.category.LAUNCHER&#8221; />

</intent-filter>

</activity>

<activity android:name=&#8221;Life_CyclesActivity02&#8243;

android:label=&#8221;Lift_cycles 02&#8243;>

<intent-filter>

<action android:name=&#8221;android.intent.action.MAIN&#8221; />

<category android:name=&#8221;android.intent.category.LAUNCHER&#8221; />

</intent-filter>

</activity>

&nbsp;