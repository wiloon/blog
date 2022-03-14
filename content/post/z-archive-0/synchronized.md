---
title: synchronized
author: "-"
date: 2012-10-16T06:16:48+00:00
url: synchronized
categories:
  - Java
tags:
  - lock

---
## synchronized
### 多线程
在现代计算机中往往存在多个CPU核心，而1个CPU能同时运行一个线程，为了充分利用CPU多核心，提高CPU的效率，多线程就应时而生了。
那么多线程就一定比单线程快吗? 答案是不一定，因为多线程存在单线程没有的问题
#### 上下文切换
线程执行过程中发生**系统调用**或者**线程调度**时都会发生上下文切换
线程从运行状态切换到阻塞状态或者等待状态的时候需要将线程的运行状态保存，线程从阻塞状态或者等待状态切换到运行状态的时候需要加载线程上次运行的状态。线程的运行状态从保存到再加载就是一次上下文切换，而上下文切换的开销是非常大的，而我们知道CPU给每个线程分配的时间片很短，通常是几十毫秒(ms)，那么线程的切换就会很频繁。
#### 死锁
死锁的一般场景是，线程A和线程B都在互相等待对方释放锁，死锁会造成系统不可用。
#### 资源限制的挑战
资源限制指计算机硬件资源或软件资源限制了多线程的运行速度，例如某个资源的下载速度是1Mb/s，资源的服务器带宽只有2Mb/s，那么开10个线程下载资源并不会将下载速度提升到10Mb/s。
既然多线程存在这些问题，那么我们在开发的过程中有必要使用多线程吗？我们知道任何技术都有它存在的理由，总而言之就是多线程利大于弊，只要我们合理使用多线程就能达到事半功倍的效果。
多线程的意思就是多个线程同时工作，那么多线程之间如何协同合作，这也就是我们需要解决的**线程通信**、**线程同步**问题
##### 线程通信
线程通信指线程之间以何种机制来交换消息，线程之间的通信机制有两种: 共享内存和消息传递。共享内存即线程通过对共享变量的读写而达到隐式通信，消息传递即线程通过发送消息给对方显示的进行通信。
##### 线程同步
线程同步指不同线程对同一个资源进行操作时候线程应该以什么顺序去操作，线程同步依赖于线程通信，以共享内存方式进行线程通信的线程同步是显式的，以消息传递方式进行线程通信的线程同步是隐式的。

### synchronized
synchronized 的锁机制的主要优势是Java语言内置的锁机制，因此，JVM可以自由的优化而不影响已存在的代码。

synchronized 是 Java 的关键字，可用于同步实例方法、类方法(静态方法)和代码块
- 同步实例方法: 当 synchronized 修饰实例方法 (函数修饰符）的时候，同步的范围是当前实例的实例方法。
- 同步类方法(静态方法): 当 synchronized 修饰类方法的时候，同步的范围是当前类的方法。用synchronized修饰方法名时，编译后会在方法名上生成一个ACC_SYNCHRONIZED标识来实现同步
- 同步代码块: 当 synchronized 修饰代码块的时候，同步的范围是()中的对象。当使用synchronized修饰代码块时，编译后会在代码块的前后生成monitorenter和monitorexit字节码来实现同步。

synchronized 是非公平锁

synchronized 关键字经过编译之后，会在同步块的前后分别形成 monitorenter 和 monitorexit 这两个字节码指令，这两个字节码需要关联到一个监视对象，当线程执行 monitorenter 指令时，需要首先获得获得监视对象的锁，这里监视对象锁就是进入同步块的凭证，只有获得了凭证才可以进入同步块，当线程离开同步块时，会执行 monitorexit 指令，释放对象锁。

synchronized 关键字，代表这个方法加锁,相当于不管哪一个线程 (例如线程A) ，运行到这个方法时, 都要检查有没有其它线程B (或者C、 D等) 正在用这个方法，有的话要等正在使用 synchronized 方法的线程B (或者C 、D) 运行完这个方法后再运行此线程 A,没有的话,直接运行。

### markword
markword数据的长度在32位和64位的虚拟机 (未开启压缩指针) 中分别为32bit和64bit，它的最后2bit是锁状态标志位，用来标记当前对象的状态，对象的所处的状态，决定了markword存储的内容

java 对象都拥有对象头这一数据结构来支持锁, 但是对于较大的对象系统开销会更大一些.

java中的每一个对象都至少包含2个字 (2*4 Bytes for 32bits & 2*8 Bytes for 64bits, 不包括已压缩的对象) 。
第一个字被称为 Mark Word。这是一个对象的头，它包含了不同的信息，包括锁的相关信息

第二个字是指向 metadata class 的指针, metadata class字义了对象的类型。这部分也包含了VMT (Virtual Method Table) 

### Mark Word 的结构
Mark Word 根据最低两位 (Tag) 的所表示的状态，编码了不同的信息。
如果这个对象没有被用作锁，Mark Word 记录了hashcode和对象年龄 (for GC/survivors) 。
除此之外，有3种状态对应锁: 偏向锁, 轻量级锁, 重量级锁。

重量级锁是悲观锁的一种，自旋锁、轻量级锁与偏向锁属于乐观锁

### 轻量级锁
所有现代JVM都引入了轻量级锁: 避免将每个对象关联操作系统的 mutex/condition 变量  (重量级锁) 

当不存在锁竞争时，使用原子操作(CAS)来进入退出同步块

如果发生锁竞争，回退到操作系统的重量级锁

引入轻量级锁会提高锁效率，因为大部分锁都不存在竞争。

### 轻量级锁的加锁过程
1. 当线程访问同步块，先判断锁状态标志位，如果是00，则说明是轻量级锁，JVM会先在当前线程栈帧中分配 Lock Record 空间；
2. 将锁对象头中的 Mark Word 拷贝到当前线程的 Lock Record 中，称为 Displaced Mark Word，然后使用 CAS，将对象头中的 Mark Word 修改为指向当前线程栈中 Lock Record 的指针。如果成功，则获取轻量级锁，执行同步块中的代码，如果失败，则进行自旋竞争锁，自旋达到一定的次数如果依旧没有获取到锁，则升级为重量级锁 (因为自旋会消耗CPU，为了避免无用的自旋，一旦锁升级为重量级锁，就不会恢复到轻量级锁，自旋的线程会被挂起阻塞住) ；
3. 执行完同步代码块代码，退出同步代码块，使用CAS开始轻量级锁解锁，解锁的条件需要满足以下两个: 
- 对象头Mark Word中锁记录指针是否依旧指向当前线程Lock Record  (可能已经被其他线程修改成了重量级锁）
- 拷贝在当前线程Lock Record的Mark Word信息是否与对象头中的Mark Word一致
4. 如果满足，则成功释放锁；
5. 如果不满足，则释放锁，唤醒被挂起阻塞的线程，开始重量级锁的竞争。

注: 当超过自旋阈值，竞争的线程就会把锁对象Mark Word指向重量级锁，导致Mark Word中的值发生了变化，当原持有轻量级锁的线程执行完毕，尝试通过 CAS 释放锁时，因为Mark Word已经指向重锁，不再是指向当前线程Lock Record的指针，于是解锁失败，这时原持有轻量级锁的线程就会知道锁已经升级为重量级锁。

#### 偏向锁升级为轻量级锁
1.先在原持有偏向锁的线程栈帧中分配 Lock Record
2.将对象头Mark Word拷贝到原持有偏向锁的线程 Lock Record 中, 然后使用CAS, 将对象头中的Mark Word修改为指向当前线程栈中Lock Record的指针。将原持有偏向锁的线程升级为持有偏向锁的线程
3.唤醒线程，从安全点继续执行，执行完毕解锁

### 偏向锁
#### 偏向锁的引入
在多处理器上CAS操作可能开销很大。

大多数锁不仅不存在竞争，而且往往由同一个线程使用。

使单独一个线程获取锁的开销更低。

代价是使另一个线程获取锁开销增大。

#### 偏向锁加锁过程
当锁对象第一次被线程获取时，VM把对象头中的标志位设为101，即偏向模式。同时使用CAS把获取到这个锁的线程ID记录在对象的mark word中，如果CAS成功，则持有偏向锁的线程以后每次进行这个锁相关的同步块时，不再进行任务同步操作，只进行比较Mark word中的线程ID是否是当前线程的ID。

#### 偏向锁的解锁过程
当另外一个线程去尝试获取这个锁时，偏向模式结束。根据锁对象目前是否处于被锁定状态，撤销偏向后恢复到未锁定或轻量级锁定状态。

VM会停止持有偏向锁的线程 (实际上，VM不能停止单一线程，而是在安全点进行的操作) 。
遍历持有偏向锁的线程的栈，找到锁记录空间，将displaced mark 写入到最旧的锁记录空间，其他的写0。
更新锁对象的mark word。如果被锁定，则指向最旧的锁记录空间，否则，填入未锁定值。

偏向锁的特点: 

偏向于第一个获取锁的线程: 

在mark word的Tag中增加一位
001表示无锁状态
101表示偏向或可偏向状态 (thread ID ==0 == unlock) 
通过CAS来获取偏向锁
对于持有锁的线程接下的锁获取和释放开销非常小 (仅仅判断下，不需要CAS同步操作) 。

如果另一个线程锁定了偏向锁对象，则偏向锁收回，升级为轻量级锁 (增加了另一个线程获取锁的开销) 。

### 重量级锁
重量级锁是悲观锁的一种

JAVA的synchronized关键字能够作为函数的修饰符，也可作为函数内的语句，也就是平时说的synchronized 方法和 synchronized 块。假如再细的分类: 
  
synchronized可作用于:
- instance变量，
- object reference (对象引用) ,
- static函数,
- class literals(类名称字面常量),

身上。 在进一步阐述之前，我们需要明确几点: 

A．无论synchronized关键字加在方法上还是对象上，他取得的锁都是对象，而不是把一段代码或函数当作锁――而且同步方法很可能还会被其他线程的对象访问。
  
B．每个对象只有一个锁 (lock) 和之相关联。
  
C．实现同步是要很大的系统开销作为代价的，甚至可能造成死锁，所以尽量避免无谓的同步控制。 接着来讨论synchronized用到不同地方对代码产生的影响:  假设P1、P2是同一个类的不同对象，这个类中定义了以下几种情况的同步块或同步方法，P1、P2就都能够调用他们。

把synchronized当作函数修饰符时，示例代码如下: 

```java
java Public synchronized void method(){}
  
```

这也就是同步方法，那这时 synchronized 锁定的是哪个对象呢？他锁定的是调用这个同步方法对象。也就是说，当一个对象P1在不同的线程中执行这个同步方法时，他们之间会形成互斥，达到同步的效果。但是这个对象所属的Class所产生的另一对象P2却能够任意调用这个被加了synchronized关键字的方法。 上边的示例代码等同于如下代码: 

```java
public void method(){
synchronized (this){
}
}
```

此处的this指的是什么呢？他指的就是调用这个方法的对象，如P1。可见同步方法实质是将synchronized作用于object reference。-那个拿到了P1对象锁的线程，才能够调用P1的同步方法，而对P2而言，P1这个锁和他毫不相干，程序也可能在这种情形下摆脱同步机制的控制，造成数据混乱。

### 同步块
```java
public void method(SomeObject so) {
synchronized(so){
}
} 
```

这时，锁就是so这个对象，谁拿到这个锁谁就能够运行他所控制的那段代码。当有一个明确的对象作为锁时，就能够这样写，但当没有明确的对象作为锁，只是想让一段代码同步时，能够创建一个特别的instance变量 (他得是个对象) 来充当锁: 
### instance变量
```java 
class Foo implements Runnable{
private byte[] lock = new byte[0]; // 特别的instance变量
Public void method(){
synchronized(lock) {
  
//...
  
} 
} 
} 
```

注: 零长度的byte数组对象创建起来将比任何对象都经济-查看编译后的字节码: 生成零长度的byte[]对象只需3条操作码，而Object lock = new Object()则需要7行操作码。

### 将synchronized作用于static 函数
```java
  
Class Foo{
      
// 同步的static 函数
      
public synchronized static void method1(){
      
//….
      
}
      
public void method2(){
        
// class literal(类名称字面常量)
        
synchronized(Foo.class){}
      
}
  
}
  
```

代码中的method2()方法是把class literal作为锁的情况，他和同步的static函数产生的效果是相同的，class litera取得的锁很特别，是当前调用这个方法的对象所属的类 (Class，而不再是由这个Class产生的某个具体对象了) 。
  
假如一个类中定义了一个synchronized的static函数A，也定义了一个synchronized 的instance函数B，那么这个类的同一对象Obj在多线程中分别访问A和B两个方法时，不会构成同步，因为他们的锁都不相同。A方法的锁是Obj所属的那个Class，而B的锁是Obj所属的这个对象。

作为修饰符加在方法声明上, synchronized修饰非静态方法时表示锁住了调用该方法的堆对象, 修饰静态方法时表示锁住了这个类在方法区中的类对象.

synchronized(X.class) 使用类对象(class literal)作为锁. 同一时间只有一个线程可以能访问块中资源.
  
synchronized(this)和synchronized(mutex) 都是对象锁, 同一时间每个实例都保证只能有一个实例能访问块中资源.
  
sychronized的对象最好选择引用不会变化的对象 (例如被标记为final,或初始化后永远不会变) , 虽然synchronized是在对象上加锁, 但是它首先要通过引用来定位对象, 如果引用会变化, 可能带来意想不到的后果

Java的synchronized使用方法小结如下:  搞清楚synchronized锁定的是哪个对象，就能帮助我们设计更安全的多线程程式。 更有一些技巧能够让我们对共享资源的同步访问更加安全: 
  
1．定义private 的instance变量和他的get方法，而不要定义public/protected的instance变量。假如将变量定义为public，对象在外界能够绕过同步方法的控制而直接取得他，并改变他。这也是JavaBean的标准实现方式之一。
  
2．假如instance变量是个对象，如数组或ArrayList什么的，那上述方法仍然不安全，因为当外界对象通过get方法拿到这个instance对象的引用后，又将其指向另一个对象，那么这个private变量也就变了，岂不是很危险。 这个时候就需要将get方法也加上synchronized同步，并且，只返回这个private对象的clone()――这样，调用端得到的就是对象副本的引用了。

### synchronized 重入
当一个线程请求其它的线程已经占有的锁时，请求线程将被阻塞。

然而内部锁是可重进入的，因此线程在试图获得它自己占用的锁时，请求会成功。重入意味着请求是基于"每一个线程"，而不是基于"每一次调用" (互斥锁是基于每次调用的) 。重进入的实现是通过为每一个锁关联一个请求计数器和一个占有他的线程。当计数为0时，认为锁是未被占用的。线程请求一个未被占有的锁时候，JVM将记录锁的占有者，并且将请求计数设置为1。如果同一个线程再次请求这个锁，计数将递增；每次占用线程退出语句块时，计数器值将递减，直到计数器达到0时候，锁被释放。
  
重入方便了锁行为的封装，因此简化了面向对象并发代码的开发。
  
public class Widget {
      
public synchronized void doSomething() {
          
...
      
}
  
}

public class LoggingWidget extends Widget {
      
public synchronized void doSomething() {
          
System.out.println(toString() + ": calling doSomething");
          
super.doSomething();//若内置锁是不可重入的，则发生死锁
      
}
  
}

在例子中，子类覆盖了父类的 synchronized 类型的方法，并调用父类中的方法。如果没有可重入的锁，子类中可能就会产生死锁，因为Widget和LoggingWidget中的dosomething方法都是synchronized 类型的，都会在处理前试图获得Widget的锁。倘若内部锁不是可重入的，super.doSomething的调用者就永远无法获得Widget的锁。因为锁已经被占用，导致线程永久的延迟，等待着一个永远无法获得的锁。

以上代码在同一个线程执行时，不会导致死锁，java中的synchronized 本身就是可以重入的 (reentrant) ， 不管是synchronized方法，还是synchronized statements。参见: 
  
>http://docs.oracle.com/javase/tutorial/essential/concurrency/locksync.html 
>http://stackoverflow.com/questions/5787957/reentrant-synchronization-behavior-with-synchronized-statements

LoggingWidget 的对象调用doSomething方法时，锁对象为LoggingWidget对象 super.doSomething()调用是锁对象是LoggingWidget对象运行程序，查看thread dump发现: 调用super.doSomething()时锁对象依然是LoggingWidget对象。

"线程#1" prio=6 tid=0x0bd60400 nid=0x16f8 waiting on condition [0x0bf8f000..0x0bf8fd68]
  
java.lang.Thread.State: TIMED_WAITING (sleeping)
  
at java.lang.Thread.sleep(Native Method)
  
at Widget.doSomething(Widget.java:4)
  
- locked <0x03fbc150> (a LoggingWidget)
  
at LoggingWidget.doSomething(LoggingWidget.java:5)
  
- locked <0x03fbc150> (a LoggingWidget)
  
at LoggingWidget$1.run(LoggingWidget.java:15)
     
Locked ownable synchronizers:
  
- None

super.doSomething();子类会去get Widget的monitorlock，此时就会取到lock，如果monitorlock不可重入，就需要再次拿LoggingWidget的lock，but，此时LoggingWidget的lock已经被占用了，所以会发生deadlock。

支持可重入的话，只是简单的实现进入计数，每次进入+1，退出-1，如果计数器为0，则认为此时对象是没有被加锁 。
  
因为JVM的可重入解决了这个问题啊，所以dump里看到的是正确的流程。

### 可见性
在说明Java多线程内存可见性之前，先来简单了解一下Java内存模型。
  
Java所有变量都存储在主内存中
  
每个线程都有自己独立的工作内存，里面保存该线程的使用到的变量副本 (该副本就是主内存中该变量的一份拷贝) 
  
线程对共享变量的所有操作都必须在自己的工作内存中进行，不能直接在主内存中读写
  
不同线程之间无法直接访问其他线程工作内存中的变量，线程间变量值的传递需要通过主内存来完成。
  
线程1对共享变量的修改，要想被线程2及时看到，必须经过如下2个过程: 
  
把工作内存1中更新过的共享变量刷新到主内存中
  
将主内存中最新的共享变量的值更新到工作内存2中

### 可见性与原子性
可见性: 一个线程对共享变量的修改，更够及时的被其他线程看到
  
原子性: 即不可再分了，不能分为多步操作。比如赋值或者return。比如"a = 1;"和 "return a;"这样的操作都具有原子性。类似"a += b"这样的操作不具有原子性，在某些JVM中"a += b"可能要经过这样三个步骤: 
  
    ①取出a和b
    ②计算a+b
    ③将计算结果写入内存

### Synchronized能够实现原子性和可见性/synchronized和volatile比较
Synchronized能够实现原子性和可见性；在Java内存模型中，synchronized规定，线程在加锁时，先清空工作内存→在主内存中拷贝最新变量的副本到工作内存→执行完代码→将更改后的共享变量的值刷新到主内存中→释放互斥锁。

把代码块声明为 synchronized，有两个重要后果，通常是指该代码具有 原子性 (atomicity) 和 可见性 (visibility) 。原子性意味着一个线程一次只能执行由一个指定监控对象 (lock) 保护的代码，从而防止多个线程在更新共享状态时相互冲突。可见性则更为微妙；它要对付内存缓存和编译器优化的各种反常行为。一般来说，线程以某种不必让其他线程立即可以看到的方式 (不管这些线程在寄存器中、在处理器特定的缓存中，还是通过指令重排或者其他编译器优化) ，不受缓存变量值的约束，但是如果开发人员使用了同步，如下面的代码所示，那么运行库将确保某一线程对变量所做的更新先于对现有 synchronized 块所进行的更新，当进入由同一监控器 (lock) 保护的另一个 synchronized 块时，将立刻可以看到这些对变量所做的更新。类似的规则也存在于 volatile 变量上。

在Java内存模型中，synchronized 规定，线程在加锁时，先清空工作内存在主内存中拷贝最新变量的副本到工作内存→执行完代码→将更改后的共享变量的值刷新到主内存中→释放互斥锁。

Volatile 实现内存可见性是通过 store 和 load 指令完成的；也就是对 volatile 变量执行写操作时，会在写操作后加入一条 store 指令，即强迫线程将最新的值刷新到主内存中；而在读操作时，会加入一条 load 指令，即强迫从主内存中读入变量的值。但volatile不保证volatile变量的原子性，例如: 
```java
Private int Num=0;
Num++; //Num不是原子操作
```

Num不是原子操作，因为其可以分为: 读取Num的值，将Num的值+1，写入最新的Num的值。
      
对于Num++; 操作，线程1和线程2都执行一次，最后输出Num的值可能是: 1或者2
     
### 解释
输出结果1的解释: 当线程1执行Num++;语句时，先是读入Num的值为0，倘若此时让出CPU执行权，线程获得执行，线程2会重新从主内存中，读入Num的值还是0，然后线程2执行+1操作，最后把Num=1刷新到主内存中； 线程2执行完后，线程1由开始执行，但之前已经读取的Num的值0，所以它还是在0的基础上执行+1操作，也就是还是等于1，并刷新到主内存中。所以最终的结果是1
      
一般在多线程中使用 volatile 变量，为了安全，对变量的写入操作不能依赖当前变量的值: 如Num++或者Num=Num*5这些操作。

简单的说就是 synchronized 的代码块是确保可见性和原子性的, volatile只能确保可见性

当且仅当下面条件全部满足时, 才能使用volatile

- 对变量的写入操作不依赖于变量的当前值, (++i/i++这种肯定不行), 或者能确保只有单个线程在更新
- 该变量不会与其他状态变量一起纳入不变性条件中
- 访问变量时不需要加锁

### Synchronized和Volatile的比较
1) Synchronized保证内存可见性和操作的原子性
  
2) Volatile只能保证内存可见性
  
3) Volatile不需要加锁，比Synchronized更轻量级，并不会阻塞线程 (volatile不会造成线程的阻塞；synchronized可能会造成线程的阻塞。) 
  
4) volatile标记的变量不会被编译器优化,而synchronized标记的变量可以被编译器优化 (如编译器重排序的优化) .
  
5) volatile是变量修饰符，仅能用于变量，而synchronized是一个方法或块的修饰符。
  
volatile本质是在告诉JVM当前变量在寄存器中的值是不确定的，使用前，需要先从主存中读取，因此可以实现可见性。而对n=n+1,n++等操作时，volatile关键字将失效，不能起到像synchronized一样的线程同步 (原子性) 的效果。

### java线程阻塞的代价
java的线程是映射到操作系统原生线程之上的，如果要阻塞或唤醒一个线程就需要操作系统介入，需要在户态与核心态之间切换，这种切换会消耗大量的系统资源，因为用户态与内核态都有各自专用的内存空间，专用的寄存器等，用户态切换至内核态需要传递给许多变量、参数给内核，内核也需要保护好用户态在切换时的一些寄存器值、变量等，以便内核态调用结束后切换回用户态继续工作。

如果线程状态切换是一个高频操作时，这将会消耗很多CPU处理时间；
如果对于那些需要同步的简单的代码块，获取锁挂起操作消耗的时间比用户代码执行的时间还要长，这种同步策略显然非常糟糕的。
synchronized会导致争用不到锁的线程进入阻塞状态，所以说它是java语言中一个重量级的同步操纵，被称为重量级锁，为了缓解上述性能问题，JVM从1.5开始，引入了轻量锁与偏向锁，默认启用了自旋锁，他们都属于乐观锁。


### synchonrize和juc中的锁比较
ReentrantLock 在内存上的语义于 synchronize 相同, 但是它提供了额外的功能, 可以作为一种高级工具. 当需要一些可定时, 可轮询, 可中断的锁获取操作, 或者希望使用公平锁, 或者使用非块结构的编码时才应该考虑ReetrantLock.

总结一点, 在业务并发简单清晰的情况下推荐synchronized, 在业务逻辑并发复杂, 或对使用锁的扩展性要求较高时, 推荐使用ReentrantLock这类锁. 另外今后JVM的优化方向一定是基于底层synchronize的, 性能方面应该选择synchronize

用了锁就真的没有并发问题了么?
  
先上代码, 看一下是否有并发问题

```java
Map syncMap = Collections.synchronizedMap(new HashMap());
  
if(!map.containsKey("a")){
      
map.put("a",value);
  
}
```
  
虽然Map上所有的方法都已被synchronize保护了, 但是在外部使用的时候, 一定要注意竞态条件

竞态条件: 先检查后执行的这种操作是最常见的竞态条件
  
下面是并发条件下的一些 Donts

    Don't synchronize on an object you're changing
      
    Don't synchronize on a String literal
      
    Don't synchronize on auto-boxed values
      
    Don't synchronize on null
      
    Don't synchronize on a Lock object
      
    Don't synchronize on getClass()
      
    Be careful locking on a thread-safe object with encapsulated locking

 
【相关习题】
  
(1)下列说法不正确的是 () 
  
A.当两个并发线程访问同一个对象object中的这个synchronized(this)同步代码块时，一个时间内只能有一个线程得到执行。
  
B.当一个线程访问object的一个synchronized(this)同步代码块时，另一个线程仍然可以访问该object中的非synchronized(this)同步代码块。
  
C.当一个线程访问object的一个synchronized(this)同步代码块时，其他线程对object中所有其它synchronized(this)同步代码块的访问不会被阻塞。
  
D.当一个线程访问object的一个synchronized(this)同步代码块时，它就获得了这个object的对象锁。结果，其它线程对该object对象所有同步代码部分的访问都被暂时阻塞。
  
答案: C，当一个线程访问object的一个synchronized(this)同步代码块时，其他线程对object中所有其它synchronized(this)同步代码块的访问将会被阻塞。
  
(2) 下面叙述错误的是: 
  
A.通过synchronized和volatile都可以实现可见性
  
B.不同线程之间可以直接访问其他线程工作内存中的变量
  
C.线程对共享变量的所有操作都必须在自己的工作内存中进行
  
D.所有的变量都存储在主内存中
  
答案: B，不同线程之间无法直接访问其他线程工作内存中的变量

不论什么时候，只要您将编写的变量接下来可能被另一个线程读取，或者您将读取的变量最后是被另一个线程写入的，那么您必须进行同步。

### monitor
官方文档中对monitor的解释：  
Synchronizationis built around an internal entity known as the intrinsic lock or monitor lock. (The API specification often refers to this entity simplyas a “monitor.”)，Every object has an intrinsic lock associated with it.By convention, a thread that needs exclusive and consistent access toan object’s fields has to acquire the object’s intrinsic lock beforeaccessing them, and then release the intrinsic lock when it’s done withthem.
Monitor Object 设计模式
我们使用Monitor Object设计模式来解决这类问题：将被客户线程并发访问的对象定义为一个monitor对象。客户线程仅能通过monitor对象的同步方法才能使用monitor对象定义的服务。为了防止陷入竞争条件，在任一时刻只能有一个同步方法被执行。每一个monitor对象包含一个monitor锁，被同步方法用于串行访问对象的行为和状态。此外，同步方法可以根据一个或多个与monitor对象相关的monitor conditions来决定在何种情况下挂起或恢复它们的执行。

Java对于这样一个典型的模式做了很好的语言层面的封装，因此对于Java的开发者来说，很多关于该模式本身的东西被屏蔽掉了，如果希望从本质上对Monitor Object设计模式有一个更全面的认识，可以结合C++版本的Monitor Object设计模式。

### 在Monitor Object模式中，主要有四种类型的参与者：
- 监视者对象 (Monitor Object）：负责定义公共的接口方法，这些公共的接口方法会在多线程的环境下被调用执行；
- 同步方法：这些方法是监视者对象锁定义。为了防止竞争条件，无论是否同时有多个线程并发调用同步方法，还是监视者对象含有多个同步方法，在任一时间内只有监视者对象的一个同步方法能够被执行。
- 监视锁 (Monitor Lock）：每一个监视者对象都会拥有一把监视锁。
- 监视条件 (Monitor Condition）：同步方法使用监视锁和监视条件来决定方法是否需要阻塞或重新执行。

### Java Monitor Object
Java Monitor从两个方面来支持线程之间的同步，即：互斥执行与协作。Java使用对象锁 (通过synchronized获得对象锁）保证工作在共享的数据集上的线程互斥执行，使用 notify/notifyAll/wait 方法来协同不同线程之间的工作。这些方法在Object类上被定义，会被所有的Java对象自动继承。

实质上，Java的Object类本身就是监视者对象，Java语言对于这样一个典型并发设计模式做了内建的支持。不过，在Java里，我们已经看不到C++中的区域锁与条件变量的概念了。

线程如果获得监视锁成功，将成为监视者对象的拥有者。在任一时刻内，监视者对象只属于一个活动线程 (Owner）。拥有者线程可以调用wait方法自动释放监视锁，进入等待状态。


### monitor 机制
synchronized 关键字是 Java 在语法层面上，用来让开发者方便地进行多线程同步的重要工具。要进入一个 synchronized 方法修饰的方法或者代码块，会先获取与 synchronized 关键字绑定在一起的 Object 的对象锁，这个锁也限定了其它线程无法进入与这个锁相关的其它 synchronized 代码区域。

网上很多文章以及资料，在分析 synchronized 的原理时，基本上都会说 synchronized 是基于 monitor 机制实现的，但很少有文章说清楚，都是模糊带过。
参照前面提到的 Monitor 的几个基本元素，如果 synchronized 是基于 monitor 机制实现的，那么对应的元素分别是什么？
它必须要有临界区，这里的临界区我们可以认为是对对象头 mutex 的 P 或者 V 操作，这是个临界区
那 monitor object 对应哪个呢？mutex？总之无法找到真正的 monitor object。
所以我认为“synchronized 是基于 monitor 机制实现的”这样的说法是不正确的，是模棱两可的。
Java 提供的 monitor 机制，其实是 Object，synchronized 等元素合作形成的，甚至说外部的条件变量也是个组成部分。JVM 底层的 ObjectMonitor 只是用来辅助实现 monitor 机制的一种常用模式，但大多数文章把 ObjectMonitor 直接当成了 monitor 机制。
我觉得应该这么理解：Java 对 monitor 的支持，是以机制的粒度提供给开发者使用的，也就是说，开发者要结合使用 synchronized 关键字，以及 Object 的 wait / notify 等元素，才能说自己利用 monitor 的机制去解决了一个生产者消费者的问题。



版权声明: 本文为CSDN博主「朱清震」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/zqz_zqz/article/details/70233767



http://leo-faith.iteye.com/blog/177779
  
http://topmanopensource.iteye.com/blog/1736739
  
http://blog.csdn.net/guyuealian/article/details/52525724

版权声明: 本文为CSDN博主「codershamo」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/codershamo/java/article/details/52071996
https://ddnd.cn/2019/03/21/java-synchronized/
https://juejin.im/post/5c936018f265da60ec281bcb
>http://www.imooc.com/video/6775
>https://dymanzy.github.io/2017/08/07/synchronized%E4%B8%8E%E5%AF%B9%E8%B1%A1%E7%9A%84Monitor/