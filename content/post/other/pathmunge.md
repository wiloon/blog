---
title: pathmunge
author: "-"
date: 2012-03-15T06:01:25+00:00
url: /?p=2570
categories:
  - Linux
tags:
  - RedHat

---
## pathmunge
pathmunge是linux系统redhat系列版本系统变量/etc/profile中的函数，如果想要把某个二进制程序可以在所有的shell不用全路径运行，就需要将其所在的目录放在profile中，用过的命令正是pathmunge  (目录命) 


pathmunge{

if ! echo $PATH | /bin/egrep -q "(^|:)$1($|:)";then

if["$2"="after"];then

PATH=$PATH:$1

else

PATH=$1:$PATH

fi

fi

export PATH

}


pathmunge大致的作用是: 判断当前系统的PATH中是否有该命令的目录，如果没有，则判断是要将该目录放于PATH之前还是之后


echo "PATH" 输出PATH变量的内容以供egrep查询，

grep是利用正则表达式来搜索文本的工具，egrep用的是扩展的正则表达式

-q:do not write anything to the standart output

"(^|:)$1($|:)"为要搜索的文本，()和|都是扩展的正则表达式，()查找组，|用或的方式查找字符串，^和$是基础的正则表达式，表示待查找的字符串在开头或结尾，&1是命令所在的目录，整个表达式的意思就是在PATH开头或以: 开头，末尾是文本的末尾或以: 为末尾的该目录

！表示查找的字符串不在PATH中


下来两个if很好理解，如果你想把该目录放于整个PATH变量的后边,pathmunge (目录名) after 则PATH=$PATH:$1,否则PATH=$1:PATH

export 将新设置的变量输出，使其在当前的shell和以后的shell中都生效