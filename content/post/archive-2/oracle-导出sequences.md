---
title: oracle 导出sequences
author: "-"
date: 2016-12-28T04:58:01+00:00
url: /?p=7432
categories:
  - Uncategorized

tags:
  - reprint
---
## oracle 导出sequences
如下脚本,可以将某个用户的全部sequence查询出来,并拼成创建语句。

select 'create sequence '||sequence_name||   
  
      ' minvalue '||min_value||   
  
      ' maxvalue '||max_value||   
  
      ' start with '||last_number||   
  
      ' increment by '||increment_by||   
  
      (case when cache_size=0 then ' nocache' else ' cache '||cache_size end) ||';'  
  
from dba_sequences where sequence_owner='HR'  
  
注意: 其中的HR,是需要导出sequence的用户,貌似必须大写的说！并且使用该脚本的用户需要有访问dba_sequences的权限。

导出结果如下: 

create sequence HIBERNATE_SEQUENCE minvalue 1 maxvalue 999999999999999999999999999 start with 1 increment by 1 cache 20; 

create sequence MIAGENTVERSION_VERSION_SEQ minvalue 1 maxvalue 999999999999999999999999start with 121 increment by 1 cache 20;

---------------------------

如果你只想导出本用户的sequence那就不要那么复杂的写,只写如下语句就可以了: 

select 'create sequence '||sequence_name||  
  
      ' minvalue '||min_value||  
  
      ' maxvalue '||max_value||  
  
      ' start with '||last_number||  
  
      ' increment by '||increment_by||  
  
      (case when cache_size=0 then ' nocache' else ' cache '||cache_size end) ||';' 
  
from user_sequences