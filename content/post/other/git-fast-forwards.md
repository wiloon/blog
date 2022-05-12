---
title: git fast-forwards
author: "-"
date: 2012-07-04T10:06:20+00:00
url: git/fast-forward
categories:
  - Git
tags:
  - reprint
---
## git fast-forwards
### git pull
拉取最新代码,合并,解决冲突之后再提交
### git push -f
git push -f 强制覆盖到仓库，这会导致仓库中某些记录丢失。

### git rebase origin/master
表示将本地所有 commit 排在仓库 的 commit 记录之后。然后向仓库的 push 就会被接受。