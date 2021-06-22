---
title: Git——detached HEAD
author: "-"
type: post
date: 2018-08-03T02:51:50+00:00
url: /?p=12482
categories:
  - Uncategorized

---
在学习git的过程中，有些blog提到这种detached HEAD情况，处于好奇，去搜索了相关的文章查看这种情况的具体表现，以及解决方案，在这里作个总结。

detached head，即游离的HEAD，HEAD指向了未知的分支，即不在所有已知的分支范围内。

detached HEAD 具体示意图是这样:(网络图片)
  
这里写图片描述
  
上网看了些资料，道友们是遇到这样的问题然后解决了，但是出于好奇心来了解的我并没有这样的问题，但是仍然按照道友的解决顺序尝试了下，发现执行下面这句代码git checkout origin/master，会产生detached HEAD这种情况.

$ git checkout origin/master
  
Note: checking out 'origin/master'.

You are in 'detached HEAD' state. You can look around, make experimental
  
changes and commit them, and you can discard any commits you make in this
  
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
  
do so (now or later) by using -b with the checkout command again. Example:

git checkout -b <new-branch-name>

HEAD is now at 3e74a7a... merge bug fixed in issue1
  
此时用status指令查看，工作目录是干净的。

$ git status
  
HEAD detached at origin/master
  
nothing to commit, working tree clean
  
用git branch 可以查看到:

$ git branch
  
* (HEAD detached at origin/master)
    
dev
    
master
  
HEAD指向了一个未知的分支，再返回上面的提示，可以用 git checkout -b 基于当前分支创建一个新的临时分支保留代码，合并到合适的分支后删除。

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
  
但是与道友不同的是，使用 git checkout origin/master制造的detached HEAD的情况，再次使用切换分支就会消失: 

$ git checkout master //master或者任意已知分支
  
$ git checkout dev
  
Previous HEAD position was 3e74a7a... merge bug fixed in issue1
  
Switched to branch 'dev'
  
Your branch is up-to-date with 'origin/dev'.
  
$ git branch
  
* dev
    
master

https://blog.csdn.net/sinat_26415011/article/details/54346318