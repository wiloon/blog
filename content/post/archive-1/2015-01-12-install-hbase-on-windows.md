---
title: hbase install
author: wiloon
type: post
date: 2015-01-12T07:21:37+00:00
url: /?p=7223
categories:
  - Uncategorized
tags:
  - Hbase

---
```bash
  
tar xzvf hbase-2.0.0-SNAPSHOT-bin.tar.gz
  
cd hbase-2.0.0-SNAPSHOT/

#edit hbase-env.sh
  
#export JAVA\_HOME=/home/xxx/apps/jdk1.8.0\_111/
  
#export HBASE\_MANAGES\_ZK=false

#edit hbase-site.xml
  
```

[xml]
  
<configuration>
    
<property>
      
<name>hbase.rootdir</name>
      
<value>file:///data/hbase</value>
    
</property>
    
<property>
      
<name>hbase.zookeeper.property.dataDir</name>
      
<value>/tmp/zookeeper</value>
    
</property>
    
<property>
    
<name>hbase.cluster.distributed</name>
    
<value>true</value>
  
</property>
  
</configuration>
  
[/xml]

```bash
  
#start hbase
  
start-hbase.sh

#cli
  
./hbase hsell

create 'test', 'cf'
  
list 'test'
  
put 'test', 'row1', 'cf:a', 'value1'
  
scan 'test'
  
get 'test', 'row1'
  
disable 'test'
  
enable 'test'
  
drop 'test'
  
```