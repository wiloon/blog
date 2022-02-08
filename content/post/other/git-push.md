---
title: git push 撤销
author: "-"
date: 2022-01-25 03:34:33
url: git/push
categories:
  - Git
tags:
  - Git

---
## git push 撤销
## git push
wiloon@debian:~/development/source/et$ git push
  
No refs in common and none specified; doing nothing.
  
Perhaps you should specify a branch such as 'master'.
  
fatal: The remote end hung up unexpectedly
  
error: failed to push some refs to 'gitolite@localhost:et'


should use.... git push origin master


### git push提交成功后如何撤销回退
```bash
git log
git reflog
# git reflog 可以查看所有分支的所有操作记录（包括（包括commit和reset的操作），包括已经被删除的commit记录，git log则不能察看已经删除了的commit记录。
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

#### git reset
git reset并不会产生commits（不是不会产生，而是会产生 但是都是一样的）
git reset可以看成不产生commits，它只是改变了当前HEAD指向的commits。

##### git reset --hard
--hard 参数会抛弃当前工作区的修改
删除工作空间改动代码，撤销commit，撤销git add .
注意完成这个操作后，就恢复到了上一次的commit状态。
```
git reset --hard 提交id
HEAD 指向 第五次,所以 reset 一下 HEAD 就好啦

```
直接会改变本地源码，不仅仅指向变化了，代码也回到了那个版本时的代码

git commit --hard 是具有破坏性，是很危险的操作，它很容易导致数据丢失，如果我们真的进行了该操作想要找回丢失的数据，那么此时可以使用git reflog 回到未来，找到丢失的commit。


#### git reset --soft
前者表示只是改变了HEAD的指向，本地代码不会变化，我们使用git status依然可以看到，同时也可以git commit提交
不删除工作空间改动代码，撤销commit，不撤销git add .
--soft 这个版本的命令有“最小”影响，只改变一个符号引用的状态使其指向一个新提交，不会改变其索引和工作目录，

因为当前分支的版本低于远程分支的版本，所以要想覆盖掉它，必须使用force
git push origin 分支 --force ok，大功告成
##### --mixed
意思是：不删除工作空间改动代码，撤销commit，并且撤销git add . 操作
这个为默认参数,git reset --mixed HEAD^ 和 git reset HEAD^ 效果是一样的。

```
git push origin <分支名>
会提示本地的版本落后于远端的版本；
 为覆盖掉远端的版本信息，使远端的仓库也回退相应版本，加上参数–force

git push origin <分支名> --force
```

```
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
### git revert


### git reset 和 git revert 的区别
1、git revert是用一次新的commit来 回滚之前的commit，git reset是直接 删除指定的commit。
2、在回滚这一操作上看，效果差不多。但是在日后继续merge以前的老版本时有区别。因为git revert是用一次逆向的commit“中和”之前的提交，因此日后合并老的branch时，导致这部分改变不会再次出现，但是git reset是之间把某些commit在某个branch上删除，因而和老的branch再次merge时，这些被回滚的commit应该还会被引入。
3、git reset 是把HEAD向后移动了一下，而git revert是HEAD继续前进，只是新的commit的内容和要revert的内容正好相反，能够抵消要被revert的内容。

作者：鹅鹅鹅曲项向天歌呀
链接：https://www.jianshu.com/p/491a14d414f6
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



### ps:如何删除已经push的idea等不想要的文件?
第一步:配置好.gitignore文件,把idea加进去
第二步:git rm -r --cached . (不要忘记点哦~)
第三步:git add .(不要忘记点哦~)
第四部:git commit -m "这里是备注"
第五步:git push
大功告成~~~

作者：鹅鹅鹅曲项向天歌呀
链接：https://www.jianshu.com/p/491a14d414f6
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
