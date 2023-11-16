---
title: Git 库空间优化/清理
author: "-"
date: 2012-10-26T04:44:51+00:00
url: git/disk
categories:
  - Git
tags:
  - reprint
---
## Git 库空间优化/清理

git仓库过大会导致哪些问题?

git仓库体积过大,占用电脑本地闪存的存储空间;
clone git仓库时,耗时过长,甚至完全clone不下来导致git报错;
git pull时会由于引用对象过多会报错,导致本地代码无法更新;
在切换分支的时候经常会出现cpu占满,内存占满的情况导致电脑死机;

作者：江霖丶
链接：[https://juejin.cn/post/7024922528514572302](https://juejin.cn/post/7024922528514572302)
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

Git库随着使用时间的延续，空间会不断增长，但实际代码其实只占很小的空间，更多的是git库本身的归档文件，其中包括已删除的文件纪录。Git优化的本质就是清除已删除文件的归档历史，并重写commit记录。

另外可以将git中变化很少，与代码无关的文件移除，如一些资源文件，放到统一的位置，可以减小很大一部分空间占用。

1. 克隆远程库到本地
$ git clone remote-url
用下面的脚本获取所有分支.

# !/bin/bash
for branch in `git branch -a | grep remotes | grep -v HEAD`
do
  git branch --track ${branch##*/} $branchdone
done
现在你拥有了远程git库的完整克隆，可先在本地进行一些测试、验证工作。

2. 分析git库
代码文件一般都很小，Git库的优化主要从大文件入手。
用下面的脚本可以找出git归档记录中排名前十的大文件，包括已删除的文件。

# !/bin/bash
# set -x

# Shows you the largest objects in your repo's pack file

# Written for osx

#

# @see [http://stubbisms.wordpress.com/2009/07/10/git-script-to-show-largest-pack-objects-and-trim-your-waist-line/](http://stubbisms.wordpress.com/2009/07/10/git-script-to-show-largest-pack-objects-and-trim-your-waist-line/)

# @author Antony Stubbs

# set the internal field spereator to line break, so that we can iterate easily over the verify-pack output

IFS=$'\n';

# list all objects including their size, sort by size, take top 10

objects=`git verify-pack -v .git/objects/pack/pack-*.idx | grep -v chain | sort -k3nr | head`

echo "All sizes are in kB. The pack column is the size of the object, compressed, inside the pack file."

output="size,pack,SHA,location"
for y in $objects
do
    # extract the size in bytes
    size=$((`echo $y | cut -f 5 -d ' '`/1024))
    # extract the compressed size in bytes
    compressedSize=$((`echo $y | cut -f 6 -d ' '`/1024))
    # extract the SHA
    sha=`echo $y | cut -f 1 -d ' '`
    # find the objects location in the repository tree
    other=`git rev-list --all --objects | grep $sha`
    #lineBreak=`echo -e "\n"`
    output="${output}\n${size},${compressedSize},${other}"
done

echo -e $output | column -t -s ', '
比较输出结果与现有git库中的文件，可以分为以下3类：

只存在归档于历史中，这部分是已删除的文件，可以直接在归档纪录中抹去。
归档历史和Git库都存在，但可以移除的文件，这部分文件应先从git库中删除，再抹去归档历史的纪录。
正常的代码文件，不作处理。
3. 清理git库
用下面的命令从归档历史中清理已删除的文件，并重写commit记录。

$ git filter-branch --tag-name-filter cat --index-filter 'git rm -r --cached --ignore-unmatch FILENAME ' --prune-empty -f -- --all
将FILENAME替换为文件名，多个以空格分隔， 可以用*匹配目录。
执行完成后，归档历史已经清理完成，但还有一些垃圾文件，用下面的命令清理.

$ rm -rf .git/refs/original/
$ git reflog expire --expire=now --all
$ git gc --prune=now
$ git gc --aggressive --prune=now
ok,到此，大功告成，du -sh . 可以看到成果。

4. push优化后的代码到远处仓库
$ git push origin --force --all
$ git push origin --force --tags
操作前一定做好备份，告知所有成员，优化完成后需要重新clone代码.

文中的脚本和命令参考了下面的文章:
[http://stevelorek.com/how-to-shrink-a-git-repository.html](http://stevelorek.com/how-to-shrink-a-git-repository.html)

作者：真徐小白
链接：[https://www.jianshu.com/p/28a6d82b2085](https://www.jianshu.com/p/28a6d82b2085)
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
