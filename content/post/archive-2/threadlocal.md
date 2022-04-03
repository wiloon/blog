---
title: ThreadLocal
author: "-"
date: 2017-03-24T09:14:42+00:00
url: threadlocal
categories:
  - java
tags:
  - thread

---
## ThreadLocal
- 弱引用
- 避免内存溢出的操作
- 开放地址法解决hash 冲突
- 各种内部类

线程本地变量有时会简写为TLV,Thread Local Variables。

### ThreadLocal 是什么
ThreadLocal是线程的局部变量, 也就是说这个变量是线程独有的。
通常情况下,我们创建的变量是可以被任何一个线程访问并修改的。而使用ThreadLocal创建的变量只能被当前线程访问,其他线程则无法访问和修改。

变量是同一个,但是每个线程都使用同一个初始值,也就是使用同一个变量的一个新的副本,这种情况下TreadLocal就非常有用。

应用场景: 当很多线程需要多次使用同一个对象,并且需要该对象具有相同初始值的时候,最适合使用TreadLocal。

事实上,从本质上讲,就是每个线程都维持一个MAP,而这个map的key就是TreadLocal,而值就是我们set的那个值,每次线程在get的时候,都从自己的变量中取值,既然从自己的变量中取值,那就肯定不存在线程安全的问题。总体来讲,TreadLocal这个变量的状态根本没有发生变化。它仅仅是充当了一个key的角色,另外提供给每一个线程一个初始值。如果允许的话,我们自己就能实现一个这样的功能,只不过恰好JDK就已经帮助我们做了这个事情。

使用TreadLocal维护变量时,TreadLocal为每个使用该变量的线程提供独立地变量副本,所以每一个线程都可以独立地改变自己的副本,而不会影响其他线程所对应的副本。从线程的角度看,目标变量对象是线程的本地变量,这也是类名中Local所需要表达的意思。

#### TreadLocal的四个方法: 
void set(Object val),设置当前线程的线程局部变量的值
Object get () 返回当前线程所对用的线程局部变量。
void remove() 将当前线程局部变量的值删除,目的是为了减少内存的占用,线程结束后,局部变量自动被GC
Object initValue() 返回该线程局部变量的初始值,使用protected修饰,显然是为了让子类覆盖而设计的。

### ThreadLocalMap
1.  HashMap 的数据结构是数组+链表
2.  ThreadLocalMap的数据结构仅仅是数组
3.  HashMap 是通过链地址法解决hash 冲突的问题
4.  ThreadLocalMap 是通过开放地址法来解决hash 冲突的问题
5.  HashMap 里面的Entry 内部类的引用都是强引用
6.  ThreadLocalMap里面的Entry 内部类中的key 是弱引用,value 是强引用
#### 对象存放在哪里
在Java中,栈内存归属于单个线程,每个线程都会有一个栈内存,其存储的变量只能在其所属线程中可见,即栈内存可以理解成线程的私有内存。而堆内存中的对象对所有线程可见。堆内存中的对象可以被所有线程访问。

问: 那么是不是说ThreadLocal的实例以及其值存放在栈上呢？

其实不是,因为ThreadLocal实例实际上也是被其创建的类持有 (更顶端应该是被线程持有) 。而ThreadLocal的值其实也是被线程实例持有。

它们都是位于堆上,只是通过一些技巧将可见性修改成了线程可见。

### Global && Local
上面的两个修饰看似矛盾,实则不然。

Global 意思是在当前线程中,任何一个点都可以访问到ThreadLocal的值。
  
Local 意思是该线程的ThreadLocal只能被该线程访问,一般情况下其他线程访问不到。
  
用法简介
  
创建,支持泛型

ThreadLocal<String> mStringThreadLocal = new ThreadLocal<>();
  
set方法

mStringThreadLocal.set("droidyue.com");
  
get方法

mStringThreadLocal.get();

```java
private void testThreadLocal() {
      
Thread t = new Thread() {
ThreadLocal<String> mStringThreadLocal = new ThreadLocal<>();
        @Override
        public void run() {
            super.run();
            mStringThreadLocal.set("droidyue.com");
            mStringThreadLocal.get();
        }
    };
    t.start();
}
```

ThreadLocal初始值
  
为ThreadLocal设置默认的get初始值,需要重写initialValue方法,下面是一段代码,我们将默认值修改成了线程的名字

ThreadLocal<String> mThreadLocal = new ThreadLocal<String>() {
      
@Override
      
protected String initialValue() {
        
return Thread.currentThread().getName();
      
}
  
};
  
Android中的应用
  
在Android中,Looper类就是利用了ThreadLocal的特性,保证每个线程只存在一个Looper对象。

static final ThreadLocal<Looper> sThreadLocal = new ThreadLocal<Looper>();
  
private static void prepare(boolean quitAllowed) {
      
if (sThreadLocal.get() != null) {
          
throw new RuntimeException("Only one Looper may be created per thread");
      
}
      
sThreadLocal.set(new Looper(quitAllowed));
  
}
  
如何实现
  
为了更好的掌握ThreadLocal,我认为了解其内部实现是很有必要的,这里我们以set方法从起始看一看ThreadLocal的实现原理。

下面是ThreadLocal的set方法,大致意思为

首先获取当前线程
  
利用当前线程作为句柄获取一个ThreadLocalMap的对象
  
如果上述ThreadLocalMap对象不为空,则设置值,否则创建这个ThreadLocalMap对象并设置值
  
源码如下

public void set(T value) {
      
Thread t = Thread.currentThread();
      
ThreadLocalMap map = getMap(t);
      
if (map != null)
          
map.set(this, value);
      
else
          
createMap(t, value);
  
}
  
下面是一个利用Thread对象作为句柄获取ThreadLocalMap对象的代码

ThreadLocalMap getMap(Thread t) {
      
return t.threadLocals;
  
}
  
上面的代码获取的实际上是Thread对象的threadLocals变量,可参考下面代码

class Thread implements Runnable {
      
/* ThreadLocal values pertaining to this thread. This map is maintained
       
\* by the ThreadLocal class. */

    ThreadLocal.ThreadLocalMap threadLocals = null;
    

}
  
而如果一开始设置,即ThreadLocalMap对象未创建,则新建ThreadLocalMap对象,并设置初始值。

void createMap(Thread t, T firstValue) {
      
t.threadLocals = new ThreadLocalMap(this, firstValue);
  
}
  
总结: 实际上ThreadLocal的值是放入了当前线程的一个ThreadLocalMap实例中,所以只能在本线程中访问,其他线程无法访问。

对象存放在哪里
  
在Java中,栈内存归属于单个线程,每个线程都会有一个栈内存,其存储的变量只能在其所属线程中可见,即栈内存可以理解成线程的私有内存。而堆内存中的对象对所有线程可见。堆内存中的对象可以被所有线程访问。

问: 那么是不是说ThreadLocal的实例以及其值存放在栈上呢？
  
其实不是,因为ThreadLocal实例实际上也是被其创建的类持有 (更顶端应该是被线程持有) 。而ThreadLocal的值其实也是被线程实例持有。

它们都是位于堆上,只是通过一些技巧将可见性修改成了线程可见。

关于堆和栈的比较,请参考Java中的堆和栈的区别

真的只能被一个线程访问么
  
既然上面提到了ThreadLocal只对当前线程可见,是不是说ThreadLocal的值只能被一个线程访问呢？

使用InheritableThreadLocal可以实现多个线程访问ThreadLocal的值。

如下,我们在主线程中创建一个InheritableThreadLocal的实例,然后在子线程中得到这个InheritableThreadLocal实例设置的值。

private void testInheritableThreadLocal() {
      
final ThreadLocal threadLocal = new InheritableThreadLocal();
      
threadLocal.set("droidyue.com");
      
Thread t = new Thread() {
          
@Override
          
public void run() {
              
super.run();
              
Log.i(LOGTAG, "testInheritableThreadLocal =" + threadLocal.get());
          
}
      
};

    t.start();
    

}
  
上面的代码输出的日志信息为

I/MainActivity( 5046): testInheritableThreadLocal =droidyue.com
  
使用InheritableThreadLocal可以将某个线程的ThreadLocal值在其子线程创建时传递过去。因为在线程创建过程中,有相关的处理逻辑。

//Thread.java
   
private void init(ThreadGroup g, Runnable target, String name,
                        
long stackSize, AccessControlContext acc) {
          
//code goes here
          
if (parent.inheritableThreadLocals != null)
              
this.inheritableThreadLocals =
                  
ThreadLocal.createInheritedMap(parent.inheritableThreadLocals);
          
/* Stash the specified stack size in case the VM cares */
          
this.stackSize = stackSize;

        /* Set thread ID */
        tid = nextThreadID();
    

}
  
上面代码就是在线程创建的时候,复制父线程的inheritableThreadLocals的数据。

会导致内存泄露么
  
有网上讨论说ThreadLocal会导致内存泄露,原因如下

首先ThreadLocal实例被线程的ThreadLocalMap实例持有,也可以看成被线程持有。
  
如果应用使用了线程池,那么之前的线程实例处理完之后出于复用的目的依然存活
  
所以,ThreadLocal设定的值被持有,导致内存泄露。
  
上面的逻辑是清晰的,可是ThreadLocal并不会产生内存泄露,因为ThreadLocalMap在选择key的时候,并不是直接选择ThreadLocal实例,而是ThreadLocal实例的弱引用。

static class ThreadLocalMap {

/**
  
* The entries in this hash map extend WeakReference, using
  
* its main ref field as the key (which is always a
  
* ThreadLocal object). Note that null keys (i.e. entry.get()
  
* == null) mean that the key is no longer referenced, so the
  
* entry can be expunged from table. Such entries are referred to
  
* as "stale entries" in the code that follows.
  
*/
      
static class Entry extends WeakReference<ThreadLocal<?>> {
          
/*\* The value associated with this ThreadLocal. */
          
Object value;

        Entry(ThreadLocal<?> k, Object v) {
            super(k);
            value = v;
        }
    }
    

}
  
所以实际上从ThreadLocal设计角度来说是不会导致内存泄露的。关于弱引用,了解更多,请访问译文: 理解Java中的弱引用

使用场景
  
实现单个线程单例以及单个线程上下文信息存储,比如交易id等
  
实现线程安全,非线程安全的对象使用ThreadLocal之后就会变得线程安全,因为每个线程都会有一个对应的实例
  
承载一些线程相关的数据,避免在方法中来回传递参数
  
注意: Android的ThreadLocal与Java实现略有不同,但是原理是一致的。

参考文章
  
Java ThreadLocal
  
Threadlocals and memory leaks in J2EE
  
Java Thread Local – How to use and code sample
  
ThreadLocal in Java – Example Program and Tutorial

### Hash冲突怎么解决
和HashMap的最大的不同在于,ThreadLocalMap结构非常简单,没有next引用,也就是说ThreadLocalMap中解决Hash冲突的方式并非链表的方式,而是采用线性探测的方式,所谓线性探测,就是根据初始key的hashcode值确定元素在table数组中的位置,如果发现这个位置上已经有其他key值的元素被占用,则利用固定的算法寻找一定步长的下个位置,依次判断,直至找到能够存放的位置。

ThreadLocalMap解决Hash冲突的方式就是简单的步长加1或减1,寻找下一个相邻的位置。

显然ThreadLocalMap采用线性探测的方式解决Hash冲突的效率很低,如果有大量不同的ThreadLocal对象放入map中时发送冲突,或者发生二次冲突,则效率很低。

所以这里引出的良好建议是: 每个线程只存一个变量,这样的话所有的线程存放到map中的Key都是相同的ThreadLocal,如果一个线程要保存多个变量,就需要创建多个ThreadLocal,多个ThreadLocal放入Map中时会极大的增加Hash冲突的可能。

 

ThreadLocalMap的问题
ThreadLocal在ThreadLocalMap中是以一个弱引用身份被Entry中的Key引用的

由于Entry的key是弱引用,而Value是强引用。这就导致了一个问题,ThreadLocal在没有外部对象强引用时,发生GC时弱引用Key会被回收,而Value不会回收,如果创建ThreadLocal的线程一直持续运行,那么这个Entry对象中的value就有可能一直得不到回收,发生内存泄露。

为什么使用弱引用？
key 使用强引用: 引用的ThreadLocal的对象被回收了,但是ThreadLocalMap还持有ThreadLocal的强引用,如果没有手动删除,ThreadLocal不会被回收,导致Entry内存泄漏。
key 使用弱引用: 引用的ThreadLocal的对象被回收了,由于ThreadLocalMap持有ThreadLocal的弱引用,即使没有手动删除,ThreadLocal也会被回收。value在下一次ThreadLocalMap调用set,get,remove的时候会被清除。

比较两种情况,我们可以发现: 由于ThreadLocalMap的生命周期跟Thread一样长,如果都没有手动删除对应key,都会导致内存泄漏,但是使用弱引用可以多一层保障: 弱引用ThreadLocal不会内存泄漏,对应的value在下一次ThreadLocalMap调用set,get,remove的时候会被清除。
 

如何避免泄漏
既然Key是弱引用,那么我们要做的事,就是在调用ThreadLocal的get()、set()方法时完成后再调用remove方法,将Entry节点和Map的引用关系移除,这样整个Entry对象在GC Roots分析后就变成不可达了,下次GC的时候就可以被回收。

如果使用ThreadLocal的set方法之后,没有显示的调用remove方法,就有可能发生内存泄露,所以养成良好的编程习惯十分重要,使用完ThreadLocal之后,记得调用remove方法。

每个ThreadLocal只能保存一个变量副本,如果想要上线一个线程能够保存多个副本以上,就需要创建多个ThreadLocal。
ThreadLocal内部的ThreadLocalMap键为弱引用,会有内存泄漏的风险。

### 魔数0x61c88647
魔数0x61c88647与碰撞解决#
机智的读者肯定发现ThreadLocalMap并没有使用链表或红黑树去解决hash冲突的问题,而仅仅只是使用了数组来维护整个哈希表,那么重中之重的散列性要如何保证就是一个很大的考验
ThreadLocalMap通过结合三个巧妙的设计去解决这个问题: 
1.Entry的key设计成弱引用,因此key随时可能被GC (也就是失效快) ,尽量多的面对空槽
2.(单个ThreadLocal时)当遇到碰撞时,通过线性探测的开放地址法解决冲突问题
3.(多个ThreadLocal时)引入了神奇的0x61c88647,增强其的散列性,大大减少碰撞几率
之所以不用累加而用该值,笔者认为可能跟其找最近的空槽有关 (跳跃查找比自增1查找用来找空槽可能更有效一些,因为有了更多可选择的空间spreading out) ,同时也跟其良好的散列性有关
0x61c88647与黄金比例、Fibonacci 数有关,读者可参见What is the meaning of 0x61C88647 constant in ThreadLocal.java

>https://stackoverflow.com/questions/38994306/what-is-the-meaning-of-0x61c88647-constant-in-threadlocal-java
>https://web.archive.org/web/20161121124236/http://brpreiss.com/books/opus4/html/page214.html


### 链地址法和开放地址法的优缺点
开放地址法: 

容易产生堆积问题,不适于大规模的数据存储。
散列函数的设计对冲突会有很大的影响,插入时可能会出现多次冲突的现象。
删除的元素是多个冲突元素中的一个,需要对后面的元素作处理,实现较复杂。

链地址法: 

处理冲突简单,且无堆积现象,平均查找长度短。
链表中的结点是动态申请的,适合构造表不能确定长度的情况。
删除结点的操作易于实现。只要简单地删去链表上相应的结点即可。
指针需要额外的空间,故当结点规模较小时,开放定址法较为节省空间。

ThreadLocalMap 采用开放地址法原因

ThreadLocal 中看到一个属性 HASH_INCREMENT = 0x61c88647 ,0x61c88647 是一个神奇的数字,让哈希码能均匀的分布在2的N次方的数组里, 即 Entry[] table,关于这个神奇的数字google 有很多解析,这里就不重复说了
ThreadLocal 往往存放的数据量不会特别大 (而且key 是弱引用又会被垃圾回收,及时让数据量更小) ,这个时候开放地址法简单的结构会显得更省空间,同时数组的查询效率也是非常高,加上第一点的保障,冲突概率也低


https://juejin.cn/post/6844903974454329358
来源: 掘金
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

---

https://zhuanlan.zhihu.com/p/139214244  
https://droidyue.com/blog/2016/03/13/learning-threadlocal-in-java/

https://www.liaoxuefeng.com/wiki/1252599548343744/1306581251653666  
https://blog.csdn.net/Summer_And_Opencv/article/details/104632272  
https://juejin.cn/post/6844903974454329358  
