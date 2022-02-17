---
title: Jenkins setup
author: "-"
date: 2011-09-30T06:56:52+00:00
url: /?p=990
categories:
  - CI
tags:
  - Jenkins

---
## Jenkins setup
  * download jenkins.war; <http://mirrors.jenkins-ci.org/war/1.432/>
  * deploy the war to jboss(version:4.0.5.GA) or tomcat
  * start jboss
  * open url http://localhost:8080/jenkins
  * navigate to  Manage Jenkins>Configure system
  * configure name and path for maven
  * go to jenkins > manage jenkins> manage plugins>advanced
  * configure proxy (optional)
  * click "choose file" to upload the plugin; e.g.: git plugin
  * restart jboss
  * go to jenkins>Manage Jenkins>Configure system
  * configure name and path for git plugin(optional)
  * Create a new job, jenkins>new item
  *  input job name , select **Build a free-style software project**
  * **[Source Code Management], select git, input URL of repository**
  * **[build], click "add build step",  select invoke top-level Maven targets**
  * **select maven version**
  * **input Goals. e.g. clean, install, surefire-report:report, cobertura:cobertura**
  * **
  
** 


## Jenkins plugins
<http://updates.jenkins-ci.org/download/plugins/>