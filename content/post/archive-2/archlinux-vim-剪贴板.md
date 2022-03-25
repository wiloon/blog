---
title: archlinux vim 剪贴板
author: "-"
date: 2018-12-16T02:09:20+00:00
url: /?p=13100
categories:
  - Uncategorized

tags:
  - reprint
---
## archlinux vim 剪贴板
```bash
sudo pacman -S gvim

#复制到系统粘贴板
"+y

#从系统粘贴板粘贴
"+p
```

https://blog.csdn.net/dadoneo/article/details/6003415

用vim这么久 了,始终也不知道怎么在vim中使用系统粘贴板,通常要在网上复制一段代码都是先gedit打开文件,中键粘贴后关闭,然后再用vim打开编辑,真的不 爽；上次论坛上有人问到了怎么在vim中使用系统粘贴板,印象里回复很多,有好几页的回复却没有解决问题,今天实在受不了了又在网上找办法,竟意外地找到 了,贴出来分享一下。

如果只是想使用系统粘贴板的话直接在输入模式按Shift+Inset就可以了,下面讲一下vim的粘贴板的基础知识,有兴趣的可以看看,应该会有所收获的。
  
vim帮助文档里与粘贴板有关的内容如下: 

vim(我这是GVIM)有17个粘贴板,分别是"、 0、1、2、...、9、-、_、+、. 、 : 、/:: ；用:reg命令可以查看各个粘贴板里的内容。在vim中简单用y只是复制到" (双引号)粘贴板里,同样用p粘贴的也是这个粘贴板里的内容；
  
要将vim的内容复制到某个粘贴板,需要退出编辑模式,进入正常模式后,选择要复制的内容,然后按"Ny完成复制,其中N为粘贴板号(注意是按一下双引号然后按粘贴板号最后按y),例如要把内容复制到粘贴板a,选中内容后按"ay就可以了,有两点需要说明一下: 
  
VIM内部 (") : "号粘贴板 (临时粘贴板) 比较特殊,直接按y就复制到这个粘贴板中了,直接按p就粘贴这个粘贴板中的内容 (也可以说是VIM专用吧) ；
  
与外部程序交互(_/+): +号粘贴板是系统粘贴板,用"+y将内容复制到该粘贴板后可以使用Ctrl+V将其粘贴到其他文档 (如firefox、gedit) 中,同理,要把在其他地方用Ctrl+C或右键复制的内容复制到vim中,需要在正常模式下按"+p；
  
要将vim某个粘贴板里的内容粘贴进来,需要退出编辑模式,在正常模式按"Np,其中N为粘贴板号,如上所述,可以按"5p将5号粘贴板里的内容粘贴进来,也可以按"+p("+* 也行)将系统全局粘贴板里的内容粘贴进来。
  
我用的是GVIM,可能与某些帖子说的不一样,但大体操作还是一样的。好了,现在可以完美运用VIM复制粘贴了,再也不用慢腾腾地点鼠标了。
  
The vim package is built without Xorg support; specifically the +clipboard feature is missing, so Vim will not be able to operate with the primary and clipboard selection buffers. The gvim package provides also the CLI version of Vim with the +clipboard feature.