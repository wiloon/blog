---
title: oracle commands
author: "-"
type: post
date: 2015-01-14T01:19:57+00:00
url: /?p=7235
categories:
  - Uncategorized

---
## oracle commands
[sql]

to_number('2')

- create sequence

create sequence sequence_name
  
minvalue 1
  
maxvalue 9999999999999999999999999999
  
start with 1
  
increment by 1
  
cache 20;

- create trigger

CREATE OR REPLACE TRIGGER "trigger_name" BEFORE
  
insert ON table_name FOR EACH ROW
  
begin
  
select sequence_name.nextval into:New.column_name from dual;
  
end;

[/sql]