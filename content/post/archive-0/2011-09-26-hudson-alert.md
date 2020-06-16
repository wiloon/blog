---
title: hudson i18n alert
author: wiloon
type: post
date: 2011-09-26T15:22:26+00:00
url: /?p=933
bot_views:
  - 9
categories:
  - CI
tags:
  - Tomcat

---
Your container doesn&#8217;t use UTF-8 to decode URLs. If you use non-ASCII characters as a job name etc, this will cause problems. See Containers and Tomcat i18n for more details.

Some versions of Tomcat (such as 5.0.28) uses iso-8859-1 to decode URLs, which is in a clear violation of the relevant RFCs. To fix this problem, add the following URIEncoding attribute to the connector definition in $TOMCAT_HOME/conf/server.xml.

&lt;Connector port="8080"  URIEncoding="UTF-8"/&gt;