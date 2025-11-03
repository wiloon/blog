---
title: java main函数 执行spring 代码
author: "-"
date: 2015-09-22T07:42:57+00:00
url: /?p=8327
categories:
  - Inbox
tags:
  - reprint
---
## java main函数 执行spring 代码
```java

package com.zuidaima.test;

import org.springframework.context.support.GenericXmlApplicationContext;

import com.service.UserService;

public class Main {

public static void main(String[] args) throws InterruptedException {
  
GenericXmlApplicationContext context = new GenericXmlApplicationContext();
  
context.setValidating(false);
  
context.load("classpath\*:applicationContext\*.xml");
  
context.refresh();
  
UserService userService = context.getBean(UserService.class);
  
while (true) {
  
System.out.println(userService.findUser());
  
Thread.sleep(10000);
  
}
  
}
  
}

```