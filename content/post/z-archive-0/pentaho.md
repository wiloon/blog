---
title: Pentaho
author: "-"
date: 2012-02-03T04:22:57+00:00
url: /?p=2246
categories:
  - Uncategorized
tags:
  - Pentaho

---
## Pentaho
home page: http://www.pentaho.com/

community: http://community.pentaho.com/

License: GPLv2:http://community.pentaho.com/faq/platform_licensing.php

download:http://sourceforge.net/projects/pentaho/files/

Business Analytics Platform: biserver-ce-xxx.zip

Data Integration (Kettle):pdi-ce-xxx.zip

Report Designer: prd-ce-xxx.zip

Marketplace: marketplace-xxx.zip

Metadata Editor: pme-ce-xxx.zip

Schema Workbench: psw-ce-xxx.zip

Aggregation Designer: pad-ce-xxx.zip

pentaho是世界上最流行的开源商务智能软件，以工作流为核心的、强调面向解决方案而非工具组件的BI套件，整合了多个开源项目，目标是和商业BI相抗衡。它是一个基于java平台的商业智能(Business Intelligence,BI)套件，之所以说是套件是因为它包括一个web server平台和几个工具软件: 报表，分析，图表，数据集成，数据挖掘等，可以说包括了商务智能的方方面面。

Pentaho是一个它偏向于与业务流程相结合的BI解决方案，侧重于大 中型企业应用。它允许商业分析人员或开发人员创建报表，仪表盘，分析模型，商业规则和 BI 流程。

## 功能和特点 {.headline-1}


  ◆ 集成管理和开发环境: Eclipse


  ◆ ETL工具: Enhydra/Kettle


  ◆ OLAP Server: Mondrian


  ◆ OLAP展示: JPivot


  ◆ 数据挖掘组件: Weka


  ◆ 应用服务器和Portal服务器: JBoss


  ◆ 单点登陆服务及LDap认证: JOSSO


  ◆ 自定义脚本支持: Mozilla Rhino Javascript脚本处理器。[1]



## 授权

分为两个版本: 商业版和社区版。

### 社区版

社区版为开源，授权协议为: GPL,LGPL。

社区版代码以从官方网站分离，由sourceforge(<http://sourceforge.net/projects/pentaho/>)代为管理。

代码及开发工具见扩展1。

### 商业版

商业版需要付费，有试用demo可下载。

官方网站[http://www.pentaho.com][1]

## 核心思想和特色

较其它BI框架而言，pentaho也提出了自己平台的特色，是面向解决方案的思想。

由技术白皮书中节选的一段案例分析，可以了解到，什么是pentaho的"面向解决方案"。

**业务问题: **当一个许可证有效期已满的雇员在一家医疗机构工作时，需要: 

注意到这个问题，一个代理工人必须替换这个雇员，直到他们的许可证被更新过。注意到何种情况下，一个病人的安全是有风险的和发生风险的可能性。

**业务目标**: 提高病人的安全，减少没有许可证的雇员的责任，减少替换没有许可证的雇员时，雇用的代理职员上的花销。

**当前业务流程**: 每个经理维护她所在部门的许可证有效期的一个列表。

**建议解决方案**: 从一个集中式的数据库，预约生成报表，它根据部门，列出了每个雇员持有的许可证，以及他们当前许可证的有效期。

## 方案1: 给他们要求的东西

创建一个50 页的报表并每月发送给每个部门。

Resulting Business 业务流程: 

报表的运行没有被审计。如果报表没有被如期的产生，那人们需要多久才能发现这种情况呢？每个部门的经理需要读取报表和过滤信息。但是，有可能报表丢失，管理员休假，或者日期搞错了。当管理员发现license 即将过期时，他们会使用邮件给同事们发一个通知。但通知可能会丢失或弄错邮箱。雇员尽力规划预备工作，申请和认证时间。但如果时间表发生冲突, 将导致预备工作受损。雇员在license 过期前，因为没有时间做更多的预备工作或者认证而失败.

这个solution 是不完整的，因为它仅仅自动化了信息传递，它对于必须要发生的真实业务流程并没有任何辅助作用。业务目标被使用报表产品的方式来达到。

## 方案2: 给他们真正需要的东西

创建业务规则来判定为了对每种类型的license做足预备工作而需要的交付周期，并增加对问题域的解决路径。每天或每周运行一个列出雇员在他们交付周期内的审计报表。对于每个雇员，初始化一个预定义的license更新业务流程:1. 在经理与雇员之间双向传递电子化信息


2. 要求经理与雇员都要做电子化确认；


3. 指导雇员编排预备工作时间表


4. 指导经理审核并批准时间表


5. 要求雇员输入认证测试日期


6. 逐步告警功能，如果没有足够的再测试时间获得的话


7. 要求经理校验新的license


8. 传递认证失败的通知给经理和时间表调度程序


提供许可证更新业务流程的在线、实时的报表。产生月度和季度的绩效审计报表

 [1]: http://www.pentaho.com/