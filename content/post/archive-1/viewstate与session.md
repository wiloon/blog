---
title: ViewState与Session
author: "-"
date: 2013-08-21T04:21:22+00:00
url: /?p=5785
categories:
  - Inbox
tags:
  - reprint
---
## ViewState与Session
昨天偶然看到网上有人讨论究竟是该用viewstate还是session来保存信息. 忽然觉得有必要去深入的研究一下这两个东西了.

我们先来看深入分析一下viewstate, 为了分析的相对完整性,先从简单的说起:

在asp时代, 大家都知道一个html控件的值,比如input 控件值,当我们把表单提交到服务器后, 页面再刷新回来的时候, input里面的数据已经被清空. 这是因为web的无状态性导致的, 服务端每次把html输出到客户端后就不再于客户端有联系.

asp.net巧妙的改变了这一点. 当我们在写一个asp.net表单时, 一旦标明了 form runat=server ,那么,asp.net就会自动在输出时给页面添加一个隐藏域

  <input type="hidden" name="__VIEWSTATE" value="">

那么,有了这个隐藏域,页面里其他所有的控件的状态,包括页面本身的一些状态都会保存到这个控件值里面. 每次页面提交时一起提交到后台,asp.net对其中的值进行解码,然后输出时再根据这个值来恢复各个控件的状态. 我们再看这个控件的value值,它可能类似如下的形式:Oz4+O2w8aTwxPjs+O2w8....
  
很多人会认为这是加密的信息,其实不是, ms仅仅是给各个控件和页面的状态存入适当的对象里面,然后把该对象序列化, 最后再做一次base64编码,直接赋值给viewstate控件.

说到这,想必你一定想看看这个viewstate里面到底存了哪些东西, 嗯,你是可以写一个base64 to string的转换代码来实现.不过,viewstate是有层次之分的,普通的转换后,你看到的也是很乱的文字. 这里提供了一个专门转换viewstate值的地方 [http://www.wilsondotnet.com/Demos/ViewState.aspx][1] . 你可以去将自己的viewstate输入进去,让它给你转化一下,这可是带结构的哦 🙂

好, 以上说的这些你可能会觉得: 这与session有什么关系? 这个viewstate不是由asp.net自动去维护吗? 是的, 如果仅仅是保存控件的状态, 你可以感觉不到它与session有什么瓜葛( 呵呵,其实它们就没有瓜葛),不过,接下来,我们看看这种使用方法: 在后台aspx.cs代码里:

  private void Page_Load(object sender, System.EventArgs e) { ViewState["myvalue"] = "viewstatevalue"; //..... }

呵呵, 可以在页面后台直接给viewstate集合赋值, 现在你是不是觉得和session的使用方法差不多了呢? 对,这一点就是几乎所有初学asp.net的人的疑惑. 会认为asp.net也像session那样把这个值保存到服务器内存里面, 其实不是!

那么,这里的viewstate值是属于谁?又存在哪里? 其实,它和上面的其他控件的状态保存一样,也是存储到那个隐藏的viewstate控件值里面, 上面已经说了, viewstate用来保存状态,包括页面本身, 那么,这里的viewstate就属于页面本身的状态.

分析到此,估计大家对viewstate的使用应该是没有什么疑问了. 那么,我们可以来与session做一下类比, session值是保存在服务器内存上,那么,可以肯定,大量的使用session将导致服务器负担加重. 而viewstate由于只是将数据存入到页面隐藏控件里,不再占用服务器资源,因此, 我们可以将一些需要服务器"记住"的变量和对象保存到viewstate里面. 而sesson则只应该应用在需要跨页面且与每个访问用户相关的变量和对象存储上. 另外,session在默认情况下20分钟就过期,而viewstate则永远不会过期.

但viewstate并不是能存储所有的.net类型数据,它仅仅支持String、Integer、Boolean、Array、ArrayList、Hashtable 以及自定义的一些类型.

当然,任何事物都有两面性, 使用viewstate会增加页面html的输出量,占用更都的带宽,这一点是需要我们慎重考虑的. 另外, 由于所有的viewstate都是存储在一个隐藏域里面,用户可以很容易的通过查看源码来看到这个经过base64编码的值.然后再经过转换就可以获取你存储其中的对象和变量值.

其实,对于viewstate的安全性问题,asp.net还给我们提供了更多的选择.一般如果要保护viewstate有两种方式: 一种是防篡改,一种是加密. 一说到防篡改,我们就想起了使用散列代码. 没错, 我们可以在页面顶部加入如下代码:Page EnableViewStateMAC=true

这样asp.net就会自动的在viewstate中追加一个散列码,在页面回传时,服务器根据回传的viewstate生成一个散列码,再与回传的散列码相比较,如果不对,则丢弃该viewstate,同时控件将恢复初试状态. (默认情况下asp.net是通过SHA1算法而不是md5算法来生成散列,不过这个可以在machine.config里面配置machineKey validation="MD5"即可)

而viewstate加密就更简单了, 只要在machine.config里设置一下machineKey validation="3DES"即可实现用des加密viewstate了.

呵呵,至此,我们对viewstate应该有个很清晰的认识了, 不过,初步研究viewstate, 理解有误之处还望大家多指教 🙂

 [1]: http://www.wilsondotnet.com/Demos/ViewState.aspx ""