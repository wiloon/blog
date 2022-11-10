---
title: git merge
author: "-"
date: 2018-08-03T02:49:34+00:00
url: /?p=12479
categories:
  - Inbox
tags:
  - reprint
---
### git merge, git rebase

## git merge

特点：自动创建一个新的 commit
如果合并的时候遇到冲突，仅需要修改后重新 commit
优点：记录了真实的 commit 情况，包括每个分支的详情
缺点：因为每次 merge 会自动产生一个 merge commit，所以在使用一些 git 的 GUI tools，特别是commit比较频繁时，看到分支很杂乱。

```bash
git merge b0
  
git status
  
git mergetool
  
#"The merge tool bc is not available as" 'bcompare'
  
git config -global merge.tool vimdiff

:diffg RE " get from REMOTE
  
:diffg BA " get from BASE
  
:diffg LO " get from LOCAL
  
:wqa
  
```

### 把 master merge 到 feature 上

```bash
git checkout feature
git merge master
# 或者
git merge master feature
```

#### git rebase

rebase 特点：会合并之前的 commit 历史
优点：得到更简洁的项目历史，去掉了 merge commit
缺点：如果合并出现代码问题不容易定位，因为 re-write 了 history

作者：AlvinStar
链接：<https://www.jianshu.com/p/f23f72251abc>
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

### rebase 做了什么

#### 场景：分支合并

从 master 分支切出一个 dev 分支 (feature1)，进行开发
再执行 git rebase master
首先，git 会把 feature1 分支里面的每个 commit 取消掉；
其次，把上面的操作临时保存成 patch 文件，存在 .git/rebase 目录下；
然后，把 feature1 分支更新到最新的 master 分支；
最后，把上面保存的 patch 文件应用到 feature1 分支上；


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

<https://git-scm.com/book/zh/v1/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6>
  
<http://blog.hanghu.me/git/2017/03/08/The-merge-tool-bc-is-not-available-as-bcompare.html>
  
<http://www.rosipov.com/blog/use-vimdiff-as-git-mergetool/>
