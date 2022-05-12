---
title: HttpSessionListener
author: "-"
date: 2012-06-22T03:46:07+00:00
url: /?p=3591
categories:
  - Java
  - Web
tags:
  - reprint
---
## HttpSessionListener

     Session创建事件发生在每次一个新的session创建的时候，类似地Session失效事件发生在每次一个Session失效的时候。


  这个接口也只包含两个方法，分别对应于Session的创建和失效: 
 # public void sessionCreated(HttpSessionEvent se);
 # public void sessionDestroyed(HttpSessionEvent se); 
  
  
  
    我的web应用上想知道到底有多少用户在使用？
  
  
  
  
    在网站中经常需要进行在线人数的统计。过去的一般做法是结合登录和退出功能，即当用户输入用户名密码进行登录的时候计数器加1，然后当用户点击退出按钮退出系统的时候计数器减1。这种处理方式存在一些缺点，例如: 用户正常登录后，可能会忘记点击退出按钮，而直接关闭浏览器，导致计数器减1的操作没有及时执行；网站上还经常有一些内容是不需要登录就可以访问的，在这种情况下也无法使用上面的方法进行在线人数统计。
 我们可以利用Servlet规范中定义的事件监听器 (Listener) 来解决这个问题，实现更准确的在线人数统计功能。对每一个正在访问的用户，J2EE应用服务器会为其建立一个对应的HttpSession对象。当一个浏览器第一次访问网站的时候，J2EE应用服务器会新建一个HttpSession对象 ，并触发 HttpSession创建事件 ，如果注册了HttpSessionListener事件监听器，则会调用HttpSessionListener事件监听器的sessionCreated方法。相反，当这个浏览器访问结束超时的时候，J2EE应用服务器会销毁相应的HttpSession对象，触发 HttpSession销毁事件，同时调用所注册HttpSessionListener事件监听器的sessionDestroyed方法。
  
  
 
    
    
      
        import javax.servlet.http.HttpSessionListener;
      
      
        import javax.servlet.http.HttpSessionEvent;
      
      
      
      
        public class SessionCounter implements HttpSessionListener {
      
      
        private static int activeSessions =0;
      
      
        /* Session创建事件 */
      
      
        public void sessionCreated(HttpSessionEvent se) {
      
      
              ServletContext ctx = event.getSession( ).getServletContext( );
      
      
                Integer numSessions = (Integer) ctx.getAttribute("numSessions");
      
      
                if (numSessions == null) {
      
      
                    numSessions = new Integer(1);
      
      
                }
      
      
                else {
      
      
                    int count = numSessions.intValue( );
      
      
                    numSessions = new Integer(count + 1);
      
      
                }
      
      
                ctx.setAttribute("numSessions", numSessions);
      
      
        }
      
      
        /* Session失效事件 */
      
      
        public void sessionDestroyed(HttpSessionEvent se) {
      
      
         ServletContext ctx=se.getSession().getServletContext();
      
      
         Integer numSessions = (Integer)ctx.getAttribute("numSessions");
      
      
                if(numSessions == null)
      
      
                    numSessions = new Integer(0);
      
      
                }
      
      
                else {
      
      
                    int count = numSessions.intValue( );
      
      
                    numSessions = new Integer(count - 1);
      
      
                }
      
      
                ctx.setAttribute("numSessions", numSessions);
      
      
      
      
      
      
      
      
        }
      
      
        }
      
    
  
  
    在这个解决方案中，任何一个Session被创建或者销毁时，都会通知SessionCounter 这个类，当然通知的原因是必须在web.xml文件中做相关的配置工作。如下面的配置代码: 
  
  
    
  
    
    
      
        
      
      
            demo.listener.SessionCounter</listener-class>
      
      
        </listener>
      
    
  
  
    以下两种情况下就会发生sessionDestoryed (会话销毁) 事件: 
 1.执行session.invalidate()方法时 。
 既然LogoutServlet.java中执行session.invalidate()时，会触发sessionDestory()从在线用户 列表中清除当前用户，我们就不必在LogoutServlet.java中对在线列表进行操作了，所以LogoutServlet.java的内容现在是 这样。
  
  
    
  
    
    
      
        public void doGet(HttpServletRequest request,HttpServletResponse response)
      
      
            throws ServletException, IOException {
      
      
            // 销毁session
      
      
            request.getSession().invalidate();
      
      
            // 成功
      
      
            response.sendRedirect("index.jsp");
      
      
        }
      
    
  
  
  
  
    2.
 如果用户长时间没有访问服务器，超过了会话最大超时时间 ，服务器就会自动销毁超时的session。
 会话超时时间可以在web.xml中进行设置，为了容易看到超时效果，我们将超时时间设置为最小值。
  
  
 
    
    
      
        <session-config>
      
      
            <session-timeout>1</session-timeout>
      
      
        </session-config>
      
    
  
  
  
  
    时间单位是一分钟，并且只能是整数，如果是零或负数，那么会话就永远不会超时。
  
  
  
  
    2.HttpSessionEvent
  
  
    这是类代表一个web应用程序内更改会话事件通知。
  
  
 
    
      
        public class ShopSessionListener implements HttpSessionListener {
      
      
      
      
            public void sessionCreated(HttpSessionEvent se) {
      
      
      
      
            }
      
      
            public void sessionDestroyed(HttpSessionEvent se) {
      
      
                String sessionid = se.getSession().getId();
      
      
                EopSite site  =(EopSite)ThreadContextHolder.getSessionContext().getAttribute("site_key");
      
      
      
      
                if(site!=null){
      
      
                ICartManager cartManager = SpringContextHolder.getBean("cartManager");
      
      
                cartManager.clean(sessionid,site.getUserid(),site.getId());
      
      
                }
      
      
            }
      
      
        }
      
    
  
  
  
  
    se.getSession().getId();
  
  
    HttpSession 接口中的getId():
  
  
    Returns a string containing the unique identifier assigned to this session.
  
  
    返回一个字符串，其中包含唯一标识符分配给本次会话。
  
  
  
