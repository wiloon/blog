---
title: Git basic commands, git 常用命令
author: "-"
date: 2022-01-29 10:33:11
url: git/basic
categories:
    - Git
tags:
    - remix
    - reprint
---
## Git basic commands, git 常用命令

## origin

<https://www.zhihu.com/question/27712995>

origin 是远程仓库的默认别名, 查看配置了几个远程仓库和别名 `git remote -v`

## 分支, branch

最新版本的 Git 提供了新的 `git switch` 命令来切换分支, `git switch`，比 `git checkout` 要更容易理解。

```bash
# 分支改名
git branch -m branch0 branch1
```

### 设置默认的分支名

```bash
# 设置默认分支名，不设置的话，默认是 master
git config --global init.defaultBranch <name>
git config --global init.defaultBranch main
# The just-created branch can be renamed via this command
git branch -m main
```

### 打印当前分支名

```bash
git symbolic-ref --short HEAD  
```

### 查看

```bash
## 查看所有的分支, 本地 + 远程
git branch -a
# 查看本地分支, 当前分支前面会标一个 `*` 号
git branch
## 查看远程所有分支
git branch -r 
# check branch detail
git branch -v
# git查看本地分支关联（跟踪）的远程分支之间的对应关系，本地分支对应哪个远程分支
git branch -vv
```

### 新建分支

新建分支其实就是在当前位置打个标签, 也就是说... 新分支是以当前分支的 commit 为基础的.

### 新建并切换到分支

```bash
git switch -c dev
git checkout -b branch0
```

```bash
# 从当前分支创建新分支, 新 branch 名字: branch0
git branch branch0
# 从 branch0 分支 创建 branch1 分支
git branch1 branch0
# 从 branch0 分支 创建 branch1 分支并切换到 branch1 分支 
git checkout -b branch1 branch0
# 从 tag v1.2.3 创建分支 branch1
git checkout -b branch1 v1.2.3
```

### 切换到分支

```bash
git switch branch0
git checkout branch0
```

### 把新建的分支推送到远端

```bash
git push origin branch0
```

### 删除分支

```bash
# 删除本地分支
git branch -d branch0
# 删除远程分支
git push origin --delete branch0
# 强制删除分支，删除没 merge 的分支
git branch -D branch0
```

#### 删除远程的 todo branch

```bash
git branch -d -r origin/todo
```

## git tag

轻量标签 (lightweight）与附注标签 (annotated）。

### 附注标签 (annotated）

附注标签是存储在 Git 数据库中的一个完整对象, 它们是可以被校验的，其中包含打标签者的名字、电子邮件地址、日期时间，此外还有一个标签信息，并且可以使用 GNU Privacy Guard  (GPG）签名并验证。通常会建议创建附注标签，这样你可以拥有以上所有信息。

在运行 tag 命令时指定 -a 选项, 创建附注标签

```bash
git tag -a v1.4 -m "message0"
# 对历史提交打标签
git tag -a v1.2 9fceb02
git push origin v1.5
git push --tag
```

### 轻量标签 (lightweight）

```bash
# list local tags
git tag
git tag -l "v1.8.5*"

# list remote tags
git ls-remote --tags origin

# 显示提交信息
git show v0.0.1

# 查看 tag 在哪个分支上
git branch --contains tags/<tag>

# 查看commit内容
git show commit_id

# checkout tag
git checkout tag_name

# add a tag
git tag v1.0.0

# 共享标签, 提交标签, commit tag
git push origin <tagname>
git push origin v1.0.0

# delete tag, 删除 tag
git tag -d v1.0.0

# delete remote tag
git push --delete origin tag0
git push origin :refs/tags/v1.0.0
```

## merge 合并分支, git merge 命令用于合并指定分支到当前分支

```bash
# merge 默认会把 commit 的历史都合并进来
# 把 branch0 合并到当前分支
git merge branch0
git merge branch0 -m "MSG0"
```

### git merge --squash

```bash
# git merge --squash, 把多次 commit 的历史合并成一次 commit
# 把 branch1 的提交 合并 到 branch0
# 切换到 branch0 然后执行以下命令
git merge --squash branch1
git commit -m "comments0"
```

```bash
# 解决Git报错:error: You have not concluded your merge (MERGE_HEAD exists).
git merge --abort
```

### 本地分支重命名 (还没有推送到远程)

```bash
git branch -m oldName newName
```

## commands

```bash
# 计算对象数和磁盘消耗
git count-objects -vH
# 指定目录 1.8.5 以前
git --git-dir=/Users/jhoffmann/tmp/my-project/.git --work-tree=/Users/jhoffmann/tmp/my-project/ pull
# 指定目录 >=1.8.5
git -C /Users/jhoffmann/tmp/my-project/ pull
```

## Git 连通性测试

```bash
ssh -T git@github.com
```

### git add

git add 命令可将该文件添加到 `暂存区`

### config git editor

```bash
git config --global core.editor vim
export EDITOR=vim
```

### commit

#### 修改已经push了的commit信息

```bash
如题，本条仅适用于修改已经push过了的最近一次的commit注释信息，确保本地文件的最新的。

step1：使用【git commit --amend】命令，会进入到vim编辑器。

step2：输入【i】，即进入编辑模式，此时编辑提交信息。

step3：编辑好之后，按键【Esc】，输入【:wq】，即保存和退出。

step4：输入【git push -f】强制提交。

操作完之后，再看提交记录，即可看到修改的注释信息。
```

#### 修改最近一次的 commit message

```bash
git commit --amend
git commit --amend -m "New commit message."
```

Rewriting the most recent commit message
You can change the most recent commit message using the git commit --amend command.

In Git, the text of the commit message is part of the commit. Changing the commit message will change the commit ID--i.e., the SHA1 checksum that names the commit. Effectively, you are creating a new commit that replaces the old one.

### 修改最近的第 n 次 commit message

```bash
# 数字代表显示倒数第几次, #-i, --interactive
git rebase -i HEAD~2
# git log你可以发现，git的最后一次提交已经变成你选的那个了
# 把pick 修改成edit然后保存退出，然后会看到提示 git commit --amend
git commit --amend
# 修改注释之后，保存退出，然后 git rebase --continue
git rebase --continue
# 把本地仓库的代码推送到远程
git push origin master
# 修改了已经push的注释，得用强制push, force push对其它人有影响慎用.
git push --force origin master
```

### git 清除所有被 Ignore 的文件

#### 查看所有被 Git 忽略的文件, Git 1.6+

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

##### 清除文件或文件夹， -f 选项强制删除，-d 删除目录 (小心）

git 删除未跟踪文件

```bash
# 删除 untracked files
git clean -f
 
# 连 untracked 的目录也一起删掉
git clean -fd
 
# 连 gitignore 的 untrack 文件/目录也一起删掉 （慎用，一般这个是用来删掉编译出来的 .o之类的文件用的）
git clean -xfd
 
# 在用上述 git clean 前，墙裂建议加上 -n 参数来先看看会删掉哪些文件，防止重要文件被误删
git clean -nxfd
git clean -nf
git clean -nfd
```

<https://ruby-china.org/topics/17951>

## git remote

### 查看远程仓库地址 url

```bash
git remote -v
```

### 添加远程库

```bash
# 添加一个新的远程 Git 仓库，同时指定一个方便使用的简写
# 命令格式
git remote add <shortname> <url>
# 示例
git remote add pingd http://192.168.50.13:10880/wiloon/wiloon.com.git
# 向远程仓库推送代码
# origin 是远程库的名字, 单个远程库, 一般用默认的 origin, 多个远程库的时候可以改成方便记忆的名字.
git push -u origin master
```

### 删除远程库

```bash
git remote rm repo0
```

### 删除文件

git rm /xxx/xxx/xxx.xxx  
git rm -r xxx/xxx

### 将指定的提交 (commit) 应用于其他分支

```bash
git cherry-pick <commitHash>
```

<https://www.ruanyifeng.com/blog/2020/04/git-cherry-pick.html>

### 指定ssh 私钥

```bash
GIT_SSH_COMMAND="ssh -i ~/tmp/id_rsa" git clone git@github.com:wiloon/foo.git
```

### 打印当前版本

```bash
git rev-parse HEAD
```

### git checkout 检出

git checkout: Git的checkout有两个作用，其一是在不同的branch之间进行切换，例如'git checkout new_branch'就会切换到new_branch的分支上去；另一个功能是还原代码的作用，例如'git checkout app/model/user.rb'就会将user.rb文件从上一个已提交的版本中更新回来，未提交的内容全部会回滚

git checkout -f     //提取当前branch的所有文件．

git checkout HEAD . # 将所有代码都 checkout 出來(最后一次 commit 的版本), 注意, 若有修改的代码都会被还原到上一版. (git checkout -f 亦可)

### checkout 指定版本

```bash
git checkout 788258e49531eb24bfd347a600d69a16f966c495
```

### 放弃本地未提交的修改

To discard all local changes, you do not use revert. revert is for reverting commits. Instead, do:

```bash
git checkout . #本地所有修改的。没有的提交的，都返回到原来的状态
```

<https://blog.csdn.net/leedaning/article/details/51304690>

### 指定克隆深度

在git clone时加上--depth=1

depth用于指定克隆深度，为1即表示只克隆最近一次commit.

git checkout master

## git config

### 查看 config

config 配置有system级别 global (用户级别)  和local (当前仓库) 三个 设置先从system-》global-》local  底层配置会覆盖顶层配置 分别使用--system/global/local 可以定位到配置文件

```bash
git config --list
git config --system --list
git config --global core.editor vim
```

查看当前用户 (global) 配置

```bash
git config --global  --list
```

查看当前仓库配置信息

```bash
git config --local  --list
```

### 设置

```bash
#设置电子邮件地址
# global
git config --global user.name "name0"
git config --global user.email "email@example.com"

# local
git config --local user.name "name0"
git config --local user.email "email@example.com"


#确认在 Git 中正确设置了电子邮件地址
git config --global user.email
git config --local  user.email
```

### edit: set, delete

```bash
git config --edit
git config --global --edit
```

## git log

```bash
git log
git log file0
git log -3 file0
git log --oneline
git log --reverse

# git log 倒序, 仓库创建时间
git log --reverse

echo "# project name" >> README.md
```

git reflog 可以查看所有分支的所有操作记录 (包括 (包括 commit 和 reset 的操作），包括已经被删除的commit记录，git log 则不能察看已经删除了的 commit 记录。

```bash
git reflog
```

### 更改最多的文件

git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -10

--pretty。 使用不同于默认格式的方式展示提交历史
format ，可以定制记录的显示格式。 --pretty=format:"%h - %an, %ar : %s"
--name-only参数仅显示受影响的文件名。如果你想看看每个文件发生了什么(删除，修改，添加)，请改用--name-status

### 初始化 Git 仓库

git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:wiloon/go-angular-x.git
git push -u origin master

```bash
git rm
git rm -f
```

## git fetch

git fetch 命令用来拉取其它仓库的数据 (objects and refs).  
默认情况下，git fetch 取回**所有**分支 (branch) 的更新。如果只想取回特定分支的更新，可以指定分支名。  

```bash
git fetch <远程主机名> <分支名>
# 比如，取回 origin 主机的 master 分支。
git fetch origin master
# -p, 分支在远程删掉之后, 执行 git fetch -p, 更新一下本地的分支列表, 本地就看不到已经删除的分支了
git fetch -p
```

### git fetch 与 git pull

git fetch 和 git pull 都可以将远端仓库更新至本地那么他们之间有何区别?想要弄清楚这个问题有有几个概念不得不提。

FETCH_HEAD: 是一个版本链接，记录在本地的一个文件中，指向着目前已经从远程仓库取下来的分支的末端版本。
commit-id: 在每次本地工作完成后，都会做一个git commit 操作来保存当前工作到本地的repo， 此时会产生一个commit-id，这是一个能唯一标识一个版本的序列号。 在使用 git push 后，这个序列号还会同步到远程仓库。

有了以上的概念再来说说 git fetch
git fetch: 这将更新 git remote 中所有的远程仓库所包含分支的最新 commit-id, 将其记录到.git/FETCH_HEAD 文件中
git fetch 更新远程仓库的方式如下:

git fetch origin master: tmp
//在本地新建一个temp分支，并将远程origin仓库的master分支代码下载到本地temp分支

## git diff

git diff tmp

git diff，不加任何参数，默认比较的是工作区和暂存区之间的文件差异

// 来比较本地代码与刚刚从远程下载下来的代码的区别
git merge tmp
//合并temp分支到本地的master分支
git branch -d temp
//如果不想保留temp分支 可以用这步删除

 (1) 如果直接使用git fetch，则步骤如下:

创建并更新本 地远程分支。即创建并更新origin/xxx 分支，拉取代码到origin/xxx分支上。
在FETCH_HEAD中设定当前分支-origin/当前分支对应，如直接到时候git merge就可以将origin/abc合并到abc分支上。
 (2) git fetch origin
只是手动指定了要fetch的remote。在不指定分支时通常默认为master
 (3) git fetch origin dev
指定远程remote和FETCH_HEAD，并且只拉取该分支的提交。

## git pull

命令的作用是，取回远程主机某个分支的更新，再与本地的指定分支合并。

git pull: 首先，基于本地的FETCH_HEAD记录，比对本地的FETCH_HEAD记录与远程仓库的版本号，然后git fetch 获得当前指向的远程分支的后续版本的数据，然后再利用git merge 将其与本地的当前分支合并。所以可以认为git pull是git fetch和git merge两个步骤的结合。
git pull的用法如下:

git pull <远程主机名> <远程分支名>:<本地分支名>
//取回远程主机某个分支的更新，再与本地的指定分支合并。

因此，与git pull相比git fetch相当于是从远程获取最新版本到本地，但不会自动merge。如果需要有选择的合并git fetch是更好的选择。效果相同时git pull将更为快捷。

`git pull` 标准或完整的命令是 `git pull remote_repository_name branch_name`

```bash
git pull
# verbos
git pull -v
git pull origin master
git pull origin branch0
```

```bash
man git-fetch
git fetch --prune  #在本地删除在远程不存在的branch
git fetch --all 告诉 Git 同步所有的远端仓库。

# git分析指定的tag标签创建分支的命令
git checkout -b branch_name tag_name
```

<https://git-scm.com/book/zh/v2/Git-%E5%9F%BA%E7%A1%80-%E6%89%93%E6%A0%87%E7%AD%BE>

### git clone

git clone <版本库的网址> <本地目录名>

```bash

git clone https://user0:password0@git.foo.com/path/to/project.git

git log --pretty=oneline

git-ls-files  # - Show information about files in the index and the working tree

# list deleted files

git ls-files -d

# 恢复已删除的文件

git ls-files -d | xargs git checkout --
```

## git push

```bash
# push 
git push <远程仓库名> <本地分支名>:<远程分支名>
# 提交本地test分支作为远程的 master 分支
git push origin test:master
 
# 如果本地分支名与远程分支名相同，则可以省略冒号：
git push <远程仓库名> <本地分支名>
# 将本地的 master 分支推送到 origin 主机的 master 分支。
git push origin master:master
# 省略冒号简写成这样
git push origin master

# 如果配置了多个远程仓库，则可以使用 -u 选项指定一个默认仓库，以后再执行 git push 就可以不显示的指定仓库了.
git push -u origin master
# -f 强制覆盖到仓库，这会导致仓库中某些记录丢失。
git push -f

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

git status -s
git add .

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
此文中统一将远程项目<https://github.com/maonx/vimwiki-assets.git克隆到本地assets>文件夹。

$ git submodule add <https://github.com/maonx/vimwiki-assets.git> assets

### [0x7FFA0BF6E0A4] ANOMALY: use of REX.w is meaningless (default operand size is 64)

导致这个问题的原因之一，是因为电脑安装了浪潮的 IP-GUARD 监控软件。
卸载电脑原先的Git，安装32位Git。
或者卸载监控软件

### git restore

将在工作空间但是不在暂存区的文件撤销更改

```bash
git restore

```

#### 将暂存区的文件从暂存区撤出，但不会更改文件

```bash
git restore --staged /path/to/file
```

><https://blog.csdn.net/u013493841/article/details/104451987>

### 关闭ssl校验

```bash
git config –global http.sslVerify false
```

><https://git-scm.com/docs>
><https://git-scm.com/book/zh/v2>

<http://zensheno.blog.51cto.com/2712776/490748>  
<http://blog.csdn.net/ithomer/article/details/7529841>  
<http://www.cnblogs.com/springbarley/archive/2012/11/03/2752984.html>  
<http://git-scm.com/book/zh/v1/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6>  
<http://yijiebuyi.com/blog/eacf4d053fad77affffae397d9af7172.html>  
<http://www.ruanyifeng.com/blog/2014/06/git_remote.html>  
<https://www.liaoxuefeng.com/wiki/896043488029600/900003767775424>  
<https://blog.csdn.net/riddle1981/article/details/74938111>  
<https://blog.csdn.net/SCHOLAR_II/article/details/72191042>  
<https://www.jianshu.com/p/38f04aef1c9d>

><https://www.jianshu.com/p/9000cd49822c>
><https://blog.csdn.net/CrazyZhang1990/article/details/42780285>

### pre-commit

.git/hook/pre-commit

### create a new repository on the command line

echo "# jetbrain-eap-installer" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:wiloon/jetbrain-eap-installer.git
git push -u origin main

### push an existing repository from the command line

git remote add origin git@github.com:wiloon/jetbrain-eap-installer.git
git branch -M main
git push -u origin main

## 删除大文件

><https://harttle.land/2016/03/22/purge-large-files-in-gitrepo.html>

## 按修改次数排序

```bash
git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -20
```

## fatal: refusing to merge unrelated histories

两个分支是两个不同的版本，具有不同的提交历史

```bash
#允许不相关历史提，强制合并：
git pull --allow-unrelated-histories

```

原因："git merge" used to allow merging two branches that have no common base by default, which led to a brand new history of an existing project created and then get pulled by an unsuspecting maintainer, which allowed an unnecessary parallel history merged into the existing project. The command has been taught not to allow this by default, with an escape hatch "--allow-unrelated-histories" option to be used in a rare event that merges histories of two projects that started their lives independently（stackoverflow）.

作者：勿以浮沙筑高台
链接：<https://www.jianshu.com/p/536080638cc9>
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

## Git 删除某个文件的历史记录

```bash
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch /content/post/archive-2/cross-compile.md' --prune-empty --tag-name-filter cat -- --all

# 本地记录覆盖到Github,(所有branch以及所有tags)
git push origin --force --all
git push origin --force --tags

# 确保没有什么问题之后,强制解除对本地存储库中的所有对象的引用和垃圾收集
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all

```

————————————————
版权声明：本文为CSDN博主「JAVA|Mr.Java」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/q258523454/article/details/83899911>

## TortoiseGit, ssh key

把 key 转成 ppk 格式 加到 Pageant 里.

<https://www.jianshu.com/p/1bbf5e25c912>

## git 没提交的代码迁移到新分支

```bash
// 先将本地修改进行暂存
> git stash
 
// 暂存完毕后执行 git status 会显示不出本地的修改
// 再拉取当前分支
> git pull 
 
// 新建并切换到开发分支，如dev-2021-11
> git checkout -b dev-2021-11
 
// 将暂存的本地修改取出
> git stash apply
 
// 这时执行 git status 可以看到本地修改又显示出来了
// 正常提交即可
> git add .
> git commit -am "local code"
> git push origin dev-2021-11
```

<https://www.cnblogs.com/toutou/p/git_stash.html>

## There is no tracking information for the current branch

是因为本地分支和远程分支没有建立联系 (使用git branch -vv 可以查看本地分支和远程分支的关联关系) .根据命令行提示只需要执行以下命令即可

git branch --set-upstream-to=origin/远程分支的名字(我的是master) 本地分支的名字(我的是master)

<https://segmentfault.com/a/1190000009128253>
