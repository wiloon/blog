---
title: Pentaho Data Integration(PDI)
author: "-"
date: 2015-01-08T09:34:04+00:00
url: /?p=7214
categories:
  - Uncategorized

tags:
  - reprint
---
## Pentaho Data Integration(PDI)

<http://www.cnblogs.com/wukenaihe/p/3209618.html>

Spoon是构建ETL Jobs和Transformations的工具。Spoon可以以拖拽的方式图形化设计,能够通过spoon调用专用的数据集成引擎或者集群。

Data Integration Server是一个专用的ETL Server,它的主要功能有:

        功能
      
    
    
    
      
        描述
      
    
  
  
  
    
      
        执行
      
    
    
    
      
        通过Pentaho Data Integration引擎执行ETL的作业或转换
      
    
  
  
  
    
      
        安全性
      
    
    
    
      
        管理用户、角色或集成的安全性
      
    
  
  
  
    
      
        内容管理
      
    
    
    
      
        提供一个集中的资源库,用来管理ETL的作业和转换。资源库包含所有内容和特征的历史版本。
      
    
  
  
  
    
      
        时序安排
      
    
    
    
      
        在spoon设计者环境中提供管理Data Integration Server上的活动的时序和监控的服务

Enterprise Console提供了一个小型的客户端,用于管理Pentaho Data Integration企业版的部署,包括企业版本的证书管理、监控和控制远程Pentaho Data Integration服务器上的活动、分析已登记的作业和转换的动态绩效。

## 2. PDI的组成部分

        名称
      
    
    
    
      
        描述
      
    
  
  
  
    
      
        Spoon
      
    
    
    
      
        通过图形接口,用于编辑作业和转换的桌面应用。
      
    
  
  
  
    
      
        Pan
      
    
    
    
      
        一个独立的命令行程序,用于执行由Spoon编辑的转换和作业。
      
    
  
  
  
    
      
        Kitchen
      
    
    
    
      
        一个独立的命令行程序,用于执行由Spoon编辑的作业。
      
    
  
  
  
    
      
        Carte
      
    
    
    
      
        Carte是一个轻量级的Web容器,用于建立专用、远程的ETL Server。
