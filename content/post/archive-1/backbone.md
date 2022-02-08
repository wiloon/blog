---
title: Backbone
author: "-"
date: 2013-02-02T06:38:02+00:00
url: /?p=5096
categories:
  - Web

tags:
  - reprint
---
## Backbone
Backbone 是一个 JavaScript 框架,可用于创建模型-视图-控制器 (model-view-controller, MVC) 类应用程序和单页界面。

当我们开发含有大量Javascript的web应用程序时,首先你需要做的事情之一便是停止向DOM对象附加数据。 通过复杂多变的jQuery选择符和回调函数创建Javascript应用程序,包括在HTML UI,Javascript逻辑和数据之间保持同步,都不复杂。 但对富客户端应用来说,良好的架构通常是有很多益处的。

Backbone将数据呈现为 [模型][1], 你可以创建模型、对模型进行验证和销毁,甚至将它保存到服务器。 当UI的变化引起模型属性改变时,模型会触发_"change"_事件； 所有显示模型数据的 [视图][2] 会接收到该事件的通知,继而视图重新渲染。 你无需查找DOM来搜索指定_id_的元素去手动更新HTML。 — 当模型改变了,视图便会自动变化。

 [1]: http://www.csser.com/tools/backbone/backbone.js.html#Model
 [2]: http://www.csser.com/tools/backbone/backbone.js.html#View