---
title: gradle maven snapshot
author: "-"
date: 2016-11-06T03:54:47+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: gradle-maven-snapshot
categories:
  - Java
tags:
  - gradle
  - maven
  - remix
  - AI-assisted
aliases:
  - /p8683/
  - /p8813/
  - /p9362/
---
## gradle maven snapshot

configurations.all {
  
// check for updates every build
  
resolutionStrategy.cacheChangingModulesFor 0, 'seconds'
  
}
  
dependencies {
  
compile group: "group", name: "projectA", version: "1.1-SNAPSHOT", changing: true
  
}

[https://discuss.gradle.org/t/how-to-get-gradle-to-download-newer-snapshots-to-gradle-cache-when-using-an-ivy-repository/7344](https://discuss.gradle.org/t/how-to-get-gradle-to-download-newer-snapshots-to-gradle-cache-when-using-an-ivy-repository/7344)

## gradle maven plugin

[https://docs.gradle.org/current/userguide/publishing_maven.html#header](https://docs.gradle.org/current/userguide/publishing_maven.html#header)

gradle v5.3.1

```kotlin
group = "com.wiloon.group0"
version = "0.0.1-SNAPSHOT"

plugins {
    `java-library`
    `maven-publish`
    id("com.gradle.build-scan") version "2.2.1"
}

tasks.register<Jar>("sourcesJar") {
    from(sourceSets.main.get().allJava)
    archiveClassifier.set("sources")
}

tasks.register<Jar>("javadocJar") {
    from(tasks.javadoc)
    archiveClassifier.set("javadoc")
}

publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])
            artifact(tasks["sourcesJar"])
            artifact(tasks["javadocJar"])
        }
    }
    repositories {
        maven {
            val releasesRepoUrl = "http://nexus.wiloon.com/repository/maven-releases"
            val snapshotsRepoUrl = "http://nexus.wiloon.com/repository/maven-snapshots"
            url = uri(if (version.toString().endsWith("SNAPSHOT")) snapshotsRepoUrl else releasesRepoUrl)
            credentials {
                username = "admin"
                password = "password"
            }
        }
    }
}
```

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
