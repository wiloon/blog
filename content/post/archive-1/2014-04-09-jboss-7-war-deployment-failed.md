---
title: Jboss 7 war deployment failed
author: "-"
type: post
date: 2014-04-09T03:11:56+00:00
url: /?p=6496
categories:
  - Uncategorized
tags:
  - Jboss

---
http://stackoverflow.com/questions/15001342/jboss-7-war-deployment-failed

Go to `Jboss_installation_dir\standalone\configuration` and find the file `standalone.xml`. Change the following line:

    <subsystem xmlns="urn:jboss:domain:deployment-scanner:1.0">
        <deployment-scanner scan-interval="5000" relative-to="jboss.server.base.dir" path="deployments"  />
    </subsystem>

into:

    <subsystem xmlns="urn:jboss:domain:deployment-scanner:1.0">
        <deployment-scanner scan-interval="5000" relative-to="jboss.server.base.dir" path="deployments" deployment-timeout="1000" />
    </subsystem>