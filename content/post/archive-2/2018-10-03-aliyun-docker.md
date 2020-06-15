---
title: aliyun docker
author: wiloon
type: post
date: 2018-10-03T08:56:36+00:00
url: /?p=12733
categories:
  - Uncategorized

---
https://cr.console.aliyun.com/cn-qingdao/mirrors

  1. 安装／升级Docker客户端
  
    推荐安装1.10.0以上版本的Docker客户端，参考文档 docker-ce 
  2. 配置镜像加速器
  
    针对Docker客户端版本大于 1.10.0 的用户

您可以通过修改daemon配置文件/etc/docker/daemon.json来使用加速器
  
sudo mkdir -p /etc/docker
  
sudo tee /etc/docker/daemon.json <<-&#8216;EOF&#8217;
  
{
    
"registry-mirrors&#8221;: ["https://xxxxxx.mirror.aliyuncs.com&#8221;]
  
}
  
EOF
  
sudo systemctl daemon-reload
  
sudo systemctl restart docker