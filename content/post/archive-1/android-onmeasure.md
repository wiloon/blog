---
title: 'Android  onMeasure'
author: "-"
date: 2014-11-17T06:53:06+00:00
url: /?p=7017
categories:
  - Uncategorized

tags:
  - reprint
---
## 'Android  onMeasure'
Android中View的绘制过程
  
当Activity获得焦点时，它将被要求绘制自己的布局，Android framework将会处理绘制过程，Activity只需提供它的布局的根节点。

绘制过程从布局的根节点开始，从根节点开始测量和绘制整个layout tree。

每一个ViewGroup 负责要求它的每一个孩子被绘制，每一个View负责绘制自己。

因为整个树是按顺序遍历的，所以父节点会先被绘制，而兄弟节点会按照它们在树中出现的顺序被绘制。

绘制是一个两遍 (two pass) 的过程: 一个measure pass和一个layout pass。

测量过程 (measuring pass) 是在measure(int, int)中实现的，是从树的顶端由上到下进行的。

在这个递归过程中，每一个View会把自己的dimension specifications传递下去。

在measure pass的最后，每一个View都存储好了自己的measurements，即测量结果。


第二个是布局过程 (layout pass) ，它发生在 layout(int, int, int, int)中，仍然是从上到下进行 (top-down) 。

在这一遍中，每一个parent都会负责用测量过程中得到的尺寸，把自己的所有孩子放在正确的地方。


http://www.cnblogs.com/mengdd/p/3332882.html