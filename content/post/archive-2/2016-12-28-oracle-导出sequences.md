---
title: oracle 导出sequences
author: wiloon
type: post
date: 2016-12-28T04:58:01+00:00
url: /?p=7432
categories:
  - Uncategorized

---
如下脚本，可以将某个用户的全部sequence查询出来，并拼成创建语句。

<wbr />select &#8216;create sequence &#8216;||sequence_name|| <wbr /> <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216; minvalue &#8216;||min_value|| <wbr /> <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216; maxvalue &#8216;||max_value|| <wbr /> <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216; start with &#8216;||last_number|| <wbr /> <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216; increment by &#8216;||increment_by|| <wbr /> <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> (case when cache\_size=0 then &#8216; nocache&#8217; else &#8216; cache &#8216;||cache\_size end) ||&#8217;;&#8217; <wbr /> <wbr />
  
from dba\_sequences where sequence\_owner=&#8217;HR&#8217; <wbr /> <wbr />
  
注意：其中的HR，是需要导出sequence的用户，貌似必须大写的说！并且使用该脚本的用户需要有访问dba_sequences的权限。

导出结果如下：

<wbr />create sequence HIBERNATE_SEQUENCE minvalue 1 maxvalue 999999999999999999999999<wbr />999 start with 1 increment by 1 cache 20; <wbr />

create sequence MIAGENTVERSION\_VERSION\_SEQ minvalue 1 maxvalue 999999999999999999999999<wbr />start with 121 increment by 1 cache 20;

&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8211;

如果你只想导出本用户的sequence那就不要那么复杂的写，只写如下语句就可以了：

select &#8216;create sequence &#8216;||sequence_name|| <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216; minvalue &#8216;||min_value|| <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216; maxvalue &#8216;||max_value|| <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216; start with &#8216;||last_number|| <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216; increment by &#8216;||increment_by|| <wbr /> <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> (case when cache\_size=0 then &#8216; nocache&#8217; else &#8216; cache &#8216;||cache\_size end) ||&#8217;;&#8217; <wbr />
  
from user_sequences