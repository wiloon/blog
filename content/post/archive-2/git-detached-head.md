---
title: Git detached HEAD
author: "-"
date: 2018-08-03T02:51:50+00:00
url: /?p=12482
categories:
  - git
tags:
  - reprint
---
## Git detached HEAD

git checkout本质上是修改HEAD里面的内容来让它指向不同分支的,而HEAD文件指向的分支就是我们当前的分支,但是有时候HEAD不会指向任何分支,严谨的说是HEAD指向了一个没有分支名字的修订版本,此时恭喜你,已经处于游离状态了(detached HEAD).这时候我们在进行commit操作不会提交到任何分支上去.

这个时候输入git status查看当前状态发现我没有在任何本地分支上也验证了刚才的猜想,而这时候我又作死的进行了commit操作,git提示我

使用的是 git checkout < commit id>,即切换到指定的某一次提交,HEAD 就会处于 detached 状态 (游离状态) 。
HEAD 游离状态的利与弊
HEAD 处于游离状态时,我们可以很方便地在历史版本之间互相切换,比如需要回到某次提交,直接 checkout 对应的 commit id 或者 tag 名即可。

它的弊端就是: 在这个基础上的提交会新开一个匿名分支！
也就是说我们的提交是无法可见保存的,一旦切到别的分支,游离状态以后的提交就不可追溯了。
解决办法就是新建一个分支保存游离状态后的提交:

detached head,即游离的HEAD,HEAD指向了未知的分支,即不在所有已知的分支范围内。

上网看了些资料, 道友们是遇到这样的问题然后解决了,但是出于好奇心来了解的我并没有这样的问题,但是仍然按照道友的解决顺序尝试了下,发现执行下面这句代码git checkout origin/master,会产生detached HEAD这种情况.

$ git checkout origin/master
  
Note: checking out 'origin/master'.

You are in 'detached HEAD' state. You can look around, make experimental changes and commit them, and you can discard any commits you make in this state without impacting any branches by performing another checkout. If you want to create a new branch to retain commits you create, you may do so (now or later) by using -b with the checkout command again. Example:

```bash
git checkout -b <new-branch-name>
# HEAD is now at 3e74a7a... merge bug fixed in issue1
```
  
此时用status指令查看,工作目录是干净的。

$ git status
  
HEAD detached at origin/master
  
nothing to commit, working tree clean
  
用git branch 可以查看到:

$ git branch
  
* (HEAD detached at origin/master)

dev

master
  
HEAD 指向了一个未知的分支,再返回上面的提示,可以用 git checkout -b 基于当前分支创建一个新的临时分支保留代码,合并到合适的分支后删除。

$ git checkout -b temp
  
Switched to a new branch 'temp'
  
$ git branch

dev

master
  
* temp
  
$ git checkout master
  
Switched to branch 'master'
  
Your branch is up-to-date with 'origin/master'.
  
$ git merge temp
  
Already up-to-date.
  
$ git branch -d temp
  
Deleted branch temp (was 3e74a7a).
  
但是与道友不同的是,使用 git checkout origin/master制造的detached HEAD的情况,再次使用切换分支就会消失:

$ git checkout master //master或者任意已知分支
  
$ git checkout dev
  
Previous HEAD position was 3e74a7a... merge bug fixed in issue1
  
Switched to branch 'dev'
  
Your branch is up-to-date with 'origin/dev'.
  
$ git branch
  
* dev

master

<https://blog.csdn.net/sinat_26415011/article/details/54346318>
