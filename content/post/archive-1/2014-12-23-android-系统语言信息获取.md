---
title: Android 系统语言信息获取
author: "-"
date: 2014-12-23T03:09:27+00:00
url: /?p=7123
categories:
  - Uncategorized

---
## Android 系统语言信息获取
http://blog.csdn.net/netwalk/article/details/9796979

Android系统的当前系统语言，可以通过Locale类获取，主要方法: Locale.getDefault().getLanguage()，返回的是es或者zh；通过Locale.getDefault().getCountry()获取当前国家或地区，返回为CN或US；如果当前手机设置为中文- 中国，则使用此方法返回zh-CN，同理可得到其他语言与地区的信息。

//得到Android系统上的语言列表

Locale mSystemLanguageList[]= Locale.getAvailableLocales()。

使用getLanguage()方法和getCountry方法，获取系统设置的语言和区域。

//获取系统当前使用的语言

String lan =Locale.getDefault().getLanguage();

//获取区域

String country =Locale.getDefault().getCountry();

//设置成简体中文的时候，getLanguage()返回的是zh,getCountry()返回的是cn.

还有另外一种获取当前语言的方法: 


Localelocale = getResources().getConfiguration().locale;

String language =locale.getLanguage(); // 获得语言码

参考代码如下: 


```java view plaincopy
  
private Locale[] getSystemLanguageList(){
  
//获取Android系统上的语言列表
  
Locale mLanguagelist[] = Locale.getAvailableLocales();
  
return mLanguagelist;
  
}

private static String getCurrentLauguage(){
  
//获取系统当前使用的语言
  
String mCurrentLanguage = Locale.getDefault().getLanguage();
  
//设置成简体中文的时候，getLanguage()返回的是zh
  
return mCurrentLanguage;
  
}
  
private String getCurrentLauguageUseResources(){
  
/**
  
* 获得当前系统语言
  
*/
  
Locale locale = getResources().getConfiguration().locale;
  
String language = locale.getLanguage(); // 获得语言码
  
return language;
  
}