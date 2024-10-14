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

## jenkins docker

```Bash
docker network create jenkins

docker image pull docker:dind

# generate cert
su - root
mkdir /root/certs && cd /root/certs
openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out MyCertificate.crt -keyout MyKey.key

docker run \
  --name jenkins-docker \
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

### dockerfile

创建镜像

```Bash
FROM jenkins/jenkins:2.480-jdk21
USER root
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli
USER jenkins
```

构建镜像

```Bash
docker build -t myjenkins .
```

```Bash

运行容器

docker run \
  --name jenkins \
  --restart=on-failure \
  --detach \
  --network jenkins \
  --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  jekins0

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

  * **
  
**

## Jenkins plugins

[http://updates.jenkins-ci.org/download/plugins/](http://updates.jenkins-ci.org/download/plugins/)

## jenkins sender email address

Jenkins uses the _System Admin e-mail address_ as the sender address for e-mail notification. You can configure this under _Manage Jenkins -> Configure System_. This is under the _Jenkins Location_ header on that page

[http://stackoverflow.com/questions/9693526/how-can-i-set-the-senders-address-in-jenkins](http://stackoverflow.com/questions/9693526/how-can-i-set-the-senders-address-in-jenkins)
