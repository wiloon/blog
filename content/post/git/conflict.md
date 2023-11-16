---
title: git 冲突解决, conflict, <<< === >>>
author: "-"
date: 2012-04-22T01:37:04+00:00
url: git/conflict
categories:
  - Git
tags:
  - reprint
---
## git 冲突解决, conflict, <<< === >>>

### 远程文件覆盖本地文件

git pull 出现冲突后丢弃本地冲突文件修改，采用远程文件覆盖本地文件

```bash
git checkout
git checkout test/src/main/resources/spring-shiro.xml  
```

### 方法二

git pull 出现冲突后可以暂存本地修改 git stash ,然后git pull 更新代码，git stash list 可查看暂存记录列表，释放本地暂存 git stash apply stash@{0} ，出现冲突文件，找到并解决，然后可以提交git add . 加入索引库，然后本地提交git commit -m '注释' 最后git push到远程

### 方法三

1.git pull

更新代码，发现

error: Your local changes to the following files would be overwritten by merge:pom.xml

Please commit your changes or stash them before you merge.
这说明你的pom.xml与远程有冲突，你需要先提交本地的修改然后更新。

2.git add pom.xml

```bash
git commit -m '冲突解决'
```

 提交本地的pom.xml文件，不进行推送远程

3.git pull

### 更新代码

Auto-merging pom.xml
CONFLICT (content): Merge conflict in pom.xml
Automatic merge failed; fix conflicts and then commit the result.
更新后你的本地分支上会出现 (develop|MERGING) 类似这种标志

找到你本地的文件，并打开

你会在文件中发现 `<<<<<<< HEAD`, `=======`, `>>>>>>> ae9a0f6b7e42fda2ce9b14a21a7a03cfc5344d61`

- `<<<<<<< HEAD` 和 `=======` 中间的是你自己的代码
- `=======`  和 `>>>>>>>` 中间的是其他人修改的代码

自己确定保留哪一部分代码，最后删除 `<<<<<<< HEAD, =======, >>>>>>>` 这种标志

```bash
git add pom.xml
git commit -m '冲突解决结束'
```

再次将本地的pom.xml文件提交

```bash
git push
```

将解决冲突后的文件推送到远程

版权声明：本文为CSDN博主「落日流年」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/zwl18210851801/article/details/79106448](https://blog.csdn.net/zwl18210851801/article/details/79106448)
