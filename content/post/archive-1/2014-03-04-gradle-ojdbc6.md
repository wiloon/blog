---
title: gradle ojdbc6
author: wiloon
type: post
date: 2014-03-04T06:17:30+00:00
url: /?p=6318
categories:
  - Uncategorized
tags:
  - Gradle

---
install ojdbc into loacal repo  http://www.wiloon.com/wordpress/?p=4863

modify build.gradle, then gradle can search local maven repo

[java]
  
apply plugin: &#8216;java&#8217;

apply plugin: &#8216;eclipse&#8217;

apply plugin: &#8216;war&#8217;

apply plugin: "maven"

repositories {

mavenCentral()

maven {

name &#8216;local-repo&#8217;

url &#8216;file:///D:/dev/mavenRepo/&#8217;

}

}
  
[/java]

http://forums.gradle.org/gradle/topics/access\_a\_oracle\_db\_runs\_no\_more\_with\_gradle\_1\_0\_rc\_3





http://blog.csdn.net/howdy_world/article/details/25650281