---
title: oracle create user
author: wiloon
type: post
date: 2011-11-02T07:05:15+00:00
url: /?p=1433
bot_views:
  - 6
views:
  - 4
categories:
  - DataBase

---
connect to oracle with sqlplus

http://www.wiloon.com/wordpress/?p=5560

```bash

create user user0 identified by password0;

grant connect, resource to user0;

drop user user0 cascade;

```

oracle create user, pl sql developer

#general

##name xxx

##password xxx

##default tablespace users

##temporary tablespace temp

##profile default

#role privileges

connect, dba, resource

#system privileges

unlimited tablespace


http://www.2cto.com/database/201109/103010.html