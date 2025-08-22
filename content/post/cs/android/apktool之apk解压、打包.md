---
title: QNAP
author: "-"
date: 2014-12-30T06:52:58+00:00
url: qnap
categories:
  - CS
tags:
  - reprint
  - remix
---

## QNAP

### qnap, plex server, apple tv, av1

https://www.reddit.com/r/PleX/comments/12pe5tx/comment/jgrrjnc/
https://github.com/currifi/plex_av1_tvos?tab=readme-ov-file

https://support.plex.tv/articles/202915258-where-is-the-plex-media-server-data-directory-located/

https://www.qnap.com/en/how-to/faq/article/how-do-i-access-my-qnap-nas-using-ssh

QNAP 启用 ssh 服务
```Bash
ssh admin@192.168.50.227
# print The exact data directory location
getcfg -f /etc/config/qpkg.conf PlexMediaServer Install_path
mkdir /share/CACHEDEV1_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/Profiles

# copy file https://github.com/scriptsingh/plex_av1_tvos/blob/main/tvOS.xml to Profiles dir

```

重启 plex server
威联通 nas web ui> app center> plex server 
stop 
start

