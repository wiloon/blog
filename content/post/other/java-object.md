---
title: java 对象
author: "-"
date: 2014-11-19T07:10:27+00:00
url: /?p=7023
categories:
  - Java
tags:
  - reprint
---
## java 对象

<http://www.jianshu.com/p/ebaa1a03c594>

Java程序执行时,第一步系统创建虚拟机进程,然后虚拟器用类加载器Class Loader加载java程序类文件到方法区。

方法区放哪些东西？

存放加载过的类信息、常量、静态变量、及jit编译后的代码 (类方法) 等数据的内存区域。它是线程共享的。

方法区存放的信息包括: 类的基本信息、运行时常量池、变量字段信息、方法信息等。这部分的详细介绍看下面链接的文章。

详细Java程序运行的内存结构介绍 点此处

简要过程:

类加载完成后,主线程运行static main () 时在虚拟机栈中建栈帧,压栈。

执行到new Object () 时,在堆heap里创建对象。

对象创建的过程就是堆上分配实例对象内容空间的过程,在堆中对象内存空间的具体结构如下:

对象头 这个头包括两个部分,第一部分用于存储自身运行时的数据例如GC标志位、哈希码、锁状态等信息。第二部分存放指向方法区类静态数据的指针。

实例变量 存放类的属性数据信息,包括父类的属性信息。如果是数组的实例部分还包括数组的长度。这部分内存按4字节对齐。

填充数据 这是因为虚拟机要求对象起始地址必须是8字节的整数倍。填充数据不是必须存在的,仅仅是为了字节对齐。HotSpot VM的自动内存管理要求对象起始地址必须是8字节的整数倍。对象头本身是8的倍数,当对象的实例变量数据不是8的倍数,便需要填充数据来保证8字节的对齐。另外,堆上对象内存的分配是并发进行的.

然后执行类的构造函数初始化。

Java虚拟机规范规定该区域可抛出OutOfMemoryError。

详细步骤

例如:

Dog dog= new Dog()；
  
当虚拟机执行到new指令时,它先在常量池中查找"Dog",看能否定位到Dog类的符号引用；如果能,说明这个类已经被加载到方法区了,则继续执行。如果没有,就让Class Loader先执行类的加载。

然后,虚拟机开始为该对象分配内存,对象所需要的内存大小在类加载完成后就已经确定了。这时候只要在堆中按需求分配空间即可。具体分配内存时有两种方式,第一种,内存绝对规整,那么只要在被占用内存和空闲内存间放置指针即可,每次分配空间时只要把指针向空闲内存空间移动相应距离即可,当某对象被GC回收后,则需要进行某些对象内存的迁移。第二种,空闲内存和非空闲内存夹杂在一起,那么就需要用一个列表来记录堆内存的使用情况,然后按需分配内存。

对于多线程的情况,如何确保一个线程分配了对象内存但尚未修改内存管理指针时,其他线程又分配该块内存而覆盖的情况？有一种方法,就是让每一个线程在堆中先预分配一小块内存 (TLAB本地线程分配缓冲) ,每个线程只在自己的内存中分配内存。但对象本身按其访问属性是可以线程共享访问的。

内存分配到后,虚拟机将分配的内存空间都初始化为零值(不包括对象头)。实例变量按变量类型初始化相应的默认值 (数值型为0,boolan为false) ,所以实例变量不赋初值也能使用。接着设置对象头信息,比如对象的哈希值,GC分代年龄等。

从虚拟机角度,此时一个新的对象已经创建完成了。但从我们程序运行的角度,新建对象才刚刚开始,对象的构造方法还没有执行。只有执行完构造方法,按构造方法进行初始化后,对象才是彻底创建完成了。

构造函数的执行还涉及到调用父类构造器,如果没有显式声明调用父类构造器,则自动添加默认构造器。

到此,new运算符可以返回堆中这个对象的引用了。

此刻,会根据dog这个变量是实例变量、局部变量或静态变量的不同将引用放在不同的地方:

如果dog局部变量,dog变量在栈帧的局部变量表,这个对象的引用就放在栈帧。

如果dog是实例变量,dog变量在堆中,对象的引用就放在堆。

如果dog是静态变量,dog变量在方法区,对象的引用就放在方法区。

Java有三种方法可以创建对象实例。

### new

通常都是使用java的关键字new来创建对象实例。

若有一个Something类,则可以通过下面的语句创建Something类的对象实例并指定到变量obj。

```java

Something something New = new Something()；

```

通过new创建对象实例必须把类名写在原代码里面。

### clone

若程序写成如下,则可以根据当前对象 (this) 建立一个新实例对象 (没有调用构造函数) .

```java

public class Something implements Cloneable{

private Something obj;

public Something cloneSomething()

{

try {

obj = (Something)this.clone();

// obj = (Something)clone();

} catch (CloneNotSupportedException e) {

e.printStackTrace();

}

return obj;

}

}

```

如果需要复制上面的那个obj指向的对象实例时,调用somethingNew.cloneSomething()方法就ok了。

但是为什么不直接使用somethingNew.clone()呢？

JDK中Object# clone()方法的原型是:

protected native Object clone() throws CloneNotSupportedException;

方法修饰符是protected,而不是public。这种访问的不可见性使得我们对Object#clone()方法不可见。

所以,必需重写Object的clone方法后才能使用。

```java

public Object clone()throws CloneNotSupportedException

{

Something obj;

obj= (Something)super.clone();

return obj;

}

```

值得注意的是 : 如果需要使用clone方法,必需实现java.lang.Cloneable接口,否则会抛出java.lang.CloneNotSupportedException。

另外clone方法所做的的操作是直接复制字段的内容,换句话说,这个操作并不管该字段对应的对象实例内容。

像这样字段对字段的拷贝 (field to field copy) 就成为"浅拷贝",clone方法所做的正是"浅拷贝".

3.newInstance

利用java.lang.Class类的newInstance方法,则可根据Class对象的实例,建立该Class所表示的类的对象实例。

创建Something类的对象实例可以使用下面的语句 (这样需要一个已经存在的对象实例) 。

```java

somethingNew.getClass().newInstance().

```

或者使用下面的语句 (只需要存在相应的.class文件即可)

```java

Something instance = (Something) Class.forName("cn.softkid.test.Something").newInstance();

```

如果包下不存在相应.class文件,则会抛出ClassNotFoundException。

注意 : newInstance创建对象实例的时候会调用无参的构造函数,所以必需确保类中有无参数的构造函数,否则将会

抛出java.lang.InstantiationException异常。无法进行实例化。

### 打印对象内存地址

```java
String s3 = "helloworld";
System.out.println(System.identityHashCode(s3));
```

String类重写了hashCode方法,它根据String的值来确定hashCode的值,所以只要值一样,hashCode就会一样。
identityHashCode和hashCode的区别是,identityHashCode会返回对象的hashCode,而不管对象是否重写了hashCode方法。

### Java对象结构

Java对象存储在堆 (Heap) 内存。那么一个Java对象到底包含什么呢？概括起来分为对象头、对象体和对齐字节。
几个部分的作用:

1. 对象头中的Mark Word (标记字) 主要用来表示对象的线程锁状态,另外还可以用来配合GC、存放该对象的hashCode；
2. Klass Word是一个指向方法区中Class信息的指针,意味着该对象可随时知道自己是哪个Class的实例；
3. 数组长度也是占用64位 (8字节) 的空间,这是可选的,只有当本对象是一个数组对象时才会有这个部分；
4. 对象体是用于保存对象属性和值的主体部分,占用内存空间取决于对象的属性数量和类型；
5. 对齐字是为了减少堆内存的碎片空间 (不一定准确) 。

————————————————
版权声明: 本文为CSDN博主「六吨代码」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: <https://blog.csdn.net/liudun_cool/article/details/86286872>

### Mark Word (标记字)

#### lock

2位的锁状态标记位,由于希望用尽可能少的二进制位表示尽可能多的信息,所以设置了lock标记。该标记的值不同,整个Mark Word表示的含义不同。biased_lock和lock一起,表达的锁状态含义如下:

    biased_lock       lock            状态
    0                 01              无锁
    1                 01              偏向锁
                      00              轻量级锁
                      10              重量级锁
                      11              GC标记

#### biased_lock

对象是否启用偏向锁标记,只占1个二进制位。为1时表示对象启用偏向锁,为0时表示对象没有偏向锁。lock和biased_lock共同表示对象处于什么锁状态。

#### age

4位的Java对象年龄。在GC中,如果对象在Survivor区复制一次,年龄增加1。当对象达到设定的阈值时,将会晋升到老年代。默认情况下,并行GC的年龄阈值为15,并发GC的年龄阈值为6。由于age只有4位,所以最大值为15,这就是-XX:MaxTenuringThreshold选项最大值为15的原因。

identity_hashcode: 31位的对象标识hashCode,采用延迟加载技术。调用方法System.identityHashCode()计算,并会将结果写到该对象头中。当对象加锁后 (偏向、轻量级、重量级) ,MarkWord的字节没有足够的空间保存hashCode,因此该值会移动到管程Monitor中。

thread: 持有偏向锁的线程ID。

epoch: 偏向锁的时间戳。

ptr_to_lock_record: 轻量级锁状态下,指向栈中锁记录的指针。

ptr_to_heavyweight_monitor: 重量级锁状态下,指向对象监视器Monitor的指针。

我们通常说的通过synchronized实现的同步锁,真实名称叫做重量级锁。但是重量级锁会造成线程排队 (串行执行) ,且会使CPU在用户态和核心态之间频繁切换,所以代价高、效率低。为了提高效率,不会一开始就使用重量级锁,JVM在内部会根据需要,按如下步骤进行锁的升级:

        1.初期锁对象刚创建时,还没有任何线程来竞争,对象的Mark Word是下图的第一种情形,这偏向锁标识位是0,锁状态01,说明该对象处于无锁状态 (无线程竞争它) 。

        2.当有一个线程来竞争锁时,先用偏向锁,表示锁对象偏爱这个线程,这个线程要执行这个锁关联的任何代码,不需要再做任何检查和切换,这种竞争不激烈的情况下,效率非常高。这时Mark Word会记录自己偏爱的线程的ID,把该线程当做自己的熟人。如下图第二种情形。

        3.当有两个线程开始竞争这个锁对象,情况发生变化了,不再是偏向 (独占) 锁了,锁会升级为轻量级锁,两个线程公平竞争,哪个线程先占有锁对象并执行代码,锁对象的Mark Word就执行哪个线程的栈帧中的锁记录。如下图第三种情形。

        4.如果竞争的这个锁对象的线程更多,导致了更多的切换和等待,JVM会把该锁对象的锁升级为重量级锁,这个就叫做同步锁,这个锁对象Mark Word再次发生变化,会指向一个监视器对象,这个监视器对象用集合的形式,来登记和管理排队的线程。如下图第四种情形。

### Klass Word (类指针)

这一部分用于存储对象的类型指针,该指针指向它的类元数据,JVM通过这个指针确定对象是哪个类的实例。该指针的位长度为JVM的一个字大小,即32位的JVM为32位,64位的JVM为64位。

如果应用的对象过多,使用64位的指针将浪费大量内存,统计而言,64位的JVM将会比32位的JVM多耗费50%的内存。为了节约内存可以使用选项+UseCompressedOops 开启指针压缩,其中,oop即 ordinary object pointer 普通对象指针。开启该选项后,下列指针将压缩至32位:

- 每个Class的属性指针 (即静态变量)
- 每个对象的属性指针 (即对象变量)
- 普通对象数组的每个元素指针

当然,也不是所有的指针都会压缩,一些特殊类型的指针JVM不会优化,比如指向 PermGen 的 Class 对象指针 (JDK8中指向元空间的Class对象指针)、本地变量、堆栈元素、入参、返回值和NULL指针等。

三、数组长度
如果对象是一个数组,那么对象头还需要有额外的空间用于存储数组的长度,这部分数据的长度也随着JVM架构的不同而不同: 32位的JVM上,长度为32位；64位JVM则为64位。64位JVM如果开启+UseCompressedOops选项,该区域长度也将由64位压缩至32位
————————————————
版权声明: 本文为CSDN博主「六吨代码」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: <https://blog.csdn.net/liudun_cool/article/details/86286872>
