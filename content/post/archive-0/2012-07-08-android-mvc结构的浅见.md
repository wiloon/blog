---
title: Android MVC结构的浅见
author: w1100n
type: post
date: 2012-07-08T11:24:01+00:00
url: /?p=3819
categories:
  - Uncategorized

---

  <a href="http://qianjigui.iteye.com/blog/856259">http://qianjigui.iteye.com/blog/856259</a> 
  
    <a href="http://www.iteye.com/blogs/tag/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84">数据结构</a><a href="http://www.iteye.com/blogs/tag/MVC">MVC</a><a href="http://www.iteye.com/blogs/tag/Android">Android</a><a href="http://www.iteye.com/blogs/tag/%E7%BD%91%E7%BB%9C%E5%BA%94%E7%94%A8">网络应用</a><a href="http://www.iteye.com/blogs/tag/%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1%E5%99%A8">应用服务器</a>
  

<div id="blog_content">
  
    http://www.cs.otago.ac.nz/cosc346/labs/COSC346-lab2.2up.pdf 写道
  
  
    在Android应用程序中，我们不能够非常清楚地区分MVC结构中的视图部分和控制器部分。Android框架期望开发者们将Activity基础类作为UI处理，这也就意味着一个Activity需要负责视图与控制器两个部分的任务。 
    
    
      利用观察者模式将Model进行绑定处理。
  
  
    Android近期学习总结——开发笔记 写道
  
  
    Android采用了典型的MVC结构。其表现如下： 
    
    
      View既可以通过xml(layout目录下)生成，也可以通过硬编码的方式直接通过代码生成。对于xml中的View资源，可以在代码中通过getViewById()的方法获得。
    
    
    
      Model既可以通过xml(values目录下)生成，也可以硬编码的方式直接在代码中指定。View和Model通过Adapter来进行连接。典型的Adapter包括ArrayAdapter(可以Sort()操作)、CusorAdapter(从Cusor中查询到数据源),ListAdapter、SimpleAdapter(最常用)、SpinnerAdapter(它是一个接口，设置Spinner应用SimpleAdapter的setDropDownResource方法)。
  
  
    谈对android开发的认识 写道
  
  
    Android应用开发一般来说由四大块构成 activity, intent, provider, broadcastreciver. 
    
    
      从这种结构上来看，android系统是提供了从显示层到数据层到消息机制的一整套的应用开发方案，而且是一种比较先进的解决方案。
    
    
    
      从写android代码的过程中，android项目整体是一种典型的MVC结构，非常类似于主要用于WEB开发的J2EE架构。
    
    
    
      xml布局文件是view相当于JSP页面; activity和intent起到了controller的作用; provider对数据层做了良好的封装，而且provider把数据管理的范畴从数据库泛化到了数据的概念，不光管理数据记录，只要是数据文件(图片、视频、声音文件、所有其他的一切的file)都纳入管理，且提供了数据共享的机制，这是比较出彩的地方; broadcastreceiver提供了一种良好的消息机制，使得一个应用不再是一个信息孤岛，而是和其他的应用、服务等构成了信息网络，从而极大的丰富了应用的开发空间，给了应用开发者极大的想象创造的可能。
  
  
    在看了上述讨论后，我受益匪浅。按照以前开发RoR的经验，总觉得如果仅仅将xml布局看作View层未免太单薄，而且负责渲染与事件绑定的工作也全部落到了Activity的头上，这看上去不太合理。不过另一方面说，这看上去不合理的原因是自己见识的太少以及教条主义的影响。
  
  
    那么究竟该如何划分这几层结构呢？我觉得可以换个思路出发，我们究竟该如何合理地组织一个Android应用程序呢？我们不必教条地、具有成见地将原先系统划分结构带入到这样一个新的框架结构中，而是需要在这个特定结构中发挥其框架的效果：
  
  <ol>
    <li>
      xml布局负责将界面布局做好，并且尽量做到合理分割与减少层次
    </li>
    <li>
      Activity做好控件事件绑定与业务流程控制
    </li>
    <li>
      Intent做好Activity间的session传递管理
    </li>
    <li>
      自己创建Model（可以通过Observer模式进行绑定处理、并且包装好各种provider）将处理数据的工作做好。不建议简单地将各个数据字段散乱地存放在Activity周围，而是借助数据Bean的思路存放在Model下面，这样在Model数据项变得庞大后难于管理与重构，而且这多为非面对对象的设计方案。
    </li>
    <li>
      Adapter是数据与呈现的粘合剂
    </li>
  </ol>
  
    以上是个人在做了个Android的一个小应用后的反思与看法，整体上层次是非常低的。在这次开发中，我看到了自己在做客户端软件方面的一些问题，先分享与大家，希望能够共勉：
  
  <ol>
    <li>
      上手新框架时，成见较多，借助以前的思路机械搭建应用。这样没有合理发挥Android框架的优势，做了很多无用功。
    </li>
    <li>
      整个知识网络的整合上面有欠缺，在做RoR时能够良好地利用Bean做数据传递与统一化工作。而在客户端程序时，将数据字段散乱的放在了Activity中。产生这个问题一方面来源于自己的懒惰，因为刚刚开始处理时字段就一个，所以就直接放上去了；到后来数据项激增，但是思路却没有变化。
    </li>
    <li>
      Observer模式是个不错的方案，在应用开发中却没有应用。我觉得这也是在做RoR时的一些问题，和ASP.net不同（事件驱动，容易考虑到观察者模式），RoR多为URL传递后行为触发，各种行为被自然放在了control中。而在Android应用中，错误地将Activity简单地当作了Control，将业务控制逻辑放在了里面最后忘却了观察者模式。
    </li>
    <li>
      测试->开发->重构，的模式可以进一步上升一个层次，对整个流程再重构，这样不至于陷入思维陷阱。
    </li>
  </ol>
