---
title: Jenkins basic
author: "-"
date: 2011-09-30T06:56:52+00:00
url: /?p=990
categories:
  - CI
tags:
  - Jenkins

---
## Jenkins basic

## archlinux install jenkins

```bash
# 直接 pacman 安装
pacman -S jenkins
# start jenkins
systectl start jenkins
```

jenkins 默认用 jenkins 用户启动和执行编译

jenkins 默认的 home 目录 /var/lib/jenkins/, 比如 .ssh 目录的位置 /var/lib/jenkins/.ssh

## docker 

```bash
docker run \
  --name jenkins \
  --rm \
  --detach \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --volume jenkins-data:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind \
  --storage-driver overlay2
```

## Jenkins setup

* download jenkins.war; [http://mirrors.jenkins-ci.org/war/1.432/](http://mirrors.jenkins-ci.org/war/1.432/)
* deploy the war to jboss(version:4.0.5.GA) or tomcat
* start jboss
* open url [http://localhost:8080/jenkins](http://localhost:8080/jenkins)
* navigate to  Manage Jenkins>Configure system
* configure name and path for maven
* go to jenkins > manage jenkins> manage plugins>advanced
* configure proxy (optional)
* click "choose file" to upload the plugin; e.g.: git plugin
* restart jboss
* go to jenkins>Manage Jenkins>Configure system
* configure name and path for git plugin(optional)
* Create a new job, jenkins>new item
* input job name , select **Build a free-style software project**
* **[Source Code Management], select git, input URL of repository**
* **[build], click "add build step",  select invoke top-level Maven targets**
* **select maven version**
* **input Goals. e.g. clean, install, surefire-report:report, cobertura:cobertura**

## Jenkins plugins

[http://updates.jenkins-ci.org/download/plugins/](http://updates.jenkins-ci.org/download/plugins/)

## jenkins sender email address

Jenkins uses the _System Admin e-mail address_ as the sender address for e-mail notification. You can configure this under _Manage Jenkins -> Configure System_. This is under the _Jenkins Location_ header on that page

[http://stackoverflow.com/questions/9693526/how-can-i-set-the-senders-address-in-jenkins](http://stackoverflow.com/questions/9693526/how-can-i-set-the-senders-address-in-jenkins)
