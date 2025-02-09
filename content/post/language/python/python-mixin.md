---
title: python mixin
author: "-"
date: 2012-04-25T14:15:38+00:00
url: python/mixin
categories:
  - Python
tags:
  - reprint
---
## python mixin

什么是Mixin设计模式
mixin设计模式可以看做是多继承的一种。那么首先，咱们谈谈为什么会出现多继承这种语法。

汽车和飞机他们都同属于交通工具，但飞机可以飞行，汽车无法做到，所以，飞行这个行为不能写到交通工具这个类中，如果每一个交通工具各自实现自己的行驶方法，就违背了代码尽可能重用的原则(如果交通工具种类越来越多，就会造成大量代码冗余)。

所以，我们要表示飞行这个行为，就需要进行多继承。但这样，我们就违背了继承关系必须是is-a原则。

在java中，虽然没有多继承，但我们可以通过interface来实现多继承。

在python中，没有interface这一语法，但它本身是支持多继承的。

在使用多继承的时候，很容易就会设计不当，导致继承链混乱，影响mro查找，所以，在编程的时候我们的原则就是，能使用其他方法代替多继承就尽量不适用多继承。

这个时候Mixin设计模式就应运而生，Mixin直译理解就是混入、补充的意思，它是多继承的一种。在多继承中，查找顺序是按mro继承链中的顺序进行的。
这样一来，我们不需要复杂而庞大的继承链，只要选择组合不同的类的功能，就可以快速构造出所需的子类。

2.Mixin设计模式实例
class Vehicle:
pass

class PlaneMixin:
def fly(self):
print("Flying")

class Airplane(Vehicle, PlaneMixin):
pass

可以看到，上述代码中，Airplane类实现了多继承，在继承链上，它继承了Vehicle类和PlaneMixin类，这里我们遵循Mixin设计模式的要求，在后面添加上后缀Mixin增强代码的可读性。

上述代码可以这么理解，Airplane只是一个Vehicle类，而不是Plane类，而Mixin后缀，它告诉其他读者，这个类是作为功能添加到子类中的，并不是作为父类，它的作用等同于Java中的interface。

3. 使用Mixin设计模式的原则
   在使用Mixin设计模式实现多重继承的时候要特别注意下列几点原则：

首先，Mixin类必须表示某一种功能，而不是某一个物体，这点跟java中的Runnable和Callable是一样的。
其次，它表示的责任必须单一，如果有多个功能，我们应该去实现多个Mixin类。
接下来，Mixin类不依赖于子类的实现,且属于抽象类，本身不能实例化，也不能继承Mixin以外的类。
最后，子类即使没有继承Mixin类，也必须照常工作，只是部分功能缺少无法使用。
Java的接口，只提供了“规格”的多重继承。Mixin类则同时提供了“规格”和“实现”的多重继承，使用上相比接口会更加简单。

4. 补充
   在其他框架或者语言中，也有类似的Mixin功能，如Ruby，Django，Vue, React等等。
   ————————————————

                            版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

原文链接：https://blog.csdn.net/u011544909/article/details/106890774