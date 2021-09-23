---
title: Global.asax
author: "-"
type: post
date: 2013-07-08T12:37:39+00:00
url: /?p=5621
categories:
  - Uncategorized

---
在网上找了N多相关的东西总说的不够细,现在终于找到了.可以了解web.cofig和Global.asax之间的关系以及执行的顺序.

在Global.asax.cs文件中

protected void Application_BeginRequest(Object sender, EventArgs e)
  
{
  
Application["StartTime"] = System.DateTime.Now;
  
}

再在webform1中的page_load事件中添加
  
private void Page_Load(object sender, System.EventArgs e)
  
{
  
System.DateTime startTime = (System.DateTime)Application["StartTime"];
  
System.DateTime endTime = System.DateTime.Now;
  
System.TimeSpan ts = endTime - startTime;
  
Response.Write("页面执行时间:"+ ts.Milliseconds +" 毫秒");
  
}

如果是０５版本中,就要手动添加了,自己在App_Code中添加Global.asax.cs,然后设置Global.asax的属性Inherits="Global"或CodeBehind="Global.asax.cs"即可<%@ Application Language="C#" Codebehind="Global.asax.cs" %>

以上测试在０３/０５均通过．

以下转对Global.asax文件的了解

1 Global.asax文件的作用

先看看MSDN的解释,Global.asax 文件（也称为 ASP.NET 应用程序文件) 是一个可选的文件,该文件包含响应 ASP.NET 或HTTP模块所引发的应用程序级别和会话级别事件的代码。Global.asax 文件驻留在 ASP.NET 应用程序的根目录中。运行时,分析 Global.asax 并将其编译到一个动态生成的 .NET Framework 类,该类是从HttpApplication基类派生的。配置 ASP.NET,以便自动拒绝对 Global.asax 文件的任何直接的 URL 请求；外部用户不能下载或查看其中的代码。Global.asax 文件是可选的。只在希望处理应用程序事件或会话事件时,才应创建它.

2 Global.asax文件的创建

点击Web站点>>添加新建项>>全局应用程序类,即可添加Global.asax文件。在.Net2003里,直接右击Global.asax文件查看代码就可以编辑Global.asax.cs文件,但是在.Net2005中,没有这个选项,因此需要自己在App_Code中添加Global.asax.cs,然后设置Global.asax的属性Inherits="Global"或CodeBehind="Global.asax.cs"即可。不可知道还有没有其他更好的方法。

3 Global.asax文件的执行

例如,IIS现在接到一个访问ASP.NET应用程序的请求,这时候IIS会将这个请求映射给aspnet_isapi.dll,当aspnet_isapi.dll接到这个请求后,会新建一个aspnet_wp.exe的进程（windows server 2003下是w3wp.exe进程) ,这个进程会将请求传递给一个被指定的AppDomain,当这个AppDomain被创建时,就会去加载一些配置文件中的信息（加载顺序是从machine.config文件到web.config文件中的一些相关配置) ,而当这些信息都被加载以后,AppDomain会去获得一个HttpApplication的实例,这个时候global类就会被编译加载了,接下来AppDomain会做一些相关的处理创建Page类的实例,最后这个页面呈现到客户端浏览器上。但这里有一点问题需要注意,当配置文件被加载的时候,并不是表示AppDomain会加载配置文件中所有的信息,而仅是加载一些需要的信息。而有些配置信息是在需要时,才会被AppDomain加载。例如我们在web.config文件中配置了很多HttpModule,但是仅当每一个HttpModule被访问到时,AppDomain才会去加载并处理这些信息。所以说web.config文件和global没有先后执行的顺序,只是视具体的信息什么时候会被加载和处理。

4 Global.asax.cs中的方法的含义

Application_Init: 在每一个HttpApplication实例初始化的时候执行

Application_Disposed: 在每一个HttpApplication实例被销毁之前执行

Application_Error: 所有没有处理的错误都会导致这个方法的执行

Application_Start: 在程序初始化的时候执行。在Web应用程序的生命周期里就执行一次,这里只能放一些公用的信息,比如HttpApplicationState。

Application_End: 应用程序结束时,在最后一个HttpApplication销毁之后执行。对应Application_Start,在整个生命周期里面也是只执行一次。

Session_Start: 会话开始时执行。

Session_End: 会话结束或过期时执行。

Application_BeginRequest: BeginRequest是在收到Request时第一个触发的事件,这个方法第一个执行。

Application_AuthenticateRequest: 当安全模块已经建立了当前用户的标识后执行。

Application_AuthorizeRequest: 当安全模块已经验证了当前用户的授权时执行。

Application_ResolveRequestCache: 当ASP.NET完成授权事件以使缓存模块从缓存中为请求提供服务时发生,从而跳过处理程序（页面或者是WebService) 的执行。这样做可以改善网站的性能,这个事件还可以用来判断正文是不是从Cache中得到的。

Application_AcquireRequestState: 当ASP.NET获取当前请求所关联的当前状态（如Session) 时执行。

Application_PreRequestHandlerExecute: 当ASP.Net即将把请求发送到处理程序对象（页面或者是WebService) 之前执行。这个时候,Session就可以用了。

Application_PostRequestHandlerExecute: 当处理程序对象工作完成后执行。

Application_ReleaseRequestState: 在ASP.NET执行完所有请求处理程序后执行。ReleaseRequestState事件将使当前状态数据被保存。

Application_UpdateRequestCache: 在ASP.NET执行完处理程序后为了后续的请求而更新响应缓存时执行。

Application_EndRequest: 同上,EndRequest是在响应Request时最后一个触发的事件,这个方法自然就是最后一个执行的了。

Application_PreSendRequestHeaders: 向客户端发送Http标头之前执行。

Application_PreSendRequestContent: 向客户端发送Http正文之前执行。

Request相应的事件执行顺序: 

1.BeginRequest 2.AuthenticateRequest 3.AuthorizeRequest 4.ResolveRequestCache 5.AcquireRequestState 6.PreRequestHandlerExecute 7.PostRequestHandlerExecute 8.ReleaseRequestState 9.UpdateRequestCache 10.EndRequest

转自: http://hi.baidu.com/mycolorwind/blog/item/45384980228cbfdf9023d960.html