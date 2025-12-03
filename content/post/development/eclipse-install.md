---
title: eclipse install/setting
author: "-"
date: 2014-01-07T05:38:33+00:00
url: /?p=6163
categories:
  - Inbox
tags:
  - reprint
---
## eclipse install/setting

### plugin

#### eclipse gradle integration

install gradel eclipse integration from eclipse marketplace
  
[https://github.com/spring-projects/eclipse-integration-gradle/](https://github.com/spring-projects/eclipse-integration-gradle/)

##### config gradle heap space

Preference>Gradle>Arguments>JVM Arguments
  
-Xms256m -Xmx512m
  
[http://stackoverflow.com/questions/12585506/eclipse-gradle-sts-extension-could-not-reserve-enough-space-for-object-heap](http://stackoverflow.com/questions/12585506/eclipse-gradle-sts-extension-could-not-reserve-enough-space-for-object-heap)

### git: EGit

### groovy plugin

groovy plugin:[http://groovy.codehaus.org/Eclipse+Plugin](http://groovy.codehaus.org/Eclipse+Plugin)

#### subclipse

[https://github.com/subclipse/subclipse/wiki](https://github.com/subclipse/subclipse/wiki)
  
latest: [https://dl.bintray.com/subclipse/releases/subclipse/latest/](https://dl.bintray.com/subclipse/releases/subclipse/latest/)

### config

window>Preference

### class can not be resolved

[https://crunchify.com/mavenmvn-clean-install-update-project-and-project-clean-options-in-eclipse-ide-to-fix-any-dependency-issue/](https://crunchify.com/mavenmvn-clean-install-update-project-and-project-clean-options-in-eclipse-ide-to-fix-any-dependency-issue/)

### error, no test found with test runner junit 5

[https://stackoverflow.com/questions/46717693/eclipse-no-tests-found-using-junit-5-caused-by-noclassdeffounderror-for-launcher](https://stackoverflow.com/questions/46717693/eclipse-no-tests-found-using-junit-5-caused-by-noclassdeffounderror-for-launcher)
  
test config > junit 4 runner
