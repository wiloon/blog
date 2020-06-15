---
title: 动态代理 Dynamic Proxy
author: wiloon
type: post
date: 2012-10-16T08:20:11+00:00
url: /?p=4504
categories:
  - Java
tags:
  - DesignPattern

---
从JDK1.3开始，Java就引入了动态代理的概念。动态代理（Dynamic Proxy）可以帮助你减少代码行数，真正提高代码的可复用度。例如，你不必为所有的类的方法里面都写上相同的Log代码行，取而代之的是实用类的动态代理类。当然，这种便利是有条件的。本文简单介绍Java动态代理的原理，并实现一个被代理的Servlet创建，和调用的过程。

<div id="article_content">
  <div>
  </div>
  
  <div>
    1．代理模式（Proxy Pattern）
  </div>
  
  <div>
    在JDK1.3以前，代理模式就已流行，所以得代理模式是生成一个和类相同接口的代理类，用户通过使用代理类来封装某个实现类。如图1，其目的是加强实现类的某个方法的功能，而不必改变原有的源代码。
  </div>
  
  <div>
    <img src="http://p.blog.csdn.net/images/p_blog_csdn_net/tyrone1979/proxy1.JPG" alt="" />
  </div>
  
  <div>
    2．动态代理（Dynamic Proxy）
  </div>
  
  <div>
    随着Proxy的流行，Sun把它纳入到JDK1.3实现了Java的动态代理。动态代理和普通的代理模式的区别，就是动态代理中的代理类是由java.lang.reflect.Proxy类在运行期时根据接口定义，采用Java反射功能动态生成的。和java.lang.reflect.InvocationHandler结合，可以加强现有类的方法实现。如图2，图中的自定义Handler实现InvocationHandler接口，自定义Handler实例化时，将实现类传入自定义Handler对象。自定义Handler需要实现invoke方法，该方法可以使用Java反射调用实现类的实现的方法，同时当然可以实现其他功能，例如在调用实现类方法前后加入Log。而Proxy类根据Handler和需要代理的接口动态生成一个接口实现类的对象。当用户调用这个动态生成的实现类时，实际上是调用了自定义Handler的invoke方法。
  </div>
  
  <div>
  </div>
  
  <div>
    <img src="http://p.blog.csdn.net/images/p_blog_csdn_net/tyrone1979/proxy2.JPG" alt="" width="683" height="284" />
  </div>
  
  <div>
    3．动态代理Servlet
  </div>
  
  <div>
                  虽然Web Application Server的产品很多，但Servlet的处理原理是相似的：动态加载Servlet，调用Servlet的init方法（只被调用一次），并保存到Servlet容器；Servlet使用时，调用Servlet的service方法。本文动态代理Servlet接口，使其init和service被调用时会在控制台打出方法调用前后信息。
  </div>
  
  <div>
    首先实现2个Servlet，DefaultServlet和UserServlet
  </div>
  
  <div>
    [java]<br /> package org.colimas.servlet;</p> 
    
    <p>
      import javax.servlet.Servlet;
    </p>
    
    <p>
      import javax.servlet.ServletException;
    </p>
    
    <p>
      import javax.servlet.http.HttpServlet;
    </p>
    
    <p>
      public class DefaultServlet extends HttpServlet implements Servlet {
    </p>
    
    <p>
      public void init() throws ServletException {
    </p>
    
    <p>
      super.init();
    </p>
    
    <p>
      System.out.println(DefaultServlet.class.getName()+":Running init");
    </p>
    
    <p>
      }
    </p>
    
    <p>
      public String getServletInfo() {
    </p>
    
    <p>
      return DefaultServlet.class.getName();
    </p>
    
    <p>
      }
    </p>
    
    <p>
      }
    </p>
    
    <p>
      package org.colimas.servlet;
    </p>
    
    <p>
      import java.io.IOException;
    </p>
    
    <p>
      import javax.servlet.Servlet;
    </p>
    
    <p>
      import javax.servlet.ServletException;
    </p>
    
    <p>
      import javax.servlet.http.HttpServlet;
    </p>
    
    <p>
      import javax.servlet.http.HttpServletRequest;
    </p>
    
    <p>
      import javax.servlet.http.HttpServletResponse;
    </p>
    
    <p>
      public class UserServlet extends HttpServlet implements Servlet {
    </p>
    
    <p>
      private static final long serialVersionUID = -7016554795165038652L;
    </p>
    
    <p>
      public void init() throws ServletException {
    </p>
    
    <p>
      super.init();
    </p>
    
    <p>
      System.out.println(UserServlet.class.getName()+":Running init");
    </p>
    
    <p>
      }
    </p>
    
    <p>
      protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    </p>
    
    <p>
      System.out.println(UserServlet.class.getName()+":Do UserSErvlet Get");
    </p>
    
    <p>
      }
    </p>
    
    <p>
      public String getServletInfo() {
    </p>
    
    <p>
      return UserServlet.class.getName();
    </p>
    
    <p>
      }<br /> }<br /> 然后实现InvocationHandler
    </p>
    
    <p>
      package org.colimas.webapp;
    </p>
    
    <p>
      import java.lang.reflect.InvocationHandler;
    </p>
    
    <p>
      import java.lang.reflect.Method;
    </p>
    
    <p>
      import javax.servlet.Servlet;<br /> public class ServletHandler implements InvocationHandler {
    </p>
    
    <p>
      private Servlet obj;
    </p>
    
    <p>
      public ServletHandler(Servlet obj){
    </p>
    
    <p>
      this.obj=obj;
    </p>
    
    <p>
      }
    </p>
    
    <p>
      public Object invoke(Object arg0, Method arg1, Object[] arg2)
    </p>
    
    <p>
      throws Throwable {
    </p>
    
    <p>
      
    </p>
    
    <p>
      if(arg1.getName().compareTo("init")==0) //调用init时
    </p>
    
    <p>
      {
    </p>
    
    <p>
      System.out.println(obj.getServletInfo()+":Init servlet starting&#8230;"); //增加控制台输出。
    </p>
    
    <p>
      arg1.invoke(obj,arg2); //调用init方法
    </p>
    
    <p>
      System.out.println(obj.getServletInfo()+":Init servlet ending&#8230;"); //增加控制台输出。
    </p>
    
    <p>
      }else if(arg1.getName().compareTo("service")==0){ //调用service时
    </p>
    
    <p>
      System.out.println(obj.getServletInfo()+":service starting&#8230;"); //增加控制台输出。
    </p>
    
    <p>
      
    </p>
    
    <p>
      arg1.invoke(obj,arg2); //调用service方法。
    </p>
    
    <p>
      System.out.println(obj.getServletInfo()+":service ending&#8230;"); //增加控制台输出。
    </p>
    
    <p>
      
    </p>
    
    <p>
      }
    </p>
    
    <p>
      return null;
    </p>
    
    <p>
      }
    </p>
    
    <p>
      
    </p>
    
    <p>
      }
    </p>
    
    <p>
      
    </p>
    
    <p>
      实现Servlet的调用
    </p>
    
    <p>
      package org.colimas.webapp;
    </p>
    
    <p>
      
    </p>
    
    <p>
      import java.lang.reflect.InvocationHandler;
    </p>
    
    <p>
      import java.lang.reflect.Proxy;
    </p>
    
    <p>
      
    </p>
    
    <p>
      import javax.servlet.Servlet;
    </p>
    
    <p>
      import javax.servlet.ServletConfig;
    </p>
    
    <p>
      import javax.servlet.ServletContext;
    </p>
    
    <p>
      import javax.servlet.ServletException;
    </p>
    
    <p>
      
    </p>
    
    <p>
      public class ServletWrapperImp {
    </p>
    
    <p>
      
    </p>
    
    <p>
      private Class servletClass;
    </p>
    
    <p>
      private ServletConfig config;
    </p>
    
    <p>
      private String _servletname;
    </p>
    
    <p>
      private Servlet _theServlet;
    </p>
    
    <p>
      private ServletContext context;
    </p>
    
    <p>
      public ServletWrapperImp(ServletConfig config){
    </p>
    
    <p>
      this.config=config;
    </p>
    
    <p>
      this._servletname=this.config.getServletName();
    </p>
    
    <p>
      this.context=this.config.getServletContext();
    </p>
    
    <p>
      }
    </p>
    
    <p>
      
    </p>
    
    <p>
      public Servlet getServlet() throws ServletException{
    </p>
    
    <p>
      
    </p>
    
    <p>
      destroy();
    </p>
    
    <p>
      try {
    </p>
    
    <p>
      WebAppClassLoader loader=new WebAppClassLoader(this.getClass().getClassLoader()); //自定义class loader
    </p>
    
    <p>
      String name=getServletName(); //从ServletConfig中获得Servlet Name
    </p>
    
    <p>
      synchronized (context) {
    </p>
    
    <p>
      Servlet theServlet=context.getServlet(name); //在ServletContext中查找Servlet
    </p>
    
    <p>
      if(theServlet==null){ //如果ServletContext没有。
    </p>
    
    <p>
      servletClass = loader.loadClass(name); //由Class loader 加载Servlet class。
    </p>
    
    <p>
      theServlet = (Servlet) servletClass.newInstance(); //Servlet实例化。
    </p>
    
    <p>
      WebAppContext.addServlet(name,theServlet); //将Servlet实例存入ServletContext。
    </p>
    
    <p>
      InvocationHandler handler=new ServletHandler(theServlet); //自定义ServletHandler，参见ServletHandler类。
    </p>
    
    <p>
      _theServlet=(Servlet)Proxy.newProxyInstance(theServlet.getClass().getClassLoader(),
    </p>
    
    <p>
      new Class[]{Servlet.class},handler); //代理类实例化。
    </p>
    
    <p>
      _theServlet.init(config); //Servlet代理对象调用init方法。参见ServletHandler的invoke方法。
    </p>
    
    <p>
      
    </p>
    
    <p>
      }else{ //ServletContext里已存在。
    </p>
    
    <p>
      InvocationHandler handler=new ServletHandler(theServlet); //自定义ServletHandler，参见ServletHandler类。
    </p>
    
    <p>
      _theServlet=(Servlet)Proxy.newProxyInstance(theServlet.getClass().getClassLoader(),
    </p>
    
    <p>
      new Class[]{Servlet.class},handler); //代理Servlet接口，动态生成代理类，并实例化。
    </p>
    
    <p>
      }
    </p>
    
    <p>
      }
    </p>
    
    <p>
      return _theServlet; //返回Servlet代理对象
    </p>
    
    <p>
      } catch( ClassNotFoundException ex1 ) {
    </p>
    
    <p>
      
    </p>
    
    <p>
      } catch( InstantiationException ex ) {
    </p>
    
    <p>
      
    </p>
    
    <p>
      }catch(IllegalAccessException ex2){
    </p>
    
    <p>
      
    </p>
    
    <p>
      }
    </p>
    
    <p>
      return null;
    </p>
    
    <p>
      }
    </p>
    
    <p>
      public void destroy() {
    </p>
    
    <p>
      if (_theServlet != null) {
    </p>
    
    <p>
      _theServlet.destroy();
    </p>
    
    <p>
      }
    </p>
    
    <p>
      }
    </p>
    
    <p>
      
    </p>
    
    <p>
      protected String getServletName(){
    </p>
    
    <p>
      return _servletname;
    </p>
    
    <p>
      }
    </p>
    
    <p>
      }<br /> <pre><br /> [/java]
    </p>
  </div>
  
  <div>
    其中的ServletConfig保存Servlet相关信息。ServletContext保存所有的Servlet对象。WebAppClassLoader为自定义class loader,参见<a href="http://blog.csdn.net/tyrone1979/archive/2006/09/03/1164262.aspx">http://blog.csdn.net/tyrone1979/archive/2006/09/03/1164262.aspx</a>。
  </div>
  
  <div>
  </div>
  
  <div>
    最后编写测试类Main，该类模拟10个用户访问Servlet，5人访问DefaultServlet，5人访问UserServlet。
  </div>
  
  <div>
    [java]</pre><br /> package org.colimas.main;</p> 
    
    <p>
      
    </p>
    
    <p>
      import java.io.IOException;
    </p>
    
    <p>
      
    </p>
    
    <p>
      import javax.servlet.Servlet;
    </p>
    
    <p>
      import javax.servlet.ServletConfig;
    </p>
    
    <p>
      import javax.servlet.ServletException;
    </p>
    
    <p>
      
    </p>
    
    <p>
      import org.colimas.webapp.HttpServletRequestWrapper;
    </p>
    
    <p>
      import org.colimas.webapp.HttpServletResponseWrapper;
    </p>
    
    <p>
      import org.colimas.webapp.ServletConfigImpl;
    </p>
    
    <p>
      import org.colimas.webapp.ServletWrapper;
    </p>
    
    <p>
      import org.colimas.webapp.ServletWrapperImp;
    </p>
    
    <p>
      import org.colimas.webapp.WebAppContext;
    </p>
    
    <p>
      
    </p>
    
    <p>
      public class Main {
    </p>
    
    <p>
      
    </p>
    
    <p>
      private ThreadGroup _threadGroup;
    </p>
    
    <p>
      private Thread[] _threads;
    </p>
    
    <p>
      String defaultServletName="org.colimas.servlet.DefaultServlet";
    </p>
    
    <p>
      String userServletName="org.colimas.servlet.UserServlet";
    </p>
    
    <p>
      WebAppContext context=WebAppContext.newInstance();
    </p>
    
    <p>
      
    </p>
    
    <p>
      public void doStart(){
    </p>
    
    <p>
      
    </p>
    
    <p>
      _threadGroup=new ThreadGroup("SERVLETS");
    </p>
    
    <p>
      int i=0;
    </p>
    
    <p>
      _threads=new ServletThread[10]; //模拟10位用户。
    </p>
    
    <p>
      for(i=0;i<5;i++){
    </p>
    
    <p>
      _threads[i]=new ServletThread(_threadGroup,new Integer(i).toString(),
    </p>
    
    <p>
      defaultServletName);
    </p>
    
    <p>
      _threads[i].start();
    </p>
    
    <p>
      }
    </p>
    
    <p>
      for(i=5;i<10;i++){
    </p>
    
    <p>
      _threads[i]=new ServletThread(_threadGroup,new Integer(i).toString(),
    </p>
    
    <p>
      userServletName);
    </p>
    
    <p>
      _threads[i].start();
    </p>
    
    <p>
      }
    </p>
    
    <p>
      
    </p>
    
    <p>
      }
    </p>
    
    <p>
      /**
    </p>
    
    <p>
      * @param args
    </p>
    
    <p>
      */
    </p>
    
    <p>
      public static void main(String[] args) {
    </p>
    
    <p>
      Main _main=new Main();
    </p>
    
    <p>
      _main.doStart();
    </p>
    
    <p>
      
    </p>
    
    <p>
      }
    </p>
    
    <p>
      //模拟用户线程
    </p>
    
    <p>
      private class ServletThread extends Thread{
    </p>
    
    <p>
      
    </p>
    
    <p>
      private String servletName;
    </p>
    
    <p>
      
    </p>
    
    <p>
      public ServletThread(ThreadGroup group,String threadname,String servletname){
    </p>
    
    <p>
      super(group,threadname);
    </p>
    
    <p>
      servletName=servletname;
    </p>
    
    <p>
      }
    </p>
    
    <p>
      //调用Servlet的service.
    </p>
    
    <p>
      public void run() { //用户调用Servlet
    </p>
    
    <p>
      ServletConfig config=new ServletConfigImpl(servletName,context); //调用的Servlet信息。
    </p>
    
    <p>
      ServletWrapperImp wrapper=new ServletWrapperImp(config);
    </p>
    
    <p>
      try {
    </p>
    
    <p>
      Servlet defaultServlet=wrapper.getServlet(); //获得Servlet对象，实际是Servlet的代理对象
    </p>
    
    <p>
      defaultServlet.service(new HttpServletRequestWrapper(),
    </p>
    
    <p>
      new HttpServletResponseWrapper()); 调用代理对象的service方法，参见ServletHandler的invoke方法。
    </p>
    
    <p>
      } catch (ServletException e) {
    </p>
    
    <p>
      e.printStackTrace();
    </p>
    
    <p>
      } catch(IOException e){
    </p>
    
    <p>
      
    </p>
    
    <p>
      }
    </p>
    
    <p>
      }
    </p>
    
    <p>
      
    </p>
    
    <p>
      }
    </p>
    
    <p>
      }<br /> <pre><br /> [/java]
    </p>
  </div>
  
  <div>
    HttpServletRequestWrapper和HttpServletResponseWrapper实现HttpServletRequest，和HttpServletResponse。
  </div>
  
  <div>
    测试结果如下
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:Init servlet starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:Running init
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:Init servlet ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:Init servlet starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:Running init
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:Init servlet ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:service starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:service ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:service starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:service ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:service starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:Do UserSErvlet Get
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:service ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:service starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:Do UserSErvlet Get
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:service ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:service starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:Do UserSErvlet Get
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:service ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:service starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:service starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:service starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:service starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:service starting&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:Do UserSErvlet Get
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:service ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:Do UserSErvlet Get
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:service ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.DefaultServlet:service ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:service ending&#8230;
  </div>
  
  <div align="left">
    org.colimas.servlet.UserServlet:service ending&#8230;
  </div>
  
  <div>
  </div>
  
  <div>
    2个Servlet第一次Load时初始化，被调用init，之后保存到ServletContext中。第二次直接从ServletContext获得，执行service。红字表示代理类里增加的输出结果。
  </div>
  
  <div>
  </div>
  
  <div>
    4．动态代理的限制
  </div>
  
  <div>
                  JDK的动态代理并不能随心所欲的代理所有的类。Proxy.newProxyInstance方法的第二个参数只能是接口数组， 也就是Proxy只能代理接口。
  </div>
</div>