---
title: oracle commands
author: wiloon
type: post
date: 2015-01-14T01:19:57+00:00
url: /?p=7235
categories:
  - Uncategorized

---
[sql]

to_number(&#8216;2&#8217;)

&#8212; create sequence

create sequence sequence_name
  
minvalue 1
  
maxvalue 9999999999999999999999999999
  
start with 1
  
increment by 1
  
cache 20;

&#8212; create trigger

CREATE OR REPLACE TRIGGER "trigger_name" BEFORE
  
insert ON table_name FOR EACH ROW
  
begin
  
select sequence\_name.nextval into:New.column\_name from dual;
  
end;

[/sql]