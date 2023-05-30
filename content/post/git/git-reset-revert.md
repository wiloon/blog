---
title: "git reset"
author: "-"
date: "2022-08-17 11:35:15"
url: "git/reset"
categories:
  - "Git"
tags:
  - "reprint"
  - "remix"
---
## git reset

```bash
# reset 最近一次 commit
git reset --hard HEAD^
git reset --hard HEAD~1

# reset 最近两次 commit
git reset --hard HEAD~2
# reset 到某一个 commit, 退到/进到 指定commit_id
git reset --hard commit_id

git reset --soft HEAD^
```

进行了错误的提交，但是还没有 push 到远程分支，想要撤销最近的几次提交 (commit)，可以使用 git reset –-soft/hard 命令。

git reset 并不会产生 commits (不是不会产生，而是会产生但是都是一样的）
git reset 可以看成不产生 commits，它只是改变了当前 HEAD 指向的 commits。

HEAD^ 的意思是最近一个 commit，也可以写成 HEAD~1, 如果撤回最近两次 commit 就是 HEAD~2

## git reset --hard

hard （修改版本库，修改暂存区，修改工作区）
--hard HEAD～1 (或是版本号) 意为将版本库回退 1 个版本，但是不仅仅是将本地版本库的头指针全部重置到指定版本，也会丢弃 `工作区` (撤销 git add .) 和 `暂存区` (撤销 commit) 的本次修改, 回退到上一次提交的状态.

```bash
git reset --hard HEAD~1 (或者版本号)
```

直接会改变本地源码，不仅仅指向变化了，代码也回到了那个版本时的代码

git commit --hard 是具有破坏性，是很危险的操作，它很容易导致数据丢失，如果我们真的进行了该操作想要找回丢失的数据，那么此时可以使用 git reflog 回到未来，找到丢失的commit。

### git reset --soft

soft （修改版本库，保留暂存区，保留工作区）
--soft HEAD～1 意为将版本库软回退1个版本，所谓软回退表示将本地版本库的头指针全部重置到指定版本，且将这次提交之后的所有变更都移动到暂存区。

从本地仓库 (Local Repository) 撤消 n 个 commit, 保留暂存区，保留工作区, 撤消了 commit 但是保留修改, 可以再次提交(commit).

前者表示只是改变了 HEAD 的指向，本地代码不会变化，我们使用 git status 依然可以看到，同时也可以 git commit 提交
不删除工作空间改动代码，撤销 commit，不撤销 `git add .`
--soft 这个版本的命令有 “最小” 影响，只改变一个符号引用的状态使其指向一个新提交，不会改变其索引和工作目录，

因为当前分支的版本低于远程分支的版本，所以要想覆盖掉它，必须使用force
git push origin 分支 --force ok，大功告成

### --mixed

意思是：不删除工作空间改动代码，撤销 commit，并且撤销 git add .
这个为默认参数, git reset --mixed HEAD^ 和 git reset HEAD^ 效果是一样的。

```bash
git push origin <分支名>
会提示本地的版本落后于远端的版本；
为覆盖掉远端的版本信息，使远端的仓库也回退相应版本，加上参数–force

git push origin <分支名> --force
```

```bash
# 按需选择想要回到哪个版本
# 回到HEAD
git reset --soft HEAD

# 回到HEAD的前一个版本
git reset --soft HEAD^

# 回到 HEAD 的前 5 个版本
git reset --soft HEAD~5

# 利用 commit id回到指定版本
git reset --soft a06ef2f

# 将撤销的代码暂存起来
git stash

# 切换到正确的分支
git checkout feat/xxx

# 重新应用缓存
git stash pop

# 在正确的分支进行提交操作
git add . && git commit -m "update xxxx"
```

git reset ** file0

彻底回退到某个版本，本地的源码也会变成为上一个版本的内容

```bash
git reset -hard file0

git reset -mixed: 此为默认方式，不带任何参数的 git reset，这种方式，它回退到某个版本，只保留源码，回退commit 和 index 信息
git reset -soft: 回退到某个版本，只回退了 commit 的信息，不会恢复到 index file 一级。如果还要提交，直接commit 即可

```

```bash
git reset --hard
```

```bash
git reset [-q] [<tree-ish>] [--] <paths>…​
git reset (--patch | -p) [<tree-ish>] [--] [<paths>…​]
EXPERIMENTAL: git reset [-q] [--stdin [-z]] [<tree-ish>]
git reset [--soft | --mixed [-N] | --hard | --merge | --keep] [-q] [<commit>]
```

回退HEAD到某一个`<commit>`
git reset `<paths>`
这是 git add `<paths>` 的反向用法。

git add `<paths>` 是将修改后的文件添加到暂存区。
git reset `<paths>` 则是将暂存区内的文件移出。如果没有指定路径文件，则会将暂存区内修改的文件全部移出。

假设master分支上的提交记录如下：
A->B->C->D
目前HEAD指向commit D,我们要将代码回退到B提交时的状态

方法1
git reset --soft B
这个时候可以发现，C,D两次提交做的修改依然存在，并且在索引区内，这个时候如果直接调用git commit ，可以生成一个新的提交E,E包含C、D两次提 交的修改。

### mixed

```bash
git reset --mixed B
# 二者是一样的
git reset B
```

这个时候可以发现，C,D 两次提交做的修改依然存在，但是不在索引区内，，记如果需要重新提交，则需要先调用git add。

### hard

git reset --hard B
和--soft、--mixed不同的是，C,D两次提交做的修改以及D以后做的一些没有提交的修改都不复存在

--merge说明
这个参数使用的有一定的前提，需要保证没有添加到索引区的修改文件在新旧两个HEAD直接的提交中没有过修改。如果下面命令调用成功
git reset --merge B
则会保留没有添加到索引区的修改。即，假设commit C 和 commit D都只修改了a.txt,而在D后我们又修改了b.txt,但是没有调用git add b.txt保存修改到索引区，则调用git reset --merge B 成功后，原来对b.txt做的修改还会存在，但是C、D提交中的修改将会回滚消失

--keep 说明
和 --merge 有一些类似。使用成功的前提是：在 D 后有本地修改的文件在 C、D 两次提交中没有修改过，即 C、D 两次提交中没有它的修改记录。
假设我们在D后修改了 a.txt 文件，而且 C、D 两次提交中我们都没有修改 a.txt 文件，这样我们调用 git reset --keep B 可以成功，并且a.txt文件中的修改依然会保留。

## git checkout, revert, reset, 回退, 撤消

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
git reset --soft xx 版本号 xxxx 
git reset --hard xx 版本号 xxx
git reset --soft HEAD~1
git reset --hard HEAD~1
git reset --hard HEAD^ 回退到上 1 个版本
git reset --hard commit_id 退到/进到 指定commit_id

# 简洁显示日志记录
git log --pretty=oneline
git log --oneline --graph -4 --decorate
```

### git revert

git revert 也是撤销命令，区别在于 reset 是指向原地或者向前移动指针，git revert 是创建一个 commit 来回滚当前的 commit，指针向后移动。

放弃一个或多个提交，并生成一个或多个新的提交来记录这些放弃操作。

### git reset 和 git revert 的区别

1. git revert 是用一次新的 commit 来回滚之前的 commit，git reset 是直接删除指定的 commit。
2. 在回滚这一操作上看，效果差不多。但是在日后继续 merge 以前的老版本时有区别。因为 git revert 是用一次逆向的 commit“中和”之前的提交，因此日后合并老的 branch 时，导致这部分改变不会再次出现，但是 git reset 是之间把某些 commit 在某个branch 上删除，因而和老的 branch 再次 merge 时，这些被回滚的 commit 应该还会被引入。
3. git reset 是把 HEAD 向后移动了一下，而 git revert 是 HEAD 继续前进，只是新的 commit 的内容和要 revert 的内容正好相反，能够抵消要被 revert 的内容。

### ps: 如何删除已经 push 的 idea 等不想要的文件?

第一步: 配置好 .gitignore 文件, 把 idea 加进去
第二步: `git rm -r --cached .` (不要忘记点哦~)
第三步: git add .(不要忘记点哦~)
第四部: git commit -m "这里是备注"
第五步: git push
大功告成

#### 撤销前一次 commit

```bash
git revert HEAD
```

#### 撤销前前一次 commit

```bash
git revert HEAD^
```

#### 撤销指定的版本，撤销也会作为一次提交进行保存

```bash
# revert commit id: 4945db2
git revert 4945db2
git revert
git revert [--[no-]edit] [-n] [-m parent-number] [-s] [-S[<keyid>]] <commit>…​
git revert --continue
git revert --quit
git revert --abort
```

```bash
git revert [--[no-]edit] [-n] [-m parent-number] [-s] [-S[<keyid>]] <commit>…​
```

--edit or --no-edit 是否弹出 commit message 窗口
**-n** 是 --no-commit 的缩写
-m parent-number 存在 merge 是，指定父系分支号？这个还不怎么懂，暂时略过。

假设 master 分支上的提交记录如下：
A->B->C->D
目前HEAD指向 commit D, 我们要将代码 rever t到 B 提交时的状态

方法1
git revert C D
会生成2个新的commit分别覆盖C、D的提交
方法2
git revert -n C D
不会生成新的提交，但是回滚变动会作为修改变动添加到了索引区，可以直接调用 git commit 保存或者 git revert --conitnue 弹出 commit 页面

方法3
git revert -n C..D  //git revert C..D
类似方法1，revert从C到D之间的提交，假设中间还有很多提交时可以用这种

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

作者：jrg陈咪咪sunny
链接：<https://www.jianshu.com/p/952d83fc5bc8>
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

作者：鹅鹅鹅曲项向天歌呀
链接：<https://www.jianshu.com/p/491a14d414f6>
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
