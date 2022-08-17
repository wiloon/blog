---
title: git checkout, rebase, revert, reset, 回退, 撤消
author: "-"
date: 2022-01-25 03:34:33
url: git/push
categories:
  - Git
tags:
  - Git

---
## git checkout, rebase, revert, reset, 回退, 撤消

## 撤销本地修改

对文件的修改还没有提交, 撤消本地的修改, 已经 add/commit的不适用

```bash
git checkout .
```

回滚提示  
本地或者自己单独的仓库使用 reset 或者 revert 都可以  
涉及到远程仓库 (公用仓库）时，不要使用 reset, 而使用 revert 回滚  

### git push 提交成功后如何撤销/回退

```bash
git log
git reflog
# git reflog 可以查看所有分支的所有操作记录 (包括 (包括commit和reset的操作），包括已经被删除的commit记录，git log 则不能察看已经删除了的 commit 记录。
git reset --soft xx版本号xxxx 
git reset --hard xx版本号xxx
git reset --soft HEAD~1
git reset --hard HEAD~1
git reset --hard HEAD^ 回退到上个版本
git reset --hard commit_id 退到/进到 指定commit_id

#简洁显示日志记录
git log --pretty=oneline
git log --oneline --graph -4 --decorate
```

### git revert

放弃一个或多个提交，并生成一个或多个新的提交来记录这些放弃操作。

### git reset 和 git revert 的区别

1. git revert 是用一次新的 commit 来回滚之前的 commit，git reset 是直接删除指定的 commit。
2. 在回滚这一操作上看，效果差不多。但是在日后继续 merge 以前的老版本时有区别。因为 git revert 是用一次逆向的 commit“中和”之前的提交，因此日后合并老的 branch 时，导致这部分改变不会再次出现，但是 git reset 是之间把某些 commit 在某个branch 上删除，因而和老的 branch 再次 merge 时，这些被回滚的 commit 应该还会被引入。
3. git reset 是把 HEAD 向后移动了一下，而 git revert 是 HEAD 继续前进，只是新的 commit 的内容和要 revert 的内容正好相反，能够抵消要被 revert 的内容。

作者：鹅鹅鹅曲项向天歌呀
链接：<https://www.jianshu.com/p/491a14d414f6>
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

### ps: 如何删除已经 push 的 idea 等不想要的文件?

第一步:配置好.gitignore文件, 把idea加进去
第二步: `git rm -r --cached .` (不要忘记点哦~)
第三步: git add .(不要忘记点哦~)
第四部:git commit -m "这里是备注"
第五步:git push
大功告成~~~

作者：鹅鹅鹅曲项向天歌呀
链接：<https://www.jianshu.com/p/491a14d414f6>
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

#### 撤销前一次 commit

```bash
git revert HEAD
```

#### 撤销前前一次 commit

    git revert HEAD^

#### 撤销指定的版本，撤销也会作为一次提交进行保存

    git revert commit  (比如：fa042ce57ebbe5bb9c8db709f719cec2c58ee7ff）
    git revert
    git revert [--[no-]edit] [-n] [-m parent-number] [-s] [-S[<keyid>]] <commit>…​
    git revert --continue
    git revert --quit
    git revert --abort

git revert [--[no-]edit] [-n] [-m parent-number] [-s] [-S[<keyid>]] <commit>…​
--edit or --no-edit 是否弹出commit message窗口
**-n**是 --no-commit 的缩写
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

drop命令表示你要丢弃这个commit以及它的修改。同样可以删除这一行来表示。 (在git比较低的版本中，比如我使用的1.9.0版本中，只能通过删除那一行的方式来做，不支持drop命令）

#### squash 和 fixup

这两个命令都是用来将几个commit合并为一个的。其中，fixup命令，rebase的时候将会直接忽略掉它的commit message，而 squash 命令，则会在git rebase --continue之后打开一个文件，该文件中将会出现所有设置为squash的commit，这时删除掉多余的commit message，留下 (或者修改）一行作为合并之后的commit的commit message。

到此为止，讲这个文件保存并退出，输入git status查看需要进行什么操作 (比如需要解决冲突），之后执行git rebase --continue即可。

执行之后会根据你使用的命令的不同进行不同的操作，比如有的可以直接rebase有的则会打开一个文件让你进行一些操作，具体信息见上面的描述。

---

作者：顾小浪
链接：<https://www.jianshu.com/p/7e513b302d47>
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

<http://zhaojunde1976.blog.163.com/blog/static/12199866820136119201752/>

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

<https://www.jianshu.com/p/7e513b302d47>

<https://swumao.github.io/swumao/update/git/rebase/pick/edit/reword/drop/squash/fixup/2016/08/31/Git-rebase-%E5%90%88%E5%B9%B6%E5%A4%9A%E4%B8%AAcommit.html>
