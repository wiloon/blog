---
title: shiro 标签
author: "-"
date: 2013-01-20T03:01:22+00:00
url: /?p=5046
categories:
  - Java
  - Web
tags:
  - reprint
---
## shiro 标签
[http://kdboy.iteye.com/blog/1155450](http://kdboy.iteye.com/blog/1155450)

授权即访问控制,它将判断用户在应用程序中对资源是否拥有相应的访问权限。
  
如,判断一个用户有查看页面的权限,编辑数据的权限,拥有某一按钮的权限,以及是否拥有打印的权限等等。

**一、授权的三要素**

授权有着三个核心元素: 权限、角色和用户。

**权限**
  
权限是Apache Shiro安全机制最核心的元素。它在应用程序中明确声明了被允许的行为和表现。一个格式良好好的权限声明可以清晰表达出用户对该资源拥有的权限。
  
大多数的资源会支持典型的CRUD操作 (create,read,update,delete) ,但是任何操作建立在特定的资源上才是有意义的。因此,权限声明的根本思想就是建立在资源以及操作上。
  
而我们通过权限声明仅仅能了解这个权限可以在应用程序中做些什么,而不能确定谁拥有此权限。
  
于是,我们就需要在应用程序中对用户和权限建立关联。
  
通常的做法就是将权限分配给某个角色,然后将这个角色关联一个或多个用户。

**权限声明及粒度**
  
Shiro权限声明通常是使用以冒号分隔的表达式。就像前文所讲,一个权限表达式可以清晰的指定资源类型,允许的操作,可访问的数据。同时,Shiro权限表达式支持简单的通配符,可以更加灵活的进行权限设置。
  
下面以实例来说明权限表达式。
  
可查询用户数据
  
User:view
  
可查询或编辑用户数据
  
User:view,edit
  
可对用户数据进行所有操作
  
User:* 或 user
  
可编辑id为123的用户数据
  
User:edit:123

**角色**
  
Shiro支持两种角色模式: 
  
1. 传统角色: 一个角色代表着一系列的操作,当需要对某一操作进行授权验证时,只需判断是否是该角色即可。这种角色权限相对简单、模糊,不利于扩展。
  
2. 权限角色: 一个角色拥有一个权限的集合。授权验证时,需要判断当前角色是否拥有该权限。这种角色权限可以对该角色进行详细的权限描述,适合更复杂的权限设计。
  
下面将详细描述对两种角色模式的授权实现。

**二、授权实现**

Shiro支持三种方式实现授权过程: 

  * 编码实现
  * 注解实现
  * JSP Taglig实现

**1、基于编码的授权实现**

**1.1基于传统角色授权实现**
  
当需要验证用户是否拥有某个角色时,可以调用Subject 实例的hasRole*方法验证。


  
    
      Java代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      Subject currentUser = SecurityUtils.getSubject();
    
    
      if (currentUser.hasRole("administrator")) {
    
    
          //show the admin button
    
    
      } else {
    
    
          //don't show the button?  Grey it out?
    
    
      }
    
  

相关验证方法如下: 


  
    
      Subject方法
    
    
    
      描述
    
  
  
  
    
      hasRole(String roleName)
    
    
    
      当用户拥有指定角色时,返回true
    
  
  
  
    
      hasRoles(List<String> roleNames)
    
    
    
      按照列表顺序返回相应的一个boolean值数组
    
  
  
  
    
      hasAllRoles(Collection<String> roleNames)
    
    
    
      如果用户拥有所有指定角色时,返回true
    
  


**断言支持**
  
Shiro还支持以断言的方式进行授权验证。断言成功,不返回任何值,程序继续执行；断言失败时,将抛出异常信息。使用断言,可以使我们的代码更加简洁。


  
    
      Java代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      Subject currentUser = SecurityUtils.getSubject();
    
    
      //guarantee that the current user is a bank teller and
    
    
      //therefore allowed to open the account:
    
    
      currentUser.checkRole("bankTeller");
    
    
      openBankAccount();
    
  

断言的相关方法: 


  
    
      Subject方法
    
    
    
      描述
    
  
  
  
    
      checkRole(String roleName)
    
    
    
      断言用户是否拥有指定角色
    
  
  
  
    
      checkRoles(Collection<String> roleNames)
    
    
    
      断言用户是否拥有所有指定角色
    
  
  
  
    
      checkRoles(String... roleNames)
    
    
    
      对上一方法的方法重载
    
  


**1.2 基于权限角色授权实现**
  
相比传统角色模式,基于权限的角色模式耦合性要更低些,它不会因角色的改变而对源代码进行修改,因此,基于权限的角色模式是更好的访问控制方式。
  
它的代码实现有以下几种实现方式: 
  
**1、基于权限对象的实现**
  
创建org.apache.shiro.authz.Permission的实例,将该实例对象作为参数传递给Subject.isPermitted () 进行验证。


  
    
      Java代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      Permission printPermission = new PrinterPermission("laserjet4400n", "print");
    
    
      Subject currentUser = SecurityUtils.getSubject();
    
    
      if (currentUser.isPermitted(printPermission)) {
    
    
          //show the Print button
    
    
      } else {
    
    
          //don't show the button?  Grey it out?
    
    
      }
    
    
      Permission printPermission = new PrinterPermission("laserjet4400n", "print");
    
    
      Subject currentUser = SecurityUtils.getSubject();
    
    
      if (currentUser.isPermitted(printPermission)) {
    
    
          //show the Print button
    
    
      } else {
    
    
          //don't show the button?  Grey it out?
    
    
      }
    
  

相关方法如下: 


  
    
      Subject方法
    
    
    
      描述
    
  
  
  
    
      isPermitted(Permission p)
    
    
    
      Subject拥有制定权限时,返回treu
    
  
  
  
    
      isPermitted(List<Permission> perms)
    
    
    
      返回对应权限的boolean数组
    
  
  
  
    
      isPermittedAll(Collection<Permission> perms)
    
    
    
      Subject拥有所有制定权限时,返回true
    
  


**2、 基于字符串的实现**
  
相比笨重的基于对象的实现方式,基于字符串的实现便显得更加简洁。


  
    
      Java代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      Subject currentUser = SecurityUtils.getSubject();
    
    
      if (currentUser.isPermitted("printer:print:laserjet4400n")) {
    
    
          //show the Print button
    
    
      } else {
    
    
          //don't show the button?  Grey it out?
    
    
      }
    
  

使用冒号分隔的权限表达式是org.apache.shiro.authz.permission.WildcardPermission 默认支持的实现方式。
  
这里分别代表了 资源类型: 操作: 资源ID

类似基于对象的实现相关方法,基于字符串的实现相关方法: 
  
isPermitted(String perm)、isPermitted(String... perms)、isPermittedAll(String... perms)

**基于权限对象的断言实现**


  
    
      Java代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      Subject currentUser = SecurityUtils.getSubject();
    
    
      //guarantee that the current user is permitted
    
    
      //to open a bank account:
    
    
      Permission p = new AccountPermission("open");
    
    
      currentUser.checkPermission(p);
    
    
      openBankAccount();
    
  

**基于字符串的断言实现**


  
    
      Java代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      Subject currentUser = SecurityUtils.getSubject();
    
    
      //guarantee that the current user is permitted
    
    
      //to open a bank account:
    
    
      currentUser.checkPermission("account:open");
    
    
      openBankAccount();
    
  

断言实现的相关方法


  
    
      Subject方法
    
    
    
      说明
    
  
  
  
    
      checkPermission(Permission p)
    
    
    
      断言用户是否拥有制定权限
    
  
  
  
    
      checkPermission(String perm)
    
    
    
      断言用户是否拥有制定权限
    
  
  
  
    
      checkPermissions(Collection<Permission> perms)
    
    
    
      断言用户是否拥有所有指定权限
    
  
  
  
    
      checkPermissions(String... perms)
    
    
    
      断言用户是否拥有所有指定权限
    
  


**2、基于注解的授权实现**
  
Shiro注解支持AspectJ、Spring、Google-Guice等,可根据应用进行不同的配置。

相关的注解: 
  
**@ RequiresAuthentication**
  
可以用户类/属性/方法,用于表明当前用户需是经过认证的用户。


  
    
      Java代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      @RequiresAuthentication
    
    
      public void updateAccount(Account userAccount) {
    
    
          //this method will only be invoked by a
    
    
          //Subject that is guaranteed authenticated
    
    
          ...
    
    
      }
    
  

**@ RequiresGuest**
  
表明该用户需为"guest"用户

**@ RequiresPermissions**
  
当前用户需拥有制定权限


  
    
      Java代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      @RequiresPermissions("account:create")
    
    
      public void createAccount(Account account) {
    
    
          //this method will only be invoked by a Subject
    
    
          //that is permitted to create an account
    
    
          ...
    
    
      }
    
  

**@RequiresRoles**
  
当前用户需拥有制定角色

**@ RequiresUser**
  
当前用户需为已认证用户或已记住用户

**3、基于JSP  TAG的授权实现**
  
Shiro提供了一套JSP标签库来实现页面级的授权控制。
  
在使用Shiro标签库前,首先需要在JSP引入shiro标签: 


  
    
      Java代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      <%@ taglib prefix="shiro" uri="http://shiro.apache.org/tags" %>
    
  

下面一一介绍Shiro的标签: 
  
guest标签
  
验证当前用户是否为"访客",即未认证 (包含未记住) 的用户


  
    
      Xml代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      <shiro:guest>
    
    
          Hi there!  Please Login or Signup today!
    
    
      </shiro:guest>
    
  

user标签
  
认证通过或已记住的用户


  
    
      Xml代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      <shiro:user>
    
    
          Welcome back John!  Not John? Click here to login.
    
    
      </shiro:user>
    
  

authenticated标签
  
已认证通过的用户。不包含已记住的用户,这是与user标签的区别所在。


  
    
      Xml代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      <shiro:authenticated>
    
    
          Update your contact information.
    
    
      </shiro:authenticated>
    
  

notAuthenticated标签
  
未认证通过用户,与authenticated标签相对应。与guest标签的区别是,该标签包含已记住用户。


  
    
      Xml代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      <shiro:notAuthenticated>
    
    
          Please login in order to update your credit card information.
    
    
      </shiro:notAuthenticated>
    
  

principal 标签
  
输出当前用户信息,通常为登录帐号信息


  
    
      Xml代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      Hello, <shiro:principal/>, how are you today?
    
  

hasRole标签
  
验证当前用户是否属于该角色


  
    
      Xml代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      <shiro:hasRole name="administrator">
    
    
          Administer the system
    
    
      </shiro:hasRole>
    
  

lacksRole标签
  
与hasRole标签逻辑相反,当用户不属于该角色时验证通过


  
    
      Xml代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      <shiro:lacksRole name="administrator">
    
    
          Sorry, you are not allowed to administer the system.
    
    
      </shiro:lacksRole>
    
  

hasAnyRole标签
  
验证当前用户是否属于以下任意一个角色。


  
    
      Xml代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      <shiro:hasAnyRoles name="developer, project manager, administrator">
    
    
          You are either a developer, project manager, or administrator.
    
    
      </shiro:lacksRole>
    
  

hasPermission标签
  
验证当前用户是否拥有制定权限


  
    
      Xml代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      <shiro:hasPermission name="user:create">
    
    
          Create a new User
    
    
      </shiro:hasPermission>
    
  

lacksPermission标签
  
与hasPermission标签逻辑相反,当前用户没有制定权限时,验证通过


  
    
      Xml代码  <img alt="收藏代码" src="http://kdboy.iteye.com/images/icon_star.png" />
  
  
  
    
      <shiro:hasPermission name="user:create">
    
    
          Create a new User
    
    
      </shiro:hasPermission>
    
  
