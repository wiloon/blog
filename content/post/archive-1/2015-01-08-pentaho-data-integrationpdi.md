---
title: Pentaho Data Integration(PDI)
author: wiloon
type: post
date: 2015-01-08T09:34:04+00:00
url: /?p=7214
categories:
  - Uncategorized

---
http://www.cnblogs.com/wukenaihe/p/3209618.html

Spoon是构建ETL Jobs和Transformations的工具。Spoon可以以拖拽的方式图形化设计，能够通过spoon调用专用的数据集成引擎或者集群。

Data Integration Server是一个专用的ETL Server，它的主要功能有：

<table class="-11" border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td valign="top" width="92">
      <p class="a0">
        <strong>功能</strong>
      </p>
    </td>
    
    <td valign="top" width="476">
      <p class="a0">
        <strong>描述</strong>
      </p>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="92">
      <p class="a0">
        <strong>执行</strong>
      </p>
    </td>
    
    <td valign="top" width="476">
      <p class="a0">
        通过Pentaho Data Integration引擎执行ETL的作业或转换
      </p>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="92">
      <p class="a0">
        <strong>安全性</strong>
      </p>
    </td>
    
    <td valign="top" width="476">
      <p class="a0">
        管理用户、角色或集成的安全性
      </p>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="92">
      <p class="a0">
        <strong>内容管理</strong>
      </p>
    </td>
    
    <td valign="top" width="476">
      <p class="a0">
        提供一个集中的资源库，用来管理ETL的作业和转换。资源库包含所有内容和特征的历史版本。
      </p>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="92">
      <p class="a0">
        <strong>时序安排</strong>
      </p>
    </td>
    
    <td valign="top" width="476">
      <p class="a0">
        在spoon设计者环境中提供管理Data Integration Server上的活动的时序和监控的服务
      </p>
    </td>
  </tr>
</table>

Enterprise Console提供了一个小型的客户端，用于管理Pentaho Data Integration企业版的部署，包括企业版本的证书管理、监控和控制远程Pentaho Data Integration服务器上的活动、分析已登记的作业和转换的动态绩效。

## 2. PDI的组成部分

<table class="-11" border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td valign="top" width="92">
      <p class="a0">
        <strong>名称</strong>
      </p>
    </td>
    
    <td valign="top" width="476">
      <p class="a0">
        <strong>描述</strong>
      </p>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="92">
      <p class="a0">
        <strong>Spoon</strong>
      </p>
    </td>
    
    <td valign="top" width="476">
      <p class="a0">
        通过图形接口，用于编辑作业和转换的桌面应用。
      </p>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="92">
      <p class="a0">
        <strong>Pan</strong>
      </p>
    </td>
    
    <td valign="top" width="476">
      <p class="a0">
        一个独立的命令行程序，用于执行由Spoon编辑的转换和作业。
      </p>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="92">
      <p class="a0">
        <strong>Kitchen</strong>
      </p>
    </td>
    
    <td valign="top" width="476">
      <p class="a0">
        一个独立的命令行程序，用于执行由Spoon编辑的作业。
      </p>
    </td>
  </tr>
  
  <tr>
    <td valign="top" width="92">
      <p class="a0">
        <strong>Carte</strong>
      </p>
    </td>
    
    <td valign="top" width="476">
      <p class="a0">
        Carte是一个轻量级的Web容器，用于建立专用、远程的ETL Server。
      </p>
    </td>
  </tr>
</table>

