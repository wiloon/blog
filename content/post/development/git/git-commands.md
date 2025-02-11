---
title: Git basic commands, git 常用命令
author: "-"
date: 2022-01-29 10:33:11
url: git/basic
categories:
- Git
tags:
- reprint
- remix
---
## Git basic commands

目前比较流行的版本管理系统

相比同类软件，Git有很多优点。其中很显著的一点，就是版本的分支 (branch) 和合并 (merge) 十分方便。
有些传统的版本管理软件，分支操作实际上会生成一份现有代码的物理拷贝，而Git只生成一个指向当前版本 (又称"快照") 的指针，因此非常快捷易用。

## commands

```bash
显示出 HEAD 对应的提交的 hash 值
git rev-parse HEAD
git rev-parse --short HEAD

# windows install git
winget install Git.Git

# 显示工作树状态, (已经修改但是没 git add, 或者 没有 git commit)
# 显示索引文件和当前HEAD提交有差异的路径，工作树和索引文件有差异的路径，以及工作树中不被Git追踪的路径（也不被gitignore[5]忽略）。前者是你通过运行 "git commit "会提交的东西；第二和第三者是你在运行 "git commit "之前通过运行 "git add "可以提交的东西。
git status -s

# 查看本地仓库的当前分支和远程分支的差异(已经 commit 但是还没 push), 只显示 commit id 和 comments
git cherry -v

# 查看本地仓库的当前分支和远程分支的差异(已经 commit 但是还没 push), 展示方式类似 git log
git log master ^origin/master
# 计算对象数和磁盘消耗
git count-objects -vH
# 指定目录 1.8.5 以前
git --git-dir=/Users/jhoffmann/tmp/my-project/.git --work-tree=/Users/jhoffmann/tmp/my-project/ pull
# 指定目录 >=1.8.5
git -C /Users/jhoffmann/tmp/my-project/ pull
```

### options

- -C, 大写 `C` 指定目录, `.git` 所在的目录
- --version, 查看 git 版本

### origin

[https://www.zhihu.com/question/27712995](https://www.zhihu.com/question/27712995)

origin 是远程仓库的默认别名, 查看配置了几个远程仓库和别名 `git remote -v`


## commit

通过git commit命令将暂存区内容添加到本地仓库后，git会生成相应的commit id。

```bash
# 在 commit 的时候使用指定的 author 信息
git commit -m "message0" --author="author0 <auther0@foo.com>"
```

### --amend

Rewriting the most recent commit message
You can change the most recent commit message using the git commit --amend command.

In Git, the text of the commit message is part of the commit.
Changing the commit message will change the commit ID--i.e., the SHA1 checksum that names the commit.
Effectively, you are creating a new commit that replaces the old one.

修改 分支 branch_0 最近一次的 commit message, author

https://blog.csdn.net/scgaliguodong123_/article/details/122423940

```bash
git switch branch_0
git pull

# 不带参数, 执行后会提示输入 new commit message
# author 会变成默认的
git commit --amend
# 或者直接提供 new commit message
git commit --amend -m "New commit message."

# 修改 author, 然后也会提示修改 message
git commit --amend --author="Wang Yue<yue.wang>"
# 只修改 author
git commit --amend --author="Wang Yue<yue.wang>" --no-edit
# 这个 commit 已经被 push 到了远程仓库, 修改之后得再 push 一下, 把这个修改强制推送到远程仓库
git push -f
```

#### 修改已经 push 了的 commit, git 修改 message, 不是最近一次提交

进入 git rebase 的交互模式修改

```bash
  git rebase -i commit_id_0  
  # 把对应的 commit 的 action 改成 e
   
  git commit --amend --author="auth0 <auth0@foo.com>"
  git rebase --continue
  git push -f
```

### emoji

https://cloud.tencent.com/developer/article/2067309

git commit 时可以加入表情，可以使得提交历史内容清晰

```Bash
  git commit -m ":bug: message_0"
```

- 🐛 (bug), :bug:, 修复 bug
- 🔊 (喇叭), :loud_sound:, 增加/更新日志

## git log

```bash
# --no-pager, 不使用默认的 less pager
# --oneline, 显示简化版的 log, 没有 Author, 没有 Date
git --no-pager log --oneline -n 10

# 按 s 向下翻 log
git log
# 显示最近的 3 个 commit
git log -n 3
# 查看某一个分支的 log
git log branch0
# 查看某一个远程分支的 log
git log remotes/origin/branch0

git log file0
git log -3 file0
# 以一行展现
git log --oneline
git log --reverse

# git log 倒序, 仓库创建时间
git log --reverse
git log --graph --pretty=oneline --abbrev-commit
git log --all --pretty=oneline --abbrev-commit --graph
git log --graph --oneline --all
echo "# project name" >> README.md
```

### 日志过滤

```Bash
# 按本地分支过滤
git log branch_0
# 按远程分支过滤
git log origin/branch_0
# 按照数量过滤
git log -3
# 按照日期过滤
git log --after="2014-7-1"
git log --after="yesterday"
git log --after="2014-7-1" --before="2014-7-4"
# 按照作者过滤
git log --author="John"
git log --author="John|Mary"
# 按照提交信息过滤
git log --grep="JRA-224:"
# 按照文件过滤
git log -- foo.py bar.py
# 按照提交内容过滤
git log -S"Hello, World!"
```

### reflog

```Bash
# 查看引用日志（reflog）
git log -g
```

## git fetch

默认更新

- tag
- FETCH_HEAD
- 分支历史 commit

git fetch 是更新(update) 在本地电脑上的远程跟踪分支（如origin/master分支，注意远程跟踪分支是保存在本地，
一般在.git\refs\remotes\origin目录下），并更新(update) .git/FETCH_HEAD 文件。并不会和本地分支 merge，即不会更新本地分支。

git fetch 命令用来拉取远程仓库的数据 (objects and refs).
默认情况下，git fetch 取回**所有**分支 (branch) 的更新。如果只想取回特定分支的更新，可以指定分支名。

更新 (update) .git/FETCH_HEAD 文件

- git fetch 从远程仓库取数据更新到本地仓库, JetBrains git plugin 里的 git 分支后面会出现蓝色箭头, 代表识别到了远程仓库有新的 commit
- working tree/local branch 不会被更新
- JetBrains 里分支 commit 历史不会更新

```Bash
# 获取所有的 tag
git fetch --tags
```

### git fetch 更新其它分支

```bash
# 当前分支不是 dev 分支, 并且 dev 分支在本地没有修改的时候 更新 dev 分支
git fetch origin dev:dev
```

该命令必须严格同时满足以下两个条件：

1. 本地当前分支不能是 dev
2. 本地 dev 分支和 origin/dev 不能分叉, 就是说可以 fast-forward merge

则该命令执行后，可以实现 本地 dev 和远程 dev 分支进行 fast-forward merge，更新本地 dev 分支
只要这两个条件其中一个不满足，则执行该命令会报错

版权声明：本文为 CSDN 博主「啊大1号」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/a3192048/article/details/100069772](https://blog.csdn.net/a3192048/article/details/100069772)

```bash
# git fetch [<options>] [<repository> [<refspec>…​]]
# git fetch <远程仓库名> <分支名>
# <远程仓库名> 默认值: origin
# <分支名> 默认值: 当前分支
git fetch
# 取回对应分支的更新, -u or --update-head-ok
git fetch -u origin dev:dev
# 取回所有分支的更新
git fetch
# 比如，取回 origin 仓库的 master 分支
git fetch origin master
# -p, 分支在远程删掉之后, 执行 git fetch -p, 更新一下本地的分支列表, 本地就看不到已经删除的分支了
# -p 是 --prune 的缩写。它的作用是清理本地的远程跟踪分支
git fetch -p
```

### git fetch 与 git pull

git fetch 和 git pull 都可以将远端仓库更新至本地那么他们之间有何区别? 想要弄清楚这个问题有有几个概念不得不提。

FETCH_HEAD: 是一个版本链接，记录在本地的一个文件中，指向着目前已经从远程仓库取下来的分支的末端版本。
commit-id: 在每次本地工作完成后，都会做一个 git commit 操作来保存当前工作到本地的 repo， 此时会产生一个 commit-id，
这是一个能唯一标识一个版本的序列号。 在使用 git push 后，这个 id 会同步到远程仓库。

有了以上的概念再来说说 git fetch
git fetch: 这将更新本地仓库关联的所有的远程仓库所包含所有分支的最新 commit-id, 
将其记录到 .git/FETCH_HEAD 文件中
git fetch 更新远程仓库的方式如下:

```Bash
git fetch origin master:tmp
```

在本地新建一个 temp 分支，并将远程 origin 仓库的 master 分支代码下载到本地 temp 分支

## 分支, branch

[http://www.ruanyifeng.com/blog/2012/07/git.html](http://www.ruanyifeng.com/blog/2012/07/git.html)

https://stackoverflow.com/questions/4330610/switch-to-another-git-tag

最新版本的 Git 提供了新的 `git switch` 命令来切换分支, `git switch`，比 `git checkout` 要更容易理解, 更安全, 所有 git checkout 能实现的切换类操作, 都建议用 git switch 替换.

As of Git v2.23.0 (August 2019), git switch is preferred over git checkout when you’re simply switching branches/tags. I’m guessing they did this since git checkout had two functions: for switching branches and for restoring files. So in v2.23.0, they added two new commands, git switch, and git restore, to separate those concerns. I would predict at some point in the future, git checkout will be deprecated.

To switch to a normal branch, use git switch <branch-name>. To switch to a commit-like object, including single commits and tags, use git switch --detach <commitish>, where <commitish> is the tag name or commit number.

The --detach option forces you to recognize that you’re in a mode of “inspection and discardable experiments”. To create a new branch from the commitish you’re switching to, use git switch -c <new-branch> <start-point>.

### 查看分支

```bash
# 查看本地分支, 当前分支前面会标一个 `*` 号
git branch

# 查看远程分支
git branch -r

# 查看所有的分支, 本地 + 远程
git branch -a

# check branch detail
git branch -v

# git 查看本地分支关联（跟踪）的远程分支之间的对应关系，本地分支对应哪个远程分支
git branch -vv

# 获取当前的分支名称
git rev-parse --abbrev-ref HEAD

# 获取当前的分支名称, Git 2.22 及更高版本
git branch --show-current

# 查看本地分支对应的远程分支
# 查看本地分支和远程分支的同步状态, update to date, local out of date
git remote show origin
```

### 新建分支

```bash
# 从 tag v1.2.3 创建分支 branch1
# 建议使用 git switch
# git checkout -b branch_name tag_name
# git checkout -b branch1 v1.2.3
git switch -c branch1 v1.2.3
# create branch from a commit
# git branch branch_name <commit-hash or HEAD~3>

# 新建并切换到分支, 不加 -c 的话 git switch 到一个不存在的分支会报错
# -c, --create
git switch -c branch0

# 把新分支推到远程仓库并设置本地分支和远程分支的关联
git push --set-upstream origin branch0
```

新建分支其实就是在当前位置打个标签, 也就是说... 新分支是以当前分支的 commit 为基础的.

```bash
# 从当前分支创建新分支, 新 branch 名字: branch0
git branch branch0

# 从 branch0 分支 创建 branch1 分支
git branch branch1 branch0
# 切换到 分支  branch0
# git checkout -b branch0
git switch branch0

# 从 branch0 分支 创建 branch1 分支并切换到 branch1 分支 
# git checkout -b branch1 branch0
git switch -c branch1 branch0
```

### 切换到分支

使用 --recurse-submodules，将根据超级项目中记录的提交更新所有活动子模块的内容。如果什么都不使用（或 --no-recurse-submodules），子模块工作树将不会被更新。就像 git-submodule，这会分离子模块的 HEAD。

```bash
# 切换到已经存在的某一个分支
# git checkout branch0
git switch branch0

# 切换到 branch0 并且更新 submodule
git switch --recurse-submodules branch0

```

### 把新建的分支推送到远端

```bash
git push origin branch0
# fatal: The current branch branch0 has no upstream branch
git push --set-upstream origin branch0
# 设置本地分支和远程分支的关联, 新建分支的时候 git 不会自动 设置本地分支 和远程分支的关联,需要手动设置,或者像上面的命令一样加参数, 在把分支推送到远程仓库的时候设置关联
git branch --set-upstream-to=origin/<remote_branch> <local_branch>
```

### 删除分支

```bash
# 删除本地分支
git branch -d branch0

# 删除远程分支
git push origin --delete branch0
# 删除之后本地缓存里还能看到这个远程分支, 要用下面的 git fetch -p 清理一下
# -p 清理本地的远程跟踪分支
git fetch -p

# 强制删除分支，删除没 merge 的分支
git branch -D branch0
```

```bash
# 删除远程的 branch_0
git branch -d -r origin/branch_0
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

### 修改分支名, 分支改名, 分支重命名

#### 在 github 页面上改分支名

github 可以直接在页面上改分支名, 如果本地有已经 clone 的代码, 需要执行以下操作

```Bash
# 在 github 页面上修改分支名
git branch -m master main
git fetch origin
# -u, --set-upstream-to <upstream>
git branch -u origin/main main
# 设置默认分支
git remote set-head origin -a
```

https://juejin.cn/post/6844903880115896327

```Bash
# 分支改名, branch rename
# 本地分支重命名  (还没有推送到远程)
# -m, --move            move/rename a branch and its reflog
git branch -m oldBranch newBranch

# 分支改名之后如果直接 git push 会报错说上游的分支名跟本地的不一样

# 删除远程分支（远端无此分支则跳过该步骤）
git push --delete origin oldBranch

# 将重命名后的分支推到远端
git push origin newBranch
# 或者
git push origin HEAD:newBranch

# 把修改后的本地分支与远程分支关联
git branch --set-upstream-to origin/newBranch
```

## git tag

```Bash
git tag v1.0.0 -a -m "message0"
```

### git tag options

- -a, --annotate        annotated tag, needs a message
- -m <msg>, --message=<msg>

轻量标签 lightweight tag 与附注标签 annotated tag

```bash
# 打印当前分支最新的 tag
git describe --tags --abbrev=0

git tag v1.0.0 -a -m "message0"
git push origin v1.0.0

# list all the tags along with annotations & 9 lines of message for every tag
git tag -n9
git tag -l -n9
git tag -l -n9 'v1.38.*'
```

### 附注标签 annotated tag

附注标签是存储在 Git 数据库中的一个完整对象, 它们是可以被校验的，其中包含打标签者的名字、电子邮件地址、日期时间，此外还有一个标签信息，并且可以使用 GNU Privacy Guard  (GPG）签名并验证。通常会建议创建附注标签，这样你可以拥有以上所有信息。

在运行 tag 命令时指定 -a 选项, 创建附注标签

```bash
git tag -a v1.0.0 -m "message0"
# 对历史提交打标签
git tag -a v1.2 9fceb02
git push origin v1.5
git push --tag
# 对某一个 commit 打 tag
# Tag the commit
git tag -a v1.0.0 <commit0> -m "msg0"
```

### 轻量标签 lightweight

```bash
# list local tags
git tag
git tag -l "v1.8.5*"

# list remote tags
git ls-remote --tags origin

# 显示 tag 的 commit 信息
git show v0.0.1

# 查看 tag 在哪个分支上, 只能查看已经拉到本地的 tag, 如果 tag 的确是存在的, 但是用以下命令查不到, 先切换分支, 然后 git pull, 再执行以下命令就能看到了
git branch --contains tags/<tag>

# 查看 commit 内容
git show commit_id

# checkout tag, tag name=v1.2.3
# git checkout v1.2.3
git switch --detach v1.2.3

# add a tag
git tag v1.0.0

# 共享标签, 提交标签, commit tag, Specify the tag in the git push command
git push origin <tagname>
git push origin v1.0.0

# delete tag, 删除 tag
git tag -d v1.0.0

# delete remote tag
git push --delete origin tag0
git push origin :refs/tags/v1.0.0
```

```bash
git rev-parse tags/v1.0.0
git branch --contains commit0
```

## merge 合并

git merge 命令用于合并指定分支到当前分支

```bash
# merge 默认会把 commit 的历史都合并进来
# 把 branch0 合并到当前分支
git merge branch0

git merge branch0 -m "MSG0"
# 禁用 Fast forward
git merge branch0 -m "merge with no-ff" --no-ff
```

### fast-forward

- fast forward 模式，快速合并，看不出做过合并。 不会显示 feature，只保留单条分支记录
- --no-ff, no fast-forward 模式，普通合并，可以保存之前的分支历史。能够更好的查看 merge 历史，以及branch 状态。会生成一个新的commit-id

默认情况下，Git执行 快进式合并, fast-forward merge，会直接将 Master 分支指向 Develop 分支。使用 --no-ff 参数后，会执行正常合并，在Master 分支上生成一个新节点。为了保证版本演进的清晰，我们希望采用这种做法。关于合并的更多解释，请参考 `Benjamin Sandofsky` 的《Understanding the Git Workflow》。

### git merge --squash

```bash
# git merge --squash, 把多次 commit 的历史合并成一次 commit
# 把 branch1 的提交 合并 到 branch0
git switch branch0
git merge --squash branch1
git commit -m "comments0"
```

```bash
# 解决Git报错:error: You have not concluded your merge (MERGE_HEAD exists).
git merge --abort
```

## git remote

```bash
# 查看远程仓库地址/url
git remote -v
# 添加远程库
# 添加一个新的远程 Git 仓库，同时指定一个方便使用的简写
# 命令格式
git remote add <shortname> <url>
# 示例
git remote add pingd http://192.168.50.13:10880/wiloon/wiloon.com.git
# 向远程仓库推送代码
# origin 是远程库的名字, 单个远程库, 一般用默认的 origin, 多个远程库的时候可以改成方便记忆的名字.
git push -u origin master
# 更改远程仓库指向 remote url
git remote set-url origin git@github.com:test/thinkphp.git
# 删除远程库
git remote rm repo0
```

## Git, github 连通性测试

```bash
ssh -T git@github.com
```

### git add

git add, 用工作树的内容更新 `索引文件`

git add -u, add modified and deleted files
`git add .`, `git add -A` add new, modified and deleted files

https://blog.csdn.net/haohaibo031113/article/details/70821321

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

```bash
# 查看在清理之前会做的操作
git clean -Xn
```

##### 清除文件或文件夹，-f 选项强制删除，-d 删除目录 (小心）

git 删除未跟踪文件

```bash
# -n, --[no-]dry-run    dry run
# -f, --[no-]force      force
# -d                    remove whole directories
# -x                    remove ignored files, too
# -X                    remove only ignored files
# 在使用 git clean 前，强烈建议加上 -n 参数先看看会删掉哪些文件，防止重要文件被误删
# 删除未跟踪文件 dry-run
git clean -nf
# 删除
git clean -f

git clean -nfd
git clean -nxfd
git clean -nf
git clean -nfd

# 删除 untracked files
git clean -f
 
# 连 untracked 的目录也一起删掉
git clean -fd
 
# 连 gitignore 的 untrack 文件/目录也一起删掉 （慎用，一般这个是用来删掉编译出来的 .o 之类的文件用的）
git clean -xfd
 
```

[https://ruby-china.org/topics/17951](https://ruby-china.org/topics/17951)

## 删除文件, git delete file

```bash
git rm /xxx/xxx/xxx.xxx  
git rm -rf xxx/xxx
# 不支持 `git rm .`
# 需要删除多个文件的时候可以用 -A: stage all (new, modified, deleted) files
git add -A
```

## 将指定的提交 (commit) 应用于其他分支

```bash
git cherry-pick <commitHash>
```

[https://www.ruanyifeng.com/blog/2020/04/git-cherry-pick.html](https://www.ruanyifeng.com/blog/2020/04/git-cherry-pick.html)

## 指定 ssh 私钥

```bash
GIT_SSH_COMMAND="ssh -i ~/tmp/id_rsa" git clone git@github.com:wiloon/foo.git
```

## 打印当前版本

```bash
git rev-parse HEAD
```

## git checkout 检出

Switch branches or restore working tree files

切换分支可以用新的命令 git switch, restore working tree 可以用 git reset

Git 的 checkout 有两个作用，其一是在不同的 branch 之间进行切换，例如 'git checkout branch0' 就会切换到 branch0 的分支上去；
另一个功能是还原代码的作用，例如 'git checkout path/to/foo.py' 就会将 foo.py 文件从上一个已提交的版本中更新回来，未提交的内容全部会回滚/丢失.

### 放弃本地未提交的修改

To discard all local changes, you do not use revert. revert is for reverting commits. Instead, do `git checkout .`

```bash
# todo git restore
# 对文件的修改还没有提交, 撤消本地的修改, 已经 add/commit 的不适用
git checkout . # 本地所有修改的。没有的提交的，都返回到原来的状态
```

`git checkout -f` 提取当前 branch 的所有文件.

`git checkout HEAD .` # 将所有代码都 checkout 出來(最后一次 commit 的版本), 注意, 若有修改的代码都会被还原到上一个版本. (`git checkout -f` 亦可)

### checkout 指定版本(某一个 commit)

```bash
# 建议用 switch
# 切换到某一个 commit, 相当于 git checkout fff57bd92e7ad1f90d2b9367b7b7208ea72d9e93
# git checkout 788258e49531eb24bfd347a600d69a16f966c495
git switch --detach 788258e49531eb24bfd347a600d69a16f966c495
```

[https://blog.csdn.net/leedaning/article/details/51304690](https://blog.csdn.net/leedaning/article/details/51304690)

## git config

### 查看 config

config 配置有 system 级别 global (用户级别)  和 local (当前仓库) 三个, 设置先从 system -> global -> local
底层配置会覆盖顶层配置分别使用 --system/global/local 可以定位到配置文件

```bash
# 查看当前用户 (global) 配置
git config --global  --list

# 查看当前仓库配置信息
# 如果当前仓库的配置信息里没有配置某个 key, git会默认读 global 配置
git config --local  --list

git config --list
git config --system --list
git config --global core.editor vim

# 查看全局用户名
git config user.name

# 查看全局邮箱
git config user.email
```

### 设置

```bash
# 打开 vi 直接编辑
git config -e
# 设置电子邮件地址
# global
git config --global user.name "name0"
git config --global user.email "email@example.com"

# local, 当前仓库
git config --local user.name "name0"
git config --local user.email "email@example.com"

# 确认在 Git 中正确设置了电子邮件地址
git config --global user.email
git config --local  user.email

# http proxy
git config --global https.proxy http://127.0.0.1:1080

# remove config key
git config --global --unset user.name
git config --global --edit
```

### edit: set, delete

```bash
# edit the config file
git config --edit
git config --global --edit
```

### config git editor

```bash
git config --global core.editor vim
export EDITOR=vim
```

git reflog 可以查看所有分支的所有操作记录 (包括 commit 和 reset 的操作），包括已经被删除的 commit 记录，git log 则不能察看已经删除了的 commit 记录。

```bash
git reflog
git reflog show

# 查看 merge 和 checkout 记录
git reflog show --date=local | grep 分支名
```

### 更改最多的文件

`git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -10`

--pretty。 使用不同于默认格式的方式展示提交历史
format ，可以定制记录的显示格式。 --pretty=format:"%h - %an, %ar : %s"
--name-only参数仅显示受影响的文件名。如果你想看看每个文件发生了什么(删除，修改，添加)，请改用--name-status

### 初始化 Git 仓库

```bash
git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:wiloon/go-angular-x.git
git push -u origin master
```

## git diff

```bash
git diff 不加参数即默认比较工作区与暂存区
git diff --cached [<path>...]比较暂存区与最新本地版本库（本地库中最近一次commit的内容）
git diff HEAD [<path>...]比较工作区与最新本地版本库。如果HEAD指向的是master分支，那么HEAD还可以换成master
git diff commit-id [<path>...]比较工作区与指定commit-id的差异　　　　　　
git diff --cached [<commit-id>] [<path>...]比较暂存区与指定commit-id的差异
git diff [<commit-id>] [<commit-id>]比较两个commit-id之间的差异

```

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

git pull 命令用于从另一个存储库或本地分支获取并集成(整合)。git pull 命令的作用是：取回远程主机某个分支的更新，再与本地的指定分支合并

git pull: 首先，基于本地的 FETCH_HEAD 记录，比对本地的 FETCH_HEAD 记录与远程仓库的版本号，然后 git fetch 获得当前指向的远程分支的后续版本的数据，然后再利用 git merge 将其与本地的当前分支合并。所以可以认为 git pull 是 git fetch 和 git merge 两个步骤的结合。

git pull 的用法如下:

```bash
git pull <远程主机名> <远程分支名>:<本地分支名>
```

因此，与 git pull 相比 git fetch 相当于是从远程获取最新版本到本地，但不会自动 merge。如果需要有选择的合并 git fetch 是更好的选择。效果相同时 git pull 将更为快捷。

标准或完整的命令是 `git pull remote_repository_name branch_name`

```bash
# 除了做了 git fetch origin master:mymaster 的工作外，还会将远程分支 merge 进本地当前分支。
git pull origin <远程分支名>:<本地分支名>
git branch --set-upstream-to=origin/<remote_branch> <local_branch>
git pull
# verbose
git pull -v
git pull origin master
git pull origin branch0
git pull --rebase # rebase the current branch on top of the upstream branch after fetching.
git pull --no-rebase # merge
git config --global pull.rebase true # merge
git config pull.rebase false  # merge
git config pull.rebase true   # rebase
git config pull.ff only       # fast-forward only
git pull --ff-only
```

```bash
man git-fetch
git fetch --prune  #在本地删除在远程不存在的branch
git fetch --all 告诉 Git 同步所有的远端仓库
```

[https://git-scm.com/book/zh/v2/Git-%E5%9F%BA%E7%A1%80-%E6%89%93%E6%A0%87%E7%AD%BE](https://git-scm.com/book/zh/v2/Git-%E5%9F%BA%E7%A1%80-%E6%89%93%E6%A0%87%E7%AD%BE)

## git clone

git clone <版本库的网址> <本地目录名>

```bash
# checkout/clone tag/branch, clone 某个仓库的某个分支
# -b, --[no-]branch <branch>, checkout <branch> instead of the remote's HEAD
git clone --branch <branch or tag name> <repo_url>
git clone -b dev_jk http://10.1.1.11/service/tmall-service.git
git clone -b v1.30.0 https://github.com/foo/bar
# -b 也可以写后面
git clone [git-url] -b [branch-name]

# 如果给 git clone 命令传递 --recurse-submodules 选项，它就会自动初始化并更新仓库中的每一个子模块， 包括可能存在的嵌套子模块。
git clone --recurse-submodules https://github.com/chaconinc/MainProject

#  -j8 is an optional performance optimization that became available in version 2.8, and fetches up to 8 submodules at a time in parallel — see man git-clone.
git clone --recurse-submodules -j8 git://github.com/foo/bar.git

git clone https://user0:password0@git.foo.com/path/to/project.git

### 指定克隆深度

在 git clone 时加上 --depth=1

depth 用于指定克隆深度, 为1即表示只克隆最近一次 commit.

#git checkout main
git switch main

git log --pretty=oneline

git-ls-files  # - Show information about files in the index and the working tree

# list deleted files
git ls-files -d

# 恢复已删除的文件

git ls-files -d | xargs git checkout --

git clone --progress --verbose
```

## git push

```bash
# push <远程仓库名> <本地分支名>:<远程分支名>

# 提交本地 test 分支作为远程的 master 分支
git push origin test:master

# 将本地的 master 分支推送到 origin 主机的 master 分支
git push origin master:master

# 可以省略掉 仓库名, 如果只有一个 origin 仓库, git push <远程仓库名>:<本地分支名>

# 如果本地分支名与远程分支名相同，则可以省略冒号
# 省略冒号简写成这样
git push origin master

# 如果配置了多个远程仓库，则可以使用 -u 选项指定一个默认仓库，以后再执行 git push 就可以不显示的指定仓库了.
git push -u origin master

# -f 强制覆盖到仓库，这会导致仓库中某些记录丢失。
git push -f

# fatal: The current branch production has no upstream branch.
git push --set-upstream origin production

#To push to the branch of the same name on the remote, use
# 已经关联了远程分支, 在本地改名之后, 远程不会改, 删除远程分支之后执行这个命令
git push origin HEAD
```

git am –show-current-patch

## core.autocrlf

core.autocrlf配置
假如你正在Windows上写程序，又或者你正在和其他人合作，他们在Windows上编程，而你却在其他系统上，在这些情况下，你可能会遇到行尾结束符问题。这是因为Windows使用回车和换行两个字符来结束一行，而Mac和Linux只使用换行一个字符。虽然这是小问题，但它会极大地扰乱跨平台协作。

Git可以在你提交时自动地把行结束符 `CRLF` 转换成 LF，而在签出代码时把 LF 转换成 `CRLF`。用 core.autocrlf 来打开此项功能，如果是在 Windows 系统上，把它设置成 true，这样当签出代码时，LF 会被转换成 `CRLF`:

```bash
git config --global core.autocrlf true
```

Linux 或 Mac 系统使用 LF 作为行结束符，因此你不想 Git 在签出文件时进行自地的转换；当一个以 `CRLF` 为行结束符的文件不小心被引入时你肯定想进行修正，把 core.autocrlf 设置成 input 来告诉 Git 在提交时把 `CRLF` 转换成 LF，签出时不转换:

```bash
git config --global core.autocrlf input
```

这样会在Windows系统上的签出文件中保留CRLF，会在Mac和Linux系统上，包括仓库中保留LF。

如果你是Windows程序员，且正在开发仅运行在Windows上的项目，可以设置false取消此功能，把回车符记录在库中:

```bash
git config --global core.autocrlf false
```

## submodule

当你在一个 Git 项目上工作时，你需要在其中使用另外一个Git 项目。也许它是一个第三方开发的Git 库或者是你独立开发和并在多个父项目中使用的。这个情况下一个常见的问题产生了: 你想将两个项目单独处理但是又需要在其中一个中使用另外一个。

在 Git 中你可以用子模块 submodule 来管理这些项目，submodule 允许你将一个 Git 仓库当作另外一个 Git 仓库的子目录。这允许你克隆另外一个仓库到你的项目中并且保持你的提交相对独立。

- 主仓库切换分支之后,子仓库并不会跟着一起切换, 得在主仓库上执行一次 git submodule update

git submodule update --init 将 git submodule init 和 git submodule update 合并成一步。如果还要初始化、抓取并检出任何嵌套的子模块， 请使用简明的 git submodule update --init --recursive。

```bash
# 为已有的 git 仓库增加子模块, 命令执行完成，会在当前工程根路径下生成一个名为“.gitmodules”的文件
git submodule add https://github.com/maonx/vimwiki-assets.git assets

# 已经配置子模块的仓库, 主项目和子模块一起克隆
git clone -b branch0 git@github.com:foo/bar.git --recursive

# 查看子模块, 如果 git submodule 返回的 hash 前面有一个减号, 代表子模块还没有检出, 加号代表 submodule 距离上一次跟主仓库关联的 commit id 有新的 commit, 这时在主仓库里对 submodule 所在的目录做 git add folder0 之后 git submodule 命令返回的数据不再有加号.
# git submodule 返回的 commit id 是当前 submodule 目录当前的 commit id
# commit id 前面 的加号代表远程仓库关联的submodule 有更新, 执行 git submodule update 之后 , submodule 的版本会更新到与远程主仓库关联的submodule commit id 一致.
git submodule
# 比如只克隆了主仓库, submodule所在的目录肯定是空的, 要用这个命令初始化一下 submodule, 然后再执行 git submodule update, submodule 目录就克隆下来了.
git submodule init
# 把submodule 更新到跟远程主仓库关联的 commit id 一致, git status 应该是clear的
git submodule update
# 把 submodule 更新到子仓库最新的 commit id, 这个 commit 有可能跟之前关联的 commit id 不一样, 一般会比之前 关联的 commit id 更新, git status 会看到 submodule 有变更需要提交, 需要更新 关联的 commit id.
git submodule update --remote

```

使用 submodule, 主仓库 git pull 之后, submodule 不会自动更新, 还要检查一下 submodule 的版本, 可能需要执行git submodule update 更新 一下.

### 删除子模块

```bash
rm -rf 子模块目录 删除子模块目录及源码
vi .gitmodules 删除项目目录下.gitmodules文件中子模块相关条目
vi .git/config 删除配置项中子模块相关条目
rm .git/module/* 删除模块下的子模块目录，每个子模块对应一个目录，注意只删除对应的子模块目录即可

```

————————————————
版权声明：本文为CSDN博主「`guotianqing`」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/guotianqing/article/details/82391665](https://blog.csdn.net/guotianqing/article/details/82391665)

### git restore

将在工作空间但是不在暂存区的文件撤销更改

```bash
git restore
```

#### 将暂存区的文件从暂存区撤出，但不会更改文件

```bash
git restore --staged /path/to/file
```

[https://blog.csdn.net/u013493841/article/details/104451987](https://blog.csdn.net/u013493841/article/details/104451987)

### 关闭 ssl 校验

```bash
git config –global http.sslVerify false
```

[https://git-scm.com/docs](https://git-scm.com/docs)

[https://git-scm.com/book/zh/v2](https://git-scm.com/book/zh/v2)

[http://zensheno.blog.51cto.com/2712776/490748](http://zensheno.blog.51cto.com/2712776/490748)  
[http://blog.csdn.net/ithomer/article/details/7529841](http://blog.csdn.net/ithomer/article/details/7529841)  
[http://www.cnblogs.com/springbarley/archive/2012/11/03/2752984.html](http://www.cnblogs.com/springbarley/archive/2012/11/03/2752984.html)  
[http://git-scm.com/book/zh/v1/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6](http://git-scm.com/book/zh/v1/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6)  
[http://yijiebuyi.com/blog/eacf4d053fad77affffae397d9af7172.html](http://yijiebuyi.com/blog/eacf4d053fad77affffae397d9af7172.html)  
[http://www.ruanyifeng.com/blog/2014/06/git_remote.html](http://www.ruanyifeng.com/blog/2014/06/git_remote.html)  
[https://www.liaoxuefeng.com/wiki/896043488029600/900003767775424](https://www.liaoxuefeng.com/wiki/896043488029600/900003767775424)  
[https://blog.csdn.net/riddle1981/article/details/74938111](https://blog.csdn.net/riddle1981/article/details/74938111)  
[https://blog.csdn.net/SCHOLAR_II/article/details/72191042](https://blog.csdn.net/SCHOLAR_II/article/details/72191042)  
[https://www.jianshu.com/p/38f04aef1c9d](https://www.jianshu.com/p/38f04aef1c9d)

>[https://www.jianshu.com/p/9000cd49822c](https://www.jianshu.com/p/9000cd49822c)
>[https://blog.csdn.net/CrazyZhang1990/article/details/42780285](https://blog.csdn.net/CrazyZhang1990/article/details/42780285)

### pre-commit

.git/hook/pre-commit

### create a new repository on the command line

```bash
echo "# jetbrain-eap-installer" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:wiloon/jetbrain-eap-installer.git
git push -u origin main

```

### push an existing repository from the command line

```bash
git remote add origin git@github.com:wiloon/jetbrain-eap-installer.git
git branch -M main
git push -u origin main
```

## 删除大文件

[https://harttle.land/2016/03/22/purge-large-files-in-gitrepo.html](https://harttle.land/2016/03/22/purge-large-files-in-gitrepo.html)

## 按修改次数排序

```bash
git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -20
```

## fatal: refusing to merge unrelated histories

两个分支是两个不同的版本，具有不同的提交历史

```bash
# 允许不相关历史提交，强制合并：
git pull --allow-unrelated-histories

```

原因： "git merge" used to allow merging two branches that have no common base by default, which led to a brand-new history of an existing project created and then get pulled by an unsuspecting maintainer, which allowed an unnecessary parallel history merged into the existing project. The command has been taught not to allow this by default, with an escape hatch "--allow-unrelated-histories" option to be used in a rare event that merges histories of two projects that started their lives independently（stackoverflow）.

作者：勿以浮沙筑高台
链接：[https://www.jianshu.com/p/536080638cc9](https://www.jianshu.com/p/536080638cc9)
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

## Git 删除某个文件的历史记录, 删除 commit 历史

```bash
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch /content/post/archive-2/cross-compile.md' --prune-empty --tag-name-filter cat -- --all

# 本地记录覆盖到 Github, (所有 branch 以及所有 tags)
git push origin --force --all
git push origin --force --tags

# 确保没有什么问题之后, 强制解除对本地存储库中的所有对象的引用和垃圾收集
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
```

————————————————
版权声明：本文为CSDN博主「JAVA|Mr.Java」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/q258523454/article/details/83899911](https://blog.csdn.net/q258523454/article/details/83899911)

## TortoiseGit, ssh key

把 key 转成 ppk 格式 加到 Pageant 里.

[https://www.jianshu.com/p/1bbf5e25c912](https://www.jianshu.com/p/1bbf5e25c912)

## git 没提交的代码迁移到新分支

```bash
// 先将本地修改进行暂存
git stash
 
// 暂存完毕后执行 git status 会显示不出本地的修改
// 再拉取当前分支
git pull 
 
// 新建并切换到开发分支, 如dev-2021-11
# git checkout -b dev-2021-11
git switch dev-2021-11
 
// 将暂存的本地修改取出
git stash apply
 
// 这时执行 git status 可以看到本地修改又显示出来了
// 正常提交即可
git add .
git commit -am "local code"
git push origin dev-2021-11
```

[https://www.cnblogs.com/toutou/p/git_stash.html](https://www.cnblogs.com/toutou/p/git_stash.html)

## There is no tracking information for the current branch

是因为本地分支和远程分支没有建立联系 (使用git branch -vv 可以查看本地分支和远程分支的关联关系) .根据命令行提示只需要执行以下命令即可

git branch --set-upstream-to=origin/远程分支的名字(我的是master) 本地分支的名字(我的是master)

```Bash
git branch --set-upstream-to=origin/master master
```

[https://segmentfault.com/a/1190000009128253](https://segmentfault.com/a/1190000009128253)

## Your branch and 'origin/branch0' have diverged

```r
On branch branch0
Your branch and 'origin/branch0' have diverged,
and have 4 and 2 different commits each, respectively.
  (use "git pull" to merge the remote branch into yours)

nothing to commit, working tree clean
```

[https://segmentfault.com/q/1010000015716120](https://segmentfault.com/q/1010000015716120)

假设，远程上的 commit 是 A -> B
你在 A 电脑上 commit 和 push 之后，远程变成了 A -> B -> C -> D
现在，B 电脑上还是 A -> B。然后你 commit 了，那么 B 电脑上就是 A -> B -> E。

所以，你需要的是把 B 电脑上的历史线变成 A -> B -> C -> D -> E
这时，你需要在 B 电脑上：

git pull --rebase origin dev
这个命令等同于：

git fetch origin
git rebase origin/dev
执行之后，B 电脑上的历史线就会变成 A -> B -> C -> D -> E，然后你就可以 push 了

多说一句，之所以显示上面的“错误”，是因为 A -> B -> C -> D 和 A -> B -> E 有一个共同的祖先 B，你在本地多了一个 commit E，远程多了两个 commits C 和 D。这个时候如果你要在 A -> B -> E 的 branch 上 push，git 猜不出到底想保留 C 和 D，还是只要 E，还是都要，就会出现上面的提示。

## git status, git status -s

```bash
git status
git status -s
```

```bash
XY PATH
XY ORIG_PATH -> PATH
```

- `XY` 是一个双字母的状态代码。
    - `X` 显示索引文件 (index) 的状态
    - `Y` 显示工作树 (working tree) 的状态。
    - ' ' = 空格表示未修改的
    - M = 修改过的
    - U = 更新但未合并
    - ？= 未被追踪的, 未被 git 进行管理，可以使用 git add file0 把 file0 添加进 git, 使其能被 git 进行管理
    - MM: 索引有修改没 commit, working tree 有修改  没 git add
- 当一个路径没有被追踪时，`X`和`Y`总是相同的，因为它们是未知的索引。
- `??` 用于未跟踪的路径。除非使用了 `--ignored`, 文件刚刚被加入一个git管理的目录的时候的状态.
- `AA` 文件加入之后执行了一次 git add
- ` M` 表示工作树有修改但是没有执行 `git add`, 没有更新到索引.
- `M ` 表示索引有更新但是没有提交到 local repo, 没有执行过 `git commit`
- ` D` 从工作树中删除还没有执行 git rm
- `D ` 执行过 git rm 之后, 已经从索引中删除了
- `R ` 有可能是 rename 的缩写, 比如把文件移到了另外一个目录


第一列 M（绿色M）：代表版本库(working tree)和中间状态(staging)有差异。就是工作树版本库和提交到暂存区中文件的差异，意思就是这篇文章中执行 git diff --cached 时出现的差异。最后一次commit提交到工作版本库中的文件和add到暂存区中的文件差别。  
第二列 M（红色M）：代表工作区(working tree)和当前文件状态的差异。就是工作树版本库和本地开发文件的差异，意思就是这篇文章中执行git diff head 时出现的差异。最后一次commit提交到工作树版本库中文件和本地开发文件的差别。

## git credential, 保存凭证/密码/token

```bash
git config --global credential.helper store
git config credential.helper store
# token 默认以明文保存在 ~/.git-credentials
```

## git cherry

- git-cherry - Find commits yet to be applied to upstream
- 查看哪些 commit 还没有 push 到远程分支

```bash
git cherry
git cherry -v
# 比较本地的 asa 分支和远程 master 的差别
git cherry -v origin/master asa
# 比较本地 asa 分支和本地 master 分支之间的差别
git cherry -v master asa
```

[https://www.cnblogs.com/rainbow-tan/p/15314711.html](https://www.cnblogs.com/rainbow-tan/p/15314711.html)

## git cherry-pick

把某一个或几个 commit 应用到当前分支.

比如 commit_id_0 commit_id_1 是 feature0 分支的 commit, 执行 cherry-pick 把它们应用到 main 分支

```bash
# 切换到 main 分支
git cherry-pick commit_id_0 commit_id_1
# 执行过 cherry-pick 之后这两个 commit 默认是提交到了 local repo, 需要 再执行一次  git push
```

## git rerere

Reuse recorded resolution

```bash
git rerere [clear | forget <pathspec>…​ | diff | status | remaining | gc]
```

## `.gitattributes`

[https://zhuanlan.zhihu.com/p/108266134](https://zhuanlan.zhihu.com/p/108266134)

## 已存在的目录转换为一个 GIT 项目并托管到 GITHUB 仓库

```bash
git init
git add .
git commit -m "Initial commit"
#访问 GitHub, 创建一个新仓库
git remote add origin https://github.com/superRaytin/alipay-app-ui.git
#git push origin master
git push -u origin master -f
```

[http://leonshi.com/2016/02/01/add-existing-project-to-github/](http://leonshi.com/2016/02/01/add-existing-project-to-github/)

[http://blog.csdn.net/shiren1118/article/details/7761203](http://blog.csdn.net/shiren1118/article/details/7761203)

## IP-GUARD

[0x7FFA0BF6E0A4] ANOMALY: use of REX.w is meaningless (default operand size is 64)

导致这个问题的原因之一，是因为电脑安装了浪潮的 IP-GUARD 监控软件  
卸载电脑原先的 Git，安装 32位 Git  
或者卸载监控软件
或者修改注册表让 ip guard 不监控 git.exe

## git orphan, 清除 git 所有历史提交记录

1.创建新分支
语法：git checkout --orphan <new_branch>
例句：git checkout --orphan latest_branch

使用 --orphan 选项，可创建1个"清洁"分支(无任何的提交历史，但是当前分支的内容一应俱全。
但严格意义上说，这样创建的分支还不是一个真正的分支，因为HEAD指向的引用中没有commit值，只有在进行一次提交后，它才算得上真正的分支。

作者：萌木盖
链接：https://www.jianshu.com/p/e2b3d04542cb
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```Bash
git checkout --orphan branch0
git add .
# 或 git add -A
git commit -m "message0"
git push --set-upstream origin branch0

# 删除原来的分支(master)
git branch -D master
```

## 修改历史 commit 的 user 和 email

foo.sh

```Bash
#!/bin/sh
git filter-branch --env-filter '
OLD_EMAIL="原来的邮箱"
CORRECT_NAME="现在的名字"
CORRECT_EMAIL="现在的邮箱"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```

```Bash
chmod u+x foo.sh
./foo.sh
git push -f
```

## windows vscode git

vscode 会直接读 c:/user/user0/.ssh/ 里面的私钥, win 下可以在 cmd 里执行 ssh-keygen 生成 密钥对.

## 恢复 github 已经删除的分支

```Bash
# 在 github 按分支名过滤 pr
is:pr is:closed base:branch_0
# 找到 branch_0 作为目录分支的最后一个 pr
# 找到 commit  id
# 从这个 commit id 新建分支 
git branch branch_0 commit_id_0
```
