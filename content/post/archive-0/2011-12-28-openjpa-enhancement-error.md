---
title: openJPA enhancement error
author: wiloon
type: post
date: 2011-12-28T04:18:46+00:00
url: /?p=2041
categories:
  - Development
tags:
  - openJPA

---
<openjpa-2.1.1-r422266:1148538 nonfatal user error> org.apache.openjpa.persistence.ArgumentException: This configuration disallows runtime optimization, but the following listed types were not enhanced at build time or at class load time with a javaagent: &#8221;
  
com.wiloon.openjpa.entity.Animal&#8221;.

add line :

<property name=&#8221;openjpa.RuntimeUnenhancedClasses&#8221; value=&#8221;supported&#8221; />

in persistence.xml