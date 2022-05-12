---
title: HttpSessionBindingListener
author: "-"
date: 2012-06-22T10:04:32+00:00
url: /?p=3609
categories:
  - Java
  - Web
tags:$
  - reprint
---
## HttpSessionBindingListener
捕获Session事件的意义: 
  
1.          记录网站的客户登录日志 (登录，退出信息等) 
  
2.          统计在线人数
  
3.          等等还有很多，呵呵，自己想吧……总之挺重要的。

Session代表客户的会话过程，客户登录时，往Session中传入一个对象，即可跟踪客户的会话。在Servlet中，传入Session的对象如果是一个实现HttpSessionBindingListener接口的对象 (方便起见，此对象称为监听器) ，则在传入的时候 (即调用HttpSession对象的setAttribute方法的时候) 和移去的时候 (即调用HttpSession对象的removeAttribute方法的时候或Session   Time   out的时候) Session对象会自动调用监听器的valueBound和valueUnbound方法 (这是HttpSessionBindingListener接口中的方法) 。
  
由此可知，登录日志也就不难实现了。
  
另外一个问题是，如何统计在线人数，这个问题跟实现登录日志稍微有点不同，统计在线人数 (及其信息) ，就是统计现在有多少个Session实例存在，我们可以增加一个计数器 (如果想存储更多的信息，可以用一个对象来做计数器，随后给出的实例中，简单起见，用一个整数变量作为计数器) ，通过在valueBound方法中给计数器加1，valueUnbound方法中计数器减1，即可实现在线人数的统计。当然，这里面要利用到ServletContext的全局特性。(有关ServletContext的叙述请参考Servlet规范)，新建一个监听器，并将其实例存入ServletContext的属性中，以保证此监听器实例的唯一性，当客户登录时，先判断ServletContext的这个属性是否为空，如果不为空，证明已经创建，直接将此属性取出放入Session中，计数器加1；如果为空则创建一个新的监听器，并存入ServletContext的属性中。

举例说明: 

实现一个监听器: 
  
//   SessionListener.java

import   java.io.*;
  
import   java.util.*;
  
import   javax.servlet.http.*;

//监听登录的整个过程
  
public   class   SessionListener   implements   HttpSessionBindingListener
  
{

public   String   privateInfo= " ";                 //生成监听器的初始化参数字符串
  
private   String   logString= " ";                 //日志记录字符串
  
private   int   count=0;                 //登录人数计数器

public   SessionListener(String   info){
  
this.privateInfo=info;
  
}

public   int   getCount(){
  
return   count;
  
}

public   void   valueBound(HttpSessionBindingEvent   event)
  
{
  
count++;
  
if   (privateInfo.equals( "count "))
  
{
  
return;
  
}
  
try{
  
Calendar   calendar=new   GregorianCalendar();
  
System.out.println( "LOGIN: "+privateInfo+ "   TIME: "+calendar.getTime());
  
logString= "nLOGIN: "+privateInfo+ "   TIME: "+calendar.getTime()+ "n ";
  
for(int   i=1;i <1000;i++){
  
File   file=new   File( "yeeyoo.log "+i);
  
if(!(file.exists()))
  
file.createNewFile();       //如果文件不存在，创建此文件
  
if(file.length()> 1048576)   //如果文件大于1M，重新创建一个文件
  
continue;
  
FileOutputStream   foo=new   FileOutputStream( "yeeyoo.log "+i,true);//以append方式打开创建文件
  
foo.write(logString.getBytes(),0,logString.length());   //写入日志字符串
  
foo.close();
  
break;//退出
  
}
  
}catch(FileNotFoundException   e){}
  
catch(IOException   e){}
  
}

public   void   valueUnbound(HttpSessionBindingEvent   event)
  
{
  
count-;
  
if   (privateInfo.equals( "count "))
  
{
  
return;
  
}
  
try{
  
Calendar   calendar=new   GregorianCalendar();
  
System.out.println( "LOGOUT: "+privateInfo+ "   TIME: "+calendar.getTime());
  
logString= "nLOGOUT: "+privateInfo+ "   TIME: "+calendar.getTime()+ "n ";
  
for(int   i=1;i <1000;i++){
  
File   file=new   File( "yeeyoo.log "+i);
  
if(!(file.exists()))
  
file.createNewFile();       //如果文件不存在，创建此文件
  
if(file.length()> 1048576)   //如果文件大于1M，重新创建一个文件
  
continue;
  
FileOutputStream   foo=new   FileOutputStream( "yeeyoo.log "+i,true);//以append方式打开创建文件
  
foo.write(logString.getBytes(),0,logString.length());   //写入日志字符串
  
foo.close();
  
break;//退出
  
}
  
}catch(FileNotFoundException   e){}
  
catch(IOException   e){}
  
}

}

登录日志的实现: 

下面再来看看我们的登录Servlet中使用这个监听器的部分源代码: 
  
……
  
HttpSession   session   =   req.getSession   (true);
  
……
  
///////////////////////////////////////////////////////////////////////
  
SessionListener   sessionListener=new   SessionListener( "   IP: "+req.getRemoteAddr());     //对于每一个会话过程均启动一个监听器
  
session.setAttribute( "listener ",sessionListener);     //将监听器植入HttpSession，这将激发监听器调用valueBound方法，从而记录日志文件。
  
///////////////////////////////////////////////////////////////////////
  
当系统退出登录时，只需简单地调用session.removeAttribute("listener");即可自动调用监听器的valueUnbound方法。或者，当Session   Time   Out的时候也会调用此方法。

登录人数的统计: 
  
ServletContext   session1=getServletConfig().getServletContext();//取得ServletContext对象实例
  
if((SessionListener)session1.getAttribute( "listener1 ")==null)
  
{
  
SessionListener   sessionListener1=new   SessionListener( "count ");//只设置一次，不同于上面日志文件的记录每次会话均设置。即当第一个客户连接到服务器时启动一个全局变量，此后所有的客户将使用相同的上下文。
  
session1.setAttribute( "listener1 ",sessionListener1);//将监听器对象设置成ServletContext的属性，具有全局范围有效性，即所有的客户均可以取得它的实例。
  
}
  
session.setAttribute( "listener1 ",(SessionListener)session1.getAttribute( "listener1 "));//取出此全局对象，并且将此对象绑定到某个会话中，此举将促使监听器调用valueBound，计数器加一。
  
在此后的程序中随时可以用以下代码取得当前的登录人数: 
  
((SessionListener)session.getAttribute( "listener1 ")).getCount()
  
getCount()是监听器的一个方法，即取得当前计数器的值也就是登录人数了。