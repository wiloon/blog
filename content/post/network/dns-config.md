---
author: "-"
date: "2020-06-26T13:10:40Z"
title: "dns config"

categories:
  - inbox
tags:
  - reprint
---
## "dns config"
主机记录

www :   
 将域名解析为[www.example.com](https://link.jianshu.com?t=http://www.example.com),填写www；

@ :   
 将域名解析为[example.com](https://link.jianshu.com?t=http://example.com) (不带www) ,填写@或者不填写；

mail :   
 将域名解析为mail.example.com,通常用于解析邮箱服务器；

\*:   
 泛解析,所有子域名均被解析到统一地址 (除单独设置的子域名解析) ；

#### 解析线路

为加速访问域名,可设置与用户相同的网络类型,但用户的网络类型多种多样,所以解析线路设置为默认,这样DNS服务商一般会智能使用解析线路,当判断访问者来源为联通用户,就将域名解析到联通的服务器IP上；当判断访问者来源为电信用户,就将域名解析到到电信的服务器IP上。
  
作者: 大猫黄  
链接: [https://www.jianshu.com/p/d1840c71a57c](https://www.jianshu.com/p/d1840c71a57c "https://www.jianshu.com/p/d1840c71a57c")  
来源: 简书  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。
