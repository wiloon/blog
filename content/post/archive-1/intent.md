---
title: Intent
author: "-"
date: 2014-08-29T08:16:27+00:00
url: /?p=6968
categories:
  - Uncategorized

tags:
  - reprint
---
## Intent
Android中提供了Intent机制来协助应用间的交互与通讯，Intent负责对应用中一次操作的动作、动作涉及数据、附加数据进行描述，Android则根据此Intent的描述，负责找到对应的组件，将 Intent传递给调用的组件，并完成组件的调用。Intent不仅可用于应用程序之间，也可用于应用程序内部的Activity/Service之间的交互。因此，Intent在这里起着一个媒体中介的作用，专门提供组件互相调用的相关信息，实现调用者与被调用者之间的解耦。在SDK中给出了Intent作用的表现形式为: 

通过Context.startActivity() orActivity.startActivityForResult() 启动一个Activity；
  
通过 Context.startService() 启动一个服务，或者通过Context.bindService() 和后台服务交互；
  
通过广播方法(比如 Context.sendBroadcast(),Context.sendOrderedBroadcast(), Context.sendStickyBroadcast()) 发给broadcast receivers。
  
Intent属性的设置，包括以下几点:  (以下为XML中定义，当然也可以通过Intent类的方法来获取和设置) 

【putExtra("A",B)中，AB为键值对，第一个参数为键名，第二个参数为键对应的值。顺便提一下，如果想取出Intent对象中的这些值，需要在你的另一个Activity中用getXXXXXExtra方法，注意需要使用对应类型的方法，参数为键名】

http://www.cnblogs.com/feisky/archive/2010/01/16/1649081.html

http://www.eoeandroid.com/thread-204417-1-1.html