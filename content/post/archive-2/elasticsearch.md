---
title: elasticsearch
author: "-"
date: 2018-06-12T05:36:22+00:00
url: /?p=12299
categories:
  - Uncategorized

tags:
  - reprint
---
## elasticsearch

```bash
#查看索引
GET /_cat/indices?pretty
curl -X GET "localhost:9200/_cat/indices?v"

GET /index-2018.09.29/_stats
GET /_cat/indices?pretty

# elasticsearch 重启后用以下命令观察集群状态。
watch -n 1 -d curl -XGET http://localhost:9200/_cluster/health\?pretty

curl -X GET "localhost:9200/_cluster/allocation/explain?pretty" -H 'Content-Type: application/json' -d'
{
  "index": "myindex",
  "shard": 0,
  "primary": true
}
'

```

unassigned_shards: 没有被分配到节点的分片
  
unassigned_shards 在elasticsearch 重启后会逐渐减少,如果最终unassigned_shards不为0,则需要手动处理。

```bash
# 找出未分配到结点的分片
curl -s "http://localhost:9200/_cat/shards" | grep UNASSIGNED

curl 'localhost:9200/_cat/master?v'

ES_JAVA_OPTS="-Xms2g -Xmx2g" /usr/share/elasticsearch/bin/elasticsearch -d -Ecluster.name=my-application -Enode.name=node-1 -Enode.master=true -Enode.data=false -Epath.data=/data/server/elasticsearch-node1 -Epath.logs=/data/logs/elasticsearch-node1 -Enetwork.host=0.0.0.0 -Ehttp.port=9200 -p /home/elasticsearch/node1_pid

kill `cat /home/elasticsearch/node1_pid`

curl -XGET http://localhost:9200/_cluster/health\?pretty
curl -XGET http://localhost:9200/_cat/shards
curl -s "http://localhost:9200/_cat/shards/index-0"

curl 'localhost:9200/_nodes/process?pretty'

#check if index exist
curl --head "localhost:9200/twitter"

curl -X GET "localhost:9200/_cat/health?v"
curl -X GET "localhost:9200/_cat/nodes?v"

curl -X PUT "localhost:9200/customer?pretty"
curl -X PUT "localhost:9200/customer/_doc/1?pretty" -H 'Content-Type: application/json' -d'
{
  "name": "John Doe"
}
'

curl -X GET "localhost:9200/customer/_doc/1?pretty"

# delete index
curl -X DELETE "localhost:9200/index-0?pretty"
curl -X DELETE "localhost:9200/customer/_doc/2?pretty"
curl -H "Content-Type: application/json" -XPOST "localhost:9200/bank/_doc/_bulk?pretty&refresh" --data-binary "@accounts.json"
curl "localhost:9200/_cat/indices?v"

```
