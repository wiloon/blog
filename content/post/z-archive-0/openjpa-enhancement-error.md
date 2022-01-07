---
title: openJPA enhancement error
author: "-"
date: 2011-12-28T04:18:46+00:00
url: /?p=2041
categories:
  - Development
tags:
  - openJPA

---
## openJPA enhancement error
<openjpa-2.1.1-r422266:1148538 nonfatal user error> org.apache.openjpa.persistence.ArgumentException: This configuration disallows runtime optimization, but the following listed types were not enhanced at build time or at class load time with a javaagent: "
  
com.wiloon.openjpa.entity.Animal".

add line :

<property name="openjpa.RuntimeUnenhancedClasses" value="supported" />

in persistence.xml