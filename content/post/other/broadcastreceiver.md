---
title: BroadCastReceiver
author: "-"
date: 2014-07-31T02:15:00+00:00
url: /?p=6861
categories:
  - Inbox
tags:
  - reprint
---
## BroadCastReceiver
http://yangguangfu.iteye.com/blog/1063732

Android 中的BroadCastReceiver

作者: 阿福
  
BroadCastReceiver 简介  (末尾有源码) 
  
BroadCastReceiver 源码位于:  framework/base/core/java/android.content.BroadcastReceiver.java

广播接收者 ( BroadcastReceiver ) 用于接收广播 Intent ，广播 Intent 的发送是通过调用 Context.sendBroadcast() 、 Context.sendOrderedBroadcast() 来实现的。通常一个广播 Intent 可以被订阅了此 Intent 的多个广播接收者所接收。

广播是一种广泛运用的在应用程序之间传输信息的机制 。而 BroadcastReceiver 是对发送出来的广播进行过滤接收并响应的一类组件；

来自普通应用程序，如一个应用程序通知其他应用程序某些数据已经下载完毕。
  
BroadcastReceiver 自身并不实现图形用户界面，但是当它收到某个通知后， BroadcastReceiver 可以启动 Activity 作为响应，或者通过 NotificationMananger 提醒用户，或者启动 Service 等等。
  
BroadCastReceiver 的机制
  
1. 机制
  
在 Android 里面有各种各样的广播，比如电池的使用状态，电话的接收和短信的接收都会产生一个广播，应用程序开发者也可以监听这些广播并做出程序逻辑的处理。如图: 

2. 实现
  
用接收短信举例: 

第一种方式 : 
  
实现
  
public class MyBroadcastReceiver extends BroadcastReceiver {

// action 名称
  
String SMS_RECEIVED = "android.provider.Telephony.SMS_RECEIVED" ;

public void onReceive(Context context, Intent intent) {

if (intent.getAction().equals( SMS_RECEIVED )) {
  
// 相关处理 : 地域变换、电量不足、来电来信；
  
}
  
}
  
}
  
系统注册: 在 AndroidManifest.xml 中注册
  
< receiver android:name = ".MyBroadcastReceiver" >
  
< intent-filter android:priority = "1000" >

< action android:name = " android.provider.Telephony.SMS_RECEIVED" />
  
</ intent-filter >
  
</ receiver > 当然了需要权限 : 

< uses-permission android:name = "android.permission.RECEIVE_SMS" />
  
< uses-permission android:name = "android.permission.SEND_SMS" />

第二种方式: 

// 广播接收者 - 广播的接收
  
private BroadcastReceiver myBroadcastReceiver = new BroadcastReceiver() {

@Override
  
public void onReceive(Context context, Intent intent) {
  
// 相关处理，如收短信，监听电量变化信息
  
}

};

代码中注册: 
  
IntentFilter intentFilter = new IntentFilter( "android.provider.Telephony.SMS_RECEIVED " );
  
registerReceiver( mBatteryInfoReceiver , intentFilter);

3. 生命周期

描述了 Android 中广播的生命周期，其次它并不像 Activity 一样复杂，运行原理很简单如下图: 

生命周期只有十秒左右，如果在 onReceive() 内做超过十秒内的事情，就会报错 。

每次广播到来时 , 会重新创建 BroadcastReceiver 对象 , 并且调用 onReceive() 方法 , 执行完以后 , 该对象即被销毁 . 当 onReceive() 方法在 10 秒内没有执行完毕， Android 会认为该程序无响应 . 所以在
  
BroadcastReceiver 里不能做一些比较耗时的操作 , 否侧会弹出 ANR(Application No
  
Response) 的对话框 . 。 (如图) : 

怎么用好 BroadcastReceiver ？
  
如果需要完成一项比较耗时的工作 , 应该通过发送 Intent 给 Service, 由 Service 来完成 . 这里不能使用子线程来解决 , 因为 BroadcastReceiver 的生命周期很短 , 子线程可能还没有结束
  
BroadcastReceiver 就先结束了 .BroadcastReceiver 一旦结束 , 此时 BroadcastReceiver 的
  
所在进程很容易在系统需要内存时被优先杀死 , 因为它属于空进程 ( 没有任何活动组件的进程 ). 如果它的宿主进程被杀死 , 那么正在工作的子线程也会被杀死 . 所以采用子线程来解决是不可靠的 .

广播类型及广播的收发
  
广播类型
  
普通广播 (Normal broadcasts)
  
发送一个广播，所以监听该广播的广播接收者都可以监听到改广播。
  
异步广播 , 当处理完之后的Intent ，依然存在，这时候registerReceiver(BroadcastReceiver, IntentFilter) 还能收到他的值，直到你把它去掉 , 不能将处理结果传给下一个接收者 , 无法终止广播 .

有序广播 (Ordered broadcasts)
  
按照接收者的优先级顺序接收广播 , 优先级别在 intent-filter 中的 priority 中声明 ,-1000 到
  
1000 之间 , 值越大 , 优先级越高 . 可以终止广播意图的继续传播 . 接收者可以篡改内容 .