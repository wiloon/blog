---
title: HttpSessionListener
author: wiloon
type: post
date: 2012-06-22T03:46:07+00:00
url: /?p=3591
categories:
  - Java
  - Web

---
<div>
     Session创建事件发生在每次一个新的session创建的时候，类似地Session失效事件发生在每次一个Session失效的时候。
</div>

<div id="blog_content">
  这个接口也只包含两个方法，分别对应于Session的创建和失效：<br /> # public void sessionCreated(HttpSessionEvent se);<br /> # public void sessionDestroyed(HttpSessionEvent se);</p> 
  
  <p>
    &nbsp;
  </p>
  
  <p>
    我的web应用上想知道到底有多少用户在使用？
  </p>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    在网站中经常需要进行在线人数的统计。过去的一般做法是结合登录和退出功能，即当用户输入用户名密码进行登录的时候计数器加1，然后当用户点击退出按钮退出系统的时候计数器减1。这种处理方式存在一些缺点，例如：用户正常登录后，可能会忘记点击退出按钮，而直接关闭浏览器，导致计数器减1的操作没有及时执行；网站上还经常有一些内容是不需要登录就可以访问的，在这种情况下也无法使用上面的方法进行在线人数统计。<br /> 我们可以利用Servlet规范中定义的事件监听器（Listener）来解决这个问题，实现更准确的在线人数统计功能。对每一个正在访问的用户，J2EE应用服务器会为其建立一个对应的HttpSession对象。当一个浏览器第一次访问网站的时候，J2EE应用服务器会新建一个HttpSession对象 ，并触发 HttpSession创建事件 ，如果注册了HttpSessionListener事件监听器，则会调用HttpSessionListener事件监听器的sessionCreated方法。相反，当这个浏览器访问结束超时的时候，J2EE应用服务器会销毁相应的HttpSession对象，触发 HttpSession销毁事件，同时调用所注册HttpSessionListener事件监听器的sessionDestroyed方法。
  </p>
  
  <div id="">
    <div>
      <div>
        Java代码  <a title="收藏这段代码"><img src="http://uule.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
      </div>
    </div>
    
    <ol start="1">
      <li>
        import javax.servlet.http.HttpSessionListener;
      </li>
      <li>
        import javax.servlet.http.HttpSessionEvent;
      </li>
      <li>
      </li>
      <li>
        public class SessionCounter implements HttpSessionListener {
      </li>
      <li>
        private static int activeSessions =0;
      </li>
      <li>
        /* Session创建事件 */
      </li>
      <li>
        public void sessionCreated(HttpSessionEvent se) {
      </li>
      <li>
              ServletContext ctx = event.getSession( ).getServletContext( );
      </li>
      <li>
                Integer numSessions = (Integer) ctx.getAttribute(&#8220;numSessions&#8221;);
      </li>
      <li>
                if (numSessions == null) {
      </li>
      <li>
                    numSessions = new Integer(1);
      </li>
      <li>
                }
      </li>
      <li>
                else {
      </li>
      <li>
                    int count = numSessions.intValue( );
      </li>
      <li>
                    numSessions = new Integer(count + 1);
      </li>
      <li>
                }
      </li>
      <li>
                ctx.setAttribute(&#8220;numSessions&#8221;, numSessions);
      </li>
      <li>
        }
      </li>
      <li>
        /* Session失效事件 */
      </li>
      <li>
        public void sessionDestroyed(HttpSessionEvent se) {
      </li>
      <li>
         ServletContext ctx=se.getSession().getServletContext();
      </li>
      <li>
         Integer numSessions = (Integer)ctx.getAttribute(&#8220;numSessions&#8221;);
      </li>
      <li>
        <span class=&#8221;oblog_text&#8221;>        if(numSessions == null)
      </li>
      <li>
                    numSessions = new Integer(0);
      </li>
      <li>
                }
      </li>
      <li>
                else {
      </li>
      <li>
                    int count = numSessions.intValue( );
      </li>
      <li>
                    numSessions = new Integer(count &#8211; 1);
      </li>
      <li>
                }
      </li>
      <li>
                ctx.setAttribute(&#8220;numSessions&#8221;, numSessions);</span>
      </li>
      <li>
      </li>
      <li>
      </li>
      <li>
      </li>
      <li>
        }
      </li>
      <li>
        }
      </li>
    </ol>
  </div>
  
  <p>
    在这个解决方案中，任何一个Session被创建或者销毁时，都会通知SessionCounter 这个类，当然通知的原因是必须在web.xml文件中做相关的配置工作。如下面的配置代码：
  </p>
  
  <div id="">
    <div>
      <div>
        Java代码  <a title="收藏这段代码"><img src="http://uule.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
      </div>
    </div>
    
    <ol start="1">
      <li>
        <listener>
      </li>
      <li>
            <listener-class>demo.listener.SessionCounter</listener-class>
      </li>
      <li>
        </listener>
      </li>
    </ol>
  </div>
  
  <p>
    以下两种情况下就会发生sessionDestoryed（会话销毁）事件：<br /> 1.执行session.invalidate()方法时 。<br /> 既然LogoutServlet.java中执行session.invalidate()时，会触发sessionDestory()从在线用户 列表中清除当前用户，我们就不必在LogoutServlet.java中对在线列表进行操作了，所以LogoutServlet.java的内容现在是 这样。
  </p>
  
  <div id="">
    <div>
      <div>
        Java代码  <a title="收藏这段代码"><img src="http://uule.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
      </div>
    </div>
    
    <ol start="1">
      <li>
        public void doGet(HttpServletRequest request,HttpServletResponse response)
      </li>
      <li>
            throws ServletException, IOException {
      </li>
      <li>
            // 销毁session
      </li>
      <li>
            request.getSession().invalidate();
      </li>
      <li>
            // 成功
      </li>
      <li>
            response.sendRedirect(&#8220;index.jsp&#8221;);
      </li>
      <li>
        }
      </li>
    </ol>
  </div>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    2.<br /> 如果用户长时间没有访问服务器，超过了会话最大超时时间 ，服务器就会自动销毁超时的session。<br /> 会话超时时间可以在web.xml中进行设置，为了容易看到超时效果，我们将超时时间设置为最小值。
  </p>
  
  <div id="">
    <div>
      <div>
        Java代码  <a title="收藏这段代码"><img src="http://uule.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
      </div>
    </div>
    
    <ol start="1">
      <li>
        <session-config>
      </li>
      <li>
            <session-timeout>1</session-timeout>
      </li>
      <li>
        </session-config>
      </li>
    </ol>
  </div>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    时间单位是一分钟，并且只能是整数，如果是零或负数，那么会话就永远不会超时。
  </p>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    2.HttpSessionEvent
  </p>
  
  <p>
    这是类代表一个web应用程序内更改会话事件通知。
  </p>
  
  <p>
    &nbsp;
  </p>
  
  <div id="">
    <div>
      <div>
        Java代码  <a title="收藏这段代码"><img src="http://uule.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
      </div>
    </div>
    
    <ol start="1">
      <li>
        public class ShopSessionListener implements HttpSessionListener {
      </li>
      <li>
      </li>
      <li>
            public void sessionCreated(HttpSessionEvent se) {
      </li>
      <li>
      </li>
      <li>
            }
      </li>
      <li>
            public void sessionDestroyed(HttpSessionEvent se) {
      </li>
      <li>
                String sessionid = se.getSession().getId();
      </li>
      <li>
                EopSite site  =(EopSite)ThreadContextHolder.getSessionContext().getAttribute(&#8220;site_key&#8221;);
      </li>
      <li>
      </li>
      <li>
                if(site!=null){
      </li>
      <li>
                ICartManager cartManager = SpringContextHolder.getBean(&#8220;cartManager&#8221;);
      </li>
      <li>
                cartManager.clean(sessionid,site.getUserid(),site.getId());
      </li>
      <li>
                }
      </li>
      <li>
            }
      </li>
      <li>
        }
      </li>
    </ol>
  </div>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    se.getSession().getId();
  </p>
  
  <p>
    HttpSession 接口中的getId():
  </p>
  
  <p>
    Returns a string containing the unique identifier assigned to this session.
  </p>
  
  <p>
    返回一个字符串，其中包含唯一标识符分配给本次会话。
  </p>
  
  <p>
    &nbsp;
  </p>
</div>