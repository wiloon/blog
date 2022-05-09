---
title: java import cert
author: "-"
date: 2018-08-03T02:55:02+00:00
url: /?p=12484
categories:
  - Inbox
tags:
  - reprint
---
## java import cert
```bash
keytool -importcert -keystore /path/to/jre/lib/security/cacerts -storepass changeit -noprompt -file /path/to/ca.der -alias "digicertglobalrootca"
# storepass 默认值changeit
keytool -list -keystore $JAVA_HOME/jre/lib/security/cacerts -storepass changeit | grep digicertglobalrootca

```