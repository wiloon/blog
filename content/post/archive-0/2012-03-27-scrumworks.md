---
title: scrumWorks
author: wiloon
type: post
date: 2012-03-27T03:05:55+00:00
url: /?p=2642
categories:
  - Agile

---
scrumWorks Pro是一个敏捷项目管理工具，它能够帮助团队跟踪每次迭代与整个版本发布的过程。本次版本的变化集中在两个方面：可用性的改进以及使用[MySQL][1]作为后端数据库。

根据Danube的CTO Victor Szalvay所说，这一版本关注的一 个方面是对界面美观性和可用性方面的改进。对UI作出的多个改进包括：

<ul id="dosl" type="disc">
  <li id="y28b">
    <strong id="s.wh">新的产品创建向导</strong>——指导用户根据决策（团队、角色和权限以及产品的属性）创建一个新产品。
  </li>
  <li id="xs6d">
    <strong id="cshf">Docking框架</strong>——与Eclipse相似，用户能够使窗口停靠（dock）在其父控件的任何一侧，以便于能够同时浏览多个编辑器。
  </li>
  <li id="pshu">
    <strong id="d7g:">标签方式编辑</strong>——与Firefox相似，用户能够在自己的标签（tab）中，整齐地显示针对不同故事或任务的编辑器。
  </li>
  <li id="eywj">
    <strong id="nlh2">拆分（Split）特性</strong>——在创建一批故事（或者任务）时，用户通常认为一个单独的故事会拥有多个条目。拆分特性简化了将它转换到一个单独故事的步骤。
  </li>
  <li id="ymuq">
    <strong id="y8d8">Sprint详细信息视图</strong>——增强了树型视图的支持，该视图能够将任务与它们的故事关联起来。此外，Sprint视图还支持根据“认领人”、“任务状态”或其他 任一列对内容进行筛选。
  </li>
</ul>

根据 Victor的观点，或许最重要的改变是对MySQL的支持，企业用户希望工具能够支持更大的部署需求规模，而不是使用一个内嵌的数据库。

 [1]: http://www.oschina.net/p/mysql