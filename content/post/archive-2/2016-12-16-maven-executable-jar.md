---
title: java maven 可执行 jar/ executable jar
author: wiloon
type: post
date: 2016-12-16T07:45:40+00:00
url: /?p=9566
categories:
  - Uncategorized
tags:
  - Java
  - Maven

---
[xml]

<plugin>
  
<artifactId>maven-assembly-plugin</artifactId>
  
<configuration>
  
<archive>
  
<manifest>
  
<mainClass>
  
com.wiloon.xxx.xxx.xxx
  
</mainClass>
  
</manifest>
  
</archive>
  
<descriptorRefs>
  
<descriptorRef>jar-with-dependencies</descriptorRef>
  
</descriptorRefs>
  
</configuration>
  
</plugin>

[/xml]



[shell]

mvn assembly:assembly

[/shell]