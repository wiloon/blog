---
title: Android Handler
author: "-"
date: 2014-08-13T08:28:06+00:00
url: /?p=6939
categories:
  - Uncategorized

tags:
  - reprint
---
## Android Handler
http://www.cnblogs.com/devinzhang/archive/2011/12/30/2306980.html

Android之Handler用法总结

方法一: (java习惯，在android平台开发时这样是不行的，因为它违背了单线程模型) 

刚刚开始接触android线程编程的时候，习惯好像java一样，试图用下面的代码解决问题

new Thread( new Runnable() {
  
public void run() {
  
myView.invalidate();
  
}
  
}).start();
  
可以实现功能，刷新UI界面。但是这样是不行的，因为它违背了单线程模型: Android UI操作并不是线程安全的并且这些操作必须在UI线程中执行。

方法二:  (Thread+Handler)

查阅了文档和apidemo后，发觉常用的方法是利用Handler来实现UI线程的更新的。

Handler来根据接收的消息，处理UI更新。Thread线程发出Handler消息，通知更新UI。

复制代码
  
Handler myHandler = new Handler() {
  
public void handleMessage(Message msg) {
  
switch (msg.what) {
  
case TestHandler.GUIUPDATEIDENTIFIER:
  
myBounceView.invalidate();
  
break;
  
}
  
super.handleMessage(msg);
  
}
  
};
  
复制代码

复制代码
  
class myThread implements Runnable {
  
public void run() {
  
while (!Thread.currentThread().isInterrupted()) {

Message message = new Message();
  
message.what = TestHandler.GUIUPDATEIDENTIFIER;

TestHandler.this.myHandler.sendMessage(message);
  
try {
  
Thread.sleep(100);
  
} catch (InterruptedException e) {
  
Thread.currentThread().interrupt();
  
}
  
}
  
}
  
}
  
复制代码
  
以上方法demo看:http://rayleung.javaeye.com/blog/411860

方法三:  (java习惯。Android平台中，这样做是不行的，这跟Android的线程安全有关) 

在Android平台中需要反复按周期执行方法可以使用Java上自带的TimerTask类，TimerTask相对于Thread来说对于资源消耗的更低，除了使用Android自带的AlarmManager使用Timer定时器是一种更好的解决方法。 我们需要引入import java.util.Timer; 和 import java.util.TimerTask;

复制代码
  
public class JavaTimer extends Activity {

Timer timer = new Timer();
  
TimerTask task = new TimerTask(){
  
public void run() {
  
setTitle("hear me?");
  
}
  
};

public void onCreate(Bundle savedInstanceState) {
  
super.onCreate(savedInstanceState);
  
setContentView(R.layout.main);

timer.schedule(task, 10000);

}
  
}
  
复制代码

方法四: (TimerTask + Handler)

通过配合Handler来实现timer功能的！

复制代码
  
public class TestTimer extends Activity {

Timer timer = new Timer();
  
Handler handler = new Handler(){
  
public void handleMessage(Message msg) {
  
switch (msg.what) {
  
case 1:
  
setTitle("hear me?");
  
break;
  
}
  
super.handleMessage(msg);
  
}

};

TimerTask task = new TimerTask(){
  
public void run() {
  
Message message = new Message();
  
message.what = 1;
  
handler.sendMessage(message);
  
}
  
};

public void onCreate(Bundle savedInstanceState) {
  
super.onCreate(savedInstanceState);
  
setContentView(R.layout.main);

timer.schedule(task, 10000);
  
}
  
}
  
复制代码

方法五: ( Runnable + Handler.postDelayed(runnable,time) )

在Android里定时更新 UI，通常使用的是 java.util.Timer, java.util.TimerTask, android.os.Handler组合。实际上Handler 自身已经提供了定时的功能。

复制代码
  
private Handler handler = new Handler();

private Runnable myRunnable= new Runnable() {
  
public void run() {

if (run) {
  
handler.postDelayed(this, 1000);
  
count++;
  
}
  
tvCounter.setText("Count: " + count);

}
  
};
  
复制代码
  
然后在其他地方调用

handler.post(myRunnable);

handler.post(myRunnable,time);

案例看: http://shaobin0604.javaeye.com/blog/515820

====================================================================

知识点总结补充: 

很多初入Android或Java开发的新手对Thread、Looper、Handler和Message仍然比较迷惑，衍生的有HandlerThread、java.util.concurrent、Task、AsyncTask由于目前市面上的书籍等资料都没有谈到这些问题，今天就这一问题做更系统性的总结。我们创建的Service、Activity以及Broadcast均是一个主线程处理，这里我们可以理解为UI线程。但是在操作一些耗时操作时，比如I/O读写的大文件读写，数据库操作以及网络下载需要很长时间，为了不阻塞用户界面，出现ANR的响应提示窗口，这个时候我们可以考虑使用Thread线程来解决。

对于从事过J2ME开发的程序员来说Thread比较简单，直接匿名创建重写run方法，调用start方法执行即可。或者从Runnable接口继承，但对于Android平台来说UI控件都没有设计成为线程安全类型，所以需要引入一些同步的机制来使其刷新，这点Google在设计Android时倒是参考了下Win32的消息处理机制。

1. 对于线程中的刷新一个View为基类的界面，可以使用postInvalidate()方法在线程中来处理，其中还提供了一些重写方法比如postInvalidate(int left,int top,int right,int bottom) 来刷新一个矩形区域，以及延时执行，比如postInvalidateDelayed(long delayMilliseconds)或postInvalidateDelayed(long delayMilliseconds,int left,int top,int right,int bottom) 方法，其中第一个参数为毫秒

2. 当然推荐的方法是通过一个Handler来处理这些，可以在一个线程的run方法中调用handler对象的 postMessage或sendMessage方法来实现，Android程序内部维护着一个消息队列，会轮训处理这些，如果你是Win32程序员可以很好理解这些消息处理，不过相对于Android来说没有提供 PreTranslateMessage这些干涉内部的方法。

3. Looper又是什么呢? ，其实Android中每一个Thread都跟着一个Looper，Looper可以帮助Thread维护一个消息队列，但是Looper和Handler没有什么关系，我们从开源的代码可以看到Android还提供了一个Thread继承类HanderThread可以帮助我们处理，在HandlerThread对象中可以通过getLooper方法获取一个Looper对象控制句柄，我们可以将其这个Looper对象映射到一个Handler中去来实现一个线程同步机制，Looper对象的执行需要初始化Looper.prepare方法就是昨天我们看到的问题，同时推出时还要释放资源，使用Looper.release方法。

4.Message 在Android是什么呢? 对于Android中Handler可以传递一些内容，通过Bundle对象可以封装String、Integer以及Blob二进制对象，我们通过在线程中使用Handler对象的sendEmptyMessage或sendMessage方法来传递一个Bundle对象到Handler处理器。对于Handler类提供了重写方法handleMessage(Message msg) 来判断，通过msg.what来区分每条信息。将Bundle解包来实现Handler类更新UI线程中的内容实现控件的刷新操作。相关的Handler对象有关消息发送sendXXXX相关方法如下，同时还有postXXXX相关方法，这些和Win32中的道理基本一致，一个为发送后直接返回，一个为处理后才返回 .

5. java.util.concurrent对象分析，对于过去从事Java开发的程序员不会对Concurrent对象感到陌生吧，他是JDK 1.5以后新增的重要特性作为掌上设备，我们不提倡使用该类，考虑到Android为我们已经设计好的Task机制，这里不做过多的赘述，相关原因参考下面的介绍:

6. 在Android中还提供了一种有别于线程的处理方式，就是Task以及AsyncTask，从开源代码中可以看到是针对Concurrent的封装，开发人员可以方便的处理这些异步任务。

摘录自: http://www.cnblogs.com/playing/archive/2011/03/24/1993583.html