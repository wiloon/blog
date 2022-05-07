---
title: Visio Forward Engineer Addin 正向工程
author: "-"
date: 2015-04-23T02:32:35+00:00
url: /?p=7488
categories:
  - Inbox
tags:
  - Office

---
## Visio Forward Engineer Addin 正向工程
http://www.it165.net/pro/html/201303/5237.html

您跟笔者有一样的困扰吗？设计数据库时利用 Visio 画数据库模型图，画好之后得重新以土法炼钢的方式，透过 SSMS 或 SSDT 等工具，把数据库模型中的数据表以及字段的定义，一个一个的重新输入一次，若数据库中的数据表数量不多时，这也许花不了多少时间，但如果是遇上庞大的系统，数据表数量多得吓人时，传统方式恐怕是旷日废时。透过安装 Visio Forward Engineer Addin 让您可以将在 Visio 2010  画好的数据库模型图直接产生相关的 T-SQL 指令码，详细作法请见下一节。

【实作步骤】

步骤一、下载 Visio Forward Engineer Addin

首先您必须到 CodePlex 下载 Visio 2010 的 Addin 程序，安装完毕之后开启 Visio 2010 就会看到多一个 Forward Engineer 的功能选单。


步骤二、新增数据库模型图

于 Visio 2010 中点选【档案 > 新增 > 数据库模型图】然后按建立来新增一个空白的数据库模型。

于数据库模型图中建立使用者数据表 (Users) 及角色数据表 (Roles) 两个实体，并建立由使用者数据表的 RoleId 数据行参考到角色数据表的  RoleId 数据行。


步骤三、Forward Engineer

点选【Forward Engineer】功能区块，您会看到两个按钮，其中【Validate Data Model】是用来验证您的数据库模型是否正确无误。


验证如果没问题您将看到如下图的画面: 


【Forward Engineer】 则是用来产生模型的相对应的数据库对象指令码。


在进行正向工程时必须在 Forward Engineer to SQL Server 窗口设定下列信息:  www.it165.net

1. Database Name: 搭配 Generate CREATE DATABAE 选项，用来让 Visio Forward Engineer Addin 帮您建立数据库，预设是以您的 VISIO 文件名称当作数据库名称。

2. Output file name: 指定您的指令码的路径及文件名称。

3. Append Code: 是否将 Forward Engineer Addin 产生的指令码附加到指定的档案中。

4. Generate DROP DATABASE: 选择是否产生移除数据库的指令码。

5. Generate CREATE DATABASE: 选择是否产生建立数据库的指令码。

6. Open generated script when finished: 选择是否在指令码建立后开启档案。

下图的设定为为笔者示范之用，您可以依照您的实际需求设定选项内容。


输入相关信息后按 Ok，若您的 *.sql 指令码档案预设是以 SSMS 开启，您应该在产生指令码成功后，会直接开启 SSMS 要求输入连接到数据库的服务器名称及验证信息 (如下图) 。


此时只要按下【F5】即可将 Visio 画好的数据库模型部署到您指定的 SQL Server 之中，执行完毕之后透过数据库图表来查看数据表的关联是否和数据库模型相同，结果如下: 


【结论】

经过测试似乎这个外挂组件有点小问题，若您进行正向工程时有勾选【Append Code】，产生出来的指令码会不完整，不晓得是笔者哪边没设定好，待确认后再上来更新文章。