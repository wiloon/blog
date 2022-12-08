---
title: '设计模式, Design Pattern, Front Controller Pattern'
author: "-"
date: 2017-02-12T11:45:56+00:00
url: /?p=9800
categories:
  - Pattern
tags:
  - reprint
---
## 设计模式, Design Pattern, Front Controller Pattern

<http://www.cnblogs.com/TonyYPZhang/p/5516192.html>

Front Controller Pattern, 即前端控制器模式,用于集中化用户请求,使得所有请求都经过同一个前端控制器处理,处理内容有身份验证、权限验证、记录和追踪请求等,处理后再交由分发器把请求分发到对于的处理者。

前端控制器模式主要涉及下面三个角色

前端控制器(Front Controller) - 一个处理器用于处理全部的用户请求

分发器(Dispatcher) - 把处理后的请求分发到对于的业务处理程序

视图(View) - 真正处理请求业务程序

下面是前端控制器的一个简单案例。

HomeView, StudentView 分别是具体业务处理程序。Dispatcher 用于把请求分发到对于的 View 中。FrontController 是所有用户请求的入口,进行身份验证、权限验证、记录或追踪请求日志。FrontControllerDemo 演示前端控制器模式。

代码实现

HomeView, StudentView 提供真正的业务处理逻辑

public class HomeView {

public void show(){
  
System.out.println("show Home view ");
  
}
  
}
  
public class StudentView {

public void show(){
  
System.out.println("show student view ");
  
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
  
if ("homeView".equals(viewName)){
  
homeView.show();
  
}
  
else {
  
studentView.show();
  
}
  
}
  
}

FrontController 用于处理全部用户请求,进行身份验证、权限验证、请求记录或追踪,然后交由 Dispatcher 分发请求
  
public class FrontController {

private Dispatcher dispatcher;

public FrontController(){
  
dispatcher = new Dispatcher();
  
}

public boolean isAuthenticUser(){
  
System.out.println("Authenticate user");
  
return true;
  
}

public void trackRequest(String viewName){
  
System.out.println("track request " + viewName);
  
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

String viewName = "homeView";
  
frontController.dispatchRequest(viewName);

viewName = "studentView";
  
frontController.dispatchRequest(viewName);
  
}
  
}
