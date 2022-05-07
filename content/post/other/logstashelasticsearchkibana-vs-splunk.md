---
title: logstash+ElasticSearch+Kibana VS Splunk
author: "-"
date: 2015-09-10T07:56:51+00:00
url: /?p=8238
categories:
  - Inbox
tags:
  - reprint
---
## logstash+ElasticSearch+Kibana VS Splunk

<http://blog.csdn.net/firefoxbug/article/details/8018377>

最近帮磊哥移植一套开源的日志管理软件，替代Splunk． Splunk是一个功能强大的日志管理工具，它不仅可以用多种方式来添加日志，生产图形化报表，最厉害的是它的搜索功能 - 被称为"Google for IT"。Splunk有免费和收费版，最主要的差别在于每天的索引容量大小 (索引是搜索功能的基础) ，免费版每天最大为500M。在使用免费版时，如果在30天之内，有7天的索引数据量超过500M，那么就不可以再搜索了．
  
我熟悉了几天logstash，然后用ElasticSearch进行搜索，最后用Kibana来作为漂亮的三方界面，总体上不错！果然是开源的力量．整个搭建的过程比较复杂，东西比较多，有java，有ruby，有python一些列的．先介绍下三个开源项目

Logstash
  
is very useful and versatile. It's made of JRuby (Java+Ruby). You can specify inputs and outputs as well as filters. It supports various input types. One of them is "Linux Syslog". Which means, you do not have to install logging agent on every server increasing the overall load of the server. Your default rsyslog client will do just fine. Then comes the filtering part, after taking input, you can filter out logs within Logstash itself. It's awesome but it didn't serve any purpose for me as I wanted to index every log. Next is the output part, Logstash can output logs on standard output (why would anyone want that). But as with input, it supports multiple output types too. One of them is Elasticsearch.

Elasticsearch
  
is a Java based log indexer. You can search through Elasticsearch indices using Lucene search syntax for more complicated query. But, simple wildcard search works too.

Kibana
  
It provides the web frontend for Elasticsearch, written on Java Script and PHP, requires only one line to be edited for this to work out off the box.
  
下面是logstash跑出来的效果，具体的搭建还是以后有时间介绍了．Kibana查看端口默认是5601
