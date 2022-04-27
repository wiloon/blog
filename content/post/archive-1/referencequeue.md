---
title: ReferenceQueue
author: "-"
date: 2015-06-26T14:11:54+00:00
url: ReferenceQueue
categories:
  - Java
tags:
  - Java

---
## ReferenceQueue

引用队列 ReferenceQueue
使用SoftReference，WeakReference，PhantomReference 的时候，可以关联一个ReferenceQueue。那么当垃圾回收器准备回收一个被引用包装的对象时，该引用会被加入到关联的ReferenceQueue。程序可以通过判断引用队列中是否已经加入引用,来了解被引用的对象是否被GC回收。

作者: leilifengxingmw
链接: <https://www.jianshu.com/p/6ae4f53a4752>
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

<http://www.iflym.com/index.php/java-programe/201407140001.html>

在java的引用体系中，存在着强引用，软引用，虚引用，幽灵引用，这4种引用类型。在正常的使用过程中，我们定义的类型都是强引用的，这种引用类型在回收中，只有当其它对象没有对这个对象的引用时，才会被GC回收掉。简单来说，对于以下定义:

Object obj = new Object();
  
Ref ref = new Ref(obj);
  
在这种情况下，如果ref没有被GC，那么obj这个对象肯定不会GC的。因为ref引用到了obj。如果obj是一个大对象呢，多个这种对象的话，应用肯定一会就挂掉了。

那么，如果我们希望在这个体系中，如果obj没有被其它对象引用，只是在这个Ref中存在引用时，就把obj对象gc掉。这时候就可以使用这里提到的Reference对象了。

我们希望当一个对象被gc掉的时候通知用户线程，进行额外的处理时，就需要使用引用队列了。ReferenceQueue即这样的一个对象，当一个obj被gc掉之后，其相应的包装类，即ref对象会被放入queue中。我们可以从queue中获取到相应的对象信息，同时进行额外的处理。比如反向操作，数据清理等。

2 使用队列进行数据监控

一个简单的例子，通过往map中放入10000个对象，每个对象大小为1M字节数组。使用引用队列监控被放入的key的回收情况。代码如下所示:

Object value = new Object();
  
Map<Object, Object> map = new HashMap<>();
  
for(int i = 0;i < 10000;i++) {
  
byte[] bytes = new byte[_1M];
  
WeakReference<byte[]> weakReference = new WeakReference<byte[]>(bytes, referenceQueue);
  
map.put(weakReference, value);
  
}
  
System.out.println("map.size->" + map.size());
  
这里使用了weakReference对象，即当值不再被引用时，相应的数据被回收。另外使用一个线程不断地从队列中获取被gc的数据，代码如下:

Thread thread = new Thread(() -> {
  
try {
  
int cnt = 0;
  
WeakReference<byte[]> k;
  
while((k = (WeakReference) referenceQueue.remove()) != null) {
  
System.out.println((cnt++) + "回收了:" + k);
  
}
  
} catch(InterruptedException e) {
  
//结束循环
  
}
  
});
  
thread.setDaemon(true);
  
thread.start();
  
结果如下所示:

9992回收了:java.lang.ref.WeakReference@1d13cd4
  
9993回收了:java.lang.ref.WeakReference@118b73a
  
9994回收了:java.lang.ref.WeakReference@1865933
  
9995回收了:java.lang.ref.WeakReference@ad82c
  
map.size->10000
  
在这次处理中，map并没有因为不断加入的1M对象由产生OOM异常，并且最终运行结果之后map中的确有1万个对象。表示确实被放入了相应的对象信息。不过其中的key(即weakReference)对象中的byte[]对象却被回收了。即不断new出来的1M数组被gc掉了。

从命令行中，我们看到有9995个对象被gc，即意味着在map的key中，除了weakReference之外，没有我们想要的业务对象。那么在这样的情况下，是否意味着这9995个entry，我们认为就是没有任何意义的对象，那么是否可以将其移除掉呢。同时还期望size值可以打印出5，而不是10000.
  
WeakHashMap就是这样的一个类似实现。

3 在类weakHashMap中的使用

weakHashMap即使用weakReference当作key来进行数据的存储，当key中的引用被gc掉之后，它会自动(类似自动)的方式将相应的entry给移除掉，即我们会看到size发生了变化。

从简单来看，我们认为其中所有一个类似的机制从queue中获取引用信息，从而使得被gc掉的key值所对应的entry从map中被移除。这个处理点就在我们调用weakhashmap的各个处理点中，比如get,size,put等。简单点来说，就是在调用get时，weakHashMap会先处理被gc掉的key值，然后再处理我们的业务调用。

简单点代码如下:

public int size() {
  
if (size == 0)
  
return 0;
  
expungeStaleEntries();
  
return size;
  
}
  
此处的expungeStaleEntries即移除方法，具体的逻辑可以由以下的流程来描述:

A:使用一个继承于WeakReference的entry对象表示每一个kv对，其中的原引用对象即我们在放入map中的key值
  
B:为保证效率以及尽可能的不使用key值，hash经过预先计算。这样在定位数据及重新get时不再需要使用原引用对象
  
C:由queue拿到的事件对象，即这里的entry值。通过entry定位到具体的桶位置，通过链表计算将entry的前后重新连接起来(即p.pre.next = p.next)
  
因此，这里的引用处理并不是自动的，其实是我们在调用某些方法的时候处理，所以我们认为它不是一种自动的，只是表面上看起来是这种处理。
  
具体的代码，即将开始的map定义为一个WeakHashMap，最终的输出类似如下所示:

9993回收了:java.lang.ref.WeakReference@12aa816
  
9994回收了:java.lang.ref.WeakReference@2bd967
  
9995回收了:java.lang.ref.WeakReference@13e9593
  
weakHashMap.size->4
  
在上面的代码中，由于weakhashmap不允许自定义queue，所以上面的监控是针对value的。在weakHashMap中，queue在weakhashmap在内部定义，并且由内部消化使用了。如果我们在自己进一步处理，那就只能自定义类似weakHashMap实现，或者使用反向操作。即在监控到变化之后，自己处理map的kv。

4 队列监控的反向操作

反向操作，即意味着一个数据变化了，可以通过weakReference对象反向拿相关的数据，从而进行业务的处理。比如，我们可以通过继承weakReference对象，加入自定义的字段值，额外处理。一个类似weakHashMap如下，这时，我们不再将key值作为弱引用处理，而是封装在weakReference对象中，以实现额外的处理。

WeakR对象定义如下:

//描述一种强key关系的处理，当value值被回收之后，我们可以通过反向引用将key从map中移除的做法
  
//即通过在weakReference中加入其所引用的key值，以获取key信息，再反向移除map信息
  
class WeakR extends WeakReference<byte[]> {
  
private Object key;
  
WeakR(Object key, byte[] referent, ReferenceQueue<? super byte[]> q) {
  
super(referent, q);
  
this.key = key;
  
}
  
}
  
那么，相应的map，我们就使用普通的hashMap，将weakR作为value进行存储，如下所示:

final Map<Object, WeakR> hashMap = new HashMap<>();
  
for(int i = 0;i < 10000;i++) {
  
byte[] bytesKey = new byte[_1M];
  
byte[] bytesValue = new byte[_1M];
  
hashMap.put(bytesKey, new WeakR(bytesKey, bytesValue, referenceQueue));
  
}
  
相应的队列，我们则一样地进行监控，不同的是，我们对获取的WeakR对象进行了额外的处理，如下所示:

int cnt = 0;
  
WeakR k;
  
while((k = (WeakR) referenceQueue.remove()) != null) {
  
System.out.println((cnt++) + "回收了:" + k);
  
//触发反向hash remove
  
hashMap.remove(k.key);
  
//额外对key对象作其它处理，比如关闭流，通知操作等
  
}
  
其实就是拿到反向引用的key值(这里的value已经不存在了)，因为kv映射已没有意义，将其从map中移除掉。同时，我们还可以作其它的操作(具体的操作还没想到，嘿嘿)

这个也可以理解为就是一个类似cache的实现。
  
在cache中，key不重要并且通常都很少，value才是需要对待的。这里通过监控value变化，反向修改map，以达到控制kv的目的，避免出现无用的kv映射。

相应的输出，如下所示:

9995回收了:com.m_ylf.study.java.reference.TestCase$1WeakR@13c5f83
  
9996回收了:com.m_ylf.study.java.reference.TestCase$1WeakR@197558c
  
9997回收了:com.m_ylf.study.java.reference.TestCase$1WeakR@164bc7e
  
hashMap.size->1
  
5 在google guava的简单描述

在google guava中，实现了一个类似在第4中所对应的操作。同时对于反向操作，通过继承一个指定的对象(可以理解为weakReference和callback的组合对象)，当value值被gc之后，即可以直接在回调中处理业务即可，不需要自己来监控queue。 (见FinalizableReference)

转载请标明出处:i flym
  
本文地址:<http://www.iflym.com/index.php/java-programe/201407140001.html>
