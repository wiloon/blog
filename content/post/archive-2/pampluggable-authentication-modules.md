---
title: PAM(Pluggable Authentication Modules)
author: "-"
date: 2017-11-14T06:38:43+00:00
url: /?p=11431
categories:
  - Inbox
tags:
  - reprint
---
## PAM(Pluggable Authentication Modules)
auth: 表示鉴别类接口模块类型用于检查用户和密码,并分配权限；
  
account: 表示账户类接口,主要负责账户合法性检查,确认帐号是否过期,是否有权限登录系统等；
  
session: 会话类接口。实现从用户登录成功到退出的会话控制；
  
password: 口令类接口。控制用户更改密码的全过程。也就是有些资料所说的升级用户验证标记。

system-auth文件是PAM模块的重要配置文件,它主要负责用户登录系统的身份认证工作,不仅如此,其他的应用程序或服务可以通过include接口来调用它 (该文件是system-auth-ac的软链接) 。此外password-auth配置文件也是与身份验证相关的重要配置文件,比如用户的远程登录验证(SSH登录)就通过它调用。而在Ubuntu、SuSE Linux等发行版中,PAM主要配置文件是common-auth、common-account、common-password、common-session这四个文件,所有的应用程序和服务的主要PAM配置都可以通过它们来调用。

http://www.infoq.com/cn/articles/linux-pam-one

Linux中pam_cracklib.so的minlen和credit参数
  
Linux中的PAM(Pluggable Authentication Modules)包含很多有用的模块,其中pam_cracklib.so模块可以配置密码长度复杂度的需求。一般需要同时配置/etc/pam.d/目录中的system-auth和password-auth文件,例如下面

password requisite pam_cracklib.so try_first_pass retry=3 type= ocredit=2 minlen=10
  
限定密码长度主要涉及minlen参数,以及ucredit lcredit dcredit ocredit这四个credit参数,分别表示大写字符、小写字符、数字、其它字符的额外credit值。

这里的minlen=10实际上表示最小分数为10,而不是简单的最小长度为10。密码每有一个任意字符会有一分,另外,ucredit/lcredit/dcredit/ocredit默认值均为1,表示密码中四种字符的类别数,每多一种,就会得到额外的一分。

在这里,ocredit=2 minlen=10,也就是说,如果密码全是其它字符的话,最少需要minlen - ocredit = 10-2 = 8位；若密码包含其它字符和小写字符,最少需要minlen - ocredit - lcredit = 10-2-1 = 7位字符,以此类推。

另外ucredit/lcredit/dcredit/ocredit参数的值如果为负数,例如dcredit=-2,则表示密码中最少需要2位数字。

另外,除了密码长度之外,pam_cracklib.so库默认还会做其它方面的简单检查,并且库代码里写死了密码最小长度不能小于6.

reference

http://www.deer-run.com/~hal/sysadmin/pam_cracklib.html
  
http://www.infoq.com/cn/articles/linux-pam-one