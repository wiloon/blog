---
title: ServletContextListener
author: "-"
date: 2012-06-22T02:25:48+00:00
url: /?p=3580
categories:
  - Java
  - Web
tags:
  - Servlet

---
## ServletContextListener
<http://www.cnblogs.com/kentyshang/archive/2007/06/26/795878.html>

ServletContextListener处理Web应用的 servlet上下文(context)的变化的通知。这可以解释为，好像有个人在服务器旁不断地通知我们服务器在发生什么事件。那当然需要监听者了。因 此，在通知上下文(context)初始化和销毁的时候，ServletContextListner非常有用。


  import javax.servlet.ServletContextListener;
import javax.servlet.ServletContextEvent;
import javax.servlet.*;

public	class MyListener implements ServletContextListener {

	private ServletContext context = null;

	/* 这个方法在Web应用服务被移除，没有能力再接受请求的时候被调用。
	 */
	public void contextDestroyed(ServletContextEvent event){
		//Output a simple message to the server's console
		System.out.println("The Simple Web App. Has Been Removed");
		this.context = null;

	}

	// 这个方法在Web应用服务做好接受请求的时候被调用。
	public void contextInitialized(ServletContextEvent event){
		this.context = event.getServletContext();

		//Output a simple message to the server's console
		System.out.println("The Simple Web App. Is Ready");

	}
}

<web-app>
	
		
			com.listeners.MyContextListener
		</listener-class>
	</listener>
	<servlet/>
	<servlet-mapping/>
</web-app>
----------------------------------------转载http://blog.csdn.net/ezerg/archive/2004/09/24/115894.aspx
  
    ServletContextListener接口有两方需要实现的方法:contextInitialized()和contextDestroyed();
  
  
    Listener,译为监听者.顾名思义,它会监听Servlet容器,当应用开始的时候它会调用contextInitialized()方法;
 当应用关闭的时候,它同样会调用contextDestroyed()方法.
  
  
    我们可以利用这个特性初始化一些信息,当然我们也可以利用Servlet类init()方法,并在配置文件中让它启动应用的时候
 就执行,并且在关闭的时候执行destroy()方法.但是继承此接口应该更符合容器的应用.
  
  
    举个简单的例子:在一些论坛,社区及聊天室当中,删除在线的超时用户就可以利用这个接口来实现.
 可以利用JAVA的TimerTask及Timer类来实现每隔一定的时间进行自动检测.
 实例代码如下:
  
  
    UserOnlineTimerTask.java
 ------
 package com.bcxy.servlet;
  
  
    import java.util.TimerTask;
  
  
    import org.apache.commons.logging.Log;
 import org.apache.commons.logging.LogFactory;
  
  
    public class UserOnlineTimerTask extends TimerTask {
  
  
    Log log = LogFactory.getLog(UserOnlineTimerTask.class);
  
  
    public void run() {
 // 删除超时在线用户
 log.info("删除在线的超时用户....");
  
  
    }
  
  
    }
 ------------
 ------------
 SysListener.java
 ------------
 package com.bcxy.servlet;
  
  
    import java.io.IOException;
 import java.util.Timer;
  
  
    import javax.servlet.ServletContextEvent;
 import javax.servlet.ServletContextListener;
 import javax.servlet.ServletException;
 import javax.servlet.ServletRequest;
 import javax.servlet.ServletResponse;
 import javax.servlet.http.HttpServlet;
  
  
    import org.apache.commons.logging.Log;
 import org.apache.commons.logging.LogFactory;
  
  
    public class SysListener
 extends HttpServlet
 implements ServletContextListener {
  
  
    Log log = LogFactory.getLog(SysListener.class);
 Timer timer = new Timer();
  
  
    public void service(ServletRequest request, ServletResponse response)
 throws ServletException, IOException {
 //
 }
  
  
    public void contextInitialized(ServletContextEvent sce) {
  
  
    log.info("initial context....");
  
  
    timer.schedule(new UserOnlineTimerTask(), 0, 10000);
  
  
    }
  
  
    public void contextDestroyed(ServletContextEvent sce) {
  
  
    log.info("destory context....");
  
  
    timer.cancel();
 }
  
  
    }
 -----------
  
  
    如果你没有使用log4j的话,你可以把log.info()改为System.out.println()会得到同样的结果.
  
