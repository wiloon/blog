---
title: svn diff
author: "-"
date: 2019-09-02T03:02:47+00:00
url: /?p=14891
categories:
  - Uncategorized

tags:
  - reprint
---
## svn diff
转载于: http://blog.sina.com.cn/s/blog_4e5668630100ag2u.html
              
http://www.upsdn.net/html/2004-12/65.html

$ svn diff -r 2:3 rules.txt
  
(1)Index: rules.txt
  
(2)===================================================================
  
(3)- rules.txt (revision 2)
  
(4)+++ rules.txt (revision 3)
  
(5)@@ -1,4 +1,4 @@
  
(6)Be kind to others
  
(7)-Freedom = Chocolate Ice Cream
  
(8)+Freedom = Responsibility
  
(9)Everything in moderation
  
(10)Chew with your mouth open

第一行，显示文件
  
第二行，分隔符
  
第三行，老版本用"-"表示
  
第四行，新版本用"+"表示
  
第五行，(5)@@ -1,4 +1,4 @@ -表示老版本，+++表示新版本，@@ (老版本) 起始行，行数  (新版本) 起始行，行数 应改为，老版本从第1行开始显示，共显示4行，即显示1~3行； 新版本一样
  
第六行，两个版本都有
  
第七行，只有老版本有
  
第八行，只有新版本有
  
第九行，两个版本都有

# 第十行，两个版本都有

unified diff format统一差异格式
  
一种标准的文件比较格式, 不同的行之前标上'+'或者'-'表示不同的文件, 新文件用'+'表示, 旧文件用'-'表示
  
@@表示不同出现在哪一行

diff -u 可以产生这种格式的补丁文件,它与diff -c命令产生的context diff不一样，后者更适合于大量修改的源代码之间的补丁.
  
前者的好处在于便于人阅读，而且可以直接patch

如何用svn diff来建立一个补丁文件,基本的命令是
  
$svn diff –revision PREV;COMMITTED foo.c
  
PREV是你前一个版本的版本号
  
COMMITTED是你想提交的版本号

$svn diff –revision HEAD
  
显示本地工作文件与服务器上的版本的差异

svn diff foo.c 比较本地修改
  
svn diff -r 3 foo.c 比较工作拷贝和版本库
  
svn diff -r 2:3 foo.c 比较版本库与版本库
  
svn revert 删除你的本地修改,恢复到修改前的状态.