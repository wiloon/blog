---
title: jib-maven-plugin
author: "-"
date: 2013-02-21T03:25:59+00:00
url: jib-maven-plugin
categories:
  - Maven
tags:
  - reprint
---
## jib-maven-plugin

Jib 是一个构建 Docker 或者 OCI 镜像的 Maven 插件

[https://github.com/GoogleContainerTools/jib/tree/master/jib-maven-plugin](https://github.com/GoogleContainerTools/jib/tree/master/jib-maven-plugin)

```xml
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <version>3.2.1</version>
    <configuration>
        <from>
            <image>openjdk:17.0.2-jdk</image>
        </from>
        <to>
            <image>${docker.prefix}foo/${project.name}:${project.version}</image>
        </to>
        <container>
            <environment>
                <TZ>Asia/Shanghai</TZ>
            </environment>
            <jvmFlags>
                <jvmFlag>-Xms128m</jvmFlag>
            </jvmFlags>
            <mainClass>${project.main.class}</mainClass>
            <creationTime>USE_CURRENT_TIMESTAMP</creationTime>
        </container>
    </configuration>
</plugin>
```
