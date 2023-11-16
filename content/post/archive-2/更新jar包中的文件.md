---
title: 更新Jar包中的文件
author: "-"
date: 2017-08-09T10:00:39+00:00
url: /?p=11023
categories:
  - Inbox
tags:
  - reprint
---
## 更新Jar包中的文件

[http://blackwing.iteye.com/blog/1545670](http://blackwing.iteye.com/blog/1545670)

更新Jar包中的文件

解压 jar xf \***.jar

打包了个fat jar,后来程序作了小修改,如果重新打包一个fat jar再上传服务器实在麻烦,而如果能只把更改的class文件放到原来jar包替换相应文件,则简便很多。

jar命令可以替换jar包对于文件,但需要点小技巧。一般替换 (增加) jar包根目录下的文件,用到的命令是:
  
Java代码 收藏代码
  
jar uvf myjar.jar ClassToAdd.class

就能把ClassToAdd.class添加到myjar.jar包根目录下。但通常,我们的包都是有多层目录的,这时就需要做点更改。例如,我要更新jar包下: com.blackwing目录下的ClassToAdd.class文件,则命令改为:
  
Java代码 收藏代码
  
jar uvf myjar.jar com/blackwing/ClassToAdd.class

记得在运行这条命令前,需要在当前文件夹下建立:
  
com/blackwing文件夹,并且把类ClassToAdd.class放到这里,则可以更新jar包中相应目录的类。
