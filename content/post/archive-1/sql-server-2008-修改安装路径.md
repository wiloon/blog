---
title: SQL Server 2008 修改安装路径
author: "-"
date: 2012-11-13T05:29:04+00:00
url: /?p=4655
categories:
  - DataBase
tags:
  - SQLServer

---
## SQL Server 2008 修改安装路径
****
  
**** 

1. 安装时如果修改安装路径后报错

> 例如想把"C:\Program Files\Microsoft SQL Server" 修改为"D:\Program Files\Microsoft SQL Server"
> 
> 错误的详细信息是: "
> 
> "The INSTANCESHAREDWOWDIR command line value was not specified. This value must be specified when the INSTANCESHAREDDIR value is specified."
> 
> "
> 
> 这篇Post回答了这个问题: http://forums.microsoft.com/TechNet/ShowPost.aspx?PostID=3736253&SiteID=17
> 
> 翻译过来就是: 
> 
> 首先: 不修改路径,使用默认方式安装,最后在确认安装时会显示ConfigurationFile.ini文件的路径,到这个路径下面将安装配置文件复制到其他路径,例如D:\,然后退出安装
> 
> 其次: 使用记事本打开这个文件,根据实际需求将"C:\Program Files\Microsoft SQL Server" 查找替换为"D:\Program Files\Microsoft SQL Server"后保存
> 
> 最后: 在命令行转到安装目录,开始安装,如果是Vista,记得使用管理员权限运行命令行,输入以下指令: 
> 
> setup.exe /action=Install /configurationfile=D:\ConfigurationFile.ini
>