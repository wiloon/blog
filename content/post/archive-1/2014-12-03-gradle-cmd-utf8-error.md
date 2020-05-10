---
title: gradle cmd utf8 error
author: wiloon
type: post
date: 2014-12-03T03:20:58+00:00
url: /?p=7083
categories:
  - Uncategorized
tags:
  - Gradle

---
[shell]

export GRADLE_OPTS="-Dfile.encoding=utf-8"

[/shell]

&nbsp;

add

[java]

tasks.withType(JavaCompile) {
  
options.encoding = "UTF-8"
  
}

[/java]

&nbsp;

&nbsp;

The `file.encoding` system property needs to be set right when the JVM executing the Gradle build (e.g. the Gradle Daemon) starts up. One way to achieve this is with `export GRADLE_OPTS="-Dfile.encoding=utf-8"`. Another way that might work is to add `systemProp.file.encoding=utf-8`to `gradle.properties`. Of course this assumes that the build script files are actually using utf-8 encoding. To see what your platform&#8217;s (and therefore Gradle&#8217;s) default encoding is, print out the system property&#8217;s value in a build script.

&nbsp;

http://blog.csdn.net/whu_zhangmin/article/details/46468061

http://stackoverflow.com/questions/21267234/show-utf-8-text-properly-in-gradle