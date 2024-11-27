---
title: jetty-maven-plugin, jetty maven plugin
author: "-"
date: 2018-03-06T07:10:51+00:00
url: /?p=11958
categories:
  - maven
tags:
  - reprint
---
## jetty-maven-plugin, jetty maven plugin

### maven plugin

```xml
<plugin>
    <groupId>org.eclipse.jetty</groupId>
    <artifactId>jetty-maven-plugin</artifactId>
    <version>9.4.33.v20201020</version>
    <configuration>
        <stopKey>stop</stopKey>
        <stopPort>5599</stopPort>
        <webApp>
            <!-- <contextPath>/app0</contextPath> -->
            <contextPath>/</contextPath>
            <defaultsDescriptor>src/main/resources/webdefault.xml</defaultsDescriptor>
        </webApp>
        <scanIntervalSeconds>2</scanIntervalSeconds>

        [httpConnector](httpConnector)
            <port>8080</port>
        </httpConnector>
    </configuration>
</plugin>
```

### webdefault.xml

可以去maven的本地仓库找到
  
.m2\repository\org\eclipse\jetty\jetty-webapp\9.4.20.v20190813
  
解压后在这里可以找到webdefault.xml
  
jetty-webapp-9.4.20.v20190813\org\eclipse\jetty\webapp

### run

```bash
mvn jetty:run
mvnDebug jetty:run
# 默认调试端口8000
```

## debug - mvnDebug

[https://blog.wiloon.com/?p=15212](https://blog.wiloon.com/?p=15212)

mvnDebug -suspend默认为n,

>[https://www.eclipse.org/jetty/documentation/jetty-11/programming-guide/index.html#jetty-maven-plugin](https://www.eclipse.org/jetty/documentation/jetty-11/programming-guide/index.html#jetty-maven-plugin)

[http://www.blogjava.net/fancydeepin/archive/2015/06/23/maven-jetty-plugin.html](http://www.blogjava.net/fancydeepin/archive/2015/06/23/maven-jetty-plugin.html)
  
[https://my.oschina.net/jackieyeah/blog/524556](https://my.oschina.net/jackieyeah/blog/524556)
  
[https://stackoverflow.com/questions/7875002/setting-debug-configuration-for-mavenjettyeclipse](https://stackoverflow.com/questions/7875002/setting-debug-configuration-for-mavenjettyeclipse)
