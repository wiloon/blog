---
title: Jode
author: "-"
date: 2014-04-11T06:48:25+00:00
url: /?p=6521
categories:
  - Uncategorized
tags:
  - Java

---
## Jode
http://moonights.iteye.com/blog/568886

1. Jode介绍

源码开放的JODE是全球最大的开源项目网站Sourceforge.net的成员,在所有的JAVA反编译器中,JODE的反编译效果是最好的,尤其是对付一些常见的加密手段,例如混淆技术等,更是出类拔粹。JODE本身也是纯JAVA开发的,最近越来越多的JAVA反编译软件也选择JODE来做它们的核心引擎,例如JCavaj Java Decompiler、BTJ (Back To Java)、jEdit's JavaInsight plugin等。JODE是一个可运行的JAR文件,在windows环境下双击即可运行。

2. Jode Eclipse插件安装

顺序点击Eclipse上的==>help ==> Software Updates ==> Find and Install ==> Search for new features to install, 单击"New Remote Site...", 在Name中输入Jode Decompliter在URL栏输入 http://www.technoetic.com/eclipse/update 然后下一步,就可以看到"Jode Decompiler"了,选上并单击Finish就开始自动到相应的官网上去下载安装了。安装好后,可以在Window ==> Preferences... ==> Java ==> Jode Decompiler选项卡。

安装好了再设置一下文件关联就可以了,Window => Preferences... => General => Editors => File Associations找到"*.class"在"Associated editors"里面可以看到"Jode class file viewer"选中它再单击Default按钮就OK了

3.Jode的使用

其实之所以要使用Jode就是因为我们往往只有Java的class字节码文件却没有源文件,这时就只有进行反编译了,在Eclipse中我们通常为了查看一个class文件的源代码,必须将它与源文件相关联。而如果我们安装了Jode插件,那么就不用去苦苦寻找源文件了,直接反编译就OK (虽然有时会报出一堆的错误@_@) 。要注意的是Jode只认识.jar文件 (不支持war文件,因此如果是war文件,你因该先将之解压然后打包成.jar包) 。

首先将你要反编译的class文件利用Java自带的jar命令将class文件打包成.jar包,然后导入到你的Eclipse的Project中去,接着就可以展开刚才导入的jar包,查看class文件相应的源文件了。