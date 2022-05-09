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


https://discuss.gradle.org/t/how-to-get-gradle-to-download-newer-snapshots-to-gradle-cache-when-using-an-ivy-repository/7344