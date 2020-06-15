---
title: Response.Redirect, Server.Transfer
author: wiloon
type: post
date: 2012-11-15T01:51:12+00:00
url: /?p=4679
categories:
  - Web

---
<div id="art_demo">
  http://www.jb51.net/article/20928.htm



  如果你读过很多行业杂志和 ASP.NET 示例，你会发现，大多数人使用 Response.Redirect 将用户引导到另一个页面，而另一些人好像偏爱于神秘的 Server.Transfer，那么，这二者有什么区别？





<div id="con_all">


<div id="art_content">
  Response.Redirect 简单地发送一条消息到浏览器，告诉浏览器定位到另一个页面。你可以使用下面的代码将用户引导到另一个页面：
 Response.Redirect("WebForm2.aspx")
 或者
 Response.Redirect("http://www.cnnas.com/")
 Server.Transfer 也是通过一条语句将用户引导到另一页面，比如：Server.Transfer("WebForm2.aspx")。不过，这条语句有一系列独特的优缺点。
 首先，通过 Server.Transfer 引导到另一页面保留服务器资源，通过更改服务器端“焦点”和传输请求来代替告诉浏览器重定向，这就意味着你不会占用较多的 HTTP 请求，因此这可以减轻服务器的压力，使你的服务器运行更快。
 不过，请注意，由于 "transfer" 只能在同一服务器端的同一站点间运行，所以你不能用 Server.Transfer 将用户重定向到另一服务器上的站点。要重定向到服务器以外的站点，只有 Response.Redirect 能办到。
 其次，Server.Transfer 保留浏览器端的 URL 地址。这对流线型的数据输入很有帮助，不过这也增加了调试的复杂度。
 还有：Server.Transfer 方法还有另一个参数——"preserveForm"。如果你设置这个参数为 True，比如：Server.Transfer("WebForm2.aspx", True), 那么 query string 和任何 form 变量都会同时传递到你定位的页面。
 例：WebForm1.aspx 有一个文本框名为 TextBox1，你利用 preserveForm 为 True 传递到 WebForm2.aspx，你仍然可以用 Request.Form("TextBox1") 来取得文本框的值。
 这种技术对向导式的多页面输入很有用，不过这里有一个你必须注意的问题是，当你使用 preserveForm 参数时，ASP.NET 有一个 bug，通常情况下，当试图传递 form 或 query string 值时会发生错误。请参见：http://support.microsoft.com/default.aspx?id=kb;en-us;Q316920
 非官方的解决办法是在你要传递的目的页面中设置 enableViewStateMac 属性为 True，然后再将其设置回 False。这说明你需要使用 enableViewStateMac 的 False 值才能解决这个问题。
 总结：Response.Redirect 简单地告诉浏览器访问另一个页面。Server.Transfer 有利于减少服务器请求，保持地址栏 URL 不变，允许你将 query string 和 form 变量传递到另一个页面（有一点小小的缺陷）。
 重要提示：不要混淆了 Server.Transfer 和 Server.Execute，Server.Execute 执行一个页面，并返回结果，在过去 Server.Execute 很有用，不过在 ASP.NET 里，它被 fresher 方法所代替，所以忽略 Server.Execute。 
  
  
    使用HttpContext.RewritePath来配合Server.Transfer/Execute 
    
    
      我想由不少人都懂得在Applicaton_Start等事件中使用HttpContext.RewritePath来改变HttpHandler。
    
    
    
      如果在Server.Transfer/Execute的调用前，使用RewritePath，更可以起到指定QueryString的效果。
    
    
    
      例如
    
    
    
      Context.RewritePath("AA.Aspx","","OKOK=3333");
 Context.Server.Transfer("Test2.Aspx");
    
    
    
      这样，就能执行Test2.Aspx，并且QueryString是OKOK=3333。
    
    
    
      这个用途特别大。我目前用这个方法来避免使用Response.Redirect。
    
    
    
      Server.Transfer,Response.Redirect的区别
    
    
    
      Server.Transfer（ASP 3.0 以上） 和 Response.Redirect 在以前的 ASP 中就存在了，Page.Navigate 是 ASP.NET Beta 1 提供的新功能，它们之间的区别在于：
    
    
    
      1、Server.Transfer &#8211; 用于把处理的控制权从一个页面转移到另一个页面，在转移的过程中，没有离开服务器，内部控件（如：request, session 等）的保存的信息不变，因此，你能从页面 A 跳到页面 B 而不会丢失页面 A 中收集的用户提交信息。此外，在转移的过程中，浏览器的 URL 栏不变。
    
    
    
      2、Response.Redirect &#8211; 发送一个 HTTP 响应到客户端，告诉客户端跳转到一个新的页面，客户端再发送跳转请求到服务器。使用此方法时，将无法保存所有的内部控件数据，页面 A 跳转到页面 B，页面 B 将无法访问页面 A 中 Form 提交的数据。
    
    
    
      3、Page.Navigate &#8211; Page.Navigate 实现的功能和 Response.Redirect 差不多，它实际上包括三个步骤：首先调用 Response.Redirect，其次依次卸载所有的控件，最后调用 Response.End。
    
    
    
      特别要注意的是：在 .NET Beta 2 中，Microsoft 将不再包括 Page.Navigate 这个功能，大家应该现在就用 Response.Redirect 来代替 Page.Navigate，以节省将来升级时的时间。
    
  
  
  
    (1)Server.Transfer方法:
 Server.Transfer("m2.aspx");//页面转向(服务器上执行).
 服务器停止解析本页,保存此页转向前的数据后,再使页面转向到m2.aspx,
 并将转向前数据加上m2.aspx页结果返回给浏览器.
 <img title="点击图片可在新窗口打开" src="http://www.jb51.net/upload/2009-11/20091114002305895.jpg" alt="" border="0" />
  
  
  
    (2)Server.Execute方法:
 Server.Execute("m2.aspx");
 服务器保存此页转向前的数据后,使页面转向到m2.aspx执行,
 再返回本页继续执行.再将三者结果合并后返回给浏览器.
  
  
  
    以上都是服务器端页面转向所以浏览器不出现页更改记录(显示的地址不会改变).
 因此,如果用户刷新此页,也许会出现一些其它意外情况.
 此类页转向,可完成一些其它功能,比如访问到前一页面中的服务端控件.
 <img title="点击图片可在新窗口打开" src="http://www.jb51.net/upload/2009-11/20091114002305632.jpg" alt="" border="0" />
  
  
  
    (3)Response.Redirect:
 当浏览器请求aspx页面时,碰到Redirect(url)方法,
 相当于告诉浏览器,你先需访问某页面,于是浏览器再向服务器发送一个到此页面的请求.
 重定位是通过浏览器执行的,在服务器和浏览器之间会产生额外的往返过程。
 在网络状况不是很好的情况下,两次请求会大大的
 降低应用程序的反应速度,甚至占用多余的带宽.
 <img title="点击图片可在新窗口打开" src="http://www.jb51.net/upload/2009-11/20091114002305353.jpg" alt="" border="0" />
 总结:
 在网络状态较好的情况下,Redirect(url)方法效率最高!!
 Server.Transfer方法和Server.Execute方法最灵活!!
 Server.Execute方法占用资源最多.