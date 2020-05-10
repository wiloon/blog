---
title: ACL（Access Control List）
author: wiloon
type: post
date: 2019-01-19T11:04:38+00:00
url: /?p=13432
categories:
  - Uncategorized

---
setfacl命令可以用来细分linux下的文件权限。
  
chmod命令可以把文件权限分为u,g,o三个组，而setfacl可以对每一个文件或目录设置更精确的文件权限。
  
换句话说，setfacl可以更精确的控制权限的分配。
  
比如：让某一个用户对某一个文件具有某种权限。

这种独立于传统的u,g,o的rwx权限之外的具体权限设置叫ACL（Access Control List）
  
ACL可以针对单一用户、单一文件或目录来进行r,w,x的权限控制，对于需要特殊权限的使用状况有一定帮助。
  
如，某一个文件，不让单一的某个用户访问。

setfacl 参数
  
Usage: setfacl [-bkndRLP] { -m|-M|-x|-X &#8230; } file &#8230;
    
-m, &#8211;modify=acl modify the current ACL(s) of file(s)
    
-M, &#8211;modify-file=file read ACL entries to modify from file
    
-x, &#8211;remove=acl remove entries from the ACL(s) of file(s)
    
-X, &#8211;remove-file=file read ACL entries to remove from file
    
-b, &#8211;remove-all remove all extended ACL entries
    
-k, &#8211;remove-default remove the default ACL
        
&#8211;set=acl set the ACL of file(s), replacing the current ACL
        
&#8211;set-file=file read ACL entries to set from file
        
&#8211;mask do recalculate the effective rights mask
    
-n, &#8211;no-mask don&#8217;t recalculate the effective rights mask
    
-d, &#8211;default operations apply to the default ACL
    
-R, &#8211;recursive recurse into subdirectories
    
-L, &#8211;logical logical walk, follow symbolic links
    
-P, &#8211;physical physical walk, do not follow symbolic links
        
&#8211;restore=file restore ACLs (inverse of \`getfacl -R&#8217;)
        
&#8211;test test mode (ACLs are not modified)
    
-v, &#8211;version print version and exit
    
-h, &#8211;help this help text

例子：在/test 下建立一个test文件 将权限改为777 并查看其ACL设置
  
[root@localhost ~]# cd /test/
  
[root@localhost test]# touch test.txt
  
[root@localhost test]# echo 123 > test.txt
  
[root@localhost test]# cat test.txt
  
123
  
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
  
-rwxrwxrwx+ 1 root root 0 2月 6 20:40 test.txt //权限的最后多了一个“+”
  
[root@localhost test]# getfacl test.txt

# file: test.txt

# owner: root

# group: root

user::rwx
  
user:handsome:r&#8211; //handsome的权限为r
  
group::rwx
  
mask::rwx
  
other::rwx

通过handsome用户验证一下：
  
[root@localhost test]# su &#8211; handsome
  
[handsome@localhost ~]$ cat /test/test.txt
  
123
  
[handsome@localhost ~]$ echo 456 >> /test/test.txt
  
-bash: /test/test.txt: 权限不够

除了对某个文件的单个用户进行权限设置外，还可以对某个组进行同样的设置：g:[用户组]:[rwx]

还能对有效权限（mask）进行设置：有效权限(mask) 即用户或组所设置的权限必须要存在于mask的权限设置范围内才会生效

最后取消ACL权限：
  
[root@localhost test]# setfacl -x u:handsome test.txt
  
[root@localhost test]# ll
  
总用量 8
  
-rwxrwxrwx+ 1 root root 4 2月 6 20:47 test.txt

删除所有acl
  
[root@localhost test]# setfacl -b test.txt
  
[root@localhost test]# ll
  
总用量 4
  
-rwxrwxrwx. 1 root root 4 2月 6 20:47 test.txt //文件权限后面的“+”没了