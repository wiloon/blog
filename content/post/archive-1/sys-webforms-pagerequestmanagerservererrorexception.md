---
title: Sys.WebForms.PageRequestManagerServerErrorException
author: "-"
date: 2013-07-13T06:51:05+00:00
url: /?p=5647
categories:
  - Inbox
tags:
  - reprint
---
## Sys.WebForms.PageRequestManagerServerErrorException
一、
  
Sys.WebForms.PageRequestManagerServerErrorException: An unknown error occurred while processing the request on the server. The status code returned from the server was: 500错误解决办法

转载的解决办法:

A.在Web.Config
  
<system.web>
  
<pages enableEventValidation="false"/>
  
</system.web>

B.在 ScriptManager  内添加 EnablePartialRendering="false" 显示详细的错误信息。
  
如下: 
  


一般的原因都是页面存在潜在的危险字符  在 页首加入 ValidateRequest="false"
  
如下: 
  
<%@ Page Language="C#" MasterPageFile="~/MasterPages/CompanyManage.master" AutoEventWireup="true" CodeFile="CompanyIntroEdit.aspx.cs" Inherits="CompanyIntroEdit" Title="Untitled Page" ValidateRequest="false" %>

C、去掉updatepanel,看是否有代码错误。代码错误改正,再重新添加。

我的解决办法: 

google搜的结果前两页,不管中文英文都看过了,依然解决不了。用A方法,不可以。用B方法引起二次错误"Extender controls may not be registered before PreRender" 二次错误,也解决不了。用C方法,取出ajax控件,我的代码依然可以用,没有什么错误。

我的代码出现这个错误,是因为又做了一个接口,最后实在没办法,就把做接口前的代码,拿出来,之后,又把接口的类填上,代码和原来一样,然后就可以了。就这。。。。,很奇怪,想不通,记录下来吧。


二、
  
Sys.WebForms.PageRequestManagerServerErrorException: An unknown error occurred while processing the request on the server. The status code returned from the server was : 12031
 原因是查询出的数据超出web.config中的最大大小 (默认4MB) 
  
解决办法

在web.config中的<system.web>下增加如下节点,即可解决
  
<httpRuntime maxRequestLength="8192" />
  
ys.WebForms.PageRequestManagerServerErrorException: An unknown error occurred while processing the request on the server. The status code returned from the server was : 12019
  
12019       ERROR_INTERNET_INCORRECT_HANDLE_STATE
  
The requested operation cannot be carried out because the
  
handle supplied is not in the correct state.

Please refer to this: http://support.microsoft.com/kb/193625
  
这里有这个问题的论坛
  
http://forums.asp.net/p/1126173/2746307.aspx http://forums.asp.net/t/1123365.aspx
  
三、
  
用IE浏览器查看NetFlow的时候出现 Sys.WebForms.PageRequestManagerServerErrorException: An unknown error occurred while processing the request on the server. The status code returned from the server was: 404错误。这个错误出现是因为 .NET Framework 3.5 SP1 升级产生的。Firefox不会出现错误。

解决方法为打开 InetpubSolarWindsOrionMasterPage.master ,找到
  
<form runat="server" method="post" action="#" id="aspnetForm">
  
改为 <form runat="server" method="post" id="aspnetForm"> 。