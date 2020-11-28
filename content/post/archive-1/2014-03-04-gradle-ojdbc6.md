---
title: gradle ojdbc6
author: w1100n
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

```java
  
apply plugin: 'java'

apply plugin: 'eclipse'

apply plugin: 'war'

apply plugin: "maven"

repositories {

mavenCentral()

maven {

name 'local-repo'

url 'file:///D:/dev/mavenRepo/'

}

}
  
```

http://forums.gradle.org/gradle/topics/access\_a\_oracle\_db\_runs\_no\_more\_with\_gradle\_1\_0\_rc\_3

http://blog.csdn.net/howdy_world/article/details/25650281