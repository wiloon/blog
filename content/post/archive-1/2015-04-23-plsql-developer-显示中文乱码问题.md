---
title: PL/SQL Developer 显示中文乱码问题
author: w1100n
type: post
date: 2015-04-23T00:27:24+00:00
url: /?p=7478
categories:
  - Uncategorized

---
http://dw008.blog.51cto.com/2050259/934741


PL/SQL Developer 显示中文乱码问题

简单版本：

首先，通过

select userenv('language') from dual;

查询oracle服务器端的编码， 如为： AMERICAN_AMERICA.US7ASCII 显示什么编码 就设置什么编码


在我们的客户端需要和服务器端的编码保持一致。

因此在客户端，需要设置环境变量： NLS_LANG = AMERICAN_AMERICA.US7ASCII 即可。

以上是默认编码

GBK如下：

在windows中创建一个名为"NLS_LANG"的系统环境变量，设置其值为"SIMPLIFIED CHINESE_CHINA.ZHS16GBK"，然后重新启动 pl/sql developer，这样检索出来的中文内容就不会是乱码了。

UTF-8如下：

如果想转换为UTF8字符集，可以赋予"NLS_LANG"为 "AMERICAN_AMERICA.UTF8"，然后重新启动 pl/sql developer。

其它字符集设置同上。
  
NLS_LANG格式：
  
NLS_LANG = language_territory.charset
  
有三个组成部分（语言、地域和字符集），每个成分控制了NLS子集的特性。其中：language 指定服务器消息的语言。territory 指定服务器的日期和数字格式。charset 指定字符集。

详细版本：

如何设置客户端字符集与服务器端字符集一致:

运行REGEDIT,第一步选HKEY_LOCAL_MACHINE,第二步选择SOFTWARE，第三步选择 Oracle，第四步选择NLS_LANG，键入与服务器端相同的字符集。

例如:AMERICAN_AMERICA.UTF8或者SIMPLIFIED CHINESE_CHINA.ZHS16GBK

oracle 10g装上后,建了个表写入中文数据,发现通过工具PL/SQL Developer中文不能正常显示.

要正常显示中文,就必须得服务器和客户端编码一致才行。于是检查：

1.检查服务器编码:

执行SQL语法:

select * from v$nls_parameters;

也可以参照/home/oracle/.bash_profile 相关语言设置.
  
可以看到我的相关设置是:

LANG=zh_CN.GBK
  
NLS_LANG="SIMPLIFIED CHINESE_CHINA.ZHS16GBK"

2.设置本地客户端编码:

进入我的电脑,属性,高级,环境变量,添加2项:

LANG=zh_CN.GBK
  
NLS_LANG="SIMPLIFIED CHINESE_CHINA.ZHS16GBK"

如图:
  
3.重新连接sqlplus,查看数据:
  
显示正常.

4.PL/SQL Developer设置并重新连接:

在pl/sql developer的菜单->tools->preferences->user interface->fonts 中修改为中文字体

重新连接,如图:

显示正常.OK!