---
title: GetROProperty
author: "-"
date: 2012-08-31T07:52:34+00:00
url: /?p=3977
categories:
  - Uncategorized

---
## GetROProperty

GetToProperty:Returns the value of the specified property from the test object description.

GetTOProperties:Returns the collection of properties and values used to identify the object.

GetROProperty:Returns the current value of the test object property from the object in the application.

举个例子:

假设在库中有一个对象"窗口A",用于识别该对象的属性有2个,

一个属性是"text",在库中记录的值是"QQQQ".

另一个属性是"name",记录的值是"MM"

在实际运行脚本时属性"text"的值是"PPPP"而不是"QQQQ"

那么:

Window("窗口A").GetToProperty("text")返回的是:"QQQQ"

Window("窗口A").GetRoProperty("text")返回的是:"PPPP"

Window("窗口A").GetToProperties("text")返回的是用于识别"窗口A"的两个属性和值的集合


RO和TO，R，就是Runtime，T就是Testtime，O就是Object。因此顾名思义，RO就是在测试执行时的对象，TO就是录制/编写测试时的对象。是同一个类在不同的时间生成的不同的实例，一般来说TO是静态的，而RO是动态的（每次执行测试都会生成新的实例) 。