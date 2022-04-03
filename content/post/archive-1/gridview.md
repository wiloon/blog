---
title: GridView
author: "-"
date: 2012-11-14T06:56:36+00:00
url: /?p=4672
categories:
  - Uncategorized

tags:
  - reprint
---
## GridView
GridView和DataGrid的异同

GridView 是 DataGrid的后继控件，在.net framework 2 中，虽然还存在DataGrid，但是GridView已经走上了历史的前台，取代DataGrid的趋势已是势不可挡。GridView和DataGrid功能相似，都是在web页面中显示数据源中的数据，将数据源中的一行数据，也就是一条记录，显示为在web页面上输出表格中的一行。

GridView相对于DataGrid来说，具有如下优势，功能上更加丰富，因为提供了智能标记面板 (也就是show smart tag) 更加易用方便,常用的排序、分页、更新、删除等操作可以零代码实现！具有PagerTemplate属性，可以自定义用户导航页面，也就是说分页的控制更加随心所欲。GridView和DataGrid在事件模型上也多有不同之处，DataGrid控件引发的都是单个事件，而GridView控件会引发两个事件，一个在操作前发生，一个在操作后发生，操作前的事件多位\*\\*\*ing事件，操作后的事件多位\*\**ed事件，比如Sorting 事件和sorted 事件，RowDeleting和RowDeleted事件。