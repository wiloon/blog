---
title: git basic
author: "-"
date: 2011-05-28T13:01:51.000+00:00
url: "git/basic"
tags:
- Git

---
## git basic
### git add
git add 命令可将该文件添加到暂存区。

### config git editor
    git config --global core.editor vim
    export EDITOR=vim
### commit
#### 修改最近一次的 commit message
    git commit --amend
    git commit --amend -m "New commit message."

Rewriting the most recent commit message
You can change the most recent commit message using the git commit --amend command.

In Git, the text of the commit message is part of the commit. Changing the commit message will change the commit ID--i.e., the SHA1 checksum that names the commit. Effectively, you are creating a new commit that replaces the old one.

### 修改最近的第n次 commit message
    # 数字代表显示倒数第几次, #-i, --interactive
    git rebase -i HEAD~2
    # git log你可以发现，git的最后一次提交已经变成你选的那个了
    # 把pick 修改成edit然后保存退出，然后会看到提示 git commit --amend
    git commit --amend
    # 修改注释之后，保存退出，然后git rebase --continue
    git rebase --continue
    # 把本地仓库的代码推送到远程
    git push origin master
    # 修改了已经push的注释，得用强制push, force push对其它人有影响慎用.
    git push --force origin master

### git 清除所有被 Ignore 的文件
#### 查看所有被 Git 忽略的文件, Git 1.6+:
```bash
git ls-files --others -i --exclude-standard
```

#### Git 1.4, 1.5
```bash
git ls-files --others -i \
--exclude-from="`git rev-parse --git-dir`/info/exclude" \
--exclude-per-directory=.gitignore
```
#### 清除所有被 Git 忽略的文件或文件夹 (小心)
##### 查看在清理之前会做的操作
```bash
git clean -Xn
```
##### 清除文件或文件夹， -f 选项强制删除，-d 删除目录（小心）
```bash
git clean -Xdf
```

>https://ruby-china.org/topics/17951

## remote
### 查看远程仓库地址
    git remote -v

### 添加远程库
```bash
git remote add <主机名> <URL>
git remote add origin http://192.168.50.13:10880/wiloon/wiloon.com.git
# origin 是远程库的名字, 单个远程库,一般用默认的origin, 多个远程库的时候可以改成方便记忆的名字
git push -u origin master
```

### 删除远程库
    gitremote rm 仓库A

### 将指定的提交（commit) 应用于其他分支
    git cherry-pick <commitHash>

https://www.ruanyifeng.com/blog/2020/04/git-cherry-pick.html


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
git checkout . #本地所有修改的。没有的提交的，都返回到原来的状态
```
>https://blog.csdn.net/leedaning/article/details/51304690

### git reset

git reset ** file0

彻底回退到某个版本，本地的源码也会变成为上一个版本的内容

    git reset -hard file0

    git reset -mixed: 此为默认方式，不带任何参数的git reset，这种方式，它回退到某个版本，只保留源码，回退commit和index信息
    git reset -soft:回退到某个版本，只回退了commit的信息，不会恢复到index file一级。如果还要提交，直接commit即可

```bash
    git reset --hard
```

### 指定克隆深度

在git clone时加上--depth=1

depth用于指定克隆深度，为1即表示只克隆最近一次commit.

git checkout master

### git config
#### 查看 
config 配置有system级别 global（用户级别)  和local（当前仓库) 三个 设置先从system-》global-》local  底层配置会覆盖顶层配置 分别使用--system/global/local 可以定位到配置文件
    
    git config --list
    git config --system --list
    git config --global core.editor vim

查看当前用户（global) 配置

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

### git log
git log
git log file0
git log -3 file0
git log --oneline

echo "# project name" >> README.md

#### 更改最多的文件
git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -10

--pretty。 使用不同于默认格式的方式展示提交历史
format ，可以定制记录的显示格式。 --pretty=format:"%h - %an, %ar : %s"
--name-only参数仅显示受影响的文件名。如果你想看看每个文件发生了什么(删除，修改，添加)，请改用--name-status

### 初始化的 Git 仓库
git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:wiloon/go-angular-x.git
git push -u origin master

```bash
git rm
git rm -f
```

### git fetch
git fetch 命令通常用来查看其他人的进程，因为它取回的代码对你本地的开发代码没有影响。 
默认情况下，git fetch取回所有分支（branch) 的更新。如果只想取回特定分支的更新，可以指定分支名。  

    git fetch <远程主机名> <分支名>

比如，取回 origin 主机的 master 分支。

    git fetch origin master

### git fetch 与 git pull
git fetch 和 git pull 都可以将远端仓库更新至本地那么他们之间有何区别?想要弄清楚这个问题有有几个概念不得不提。

FETCH_HEAD: 是一个版本链接，记录在本地的一个文件中，指向着目前已经从远程仓库取下来的分支的末端版本。
commit-id: 在每次本地工作完成后，都会做一个git commit 操作来保存当前工作到本地的repo， 此时会产生一个commit-id，这是一个能唯一标识一个版本的序列号。 在使用git push后，这个序列号还会同步到远程仓库。

有了以上的概念再来说说 git fetch
git fetch: 这将更新 git remote 中所有的远程仓库所包含分支的最新 commit-id, 将其记录到.git/FETCH_HEAD 文件中
git fetch 更新远程仓库的方式如下: 

git fetch origin master: tmp 
//在本地新建一个temp分支，并将远程origin仓库的master分支代码下载到本地temp分支
git diff tmp 
//来比较本地代码与刚刚从远程下载下来的代码的区别
git merge tmp
//合并temp分支到本地的master分支
git branch -d temp
//如果不想保留temp分支 可以用这步删除

（1) 如果直接使用git fetch，则步骤如下: 

创建并更新本 地远程分支。即创建并更新origin/xxx 分支，拉取代码到origin/xxx分支上。
在FETCH_HEAD中设定当前分支-origin/当前分支对应，如直接到时候git merge就可以将origin/abc合并到abc分支上。
（2) git fetch origin
只是手动指定了要fetch的remote。在不指定分支时通常默认为master
（3) git fetch origin dev
指定远程remote和FETCH_HEAD，并且只拉取该分支的提交。

### git pull
git pull: 首先，基于本地的FETCH_HEAD记录，比对本地的FETCH_HEAD记录与远程仓库的版本号，然后git fetch 获得当前指向的远程分支的后续版本的数据，然后再利用git merge 将其与本地的当前分支合并。所以可以认为git pull是git fetch和git merge两个步骤的结合。
git pull的用法如下: 

git pull <远程主机名> <远程分支名>:<本地分支名>
//取回远程主机某个分支的更新，再与本地的指定分支合并。

因此，与git pull相比git fetch相当于是从远程获取最新版本到本地，但不会自动merge。如果需要有选择的合并git fetch是更好的选择。效果相同时git pull将更为快捷。


```bash
man git-fetch
git fetch --prune  #在本地删除在远程不存在的branch
git fetch --all 告诉 Git 同步所有的远端仓库。

#git分析指定的tag标签创建分支的命令
git checkout -b branch_name tag_name
```

### tag
```bash
#list local tags
git tag

# list remote tags
git ls-remote --tags origin

# checkout tag
git checkout tag_name

# add a tag
git tag v1.0.0

# commit tag
git push origin v1.0.0

# delete tag
git tag -d 1.0.0

# delete remote tag
git push origin :refs/tags/1.0.0
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
    git switch branch0
    git checkout branch0

#### 新建并切换到分支
    git switch -c dev
    git checkout -b branch0

#### 删除分支
    git branch -d branch0
    # 强制删除分支，删除没merge的分支
    git branch -D branch0
#### 删除远程的todo branch
    git branch -d -r origin/todo
#### 分支合并, git merge 命令用于合并指定分支到当前分支
    git merge branch1 -m "MSG0"

### 本地分支重命名(还没有推送到远程)
    git branch -m oldName newName

### git pull
    git pull
    git pull origin branch0
    git pull origin master

### git clone
git clone <版本库的网址> <本地目录名>

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

### git push
```bash
git push <远程主机名> <本地分支名>:<远程分支名>

#如果本地分支名与远程分支名相同，则可以省略冒号：
git push <远程主机名> <本地分支名>
# 将本地的 master 分支推送到 origin 主机的 master 分支。
git push origin master
#如果当前分支与多个主机存在追踪关系，则可以使用 -u 选项指定一个默认主机，这样后面就可以不加任何参数使用git push。
git push -u origin master

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

# 删除远程分支: 

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
Linux或Mac系统使用LF作为行结束符，因此你不想 Git 在签出文件时进行自动的转换；当一个以CRLF为行结束符的文件不小心被引入时你肯定想进行修正，把core.autocrlf设置成input来告诉 Git 在提交时把CRLF转换成LF，签出时不转换: 
$ git config --global core.autocrlf input
这样会在Windows系统上的签出文件中保留CRLF，会在Mac和Linux系统上，包括仓库中保留LF。

如果你是Windows程序员，且正在开发仅运行在Windows上的项目，可以设置false取消此功能，把回车符记录在库中: 

$ git config --global core.autocrlf false

### submodule
当你在一个Git 项目上工作时，你需要在其中使用另外一个Git 项目。也许它是一个第三方开发的Git 库或者是你独立开发和并在多个父项目中使用的。这个情况下一个常见的问题产生了: 你想将两个项目单独处理但是又需要在其中一个中使用另外一个。

在Git 中你可以用子模块submodule来管理这些项目，submodule允许你将一个Git 仓库当作另外一个Git 仓库的子目录。这允许你克隆另外一个仓库到你的项目中并且保持你的提交相对独立。

添加子模块
此文中统一将远程项目https://github.com/maonx/vimwiki-assets.git克隆到本地assets文件夹。


$ git submodule add https://github.com/maonx/vimwiki-assets.git assets

### [0x7FFA0BF6E0A4] ANOMALY: use of REX.w is meaningless (default operand size is 64)
导致这个问题的原因之一，是因为电脑安装了浪潮的 IP-GUARD 监控软件。
卸载电脑原先的Git，安装32位Git。
或者卸载监控软件

### git remove
git rm /xxx/xxx/xxx.xxx  
git rm xxx/xxx

### git restore
将在工作空间但是不在暂存区的文件撤销更改 
```bash
git restore

```


#### 将暂存区的文件从暂存区撤出，但不会更改文件
```bash
git restore --staged /path/to/file
```
>https://blog.csdn.net/u013493841/article/details/104451987

### 关闭ssl校验
```bash
git config –global http.sslVerify false

```

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

https://www.jianshu.com/p/9000cd49822c
>https://blog.csdn.net/CrazyZhang1990/article/details/42780285