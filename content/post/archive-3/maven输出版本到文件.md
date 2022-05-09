---
title: maven输出版本到文件
author: "-"
date: 2020-03-22T05:34:20+00:00
url: /?p=15799
categories:
  - Inbox
tags:
  - reprint
---
## maven输出版本到文件
https://stackoverflow.com/questions/3532135/using-maven-to-output-the-version-number-to-a-text-file

Create a text file somewhere in src/main/resources, call it version.txt (or whatever)

File content:

${project.version}

now in your pom.xml, inside the build element, put this block:

```xml
<build>
  <resources>
    <resource>
      <directory>src/main/resources</directory>
      <filtering>true</filtering>
      <includes>
        <include>**/version.txt</include>
      </includes>
    </resource>
    <resource>
      <directory>src/main/resources</directory>
      <filtering>false</filtering>
      <excludes>
        <exclude>**/version.txt</exclude>
      </excludes>
    </resource>
    ...
  </resources>
</build>
```