---
title: nginx tomcat
author: wiloon
type: post
date: 2017-11-10T02:31:10+00:00
url: /?p=11395
categories:
  - Uncategorized

---
https://www.cnblogs.com/naaoveGIS/p/5478208.html

upstream tomcat_server{
           
server localhost:8080;
  
}

server{
          
listen 80;
          
server_name enx.wiloon.com;

        location / {
                 proxy_pass http://tomcat_server;
        }
    

}