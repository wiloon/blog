---
title: git checkout
author: "-"
type: post
date: 2011-11-09T03:32:44+00:00
url: /?p=1464
bot_views:
  - 12
categories:
  - VCS
tags:
  - Git

---
git checkout: Git的checkout有两个作用，其一是在不同的branch之间进行切换，例如'git checkout new_branch'就会切换到new_branch的分支上去；另一个功能是还原代码的作用，例如'git checkout app/model/user.rb'就会将user.rb文件从上一个已提交的版本中更新回来，未提交的内容全部会回滚

git checkout -f     //提取当前branch的所有文件．

git checkout HEAD . # 将所有代码都 checkout 出來(最后一次 commit 的版本), 注意, 若有修改的代码都会被还原到上一版. (git checkout -f 亦可)