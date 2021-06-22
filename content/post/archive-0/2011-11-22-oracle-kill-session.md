---
title: oracle kill session
author: "-"
type: post
date: 2011-11-22T09:43:42+00:00
url: /?p=1574
bot_views:
  - 4
views:
  - 4
categories:
  - DataBase

---
BEGIN
  FOR ss in (select sid,serial# from v$session s where s.USERNAME='USERNAME')
  loop
    execute immediate 'ALTER system kill session '''||ss.sid||','||ss.serial#||'''';
  end loop;
end;