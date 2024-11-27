---
title: ELK Stack
author: "-"
date: 2018-01-10T08:03:10+00:00
url: /?p=11698
categories:
  - Inbox
tags:
  - reprint
---
## ELK Stack

## ELK

ELK 是 Elasticsearch、Logstash 和 Kibana 三种软件产品的首字母缩写, 这三者都是开源软件,通常配合使用,而且又先后归于 Elastic.co 公司名下,所以被简称为 ELK Stack
  
ELK Stack 已经成为目前最流行的集中式日志解决方案。

Elasticsearch: 分布式搜索和分析引擎,具有高可伸缩、高可靠和易管理等特点。基于 Apache Lucene 构建,能对大容量的数据进行接近实时的存储、搜索和分析操作。通常被用作某些应用的基础搜索引擎,使其具有复杂的搜索功能；
  
Logstash: 数据收集引擎。它支持动态的从各种数据源搜集数据,并对数据进行过滤、分析、丰富、统一格式等操作,然后存储到用户指定的位置；
  
Kibana: 数据分析和可视化平台。通常与 Elasticsearch 配合使用,对其中数据进行搜索、分析和以统计图表的方式展示；
  
Filebeat: ELK 协议栈的新成员,一个轻量级开源日志文件数据搜集器,基于 Logstash-Forwarder 源代码开发,是对它的替代。在需要采集日志数据的 server 上安装 Filebeat,并指定日志目录或日志文件后,Filebeat 就能读取数据,迅速发送到 Logstash 进行解析,亦或直接发送到 Elasticsearch 进行集中式存储和分析。

Grok 是 Logstash 最重要的插件。你可以在 grok 里预定义好命名正则表达式,在稍后(grok参数或者其他正则表达式里)引用它。

[https://www.ibm.com/developerworks/cn/opensource/os-cn-elk-filebeat/index.html](https://www.ibm.com/developerworks/cn/opensource/os-cn-elk-filebeat/index.html)
  
[https://doc.yonyoucloud.com/doc/logstash-best-practice-cn/index.html](https://doc.yonyoucloud.com/doc/logstash-best-practice-cn/index.html)
  
[http://soft.dog/2015/12/24/beats-basic/#section](http://soft.dog/2015/12/24/beats-basic/#section)
