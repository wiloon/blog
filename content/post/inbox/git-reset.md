---
title: "git reset"
author: "-"
date: "2022-08-17 11:35:15"
url: ""
categories:
  - "Git"
tags:
  - "Inbox"
  - "reprint"
  - "remix"
---
## git reset

git reset 并不会产生 commits (不是不会产生，而是会产生但是都是一样的）
git reset 可以看成不产生 commits，它只是改变了当前HEAD 指向的 commits。

HEAD^ 的意思是上一个版本，也可以写成HEAD~1

如果你进行了2次commit，想都撤回，可以使用HEAD~2

## git reset --hard

--hard 参数 会抛弃当前工作区的修改
删除工作空间改动代码，撤销 commit，撤销 git add .
注意完成这个操作后，就恢复到了上一次的 commit 状态。

```bash
git reset --hard 提交id
# HEAD 指向 第五次, 所以 reset 一下 HEAD 就好啦
```

直接会改变本地源码，不仅仅指向变化了，代码也回到了那个版本时的代码

git commit --hard 是具有破坏性，是很危险的操作，它很容易导致数据丢失，如果我们真的进行了该操作想要找回丢失的数据，那么此时可以使用 git reflog 回到未来，找到丢失的commit。

### git reset --soft

前者表示只是改变了 HEAD 的指向，本地代码不会变化，我们使用 git status 依然可以看到，同时也可以 git commit 提交
不删除工作空间改动代码，撤销 commit，不撤销 `git add .`
--soft 这个版本的命令有“最小”影响，只改变一个符号引用的状态使其指向一个新提交，不会改变其索引和工作目录，

因为当前分支的版本低于远程分支的版本，所以要想覆盖掉它，必须使用force
git push origin 分支 --force ok，大功告成

### --mixed

意思是：不删除工作空间改动代码，撤销commit，并且撤销git add . 操作
这个为默认参数, git reset --mixed HEAD^ 和 git reset HEAD^ 效果是一样的。

```bash
git push origin <分支名>
会提示本地的版本落后于远端的版本；
为覆盖掉远端的版本信息，使远端的仓库也回退相应版本，加上参数–force

git push origin <分支名> --force
```

```bash
# 将该分支的本不应该提交的commit撤销
git reset HEAD^

# 按需选择想要回到哪个版本
# 回到HEAD
git reset --soft HEAD

# 回到HEAD的前一个版本
git reset --soft HEAD^

# 回到HEAD的前10个版本
git reset --soft HEAD~5 

# 利用id回到指定版本
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

    git reset -hard file0

    git reset -mixed: 此为默认方式，不带任何参数的git reset，这种方式，它回退到某个版本，只保留源码，回退commit和index信息
    git reset -soft:回退到某个版本，只回退了commit的信息，不会恢复到index file一级。如果还要提交，直接commit即可

```bash
    git reset --hard
```

    git reset [-q] [<tree-ish>] [--] <paths>…​
    git reset (--patch | -p) [<tree-ish>] [--] [<paths>…​]
    EXPERIMENTAL: git reset [-q] [--stdin [-z]] [<tree-ish>]
    git reset [--soft | --mixed [-N] | --hard | --merge | --keep] [-q] [<commit>]

回退HEAD到某一个<commit>
git reset <paths>
这是 git add <paths> 的反向用法。

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
