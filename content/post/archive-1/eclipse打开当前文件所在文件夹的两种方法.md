---
title: eclipse打开当前文件所在文件夹的两种方法
author: "-"
date: 2014-01-09T06:10:52+00:00
url: /?p=6184
categories:
  - Uncategorized
tags:
  - Java

---
## eclipse打开当前文件所在文件夹的两种方法
http://blog.csdn.net/xzknet/article/details/4627713

如果你经常需要在Eclipse里打开相关资源文件所在的文件夹，比较麻烦，要右键，属性，在Location一栏中把所在的文件夹拷贝一下，然后再去资源管理器里输入这个路径，回车，打开它。

解决方法: 
  
用EasyExplorer插件，有了这个插件就可以很方便地打开资源文件所在的文件夹了.

安装: 
  
EasyExplorer 从 http://sourceforge.net/projects/easystruts

下载后就是一个jar压缩文件。最新版就是1.04，已经很久没有更新了，但是对最新的eclipse 3.*平台还是支持的。但是，该插件的安装方式好像通过eclipse 的自动更新管理不起作用。

他最简单的工作方式就是: 直接将该jar文件放置在eclipse的 plugin 目录下 ，然后重启eclipse平台就可以在右键中看到East Explorer菜单项，就可以打开资源所在的目录了。

但是，缺点就是新下载的插件PlugIn放在了原始的Eclipse的PlugIn目录下，一大堆，乱死你:  (

利用EasyExplorer插件可以在Eclipse用Explorer打开资源文件所在的文件夹。其它配置是在这里Windows => Preferences => Easy Explore => Target => explorer.exe {0}

可以看到在Windows平台上是用explorer.exe {0}来打开的，{0}是用来传递参数的。

技巧: 我习惯以资源管理器的方式来打开文件夹，方便进行拖动操作，即左边带文件树，那么在这里你可以设置成为explorer.exe /e,{0} 即可，这样用EasyExplore打开文件夹时就是以这种方式来打开的，而且左边的文件树里，直接定位到文件夹上面，很是方便。

Explorer.exe的参数如下: 大家可以根据自己的喜好进行设定: 
  
命令格式Explorer [/n][/e][[,/root],[path]][[,/select],[path filename]]


参数说明
  
/n表示以"我的电脑"方式打开一个新的窗口，通常打开的是Windows安装分区的根目录。
  
/e表示以"资源管理器"方式打开一个新的窗口，通常打开的也是Windows安装分区的根目录。
  
/root,[path]表示打开指定的文件夹，/root表示只显示指定文件夹下面的文件 (夹) ，不显示其它磁盘分区和文件夹；[path]表示指定的路径。
  
如果不加/root参数，而只用[path]参数，则可以显示其它磁盘分区和文件夹中的内容。另外，[path]还可以指定网络共享文件夹。
  
/select,[path filename]表示打开指定的文件夹并且选中指定的文件，[path filename]表示指定的路径和文件名。
  
如果不加/select参数，则系统会用相应的关联程序打开该文件。如果[path filename]不跟文件名就会打开该文件夹的上级目录并选中该文件夹。

通过对以上explorer.exe的参数分析，我们可能会有个希望就是实现既显示左边的文件树，又同时右边也定位到的选定的文件或文件夹上面。
  
那应当是设置为: explorer.exe /e,/select,{0} ，不过这件EasyExplore帮你打开的只是定位在文件夹上面，而不是相应的文件上面。

* * *


方法二: 

  eclipse打开当前文件所在文件夹的插件
 Run->External Tools->External Tools Configurations...
 new 一个 program
 location 里面填 : C:/WINDOWS/explorer.exe
 Arguments 里面填: ${container_loc} 
  
  <hr />

  总结: 推荐使用插件，真是方便，和Myeclipse没什么区别了
