---
title: OLAP, OLTP
author: "-"
date: 2013-02-17T05:54:30+00:00
url: /?p=5164
categories:
  - CI
tags:
  - Jenkins

---
## OLAP, OLTP
[http://www.cnblogs.com/beyondstorm/archive/2006/08/12/475011.html](http://www.cnblogs.com/beyondstorm/archive/2006/08/12/475011.html)

OLAP和OLTP的区别(基础知识)

联机分析处理 (OLAP) 的概念最早是由关系数据库之父E.F.Codd于1993年提出的，他同时提出了关于OLAP的12条准则。OLAP的提出引起了很大的反响，OLAP作为一类产品同联机事务处理 (OLTP) 明显区分开来。
  
当今的数据处理大致可以分成两大类: 联机事务处理OLTP (on-line transaction processing) 、联机分析处理OLAP (On-Line Analytical Processing) 。OLTP是传统的关系型数据库的主要应用，主要是基本的、日常的事务处理，例如银行交易。OLAP是数据仓库系统的主要应用，支持复杂的分析操作，侧重决策支持，并且提供直观易懂的查询结果。下表列出了OLTP与OLAP之间的比较。

OLTP OLAP
  
用户 操作人员,低层管理人员 决策人员,高级管理人员
  
功能 日常操作处理 分析决策
  
DB 设计 面向应用 面向主题
  
数据 当前的, 最新的细节的, 二维的分立的 历史的, 聚集的, 多维的集成的, 统一的
  
存取 读/写数十条记录 读上百万条记录
  
工作单位 简单的事务 复杂的查询
  
用户数 上千个 上百个
  
DB 大小 100MB-GB 100GB-TB
