---
title: GetROProperty
author: wiloon
type: post
date: 2012-08-31T07:52:34+00:00
url: /?p=3977
categories:
  - Uncategorized

---


GetToProperty:Returns the value of the specified property from the test object description.

GetTOProperties:Returns the collection of properties and values used to identify the object.

GetROProperty:Returns the current value of the test object property from the object in the application.

举个例子:

假设在库中有一个对象&#8221;窗口A&#8221;,用于识别该对象的属性有2个,

一个属性是&#8221;text&#8221;,在库中记录的值是&#8221;QQQQ&#8221;.

另一个属性是&#8221;name&#8221;,记录的值是&#8221;MM&#8221;

在实际运行脚本时属性&#8221;text&#8221;的值是&#8221;PPPP&#8221;而不是&#8221;QQQQ&#8221;

那么:

Window("窗口A&#8221;).GetToProperty("text&#8221;)返回的是:&#8221;QQQQ&#8221;

Window("窗口A&#8221;).GetRoProperty("text&#8221;)返回的是:&#8221;PPPP&#8221;

Window("窗口A&#8221;).GetToProperties("text&#8221;)返回的是用于识别&#8221;窗口A&#8221;的两个属性和值的集合



RO和TO，R，就是Runtime，T就是Testtime，O就是Object。因此顾名思义，RO就是在测试执行时的对象，TO就是录制/编写测试时的对象。是同一个类在不同的时间生成的不同的实例，一般来说TO是静态的，而RO是动态的（每次执行测试都会生成新的实例）。