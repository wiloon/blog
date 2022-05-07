---
title: Linux密码策略
author: "-"
date: 2019-01-25T05:33:44+00:00
url: /?p=13480
categories:
  - Inbox
tags:
  - reprint
---
## Linux密码策略
```bash
authconfig --passminlen=8 --passmaxrepeat=3 --enablereqlower --enablerequpper --enablereqdigit --enablereqother --update
```

基于RHEL的系统 (RHEL CentOS Scientific) 
  
RHEL7,CentOS7,Scientific7
  
设置密码中至少包含一个小写字符,执行命令: 

# authconfig -enablereqlower -update

查看设置: 

# grep "^lcredit" /etc/security/pwquality.conf

设置密码中至少包含一个大写字符,执行命令: 

# authconfig -enablerequpper -update

查看设置: 

# grep "^ucredit" /etc/security/pwquality.conf

设置密码中至少包含一个数字字符,执行命令: 

# authconfig -enablereqdigit -update

查看设置: 

# grep "^dcredit" /etc/security/pwquality.conf

设置密码中至少包含一个特殊字符,执行命令: 

# authconfig -enablereqother -update

查看设置: 

# grep "^ocredit" /etc/security/pwquality.conf

RHEL6,CentOS6,Scientific6
  
编辑 /etc/pam.d/system-auth 文件: 

# vim /etc/pam.d/system-auth

找到如下一行,修改: 

password requisite pam_cracklib.so try_first_pass retry=3 type= minlen=8 dcredit=-1 ucredit=-1 lcredit=-1 ocredit=-1
  
上面配置了密码至少8个字符长,并且分别包含大小写字母、数字和特殊字符。

设置密码过期时间
  
我们设置如下策略: 

一个密码使用的最长天数
  
更改密码最少天数间隔,为了不让用户频繁更改密码
  
在密码过期前多少天提醒用户