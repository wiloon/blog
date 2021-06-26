---
title: jboss port
author: "-"
type: post
date: 2011-09-30T02:52:07+00:00
url: /?p=975
bot_views:
  - 9
categories:
  - Uncategorized
tags:
  - Jboss

---
jboss-4.0.5.GA

boss通常占用的端口是1098，1099，4444，4445，8080，8009，8083，8093这几个，

默认端口是8080

1098、1099、4444、4445、8083端口在/jboss/server/default/conf/jboss-service.xml

8080, 8009, 8443端口在jboss-4.0.5.GA/server/default/deploy/jbossweb-tomcat55.sar/server.xml

8093端口在/jboss/server/default/deploy/jms/uil2-service.xml中。