---
title: nginx location, root
author: "-"
type: post
date: 2019-04-29T02:13:46+00:00
url: /?p=14262
categories:
  - Uncategorized

---
https://blog.csdn.net/u011510825/article/details/50531864

最近公司开发新项目，web server使用nginx，趁周末小小的研究了一下，一不小心踩了个坑吧，一直404 not found!!!!!当时卡在location和root中，但是网上却比较少聊这方面的关系，一般都是聊location匹配命令（这里可以看看http://www.nginx.cn/115.html) ，花了一下午，彻底搞清楚了location和root到底怎样找到文件的。

nginx指定文件路径有两种方式root和alias，这两者的用法区别，使用方法总结了下，方便大家在应用过程中，快速响应。root与alias主要区别在于nginx如何解释location后面的uri，这会使两者分别以不同的方式将请求映射到服务器文件上。

### root
语法: root path  
默认值: root html
  
配置段: http、server、location、if

[alias]
  
语法: alias path
  
配置段: location

root实例: 

location ^~ /t/ {
       
root /www/root/html/;
  
}
  
如果一个请求的URI是/t/a.html时，web服务器将会返回服务器上的/www/root/html/t/a.html的文件。
  
alias实例: 

location ^~ /t/ {
   
alias /www/root/html/new_t/;
  
}
  
如果一个请求的URI是/t/a.html时，web服务器将会返回服务器上的/www/root/html/new_t/a.html的文件。注意这里是new_t，因为alias会把location后面配置的路径丢弃掉，把当前匹配到的目录指向到指定的目录。
  
注意: 

  1. 使用alias时，目录名后面一定要加"/"。
  2. alias在使用正则匹配时，必须捕捉要匹配的内容并在指定的内容处使用。

## 4. alias只能位于location块中。（root可以不放在location中) 

作者: 果汁华
  
来源: CSDN
  
原文: https://blog.csdn.net/u011510825/article/details/50531864
  
版权声明: 本文为博主原创文章，转载请附上博文链接！