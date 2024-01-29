---
title: 'Integration of Angular  with Spring MVC'
author: "-"
date: 2019-12-18T09:53:42+00:00
url: /?p=15220
categories:
  - Inbox
tags:
  - reprint
---
## 'Integration of Angular  with Spring MVC'
https://stackoverflow.com/questions/50481885/integration-of-angular-5-with-spring-mvc

1.Create normal Dynamic web project.
  
2.Add all dependancy required for spring or user maven pom.xml
  
3.Open CMD, navigate to angular2 application. Hit command

'npm install'

and then

'ng build'

or use 'ng build -prod' for production build.
  
this command will create a "dist" folder, copy all files including all folders.


  
    Paste those files and folders into 'WebContent' directory.
  
  
    Last thing, you need to change basehref="./" in index.html.
  
