---
title: SVN中Branch/tag
author: "-"
date: 2015-11-11T02:20:43+00:00
url: /?p=8454
categories:
  - Inbox
tags:
  - reprint
---
## SVN中Branch/tag
http://blog.csdn.net/adupt/article/details/4203133

SVN中Branch/tag的比较
  
分类:  SVN2009-05-20 10:23 8700人阅读 评论(0) 收藏 举报
  
svnbranchmergetortoisesvnurl测试
  
在SVN中Branch/tag在一个功能选项中,在使用中也往往产生混淆。

在实现上,branch和tag,对于svn都是使用copy实现的,所以他们在默认的权限上和一般的目录没有区别。至于何时用tag,何时用branch,完全由人主观的根据规范和需要来选择,而不是强制的 (比如cvs) 。

一般情况下,
  
tag,是用来做一个milestone的,不管是不是release,都是一个可用的版本。这里,应该是只读的。更多的是一个显示用的,给人一个可读 (readable) 的标记。
  
branch,是用来做并行开发的,这里的并行是指和trunk进行比较。

比如,3.0开发完成,这个时候要做一个tag,tag_release_3_0,然后基于这个tag做release,比如安装程序等。trunk进入 3.1的开发,但是3.0发现了bug,那么就需要基于tag_release_3_0做一个branch,branch_bugfix_3_0,基于这 个branch进行bugfix,等到bugfix结束,做一个tag,tag_release_3_0_1,然后,根据需要决定 branch_bugfix_3_0是否并入trunk。

对于svn还要注意的一点,就是它是全局版本号,其实这个就是一个tag的标记,所以我们经常可以看到,什么什么release,基于xxx项目的 2xxxx版本。就是这个意思了。但是,它还明确的给出一个tag的概念,就是因为这个更加的可读,毕竟记住tag_release_1_0要比记住一个 很大的版本号容易的多。


svn中建立branch或者tag的方法比较简单,totoiseSVN中的操作是:
  
1.选择Branch/tag..
  
2.在出来的界面中的To URL中填上URL,一般是svn://IP/Project/branches/branch-1, 这样就建立了一个branch-1的branch. 建立tag是一样的操作,只不过URL一般是svn://IP/Project/tags/tag-1
  
3.后面的Create copy from是用于选择从你当前的working base中的哪个版本中建立branch/tag,可以根据自己的选择来订制,一般选择Head Revision
  
subclipse中几乎是一样的操作。

Merge分为很多种:
  
1.多个branch之间merge
  
2.branch merge到trunk
  
3.trunk merge到branch
  
第2种用的比较多,比如在otfs接口中netamount的需求提出后就得建立一个netamount的branch,trunk继续在非 netamount的情况下继续开发,netamount单独开发,当netamount功能测试通过后,将netamount branch merge到trunk下,然后将trunk release。
  
第3种情况用的也不少,如上的例子,当用户进行netamount测试时,如果用户不想只测试netamount的功能,则需要将trunk中的修改merge到netamount branch,然后从netamount branch中发布一个版本供用户测试。

branch merge to trunk在tortoiseSVN操作如下:
  
1.选择TortoiseSVN->Merge
  
2.选择Reintegrate a branch
  
3.选择From URL,URL填好之后可以点击Show Log,可以看看这个branch是否是你要merge的内容,下面的Working copy中也可以Show Log,可以确认一下你的工作目录是否是trunk。确认后点击Next
  
4.Merge Options里面有些选项,根据需要来选择,Test Merge按钮会告诉你这次Merge会做哪些操作,最好先Test Merge一下!如果是预期的Merge操作,点击Merge则可以将branch Merge到本地工作目录下
  
5.有冲突的文件需要解决好冲突,解决之后点击svn commit则完成了merge

从多个revision中merge到本地工作目录在tortoiseSVN的操作如下:
  
1.选择TortoiseSVN->Merge
  
2.选择Merge a range of revisions
  
3.URL to merge from填上merge的来源,merge 来源一般和你的working copy是不同的branch或者working copy是trunk 而merge from是branch
  
4.Revision range to merge填上需要merge的revision,格式是1,3,5或者 1-10
  
5.后续操作同Reintegrate a branch

subclipse进行Merge操作同tortoiseSVN的操作方式有所区别,原理基本同Merge a range of revisions。
  
点击Team->Merge后,只有一个界面,这个界面提供了两种Merge操作方式:
  
1.Merge某个版本范围内的修改到本地工作目录上
  
2.Merge feature branch到trunk (也需要先merge到本地)
  
第1种的操作方法是:
  
1.在from url中填上branch的url
  
2.from revision中选择建立这个branch的revision号,不是最新的那个版本号!
  
3.to url框中勾上"Use 'From:' URL"这个check box, To Revision中选择需要需要Merge到的revision号,一般勾head revision
  
4.Dry run让你预览一下merge效果,Unified Diff将Merge的两边进行Diff并将Diff结果保存到文件中。(在我机器中Dry run没有窗口出来,diff结果的文件除非只有很小的变化,不然看得头大)
  
5.点击Merge将merge到本地,这时候与版本库进行一下同步应该和上一步的dry run有同样的效果,如果merge过来的东西不是你预期的更改可以选择revert,但是新增的文件需要手工删除!如果是预期的merge效果,那 commit,记得在comments中写上merge来的branch、from revision、to revision(不要写head,写数字)

总的来看subclipse的merge操作并不方便,不如tortoiseSVN