---
title: 动态代理 Dynamic Proxy
author: "-"
date: 2012-10-16T08:20:11+00:00
url: /?p=4504
categories:
  - pattern
tags:
  - DesignPattern

---
## 动态代理 Dynamic Proxy

从JDK1.3开始，Java就引入了动态代理的概念。动态代理 (Dynamic Proxy) 可以帮助你减少代码行数，真正提高代码的可复用度。例如，你不必为所有的类的方法里面都写上相同的Log代码行，取而代之的是实用类的动态代理类。当然，这种便利是有条件的。本文简单介绍Java动态代理的原理，并实现一个被代理的Servlet创建，和调用的过程。

### 代理模式 (Proxy Pattern)

在JDK1.3以前，代理模式就已流行，所以得代理模式是生成一个和类相同接口的代理类，用户通过使用代理类来封装某个实现类。如图1，其目的是加强实现类的某个方法的功能，而不必改变原有的源代码。
  
    <img src="http://p.blog.csdn.net/images/p_blog_csdn_net/tyrone1979/proxy1.JPG" alt="" />
  
  
    2．动态代理 (Dynamic Proxy) 
  
  
    随着Proxy的流行，Sun把它纳入到JDK1.3实现了Java的动态代理。动态代理和普通的代理模式的区别，就是动态代理中的代理类是由java.lang.reflect.Proxy类在运行期时根据接口定义，采用Java反射功能动态生成的。和java.lang.reflect.InvocationHandler结合，可以加强现有类的方法实现。如图2，图中的自定义Handler实现InvocationHandler接口，自定义Handler实例化时，将实现类传入自定义Handler对象。自定义Handler需要实现invoke方法，该方法可以使用Java反射调用实现类的实现的方法，同时当然可以实现其他功能，例如在调用实现类方法前后加入Log。而Proxy类根据Handler和需要代理的接口动态生成一个接口实现类的对象。当用户调用这个动态生成的实现类时，实际上是调用了自定义Handler的invoke方法。
  
  
  
    <img src="http://p.blog.csdn.net/images/p_blog_csdn_net/tyrone1979/proxy2.JPG" alt="" width="683" height="284" />
  
  
    3．动态代理Servlet
  
  
                  虽然Web Application Server的产品很多，但Servlet的处理原理是相似的: 动态加载Servlet，调用Servlet的init方法 (只被调用一次) ，并保存到Servlet容器；Servlet使用时，调用Servlet的service方法。本文动态代理Servlet接口，使其init和service被调用时会在控制台打出方法调用前后信息。
  
  
    首先实现2个Servlet，DefaultServlet和UserServlet
  
  
    ```java
 package org.colimas.servlet;

      import javax.servlet.Servlet;
    
    
    
      import javax.servlet.ServletException;
    
    
    
      import javax.servlet.http.HttpServlet;
    
    
    
      public class DefaultServlet extends HttpServlet implements Servlet {
    
    
    
      public void init() throws ServletException {
    
    
    
      super.init();
    
    
    
      System.out.println(DefaultServlet.class.getName()+":Running init");
    
    
    
      }
    
    
    
      public String getServletInfo() {
    
    
    
      return DefaultServlet.class.getName();
    
    
    
      }
    
    
    
      }
    
    
    
      package org.colimas.servlet;
    
    
    
      import java.io.IOException;
    
    
    
      import javax.servlet.Servlet;
    
    
    
      import javax.servlet.ServletException;
    
    
    
      import javax.servlet.http.HttpServlet;
    
    
    
      import javax.servlet.http.HttpServletRequest;
    
    
    
      import javax.servlet.http.HttpServletResponse;
    
    
    
      public class UserServlet extends HttpServlet implements Servlet {
    
    
    
      private static final long serialVersionUID = -7016554795165038652L;
    
    
    
      public void init() throws ServletException {
    
    
    
      super.init();
    
    
    
      System.out.println(UserServlet.class.getName()+":Running init");
    
    
    
      }
    
    
    
      protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    
    
    
      System.out.println(UserServlet.class.getName()+":Do UserSErvlet Get");
    
    
    
      }
    
    
    
      public String getServletInfo() {
    
    
    
      return UserServlet.class.getName();
    
    
    
      }
 }
 然后实现InvocationHandler

      package org.colimas.webapp;
    
    
    
      import java.lang.reflect.InvocationHandler;
    
    
    
      import java.lang.reflect.Method;
    
    
    
      import javax.servlet.Servlet;
 public class ServletHandler implements InvocationHandler {

      private Servlet obj;
    
    
    
      public ServletHandler(Servlet obj){
    
    
    
      this.obj=obj;
    
    
    
      }
    
    
    
      public Object invoke(Object arg0, Method arg1, Object[] arg2)
    
    
    
      throws Throwable {
    
    
    
      
    
    
    
      if(arg1.getName().compareTo("init")==0) //调用init时
    
    
    
      {
    
    
    
      System.out.println(obj.getServletInfo()+":Init servlet starting..."); //增加控制台输出。
    
    
    
      arg1.invoke(obj,arg2); //调用init方法
    
    
    
      System.out.println(obj.getServletInfo()+":Init servlet ending..."); //增加控制台输出。
    
    
    
      }else if(arg1.getName().compareTo("service")==0){ //调用service时
    
    
    
      System.out.println(obj.getServletInfo()+":service starting..."); //增加控制台输出。
    
    
    
      
    
    
    
      arg1.invoke(obj,arg2); //调用service方法。
    
    
    
      System.out.println(obj.getServletInfo()+":service ending..."); //增加控制台输出。
    
    
    
      
    
    
    
      }
    
    
    
      return null;
    
    
    
      }
    
    
    
      
    
    
    
      }
    
    
    
      
    
    
    
      实现Servlet的调用
    
    
    
      package org.colimas.webapp;
    
    
    
      
    
    
    
      import java.lang.reflect.InvocationHandler;
    
    
    
      import java.lang.reflect.Proxy;
    
    
    
      
    
    
    
      import javax.servlet.Servlet;
    
    
    
      import javax.servlet.ServletConfig;
    
    
    
      import javax.servlet.ServletContext;
    
    
    
      import javax.servlet.ServletException;
    
    
    
      
    
    
    
      public class ServletWrapperImp {
    
    
    
      
    
    
    
      private Class servletClass;
    
    
    
      private ServletConfig config;
    
    
    
      private String _servletname;
    
    
    
      private Servlet _theServlet;
    
    
    
      private ServletContext context;
    
    
    
      public ServletWrapperImp(ServletConfig config){
    
    
    
      this.config=config;
    
    
    
      this._servletname=this.config.getServletName();
    
    
    
      this.context=this.config.getServletContext();
    
    
    
      }
    
    
    
      
    
    
    
      public Servlet getServlet() throws ServletException{
    
    
    
      
    
    
    
      destroy();
    
    
    
      try {
    
    
    
      WebAppClassLoader loader=new WebAppClassLoader(this.getClass().getClassLoader()); //自定义class loader
    
    
    
      String name=getServletName(); //从ServletConfig中获得Servlet Name
    
    
    
      synchronized (context) {
    
    
    
      Servlet theServlet=context.getServlet(name); //在ServletContext中查找Servlet
    
    
    
      if(theServlet==null){ //如果ServletContext没有。
    
    
    
      servletClass = loader.loadClass(name); //由Class loader 加载Servlet class。
    
    
    
      theServlet = (Servlet) servletClass.newInstance(); //Servlet实例化。
    
    
    
      WebAppContext.addServlet(name,theServlet); //将Servlet实例存入ServletContext。
    
    
    
      InvocationHandler handler=new ServletHandler(theServlet); //自定义ServletHandler，参见ServletHandler类。
    
    
    
      _theServlet=(Servlet)Proxy.newProxyInstance(theServlet.getClass().getClassLoader(),
    
    
    
      new Class[]{Servlet.class},handler); //代理类实例化。
    
    
    
      _theServlet.init(config); //Servlet代理对象调用init方法。参见ServletHandler的invoke方法。
    
    
    
      
    
    
    
      }else{ //ServletContext里已存在。
    
    
    
      InvocationHandler handler=new ServletHandler(theServlet); //自定义ServletHandler，参见ServletHandler类。
    
    
    
      _theServlet=(Servlet)Proxy.newProxyInstance(theServlet.getClass().getClassLoader(),
    
    
    
      new Class[]{Servlet.class},handler); //代理Servlet接口，动态生成代理类，并实例化。
    
    
    
      }
    
    
    
      }
    
    
    
      return _theServlet; //返回Servlet代理对象
    
    
    
      } catch( ClassNotFoundException ex1 ) {
    
    
    
      
    
    
    
      } catch( InstantiationException ex ) {
    
    
    
      
    
    
    
      }catch(IllegalAccessException ex2){
    
    
    
      
    
    
    
      }
    
    
    
      return null;
    
    
    
      }
    
    
    
      public void destroy() {
    
    
    
      if (_theServlet != null) {
    
    
    
      _theServlet.destroy();
    
    
    
      }
    
    
    
      }
    
    
    
      
    
    
    
      protected String getServletName(){
    
    
    
      return _servletname;
    
    
    
      }
    
    
    
      }

 ```
  
  
    其中的ServletConfig保存Servlet相关信息。ServletContext保存所有的Servlet对象。WebAppClassLoader为自定义class loader,参见http://blog.csdn.net/tyrone1979/archive/2006/09/03/1164262.aspx。
  
  
  
    最后编写测试类Main，该类模拟10个用户访问Servlet，5人访问DefaultServlet，5人访问UserServlet。
  
  
    ```java
 package org.colimas.main; 
    
    
      
    
    
    
      import java.io.IOException;
    
    
    
      
    
    
    
      import javax.servlet.Servlet;
    
    
    
      import javax.servlet.ServletConfig;
    
    
    
      import javax.servlet.ServletException;
    
    
    
      
    
    
    
      import org.colimas.webapp.HttpServletRequestWrapper;
    
    
    
      import org.colimas.webapp.HttpServletResponseWrapper;
    
    
    
      import org.colimas.webapp.ServletConfigImpl;
    
    
    
      import org.colimas.webapp.ServletWrapper;
    
    
    
      import org.colimas.webapp.ServletWrapperImp;
    
    
    
      import org.colimas.webapp.WebAppContext;
    
    
    
      
    
    
    
      public class Main {
    
    
    
      
    
    
    
      private ThreadGroup _threadGroup;
    
    
    
      private Thread[] _threads;
    
    
    
      String defaultServletName="org.colimas.servlet.DefaultServlet";
    
    
    
      String userServletName="org.colimas.servlet.UserServlet";
    
    
    
      WebAppContext context=WebAppContext.newInstance();
    
    
    
      
    
    
    
      public void doStart(){
    
    
    
      
    
    
    
      _threadGroup=new ThreadGroup("SERVLETS");
    
    
    
      int i=0;
    
    
    
      _threads=new ServletThread[10]; //模拟10位用户。
    
    
    
      for(i=0;i<5;i++){
    
    
    
      _threads[i]=new ServletThread(_threadGroup,new Integer(i).toString(),
    
    
    
      defaultServletName);
    
    
    
      _threads[i].start();
    
    
    
      }
    
    
    
      for(i=5;i<10;i++){
    
    
    
      _threads[i]=new ServletThread(_threadGroup,new Integer(i).toString(),
    
    
    
      userServletName);
    
    
    
      _threads[i].start();
    
    
    
      }
    
    
    
      
    
    
    
      }
    
    
    
      /**
    
    
    
      * @param args
    
    
    
      */
    
    
    
      public static void main(String[] args) {
    
    
    
      Main _main=new Main();
    
    
    
      _main.doStart();
    
    
    
      
    
    
    
      }
    
    
    
      //模拟用户线程
    
    
    
      private class ServletThread extends Thread{
    
    
    
      
    
    
    
      private String servletName;
    
    
    
      
    
    
    
      public ServletThread(ThreadGroup group,String threadname,String servletname){
    
    
    
      super(group,threadname);
    
    
    
      servletName=servletname;
    
    
    
      }
    
    
    
      //调用Servlet的service.
    
    
    
      public void run() { //用户调用Servlet
    
    
    
      ServletConfig config=new ServletConfigImpl(servletName,context); //调用的Servlet信息。
    
    
    
      ServletWrapperImp wrapper=new ServletWrapperImp(config);
    
    
    
      try {
    
    
    
      Servlet defaultServlet=wrapper.getServlet(); //获得Servlet对象，实际是Servlet的代理对象
    
    
    
      defaultServlet.service(new HttpServletRequestWrapper(),
    
    
    
      new HttpServletResponseWrapper()); 调用代理对象的service方法，参见ServletHandler的invoke方法。
    
    
    
      } catch (ServletException e) {
    
    
    
      e.printStackTrace();
    
    
    
      } catch(IOException e){
    
    
    
      
    
    
    
      }
    
    
    
      }
    
    
    
      
    
    
    
      }
    
    
    
      }
 
 ```
  
    HttpServletRequestWrapper和HttpServletResponseWrapper实现HttpServletRequest，和HttpServletResponse。
  
  
    测试结果如下
  
  
    org.colimas.servlet.DefaultServlet:Init servlet starting...
  
  
    org.colimas.servlet.DefaultServlet:Running init
  
  
    org.colimas.servlet.DefaultServlet:Init servlet ending...
  
  
    org.colimas.servlet.UserServlet:Init servlet starting...
  
  
    org.colimas.servlet.UserServlet:Running init
  
  
    org.colimas.servlet.UserServlet:Init servlet ending...
  
  
    org.colimas.servlet.DefaultServlet:service starting...
  
  
    org.colimas.servlet.DefaultServlet:service ending...
  
  
    org.colimas.servlet.DefaultServlet:service starting...
  
  
    org.colimas.servlet.DefaultServlet:service ending...
  
  
    org.colimas.servlet.UserServlet:service starting...
  
  
    org.colimas.servlet.UserServlet:Do UserSErvlet Get
  
  
    org.colimas.servlet.UserServlet:service ending...
  
  
    org.colimas.servlet.UserServlet:service starting...
  
  
    org.colimas.servlet.UserServlet:Do UserSErvlet Get
  
  
    org.colimas.servlet.UserServlet:service ending...
  
  
    org.colimas.servlet.UserServlet:service starting...
  
  
    org.colimas.servlet.UserServlet:Do UserSErvlet Get
  
  
    org.colimas.servlet.UserServlet:service ending...
  
  
    org.colimas.servlet.UserServlet:service starting...
  
  
    org.colimas.servlet.DefaultServlet:service starting...
  
  
    org.colimas.servlet.UserServlet:service starting...
  
  
    org.colimas.servlet.DefaultServlet:service starting...
  
  
    org.colimas.servlet.DefaultServlet:service starting...
  
  
    org.colimas.servlet.UserServlet:Do UserSErvlet Get
  
  
    org.colimas.servlet.DefaultServlet:service ending...
  
  
    org.colimas.servlet.UserServlet:Do UserSErvlet Get
  
  
    org.colimas.servlet.DefaultServlet:service ending...
  
  
    org.colimas.servlet.DefaultServlet:service ending...
  
  
    org.colimas.servlet.UserServlet:service ending...
  
  
    org.colimas.servlet.UserServlet:service ending...
  
  
  
    2个Servlet第一次Load时初始化，被调用init，之后保存到ServletContext中。第二次直接从ServletContext获得，执行service。红字表示代理类里增加的输出结果。
  
  
  
    4．动态代理的限制
  
  
                  JDK的动态代理并不能随心所欲的代理所有的类。Proxy.newProxyInstance方法的第二个参数只能是接口数组， 也就是Proxy只能代理接口。
  