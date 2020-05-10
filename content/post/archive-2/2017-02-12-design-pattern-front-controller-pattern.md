---
title: '[Design Pattern] Front Controller Pattern'
author: wiloon
type: post
date: 2017-02-12T11:45:56+00:00
url: /?p=9800
categories:
  - Uncategorized

---
http://www.cnblogs.com/TonyYPZhang/p/5516192.html

&nbsp;

Front Controller Pattern， 即前端控制器模式，用于集中化用户请求，使得所有请求都经过同一个前端控制器处理，处理内容有身份验证、权限验证、记录和追踪请求等，处理后再交由分发器把请求分发到对于的处理者。

前端控制器模式主要涉及下面三个角色

前端控制器(Front Controller) &#8211; 一个处理器用于处理全部的用户请求

分发器(Dispatcher) &#8211; 把处理后的请求分发到对于的业务处理程序

视图(View) &#8211; 真正处理请求业务程序

&nbsp;

下面是前端控制器的一个简单案例。

HomeView, StudentView 分别是具体业务处理程序。Dispatcher 用于把请求分发到对于的 View 中。FrontController 是所有用户请求的入口，进行身份验证、权限验证、记录或追踪请求日志。FrontControllerDemo 演示前端控制器模式。

&nbsp;

代码实现

HomeView, StudentView 提供真正的业务处理逻辑

public class HomeView {

public void show(){
  
System.out.println(&#8220;show Home view &#8220;);
  
}
  
}
  
public class StudentView {

public void show(){
  
System.out.println(&#8220;show student view &#8220;);
  
}
  
}
  
Dispatcher 分发用户的请求到对应业务处理程序
  
public class Dispatcher {

private StudentView studentView;
  
private HomeView homeView;

public Dispatcher(){
  
homeView = new HomeView();
  
studentView = new StudentView();
  
}

public void dispatch(String viewName){
  
if (&#8220;homeView&#8221;.equals(viewName)){
  
homeView.show();
  
}
  
else {
  
studentView.show();
  
}
  
}
  
}

FrontController 用于处理全部用户请求，进行身份验证、权限验证、请求记录或追踪，然后交由 Dispatcher 分发请求
  
public class FrontController {

private Dispatcher dispatcher;

public FrontController(){
  
dispatcher = new Dispatcher();
  
}

public boolean isAuthenticUser(){
  
System.out.println(&#8220;Authenticate user&#8221;);
  
return true;
  
}

public void trackRequest(String viewName){
  
System.out.println(&#8220;track request &#8221; + viewName);
  
}

public void dispatchRequest(String viewName){
  
trackRequest(viewName);
  
if (isAuthenticUser()){
  
dispatcher.dispatch(viewName);
  
}
  
}
  
}

演示前端控制器模式。
  
public class FrontControllerPatternDemo {

public static void main(){

FrontController frontController = new FrontController();

String viewName = &#8220;homeView&#8221;;
  
frontController.dispatchRequest(viewName);

viewName = &#8220;studentView&#8221;;
  
frontController.dispatchRequest(viewName);
  
}
  
}