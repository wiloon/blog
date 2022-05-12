---
title: agile scrum tools
author: "-"
date: 2012-10-24T03:04:32+00:00
url: /?p=4519
categories:
  - Agile
tags:$
  - reprint
---
## agile scrum tools
### wekan
https://github.com/wekan/wekan

**VersionOne**

商业化产品！没什么好说的，业界老大！

从 功能上看，的确非常新颖，贯彻了敏捷中的User Story为先的原则，和VSTS类似，将Issues、Defect、Task合并概念成为Task(在VSTS中更加优雅，叫做WorkItem)， 并且必须挂在UserStory下，这个工具值得看看，有试用版可以下载，或者可以使用他们在线提供的试验平台

基于ASP.NET and IIS和 SQL。

团队可以使用"V1: 敏捷团队"来管理产品和sprint backlog，通过交互式的"任务板 (taskboards) "和"测试板 (testboards) " 进行每日开发活动，藉由报表和燃烧图查看进度，以及其他活动。

通过这些功能，"V1: 敏捷团队"的用户可以做到: 

  * 从电子表格中快速导入故事与缺陷，管理合并后的产品backlog。
  * 利用简单的多条目拖放操作，方便地完成计划制定、对故事划分优先级。
  * 使用电子白板界面同时制定多个版本的发布计划，提高效率。
  * 通过交互式的任务板 (Taskboard) 、测试板 (Testboard) 、每日Scrum dashboard来对版本和sprint进行可视化追踪。
  * 针对版本和sprints的关键敏捷度量数据生成图表，如Burndown、Velocity、Estimate trends、Cumulative Flow Reports。

唯一的问题就是提供的选择过多，对于寻求简单明了工具的人，并不是一个好产品！.

**Rally**

商业软件用户使用率排名第二位！支持用户需求的筛选、扩展的筛选标准、改进版本剩余时间表、新的通知规则 (notification rules) ，以及用于Eclipse和CruiseControl.NET的连接器。

有免费在线试用体验版本.

**Mingle**

Mingle在ThoughtWorks官方站点可以免费下载，且5个用户以下的可以永久免费使用。Mingle是用纯Ruby打造的且运行在JRuby上 的一个产品，由于ruby是一门脚本语言，所以其移植性就很好，用其编写的程序安装起来也甚是容易，在Windows、Mac和Unix多种主流平台上跑 都是没有问题的；但也正是由于采用ruby编写，Mingle对硬件的要求也甚高，在我这台512M内存的机器上跑是超慢的、让人闹心的，建议还是放到性 能好的、单独的服务器上，内存容量官方建议是2G。还遇到了好几次ie错误，只好放弃了。

Mingle后台存储采用数据库方式，目前仅支持MySQL和Postgres两种数据库版本，这个比 较遗憾，我无法使用现成的Oracle数据库了。

简单用了一下，发现如下很好的Features: 

  * 支持建立"个性化"项目模板，便于复用；
  * 附带项目wiki，便于"项目知识积累和管理"；
  * 丰富的card properties，使需求驱动的管理流程更加清晰；
  * 支持card和源代码之间的link；.

  agilefant
  
    XPlanner
  
  
    最牛的祖父级的开源工具，完全免费，业界使用率排名第四，真的是穷人的项目管理工具！
  
  
    作为一个基于Web的XP团队计划和跟踪工具，要求 Apace Tomcat。
  
  
    XP 独特的开发概念如iteration、user stories等，XPlanner都提供了相对应的的管理工具，XPlanner支持XP开发流程，并解决利用XP思想来开发项目所碰到的问题。 XPlanner特点包括: 简单的模型规划，虚拟笔记卡(Virtual note cards),iterations、user stories与工作记录的追踪，未完成stories将自动迭代，工作时间追踪，生成团队效率，个人工时报表，SOAP界面支持。.
  

**白板**

最直接的方式，用于每天的tracking，还是非常不错的，但是对Product Backlog支持明显不够

**Excel**

我们最初也用过，主要是成员多的情况下，修改时会相互冲突，不好同步。。可以参考我写的这个文章[[scrum工具]用excel表格工具实现Scrum][1]

**ScrumWiki**

这个也用过，一开始感觉还不错。但当你的需求变多变复杂的情况下，就不容易用了。后台脚本使用Perl写的，我们的一个外国同事还对他专门进行了修改，增加了好多feature,这样才好用起来。作为免费的软件，目前已经没有人支持和维护。

**Scarab**

Java server 平台, 支持灵活定制，免费

**Double Chocco Latte**

基于PHP , 支持Apache 或IIS, MySQL or SQL Server , web 客户端，免费

**
  
** 

**GNATS**

GNATS 传统来讲，属于缺陷跟踪工具, 但根据Jeff Sutherland， 已经支持 Scrum. 免费

**Select Scope Manager**

商业化产品，有试用版可下载。定制性比较差.

**XP Plan-it**

仅仅支持把你的数据放在他的server上，你通过下载的客户端更新和查看数据。。 好像对大多数人来讲意义不大

**XPWeb**

另一个基于web的分布式方案。免费！

使用PHP+MySQL可运行于Linux, Windows, or Mac.但其演示在IE7下工作不怎么样，没法详细测试.

**
  
** 

**ScrumWorks**

个人认为对Scrum个方面支持最好的商业产品，市场排名第三位,我们一直在用。可支持不同的Team工作于不同的项目上，非常灵活。既有简单的web客户端，也有强大的java客户端。

有免费使用版，且无时间限制，我用的就是。

支持对Bugzilla和Jira的集成，带有主题过滤功能的burndown图表，以及其他辅助了解项目状况和走势的功能，还有众多别的特性。

ScrumWorks Pro与Bugzilla和Jira的集成，体现在它可以导入两者中的条目作为backlog条目，并且可以像对其他backlog条目一样，对这些条目 进行操作。可以使用搜索来选择感兴趣的条目，并进行单独或多项导入操作。Infoq与Danube科技的JD Aspinall进行了交流，讨论了这个特性的本质，以及如何与ScrumWorks Pro一起使用Bugzilla和Jira。

我想提出这个特性请求的用户们都希望同时使用这两个工具。

产品的许多用户将他们全部的bug作为Product Backlog条目录入到ScrumWorks Pro中并进行跟踪。不过也有很多其他用户，由于其他种种原因，使用不同的工具来跟踪问题，并且只选择导入某些特定的缺陷到ScrumWorks Pro中。

Burndown图表现在可以按照主题 进行分组。将backlog按照主题进行组织后 (类似于web 2.0中使用标签) ，你可以高亮或是过滤这些backlog，并且能够使用同样的主题针对burndown图进行过滤。

**ProjectCards**

ProjectCards 维持项目管理的索引卡片，精确的具体内容，一个项目控制盘，搜寻和过滤能力和拖放反复计划。六十日免费的试用。

基于 Client/Server结构，支持plug-in for Eclipse.

**TargetProcess**

是一个敏捷项目管理与Bug跟踪系统。企业版提供很多定制的功能，包括Pre-paid 20 hours of development by TargetProcess stuff和提供开发指南与API参考的全部源代码。

这个工具挺适合小项目团队的。

这儿有个 Demo 帮助读者理解这个产品，内容是通过创建一个新的项目，在迭代计划时给开发人员指派故事 (Story) 。

他们的价格模式包括"按站点 / On Site" (需要安装) 和"按需 / On Demand" (Web版) ，并提供折扣。

**ExtremePlanner**

一个基于web的工具，它的功能几乎与ProjectCards完全一样，但是它添加了在任务级别进行评估的功能，这一改进非常棒。由于是基于web的， 所以它的界面可能不够漂亮，但是由于基于浏览器，它获得了一些灵活性 (例如，当项目成员想在线查看状态报告时，如果是使用ExtremePlanner，就无需安装任何东西。) 

我还在进一步考察这个工具，但是它看起来相当不错。

要求Windows, Linux, or MacOSX平台 (with Java 1.4.2 or higher and Apache Tomcat 4.1 or higher)

**
  
** 

**TRICHORD**

这个名为"TRICHORD"的敏捷项目管理工具，是基于精益思想的，对Scrum也适用。TRI指的是三种视角 (时间、任务和团队) ，CHORD则是和谐的意思。

它作为全团队分享项目状态的一个工作空间来运作，里面提供三种层次的看板图——特性看板 (发布—特性) 、故事看板 (故事—迭代) 和任务看板 (工作日—任务) 。特性看板用停车场图来归纳，故事和任务看板用延烧图来归纳。

<http://agilescout.com/best-agile-scrum-tools/>

 [1]: http://scrumxp.blogspot.com/2008/09/excelscrum.html