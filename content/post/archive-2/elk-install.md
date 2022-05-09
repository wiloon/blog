---
title: elk install
author: "-"
date: 2018-07-12T09:51:48+00:00
url: /?p=12423
categories:
  - Inbox
tags:
  - reprint
---
## elk install
download elasticsearch
  
https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.1.rpm
  
install jdk8
  
yum localinstall elasticsearch-6.3.1.rpm

# start elasticsearch, it will generate default config file

systemctl start elasticsearch

edit config file /etc/elasticsearch/elasticsearch.yml
  
path.data: /data/server/elasticsearch
  
path.logs: /data/server/elasticsearch
  
network.host: 0.0.0.0

mkdir -p /data/server/elasticsearch/
  
chown -R elasticsearch:elasticsearch elasticsearch/
  
systemctl restart elasticsearch

install ingest geoip plugin
  
download from https://artifacts.elastic.co/downloads/elasticsearch-plugins/ingest-geoip/ingest-geoip-6.3.1.zip

download kibana
  
yum localinstall kibana

edit kibana config file, vi /etc/kibana/kibana.conf
  
server.host: "xxx"
  
elasticsearch.url: "http://elasticsearch-ip:9200"
  
systemctl restart kibana

check if kibana works http://kibana-ip:5601

download and install filebeat