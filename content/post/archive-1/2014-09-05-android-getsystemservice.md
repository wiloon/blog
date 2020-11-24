---
title: android getSystemService
author: w1100n
type: post
date: 2014-09-05T01:40:37+00:00
url: /?p=6979
categories:
  - Uncategorized

---
http://blog.sina.com.cn/s/blog_7cb2c5d50101c26t.html

android中getSystemService详解 (2012-07-23 10:53:52)转载▼
  
标签： java android it 分类： android
  
http://blog.sina.com.cn/s/blog_71d1e4fc0100o8qr.html
  
http://blog.csdn.net/bianhaohui/article/details/6220135

android的后台运行在很多service，它们在系统启动时被SystemServer开启，支持系统的正常工作，比如MountService监听是否有SD卡安装及移除，ClipboardService提供剪切板功能，PackageManagerService提供软件包的安装移除及查看等等，应用程序可以通过系统提供的Manager接口来访问这些Service提供的数据。

getSystemService是Android很重要的一个API，它是Activity的一个方法，根据传入的NAME来取得对应的Object，然后转换成相应的服务对象。以下介绍系统相应的服务。

传入的Name | 返回的对象 | 说明
  
WINDOW_SERVICE WindowManager 管理打开的窗口程序

LAYOUT\_INFLATER\_SERVICE LayoutInflater 取得xml里定义的view

ACTIVITY_SERVICE ActivityManager 管理应用程序的系统状态

POWER_SERVICE PowerManger 电源的服务

ALARM_SERVICE AlarmManager 闹钟的服务

NOTIFICATION_SERVICE NotificationManager 状态栏的服务

KEYGUARD_SERVICE KeyguardManager 键盘锁的服务

LOCATION_SERVICE LocationManager 位置的服务，如GPS

SEARCH_SERVICE SearchManager 搜索的服务

VEBRATOR_SERVICE Vebrator 手机震动的服务

CONNECTIVITY_SERVICE Connectivity 网络连接的服务

WIFI_SERVICE WifiManager Wi-Fi服务

TELEPHONY_SERVICE TeleponyManager 电话服务
  
Currently available names are:
  
WINDOW_SERVICE ("window")
  
The top-level window manager in which you can place custom windows. The returned object is a WindowManager.

LAYOUT\_INFLATER\_SERVICE ("layout_inflater")
  
A LayoutInflater for inflating layout resources in this context.

ACTIVITY_SERVICE ("activity")
  
A ActivityManager for interacting with the global activity state of the system.

POWER_SERVICE ("power")
  
A PowerManager for controlling power management.

ALARM_SERVICE ("alarm")
  
A AlarmManager for receiving intents at the time of your choosing.

NOTIFICATION_SERVICE ("notification")
  
A NotificationManager for informing the user of background events.

KEYGUARD_SERVICE ("keyguard")
  
A KeyguardManager for controlling keyguard.

LOCATION_SERVICE ("location")
  
A LocationManager for controlling location (e.g., GPS) updates.

SEARCH_SERVICE ("search")
  
A SearchManager for handling search.

VIBRATOR_SERVICE ("vibrator")
  
A Vibrator for interacting with the vibrator hardware.

CONNECTIVITY_SERVICE ("connection")
  
A ConnectivityManager for handling management of network connections.

WIFI_SERVICE ("wifi")
  
A WifiManager for management of Wi-Fi connectivity.

INPUT\_METHOD\_SERVICE ("input_method")
  
An InputMethodManager for management of input methods.

UI\_MODE\_SERVICE ("uimode")
  
An UiModeManager for controlling UI modes.

DOWNLOAD_SERVICE ("download")
  
A DownloadManager for requesting HTTP downloads

Note: System services obtained via this API may be closely associated with the Context in which they are obtained from. In general, do not share the service objects between various different contexts (Activities, Applications, Services, Providers, etc.)

一个例子：
  
在android 获取手机信息的时候用到这样一段代码：

public class BasicInfo {

public String getPhoneNumber()
  
{
  
// 获取手机号 MSISDN，很可能为空
  
TelephonyManager tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
  
StringBuffer inf = new StringBuffer();
  
switch(tm.getSimState()){ //getSimState()取得sim的状态 有下面6中状态
  
case TelephonyManager.SIM\_STATE\_ABSENT :inf.append("无卡");return inf.toString();
  
case TelephonyManager.SIM\_STATE\_UNKNOWN :inf.append("未知状态");return inf.toString();
  
case TelephonyManager.SIM\_STATE\_NETWORK_LOCKED :inf.append("需要NetworkPIN解锁");return inf.toString();
  
case TelephonyManager.SIM\_STATE\_PIN_REQUIRED :inf.append("需要PIN解锁");return inf.toString();
  
case TelephonyManager.SIM\_STATE\_PUK_REQUIRED :inf.append("需要PUK解锁");return inf.toString();
  
case TelephonyManager.SIM\_STATE\_READY :break;
  
}

String phoneNumber = tm.getLine1Number();
  
return phoneNumber;
  
}

在另外一个activity类里面调用的时候 总是出现进程关闭 无法获取手机信息。后来发现

getSystemService这个方法基于context,只有存在TextView控件的窗体中这个方法才会被激活~

于是：
  
1. 给BasicInfo 添加一个带参数Context的构造函数：
  
public BasicInfo (Context context)
  
{
  
this.context = context;
  
}

2. getPhoneNumber()函数里面改成：
  
context.getSystemService(Context.TELEPHONY_SERVIC);

3. 在调用类里面 BasicInfo bi = new BasicInfo(this);
  
bi.getPhoneNumber();