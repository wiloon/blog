---
title: gradle maven snapshot
author: wiloon
type: post
date: 2016-11-06T03:54:47+00:00
url: /?p=9362
categories:
  - Uncategorized

---
configurations.all {
  
// check for updates every build
  
resolutionStrategy.cacheChangingModulesFor 0, &#8216;seconds&#8217;
  
}
  
dependencies {
  
compile group: &#8220;group&#8221;, name: &#8220;projectA&#8221;, version: &#8220;1.1-SNAPSHOT&#8221;, changing: true
  
}

&nbsp;

https://discuss.gradle.org/t/how-to-get-gradle-to-download-newer-snapshots-to-gradle-cache-when-using-an-ivy-repository/7344