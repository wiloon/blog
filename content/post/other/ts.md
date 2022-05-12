---
title: ts
author: "-"
date: 2012-03-27T14:03:01+00:00
url: /?p=2666
categories:
  - Linux
tags:
  - reprint
---
## ts
author: Hex Lee lihe757@gmail.com
  
1.添加此脚本到~/.bashrc的末尾
  
2.source ~/.bashrc
  
ts hello
  
你好

```bash
  
#youdao
  
ts(){

curl -s
          
"http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=dict.top"
      
-d
      
"type=AUTO& i=$1&doctype=json&xmlVersion=1.4&keyfrom=fanyi.web&ue=UTF-8&typoResult=true&flag=false"
          
| sed -E -n 's/.\*tgt":"([^"]+)".\*entries":["","([^"]+)".*/1n 2/p';

return 0;
  
}
  
#sed -E -n 's/.\*tgt":"([^"]+)".*/1/p' ;
  
#sed -E -n 's/.\*tgt":"([^"]+)".\*entries":["","([^"]+)".*/1n 2/p';
  
```