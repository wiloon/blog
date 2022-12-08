---
title: 'linux  字体引擎'
author: "-"
date: 2017-02-15T02:48:32+00:00
url: /?p=9811
categories:
  - Font
tags:
  - reprint
---
## 'linux  字体引擎'

linux下主要使用xtt freetype xfs xft这四种字体引擎,以下是这四种字体引擎的区别,
  
xtt, freetype, xfs, xft等的区别
  
X Window是所谓client-server结构,这里的server管显示(输出)、键盘和鼠标(输入)部分,而client则是你正在用的程序,比如编辑器。Server收集键盘和鼠标的输入,送到编辑器这一client,编辑器经过处理后,回过来再让server去显示一些字到屏幕上,来回折腾。
  
怎样显示一个字呢?
  
一个字实际上就是一个小图,如果小图上的点非黑即白,就称为黑白点阵;如果小图上的点可以有不同的亮度甚至颜色,则称为AA点阵。每个字,也就是每个小图都有固定的编号,编辑器(client)可以只告诉server某个编号,server根据该编号去找出对应的小图,这种方案就是所谓的server side font,如FreeType,X-TrueType等backend就属此类;如果编辑器自己去找小图,干脆把小图送给server去显示,这种方案就是所谓client side font,Xft属这一类。
  
server side font
  
FreeType backend: 即XF86Config中的freetype模块
  
X-TrueType backend: 即XF86Config中的xtt模块
  
client side font
  
Xft: 设置文件是fonts.conf
  
还有一类,xfs,跟server side font一样,client把字编码传给server,但server并不直接从字库中读出对应该编码的小图,而是把编码再传给另外的所谓font server,由font server去字库找出对应的图,返回给X server去显示,姑且将这种方式称为font server font:
  
font server font
  
xfs: 设置文件是X11/fs/config
  
不管是哪一类,最终都要去字库文件读出对应编码的小图,至少对TrueType格式的字库文件而言,xtt也好,freetype也好,Xft也好,几乎都用到了FreeType这一字库engine,虽然xtt没人继续改进,还是用FreeType 1,别人都改用FreeType 2了。正因为大家都用FreeType字库engine,使得xtt,freetype,Xft这些名字容易弄混,让人头大。解决的办法很简单:不要再去管什么xtt,不要再去管什么freetype,不要再去管什么xfs:只要弄清Xft就够了。

X字库设置必读: Juliusz Chroboczek的Fonts in XFree86
  
<http://www.xfree86.org/~dawes/4.3.0/fonts.html>

理论知识
  
freetype分两个主要阶段的版本: 1.x和2.x。Freetype 是开源字体渲染引擎,并不只为X设计。它的功能就是读取Truetype字体信息,如大小、分辨率、编码等,然后渲染成所需的位图数据输出。2.x与1.x 相比最大的差别就是加入了抗锯齿功能。
  
其中freetype和xtt是X的内部模块,都是使用freetype1来渲染字体。
  
xfs以服务的形式出现,也可以作为X的内部模块,使用freetype2来渲染字体。
  
xft也属于一个外部服务程序,以动态链接的形式提供,也就是说在需要的时候才被加载,同时也只有xft支持antialias。xft使用FontConfig来自定义和选择字体。
  
freetype、xtt和xfs可在X下用xlsfonts列出当前可用的X核心字体,xft可用fc-list列举当前可用字体。
  
这么多引擎到底用哪个好呢？freetype推荐使用2.x版本,所以如果当你使用的程序不支持xft的时候最好使用xfs。而对于中文的支持其实xtt的效果最好,因为对于小字体用函数描述法算出来的中文字体效果不能让人满意,所以很多中文字体公司就在Truetype字体里嵌入了位图字体。这些位图字体需要用特殊的方式读出来,所有的引擎中就只有xtt能做到这一点。但xtt有个问题就是速度太慢,反正我使用debian时使用xtt的时候使用 SimSun字体很慢的,但愿是我的配置有问题吧。当然了,能使用xft的时候一定要使用xft哦,xft显示出来的字体确实很漂亮,尤其是使用 Microsoft的Tahoma字体效果特别明显,你可以用fvwm配置着试一下,使用X核心字体-microsoft-tahoma-medium- r-normal-12-\*-\*-\*-\*-*-iso8859-1,然后再使用FontConfig来渲染试下xft:Tahoma:Medium: Size=12:encoding=iso8859-1,看看效果就知道了,gtk2和kde目前都采用xft来显示字体。

配置
  
freetype 和xtt的配置很简单,只要在/etc/X11/XF86Config-4(XFree86)或/etc/X11/xorg.conf(xorg)文件中加入FontPath 您的字体目录然后加载相应的引擎模块即可,注意的一点是freetype和xtt都是用freetype1来渲染字体不能同时使用的,只能加载其中一个模块。添加新字体时只需要在你新加的字体目录中创建fonts.dir和fonts.scale文件即可,创建方法可使用mkfontdir和 mkfontscale或者ttmkfdir,据说mkfontdir和mkfontscale创建的fonts.dir和fonts.scale有问题,但我使用时好象没遇到过问题,如果不行的话就用ttmkfdir创建fonts.scale然后再复制一个fonts.scale为 fonts.dir,具体操作可以看看man pages,进入你新建的字体目录下执行mkfontdir和mkfontscale或者执行ttmkfdir && cp fonts.scale fonts.dir即可。 (注: 如果你不知道将FontPath和LoadModule加在什么地方的话就别用X了哈)
  
xfs 的配置大同小异,xfs的配置文件为/etc/X11/fs/config。如果需要添加字体也需要创建fonts.dir和fonts.scale,创建方法同上,注意这儿字体目录不是添加在/etc/X11/XF86Config-4或/etc/X11/xorg.conf,而是将字体目录添加到 /etc/X11/fs/config中的catalogue那一行中,然后重启xfs服务/etc/init.d/xfs restart,不过你要注意在你的/etc/X11/XF86Config-4或/etc/X11/xorg.conf中是否加过了FontPath "Unix/:7100",如果没有的话自己手动加上吧。
  
xft的配置稍微麻烦一些,配置文件为/etc/fonts/fonts.conf,有点累了,看看我的另外一篇文章" "吧。添加新字体的话执行一下fc-cache -fv 你的新字体目录即可。
  
添加了新字体后,如果是xft可以用fc-list看看你新添加的字体应该已经列出来了 (这个程序是基于console的,你在控制台就可以检查) ,如果是使用freetype、xtt或xfs的话你需要进入X然后执行xlsfonts检查是否列出了你新加的字体。

使用
  
用fvwm来检验效果是最好的了,你可以打开~/.fvwm/.fvwm2rc也可以在fvwm下打开fvwm的console模块进行试验,举个例子可以简单地加一个中文的菜单条目,然后配置菜单的样式。
  
如果只试验freetype你可以编辑你的XF86Config-4或xorg.conf加载freetype,注释掉FontPath "unix/:7100",如果只试验xtt也是编辑它但不同的是加载xtt而不是freetype (如果有LoadModule freetype请注释掉) ,如果只试验xfs的话就只留下FontPath "unix/:7100"同时去掉加载freetype或xtt的行。
  
对于freetype、xtt或xfs的使用都是一样的,设置fvwm的菜单样式可以这样设置MenuStyle \* Font "-adobe-helvetica-medium-r-normal-12-\*-\*-\*-\*-\*-iso8859-1,-misc-simsun-medium -r-normal-12-\*-\*-\*-\*-\*-gbk-0,-\*-" (对于iso8859-1字符集的文字使用helvetica字体显示,对于 gbk-0字符集的文字使用simsun显示,其它的自动查找吧) 。
  
如果你要在fvwm中使用xft的话不用修改XF86Config- 4或xorg.conf,直接这样设置fvwm的菜单样式MenuStyle \* Font "xft:Tahoma:Medium:Size=12:encoding=iso8859-1",如果要显示中文则这样设置MenuStyle \* Font "StringEncoding=gbk-0:xft:SimSun:Medium:Size=12:encoding=iso10646-1",使用 xft实现刚才的功能 (中英文使用不同的字体显示) 我一直没找到方法,如果你知道的话一定记得告诉我,在此谢过了。

<http://blog.csdn.net/wesleyluo/article/details/7470362>

<http://i.linuxtoy.org/docs/guide/ch19s07.html>
