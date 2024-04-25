---
title: git svn
author: "-"
date: 2013-01-07T14:37:06.000+00:00
url: git/svn
categories:
  - inbox
tags:
  - reprint
---
## git svn

### install

#### ubuntu

```bash
sudo apt-get install -y git-svn
```

```bash
# init
mkdir -p /path/to/project-foo/
git svn init https://url.to.svn.repo
git svn fetch -r 1342:HEAD
```

### 从中心服务器的 svn repository 获取最新更新

这个操作可以通过"git-svn rebase"完成。注意这里用的是rebase,而不是update。update命令对于通过git-svn检出的svn repostory的git版本库是不可用的。

```bash
git svn rebase

git commit -a -m ""
git svn dcommit
```

### Password for 'user0': Can't locate Term/ReadKey.pm

git requires perl-term-readkey when it asks for user input

Found when trying to enter a password for a `git svn dcommit`

Password for 'user0': Can't locate Term/ReadKey.pm in @INC (you may need to install the Term::ReadKey module) (@INC contains: /usr/share/perl5/site_perl /usr/lib/perl5/site_perl /usr/lib/perl5/vendor_perl /usr/share/perl5/vendor_perl /usr/lib/perl5/core_perl /usr/share/perl5/core_perl .) at /usr/share/perl5/vendor_perl/Git.pm line 565.

Installing the perl-term-readkey package fixes this

```bash
sudo pacman -S perl-term-readkey
```

### The name org.freedesktop.secrets was not provided by any .service file

insall gnome-keyring,

```bash
    pacman -S gnome-keyring
```

or disable password stores at the subversion config file \~/.subversion/config

password-stores =

[https://bbs.archlinux.org/viewtopic.php?id=239198](https://bbs.archlinux.org/viewtopic.php?id=239198)

```bash
# init
mkdir -p /path/to/project-foo/
git svn init https://url.to.svn.repo
git svn fetch -r 1342:HEAD
### checkout 所有数据, 相当于 init + fetch
    git svn clone https://path/to/svn/root -T https://path/to/trunk -b https://path/to/branches/root/branches -t https://path/to/tag/root

# create a branch
git svn branch -n  -m "comments_0" branch_name_0

# creat a tag
git svn branch -n --tag -m "comments_0" tag_name_0
git svn branch --tag -m "comments_0" tag_name_0

# -n, --dry-run, 返回将要执行的动作, 不实际执行。

git svn tag
git svn branch -n  -m "Branch for authentication bug" auth_bug

# archlinux

sudo pacman -S git subversion perl-term-readkey

# centos

sudo yum install git
sudo yum install git-svn

# add project to remote git repo

touch README.md
git add README.md
git commit -m "first git commit"

# create git repo

git remote add origin https://url/to/git/repo.git
git svn dcommit
git push -u origin master

# for merge exception

git branch --set-upstream-to=origin/master
git pull --allow-unrelated-histories

git push -u origin master -f

git svn rebase
git commit -a -m ""
git svn dcommit
```

### git-svn 解决冲突

打开冲突的文件 找到冲突的地方修改完成后保存
执行 git add 冲突文件

```bash
    git rebase --continue
    git svn dcommit
```

git与SVN协同的工作流程

git可以和SVN服务器一起使用,即,中央服务器采用svn,本地代码库使用git。这样的好处是,可以兼容以前的项目,同时本地有一套完整的版本控制系统,可以随时查看代码修改历史,随时提交,不需要网络。合适的时候再提交到SVN服务器。git-svn的工作流程也有很多,我们推荐使用下面这种方式。

git-svn初始化

git svn init SVNREMOTEURL

-s 参数是表面使用的是svn标准命名方法,即 trunk,tags,branches,这个参数有时很重要,建议使用,命 令后面还可以加个文件夹名字作为clone后的目录

git svn fetch

可能碰到只想从某个版本开始进行fetch,那么请需要 –r 参数。 例如:

$ git svn fetch -r 1342:HEAD

$ git remote add origin GITREMOTEURL 初始化远程git 地址

这⼀一步可以省略 如果没必要提交到远程git 服务器中

set current branch as remote master

git push –set-upstream origin master

git-svn基本⽤用法

本地修改代码后提交

git commit -a -m ""

同步远程svn 服务器

git svn rebase

推送到远程svn服务器

git svn dcommit

推送到远程git 服务器

git push

从SVN服务器获取代码

git svn clone 相当于运行了两条命令git svn init和 git svn fetch.

$ git svn clone [http://svnserver/project/trunk](http://svnserver/project/trunk)

创建一个本地分支

为了方便合并,减少不必要的麻烦,最好保持主分支master不变,在一个新的分支进行日常工作

git branch workA

日常修改和提交

与git的工作流程完全一样

git switch -b work

git commit -a

切回master从SVN获取最新代码

git switch master

git svn rebase

master同步后,与工作分支合并

git switch work

git rebase master ## 手工解决可能的冲突

合并主分支

git switch master
git merge work

git-svn 解决冲突

⼿动打开冲突的⽂文件 找到冲突的地⽅方修改完成后保存

执⾏行 git add 冲突⽂文件

git rebase –continue

git svn dcommit

### 冲突的处理

```Bash
git rebase --abort
```

执行之后,本地内容会回到提交之间的状态,也就是回到以前提交但没有pull是的状态,简单来说就是撤销rebase。

```Bash
git rebase --skip
```

引起冲突的commits会被丢弃,对于本文应用的例子来说开发者A对c.sh文件的commit无效,开发者A自己修改的部分全部无效,因此,在使用skip时请慎重。执行: `vim c.sh` 查看本地 c.sh 文件提交内容,展示如下图所示,执行语句之后开发者A的修改无效。

```Bash
git rebase --continue
```

`git pull --rebase` 之后,本地如果产生冲突,手动解决冲突之后,用"git add"命令去更新这些内容的索引(index),然后只要执行:

`git rebase --continue` 就可以线性的连接本地分支与远程分支,无误之后就回退出,回到主分支上。
注意: 一般情况下,修改后检查没问题,使用 `rebase continue` 来合并冲突。

[https://git-scm.com/book/zh/v1/Git-%E4%B8%8E%E5%85%B6%E4%BB%96%E7%B3%BB%E7%BB%9F-Git-%E4%B8%8E-Subversion](https://git-scm.com/book/zh/v1/Git-%E4%B8%8E%E5%85%B6%E4%BB%96%E7%B3%BB%E7%BB%9F-Git-%E4%B8%8E-Subversion)

[https://git-scm.com/docs/git-svn](https://git-scm.com/docs/git-svn)

[http://hufeng825.github.io/2013/09/03/git9/](http://hufeng825.github.io/2013/09/03/git9/)

[https://git-scm.com/book/zh/v1/Git-%E4%B8%8E%E5%85%B6%E4%BB%96%E7%B3%BB%E7%BB%9F-Git-%E4%B8%8E-Subversion](https://git-scm.com/book/zh/v1/Git-%E4%B8%8E%E5%85%B6%E4%BB%96%E7%B3%BB%E7%BB%9F-Git-%E4%B8%8E-Subversion)

[https://hanckmann.com/2012/12/28/blog.html](https://hanckmann.com/2012/12/28/blog.html)

[https://bugs.archlinux.org/task/43303](https://bugs.archlinux.org/task/43303)

[https://tonybai.com/2011/01/20/try-git-svn/](https://tonybai.com/2011/01/20/try-git-svn/ "https://tonybai.com/2011/01/20/try-git-svn/")  
[https://www.cnblogs.com/chenjunjie12321/p/6876220.html](https://www.cnblogs.com/chenjunjie12321/p/6876220.html)  
