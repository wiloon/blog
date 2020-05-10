---
title: 'Integration of Angular  with Spring MVC'
author: wiloon
type: post
date: 2019-12-18T09:53:42+00:00
url: /?p=15220
categories:
  - Uncategorized

---
https://stackoverflow.com/questions/50481885/integration-of-angular-5-with-spring-mvc

1.Create normal Dynamic web project.
  
2.Add all dependancy required for spring or user maven pom.xml
  
3.Open CMD, navigate to angular2 application. Hit command

&#8216;npm install&#8217;

and then

&#8216;ng build&#8217;

or use &#8216;ng build &#8211;prod&#8217; for production build.
  
this command will create a “dist” folder, copy all files including all folders.

<ol start="4">
  <li>
    Paste those files and folders into &#8216;WebContent&#8217; directory.
  </li>
  <li>
    Last thing, you need to change basehref=”./” in index.html.
  </li>
</ol>