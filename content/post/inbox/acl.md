---
title: ACL (Access Control List) 
author: "-"
date: 2019-01-19T11:04:38+00:00
url: /?p=13432
categories:
  - Inbox
tags:
  - reprint
---
## ACL (Access Control List)

https://www.cnblogs.com/sparkdev/p/5536868.html

ACL的全称是 Access Control List (访问控制列表) ，一个针对文件/目录的访问控制列表。它在UGO权限管理的基础上为文件系统提供一个额外的、更灵活的权限管理机制。它被设计为UNIX文件权限管理的一个补充。ACL允许你给任何的用户或用户组设置任何文件/目录的访问权限。

setfacl 命令可以用来细分linux下的文件权限。
  
chmod 命令可以把文件权限分为 u,g,o三个组, 而 setfacl可以对每一个文件或目录设置更精确的文件权限。
  
换句话说, setfacl 可以更精确的控制权限的分配。
  
比如: 让某一个用户对某一个文件具有某种权限。

这种独立于传统的u,g,o的rwx权限之外的具体权限设置叫ACL (Access Control List)
  
ACL 可以针对单一用户、单一文件或目录来进行r,w,x的权限控制,对于需要特殊权限的使用状况有一定帮助。
  
如,某一个文件,不让单一的某个用户访问。

setfacl 参数
  
Usage: setfacl [-bkndRLP] { -m|-M|-x|-X ... } file ...

-m, -modify=acl modify the current ACL(s) of file(s)

-M, -modify-file=file read ACL entries to modify from file

-x, -remove=acl remove entries from the ACL(s) of file(s)

-X, -remove-file=file read ACL entries to remove from file

-b, -remove-all remove all extended ACL entries

-k, -remove-default remove the default ACL

-set=acl set the ACL of file(s), replacing the current ACL

-set-file=file read ACL entries to set from file

-mask do recalculate the effective rights mask

-n, -no-mask don't recalculate the effective rights mask

-d, -default operations apply to the default ACL

-R, -recursive recurse into subdirectories

-L, -logical logical walk, follow symbolic links

-P, -physical physical walk, do not follow symbolic links

-restore=file restore ACLs (inverse of \`getfacl -R')

-test test mode (ACLs are not modified)

-v, -version print version and exit

-h, -help this help text

例子: 在/test 下建立一个test文件 将权限改为777 并查看其ACL设置
  
[root@localhost ~]# cd /test/
  
[root@localhost test]# touch test.txt
  
[root@localhost test]# echo 123 > test.txt
  
[root@localhost test]# cat test.txt
  
[root@localhost test]# chmod 777 test.txt
  
[root@localhost test]# ll
  
总用量 0
  
-rwxrwxrwx. 1 root root 0 2月 6 20:40 test.txt
  
[root@localhost test]# getfacl test.txt

# file: test.txt //文件名

# owner: root //文件所属者

# group: root //文件所属组

user::rwx //文件所属者权限
  
group::rwx //同组用户权限
  
other::rwx /其它者权限

现在我们让handsome用户只有读取的权限

[root@localhost test]# setfacl -m u:handsome:r test.txt
  
[root@localhost test]# ll
  
总用量 4
  
-rwxrwxrwx+ 1 root root 0 2月 6 20:40 test.txt //权限的最后多了一个"+"
  
[root@localhost test]# getfacl test.txt

# file: test.txt

# owner: root

# group: root

user::rwx
  
user:handsome:r- //handsome的权限为r
  
group::rwx
  
mask::rwx
  
other::rwx

通过handsome用户验证一下:
  
[root@localhost test]# su - handsome
  
[handsome@localhost ~]$ cat /test/test.txt
  
[handsome@localhost ~]$ echo 456 >> /test/test.txt
  
-bash: /test/test.txt: 权限不够

除了对某个文件的单个用户进行权限设置外,还可以对某个组进行同样的设置: g:[用户组]:[rwx]

还能对有效权限 (mask) 进行设置: 有效权限(mask) 即用户或组所设置的权限必须要存在于mask的权限设置范围内才会生效

最后取消ACL权限:
  
[root@localhost test]# setfacl -x u:handsome test.txt
  
[root@localhost test]# ll
  
总用量 8
  
-rwxrwxrwx+ 1 root root 4 2月 6 20:47 test.txt

删除所有acl
  
[root@localhost test]# setfacl -b test.txt
  
[root@localhost test]# ll
  
总用量 4
  
-rwxrwxrwx. 1 root root 4 2月 6 20:47 test.txt //文件权限后面的"+"没了
