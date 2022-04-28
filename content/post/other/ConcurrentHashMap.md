---
title: ConcurrentHashMap
author: "-"
date: 2015-08-12T02:39:42+00:00
url: ConcurrentHashMap
categories:
  - Java
tags:
  - Java

---
## ConcurrentHashMap

ConcurrentHashMap 是一个线程安全的Hash Table,它的主要功能是提供了一组和HashTable功能相同但是线程安全的方法。ConcurrentHashMap可以做到读取数据不加锁,并 且其内部的结构可以让其在进行写操作的时候能够将锁的粒度保持地尽量地小,不用对整个ConcurrentHashMap加锁。

### jdk1.7

由 Segment 数组、HashEntry 组成，和 HashMap 一样，仍然是数组加链表。
它的核心成员变量：
```java
/**
 * Segment 数组，存放数据时首先需要定位到具体的 Segment 中。
 */
final Segment<K,V>[] segments;
transient Set<K> keySet;
transient Set<Map.Entry<K,V>> entrySet;
```

Segment 是 ConcurrentHashMap 的一个内部类，主要的组成如下：

```java
   static final class Segment<K,V> extends ReentrantLock implements Serializable {
       private static final long serialVersionUID = 2249069246763182397L;
       
       // 和 HashMap 中的 HashEntry 作用一样，真正存放数据的桶
       transient volatile HashEntry<K,V>[] table;
       transient int count;
       transient int modCount;
       transient int threshold;
       final float loadFactor;
       
}
```
和 HashMap 非常类似，唯一的区别就是其中的核心数据如 value ，以及链表都是 volatile 修饰的，保证了获取时的可见性。

原理上来说：ConcurrentHashMap 采用了分段锁技术，其中 Segment 继承于 ReentrantLock。不会像 HashTable 那样不管是 put 还是 get 操作都需要做同步处理，理论上 ConcurrentHashMap 支持 CurrencyLevel (Segment 数组数量)的线程并发。每当一个线程占用锁访问一个 Segment 时，不会影响到其他的 Segment。

下面也来看看核心的 put get 方法。

### put 方法
```java

public V put(K key, V value) {
    Segment<K,V> s;
    if (value == null)
        throw new NullPointerException();
    int hash = hash(key);
    int j = (hash >>> segmentShift) & segmentMask;
    if ((s = (Segment<K,V>)UNSAFE.getObject          // nonvolatile; recheck
         (segments, (j << SSHIFT) + SBASE)) == null) //  in ensureSegment
        s = ensureSegment(j);
    return s.put(key, hash, value, false);
}
```
首先是通过 key 定位到 Segment，之后在对应的 Segment 中进行具体的 put。
```java
final V put(K key, int hash, V value, boolean onlyIfAbsent) {
    HashEntry<K,V> node = tryLock() ? null : scanAndLockForPut(key, hash, value);
    V oldValue;
    try {
        HashEntry<K,V>[] tab = table;
        int index = (tab.length - 1) & hash;
        HashEntry<K,V> first = entryAt(tab, index);
        for (HashEntry<K,V> e = first;;) {
            if (e != null) {
                K k;
                if ((k = e.key) == key ||
                    (e.hash == hash && key.equals(k))) {
                    oldValue = e.value;
                    if (!onlyIfAbsent) {
                        e.value = value;
                        ++modCount;
                    }
                    break;
                }
                e = e.next;
            }
            else {
                if (node != null)
                    node.setNext(first);
                else
                    node = new HashEntry<K,V>(hash, key, value, first);
                int c = count + 1;
                if (c > threshold && tab.length < MAXIMUM_CAPACITY)
                    rehash(node);
                else
                    setEntryAt(tab, index, node);
                ++modCount;
                count = c;
                oldValue = null;
                break;
            }
        }
    } finally {
        unlock();
    }
    return oldValue;
}
```
虽然 HashEntry 中的 value 是用 volatile 关键词修饰的，但是并不能保证并发的原子性，所以 put 操作时仍然需要加锁处理。

首先第一步的时候会尝试获取锁，如果获取失败肯定就有其他线程存在竞争，则利用 scanAndLockForPut() 自旋获取锁。

尝试自旋获取锁。
如果重试的次数达到了 MAX_SCAN_RETRIES 则改为阻塞锁获取，保证能获取成功。

将当前 Segment 中的 table 通过 key 的 hashcode 定位到 HashEntry。
遍历该 HashEntry，如果不为空则判断传入的 key 和当前遍历的 key 是否相等，相等则覆盖旧的 value。
不为空则需要新建一个 HashEntry 并加入到 Segment 中，同时会先判断是否需要扩容。
最后会解除在 1 中所获取当前 Segment 的锁。
### get 方法
```java
public V get(Object key) {
    Segment<K,V> s; // manually integrate access methods to reduce overhead
    HashEntry<K,V>[] tab;
    int h = hash(key);
    long u = (((h >>> segmentShift) & segmentMask) << SSHIFT) + SBASE;
    if ((s = (Segment<K,V>)UNSAFE.getObjectVolatile(segments, u)) != null &&
        (tab = s.table) != null) {
        for (HashEntry<K,V> e = (HashEntry<K,V>) UNSAFE.getObjectVolatile
                 (tab, ((long)(((tab.length - 1) & h)) << TSHIFT) + TBASE);
             e != null; e = e.next) {
            K k;
            if ((k = e.key) == key || (e.hash == h && key.equals(k)))
                return e.value;
        }
    }
    return null;
}
```
get 逻辑比较简单：

只需要将 Key 通过 Hash 之后定位到具体的 Segment ，再通过一次 Hash 定位到具体的元素上。

由于 HashEntry 中的 value 属性是用 volatile 关键词修饰的，保证了内存可见性，所以每次获取时都是最新值。

ConcurrentHashMap 的 get 方法是非常高效的，因为整个过程都不需要加锁。

### jdk1.8
1.7 已经解决了并发问题，并且能支持 N 个 Segment 这么多次数的并发，但依然存在 HashMap 在 1.7 版本中的问题。

那就是查询遍历链表效率太低。

因此 1.8 做了一些数据结构上的调整。
其中抛弃了原有的 Segment 分段锁，而采用了 CAS + synchronized 来保证并发安全性。
```java
    static class Node<K,V> implements Map.Entry<K,V> {
        final int hash;
        final K key;
        volatile V val;
        volatile Node<K,V> next;

        Node(int hash, K key, V val, Node<K,V> next) {
            this.hash = hash;
            this.key = key;
            this.val = val;
            this.next = next;
        }

        public final K getKey()       { return key; }
        public final V getValue()     { return val; }
        public final int hashCode()   { return key.hashCode() ^ val.hashCode(); }
        public final String toString(){ return key + "=" + val; }
        public final V setValue(V value) {
            throw new UnsupportedOperationException();
        }
```
也将 1.7 中存放数据的 HashEntry 改为 Node，但作用都是相同的。

其中的 val next 都用了 volatile 修饰，保证了可见性。

### put
```java
final V putVal(K key, V value, boolean onlyIfAbsent) {
        if (key == null || value == null) throw new NullPointerException();
        int hash = spread(key.hashCode()); // 1 算hashcode
        int binCount = 0;
        for (Node<K,V>[] tab = table;;) {
            Node<K,V> f; int n, i, fh;
            if (tab == null || (n = tab.length) == 0) // 2 判断是否需要进行初始化。
                tab = initTable();
            else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) { // 3, 根据hash定位 node, 如果没找到node，就cas写入数据
                if (casTabAt(tab, i, null,
                             new Node<K,V>(hash, key, value, null)))
                    break;                   // no lock when adding to empty bin
            }
            else if ((fh = f.hash) == MOVED) // 4 扩容
                tab = helpTransfer(tab, f);
            else {
                V oldVal = null;
                synchronized (f) { // 5 写入数据
                    if (tabAt(tab, i) == f) {
                        if (fh >= 0) {
                            binCount = 1;
                            for (Node<K,V> e = f;; ++binCount) {
                                K ek;
                                if (e.hash == hash &&
                                    ((ek = e.key) == key ||
                                     (ek != null && key.equals(ek)))) {
                                    oldVal = e.val;
                                    if (!onlyIfAbsent)
                                        e.val = value;
                                    break;
                                }
                                Node<K,V> pred = e;
                                if ((e = e.next) == null) {
                                    pred.next = new Node<K,V>(hash, key,
                                                              value, null);
                                    break;
                                }
                            }
                        }
                        else if (f instanceof TreeBin) {
                            Node<K,V> p;
                            binCount = 2;
                            if ((p = ((TreeBin<K,V>)f).putTreeVal(hash, key,
                                                           value)) != null) {
                                oldVal = p.val;
                                if (!onlyIfAbsent)
                                    p.val = value;
                            }
                        }
                    }
                }
                if (binCount != 0) {
                    if (binCount >= TREEIFY_THRESHOLD) //6 转红黑树？
                        treeifyBin(tab, i);
                    if (oldVal != null)
                        return oldVal;
                    break;
                }
            }
        }
        addCount(1L, binCount);
        return null;
    }
```

1. 根据 key 计算出 hashcode 。
2. 判断是否需要进行初始化。
3. f 即为当前 key 定位出的 Node，如果为空表示当前位置可以写入数据，利用 CAS 尝试写入，失败则自旋保证成功。
4. 如果当前位置的 hashcode == MOVED == -1,则需要进行扩容。
5. 如果都不满足，则利用 synchronized 锁写入数据。
6. 如果数量大于 TREEIFY_THRESHOLD 则要转换为红黑树。

### get 方法
根据计算出来的 hashcode 寻址，如果就在桶上那么直接返回值。
如果是红黑树那就按照树的方式获取值。
就不满足那就按照链表的方式遍历获取值。
1.8 在 1.7 的数据结构上做了大的改动，采用红黑树之后可以保证查询效率 (O(logn)），甚至取消了 ReentrantLock 改为了 synchronized，这样可以看出在新版的 JDK 中对 synchronized 优化是很到位的。

---

#### ConcurrentHashMap的内部结构
ConcurrentHashMap 为了提高本身的并发能力,在内部采用了一个叫做Segment的结构,一个Segment其实就是一个类Hash Table的结构,Segment内部维护了一个链表数组

从上面的结构我们可以了解到,ConcurrentHashMap定位一个元素的过程需要进行两次Hash操作,第一次Hash定位到Segment,第二次Hash定位到元素所在的链表的头部,因此,这一种结构的带来的副作用是Hash的过程要比普通的HashMap要 长,但是带来的好处是写操作的时候可以只对元素所在的Segment进行加锁即可,不会影响到其他的Segment,这样,在最理想的情况 下,ConcurrentHashMap可以最高同时支持Segment数量大小的写操作 (刚好这些写操作都非常平均地分布在所有的Segment上) , 所以,通过这一种结构,ConcurrentHashMap的并发能力可以大大的提高。
### volatile

和 HashMap 非常类似，唯一的区别就是其中的核心数据如 value ，以及链表都是 volatile 修饰的，保证了获取时的可见性。

```java
    static class Node<K,V> implements Map.Entry<K,V> {
        final int hash;
        final K key;
        volatile V val;
        volatile Node<K,V> next;
        //...
```


#### jdk 1.7 Segment
我们再来具体了解一下Segment的数据结构: 

```java
static final class Segment<K,V> extends ReentrantLock implements Serializable {
    transient volatile int count;
    transient int modCount;
    transient int threshold;
    transient volatile HashEntry<K,V>[] table;
    final float loadFactor;
}
```

原理上来说：ConcurrentHashMap 采用了分段锁技术，其中 Segment 继承于 ReentrantLock。不会像 HashTable 那样不管是 put 还是 get 操作都需要做同步处理，理论上 ConcurrentHashMap 支持 CurrencyLevel (Segment 数组数量)的线程并发。每当一个线程占用锁访问一个 Segment 时，不会影响到其他的 Segment。


详细解释一下Segment里面的成员变量的意义: 

count: Segment中元素的数量
  
modCount: 对table的大小造成影响的操作的数量 (比如put或者remove操作) 
  
threshold: 阈值,Segment里面元素的数量超过这个值依旧就会对Segment进行扩容
  
table: 链表数组,数组中的每一个元素代表了一个链表的头部
  
loadFactor: 负载因子,用于确定threshold
  
HashEntry
  
Segment中的元素是以HashEntry的形式存放在链表数组中的,看一下HashEntry的结构: 

```java
static final class HashEntry<K,V> {
    final K key;
    final int hash;
    volatile V value;
    final HashEntry<K,V> next;
}
``` 
可以看到HashEntry的一个特点,除了value以外,其他的几个变量都是final的,这样做是为了防止链表结构被破坏,出现ConcurrentModification的情况。

#### ConcurrentHashMap的初始化
下面我们来结合源代码来具体分析一下ConcurrentHashMap的实现,先看下初始化方法: 

public ConcurrentHashMap(int initialCapacity,float loadFactor, int concurrencyLevel) {
  
if (!(loadFactor > 0) || initialCapacity < 0 || concurrencyLevel <= 0)
  
throw new IllegalArgumentException();

if (concurrencyLevel > MAX_SEGMENTS)
  
concurrencyLevel = MAX_SEGMENTS;

// Find power-of-two sizes best matching arguments
  
int sshift = 0;
  
int ssize = 1;
  
while (ssize < concurrencyLevel) {
  
++sshift;
  
ssize <<= 1;
  
}
  
segmentShift = 32 - sshift;
  
segmentMask = ssize - 1;
  
this.segments = Segment.newArray(ssize);

if (initialCapacity > MAXIMUM_CAPACITY)
  
initialCapacity = MAXIMUM_CAPACITY;
  
int c = initialCapacity / ssize;
  
if (c * ssize < initialCapacity)
  
++c;
  
int cap = 1;
  
while (cap < c)
  
cap <<= 1;

for (int i = 0; i < this.segments.length; ++i)
  
this.segments[i] = new Segment<K,V>(cap, loadFactor);
  
}
  
CurrentHashMap 的初始化一共有三个参数,一个initialCapacity,表示初始的容量,一个loadFactor,表示负载参数,最后一个是 concurrentLevel,代表ConcurrentHashMap内部的Segment的数量,ConcurrentLevel一经指定,不可改 变,后续如果ConcurrentHashMap的元素数量增加导致ConrruentHashMap需要扩容,ConcurrentHashMap不会 增加Segment的数量,而只会增加Segment中链表数组的容量大小,这样的好处是扩容过程不需要对整个ConcurrentHashMap做 rehash,而只需要对Segment里面的元素做一次rehash就可以了。

整 个ConcurrentHashMap的初始化方法还是非常简单的,先是根据concurrentLevel来new出Segment,这里 Segment的数量是不大于concurrentLevel的最大的2的指数,就是说Segment的数量永远是2的指数个,这样的好处是方便采用移位 操作来进行hash,加快hash的过程。接下来就是根据intialCapacity确定Segment的容量的大小,每一个Segment的容量大小 也是2的指数,同样使为了加快hash的过程。

这 边需要特别注意一下两个变量,分别是segmentShift和segmentMask,这两个变量在后面将会起到很大的作用,假设构造函数确定了 Segment的数量是2的n次方,那么segmentShift就等于32减去n,而segmentMask就等于2的n次方减一。

ConcurrentHashMap的get操作
  
前面提到过ConcurrentHashMap的get操作是不用加锁的,我们这里看一下其实现: 


public V get(Object key) {
  
int hash = hash(key.hashCode());
  
return segmentFor(hash).get(key, hash);
  
}
  
看第三行,segmentFor这个函数用于确定操作应该在哪一个segment中进行,几乎对ConcurrentHashMap的所有操作都需要用到这个函数,我们看下这个函数的实现: 


final Segment<K,V> segmentFor(int hash) {
  
return segments[(hash >>> segmentShift) & segmentMask];
  
}
  
这 个函数用了位操作来确定Segment,根据传入的hash值向右无符号右移segmentShift位,然后和segmentMask进行与操作,结合 我们之前说的segmentShift和segmentMask的值,就可以得出以下结论: 假设Segment的数量是2的n次方,根据元素的hash值 的高n位就可以确定元素到底在哪一个Segment中。

在确定了需要在哪一个segment中进行操作以后,接下来的事情就是调用对应的Segment的get方法: 


V get(Object key, int hash) {
  
if (count != 0) { // read-volatile
  
HashEntry<K,V> e = getFirst(hash);
  
while (e != null) {
  
if (e.hash == hash && key.equals(e.key)) {
  
V v = e.value;
  
if (v != null)
  
return v;
  
return readValueUnderLock(e); // recheck
  
}
  
e = e.next;
  
}
  
}
  
return null;
  
}
  
先看第二行代码,这里对count进行了一次判断,其中count表示Segment中元素的数量,我们可以来看一下count的定义: 


transient volatile int count;
  
可以看到count是volatile的,实际上这里里面利用了volatile的语义: 


写道
  
对volatile字段的写入操作happens-before于每一个后续的同一个字段的读操作。
  
因为实际上put、remove等操作也会更新count的值,所以当竞争发生的时候,volatile的语义可以保证写操作在读操作之前,也就保证了写操作对后续的读操作都是可见的,这样后面get的后续操作就可以拿到完整的元素内容。

然后,在第三行,调用了getFirst()来取得链表的头部: 


HashEntry<K,V> getFirst(int hash) {
  
HashEntry<K,V>[] tab = table;
  
return tab[hash & (tab.length - 1)];
  
}
  
同样,这里也是用位操作来确定链表的头部,hash值和HashTable的长度减一做与操作,最后的结果就是hash值的低n位,其中n是HashTable的长度以2为底的结果。

在 确定了链表的头部以后,就可以对整个链表进行遍历,看第4行,取出key对应的value的值,如果拿出的value的值是null,则可能这个 key,value对正在put的过程中,如果出现这种情况,那么就加锁来保证取出的value是完整的,如果不是null,则直接返回value。

ConcurrentHashMap的put操作
  
看完了get操作,再看下put操作,put操作的前面也是确定Segment的过程,这里不再赘述,直接看关键的segment的put方法: 


V put(K key, int hash, V value, boolean onlyIfAbsent) {
  
lock();
  
try {
  
int c = count;
  
if (c++ > threshold) // ensure capacity
  
rehash();
  
HashEntry<K,V>[] tab = table;
  
int index = hash & (tab.length - 1);
  
HashEntry<K,V> first = tab[index];
  
HashEntry<K,V> e = first;
  
while (e != null && (e.hash != hash || !key.equals(e.key)))
  
e = e.next;

V oldValue;
  
if (e != null) {
  
oldValue = e.value;
  
if (!onlyIfAbsent)
  
e.value = value;
  
}
  
else {
  
oldValue = null;
  
++modCount;
  
tab[index] = new HashEntry<K,V>(key, hash, first, value);
  
count = c; // write-volatile
  
}
  
return oldValue;
  
} finally {
  
unlock();
  
}
  
}
  
首先对Segment的put操作是加锁完成的,然后在第五行,如果Segment中元素的数量超过了阈值 (由构造函数中的loadFactor算出) 这需要进行对Segment扩容,并且要进行rehash,关于rehash的过程大家可以自己去了解,这里不详细讲了。

第8和第9行的操作就是getFirst的过程,确定链表头部的位置。

第11行这里的这个while循环是在链表中寻找和要put的元素相同key的元素,如果找到,就直接更新更新key的value,如果没有找到,则进入21行这里,生成一个新的HashEntry并且把它加到整个Segment的头部,然后再更新count的值。

ConcurrentHashMap的remove操作
  
Remove操作的前面一部分和前面的get和put操作一样,都是定位Segment的过程,然后再调用Segment的remove方法: 


V remove(Object key, int hash, Object value) {
  
lock();
  
try {
  
int c = count - 1;
  
HashEntry<K,V>[] tab = table;
  
int index = hash & (tab.length - 1);
  
HashEntry<K,V> first = tab[index];
  
HashEntry<K,V> e = first;
  
while (e != null && (e.hash != hash || !key.equals(e.key)))
  
e = e.next;

V oldValue = null;
  
if (e != null) {
  
V v = e.value;
  
if (value == null || value.equals(v)) {
  
oldValue = v;
  
// All entries following removed node can stay
  
// in list, but all preceding ones need to be
  
// cloned.
  
++modCount;
  
HashEntry<K,V> newFirst = e.next;
  
for (HashEntry<K,V> p = first; p != e; p = p.next)
  
newFirst = new HashEntry<K,V>(p.key, p.hash,
  
newFirst, p.value);
  
tab[index] = newFirst;
  
count = c; // write-volatile
  
}
  
}
  
return oldValue;
  
} finally {
  
unlock();
  
}
  
}
  
首 先remove操作也是确定需要删除的元素的位置,不过这里删除元素的方法不是简单地把待删除元素的前面的一个元素的next指向后面一个就完事了,我们 之前已经说过HashEntry中的next是final的,一经赋值以后就不可修改,在定位到待删除元素的位置以后,程序就将待删除元素前面的那一些元 素全部复制一遍,然后再一个一个重新接到链表上去,看一下下面这一幅图来了解这个过程: 

假设链表中原来的元素如上图所示,现在要删除元素3,那么删除元素3以后的链表就如下图所示: 

ConcurrentHashMap的size操作
  
在 前面的章节中,我们涉及到的操作都是在单个Segment中进行的,但是ConcurrentHashMap有一些操作是在多个Segment中进行,比 如size操作,ConcurrentHashMap的size操作也采用了一种比较巧的方式,来尽量避免对所有的Segment都加锁。

前 面我们提到了一个Segment中的有一个modCount变量,代表的是对Segment中元素的数量造成影响的操作的次数,这个值只增不减,size 操作就是遍历了两次Segment,每次记录Segment的modCount值,然后将两次的modCount进行比较,如果相同,则表示期间没有发生 过写入操作,就将原先遍历的结果返回,如果不相同,则把这个过程再重复做一次,如果再不相同,则就需要将所有的Segment都锁住,然后一个一个遍历 了,具体的实现大家可以看ConcurrentHashMap的源码,这里就不贴了。

>https://crossoverjie.top/2018/07/23/java-senior/ConcurrentHashMap/
http://www.iteye.com/topic/1103980
http://blog.csdn.net/imzoer/article/details/8621074
https://crossoverjie.top/2018/07/23/java-senior/ConcurrentHashMap/
>wiloon.com/hashmap