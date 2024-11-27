---
title: kibana 查询
author: "-"
date: 2018-06-22T01:28:24+00:00
url: /?p=12348
categories:
  - Inbox
tags:
  - reprint
---
## kibana 查询
### 匹配查询
    message: "15909840000"
### 模糊查询
    message:1590984*

Range Searches
  
mod_date:[20020101 TO 20030101]

逻辑操作 AND OR 必须大写
  
AND OR
  
+ 表示搜索结果中必须包含此项
  
- 表示不能含有此项

source:S0 AND message:M0



https://lucene.apache.org/core/2_9_4/queryparsersyntax.html
  
https://www.jianshu.com/p/e6143951be9b