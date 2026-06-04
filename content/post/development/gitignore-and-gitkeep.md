---
title: Git 中 .gitignore 与 .gitkeep
author: "-"
date: 2012-02-25T13:43:36+00:00
lastmod: 2026-06-04T15:48:31+08:00
url: gitignore-and-gitkeep
categories:
  - Tools
tags:
  - Git
  - remix
  - AI-assisted

---
## .gitignore

`.gitignore` 用来告诉 Git 哪些文件或目录不需要纳入版本控制。

一般在项目开发过程中会产生很多中间文件（例如构建产物、日志、IDE 临时文件），这些文件不适合提交到仓库。通过 `.gitignore`，可以让 `git status` 更干净，也能减少误提交。

`.gitkeep` 则是另一个常见约定：它通常是一个空文件，放在原本为空的目录里用于占位。因为 Git 只跟踪文件，不直接跟踪空目录，所以如果希望目录结构被保留下来（例如 `logs/`、`tmp/`），就可以在目录中放一个 `.gitkeep` 并提交。

常见组合方式：

```bash
logs/
!logs/.gitkeep
```

上面的规则表示忽略 `logs/` 目录里的运行时文件，但保留 `logs/.gitkeep` 这个占位文件。

### 忽略子目录下所有某后缀的文件

```r
**/*.iml
```

具体使用请看 `man gitignore`。

在需要的目录下面添加 `.gitignore` 文件。

文件中每一行表示一个匹配规则（通常可理解为通配模式）。
  
>cat .gitignore

```bash
.metadata
# ignore obj and lib file
*.[oa]
```

当前的目录情况
  
$ls -al
  
total 24
  
drwxr-xr-x 4 root root 4096 2010-12-11 12:44 .
  
drwx-- 51 root root 4096 2010-12-11 12:44 ..
  
drwxr-xr-x 8 root root 4096 2010-12-11 12:44 .git
  
-rw-r-r- 1 root root 39 2010-12-11 12:44 .gitignore
  
drwxr-xr-x 3 root root 4096 2010-08-19 20:01 .metadata
  
-rw-r-r- 1 root root 52 2010-12-11 12:41 test.txt

如果没有添加该文件，git status会报有这些文件没有track。
  
$git status

# On branch master

# Untracked files

# (use "git add ..." to include in what will be committed)

#

# .metadata/

# gitignore

而 添加了该文件后，就可以看到，这个workspace 就是干净的了。
  
$mv gitignore .gitignore
  
[root@~/workspace]
  
$git status

# On branch master

nothing to commit (working directory clean)

这个.gitignore很简单，当前目录下有个.metadata，这个是我们不需要的，所以就写入了文件。另外如果不加.gitignore这行，git会把.gitignore也加入版本控制中。


```Bash
#注释           .gitignore的注释
*.txt           忽略所有 .txt 后缀的文件
!src.a          忽略除 src.a 外的其他文件
/todo           仅忽略项目根目录下的 todo 文件，不包括 src/todo
build/          忽略 build/目录下的所有文件，过滤整个build文件夹；
doc/*.txt       忽略doc目录下所有 .txt 后缀的文件，但不包括doc子目录的 .txt 的文件
 
bin/:           忽略当前路径下的 bin 文件夹，该文件夹下的所有内容都会被忽略，不忽略 bin 文件
/bin:           忽略根目录下的 bin 文件
/*.c:           忽略 cat.c，不忽略 build/cat.c
debug/*.obj:    忽略debug/io.obj，不忽略 debug/common/io.obj和tools/debug/io.obj
**/foo:         忽略/foo, a/foo, a/b/foo等
a/**/b:         忽略a/b, a/x/b, a/x/y/b等
!/bin/run.sh    不忽略bin目录下的run.sh文件
*.log:          忽略所有 .log 文件
config.js:      忽略当前路径的 config.js 文件
 
/mtk/           忽略整个文件夹
*.zip           忽略所有.zip文件
/mtk/do.c       忽略某个具体文件
```
