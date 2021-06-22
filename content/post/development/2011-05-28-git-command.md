---
title: git basic, command
author: "-"
date: 2011-05-28T13:01:51.000+00:00
url: "/?p=202"
tags:
- Git

---
### 设置默认的分支名
    git config --global init.defaultBranch <name>
    git config --global init.defaultBranch main
    # The just-created branch can be renamed via this command
    git branch -m main

### 指定ssh 私钥
    GIT_SSH_COMMAND="ssh -i ~/tmp/id_rsa" git clone git@github.com:wiloon/foo.git

### 打印当前版本
    git rev-parse HEAD
### checkout 指定版本
    git checkout 788258e49531eb24bfd347a600d69a16f966c495

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
    
    git config --list
    git config --system --list
    git config --global core.editor vim

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

彻底回退到某个版本，本地的源码也会变成为上一个版本的内容

    git reset -hard file0

    git reset -mixed：此为默认方式，不带任何参数的git reset，这种方式，它回退到某个版本，只保留源码，回退commit和index信息
    git reset -soft:回退到某个版本，只回退了commit的信息，不会恢复到index file一级。如果还要提交，直接commit即可

### git log

git log file0
git log -3 file0
git log --oneline

echo "# project name" >> README.md

### 初始化的 Git 仓库

git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:wiloon/go-angular-x.git
git push -u origin master

### tag
```bash
#list local tags
git tag

# list remote tags
git ls-remote --tags origin

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

### git fetch
git fetch 命令通常用来查看其他人的进程，因为它取回的代码对你本地的开发代码没有影响。 
默认情况下，git fetch取回所有分支（branch）的更新。如果只想取回特定分支的更新，可以指定分支名。  

    git fetch <远程主机名> <分支名>

比如，取回origin主机的master分支。

    git fetch origin master

### git fetch与git pull
git fetch和git pull都可以将远端仓库更新至本地那么他们之间有何区别?想要弄清楚这个问题有有几个概念不得不提。

FETCH_HEAD： 是一个版本链接，记录在本地的一个文件中，指向着目前已经从远程仓库取下来的分支的末端版本。
commit-id：在每次本地工作完成后，都会做一个git commit 操作来保存当前工作到本地的repo， 此时会产生一个commit-id，这是一个能唯一标识一个版本的序列号。 在使用git push后，这个序列号还会同步到远程仓库。

有了以上的概念再来说说git fetch
git fetch：这将更新git remote 中所有的远程仓库所包含分支的最新commit-id, 将其记录到.git/FETCH_HEAD文件中
git fetch更新远程仓库的方式如下：

git fetch origin master:tmp 
//在本地新建一个temp分支，并将远程origin仓库的master分支代码下载到本地temp分支
git diff tmp 
//来比较本地代码与刚刚从远程下载下来的代码的区别
git merge tmp
//合并temp分支到本地的master分支
git branch -d temp
//如果不想保留temp分支 可以用这步删除

（1）如果直接使用git fetch，则步骤如下：

创建并更新本 地远程分支。即创建并更新origin/xxx 分支，拉取代码到origin/xxx分支上。
在FETCH_HEAD中设定当前分支-origin/当前分支对应，如直接到时候git merge就可以将origin/abc合并到abc分支上。
（2）git fetch origin
只是手动指定了要fetch的remote。在不指定分支时通常默认为master
（3）git fetch origin dev
指定远程remote和FETCH_HEAD，并且只拉取该分支的提交。

git pull : 首先，基于本地的FETCH_HEAD记录，比对本地的FETCH_HEAD记录与远程仓库的版本号，然后git fetch 获得当前指向的远程分支的后续版本的数据，然后再利用git merge将其与本地的当前分支合并。所以可以认为git pull是git fetch和git merge两个步骤的结合。
git pull的用法如下：

git pull <远程主机名> <远程分支名>:<本地分支名>
//取回远程主机某个分支的更新，再与本地的指定分支合并。
1
2
因此，与git pull相比git fetch相当于是从远程获取最新版本到本地，但不会自动merge。如果需要有选择的合并git fetch是更好的选择。效果相同时git pull将更为快捷。
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
```
### 分支, branch
最新版本的Git提供了新的git switch命令来切换分支, 使用新的git switch命令，比git checkout要更容易理解。
### 打印当前分支名
    git symbolic-ref --short HEAD  
#### 查看本地所有分支, 当前分支前面会标一个*号。
    git branch
    # check branch detail
    git branch -v
#### 查看远程所有分支
    git branch -r 
#### 查看所有的分支    
    git branch -a
#### 新建分支
    git branch branch0
#### 切换到分支
    git checkout branch0
    git switch branch0
#### 新建并切换到分支
    git checkout -b branch0
    git switch -c dev
#### 删除分支
    git branch -d branch0
#### #删除远程的todo branch
    git branch -d -r origin/todo
#### 分支合并, git merge命令用于合并指定分支到当前分支。
    git merge branch1 -m "MSG0"

### 本地分支重命名(还没有推送到远程)
    git branch -m oldName newName

### git pull
    git pull
    git pull origin branch0
    git pull origin master


```

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
git clone --branch <tag_name> <repo_url>
git clone -b dev_jk http://10.1.1.11/service/tmall-service.git
git clone -b v1.30.0 https://github.com/foo/bar


git clean -fd

#rebase
git rebase

git stash

$ git push origin test:master // 提交本地test分支作为远程的master分支 //好像只写这一句，远程的github就会自动创建一个test分支
$ git push origin test:test // 提交本地test分支作为远程的test分支

# 删除远程分支：

git push --delete origin devel
To git@github.com:zrong/quick-cocos2d-x.git - [deleted] devel

# git pull命令的作用是，取回远程主机某个分支的更新，再与本地的指定分支合并。它的完整格式稍稍有点复杂。

$ git pull origin other-branch

git status -s
git add .

git rm
git tm -rf

git commit -m "***"
git push git@localhost:ET.git master

git clone git@DomainName:ET.git
#need port 22

git commit -m "xxx"
git push origin master

恢复一个文件"hello.rb",
$ git checkout -- hello.rb
git log master..origin/master
```

git am –show-current-patch


### core.autocrlf
core.autocrlf配置
假如你正在Windows上写程序，又或者你正在和其他人合作，他们在Windows上编程，而你却在其他系统上，在这些情况下，你可能会遇到行尾结束符问题。这是因为Windows使用回车和换行两个字符来结束一行，而Mac和Linux只使用换行一个字符。虽然这是小问题，但它会极大地扰乱跨平台协作。

Git可以在你提交时自动地把行结束符CRLF转换成LF，而在签出代码时把LF转换成CRLF。用core.autocrlf来打开此项功能，如果是在Windows系统上，把它设置成true，这样当签出代码时，LF会被转换成CRLF:
$ git config --global core.autocrlf true
Linux或Mac系统使用LF作为行结束符，因此你不想 Git 在签出文件时进行自动的转换；当一个以CRLF为行结束符的文件不小心被引入时你肯定想进行修正，把core.autocrlf设置成input来告诉 Git 在提交时把CRLF转换成LF，签出时不转换：
$ git config --global core.autocrlf input
这样会在Windows系统上的签出文件中保留CRLF，会在Mac和Linux系统上，包括仓库中保留LF。

如果你是Windows程序员，且正在开发仅运行在Windows上的项目，可以设置false取消此功能，把回车符记录在库中：

$ git config --global core.autocrlf false
 

---

http://zensheno.blog.51cto.com/2712776/490748  
http://blog.csdn.net/ithomer/article/details/7529841  
http://www.cnblogs.com/springbarley/archive/2012/11/03/2752984.html  
http://git-scm.com/book/zh/v1/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6  
http://yijiebuyi.com/blog/eacf4d053fad77affffae397d9af7172.html  
http://www.ruanyifeng.com/blog/2014/06/git_remote.html  
https://www.liaoxuefeng.com/wiki/896043488029600/900003767775424  
https://blog.csdn.net/riddle1981/article/details/74938111  
https://blog.csdn.net/SCHOLAR_II/article/details/72191042  
https://www.jianshu.com/p/38f04aef1c9d