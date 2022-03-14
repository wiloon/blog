---
title: C++
author: "-"
date: 2011-11-03T04:40:06+00:00
url: cpp
categories:
  - C
tags:
  - C

---
## C++
## 双冒号 (::）
1、表示“域操作符”
例：声明了一个类A，类A里面声明了一个成员函数 void click()，但没有在类的声明里边给出 click 的定义，那么在类外定义 click 时，就要写成 void A::click()，表示这个 click() 函数是类A的成员函数。

```c
// .h 文件中
class OFViewHelper
{
public:
    static void setReturnKeyForAllTextFields(UIReturnKeyType lastKey, UIView* rootView);
};

void OFViewHelper::setReturnKeyForAllTextFields(UIReturnKeyType lastKey, UIView* rootView)
{
    // 这里是要执行的代码 ...
}

```

直接用在全局函数前，表示是全局函数
例：在VC中，你可以在调用API函数里，在API函数名前面加`::`
3、表示引用成员函数及变量，作用域成员运算符

```c
System::Math::Sqrt() // 相当于 System.Math.Sqrt()

```
作者：管乐_VICTOR
链接：https://www.jianshu.com/p/0c2965f59780
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。