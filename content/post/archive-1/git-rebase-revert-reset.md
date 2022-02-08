---
title: git rebase,revert,reset
author: "-"
date: 2014-08-07T01:47:09+00:00
url: git/revert
categories:
  - Git
tags:
  - Git

---
## git rebase,revert,reset
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
--edit or --no-edit 是否弹出commit message窗口
**-n **是 --no-commit 的缩写
-m parent-number 存在merge是，指定父系分支号？这个还不怎么懂，暂时略过。

假设 master 分支上的提交记录如下：
A->B->C->D
目前HEAD指向commit D,我们要将代码revert到B提交时的状态

方法1
git revert C D
会生成2个新的commit分别覆盖C、D的提交
方法2
git revert -n C D
不会生成新的提交，但是回滚变动会作为修改变动添加到了索引区，可以直接调用 git commit 保存或者 git revert --conitnue 弹出 commit 页面

方法3
git revert -n C..D  //git revert C..D
类似方法1，revert从C到D之间的提交，假设中间还有很多提交时可以用这种

### git reset

    git reset [-q] [<tree-ish>] [--] <paths>…​
    git reset (--patch | -p) [<tree-ish>] [--] [<paths>…​]
    EXPERIMENTAL: git reset [-q] [--stdin [-z]] [<tree-ish>]
    git reset [--soft | --mixed [-N] | --hard | --merge | --keep] [-q] [<commit>]

回退HEAD到某一个<commit>
git reset <paths>
这是git add <paths> 的反向用法。

git add <paths> 是将修改后的文件添加到暂存区。
git reset <paths> 则是将暂存区内的文件移出。如果没有指定路径文件，则会将暂存区内修改的文件全部移出。

假设master分支上的提交记录如下：
A->B->C->D
目前HEAD指向commit D,我们要将代码回退到B提交时的状态

方法1
git reset --soft B 
这个时候可以发现，C,D两次提交做的修改依然存在，并且在索引区内，这个时候如果直接调用git commit ，可以生成一个新的提交E,E包含C、D两次提 交的修改。

### mixed
    git reset --mixed B   
    # 二者是一样的  
    git reset B

这个时候可以发现，C,D两次提交做的修改依然存在，但是不在索引区内，，记如果需要重新提交，则需要先调用git add。

### hard
git reset --hard B
和--soft、--mixed不同的是，C,D两次提交做的修改以及D以后做的一些没有提交的修改都不复存在

--merge说明
这个参数使用的有一定的前提，需要保证没有添加到索引区的修改文件在新旧两个HEAD直接的提交中没有过修改。如果下面命令调用成功
git reset --merge B
则会保留没有添加到索引区的修改。即，假设commit C 和 commit D都只修改了a.txt,而在D后我们又修改了b.txt,但是没有调用git add b.txt保存修改到索引区，则调用git reset --merge B 成功后，原来对b.txt做的修改还会存在，但是C、D提交中的修改将会回滚消失

--keep说明
和--merge有一些类似。使用成功的前提是：在D后有本地修改的文件在C、D两次提交中没有修改过，即C、D两次提交中没有它的修改记录。
假设我们在D后修改了a.txt文件，而且C、D两次提交中我们都没有修改a.txt文件，这样我们调用git reset --keep B 可以成功，并且a.txt文件中的修改依然会保留。

### git rebase
动词一共有如下几个：

- edit
- reword
- drop
- squash
- fixup

#### edit
edit命令表示你告诉了rebase，当在应用这个 commit 的时候，停下来，等待你修改了文件 和/或 修改了commit message之后在继续进行rebase。

上面说的很不好理解，建议自己尝试一下，就明白了。总之这个命令可以让你既能修改文件，又能修改commit message

#### reword
reword命令可以让你修改commit message。当你使用这个命令后，保存这个文件并退出，执行git rebase continue命令之后会再次打开一个文件，让你对这个commit的commit message进行修改，再次保存退出之后继续进行rebase

#### drop
drop命令表示你要丢弃这个commit以及它的修改。同样可以删除这一行来表示。（在git比较低的版本中，比如我使用的1.9.0版本中，只能通过删除那一行的方式来做，不支持drop命令）

#### squash 和 fixup
这两个命令都是用来将几个commit合并为一个的。其中，fixup命令，rebase的时候将会直接忽略掉它的commit message，而 squash 命令，则会在git rebase --continue之后打开一个文件，该文件中将会出现所有设置为squash的commit，这时删除掉多余的commit message，留下（或者修改）一行作为合并之后的commit的commit message。

到此为止，讲这个文件保存并退出，输入git status查看需要进行什么操作（比如需要解决冲突），之后执行git rebase --continue即可。

执行之后会根据你使用的命令的不同进行不同的操作，比如有的可以直接rebase有的则会打开一个文件让你进行一些操作，具体信息见上面的描述。

---


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

>https://www.jianshu.com/p/7e513b302d47
>https://swumao.github.io/swumao/update/git/rebase/pick/edit/reword/drop/squash/fixup/2016/08/31/Git-rebase-%E5%90%88%E5%B9%B6%E5%A4%9A%E4%B8%AAcommit.html
