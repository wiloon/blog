---
title: git basic, command
author: wiloon
date: 2011-05-28T13:01:51.000+00:00
url: "/?p=202"
tags:
- Git

---

### 放弃本地未提交的修改
To discard all local changes, you do not use revert. revert is for reverting commits. Instead, do:

```bash
git reset --hard
```

### 指定克隆深度

在git clone时加上--depth=1

depth用于指定克隆深度，为1即表示只克隆最近一次commit.

git checkout master

### git config

#### 查看 
config 配置有system级别 global（用户级别） 和local（当前仓库）三个 设置先从system-》global-》local  底层配置会覆盖顶层配置 分别使用--system/global/local 可以定位到配置文件

    git config --system --list

查看当前用户（global）配置

    git config --global  --list

查看当前仓库配置信息

    git config --local  --list

#### 设置
    #设置电子邮件地址
    # global
    git config --global user.name "name0"
    git config --global user.email "email@example.com"

    # local
    git config --local user.email "email@example.com"
    git config --local user.name "name0"
    
    #确认在 Git 中正确设置了电子邮件地址
    git config --global user.email
    git config --local  user.email

### git reset

git reset ** file0

# 彻底回退到某个版本，本地的源码也会变成为上一个版本的内容

    git reset -hard file0

    git reset -mixed：此为默认方式，不带任何参数的git reset，这种方式，它回退到某个版本，只保留源码，回退commit和index信息
    git reset -soft:回退到某个版本，只回退了commit的信息，不会恢复到index file一级。如果还要提交，直接commit即可

```

### git log

git log file0
git log -3 file0
git log --oneline

echo "# project name" >> README.md

# 初始化的 Git 仓库

git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:wiloon/go-angular-x.git
git push -u origin master
```

### tag
```bash
#list tags
git tag

# add a tag
git tag v1.0.0

# commit tag
git push origin v1.0.0

# delete tag
git tag -d 1.0.0

# delete remote tag

git push origin :refs/tags/1.0.0

```

```bash
git rm
git rm -f
```

git fetch 命令通常用来查看其他人的进程，因为它取回的代码对你本地的开发代码没有影响。

默认情况下，git fetch取回所有分支（branch）的更新。如果只想取回特定分支的更新，可以指定分支名。

$ git fetch <远程主机名> <分支名>

比如，取回origin主机的master分支。

$ git fetch origin master

```bash
# 查看远程仓库地址
git remote -v

man git-fetch
git fetch --prune  #在本地删除在远程不存在的branch
git fetch --all 告诉 Git 同步所有的远端仓库。

# checkout tag

git checkout tag_name

#git分析指定的tag标签创建分支的命令
git checkout -b branch_name tag_name

# 新建分支

git branch iss53

# 切换到分支

git checkout iss53

# 新建并切换到分支

git checkout -b branch0
\#删除分支
git branch -d branch0
\#分支合并
git merge branch1

\#查看本地所有分支
git branch

\#查看远程所有分支
git branch -r

\#查看所有的分支
git branch -a

git branch -d -r origin/todo  #删除远程的todo branch
git log
git reflog
git log --pretty=oneline

git-ls-files  # - Show information about files in the index and the working tree

# list deleted files

git ls-files -d

# 恢复已删除的文件

git ls-files -d | xargs git checkout --

```

```bash
#checkout tag/branch
git clone -b v1.30.0 https://github.com/foo/bar
git clone --branch <tag_name> <repo_url>

git clean -fd

\#rebase
git rebase

git stash

$ git push origin test:master // 提交本地test分支作为远程的master分支 //好像只写这一句，远程的github就会自动创建一个test分支
$ git push origin test:test // 提交本地test分支作为远程的test分支

# 删除远程分支：

git push --delete origin devel
To git@github.com:zrong/quick-cocos2d-x.git - \[deleted\] devel

# git pull命令的作用是，取回远程主机某个分支的更新，再与本地的指定分支合并。它的完整格式稍稍有点复杂。

$ git pull origin other-branch

git status -s
git add .

git rm
git tm -rf

git commit -m "***"
git push git@localhost:ET.git master

git clone git@DomainName:ET.git
\#need port 22

git commit -m "xxx"
git push origin master

恢复一个文件"hello.rb",
$ git checkout -- hello.rb
git log master..origin/master
```

git am –show-current-patch

http://zensheno.blog.51cto.com/2712776/490748

http://blog.csdn.net/ithomer/article/details/7529841

http://www.cnblogs.com/springbarley/archive/2012/11/03/2752984.html

http://git-scm.com/book/zh/v1/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6

http://yijiebuyi.com/blog/eacf4d053fad77affffae397d9af7172.html

http://www.ruanyifeng.com/blog/2014/06/git_remote.html