---
title: git rebase,revert,reset
author: "-"
date: 2014-08-07T01:47:09+00:00
url: /?p=6897
categories:
  - Git
tags:
  - Git

---
## git rebase, revert, reset
回滚提示
本地或者自己单独的仓库使用reset 或者revert都可以
涉及到远程仓库（公用仓库）时，不要使用reset,而使用revert回滚

### git revert
放弃一个或多个提交，并生成一个或多个新的提交来记录这些放弃操作。

#### 撤销前一次 commit
    git revert HEAD  

#### 撤销前前一次 commit
    git revert HEAD^  
#### 撤销指定的版本，撤销也会作为一次提交进行保存。      
    git revert commit （比如：fa042ce57ebbe5bb9c8db709f719cec2c58ee7ff）

####                 
    git revert
    git revert [--[no-]edit] [-n] [-m parent-number] [-s] [-S[<keyid>]] <commit>…​
    git revert --continue
    git revert --quit
    git revert --abort

git revert [--[no-]edit] [-n] [-m parent-number] [-s] [-S[<keyid>]] <commit>…​
--edit or --no-edit是否弹出commit message窗口
**-n **是 --no-commit的缩写
-m parent-number 存在merge是，指定父系分支号？这个还不怎么懂，暂时略过。
假设master分支上的提交记录如下：
A->B->C->D
目前HEAD指向commit D,我们要将代码revert到B提交时的状态

方法1
git revert C D
会生成2个新的commit分别覆盖C、D的提交
方法2
git revert -n C D
不会生成新的提交，但是回滚变动会作为修改变动添加到了索引区，可以直接调用git commit保存或者git revert --conitnue弹出commit页面

方法3
git revert -n C..D  //git revert C..D
类似方法1，revert从C到D之间的提交，假设中间还有很多提交时可以用这种

作者：顾小浪
链接：https://www.jianshu.com/p/7e513b302d47
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


http://zhaojunde1976.blog.163.com/blog/static/12199866820136119201752/

git中的后悔方法: rebase, revert, reset
 
如果git中提交了错误代码,怎么办？有三种选择 rebase, revert, reset
  
revert 用于直接取消指定某一次的提交,并且会形成两个历史记录,例如

git revert 5962845b0059f9e7702b73066e6a35aea1efaa49

这个命令取消了指定的提交内容,并且在当前的head后面增加了一次恢复注释

git log
  
Revert "Change version to 0.2"
  
This reverts commit 5962845b0059f9e7702b73066e6a35aea1efaa49.

reset 可以回滚到某一次提交,而该提交之后的所有修改都会丢失,常用的方法是

git reset -hard head~3

rebase 更高级,可以重写所有的信息,不过据说也很危险,还没有真正用过,用到的时候在补充吧。

>https://www.jianshu.com/p/7e513b302d47
