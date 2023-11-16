---
title: database DDL > puml
author: "-"
date: 2019-04-29T08:14:42+00:00
url: /?p=14270
categories:
  - Inbox
tags:
  - reprint
---
## database DDL > puml

[https://github.com/wangyuheng/ddl2plantuml](https://github.com/wangyuheng/ddl2plantuml)

```bash
java -jar ~/apps/ddl2plantuml.jar foo.sql er.puml
```

```bash
docker run \
-e DDL='/mnt/data/ddl.sql' \
-e PLANTUML='/mnt/data/er_by_docker.puml' \
-v ddl2plantuml-data:'/mnt/data' \
wangyuheng/ddl2plantuml:latest
```
