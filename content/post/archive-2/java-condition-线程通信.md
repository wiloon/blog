---
title: 线程通信
author: "-"
date: 2016-09-23T05:13:57+00:00
url: /?p=9219
categories:
  - Uncategorized

tags:
  - reprint
---
## 线程通信
http://wiki.jikexueyuan.com/project/java-concurrent/thread-communication.html

线程通信的目标是使线程间能够互相发送信号。另一方面,线程通信使线程能够等待其他线程的信号。

通过共享对象通信
  
忙等待
  
wait(),notify()和 notifyAll()
  
丢失的信号
  
假唤醒
  
多线程等待相同信号
  
不要对常量字符串或全局对象调用 wait()

通过共享对象通信
  
线程间发送信号的一个简单方式是在共享对象的变量里设置信号值。线程 A 在一个同步块里设置 boolean 型成员变量 hasDataToProcess 为 true,线程 B 也在同步块里读取 hasDataToProcess 这个成员变量。这个简单的例子使用了一个持有信号的对象,并提供了 set 和 check 方法:

public class MySignal{

protected boolean hasDataToProcess = false;

public synchronized boolean hasDataToProcess(){
      
return this.hasDataToProcess;
    
}

public synchronized void setHasDataToProcess(boolean hasData){
      
this.hasDataToProcess = hasData;
    
}

}
  
线程 A 和 B 必须获得指向一个 MySignal 共享实例的引用,以便进行通信。如果它们持有的引用指向不同的 MySingal 实例,那么彼此将不能检测到对方的信号。需要处理的数据可以存放在一个共享缓存区里,它和 MySignal 实例是分开存放的。

忙等待(Busy Wait)
  
准备处理数据的线程 B 正在等待数据变为可用。换句话说,它在等待线程 A 的一个信号,这个信号使 hasDataToProcess()返回 true。线程 B 运行在一个循环里,以等待这个信号: 

protected MySignal sharedSignal = ...

...

while(!sharedSignal.hasDataToProcess()){
    
//do nothing... busy waiting
  
}

wait(),notify()和 notifyAll()
  
忙等待没有对运行等待线程的 CPU 进行有效的利用,除非平均等待时间非常短。否则,让等待线程进入睡眠或者非运行状态更为明智,直到它接收到它等待的信号。

Java 有一个内建的等待机制来允许线程在等待信号的时候变为非运行状态。java.lang.Object 类定义了三个方法,wait()、notify()和 notifyAll()来实现这个等待机制。

一个线程一旦调用了任意对象的 wait()方法,就会变为非运行状态,直到另一个线程调用了同一个对象的 notify()方法。为了调用 wait()或者 notify(),线程必须先获得那个对象的锁。也就是说,线程必须在同步块里调用 wait()或者 notify()。以下是 MySingal 的修改版本——使用了 wait()和 notify()的 MyWaitNotify: 

public class MonitorObject{
  
}

public class MyWaitNotify{

MonitorObject myMonitorObject = new MonitorObject();

public void doWait(){
      
synchronized(myMonitorObject){
        
try{
          
myMonitorObject.wait();
        
} catch(InterruptedException e){...}
      
}
    
}

public void doNotify(){
      
synchronized(myMonitorObject){
        
myMonitorObject.notify();
      
}
    
}
  
}
  
等待线程将调用 doWait(),而唤醒线程将调用 doNotify()。当一个线程调用一个对象的 notify()方法,正在等待该对象的所有线程中将有一个线程被唤醒并允许执行 (校注: 这个将被唤醒的线程是随机的,不可以指定唤醒哪个线程) 。同时也提供了一个 notifyAll()方法来唤醒正在等待一个给定对象的所有线程。

如你所见,不管是等待线程还是唤醒线程都在同步块里调用 wait()和 notify()。这是强制性的！一个线程如果没有持有对象锁,将不能调用 wait(),notify()或者 notifyAll()。否则,会抛出 IllegalMonitorStateException 异常。

 (校注: JVM 是这么实现的,当你调用 wait 时候它首先要检查下当前线程是否是锁的拥有者,不是则抛出 IllegalMonitorStateExcept。) 

但是,这怎么可能？等待线程在同步块里面执行的时候,不是一直持有监视器对象 (myMonitor 对象) 的锁吗？等待线程不能阻塞唤醒线程进入 doNotify()的同步块吗？答案是: 的确不能。一旦线程调用了 wait()方法,它就释放了所持有的监视器对象上的锁。这将允许其他线程也可以调用 wait()或者 notify()。

一旦一个线程被唤醒,不能立刻就退出 wait()的方法调用,直到调用 notify()的线程退出了它自己的同步块。换句话说: 被唤醒的线程必须重新获得监视器对象的锁,才可以退出 wait()的方法调用,因为 wait 方法调用运行在同步块里面。如果多个线程被 notifyAll()唤醒,那么在同一时刻将只有一个线程可以退出 wait()方法,因为每个线程在退出 wait()前必须获得监视器对象的锁。

丢失的信号 (Missed Signals) 
  
notify()和 notifyAll()方法不会保存调用它们的方法,因为当这两个方法被调用时,有可能没有线程处于等待状态。通知信号过后便丢弃了。因此,如果一个线程先于被通知线程调用 wait()前调用了 notify(),等待的线程将错过这个信号。这可能是也可能不是个问题。不过,在某些情况下,这可能使等待线程永远在等待,不再醒来,因为线程错过了唤醒信号。

为了避免丢失信号,必须把它们保存在信号类里。在 MyWaitNotify 的例子中,通知信号应被存储在 MyWaitNotify 实例的一个成员变量里。以下是 MyWaitNotify 的修改版本: 

public class MyWaitNotify2{

MonitorObject myMonitorObject = new MonitorObject();
    
boolean wasSignalled = false;

public void doWait(){
      
synchronized(myMonitorObject){
        
if(!wasSignalled){
          
try{
            
myMonitorObject.wait();
           
} catch(InterruptedException e){...}
        
}
        
//clear signal and continue running.
        
wasSignalled = false;
      
}
    
}

public void doNotify(){
      
synchronized(myMonitorObject){
        
wasSignalled = true;
        
myMonitorObject.notify();
      
}
    
}
  
}
  
留意 doNotify()方法在调用 notify()前把 wasSignalled 变量设为 true。同时,留意 doWait()方法在调用 wait()前会检查 wasSignalled 变量。事实上,如果没有信号在前一次 doWait()调用和这次 doWait()调用之间的时间段里被接收到,它将只调用 wait()。

 (校注: 为了避免信号丢失, 用一个变量来保存是否被通知过。在 notify 前,设置自己已经被通知过。在 wait 后,设置自己没有被通知过,需要等待通知。) 

假唤醒
  
由于莫名其妙的原因,线程有可能在没有调用过 notify()和 notifyAll()的情况下醒来。这就是所谓的假唤醒 (spurious wakeups) 。无端端地醒过来了。

如果在 MyWaitNotify2 的 doWait()方法里发生了假唤醒,等待线程即使没有收到正确的信号,也能够执行后续的操作。这可能导致你的应用程序出现严重问题。

为了防止假唤醒,保存信号的成员变量将在一个 while 循环里接受检查,而不是在 if 表达式里。这样的一个 while 循环叫做自旋锁 (校注: 这种做法要慎重,目前的 JVM 实现自旋会消耗 CPU,如果长时间不调用 doNotify 方法,doWait 方法会一直自旋,CPU 会消耗太大) 。被唤醒的线程会自旋直到自旋锁(while 循环)里的条件变为 false。以下 MyWaitNotify2 的修改版本展示了这点: 

public class MyWaitNotify3{

MonitorObject myMonitorObject = new MonitorObject();
    
boolean wasSignalled = false;

public void doWait(){
      
synchronized(myMonitorObject){
        
while(!wasSignalled){
          
try{
            
myMonitorObject.wait();
           
} catch(InterruptedException e){...}
        
}
        
//clear signal and continue running.
        
wasSignalled = false;
      
}
    
}

public void doNotify(){
      
synchronized(myMonitorObject){
        
wasSignalled = true;
        
myMonitorObject.notify();
      
}
    
}
  
}
  
留意 wait()方法是在 while 循环里,而不在 if 表达式里。如果等待线程没有收到信号就唤醒,wasSignalled 变量将变为 false,while 循环会再执行一次,促使醒来的线程回到等待状态。

不要在字符串常量或全局对象中调用 wait()
  
 (校注: 本章说的字符串常量指的是值为常量的变量) 

本文早期的一个版本在 MyWaitNotify 例子里使用字符串常量 ("") 作为管程对象。以下是那个例子: 

public class MyWaitNotify{

String myMonitorObject = "";
    
boolean wasSignalled = false;

public void doWait(){
      
synchronized(myMonitorObject){
        
while(!wasSignalled){
          
try{
            
myMonitorObject.wait();
           
} catch(InterruptedException e){...}
        
}
        
//clear signal and continue running.
        
wasSignalled = false;
      
}
    
}

public void doNotify(){
      
synchronized(myMonitorObject){
        
wasSignalled = true;
        
myMonitorObject.notify();
      
}
    
}
  
}
  
在空字符串作为锁的同步块(或者其他常量字符串)里调用 wait()和 notify()产生的问题是,JVM/编译器内部会把常量字符串转换成同一个对象。这意味着,即使你有 2 个不同的 MyWaitNotify 实例,它们都引用了相同的空字符串实例。同时也意味着存在这样的风险: 在第一个 MyWaitNotify 实例上调用 doWait()的线程会被在第二个 MyWaitNotify 实例上调用 doNotify()的线程唤醒。这种情况可以画成以下这张图: 

起初这可能不像个大问题。毕竟,如果 doNotify()在第二个 MyWaitNotify 实例上被调用,真正发生的事不外乎线程 A 和 B 被错误的唤醒了 。这个被唤醒的线程 (A 或者 B) 将在 while 循环里检查信号值,然后回到等待状态,因为 doNotify()并没有在第一个 MyWaitNotify 实例上调用,而这个正是它要等待的实例。这种情况相当于引发了一次假唤醒。线程 A 或者 B 在信号值没有更新的情况下唤醒。但是代码处理了这种情况,所以线程回到了等待状态。记住,即使 4 个线程在相同的共享字符串实例上调用 wait()和 notify(),doWait()和 doNotify()里的信号还会被 2 个 MyWaitNotify 实例分别保存。在 MyWaitNotify1 上的一次 doNotify()调用可能唤醒 MyWaitNotify2 的线程,但是信号值只会保存在 MyWaitNotify1 里。

问题在于,由于 doNotify()仅调用了 notify()而不是 notifyAll(),即使有 4 个线程在相同的字符串 (空字符串) 实例上等待,只能有一个线程被唤醒。所以,如果线程 A 或 B 被发给 C 或 D 的信号唤醒,它会检查自己的信号值,看看有没有信号被接收到,然后回到等待状态。而 C 和 D 都没被唤醒来检查它们实际上接收到的信号值,这样信号便丢失了。这种情况相当于前面所说的丢失信号的问题。C 和 D 被发送过信号,只是都不能对信号作出回应。

如果 doNotify()方法调用 notifyAll(),而非 notify(),所有等待线程都会被唤醒并依次检查信号值。线程 A 和 B 将回到等待状态,但是 C 或 D 只有一个线程注意到信号,并退出 doWait()方法调用。C 或 D 中的另一个将回到等待状态,因为获得信号的线程在退出 doWait()的过程中清除了信号值(置为 false)。

看过上面这段后,你可能会设法使用 notifyAll()来代替 notify(),但是这在性能上是个坏主意。在只有一个线程能对信号进行响应的情况下,没有理由每次都去唤醒所有线程。

所以: 在 wait()/notify()机制中,不要使用全局对象,字符串常量等。应该使用对应唯一的对象。例如,每一个 MyWaitNotify3 的实例 (前一节的例子) 拥有一个属于自己的监视器对象,而不是在空字符串上调用 wait()/notify()。

校注: 

管程 (英语: Monitors,也称为监视器) 是对多个工作线程实现互斥访问共享资源的对象或模块。这些共享资源一般是硬件设备或一群变量。管程实现了在一个时间点,最多只有一个线程在执行它的某个子程序。与那些通过修改数据结构实现互斥访问的并发程序设计相比,管程很大程度上简化了程序设计。