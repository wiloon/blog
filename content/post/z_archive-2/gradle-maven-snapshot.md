---
title: gradle maven snapshot
author: "-"
date: 2016-11-06T03:54:47+00:00
url: /?p=9362
categories:
  - Inbox
tags:
  - reprint
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
