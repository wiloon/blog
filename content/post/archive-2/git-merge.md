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
## git merge
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

### 把master merge到 feature上
    git checkout feature
    git merge master
    # 或者
    git merge master feature

### git merge, git rebase
#### git merge
特点：自动创建一个新的commit
如果合并的时候遇到冲突，仅需要修改后重新commit
优点：记录了真实的commit情况，包括每个分支的详情
缺点：因为每次merge会自动产生一个merge commit，所以在使用一些git 的GUI tools，特别是commit比较频繁时，看到分支很杂乱。

#### git rebase
rebase 特点：会合并之前的commit历史
优点：得到更简洁的项目历史，去掉了merge commit
缺点：如果合并出现代码问题不容易定位，因为re-write了history


作者：AlvinStar
链接：https://www.jianshu.com/p/f23f72251abc
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

https://git-scm.com/book/zh/v1/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6
  
http://blog.hanghu.me/git/2017/03/08/The-merge-tool-bc-is-not-available-as-bcompare.html
  
http://www.rosipov.com/blog/use-vimdiff-as-git-mergetool/