---
title: filebeat
author: "-"
date: 2018-01-19T06:45:49+00:00
url: /?p=11760
categories:
  - Uncategorized

tags:
  - reprint
---
## filebeat

### elasticsearch output 配置索引

vim /etc/filebeat/filebeat.yml

```bash
setup.template.name: "filebeat-"
setup.template.pattern: "filebeat-*"
output.elasticsearch:
  hosts: ["http://192.168.6.8:9200"]
  index: "filebeat-%{+yyyy.MM.dd}"
```

```bash
sudo rpm --import https://packages.elastic.co/GPG-KEY-elasticsearch

```

Create a file with a .repo extension (for example, elastic.repo) in your /etc/yum.repos.d/ directory and add the following lines:

[elastic-6.x]
  
name=Elastic repository for 6.x packages
  
baseurl=<https://artifacts.elastic.co/packages/6.x/yum>
  
gpgcheck=1
  
gpgkey=<https://artifacts.elastic.co/GPG-KEY-elasticsearch>
  
enabled=1
  
autorefresh=1
  
type=rpm-md
  
Your repository is ready to use. For example, you can install Filebeat by running:

sudo yum install filebeat
  
To configure the Beat to start automatically during boot, run:

sudo chkconfig -add filebeat
