---
title: java线程安全
author: "-"
date: 2012-09-21T02:43:48+00:00
url: /?p=4139
categories:
  - Java
tags:
  - Java

---
## java线程安全
什么叫线程安全？这个首先要明确。线程安全就是说多线程访问同一代码，不会产生不确定的结果。

java的内存模型，java的线程同步机制。特别是内存模型，java的线程同步机制很大程度上都是基于内 存模型而设定的。

浅谈java内存模型
  
不同的平台，内存模型是不一样的，但是jvm的内存模型规范是统一的。其实java的多线程并发问题最终都会反映在java的内存模型上，所谓线程安全无非是要控制多个线程对某个资源的有序访问或修改。总结java的内存模型，要解决两个主要的问题: 可见性和有序性。我们都知道计算机有高速缓存的存在，处理器并不是每次处理数据都是取内存的。JVM定义了自己的内存模型，屏蔽了底层平台内存管理细节，对于java开发人员，要清楚在jvm内存模型的基础上，如果解决多线程的可见性和有序性。
  
那么，何谓可见性？ 多个线程之间是不能互相传递数据通信的，它们之间的沟通只能通过共享变量来进行。Java内存模型 (JMM) 规定了jvm有主内存，主内存是多个线程共享的。当new一个对象的时候，也是被分配在主内存中，每个线程都有自己的工作内存，工作内存存储了主存的某些对象的副本，当然线程的工作内存大小是有限制的。当线程操作某个对象时，执行顺序如下: 
  
(1) 从主存复制变量到当前工作内存 (read and load)
  
(2) 执行代码，改变共享变量值 (use and assign)
  
(3) 用工作内存数据刷新主存相关内容 (store and write)

JVM规范定义了线程对主存的操作指 令: read，load，use，assign，store，write。当一个共享变量在多个线程的工作内存中都有副本时，如果一个线程修改了这个共享变量，那么其他线程应该能够看到这个被修改后的值，这就是多线程的可见性问题。
  
那么，什么是有序性呢？线程在引用变量时不能直接从主内存中引用,如果线程工作内存中没有该变量,则会从主内存中拷贝一个副本到工作内存中,这个过程为read-load,完成后线程会引用该副本。当同一线程再度引用该字段时,有可能重新从主存中获取变量副本(read-load-use),也有可能直接引用原来的副本 (use),也就是说 read,load,use顺序可以由JVM实现系统决定。

线程不能直接为主存中的字段赋值，它会将值指定给工作内存中的变量副本(assign),完成后这个变量副本会同步到主存储区(store- write)，至于何时同步过去，根据JVM实现系统决定.有该字段,则会从主内存中将该字段赋值到工作内存中,这个过程为read-load,完成后线程会引用该变量副本，当同一线程多次重复对字段赋值时,比如: 

for(int i=0;i<10;i++)
  
a++;
  
线程有可能只对工作内存中的副本进行赋值,只到最后一次赋值后才同步到主存储区，所以assign,store,write顺序可以由JVM实现系统决定。假设有一个共享变量x，线程a执行x=x+1。从上面的描述中可以知道x=x+1并不是一个原子操作，它的执行过程如下: 
  
1 从主存中读取变量x副本到工作内存
  
2 给x加1
  
3 将x加1后的值写回主存
  
如果另外一个线程b执行x=x-1，执行过程如下: 
  
1 从主存中读取变量x副本到工作内存
  
2 给x减1
  
3 将x减1后的值写回主存

那么显然，最终的x的值是不可靠的。假设x现在为10，线程a加1，线程b减1，从表面上看，似乎最终x还是为10，但是多线程情况下会有这种情况发生: 

1: 线程a从主存读取x副本到工作内存，工作内存中x值为10
  
2: 线程b从主存读取x副本到工作内存，工作内存中x值为10
  
3: 线程a将工作内存中x加1，工作内存中x值为11
  
4: 线程a将x提交主存中，主存中x为11
  
5: 线程b将工作内存中x值减1，工作内存中x值为9
  
6: 线程b将x提交到中主存中，主存中x为9
  
同样，x有可能为11，如果x是一个银行账户，线程a存款，线程b扣款，显然这样是有严重问题的，要解决这个问题，必须保证线程a和线程b是有序执行的， 并且每个线程执行的加1或减1是一个原子操作。看看下面代码: 

public class Account {
  
private int balance;

public Account(int balance) {
  
this.balance = balance;
  
}

public int getBalance() {
  
return balance;
  
}

public void add(int num) {
  
balance = balance + num;
  
}

public void withdraw(int num) {
  
balance = balance - num;
  
}

public static void main(String[] args) throws InterruptedException {
  
Account account = new Account(1000);
  
Thread a = new Thread(new AddThread(account, 20), "add");
  
Thread b = new Thread(new WithdrawThread(account, 20), "withdraw");
  
a.start();
  
b.start();
  
a.join();
  
b.join();
  
System.out.println(account.getBalance());
  
}

static class AddThread implements Runnable {
  
Account account;
  
int amount;

public AddThread(Account account, int amount) {
  
this.account = account;
  
this.amount = amount;
  
}

public void run() {
  
for (int i = 0; i < 200000; i++) {
  
account.add(amount);
  
}
  
}
  
}

static class WithdrawThread implements Runnable {
  
Account account;
  
int amount;

public WithdrawThread(Account account, int amount) {
  
this.account = account;
  
this.amount = amount;
  
}

public void run() {
  
for (int i = 0; i < 100000; i++) {
  
account.withdraw(amount);
  
}
  
}
  
}
  
}
  
第一次执行结果为10200，第二次执行结果为1060，每次执行的结果都是不确定的，因为线程的执行顺序是不可预见的。这是java同步产生的根源，synchronized关键字保证了多个线程对于同步块是互斥的，synchronized作为一种同步手段，解决java多线程的执行有序性和内存可见性，而volatile关键字之解决多线程的内存可见性问题。后面将会详细介绍。

synchronized关键字
  
上面说了，java用synchronized关键字做为多线程并发环境的执行有序性的保证手段之一。当一段代码会修改共享变量，这一段代码成为互斥区或临界区，为了保证共享变量的正确性，synchronized标示了临界区。典型的用法如下: 

synchronized(锁){
  
临界区代码
  
}
  
为了保证银行账户的安全，可以操作账户的方法如下: 

public synchronized void add(int num) {
  
balance = balance + num;
  
}

public synchronized void withdraw(int num) {
  
balance = balance - num;
  
}
  
刚才不是说了synchronized的用法是这样的吗: 

synchronized(锁){
  
临界区代码
  
}
  
那么对于public synchronized void add(int num)这种情况，意味着什么呢？其实这种情况，锁就是这个方法所在的对象。同理，如果方法是public static synchronized void add(int num)，那么锁就是这个方法所在的class。
  
理论上，每个对象都可以做为锁，但一个对象做为锁时，应该被多个线程共享，这样才显得有意义，在并发环境下，一个没有共享的对象作为锁是没有意义的。假如有这样的代码: 

public class ThreadTest{

public void test(){

Object lock=new Object();

synchronized (lock){

//do something

}

}

}
  
lock变量作为一个锁存在根本没有意义，因为它根本不是共享对象，每个线程进来都会执行Object lock=new Object();每个线程都有自己的lock，根本不存在锁竞争。
  
每个锁对象都有两个队列，一个是就绪队列，一个是阻塞队列，就绪队列存储了将要获得锁的线程，阻塞队列存储了被阻塞的线程，当一个被线程被唤醒 (notify)后，才会进入到就绪队列，等待cpu的调度。当一开始线程a第一次执行account.add方法时，jvm会检查锁对象account 的就绪队列是否已经有线程在等待，如果有则表明account的锁已经被占用了，由于是第一次运行，account的就绪队列为空，所以线程a获得了锁， 执行account.add方法。如果恰好在这个时候，线程b要执行account.withdraw方法，因为线程a已经获得了锁还没有释放，所以线程 b要进入account的就绪队列，等到得到锁后才可以执行。
  
一个线程执行临界区代码过程如下: 
  
1 获得同步锁
  
2 清空工作内存
  
3 从主存拷贝变量副本到工作内存
  
4 对这些变量计算
  
5 将变量从工作内存写回到主存
  
6 释放锁
  
可见，synchronized既保证了多线程的并发有序性，又保证了多线程的内存可见性。

生产者/消费者模式
  
生产者/消费者模式其实是一种很经典的线程同步模型，很多时候，并不是光保证多个线程对某共享资源操作的互斥性就够了，往往多个线程之间都是有协作的。
  
假设有这样一种情况，有一个桌子，桌子上面有一个盘子，盘子里只能放一颗鸡蛋，A专门往盘子里放鸡蛋，如果盘子里有鸡蛋，则一直等到盘子里没鸡蛋，B专门 从盘子里拿鸡蛋，如果盘子里没鸡蛋，则等待直到盘子里有鸡蛋。其实盘子就是一个互斥区，每次往盘子放鸡蛋应该都是互斥的，A的等待其实就是主动放弃锁，B 等待时还要提醒A放鸡蛋。
  
如何让线程主动释放锁
  
很简单，调用锁的wait()方法就好。wait方法是从Object来的，所以任意对象都有这个方法。看这个代码片段: 

Object lock=new Object();//声明了一个对象作为锁

synchronized (lock) {

balance = balance - num;

//这里放弃了同步锁，好不容易得到，又放弃了

lock.wait();

}
  
如果一个线程获得了锁lock，进入了同步块，执行lock.wait()，那么这个线程会进入到lock的阻塞队列。如果调用 lock.notify()则会通知阻塞队列的某个线程进入就绪队列。
  
声明一个盘子，只能放一个鸡蛋 


  import java.util.ArrayList; 
  
    import java.util.List;
  
  
    public class Plate {
  
  
    List
    
    <Object>
      eggs = new ArrayList
      
      <Object>
        (); 
        
        
          public synchronized Object getEgg() {
        
        
        
          while(eggs.size() == 0) {
        
        
        
          try {
        
        
        
          wait();
        
        
        
          } catch (InterruptedException e) {
        
        
        
          }
        
        
        
          }
        
        
        
          Object egg = eggs.get(0);
        
        
        
          eggs.clear();// 清空盘子
        
        
        
          notify();// 唤醒阻塞队列的某线程到就绪队列
        
        
        
          System.out.println("拿到鸡蛋");
        
        
        
          return egg;
        
        
        
          }
        
        
        
          public synchronized void putEgg(Object egg) {
        
        
        
          while(eggs.size() > 0) {
        
        
        
          try {
        
        
        
          wait();
        
        
        
          } catch (InterruptedException e) {
        
        
        
          }
        
        
        
          }
        
        
        
          eggs.add(egg);// 往盘子里放鸡蛋
        
        
        
          notify();// 唤醒阻塞队列的某线程到就绪队列
        
        
        
          System.out.println("放入鸡蛋");
        
        
        
          }
        
        
        
          static class AddThread extends Thread{
        
        
        
          private Plate plate;
        
        
        
          private Object egg=new Object();
        
        
        
          public AddThread(Plate plate){
        
        
        
          this.plate=plate;
        
        
        
          }
        
        
        
          public void run(){
        
        
        
          for(int i=0;i<5;i++){ plate.putEgg(egg); } } } static class GetThread extends Thread{ private Plate plate; public GetThread(Plate plate){ this.plate=plate; } public void run(){ for(int i=0;i<5;i++){ plate.getEgg(); } } } public static void main(String args[]){ try { Plate plate=new Plate(); Thread add=new Thread(new AddThread(plate)); Thread get=new Thread(new GetThread(plate)); add.start(); get.start(); add.join(); get.join(); } catch (InterruptedException e) { e.printStackTrace(); } System.out.println("测试结束"); } } 执行结果:  放入鸡蛋 拿到鸡蛋 放入鸡蛋 拿到鸡蛋 放入鸡蛋 拿到鸡蛋 放入鸡蛋 拿到鸡蛋 放入鸡蛋 拿到鸡蛋 测试结束 声明一个Plate对象为plate，被线程A和线程B共享，A专门放鸡蛋，B专门拿鸡蛋。假设 1 开始，A调用plate.putEgg方法，此时eggs.size()为0，因此顺利将鸡蛋放到盘子，还执行了notify()方法，唤醒锁的阻塞队列的线程，此时阻塞队列还没有线程。 2 又有一个A线程对象调用plate.putEgg方法，此时eggs.size()不为0，调用wait()方法，自己进入了锁对象的阻塞队列。 3 此时，来了一个B线程对象，调用plate.getEgg方法，eggs.size()不为0，顺利的拿到了一个鸡蛋，还执行了notify()方法，唤醒锁的阻塞队列的线程，此时阻塞队列有一个A线程对象，唤醒后，它进入到就绪队列，就绪队列也就它一个，因此马上得到锁，开始往盘子里放鸡蛋，此时盘子是 空的，因此放鸡蛋成功。 4 假设接着来了线程A，就重复2；假设来料线程B，就重复3。 整个过程都保证了放鸡蛋，拿鸡蛋，放鸡蛋，拿鸡蛋。 volatile关键字 volatile是java提供的一种同步手段，只不过它是轻量级的同步，为什么这么说，因为volatile只能保证多线程的内存可见性，不能保证多线程的执行有序性。而最彻底的同步要保证有序性和可见性，例如synchronized。任何被volatile修饰的变量，都不拷贝副本到工作内存，任何修改都及时写在主存。因此对于Valatile修饰的变量的修改，所有线程马上就能看到，但是volatile不能保证对变量的修改是有序的。什么意思呢？假如有这样的代码:    
          
          
            public class VolatileTest{
          
          
          
            public volatile int a;
          
          
          
            public void add(int count){
          
          
          
            a=a+count;
          
          
          
            }
          
          
          
            }
 当一个VolatileTest对象被多个线程共享，a的值不一定是正确的，因为a=a+count包含了好几步操作，而此时多个线程的执行是无序的，因 为没有任何机制来保证多个线程的执行有序性和原子性。volatile存在的意义是，任何线程对a的修改，都会马上被其他线程读取到，因为直接操作主存， 没有线程对工作内存和主存的同步。所以，volatile的使用场景是有限的，在有限的一些情形下可以使用 volatile 变量替代锁。要使 volatile 变量提供理想的线程安全,必须同时满足下面两个条件:
 1)对变量的写操作不依赖于当前值。
 2)该变量没有包含在具有其他变量的不变式中
 volatile只保证了可见性，所以Volatile适合直接赋值的场景，如
            
          
          
            public class VolatileTest{
          
          
          
            public volatile int a;
          
          
          
            public void setA(int a){
          
          
          
            this.a=a;
          
          
          
            }
          
          
          
            }

在没有volatile声明时，多线程环境下，a的最终值不一定是正确的，因为this.a=a;涉及到给a赋值和将a同步回主存的步骤，这个顺序可能被 打乱。如果用volatile声明了，读取主存副本到工作内存和同步a到主存的步骤，相当于是一个原子操作。所以简单来说，volatile适合这种场 景: 一个变量被多个线程共享，线程直接给这个变量赋值。这是一种很简单的同步场景，这时候使用volatile的开销将会非常小。
          
关于线程安全总结 (－) 请看http://www.iteye.com/topic/806990 ，发该贴后，很多朋友都发站内消息问我一些问题，我把回复整理成一篇帖子。敬请高人手下留情，小可谢过了。
          
站内很多人都问我，所谓线程的"工作内存"到底是个什么东西？有的人认为是线程的栈，其实这种理解是不正确的。看看JLS (java语言规范) 对线程工作 内存的描述，线程的working memory只是cpu的寄存器和高速缓存的抽象描述。
          
可能 很多人都觉得莫名其妙，说JVM的内存模型，怎么会扯到cpu上去呢？在此，我认为很有必要阐述下，免 得很多人看得不明不白的。先抛开java虚拟机不谈，我们都知道，现在的计算机，cpu在计算的时候，并不总是从内存读取数据，它的数据读取顺序优先级 是: 寄存器－高速缓存－内存。线程耗费的是CPU，线程计算的时候，原始的数据来自内存，在计算过程中，有些数据可能被频繁读取，这些数据被存储在寄存器和高速缓存中，当线程计算完后，这些缓存的数据在适当的时候应该写回内存。当个多个线程同时读写某个内存数据时，就会产生多线程并发问题，涉及到三个特性: 原子性，有序性，可见性。在《线程安全总结》这篇文章中，为了理解方便，我把原子性和有序性统一叫做"多线程执行有序性"。支持多线程的平台都会面临这种问题，运行在多线程平台上支持多线程的语言应该提供解决该问题的方案。
      
那么，我们看看JVM，JVM是一个虚拟的计算机，它也会面临多线程并发问题，java程序运行在java虚拟机平台上，java程序员不可能直接去控制底层线程对寄存器高速缓存内存之间的同步，那么java从语法层面，应该给开发人员提供一种解决方案，这个方案就是诸如 synchronized, volatile,锁机制 (如同步块，就绪队列，阻塞队列) 等等。这些方案只是语法层面的，但我们要从本质上去理解它，不能仅仅知道一个 synchronized 可以保证同步就完了。 在这里我说的是JVM的内存模型，是动态的，面向多线程并发的，沿袭JSL的"working memory"的说法，只是不想牵扯到太多底层细节，因为 《线程安全总结》这篇文章意在说明怎样从语法层面去理解java的线程同步，知道各个关键字的使用场景。
          
今天有人问我，那java的线程不是有栈吗？ 难道栈不是工作内存吗？ 工作内存这四个字得放到具体的场景中描述，方能体现它具体的意义，在描述JVM的线程同步时，工作内存指的是寄存器和高速缓存的抽象描述，具体请自行参阅JLS。上面讲的都是动态的内存模型，甚至已经超越了JVM的范围，那么JVM的内存静态存储是怎么划分的？今天还有人问我，jvm的内存模型不是有eden区吗？也不见你提起。我跟他说，这是两个角度去看的，甚至是两个不同的范围，动态的线程同步的内存模型，涵盖了cpu，寄存器，高速缓存，内存；JVM的静态内存储模型只是一种对内存的物理划分而已，它只局限在内存，而且只局限在JVM的内存。那些什么线程栈，eden区都仅仅在JVM内存。


http://www.iteye.com/topic/806990          
http://www.iteye.com/topic/808550
http://blog.csdn.net/xiao__gui/article/details/8934832
