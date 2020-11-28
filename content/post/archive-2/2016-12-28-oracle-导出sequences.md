---
title: oracle 导出sequences
author: w1100n
type: post
date: 2016-12-28T04:58:01+00:00
url: /?p=7432
categories:
  - Uncategorized

---
如下脚本，可以将某个用户的全部sequence查询出来，并拼成创建语句。

<wbr />select 'create sequence '||sequence_name|| <wbr /> <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ' minvalue '||min_value|| <wbr /> <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ' maxvalue '||max_value|| <wbr /> <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ' start with '||last_number|| <wbr /> <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ' increment by '||increment_by|| <wbr /> <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> (case when cache\_size=0 then ' nocache' else ' cache '||cache\_size end) ||';' <wbr /> <wbr />
  
from dba\_sequences where sequence\_owner='HR' <wbr /> <wbr />
  
注意：其中的HR，是需要导出sequence的用户，貌似必须大写的说！并且使用该脚本的用户需要有访问dba_sequences的权限。

导出结果如下：

<wbr />create sequence HIBERNATE_SEQUENCE minvalue 1 maxvalue 999999999999999999999999<wbr />999 start with 1 increment by 1 cache 20; <wbr />

create sequence MIAGENTVERSION\_VERSION\_SEQ minvalue 1 maxvalue 999999999999999999999999<wbr />start with 121 increment by 1 cache 20;

---------------------------

如果你只想导出本用户的sequence那就不要那么复杂的写，只写如下语句就可以了：

select 'create sequence '||sequence_name|| <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ' minvalue '||min_value|| <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ' maxvalue '||max_value|| <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ' start with '||last_number|| <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ' increment by '||increment_by|| <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> (case when cache\_size=0 then ' nocache' else ' cache '||cache\_size end) ||';' <wbr />
  
from user_sequences