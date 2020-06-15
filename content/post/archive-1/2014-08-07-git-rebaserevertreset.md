---
title: git rebase,revert,reset
author: wiloon
type: post
date: 2014-08-07T01:47:09+00:00
url: /?p=6897
categories:
  - Uncategorized
tags:
  - Git

---
http://zhaojunde1976.blog.163.com/blog/static/12199866820136119201752/

git中的后悔方法：rebase,revert,reset

2013-07-11 09:24:06| 分类： 技术 | 标签：git |举报|字号 订阅
  
如果git中提交了错误代码，怎么办？有三种选择 rebase, revert, reset
  
revert 用于直接取消指定某一次的提交，并且会形成两个历史记录，例如

git revert 5962845b0059f9e7702b73066e6a35aea1efaa49

这个命令取消了指定的提交内容，并且在当前的head后面增加了一次恢复注释

git log
  
Revert "Change version to 0.2"
  
This reverts commit 5962845b0059f9e7702b73066e6a35aea1efaa49.

reset 可以回滚到某一次提交，而该提交之后的所有修改都会丢失，常用的方法是

git reset &#8211;hard head~3

rebase 更高级，可以重写所有的信息，不过据说也很危险，还没有真正用过，用到的时候在补充吧。