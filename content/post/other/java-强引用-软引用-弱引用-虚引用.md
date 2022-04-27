---
title: Java 强引用, 软引用, 弱引用, 虚引用
author: "-"
date: 2013-11-17T07:59:05+00:00
url: /?p=5973
categories:
  - java
tags:
  - reference

---
## Java 强引用, 软引用, 弱引用, 虚引用

强引用 StrongReference

强引用是使用最普遍的引用。如果一个对象具有强引用，那垃圾回收器绝不会回收它。当内存空间不足，Java虚拟机宁愿抛出OutOfMemoryError错误，使程序异常终止，也不会靠随意回收具有强引用的对象来解决内存不足的问题。

Object o=new Object(); // 强引用
  
如果不使用时，要通过如下方式来弱化引用，如下:

o=null; // 帮助垃圾收集器回收此对象
  
显式地设置o为null，或超出对象的生命周期范围，则gc认为该对象不存在引用，这时就可以回收这个对象。具体什么时候收集这要取决于gc的算法。

在一个方法的内部有一个强引用，这个引用保存在栈中，而真正的引用内容 (Object) 保存在堆中。当这个方法运行完成后就会退出方法栈，则引用内容的引用不存在，这个Object会被回收。

但是如果这个o是全局的变量时，就需要在不用这个对象时赋值为null，因为强引用不会被垃圾回收。

强引用在实际中有非常重要的用处，举个ArrayList的实现源代码:

private transient Object[] elementData;
  
public void clear() {

modCount++;

// Let gc do its work

for (int i = 0; i < size; i++)

elementData[i] = null;

size = 0;
  
}
  
在ArrayList类中定义了一个私有的变量elementData数组，在调用方法清空数组时可以看到为每个数组内容赋值为null。不同于elementData=null，强引用仍然存在，避免在后续调用 add()等方法添加元素时进行重新的内存分配。使用如clear()方法中释放内存的方法对数组中存放的引用类型特别适用，这样就可以及时释放内存。

软引用 SoftReference

如果内存空间足够，垃圾回收器就不会回收它，如果内存空间不足了，就会回收这些对象的内存。只要垃圾回收器没有回收它，该对象就可以被程序使用。软引用可用来实现内存敏感的高速缓存。
  
它兼有了StrongReference和WeakReference的好处，既能停留在内存中，又能在内存不足时去处理。

String str=new String("abc"); // 强引用
  
SoftReference<String> softRef=new SoftReference<String>(str); // 软引用

虚引用 PhantomReference

虚引用和弱引用比较像，在任何时候都可能被垃圾回收器回收。虚引用主要用来跟踪对象被垃圾回收器回收的活动。虚引用与软引用和弱引用的一个区别在于: 虚引用必须和引用队列  (ReferenceQueue) 联合使用。当垃圾回收器准备回收一个对象时，如果发现它还有虚引用，就会在回收对象的内存之前，把这个虚引用加入到与之关联的引用队列中。
  
ReferenceQueue queue = new ReferenceQueue ();
  
PhantomReference pr = new PhantomReference (object, queue);
  
程序可以通过判断引用队列中是否已经加入了虚引用，来了解被引用的对象是否将要被垃圾回收。如果程序发现某个虚引用已经被加入到引用队列，那么就可以在所引用的对象的内存被回收之前采取必要的行动。

### 弱引用 WeakReference

弱引用的定义是: 如果一个对象仅被一个弱引用指向，那么当下一次GC到来时，这个对象一定会被垃圾回收器回收掉。  
生命周期只能存活到下次GC前  
类似于可有可无的东西。在垃圾回收器线程扫描它所管辖的内存区域的过程中，一旦发现了只具有弱引用的对象，不管当前内存空间足够与否，都会回收它的内存
  
栈里的句柄到堆里的对象的弱引用WeakReference, 在被程序使用时, 可以通过引用找到对象, 在被GC找到时, 就相当于不可达的对象, 可以回收。

String str=new String("abc");
  
WeakReference<String> abcWeakRef = new WeakReference<String>(str);
  
str=null;
  
WeakHashMap类，这个类和哈希表HashMap几乎一样，但就是在键 key的地方使用了WeakReference
  
弱引用与软引用的区别在于: 具有 WeakReference 的对象拥有更短暂的生命周期。

---

<http://blog.csdn.net/matthewei6/article/details/12839327>

<http://speed847.iteye.com/blog/374006>

<http://droidyue.com/blog/2014/10/12/understanding-weakreference-in-java/>
  
<http://blog.csdn.net/mxbhxx/article/details/9111711>
