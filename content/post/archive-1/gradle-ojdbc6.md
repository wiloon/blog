---
title: gradle ojdbc6
author: "-"
date: 2014-03-04T06:17:30+00:00
url: /?p=6318
categories:
  - Uncategorized
tags:
  - Gradle

---
## gradle ojdbc6
install ojdbc into loacal repo  http://www.wiloon.com/?p=4863

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

http://forums.gradle.org/gradle/topics/access_a_oracle_db_runs_no_more_with_gradle_1_0_rc_3

http://blog.csdn.net/howdy_world/article/details/25650281