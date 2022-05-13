---
title: spring @ModelAttribute
author: "-"
date: 2012-12-17T15:04:26+00:00
url: /?p=4921
categories:
  - Java
  - Web
tags:
  - reprint
---
## spring @ModelAttribute

通过 SpringMVC 的 SessionAttributes Annotation 关联 User 属性

SpringMVC 文档提到了 @SessionAttributes annotation,和 @ModelAttribute 配合使用可以往 Session 中存或者从 Session 中取指定属性名的具体对象。

,@SessionAttributes 是用来在 controller 内部共享 model 属性的。从文档自带的例子来看,标注成 @SessionAttributes 属性的对象,会一直保留在 Session 或者其他会话存储中,直到 SessionStatus 被显式 setComplete()。那这个 annotation 对我们有什么帮助呢？

答案就是我们可以在需要访问 Session 属性的 controller 上加上 @SessionAttributes,然后在 action 需要的 User 参数上加上 @ModelAttribute,并保证两者的属性名称一致。SpringMVC 就会自动将 @SessionAttributes 定义的属性注入到 ModelMap 对象,在 setup action 的参数列表时,去 ModelMap 中取到这样的对象,再添加到参数列表。只要我们不去调用 SessionStatus 的 setComplete() 方法,这个对象就会一直保留在 Session 中,从而实现 Session 信息的共享。

controller的代码如下:

@Controller

@SessionAttributes("currentUser")

public class GreetingController{

@RequestMapping

public void hello(@ModelAttribute("currentUser") User user){

//user.sayHello()

}

}

使用这种方案,还需要在 SpringMVC 配置文件的 ViewResolver 定义处,加上 p:allowSessionOverride="true",这样如果你对 User 对象做了修改,SpringMVC 就会在渲染 View 的同时覆写 Session 中的相关属性。
