---
title: QTP
author: "-"
date: 2012-12-10T13:01:23+00:00
url: /?p=4879
categories:
  - Uncategorized

tags:
  - reprint
---
## QTP
QTP是quicktest Professional的简称,是一种自动测试工具。使用QTP的目的是想用它来执行重复的手动测试,主要是用于回归测试和测试同一软件的新版本。因此你在测试前要考虑好如何对应用程序进行测试,例如要测试那些功能、操作步骤、输入数据和期望的输出数据等Mercury QuickTest 企业级自动化测试工具!


现在已经被惠普收购,正式名字为HP QuickTest Professional software ,最新的版本为HP QuickTest Professional 11.0


HP QuickTest Professional 提供符合所有主要应用软件环境的功能测试和回归测试的自动化。采用关键字驱动的理念以简化测试用例的创建和维护。它让用户可以直接录制屏幕上的操作流程,自动生成功能测试或者回归测试用例。专业的测试者也可以通过提供的内置脚本和调试环境来取得对测试和对象属性的完全控制。

  1) QTP是一个侧重于功能的回归自动化测试工具；提供了很多插件,如: .NET的,Java的,SAP的,Terminal Emulator的等等,分别用于各自类型的产品测试。默认提供Web,ActiveX和VB。 
  
  
  
    2) QTP支持的脚本语言是VBScript,这对于测试人员来说,感觉要"舒服"得多 (如相比SilkTest采用C语言) 。VBScript毕竟是一种松散的、非严格的、普及面很广的语言。
  
  
  
    3) QTP支持录制和回放的功能。录制产生的脚本,可以拿来作为自己编写脚本的template。录制时,还支持一种lower level 功能,这个对于QTP不容易识别出来的对象有用,不过它是使用坐标来标识的,对于坐标位置频繁变动的对象,采用这种方式不可行。另外,QTP的编辑器支持两种视图: Keyword模式和Expert模式。Keyword模式想法是好的,提供一个 描述近似于原始测试用例的、跟代码无关的视图 (我基本很少用,除了查看、管理当前test中各个action的完整流程) ,而Expert就是代码视图,一般编写脚本都在这个区域。
  
  
  
    4) 一个有用的工具: Object Spy,可以用来查看Run-time object和Test object属性和方法。
  
  
  
    5) QTP通过三类属性来识别对象: a) Mandatory； b) Assitive； c) Ordinal identifiers。大部分情况下,通过对象的一些特定属性值就可以识别对象 (类型a) 。这些属性可以通过Tools->Object Identification 定义。
  
  
  
    6) Object Repository (OR) 是QTP存储对象的地方。测试脚本运行后,QTP根据测试脚本代码,从这个对象库中查找相应对象。每个Action可以对应有一个或者多个OR,也可以设置某个OR为 sharable的,这样可以供其他Action使用。注意,使用QTP录制功能时,默认将被测对象放在local OR中,可以通过 Resources->Object Respository,选择Local查看。
  
  
  
    7) 说到QTP的要点,不得不说Action。Action是QTP组织测试用例的具体形式,拥有自己的DataTable和Object Repository,支持Input和output参数。Action可以设置为share类型的,这样可以被其他test中的Action调用 (注意: QTP是不支持在一个test中调用另外一个test的,只有通过sharable action来调用) 。
  
  
  
8) 如3) 所述,一个test中,多个action的流程组织,只有通过Keyword视图查看和删除,在Expert视图中没有办法看到。

1. 调用Action可以通过菜单Insert->Call to *** 来实现。QTP提供三种类型的调用方式: a) call to new Action,在当前test中创建一个新的Action；b) call to Copy of Action；c) call to existing action,调用一个re-usable action,如果这个re-usable action来自另外一个test,将以只读的方式插入到当前test中。
2.  QTP提供excel 形式的数据表格DataTable,可以用来存放测试数据或参数。DataTable有两种类型: global 和local。QTP为DataTable提供了许多方法供存取数据,在对测试代码进行参数化的时候,这些方法非常有用。
3.  环境变量 (Environment Variables) 。在一个test中,环境变量可以被当前test中所有action共享。环境变量也有两种类型: build in 和user defined。用户自定义的环境变量可以指向一个XML文件,这样可以实现在众多test之间共享变量。
4.  QTP可以引用外部的VBS代码库,通过Settings-》Resource加入,也可以ExecuteFile命令在代码中直接执行。这种VBS库可以为所有action和test共享。
5.  QTP默认为每个test提供一个测试结果,包括Passed,Failed,Done,Warning和information几种状态类型,可以进行对结果Filter。但是,只能为每个test产生一个testing result,不能为多个testing产生一个总的testing result.
 