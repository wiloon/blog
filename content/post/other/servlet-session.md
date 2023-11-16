---
title: Servlet Session
author: "-"
date: 2012-06-22T06:08:16+00:00
url: /?p=3594
categories:
  - Java
  - Web
tags:
  - reprint
---
## Servlet Session
[http://developer.51cto.com/art/200907/134673.htm](http://developer.51cto.com/art/200907/134673.htm)

本文向您介绍Servlet Session机制，包括会话管理机制、事件监听等，并结合具体的示例讲解了一个基于Servlet Session登陆系统的实现。
  
    一、           Servlet的会话管理机制
  

  
    HttpSession接口提供了存储和返回标准会话属性的方法。标准会话属性如会话标识符、应用数据等，都以"键-值"对的形式保存。简而言之，HttpSession接口提供了一种把对象保存到内存、在同一用户的后继请求中提取这些对象的标准办法。在会话中保存数据的方法是setAttribute(String s, Object o)，从会话提取原来所保存对象的方法是getAttribute(String s)。
  
  
    每当新用户请求一个使用了HttpSession对象的JSP页面，JSP容器除了发回应答页面之外，它还要向浏览器发送一个特殊的数字。这个特殊的数字称为"会话标识符"，它是一个唯一的用户标识符。此后，HttpSession对象就驻留在内存之中，等待同一用户返回时再次调用它的方法。
  
  
    在客户端，浏览器保存会话标识符，并在每一个后继请求中把这个会话标识符发送给服务器。会话标识符告诉JSP容器当前请求不是用户发出的第一个请求，服务器以前已经为该用户创建了HttpSession对象。此时，JSP容器不再为用户创建新的HttpSession对象，而是寻找具有相同会话标识符的HttpSession对象，然后建立该HttpSession对象和当前请求的关联。
  
  
    会话标识符以Cookie的形式在服务器和浏览器之间传送。如果客户端不支持cookie，运用url改写机制来保证会话标识符传回服务器。
  
  
    二、           Servlet Session事件侦听
  
  
    HttpSessionBindingEvent类
 定义
 public class HttpSessionBindingEvent extends EventObject
 这个事件是在监听到HttpSession发生绑定和取消绑定的情况时连通HttpSessionBindingListener的。这可能是一个session被终止或被认定无效的结果。
 事件源是HttpSession.putValue或HttpSession.removeValue。
 构造函数
 public HttpSessionBindingEvent(HttpSession session, String name);
 通过引起这个事件的Session和发生绑定或取消绑定的对象名构造一个新的HttpSessionBindingEvent。
 方法
 1、getName
 public String getName();
 返回发生绑定和取消绑定的对象的名字。
 2、getSession
 public HttpSession getSession();
 返回发生绑定和取消绑定的session的名字。
 HttpSessionBindingListener接口
 定义
 public interface HttpSessionBindingListener
       这个对象被加入到HTTP的session中，执行这个接口会通告有没有什么对象被绑定到这个HTTP session中或被从这个HTTP session中取消绑定。
 方法
 1、valueBound
 public void valueBound(HttpSessionBindingEvent event);
 当一个对象被绑定到session中，调用此方法。HttpSession.putValue方法被调用时，Servlet引擎应该调用此方法。
 2、valueUnbound
 public void valueUnbound(HttpSessionBindingEvent event);
 当一个对象被从session中取消绑定，调用此方法。HttpSession.removeValue方法被调用时，Servlet引擎应该调用此方法。
  
  
    Session的事件处理机制与swing事件处理机制不同。Swing采用注册机制，而session没有；当任一session发生绑定或其他事件时，都会触发HttpSessionBindingEvent ，如果servlet容器中存在HttpSessionBindingListener的实现类，则会将事件作为参数传送给session侦听器的实现类。在HttpSessionBindingEvent 中可以通过getsession得到发生绑定和取消绑定的session的名字，而侦听器可以据此做更多处理。
  
  
    因此，对session的事件侦听，只需实现HttpSessionBindingListener即可。
  
  
    从servlet2.3增加了
  
  
    HttpSessionEvent (This is the class representing event notifications for changes to sessions within a web application) 
  
  
    HttpSessionActivationListener (Objects that are bound to a session may listen to container events notifying them that sessions will be passivated and that session will be activated.) 
  
  
    HttpSessionAttributeListener (This listener interface can be implemented in order to get notifications of changes to the attribute lists of sessions within this web application.) 
  
  
    分别执行不同的任务，处理基本相同。
  
  
    三、           例子 (zz) 
  
  
    捕获Servlet Session事件的意义: 
 1、 记录网站的客户登录日志 (登录，退出信息等) 
 2、 统计在线人数
 3、 等等还有很多，呵呵，自己想吧……总之挺重要的。
 Session代表客户的会话过程，客户登录时，往Session中传入一个对象，即可跟踪客户的会话。在Servlet中，传入Session的对象如果是一个实现HttpSessionBindingListener接口的对象 (方便起见，此对象称为监听器) ，则在传入的时候 (即调用HttpSession对象的setAttribute方法的时候) 和移去的时候 (即调用HttpSession对象的removeAttribute方法的时候或Session Time out的时候) Session对象会自动调用监听器的valueBound和valueUnbound方法 (这是HttpSessionBindingListener接口中的方法) 。由此可知，登录日志也就不难实现了。
 另外一个问题是，如何统计在线人数，这个问题跟实现登录日志稍微有点不同，统计在线人数 (及其信息) ，就是统计现在有多少个Session实例存在，我们可以增加一个计数器 (如果想存储更多的信息，可以用一个对象来做计数器，随后给出的实例中，简单起见，用一个整数变量作为计数器) ，通过在valueBound方法中给计数器加1，valueUnbound方法中计数器减1，即可实现在线人数的统计。当然，这里面要利用到ServletContext的全局特性。(有关ServletContext的叙述请参考Servlet规范)，新建一个监听器，并将其实例存入ServletContext的属性中，以保证此监听器实例的唯一性，当客户登录时，先判断ServletContext的这个属性是否为空，如果不为空，证明已经创建，直接将此属性取出放入Session中，计数器加1；如果为空则创建一个新的监听器，并存入ServletContext的属性中。
 举例说明: 
 实现一个监听器: 
  
  
    
      
        
          
            // SessionListener.java
          
          
          
            import java.io.*;
          
          
          
            import java.util.*;
          
          
          
            import javax.servlet.http.*;
          
          
          
            //监听登录的整个过程
          
          
          
            public class SessionListener implements HttpSessionBindingListener
          
          
          
            {
          
          
          
            public String privateInfo=""; //生成监听器的初始化参数字符串
          
          
          
            private String logString=""; //日志记录字符串
          
          
          
            private int count=0; //登录人数计数器
          
          
          
            public SessionListener(String info){
          
          
          
            this.privateInfo=info;
          
          
          
            }
          
          
          
            public int getCount(){
          
          
          
            return count;
          
          
          
            }
          
          
          
            public void valueBound(HttpSessionBindingEvent event)
          
          
          
            {
          
          
          
            count++;
          
          
          
            if (privateInfo.equals("count"))
          
          
          
            {
          
          
          
            return;
          
          
          
            }
          
          
          
            try{
          
          
          
            Calendar calendar=new GregorianCalendar();
          
          
          
            System.out.println("LOGIN:"+privateInfo+" TIME:"+calendar.getTime());
          
          
          
            logString="nLOGIN:"+privateInfo+" TIME:"+calendar.getTime()+"n";
          
          
          
            for(int i=1;i<1000;i++){
          
          
          
            File file=new File("yeeyoo.log"+i);
          
          
          
            if(!(file.exists()))
          
          
          
            file.createNewFile(); //如果文件不存在，创建此文件
          
          
          
            if(file.length()>1048576) //如果文件大于1M，重新创建一个文件
          
          
          
            continue;
          
          
          
            FileOutputStream foo=new FileOutputStream("yeeyoo.log"+i,true);
          
          
          
            //以append方式打开创建文件
          
          
          
            foo.write(logString.getBytes(),0,logString.length()); //写入日志字符串
          
          
          
            foo.close();
          
          
          
            break;//退出
          
          
          
            }
          
          
          
            }catch(FileNotFoundException e){}
          
          
          
            catch(IOException e){}
          
          
          
            }
          
          
          
            public void valueUnbound(HttpSessionBindingEvent event)
          
          
          
            {
          
          
          
            count-;
          
          
          
            if (privateInfo.equals("count"))
          
          
          
            {
          
          
          
            return;
          
          
          
            }
          
          
          
            try{
          
          
          
            Calendar calendar=new GregorianCalendar();
          
          
          
            System.out.println("LOGOUT:"+privateInfo+" TIME:"+calendar.getTime());
          
          
          
            logString="nLOGOUT:"+privateInfo+" TIME:"+calendar.getTime()+"n";
          
          
          
            for(int i=1;i<1000;i++){
          
          
          
            File file=new File("yeeyoo.log"+i);
          
          
          
            if(!(file.exists()))
          
          
          
            file.createNewFile(); //如果文件不存在，创建此文件
          
          
          
            if(file.length()>1048576) //如果文件大于1M，重新创建一个文件
          
          
          
            continue;
          
          
          
            FileOutputStream foo=new FileOutputStream("yeeyoo.log"+i,true);
          
          
          
            //以append方式打开创建文件
          
          
          
            foo.write(logString.getBytes(),0,logString.length()); //写入日志字符串
          
          
          
            foo.close();
          
          
          
            break;//退出
          
          
          
            }
          
          
          
            }catch(FileNotFoundException e){}
          
          
          
            catch(IOException e){}
          
          
          
            }
          
          
          
            }
          
        
      
    
  
  
    登录日志的实现: 
 下面再来看看我们的登录Servlet中使用这个监听器的部分源代码: 
  
  
    
      
        
          
            ……
          
          
          
            HttpSession session = req.getSession (true);
          
          
          
            ……
          
          
          
            //////////////////////////////////////////////////////////////////
          
          
          
            SessionListener sessionListener=
          
          
          
               new SessionListener("IP:"+req.getRemoteAddr());
          
          
          
            //对于每一个会话过程均启动一个监听器
          
          
          
            session.setAttribute("listener",sessionListener);
          
          
          
            //将监听器植入HttpSession，这将激发监听器调用valueBound方法，
          
          
          
            //从而记录日志文件。
          
          
          
            //////////////////////////////////////////////////////////////////
          
        
      
    
  
  
    当系统退出登录时，只需简单地调用session.removeAttribute("listener");
 即可自动调用监听器的valueUnbound方法。或者，当Session Time Out的时候也会调用此方法。
 登录人数的统计: 
  
  
    
      
        
          
            ServletContext session1=getServletConfig().getServletContext();
          
          
          
            //取得ServletContext对象实例
          
          
          
            if((SessionListener)session1.getAttribute("listener1")==null)
          
          
          
            {
          
          
          
            SessionListener sessionListener1=new SessionListener("count");
          
          
          
            //只设置一次，不同于上面日志文件的记录每次会话均设置。
          
          
          
            //即当第一个客户连接到服务器时启动一个全局变量，
          
          
          
            //此后所有的客户将使用相同的上下文。
          
          
          
            session1.setAttribute("listener1",sessionListener1);
          
          
          
            //将监听器对象设置成ServletContext的属性，具有全局范围有效性，
          
          
          
            //即所有的客户均可以取得它的实例。
          
          
          
            }
          
          
          
            session.setAttribute("listener1",(SessionListener)session1.
          
          
          
            getAttribute("listener1"));
          
          
          
            //取出此全局对象，并且将此对象绑定到某个会话中，
          
          
          
            //此举将促使监听器调用valueBound，计数器加一。
          
        
      
    
  
  
    在此后的程序中随时可以用以下代码取得当前的登录人数: 
  
  
    
      
        
          
            ((SessionListener)session.getAttribute("listener1")).getCount()
          
        
      
    
  
  
    Servlet Session中的getCount()是监听器的一个方法，即取得当前计数器的值也就是登录人数了。
  
