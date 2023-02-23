---
title: Java JUC Atomic
author: "-"
date: 2013-06-03T08:04:37+00:00
url: Atomic
categories:
  - Inbox
tags:
  - reprint
---
## Java JUC Atomic

Java从JDK1.5开始提供了java.util.concurrent.atomic包,方便程序员在多线程环境下,无锁的进行原子操作。原子变量的底层使用了处理器提供的原子指令,但是不同的CPU架构可能提供的原子指令不一样,也有可能需要某种形式的内部锁,所以该方法不能绝对保证线程不被阻塞。
  
在Atomic包里一共有12个类,四种原子更新方式,分别是原子更新基本类型,原子更新数组,原子更新引用和原子更新字段。Atomic包里的类基本都是使用Unsafe实现的包装类。

基本类: AtomicInteger、AtomicLong、AtomicBoolean；
  
引用类型: AtomicReference、AtomicReference的ABA实例、AtomicStampedRerence、AtomicMarkableReference；
  
数组类型: AtomicIntegerArray、AtomicLongArray、AtomicReferenceArray
  
属性原子修改器 (Updater) : AtomicIntegerFieldUpdater、AtomicLongFieldUpdater、AtomicReferenceFieldUpdater

看到这么多类,你是否觉得很困惑,其实没什么,因为你只需要看懂一个,其余的方法和使用都是大同小异的,相关的类会介绍他们之间的区别在哪里,在使用中需要注意的地方即可。

在使用Atomic系列前,我们需要先知道一个东西就是Unsafe类,全名为: sun.misc.Unsafe,这个类包含了大量的对C代码的操作,包括很多直接内存分配以及原子操作的调用,而它之所以标记为非安全的,是告诉你这个里面大量的方法调用都会存在安全隐患,需要小心使用,否则会导致严重的后果,例如在通过unsafe分配内存的时候,如果自己指定某些区域可能会导致一些类似C++一样的指针越界到其他进程的问题,不过它的具体使用并不是本文的重点,本文重点是Atomic系列的内容大多会基于unsafe类中的以下几个本地方法来操作:

public final native boolean compareAndSwapObject(Object obj,long Fieldoffset, Object expect, Object update);
  
public final native boolean compareAndSwapInt(Object paramObject, long paramLong, int paramInt1, int paramInt2);

对象的引用进行对比后交换,交换成功返回true,交换失败返回false,这个交换过程完全是原子的,在CPU上计算完结果后,都会对比内存的结果是否还是原先的值,若不是,则认为不能替换,因为变量是volatile类型所以最终写入的数据会被其他线程看到,所以一个线程修改成功后,其他线程就发现自己修改失败了。

参数1: 被操作的对象

参数2: fieldoffset 被操作的域在对象中的偏移量,其实对比时是对比内存单元,所以需要属性的起始位置,而引用就是修改引用地址 (根据OS、VM位数和参数配置决定宽度一般是4-8个字节) ,int就是修改相关的4个字节,而long就是修改相关的8个字节。

获取偏移量也是通过unsafe的一个方法: objectFieldOffset(Fieldfield)来获取属性在对象中的偏移量；静态变量需要通过: staticFieldOffset(Field field)获取,调用的总方法是: fieldOffset(Fieldfield)

参数3: expect 域的期望值
  
参数4: update 域的更新值

对long的操作,要看VM是否支持对Long的CAS,因为有可能VM本身不支持,若不支持,此时运算会变成Lock方式,不过现在VM都基本是支持的而已。

public final native boolean compareAndSwapLong(Object paramObject, long paramLong1, long paramLong2, long paramLong3);

我们不推荐直接使用unsafe来操作原子变量,而是通过Java封装好的一些类来操作原子变量。

实例代码1: AtomicIntegerTest.java

```java
  
import java.util.concurrent.atomic.AtomicInteger;
  
public class AtomicIntegerTest { 

/**
       
* 常见的方法列表
       
* @see AtomicInteger#get() 直接返回值
       
* @see AtomicInteger#getAndAdd(int) 增加指定的数据,返回变化前的数据
       
* @see AtomicInteger#getAndDecrement() 减少1,返回减少前的数据
       
* @see AtomicInteger#getAndIncrement() 增加1,返回增加前的数据
       
* @see AtomicInteger#getAndSet(int) 设置指定的数据,返回设置前的数据
       
*
       
* @see AtomicInteger#addAndGet(int) 增加指定的数据后返回增加后的数据
       
* @see AtomicInteger#decrementAndGet() 减少1,返回减少后的值
       
* @see AtomicInteger#incrementAndGet() 增加1,返回增加后的值
       
* @see AtomicInteger#lazySet(int) 仅仅当get时才会set
       
*
       
* @see AtomicInteger#compareAndSet(int, int) 尝试新增后对比,若增加成功则返回true否则返回false
       
*/
      
public final static AtomicInteger TEST_INTEGER = new AtomicInteger(1); 

public static void main(String []args) throws InterruptedException {
          
final Thread []threads = new Thread[10];
           
for(int i = 0 ; i < 10 ; i++) {
               
final int num = i;
               
threads[i] = new Thread() {
                   
public void run() {
                       
try {
                          
Thread.sleep(1000);
                      
} catch (InterruptedException e) {
                          
e.printStackTrace();
                      
}
                      
int now = TEST_INTEGER.incrementAndGet();
                      
System.out.println("我是线程: " + num + ",我得到值了,增加后的值为: " + now);
                   
}
               
};
               
threads[i].start();
           
}
           
for(Thread t : threads) {
               
t.join();
           
}
           
System.out.println("最终运行结果: " + TEST_INTEGER.get());
      
}
  
}
  
```

代码例子中模拟多个线程并发对AtomicInteger进行增加1的操作,如果这个数据是普通类型,那么增加过程中出现的问题就是两个线程可能同时看到的数据都是同一个数据,增加完成后写回的时候,也是同一个数据,但是两个加法应当串行增加1,也就是加2的操作,甚至于更加特殊的情况是一个线程加到3后,写入,另一个线程写入了2,还越变越少,也就是不能得到正确的结果,在并发下,我们模拟计数器,要得到精确的计数器值,就需要使用它,我们希望得到的结果是11,可以拷贝代码进去运行后看到结果的确是11,虽然输出的顺序可能不一样,也同时可以证明线程的确是并发运行的 (只是在输出的时候,征用System.out这个对象也不一定是谁先抢到) ,但是最终结果的确是11。

相信你对AtomicInteger的使用有一些了解了吧,要知道更多的方法使用,请参看这段代码中定义变量位置的注释,有关于AtomicInteger的相关方法的详细注释,可以直接跟踪进去看源码,注释中使用了简单的描述说明了方法的用途。

而对于AtomicLong呢,其实和AtomicInteger差不多,唯一的区别就是它处理的数据是long类型的就是了；

对于AtomicBoolean呢,方法要少一些,常见的方法就两个:

AtomicBoolean#compareAndSet(boolean, boolean) 第一个参数为原始值,第二个参数为要修改的新值,若修改成功则返回true,否则返回false
  
AtomicBoolean#getAndSet(boolean) 尝试设置新的boolean值,直到成功为止,返回设置前的数据

因为boolean值就两个值,所以就是来回改,相对的很多增加减少的方法自然就没有了,对于使用来讲,我们列举一个boolean的并发修改,仅有一个线程可以修改成功的例子:

实例代码2: AtomicBooleanTest.java

```java
  
import java.util.concurrent.atomic.AtomicBoolean; 

public class AtomicBooleanTest { 

/**
       
* 主要方法: 
       
* @see AtomicBoolean#compareAndSet(boolean, boolean) 第一个参数为原始值,第二个参数为要修改的新值,若修改成功则返回true,否则返回false
       
* @see AtomicBoolean#getAndSet(boolean) 尝试设置新的boolean值,直到成功为止,返回设置前的数据
       
*/
      
public final static AtomicBoolean TEST_BOOLEAN = new AtomicBoolean(); 

public static void main(String []args) {
          
for(int i = 0 ; i < 10 ; i++) {
              
new Thread() {
                  
public void run() {
                      
try {
                          
Thread.sleep(1000);
                      
} catch (InterruptedException e) {
                          
e.printStackTrace();
                      
}
                      
if(TEST_BOOLEAN.compareAndSet(false, true)) {
                          
System.out.println("我成功了！");
                      
}
                  
}
              
}.start();
          
}
      
}
  
}
  
```

这里有10个线程,我们让他们几乎同时去征用boolean值的修改,修改成功者输出: 我成功了！此时你运行完你会发现只会输出一个"我成功了！",说明征用过程中达到了锁的效果。

那么几种基本类型就说完了,我们来看看里面的实现是不是如我们开始说的Unsafe那样,看几段源码即可,我们看下AtomicInteger的一些源码,例如开始用的: incrementAndGet方法,这个,它的源码是:

public final int incrementAndGet() {

for (;;) {

int current = get();

int next = current + 1;

if (compareAndSet(current, next))

return next;

}
  
}

可以看到内部有一个死循环,只有不断去做compareAndSet操作,直到成功为止,也就是修改的根本在compareAndSet方法里面,可以去看下相关的修改方法均是这样实现,那么看下compareAndSet方法的body部分是:

public final boolean compareAndSet(int expect, int update) {

return unsafe.compareAndSwapInt(this, valueOffset, expect, update);
  
}

可以看到这里使用了unsafe的compareAndSwapInt的方法,很明显this就是指AtomicInteger当前的这个对象 (这个对象不用像上面说的它不能是static和final,它无所谓的) ,而valueOffset的定义是这样的:

private static final long valueOffset;

static {

try {

valueOffset = unsafe.objectFieldOffset(AtomicInteger.class.getDeclaredField("value"));

} catch (Exception ex) {

throw new Error(ex);
  
}
  
}
  
可以看出是通过我们前面所述的objectFieldOffset方法来获取的属性偏移量,所以你自己如果定义类似的操作的时候,就要注意,这个属性不能是静态的,否则不能用这个方法来获取

后面两个参数自然是对比值和需要修改的目标对象的地址。

其实Atomic系列你看到这里,java层面你就知道差不多了,其余的就是特殊用法和包装而已,刚才我们说了unsafe的3个方法无非是地址和值的区别在内存层面是没有本质区别的,因为地址本身也是数字值。

为了说明这个问题,我们就先说Reference的使用:

我们测试一个reference,和boolean测试方式一样,也是测试多个线程只有一个线程能修改它。

实例代码1: AtomicReferenceTest.java

```java
  
import java.util.concurrent.atomic.AtomicReference; 

public class AtomicReferenceTest { 

/**
       
* 相关方法列表
       
* @see AtomicReference#compareAndSet(Object, Object) 对比设置值,参数1: 原始值,参数2: 修改目标引用
       
* @see AtomicReference#getAndSet(Object) 将引用的目标修改为设置的参数,直到修改成功为止,返回修改前的引用
       
*/
      
public final static AtomicReference <String>ATOMIC_REFERENCE = new AtomicReference<String>("abc"); 

public static void main(String []args) {
          
for(int i = 0 ; i < 100 ; i++) {
              
final int num = i;
              
new Thread() {
                  
public void run() {
                      
try {
                          
Thread.sleep(Math.abs((int)(Math.random() * 100)));
                      
} catch (InterruptedException e) {
                          
e.printStackTrace();
                      
}
                      
if(ATOMIC_REFERENCE.compareAndSet("abc", new String("abc"))) {
                          
System.out.println("我是线程: " + num + ",我获得了锁进行了对象修改！");
                      
}
                  
}
              
}.start();
          
}
      
}
  
}
  
```

测试结果如我们所料,的确只有一个线程,执行,跟着代码: compareAndSet进去,发现源码中的调用是:

public final boolean compareAndSet(V expect, V update) {

return unsafe.compareAndSwapObject(this, valueOffset, expect, update);
  
}

**ABA问题**
  
OK,的确和我们上面所讲一致,那么此时我们又遇到了引用修改的新问题,什么问题呢？ABA问题,什么是ABA问题呢,当某些流程在处理过程中是顺向的,也就是不允许重复处理的情况下,在某些情况下导致一个数据由A变成B,再中间可能经过0-N个环节后变成了A,此时A不允许再变成B了,因为此时的状态已经发生了改变,例如: 银行资金里面做一批账目操作,要求资金在80-100元的人,增加20元钱,时间持续一天,也就是后台程序会不断扫描这些用户的资金是否是在这个范围,但是要求增加过的人就不能再增加了,如果增加20后,被人取出10元继续在这个范围,那么就可以无限套现出来,就是ABA问题了,类似的还有抢红包或中奖,比如每天每个人限量3个红包,中那个等级的奖的个数等等。

此时我们需要使用的方式就不是简单的compareAndSet操作,因为它仅仅是考虑到物理上的并发,而不是在业务逻辑上去控制顺序,此时我们需要借鉴数据库的事务序列号的一些思想来解决,假如每个对象修改的次数可以记住,修改前先对比下次数是否一致再修改,那么这个问题就简单了,AtomicStampedReference类正是提供这一功能的,其实它仅仅是在AtomicReference类的再一次包装,里面增加了一层引用和计数器,其实是否为计数器完全由自己控制,大多数我们是让他自增的,你也可以按照自己的方式来标示版本号,下面一个例子是ABA问题的简单演示:

实例代码3 (ABA问题模拟代码演示) :

```java
  
import java.util.concurrent.atomic.AtomicReference; 

/**
   
* ABA问题模拟,线程并发中,导致ABA问题,解决方案是使用|AtomicMarkableReference
   
* 请参看相应的例子: AtomicStampedReferenceTest、AtomicMarkableReferenceTest
   
*
   
*/
  
public class AtomicReferenceABATest { 

public final static AtomicReference <String>ATOMIC_REFERENCE = new AtomicReference<String>("abc"); 

public static void main(String []args) {
          
for(int i = 0 ; i < 100 ; i++) {
              
final int num = i;
              
new Thread() {
                  
public void run() {
                      
try {
                          
Thread.sleep(Math.abs((int)(Math.random() * 100)));
                      
} catch (InterruptedException e) {
                          
e.printStackTrace();
                      
}
                      
if(ATOMIC_REFERENCE.compareAndSet("abc" , "abc2")) {
                          
System.out.println("我是线程: " + num + ",我获得了锁进行了对象修改！");
                      
}
                  
}
              
}.start();
          
}
          
new Thread() {
              
public void run() {
                  
while(!ATOMIC_REFERENCE.compareAndSet("abc2", "abc"));
                  
System.out.println("已经改为原始值！");
              
}
          
}.start();
      
}
  
}
  
```

代码中和原来的例子,唯一的区别就是最后增加了一个线程让他将数据修改为原来的值,并一直尝试修改,直到修改成功为止,为什么没有直接用: 方法呢getAndSet方法呢,因为我们的目的是要让某个线程先将他修改为abc2后再让他修改回abc,所以需要这样做；

此时我们得到的结果是:

我是线程: 0,我获得了锁进行了对象修改！, abc>abc2
  
已经改为原始值！, abc2>abc
  
我是线程: 83,我获得了锁进行了对象修改！, abc>abc2

当然你的线程编号多半和我不一样,只要征用到就对,可以发现,有两个线程修改了这个字符串,我们是想那一堆将abc改成abc2的线程仅有一个成功,即使其他线程在他们征用时将其修改为abc,也不能再修改。

此时我们通过类来AtomicStampedReference解决这个问题:
  
实例代码4 (AtomicStampedReference解决ABA问题) :

[code lang=text]
  
import java.util.concurrent.atomic.AtomicStampedReference;

public class AtomicStampedReferenceTest {

public final static AtomicStampedReference <String>ATOMIC_REFERENCE = new AtomicStampedReference<String>("abc" , 0);

public static void main(String []args) {

for(int i = 0 ; i < 100 ; i++) {

final int num = i;

final int stamp = ATOMIC_REFERENCE.getStamp();

new Thread() {

public void run() {

try {

Thread.sleep(Math.abs((int)(Math.random() * 100)));

} catch (InterruptedException e) {

e.printStackTrace();

}

if(ATOMIC_REFERENCE.compareAndSet("abc" , "abc2" , stamp , stamp + 1)) {

System.out.println("我是线程: " + num + ",我获得了锁进行了对象修改！");

}

}

}.start();

}

new Thread() {

public void run() {

int stamp = ATOMIC_REFERENCE.getStamp();

while(!ATOMIC_REFERENCE.compareAndSet("abc2", "abc" , stamp , stamp + 1));

System.out.println("已经改回为原始值！");

}

}.start();

}
  
}
  
```

此时再运行程序看到的结果就是我们想要的了,发现将abc修改为abc2的线程仅有一个被访问,虽然被修改回了原始值,但是其他线程也不会再将abc改为abc2。

而类: AtomicMarkableReference和AtomicStampedReference功能差不多,有点区别的是: 它描述更加简单的是与否的关系,通常ABA问题只有两种状态,而AtomicStampedReference是多种状态,那么为什么还要有AtomicMarkableReference呢,因为它在处理是与否上面更加具有可读性,而AtomicStampedReference过于随意定义状态,并不便于阅读大量的是和否的关系,它可以被认为是一个计数器或状态列表等信息,java提倡通过类名知道其意义,所以这个类的存在也是必要的,它的定义就是将数据变换为true|false如下: 

public final static AtomicMarkableReference <String>ATOMIC_MARKABLE_REFERENCE = new AtomicMarkableReference<String>("abc" , false);

操作时使用: 
  
ATOMIC_MARKABLE_REFERENCE.compareAndSet("abc", "abc2", false, true);

好了,reference的三个类的种类都介绍了,我们下面要开始说Atomic的数组用法,因为我们开始说到的都是一些简单变量和基本数据,操作数组呢？如果你来设计会怎么设计,Atomic的数组要求不允许修改长度等,不像集合类那么丰富的操作,不过它可以让你的数组上每个元素的操作绝对安全的,也就是它细化的力度还是到数组上的元素,为你做了二次包装,所以如果你来设计,就是在原有的操作上增加一个下标访问即可,我们来模拟一个Integer类型的数组,即: AtomicIntegerArray

实例代码5 (AtomicIntegerArrayTest.java) 

```java
  
import java.util.concurrent.atomic.AtomicIntegerArray; 

public class AtomicIntegerArrayTest { 

/**
       
* 常见的方法列表
       
* @see AtomicIntegerArray#addAndGet(int, int) 执行加法,第一个参数为数组的下标,第二个参数为增加的数量,返回增加后的结果
       
* @see AtomicIntegerArray#compareAndSet(int, int, int) 对比修改,参数1: 数组下标,参数2: 原始值,参数3,修改目标值,修改成功返回true否则false
       
* @see AtomicIntegerArray#decrementAndGet(int) 参数为数组下标,将数组对应数字减少1,返回减少后的数据
       
* @see AtomicIntegerArray#incrementAndGet(int) 参数为数组下标,将数组对应数字增加1,返回增加后的数据
       
*
       
* @see AtomicIntegerArray#getAndAdd(int, int) 和addAndGet类似,区别是返回值是变化前的数据
       
* @see AtomicIntegerArray#getAndDecrement(int) 和decrementAndGet类似,区别是返回变化前的数据
       
* @see AtomicIntegerArray#getAndIncrement(int) 和incrementAndGet类似,区别是返回变化前的数据
       
* @see AtomicIntegerArray#getAndSet(int, int) 将对应下标的数字设置为指定值,第二个参数为设置的值,返回是变化前的数据
       
*/
      
private final static AtomicIntegerArray ATOMIC_INTEGER_ARRAY = new AtomicIntegerArray(new int[]{1,2,3,4,5,6,7,8,9,10}); 

public static void main(String []args) throws InterruptedException {
          
Thread []threads = new Thread[100];
          
for(int i = 0 ; i < 100 ; i++) {
              
final int index = i % 10;
              
final int threadNum = i;
              
threads[i] = new Thread() {
                  
public void run() {
                      
int result = ATOMIC_INTEGER_ARRAY.addAndGet(index, index + 1);
                      
System.out.println("线程编号为: " + threadNum + " , 对应的原始值为: " + (index + 1) + ",增加后的结果为: " + result);
                  
}
              
};
              
threads[i].start();
          
}
          
for(Thread thread : threads) {
              
thread.join();
          
}
          
System.out.println("=========================>\n执行已经完成,结果列表: ");
          
for(int i = 0 ; i < ATOMIC_INTEGER_ARRAY.length() ; i++) {
              
System.out.println(ATOMIC_INTEGER_ARRAY.get(i));
          
}
      
}
  
}
  
```

计算结果说明: 100个线程并发,每10个线程会被并发修改数组中的一个元素,也就是数组中的每个元素会被10个线程并发修改访问,每次增加原始值的大小,此时运算完的结果看最后输出的敲好为原始值的11倍数,和我们预期的一致,如果不是线程安全那么这个值什么都有可能。

而相应的类: AtomicLongArray其实和AtomicIntegerArray操作方法类似,最大区别就是它操作的数据类型是long；而AtomicReferenceArray也是这样,只是它方法只有两个:

AtomicReferenceArray#compareAndSet(int, Object, Object)
  
参数1: 数组下标；
  
参数2: 修改原始值对比；
  
参数3: 修改目标值
  
修改成功返回true,否则返回false

AtomicReferenceArray#getAndSet(int, Object)
  
参数1: 数组下标
  
参数2: 修改的目标
  
修改成功为止,返回修改前的数据

到这里你是否对数组内部的操作应该有所了解了,和当初预期一样,参数就是多了一个下标,为了完全验证这点,跟踪到源码中可以看到:

public final int addAndGet(int i, int delta) {

while (true) {

int current = get(i);

int next = current + delta;

if (compareAndSet(i, current, next))

return next;

}

}

可以看到根据get(i)获取到对应的数据,然后做和普通AtomicInteger差不多的操作,get操作里面有个细节是:

public final int get(int i) {

return unsafe.getIntVolatile(array, rawIndex(i));
  
}
  
这里通过了unsafe获取基于volatile方式获取 (可见性) 获取一个int类型的数据,而获取的位置是由rawIndex来确定,它的源码是:

private long rawIndex(int i) {

if (i < 0 || i >= array.length)

throw new IndexOutOfBoundsException("index " + i);

return base + (long) i * scale;
  
}

可以发现这个结果是一个地址位置,为base加上一个偏移量,那么看看base和scale的定义为:

private static final int base = unsafe.arrayBaseOffset(int[].class);
  
private static final int scale = unsafe.arrayIndexScale(int[].class);

可以发现unsafe里面提供了对数组base的位置的获取,因为对象是有头部的,而数组还有一个长度位置,第二个很明显是一个数组元素所占用的宽度,也就是基本精度；这里应该可以体会到unsafe所带来的强大了吧。

### Updater, AtomicIntegerFieldUpdater

AtomicXXXFieldUpdater可以以一种线程安全的方式操作非线程安全对象的某些字段。

本文最后要介绍的部分为Updater也就是修改器,它算是Atomic的系列的一个扩展,Atomic系列是为你定义好的一些对象,你可以使用,但是如果是别人已经在使用的对象会原先的代码需要修改为Atomic系列,此时若全部修改类型到对应的对象相信很麻烦,因为牵涉的代码会很多,此时java提供一个外部的Updater可以对对象的属性本身的修改提供类似Atomic的操作,也就是它对这些普通的属性的操作是并发下安全的,分别由: AtomicIntegerFieldUpdater、AtomicLongFieldUpdater、AtomicReferenceUpdater,这样操作后,系统会更加灵活,也就是可能那些类的属性只是在某些情况下需要控制并发,很多时候不需要,但是他们的使用通常有以下几个限制:

限制1: 操作的目标不能是 static 类型,前面说到 unsafe 的已经可以猜测到它提取的是非 static 类型的属性偏移量,如果是 static 类型在获取时如果没有使用对应的方法是会报错的,而这个 Updater 并没有使用对应的方法。
  
限制2: 操作的目标不能是 final 类型的,因为 final 根本没法修改。
  
限制3: 必须是 volatile 类型的数据,也就是数据本身是读一致的。
  
限制4: 属性必须对当前的 Updater 所在的区域是可见的,也就是 private 如果不是当前类肯定是不可见的,protected 如果不存在父子关系也是不可见的,default如果不是在同一个package下也是不可见的。

实现方式: 通过反射找到属性,对属性进行操作,但是并不是设置 accessable,所以必须是可见的属性才能操作。

说了这么多,来个实例看看吧。

### 实例代码6:  (AtomicIntegerFieldUpdaterTest.java)

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.atomic.AtomicIntegerFieldUpdater;

public class AtomicIntegerFieldUpdaterTest {
    private static final Logger logger = LoggerFactory.getLogger(AtomicIntegerFieldUpdaterTest.class);

    static class A {
        volatile int intValue = 100;
    }

    public final static AtomicIntegerFieldUpdater<A> ATOMIC_INTEGER_UPDATER = AtomicIntegerFieldUpdater.newUpdater(A.class, "intValue");

    public static void main(String[] args) {
        final A a = new A();
        for (int i = 0; i < 100; i++) {
            final int num = i;
            new Thread() {
                public void run() {
                    if (ATOMIC_INTEGER_UPDATER.compareAndSet(a, 100, 120)) {
                        logger.info("我是线程: " + num + ", changed intValue");
                    } else {
                        logger.info("thread: {}, change intValue failed", num);
                    }
                }
            }.start();
        }
    }
}
```

此时你会发现只有一个线程可以对这个数据进行修改,其他的方法如上面描述一样,实现的功能和 AtomicInteger 类似。

而AtomicLongFieldUpdater其实也是这样,区别在于它所操作的数据是long类型。

AtomicReferenceFieldUpdater方法较少,主要是compareAndSet以及getAndSet两个方法的使用,它的定义比数字类型的多一个参数如下:

static class A {

volatile String stringValue = "abc";
  
}

AtomicReferenceFieldUpdater ATOMIC_REFERENCE_FIELD_UPDATER = AtomicReferenceFieldUpdater.newUpdater(A.class, String.class, "stringValue");

可以看到,这里传递的参数增加了一个属性的类型,因为引用的是一个对象,对象本身也有一个类型。

### Java中的Atomic包使用指南
<http://blog.csdn.net/xieyuooo/article/details/8594713>
><https://segmentfault.com/a/1190000015864724>
