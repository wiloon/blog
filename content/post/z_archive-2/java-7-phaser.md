---
title: 'Java 7   Phaser'
author: "-"
date: 2017-09-27T06:05:52+00:00
url: /?p=11214
categories:
  - Inbox
tags:
  - reprint
---
## 'Java 7   Phaser'
http://www.oschina.net/question/12_35433

Java 7 引入了一个全新灵活的线程同步机制,名为 Phaser 。 如果你需要等待线程结束然后继续执行其他任务,那么 Phaser 是一个好的选择,接下来我们一步步来介绍 Phaser 的使用: 

首先看下面的代码: 

import java.util.ArrayList;
  
import java.util.Date;
  
import java.util.List;
  
import java.util.concurrent.Phaser;

public class PhaserExample {

public static void main(String[] args) throws InterruptedException {

List<runnable> tasks = new ArrayList<>();

for (int i = 0; i < 2; i++) {

Runnable runnable = new Runnable() {
      
@Override
      
public void run() {
       
int a = 0, b = 1;
       
for (int i = 0; i < 2000000000; i++) {
        
a = a + b;
        
b = a - b;
       
}
      
}
     
};

tasks.add(runnable);

}

new PhaserExample().runTasks(tasks);

}

void runTasks(List<runnable> tasks) throws InterruptedException {

final Phaser phaser = new Phaser(1) {
     
protected boolean onAdvance(int phase, int registeredParties) {
      
return phase >= 1 || registeredParties == 0;
     
}
    
};

for (final Runnable task : tasks) {
     
phaser.register();
     
new Thread() {
      
public void run() {
       
do {
        
phaser.arriveAndAwaitAdvance();
        
task.run();
       
} while (!phaser.isTerminated());
      
}
     
}.start();
     
Thread.sleep(500);
    
}

phaser.arriveAndDeregister();
   
}

}
  
这个例子让我们可以深入了解 Phaser 的使用,下面是对这个代码的分析: 

Line 8-27: main 方法创建了两个 Runnable 任务
  
Line 29: 任务列表当作参数传递给 runTasks 方法

runTasks 方法实际使用了一个 Phaser 用于同步任务,使得每个任务在并行执行之前必须先到达屏障(Barrier)。列表中的任务执行了两次,执行情况如下图所示: 

注意: "party" 是 Phaser 中的一个术语,相当于是线程的意思,当一个 party 到达,就是线程到达意思就是线程到了同步的屏障(Barrier)。
  
Line 35: create a Phaser that has one registered party (this means: at this time phaser expects one thread=party to arrive before it can start the execution cycle)
  
Line 36: implement the onAdvance-Method to explain that this task list is executed twice (done by: Line 37 says that it returns true if phase is equal or higher then 1)
  
Line 41: iterate over the list of tasks
  
Line 42: register this thread with the Phaser. Notice that a Phaser instance does not know the task instances. It's a simple counter of registered, unarrived and arrived parties, shared across participating threads. If two parties are registered then two parties must arrive at the phaser to be able to start the first cycle.
  
Line 46: tell the thread to wait at the barrier until the arrived parties equal the registered parties
  
Line 51: Just for demonstration purposes, this line delays execution. The original code snippet prints internal infos about the Phaser state to standard out.
  
Line 52: two tasks are registered, in total three parties are registered.
  
Line 54: deregister one party. This results in two registered parties and two arrived parties. This causes the threads waiting (Line 46) to execute the first cycle. (in fact the third party arrived while three were registered - but it does not make a difference)

原始的代码 存放在 Git 仓库中,执行的结果如下: 
  
After phaser init -> Registered: 1 - Unarrived: 1 - Arrived: 0 - Phase: 0
  
After register -> Registered: 2 - Unarrived: 2 - Arrived: 0 - Phase: 0
  
After arrival -> Registered: 2 - Unarrived: 1 - Arrived: 1 - Phase: 0
  
After register -> Registered: 3 - Unarrived: 2 - Arrived: 1 - Phase: 0
  
After arrival -> Registered: 3 - Unarrived: 1 - Arrived: 2 - Phase: 0
  
Before main thread arrives and deregisters -> Registered: 3 - Unarrived: 1 - Arrived: 2 - Phase: 0
  
On advance -> Registered: 2 - Unarrived: 0 - Arrived: 2 - Phase: 0
  
After main thread arrived and deregistered -> Registered: 2 - Unarrived: 2 - Arrived: 0 - Phase: 1
  
Main thread will terminate ...
  
Thread-0:go :Wed Dec 28 16:09:16 CET 2011
  
Thread-1:go :Wed Dec 28 16:09:16 CET 2011
  
Thread-0:done:Wed Dec 28 16:09:20 CET 2011
  
Thread-1:done:Wed Dec 28 16:09:20 CET 2011
  
On advance -> Registered: 2 - Unarrived: 0 - Arrived: 2 - Phase: 1
  
Thread-0:go :Wed Dec 28 16:09:20 CET 2011
  
Thread-1:go :Wed Dec 28 16:09:20 CET 2011
  
Thread-1:done:Wed Dec 28 16:09:23 CET 2011
  
Thread-0:done:Wed Dec 28 16:09:23 CET 2011
  
Line 1: when the Phaser is initialized in line 35 of the code snippet then one party is registered and none arrived
  
Line 2: after the first thread is registered in Line 42 in the code example there are two registered parties and two unarrived parties. Since no thread reached the barrier yet, no party is arrived.
  
Line 3: the first thread arrives and waits at the barrier (line 46 in the code snippet)
  
Line 4: register the second thread, three registered, two unarrived, one arrived
  
Line 5: the second thread arrived at the barrier, hence two arrived now
  
Line 7: one party is deregistered in the code line 54 of the code example, therefore onAdvance-Method is called and returns false. This starts the first cycle since registered parties equals arrived parties (i.e. two). Phase 1 is started -> cycle one (see image mark 1)
  
Line 8: since all threads are notified and start their work, two parties are unarrived again, non arrived
  
Line 14: After the threads executed their tasks once they arrive again (code line 46) the onAdvance-Method is called, now the 2nd cycle is executed

英文链接: http://niklasschlimm.blogspot.com/2011/12/java-7-understanding-phaser.html