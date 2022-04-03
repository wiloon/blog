---
title: MSBuild
author: "-"
date: 2013-02-17T08:51:23+00:00
url: /?p=5170
categories:
  - Uncategorized

tags:
  - reprint
---
## MSBuild

  http://blog.csdn.net/gordonliwei/article/details/1500529


我想一些朋友已经知道或是使用Microsoft的MSBuild来Build应用程序,如果您还没有听过MSBuild是什么,那么您可以在: 

<http://msdn2.microsoft.com/en-us/library/wea2sca5.aspx>

找到有关MSBuild的信息。

MSBuild内付于.Net Framework 2.0中,VS Studio 2005使用的Build就是MSBuild。MSBuild类似于Java的Ant或是.NET移植版本NAnt,都允许开发人员撰写XML文件来指定Build的流程。不过MSBuild和Ant/NAnt不太一样的地方是,MSBuild比较偏向传统的Make工具,但是MSBuild改正了许多传统Make工具的缺点。由于MSBuild在网络上有许多的信息,因此,我在这里并不是讨论MSBuild的技术面,而是想谈谈MSBuild有趣的地方。

MSBuild在VS Studio中应该是作为C#/VB.NET等项目的Build工具 (应该是因为我没有VS Studio 2005) ,因此,MSBuild主要是作为.NET程序语言项目的Build工具。但是MSBuild在理论上应该是可以作为Windows平台上通用的Build工具,而不只限于.NET程序语言项目。这当然是因为MSBuild允许开发人员使用XML撰写Build流程,此外,MSBuild也允许开发人员调用外部工具。因此,MSBuild也应该可以让Win32的开发工具用来作为通用的Build工具,例如Delphi,C++Builder,甚至是PHP等。

那么使用MSBuild作为Build工具有什么好处? 比如说Delphi和C++Builder都有自己的Build工具,那为什么还要使用MSBuild? 其实一个非常简单的答案就是Delphi For Win32,C++Builder,Delphi.NET,C#Builder以及未来的Delphi For Win64等就可以提供一个通用的Build机制和Build工具。

另外一个原因则非常重要,由于MSBuild允许开发人员使用XML撰写/定义Build流程,因此对于大型、复杂的项目而言,这允许开发工具借助MSBuild提供更为弹性的Build流程,更重要的是MSBuild允许开发人员拆解Build流程,让复杂项目中相同的部分可以执行相同的Build工作,或是在不同的项目中共享相同的Build流程。如果好好利用这个特点,那么开发人员在Build复杂项目时可以大幅减少需要的Build时间,或是对于像C++这样需要两到三个Pass的编译器而言,这可以大幅减少编译、连接等Build的时间。例如在笔者自行测试的案例中,笔者把以前许多C++Builder的项目重新使用MSBuild来重新Build,结果是使用MSBuild比以前节省了将近50%的时间,这大大说明了善用MSBuild的好处。

那么CodeGear在未来会如何善用MSBuild？我相信各位很快就会知道了。