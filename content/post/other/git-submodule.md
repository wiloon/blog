---
title: git submodule
author: "-"
date: 2015-01-18T03:38:49+00:00
url: git-submodule
categories:
  - VCS
tags:
  - reprint
  - remix
---
## git submodule

有 submodule 的 git 仓库根目录会有 .gitmodules 文件。

```bash
# check submodule with command
git submodule status
# 有输出就是有 submodule
```

当你在一个 Git 项目上工作时，你需要在其中使用另外一个Git 项目。也许它是一个第三方开发的Git 库或者是你独立开发和并在多个父项目中使用的。这个情况下一个常见的问题产生了: 你想将两个项目单独处理但是又需要在其中一个中使用另外一个。

在 Git 中你可以用子模块 submodule 来管理这些项目，submodule 允许你将一个 Git 仓库当作另外一个 Git 仓库的子目录。这允许你克隆另外一个仓库到你的项目中并且保持你的提交相对独立。

- 主仓库切换分支之后,子仓库并不会跟着一起切换, 得在主仓库上执行一次 git submodule update

git submodule update --init 将 git submodule init 和 git submodule update 合并成一步。如果还要初始化、抓取并检出任何嵌套的子模块， 请使用简明的 git submodule update --init --recursive。

```bash
# 为已有的 git 仓库增加子模块, 命令执行完成，会在当前工程根路径下生成一个名为“.gitmodules”的文件
# enx: 子模块的目录名
git submodule add git@github.com:wiloon/enx.git enx

# 已经配置子模块的仓库, 主项目和子模块一起克隆
git clone -b branch_0 git@github.com:foo/bar.git --recursive

# 查看子模块, 如果 git submodule 返回的 hash 前面有一个减号, 代表子模块还没有检出, 加号代表 submodule 距离上一次跟主仓库关联的 commit id 有新的 commit, 这时在主仓库里对 submodule 所在的目录做 git add folder0 之后 git submodule 命令返回的数据不再有加号.
# git submodule 返回的 commit id 是当前 submodule 目录当前的 commit id
# commit id 前面 的加号代表远程仓库关联的submodule 有更新, 执行 git submodule update 之后 , submodule 的版本会更新到与远程主仓库关联的submodule commit id 一致.
git submodule
# 比如只克隆了主仓库, submodule 所在的目录肯定是空的, 要用这个命令初始化一下 submodule, 然后再执行 git submodule update, submodule 目录就克隆下来了.
git submodule init
# 把submodule 更新到跟远程主仓库关联的 commit id 一致, git status 应该是 clear 的
git submodule update
# 更新指定的 submodule 到远程仓库的最新版本
git submodule update --init --remote <submodule_path>
# 把 submodule 更新到子仓库最新的 commit id, 这个 commit 有可能跟之前关联的 commit id 不一样, 一般会比之前 关联的 commit id 更新, git status 会看到 submodule 有变更需要提交, 需要更新 关联的 commit id.
git submodule update --remote
# 拉取子模块 的代码
git submodule update --init --recursive
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
