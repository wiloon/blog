---
title: Acegi
author: "-"
date: 2012-11-13T13:33:43+00:00
url: /?p=4657
categories:
  - Java
  - Web

---
## Acegi
Acegi安全系统，是一个用于Spring Framework的安全框架，能够和目前流行的Web容器无缝集成。它使用了Spring的方式提供了安全和认证安全服务，包括使用Bean Context，拦截器和面向接口的编程方式。因此，Acegi安全系统能够轻松地适用于复杂的安全需求。

Acegi成为Spring子项目后改名为Spring Security。查看安全权限管理手册<sup>[1]</sup>。

安全涉及到两个不同的概念，认证和授权。前者是关于确认用户是否确实是他们所宣称的身份。授权则是关于确认用户是否有允许执行一个特定的操作。

在Acegi安全系统中，需要被认证的用户，系统或代理称为"Principal"。Acegi安全系统和其他的安全系统不同，它并没有角色和用户组的概念。