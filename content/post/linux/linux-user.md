---
title: linux user, group, 用户 用户组
author: "-"
date: 2011-09-25T09:49:33+00:00
url: user
categories:
  - Linux
tags:
  - reprint
---
## linux user, group, 用户 用户组

## 用户

### 查看用户

cat /etc/passwd

wyue:x:513:513::/home/wyue:/bin/bash  
看第三个参数: 500 以上的，就是后来建的用户了。其它则为系统的用户。

```bash
# create user, 创建目录 /home/user0, 默认 bash
sudo useradd -m user0

sudo useradd -m -s /bin/bash user0
# create group and user
sudo useradd -m -s /bin/bash -g group0 user0
sudo passwd user0

sudo useradd -m -s /bin/zsh user0
sudo useradd -M -s /bin/false user1
sudo useradd user0
```

```bash
# -m: create home folder, 不加 -m 参数，默认不创建 home
# -M - Don't create a home directory
# -s: specify shell for user, 默认是 /bin/bash
# -s /bin/false - Don't assign a shell (or more accurately, make the shell /bin/false, so the user cannot be logged into)
# -r: create system account
# -d: home dir
# -r - Make a system user
# -g <群组>: 指定用户所属的群组；
# -G <群组>: 指定用户所属的附加群组
# -c <备注>：加上备注文字。备注文字会保存在 passwd 的备注栏位中；
```

### 删除用户

userdel -r test

```bash
-r, 删除用户home目录
```

## 创建密码

sudo passwd user0
输入密码: 一般密码至少要有六个字符，这里输入的密码是看不见的，屏幕没显示
重新输一次密码:

## 切换用户

su -

## group, 用户组

/etc/group 的内容包括用户组 (Group)

```bash
# 查看当前用户所属的组
groups
id user0

# 查看用户所属的组
groups user0

# 把 user0 加入 group0
usermod -a -G group0 user0

# 把 用户的组 切换到 group0, 用户会被从现有的 group 里删除!
usermod -G group0
```

## usermod

Add the john account to the sales group

```bash
# add user to docker group
sudo usermod -aG docker $USER
```

## linux 用户 组

```bash

# 查看所有的组, /etc/group 的内容包括用户组 (Group) 
cat /etc/group

# 创建组
groupadd group0

# create a system account
groupadd -r group0

# Create a group named "test", groupadd [-g GID] GROUP
groupadd -g 2000 dba

# delete group
groupdel  group0
# gpasswd 命令是 Linux 下 组文件 /etc/group 和 /etc/gshadow 的管理工具。

# 把用户加入组, 把用户 user0 加入 group0 组
gpasswd -a user0 group0

# 把用户移出docker组
gpasswd -d ${USER} docker
# -a: 添加用户到组；
# -d: 从组删除用户；
# -A: 指定管理员；
# -M: 指定组成员和-A的用途差不多；
# -r: 删除密码；
# -R: 限制用户登入组，只有组中的成员才可以用newgrp加入该组。
```

groups

/etc/group文件包含所有组

禁止用户登录
  
usermod -s /sbin/nologin user0

应用举例:
  
1. 将 newuser2 添加到组 staff 中

usermod -G staff newuser2

1. 修改 newuser 的用户名为 newuser1

usermod -l newuser1 newuser

1. 锁定账号 newuser1

usermod -L newuser1

1. 解除对 newuser1 的锁定

usermod -U newuser1

功能说明: 修改用户帐号。

语法: `usermod [-LU][-c <备注>][-d <登入目录>][-e <有效期限>][-f <缓冲天数>][-g <群组>][-G <群组>][-l <帐号名称>][-s <shell>][-u <uid>][用户帐号]`

补充说明: usermod可用来修改用户帐号的各项设定。

### 参数

-a, append
  
-c<备注> 修改用户帐号的备注文字。
  
-d登入目录> 修改用户登入时的目录。
  
-e<有效期限> 修改帐号的有效期限。
  
-f<缓冲天数> 修改在密码过期后多少天即关闭该帐号。
  
-g<群组> 修改用户所属的群组。
  
-G<群组> 修改用户所属的附加群组。
  
-l<帐号名称> 修改用户帐号名称。
  
-L 锁定用户密码,使密码无效。
  
-s `<shell>` 修改用户登入后所使用的shell。
  
-u `<uid>` 修改用户ID。
  
-U 解除密码锁定。

## su command

su 命令来自英文单词 switch user 的缩写，其功能是用于切换用户身份。管理员切换至任意用户身份而无须密码验证，而普通用户切换至任意用户身份均需密码验证。另外添加单个减号（-）参数为完全的身份变更，不保留任何之前用户的环境变量信息。
原文链接：[https://www.linuxcool.com/su](https://www.linuxcool.com/su)

在Linux下创建用户和删除用户，必须在root用户下，如果你当前不是用根用户登录，你可以打开终端，输入"su root"命令，再输入根口令，就可以进入root用户模式下。

查看用户是否过期

chage -l user0

(su为switch user，即切换用户的简写)

格式: su -l USERNAME (-l为login，即登陆的简写)

-l可以将l省略掉，所以此命令常写为su - USERNAME

如果不指定USERNAME (用户名) ，默认即为root，所以切换到root的身份的命令即为: su -root或是直接 su -

实例1: 普通用户user1知道root账户登录密码，要求用户user1在不注销登录的前提下查看/etc/shadow文件。

### su - 与 su

通过 su 切换用户还可以直接使用命令 su USERNAME，与 su - USERNAME 的不同之处如下:

su - USERNAME 切换用户后，同时切换到新用户的工作环境中

su USERNAME 切换用户后，不改变原用户的工作目录，及其他环境变量目录

1. 删除用户 (userdel命令)
  
语法: userdel [-r] [要删除的用户的名称]
  
例如: [root@localhost ~]userdel -r aillo

/usr/sbin/useradd

用户 (User) 和用户组 (Group) 的配置文件，是系统管理员最应该了解和掌握的系统基础文件之一，从另一方面来说，了解这些文件也是系统安全管理的重要组成部份；做为一个合格的系统管理员应该对用户和用户组配置文件透彻了解才行；

一、用户 (User) 相关；

谈到用户，就不得不谈用户管理，用户配置文件，以及用户查询和管理的控制工具；用户管理主要通过修改用户配置文件完成；用户管理控制工具最终目的也是为了修改用户配置文件。

什么是用户查询和管理控制工具呢？用户查询和控制工具是查询、添加、修改和删除用户等系统管理工具，比如查询用户的id和finger命令，添加用 户的useradd 或adduser 、userdel 用户的删除 、设置密码的passwd命令 、修改用户usermod 等等；我们需要知道的是通过用户查询和控制工具所进行的动作的最终目的也是修改用户配置文件；所以我们进行用户管理的时候，直接修改用户配置文件一样可以 达到用户管理的目的；

通过上面的解说，我们能实实在在的感觉到用户 (User) 配置文件的重要性；其实用户和用户组在系统管理中是不可分割的，但为了说明问题，我们还是 得把用户 (User) 的配置文件单列出来解说，其中包括/etc/passwd 和/etc/shadow 文件；在这之中，你还能了解UID的重要性；

通过本标题，您可以了解或掌握的内容有: 了解/etc/passwd和/etc/shadow；什么UID ；

与用户相关的系统配置文件主要有/etc/passwd 和/etc/shadow，其中/etc/shadow是用户资讯的加密文件，比如用户的密码口令的加密保存等；/etc/passwd 和/etc/shadow 文件是互补的；我们可以通过对比两个文件来差看他们的区别；

1. 关于/etc/passwd 和 UID；

/etc/passwd 是系统识别用户的一个文件，做个不恰当的比喻，/etc/passwd 是一个花名册，系统所有的用户都在这里有登录记载；当我们以beinan 这个账号登录时，系统首先会查阅 /etc/passwd 文件，看是否有beinan 这个账号，然后确定beinan的UID，通过UID 来确认用户和身份，如果存在则读取/etc/shadow 影子文件中所对应的beinan的密码；如果密码核实无误则登录系统，读取用户的配置文件；

1) /etc/passwd 的内容理解:

在/etc/passwd 中，每一行都表示的是一个用户的信息；一行有7个段位；每个段位用:号分割，比如下面是我的系统中的/etc/passwd 的两行；

beinan:x:500:500:beinan sun:/home/beinan:/bin/bash
  
linuxsir:x:505:502:linuxsir open,linuxsir office,13898667715:/home/linuxsir:/bin/bash
  
beinan:x:500:500:beinan sun:/home/beinan:/bin/bash
  
linuxsir:x:501:502::/home/linuxsir:/bin/bash
  
第一字段: 用户名 (也被称为登录名) ；在上面的例子中，我们看到这两个用户的用户名分别是 beinan 和linuxsir；
  
第二字段: 口令；在例子中我们看到的是一个x，其实密码已被映射到/etc/shadow 文件中；
  
第三字段: UID ；请参看本文的UID的解说；
  
第四字段: GID；请参看本文的GID的解说；
  
第五字段: 用户名全称，这是可选的，可以不设置，在beinan这个用户中，用户的全称是beinan sun ；而linuxsir 这个用户是没有设置全称；
  
第六字段: 用户的家目录所在位置；beinan 这个用户是/home/beinan ，而linuxsir 这个用户是/home/linuxsir ；
  
第七字段: 用户所用SHELL 的类型，beinan和linuxsir 都用的是 bash ；所以设置为/bin/bash ；

关于UID 的理解:

UID 是用户的ID 值，在系统中每个用户的UID的值是唯一的，更确切的说每个用户都要对应一个唯一的UID ，系统管理员应该确保这一规则。系统用户的UID的值从0开始，是一个正整数，至于最大值可以在/etc/login.defs 可以查到，一般Linux发行版约定为60000； 在Linux 中，root的UID是0，拥有系统最高权限；

UID 在系统唯一特性，做为系统管理员应该确保这一标准，UID 的唯一性关系到系统的安全，应该值得我们关注！比如我在/etc/passwd 中把beinan的UID 改为0后，你设想会发生什么呢？beinan这个用户会被确认为root用户。beinan这个帐号可以进行所有root的操作；

UID 是确认用户权限的标识，用户登录系统所处的角色是通过UID 来实现的，而非用户名，切记；把几个用户共用一个UID 是危险的，比如我们上面所谈到的，把普通用户的UID 改为0，和root共用一个UID ，这事实上就造成了系统管理权限的混乱。如果我们想用root权限，可以通过su或sudo来实现；切不可随意让一个用户和root分享同一个UID ；

UID是唯一性，只是要求管理员所做的，其实我们修改/etc/passwd 文件，可以修改任何用户的UID的值为0，

一般情况下，每个Linux的发行版都会预留一定的UID和GID给系统虚拟用户占用，虚拟用户一般是系统安装时就有的，是为了完成系统任务所必须的用户，但虚拟用户是不能登录系统的，比如ftp、nobody、adm、rpm、bin、shutdown等；

在Fedora 系统会把前499 个UID和GID 预留出来，我们添加新用户时的UID 从500开始的，GID也是从500开始，至于其它系统，有的系统可能会把前999UID和GID预留出来；以各个系统中/etc/login.defs 中的 UID_MIN 的最小值为准； Fedora 系统 login.defs的UID_MIN是500，而UID_MAX 值为60000，也就是说我们通过adduser默认添加的用户的UID的值是500到60000之间；而Slackware 通过adduser不指定UID来添加用户，默认UID 是从1000开始；

1. 关于/etc/shadow ；

2. /etc/shadow 概说；

/etc/shadow文件是/etc/passwd 的影子文件，这个文件并不由/etc/passwd 而产生的，这两个文件是应该是对应互补的；shadow内容包括用户及被加密的密码以及其它/etc/passwd 不能包括的信息，比如用户的有效期限等；这个文件只有root权限可以读取和操作，权限如下:

-r——– 1 root root 1.5K 10月 16 09:49 /etc/shadow
  
/etc/shadow 的权限不能随便改为其它用户可读，这样做是危险的。如果您发现这个文件的权限变成了其它用户组或用户可读了，要进行检查，以防系统安全问题的发生；

如果我们以普通用户查看这个文件时，应该什么也查看不到，提示是权限不够:

[beinan@localhost ~]$ more /etc/shadow
  
/etc/shadow: 权限不够

/etc/shadow 的内容分析；

/etc/shadow 文件的内容包括9个段位，每个段位之间用:号分割；我们以如下的例子说明；

beinan:$VE.Mq2Xfc9Qi7EQ9JP8GKF8gH7PB1:13072:0:99999:7:::
  
linuxsir:$IPDvUhXPR6J/VtPXvLyXxhLWPrnt/:13072:0:99999:7::13108:
  
第一字段: 用户名 (也被称为登录名) ，在/etc/shadow中，用户名和/etc/passwd 是相同的，这样就把passwd 和shadow中用的用户记录联系在一起；这个字段是非空的；
  
第二字段: 密码 (已被加密) ，如果是有些用户在这段是x，表示这个用户不能登录到系统；这个字段是非空的；用户组密码，这个段可以是空的或!，如果是空的或有!，表示没有密码,星号代表帐号被锁定,双叹号表示这个密码已经过期了.
  
第三字段: 上次修改口令的时间；这个时间是从1970年01月01日算起到最近一次修改口令的时间间隔 (天数) ，您可以通过passwd 来修改用户的密码，然后查看/etc/shadow中此字段的变化；
  
第四字段: 两次修改口令间隔最少的天数；如果设置为0,则禁用此功能；也就是说用户必须经过多少天才能修改其口令；此项功能用处不是太大；默认值是通过/etc/login.defs文件定义中获取，PASS_MIN_DAYS 中有定义；
  
第五字段: 两次修改口令间隔最多的天数；这个能增强管理员管理用户口令的时效性，应该说在增强了系统的安全性；如果是系统默认值，是在添加用户时由/etc/login.defs文件定义中获取，在PASS_MAX_DAYS 中定义；
  
第六字段: 提前多少天警告用户口令将过期；当用户登录系统后，系统登录程序提醒用户口令将要作废；如果是系统默认值，是在添加用户时由/etc/login.defs文件定义中获取，在PASS_WARN_AGE 中定义；
  
第七字段: 在口令过期之后多少天禁用此用户；此字段表示用户口令作废多少天后，系统会禁用此用户，也就是说系统会不能再让此用户登录，也不会提示用户过期，是完全禁用；
  
第八字段: 用户过期日期；此字段指定了用户作废的天数 (从1970年的1月1日开始的天数) ，如果这个字段的值为空，帐号永久可用；
  
第九字段: 保留字段，目前为空，以备将来Linux发展之用；

如果更为详细的，请用 man shadow来查看帮助，您会得到更为详尽的资料；

我们再根据实例分析:

beinan:$VE.Mq2Xfc9Qi7EQ9JP8GKF8gH7PB1:13072:0:99999:7:::
  
linuxsir:$IPDvUhXPR6J/VtPXvLyXxhLWPrnt/:13072:0:99999:7::13108:
  
第一字段: 用户名 (也被称之为登录名) ，在例子中有峡谷两条记录，也表示有两个用户beinan和linuxsir
  
第二字段: 被加密的密码，如果有的用户在此字段中是x，表示这个用户不能登录系统，也可以看作是虚拟用户，不过虚拟用户和真实用户都是相对的，系统管理员随时可以对任何用户操作；
  
第三字段: 表示上次更改口令的天数 (距1970年01月01日) ，上面的例子能说明beinan和linuxsir这两个用户，是在同一天更改了用户密码，当然是通过passwd 命令来更改的，更改密码的时间距1970年01月01日的天数为13072；
  
第四字段: 禁用两次口令修改之间最小天数的功能，设置为0
  
第五字段: 两次修改口令间隔最多的天数，在例子中都是99999天；这个值如果在添加用户时没有指定的话，是通过/etc/login.defs来获取默认值，PASS_MAX_DAYS 99999；您可以查看/etc/login.defs来查看，具体的值；
  
第六字段: 提 前多少天警告用户口令将过期；当用户登录系统后，系统登录程序提醒用户口令将要作废；如果是系统默认值，是在添加用户时由/etc/login.defs 文件定义中获取，在PASS_WARN_AGE 中定义；在例子中的值是7 ，表示在用户口令将过期的前7天警告用户更改期口令；
  
第七字段: 在口令过期之后多少天禁用此用户；此字段表示用户口令作废多少天后，系统会禁用此用户，也就是说系统会不能再让此用户登录，也不会提示用户过期，是完全禁用；在例子中，此字段两个用户的都是空的，表示禁用这个功能；
  
第八字段: 用 户过期日期；此字段指定了用户作废的天数 (从1970年的1月1日开始的天数) ，如果这个字段的值为空，帐号永久可用；在例子中，我们看到beinan这 个用户在此字段是空的，表示此用户永久可用；而linuxsir这个用户表示在距1970年01月01日后13108天后过期，算起来也就是2005年 11月21号过期；哈哈，如果有兴趣的的弟兄，自己来算算，大体还是差不多的;)；
  
第九字段: 保留字段，目前为空，以备将来Linux发展之用；

二、关于用户组；

具有某种共同特征的用户集合起来就是用户组 (Group) 。用户组 (Group) 配置文件主要有 /etc/group和/etc/gshadow，其中/etc/gshadow是/etc/group的加密信息文件；在本标题下，您还能了解到什么是GID ；

1. /etc/group 解说；
/etc/group 文件是用户组的配置文件，内容包括用户和用户组，并且能显示出用户是归属哪个用户组或哪几个用户组，因为一个用户可以归属一个或多个不同的用户组；同一用 户组的用户之间具有相似的特征。比如我们把某一用户加入到root用户组，那么这个用户就可以浏览root用户家目录的文件，如果root用户把某个文件 的读写执行权限开放，root用户组的所有用户都可以修改此文件，如果是可执行的文件 (比如脚本) ，root用户组的用户也是可以执行的；

用户组的特性在系统管理中为系统管理员提供了极大的方便，但安全性也是值得关注的，如某个用户下有对系统管理有最重要的内容，最好让用户拥有独立的用户组，或者是把用户下的文件的权限设置为完全私有；另外root用户组一般不要轻易把普通用户加入进去，

/etc/group 内容具体分析

/etc/group 的内容包括用户组 (Group) 、用户组口令、GID及该用户组所包含的用户 (User) ，每个用户组一条记录；格式如下:

group_name:passwd:GID:user_list
  
在/etc/group 中的每条记录分四个字段:

第一字段: 用户组名称；
  
第二字段: 用户组密码；
  
第三字段: GID
  
第四字段: 用户列表，每个用户之间用,号分割；本字段可以为空；如果字段为空表示用户组为GID的用户名；

我们举个例子:

root:x:0:root,linuxsir 注: 用户组root，x是密码段，表示没有设置密码，GID是0,root用户组下包括root、linuxsir以及GID为0的其它用户 (可以通过/etc/passwd查看) ；；
  
beinan:x:500:linuxsir 注: 用户组beinan，x是密码段，表示没有设置密码，GID是500,beinan用户组下包括linuxsir用户及GID为500的用户 (可以通过/etc/passwd查看) ；
  
linuxsir:x:502:linuxsir 注: 用户组linuxsir，x是密码段，表示没有设置密码，GID是502,linuxsir用户组下包用户linuxsir及GID为502的用户 (可以通过/etc/passwd查看) ；
  
helloer:x:503: 注: 用户组helloer，x是密码段，表示没有设置密码，GID是503,helloer用户组下包括GID为503的用户，可以通过/etc/passwd查看；
  
而/etc/passwd 对应的相关的记录为:

root:x:0:0:root:/root:/bin/bash
  
beinan:x:500:500:beinan sun:/home/beinan:/bin/bash
  
linuxsir:x:505:502:linuxsir open,linuxsir office,13898667715:/home/linuxsir:/bin/bash
  
helloer:x:502:503::/home/helloer:/bin/bash
  
由此可以看出helloer用户组包括 helloer用户；所以我们查看一个用户组所拥有的用户，可以通过对比/etc/passwd和/etc/group来得到；

1. 关于GID ；

GID和UID类似，是一个正整数或0，GID从0开始，GID为0的组让系统付予给root用户组；系统会预留一些较靠前的GID给系统虚拟用户  (也被称为伪装用户) 之用；每个系统预留的GID都有所不同，比如Fedora 预留了500个，我们添加新用户组时，用户组是从500开始的；而Slackware 是把前100个GID预留，新添加的用户组是从100开始；查看系统添加用户组默认的GID范围应该查看 /etc/login.defs 中的 GID_MIN 和GID_MAX 值；

我们可以对照/etc/passwd和/etc/group 两个文件；我们会发现有默认用户组之说；我们在 /etc/passwd 中的每条用户记录会发现用户默认的GID ；在/etc/group中，我们也会发现每个用户组下有多少个用户；在创建目录和文件时，会使用默认的用户组；我们还是举个例子；

比如我把linuxsir 加为root用户组，在/etc/passwd 和/etc/group 中的记录相关记录为:
  
linuxsir用户在 /etc/passwd 中的记录；我们在这条记录中看到，linuxsir用户默认的GID为502；而502的GID 在/etc/group中查到是linuxsir用户组；

linuxsir:x:505:502:linuxsir open,linuxsir office,13898667715:/home/linuxsir:/bin/bash
  
linuxsir 用户在 /etc/group 中的相关记录；在这里，我们看到linuxsir用户组的GID 为502，而linuxsir 用户归属为root、beinan用户组；

root:x:0:root,linuxsir
  
beinan:x:500:linuxsir
  
linuxsir:x:502:linuxsir
  
我们用linuxsir 来创建一个目录，以观察linuxsir用户创建目录的权限归属；

[linuxsir@localhost ~]$ mkdir testdir
  
[linuxsir@localhost ~]$ ls -lh
  
总用量 4.0K
  
drwxrwxr-x 2 linuxsir linuxsir 4.0K 10月 17 11:42 testdir
  
通过我们用linuxsir 来创建目录时发现，testdir的权限归属仍然是linuxsir用户和linuxsir用户组的；而没有归属root和beinan用户组，明白了吧；

但值得注意的是，判断用户的访问权限时，默认的GID 并不是最重要的，只要一个目录让同组用户可以访问的权限，那么同组用户就可以拥有该目录的访问权，在这时用户的默认GID 并不是最重要的；

/etc/gshadow 解说；

/etc/gshadow是/etc/group的加密资讯文件，比如用户组 (Group) 管理密码就是存放在这个文件。/etc/gshadow 和/etc/group是互补的两个文件；对于大型服务器，针对很多用户和组，定制一些关系结构比较复杂的权限模型，设置用户组密码是极有必要的。比如我 们不想让一些非用户组成员永久拥有用户组的权限和特性，这时我们可以通过密码验证的方式来让某些用户临时拥有一些用户组特性，这时就要用到用户组密码；

/etc/gshadow 格式如下，每个用户组独占一行；
  
groupname:password:admin,admin,…:member,member,…
  
第一字段: 用户组
  
第三字段: 用户组管理者，这个字段也可为空，如果有多个用户组管理者，用,号分割；
  
第四字段: 组成员，如果有多个成员，用,号分割；

举例:

beinan:!::linuxsir
  
linuxsir:oUS/q7NH75RhQ::linuxsir
  
第一字段: 这个例子中，有两个用户组beinan用linuxsir
  
第二字段: 用户组的密码，beinan用户组无密码；linuxsir用户组有已经，已经加密；
  
第三字段: 用户组管理者，两者都为空；
  
第 四字段: beinan用户组所拥有的成员是linuxsir ，然后还要对照一下/etc/group和/etc/passwd 查看是否还有其它用户，一般默认添加的用户，有时同时也会创建用户组和用户名同名称； linuxsir 用户组有成员linuxisir ；

如何设置用户组的密码？ 我们可以通过 gpasswd 来实现；不过一般的情况下，没有必要设置用户组的密码；不过自己实践一下也有必要；下面是一个为linuxsir用户组设置密码的例子；

gpasswd 的用法:  gpasswd 用户组

root@localhost ~]# gpasswd linuxsir
  
正在修改 linuxsir 组的密码
  
新密码:
  
请重新输入新密码:
  
用户组之间的切换，应该用 newgrp ，这个有点象用户之间切换的su ；我先举个例子:
  
[beinan@localhost ~]$ newgrp linuxsir
  
密码:
  
[beinan@localhost ~]$ mkdir lingroup
  
[beinan@localhost ~]$ ls -ld lingroup/
  
drwxr-xr-x 2 beinan linuxsir 4096 10月 18 15:56 lingroup/
  
[beinan@localhost ~]$ newgrp beinan
  
[beinan@localhost ~]$ mkdir beinangrouptest
  
[beinan@localhost ~]$ ls -ld beinangrouptest
  
drwxrwxr-x 2 beinan beinan 4096 10月 18 15:56 beinangrouptest
  
说明: 我是以beinan用户组切换到linuxsir用户组，并且建了一个目录，然后再切换回beinan用户组，又建了一个目录，请观察两个目录属用户组的不同；还是自己体会吧；

三、通过用户和用户组配置文件来查询或管理用户；

1. 用户和用户组查询的方法；

通过查看用户 (User) 和用户组的配置文件的办法来查看用户信息

我们已经用户 (User) 和用户组 (Group) 的配置文件已经有个基本的了解，通过查看用户 (User) 和用户组的配置文件，我们就能做到对系统用户的了解，当然您也可以通过id 或finger 等工具来进行用户的查询等任务。

对于文件的查看，我们可以通过 more 或cat 来查看，比如 more /etc/passwd 或cat /etc/passwd ；其它工具也一样，能对文本查看就行，比如less 也好

比如我们可以通过more 、cat 、less命令对/etc/passwd 的查看，虽然命令不同，但达到的目的是一样的， 都是得到/etc/passwd 的内容；

[root@localhost ~]# more /etc/passwd
  
[root@localhost ~]# cat /etc/passwd
  
[root@localhost ~]# less /etc/passwd

1) 通过id和finger 工具来获取用户信息；
  
除了直接查看用户 (User) 和用户组 (Group) 配置文件的办法除外，我们还有id和finger工具可用，我们一样通过命令行的操作，来完成 对用户的查询；id和finger，是两个各有测重的工具，id工具更测重用户、用户所归属的用户组、UID 和GID 的查看；而finger 测重用户资讯的查询，比如用户名 (登录名) 、电话、家目录、登录SHELL类型、真实姓名、空闲时间等等；

id 命令用法；

id 选项 用户名
  
比如: 我想查询beinan和linuxsir 用户的UID、GID 以及归属用户组的情况:
  
[root@localhost ~]# id beinan
  
uid=500(beinan) gid=500(beinan) groups=500(beinan)
  
注: beinan的UID 是 500，默认用户组是beinan，默认用户组的GID 是500,归属于beinan用户组；
  
[root@localhost ~]# id linuxsir
  
uid=505(linuxsir) gid=502(linuxsir) groups=502(linuxsir),0(root),500(beinan)
  
注: linuxsir的UID 是505,默认用户组是linuxsir ，默认用户组的GID 是502，归属于linuxsir (GID为502) 、root (GID为0) ，beinan (GID为500) ；
  
关于id的详细用法，我会在专门用户查询的文章来介绍；您可以通过man id 来查看用法，用起来还是比较简单的；

finger 的用法
  
finger 选项 用户名1 用户名2 …
  
详细用法请参看man finger ；关于更为详细用法，我会在专门用户查询的文章来介绍；

如果finger 不加任何参数和用户，会显示出当前在线用户，和w命令类似；对比一下；不过各有测重；

[root@localhost ~]# w
  
14:02:42 up 1:03, 3 users, load average: 0.04, 0.15, 0.18
  
USER TTY FROM LOGIN@ IDLE JCPU PCPU WHAT
  
linuxsir tty1 – 13:39 22:51 0.01s 0.01s -bash
  
beinan tty2 – 13:53 8:48 11.62s 0.00s /bin/sh /usr/X1
  
beinan pts/0 :0.0 13:57 0.00s 0.14s 1.08s gnome-terminal
  
[root@localhost ~]# finger
  
Login Name Tty Idle Login Time Office Office Phone
  
beinan beinan sun tty2 8 Oct 18 13:53
  
beinan beinan sun pts/0 Oct 18 13:57 (:0.0)
  
linuxsir linuxsir open tty1 22 Oct 18 13:39 linuxsir o +1-389-866-771
  
如果我们在finger 后面加上用户名，就可以看到用户更为详细的信息，可以一次查看多个用户，用空格分开，比如下面的例子中，我们一次查询两个用户beinan和linuxsir的信息；

[root@localhost ~]# finger beinan linuxsir
  
Login: beinan 注: 用户名 (也是登录名)  Name: beinan sun  (用户名全称)
  
Directory: /home/beinan 注: 家目录 Shell: /bin/bash 注: 所用SHELL类型
  
On since Tue Oct 18 13:53 (CST) on tty2 10 minutes 55 seconds idle 注: 空闲时间；
  
On since Tue Oct 18 13:57 (CST) on pts/0 from :0.0
  
No mail.
  
No Plan.
  
Login: linuxsir Name: linuxsir open
  
Directory: /home/linuxsir Shell: /bin/bash
  
Office: linuxsir office, +1-389-866-7715
  
On since Tue Oct 18 13:39 (CST) on tty1 24 minutes 58 seconds idle
  
No mail.
  
No Plan.

用户组查询的办法；

我们可以通过用户来查询所归属的组，用groups 来查询；比如我查询beinan和linuxsir 所归属的组，我们可以用groups 来查询；

[root@localhost ~]# groups beinan linuxsir
  
beinan : beinan
  
linuxsir : linuxsir root beinan
  
注: 这是通过groups 同时查看了用户beinan和linuxsir所归属的组；

1. 通过修改用户 (User) 和用户组 (Group) 配置文件的办法来添加；

由于我们已经在前面说过，可以通过修改配置文件的办法来管理用户，所以此主题应该包括此内容；当然通过用户及用户组管理工具 (比如 adduser、userdel、usermod 、userinfo、groupadd 、groupdel 、groupmod等) 也是可以的

通过修改用户 (User) 和用户组 (Group) 配置文件的方法管理用户之用户的添加流程；

我们先以添加用户为例，对用户的删除和修改都比较简单；

1) 修改 /etc/passwd ，添加用户记录；

我们按/etc/passwd的格式的约定来添加新的用户记录；当然您要让一个用户失效，可以删除您想要删除的用户记录；值得注意的是，不能让UID 重复；

比如我想添加lanhaitun 这个用户，我发现UID 508没有用户用，并且我想把其用户组也设置为lanhaitun ，用户组的GID 也设置为508,如果GID 没有占用的话；

我们要打开 /etc/passwd ，在最下面加一行；
  
lanhaitun:x:508:508::/home/lanhaitun:/bin/bash
  
然后执行pwconv ，让/etc/passwd 和/etc/shadow同步，您可以查看 /etc/shadow的内容是否同步；
  
[root@localhost beinan]# pwconv

修改/etc/group

首先，我们得查看是否有lanhaitun用户组，以及GID 508 是否被其它用户组占用；
  
[root@localhost ~]# more /etc/group |grep lanhaitun
  
[root@localhost ~]# more /etc/group |grep 508
  
通过查看，我们发现没有被占用；所以我们要添加lanhaitun 的记录到 /etc/group
  
lanhaitun:x:508:
  
其次，是运行 grpconv 来同步/etc/group 和/etc/gshadow内容，您可以通过查看/etc/gshadow的内容变化确认是不是添加组成功了；
  
[root@localhost beinan]# grpconv

1) 创建用户的家目录，并把用户启动文件也复制过去；

创建用户的家目录，我们要以/etc/passwd 中添加的新用户的记录为准，我们在/etc/passwd 中添加新用户lanhaitun ，她的家目录是处于/home/lanhaitun ；另外我们还需要把/etc/skel 目录下的.*隐藏文件复制过去；

[root@localhost ~]# cp -R /etc/skel/ /home/lanhaitun
  
[root@localhost ~]# ls -la /home/lanhaitun/

改变新增用户家目录的属主和权限；

我们发现新增用户的家目录的属主目前是root ，并且家目录下的隐藏文件也是root权限；

[root@localhost ~]# ls -ld /home/lanhaitun/
  
drwxr-xr-x 3 root root 4096 10月 18 14:53 /home/lanhaitun/
  
所以我们要通过chown 命令来改变/home/lanhaitun目录归属为lanhaitun用户；

[root@localhost ~]# chown -R lanhaitun:lanhaitun /home/lanhaitun
  
查看是否已经更换了属主为lanhaitun用户所有；
  
[root@localhost ~]# ls -ld /home/lanhaitun/
  
drwxr-xr-x 3 lanhaitun lanhaitun 4096 10月 18 14:53 /home/lanhaitun/
  
[root@localhost ~]# ls -la /home/lanhaitun/
  
看来已经实现了；

但这样还是不够的，因为/home/lanhaitun/的目录权限可能会过于公开；
  
drwxr-xr-x 3 lanhaitun lanhaitun 4096 10月 18 14:53 /home/lanhaitun/
  
我们看到 /home/lanhaitun/ 目录的权限为 drwxr-xr-x ，也就是同组用户和其它用户组所能查看，为了保密，我们有理由把新增用户家目录的权限设置为只有其自己可读可写可执行；于是… …
  
[root@localhost ~]# chmod 700 /home/lanhaitun/
  
[root@localhost ~]# ls -ld /home/lanhaitun/
  
drwx—— 3 lanhaitun lanhaitun 4096 10月 18 14:53 /home/lanhaitun/
  
我们用其它用户，当然得把具有超级权限的root用户除外；比如我以beinan用户来查看lanhaitun的家目录会得到如下信息；
  
[beinan@localhost ~]$ ls -la /home/lanhaitun/
  
ls: /home/lanhaitun/: 权限不够
  
如此看来，lanhaitun用户的家目录是安全的

1) 设置新增用户的密码；

以上各步骤都就序了，我们得为新增用户设置密码了；要通过passwd 命令来生成；这个没有办法通过修改文件解决；

passwd 的用法:

passwd 用户
  
[root@localhost ~]# passwd lanhaitun
  
Changing password for user lanhaitun.
  
New UNIX password: 注: 输入您的密码
  
Retype new UNIX password: 再输入一次
  
passwd: all authentication tokens updated successfully. 注: 设置密码成功

测试添增用户是否成功；

您可以用新增用户登录测试，也可以通过su 来切换用户测试；

[beinan@localhost ~]$ su lanhaitun
  
Password:
  
[lanhaitun@localhost beinan]$ cd ~
  
[lanhaitun@localhost ~]$ pwd
  
/home/lanhaitun
  
[lanhaitun@localhost ~]$ ls -la
  
[lanhaitun@localhost ~]$ mkdir testdir
  
[lanhaitun@localhost ~]$ ls -lh
  
总用量 4.0K
  
drwxrwxr-x 2 lanhaitun lanhaitun 4.0K 10月 18 15:16 testdir
  
通过上面一系列动作，我们会发现所创建的lanhaitun用户已经成功；

1. 通过修改用户 (User) 和用户组 (Group) 配置文件的办法来修改用户或用户组；

我们可以修改/etc/passwd 和/etc/group 来达到修改用户和用户所归属的组，这个过程和添加新用户时差不多；比如我想修改lanhaitun的用户名全称、公司以及电话等信息；我们可以修改/etc/passwd 实现；

1) 修改用户信息；

lanhaitun:x:508:508::/home/lanhaitun:/bin/bash 注: 这是初始记录；
  
我们可以修改为
  
lanhaitun:x:508:508:lanhaitun wu,Office Dalian,13000000000:/home/lanhaitun:/bin/bash
  
当然我们还可以修改用户的bash 类型，家目录等，当然如果修改家目录，还得进行建家目录、属主和权限的操作，这和前面添加用户的办法在程序上有些是相同的；

修改完成后，我们要进行pwconv 同步，通过finger 来查看用户的信息等；

[root@localhost lanhaitun]# pwconv
  
[root@localhost lanhaitun]# finger lanhaitun
  
Login: lanhaitun Name: lanhaitun wu
  
Directory: /home/lanhaitun Shell: /bin/bash
  
Office: Office Dalian, +1-300-000-0000
  
Never logged in.
  
No mail.
  
No Plan.

修改用户所归属的组，可以通过/etc/group 修改实现；

当然修改用户和用户组，不仅能通过修改配置文件来实现，还能过过 usermod 及chfn来实现；我将在以后的文档中写一写，也比较简单；您可以通过man来查看用法；在这里我们先讲一讲如何通过修改配置文件来达到目的；

如果我们想把lanhaitun 这个用户归属到root用户组，所以我们还能修改/etc/group 的办法来达到目的；找到/etc/group 中的root开头的一行，按其规划加入lanhaitun；
  
root:x:0:root,lanhaitun
  
如果不明白，看前面/etc/group的解释，谢谢；

然后执行 grpconv 命令来同步/etc/group 和/etc/gshadow两个文件的内容；
  
[root@localhost ~]# grpconv
  
查看lanhaitun归属组的信息；
  
[root@localhost ~]# id lanhaitun
  
uid=508(lanhaitun) gid=508(lanhaitun) groups=508(lanhaitun),0(root)

1) 删除用户及用户组的办法；
  
这个比较简单，我们可以通过删除/etc/passwd 和/etc/group 相应的用户和用户组记录就能达到目的，也能过过userdel 和groupdel 来实现对用户及用户组的删除；

如果是通过修改用户和用户组配置文件的办法来删除用户，就是删除相应的记录就行了，如果不想保留其家目录，删除就是了。

[root@localhost ~]# userdel lanhaitun
  
[root@localhost ~]# userdel -r lanhaitun
  
注: 可以用userdel 来删除lanhaitun 用户，我们看到第二个例子中多了一个参数-r ，第一个例子是说只删除lanhaitun用户，其家目录和mail等仍会保存；加上-r 参数，是删除家目录及mail等；所以要小心操作；用userdel 删除用户的同时，也会把其用户组删除；我们可以通过/etc/passwd 和/etc/group 的内容变化来查看；

阅读全文(0次) / 评论 / 丢小纸条 / 文件夹: Linux

用debootstrap在已有的Linux系统上安装debian
  
sinkingship @ 2007-02-01 18:31

昨天在网上找了找资料，在ubuntu上用debootstrap装了个debian，小结一下过程:
  
 (1) 装好debootstrap:
  
apt-get install debootstrap
  
 (2) 将要用来装debian的硬盘分区格式化好，挂载到任意目录，如/mnt/debinst/
  
如果想将来的debian系统不只是一个根分区/，而是把根目录下的一些目录从别的分区挂载过来，例如我们经常把/usr/local从别的分区挂过来，这一步就要挂好，例如，下面的命令就是交/usr/local从别的分区挂过来:
  
mkdir /mnt/debinst/usr/local -p
  
mount /dev/hdXX /mnt/debinst/usr/local
  
 (3) 用debootstrap在如/mnt/debinst/目录上建立一个基本系统，如:
  
debootstrap sarge /mnt/debinst/ [http://http.us.debian.org/debia](http://http.us.debian.org/debia)
  
debootstrap会从网上下载一些文件，使/mnt/debist/成为一个chroot子环境，即一个基本系统。这里说明一点，源的选择很重要，如果源corrupted，安装很可能失败，例如，第一次安时我选了cn99，结果失败了。

这时，/mnt/debinst/已经是个基本系统了，还差一些配置、软件安装和一个可引导的内核。下面就来完成这些工作:
  
 (4) 基本系统可能会缺一些设备文件，例如我安装的时候就缺少了一些块文件，如hdX，这可以从主系统中拷贝，如:
  
cp /dev/hda* /mnt/debinst/dev/ -ap
  
 (5) chroot到基本系统中:
  
chroot /mnt/debinst
  
 (6) 配置/etc/fstab，/etc/hostname，/etc/resolv.conf，/etc/network/interfaces，并把文件系统挂载上来。
  
如果挂载出错，很有可能是因为缺少设备文件，可按 (4) 解决。各配置文件的样本可以在debian.org找到，我摘抄部分如下:
  
—————————————————————————————————————————————————-
  
/etc/fstab:

/etc/fstab: static file system information

file system mount point type options dump pass

/dev/XXX / ext3 defaults 0 1
  
/dev/XXX /boot ext3 ro,nosuid,nodev 0 2

/dev/XXX none swap sw 0 0
  
proc /proc proc defaults 0 0

/dev/fd0 /mnt/floppy auto noauto,rw,sync,user,exec 0 0
  
/dev/cdrom /mnt/cdrom iso9660 noauto,ro,user,exec 0 0

/dev/XXX /tmp ext3 rw,nosuid,nodev 0 2
  
/dev/XXX /var ext3 rw,nosuid,nodev 0 2
  
/dev/XXX /usr ext3 rw,nodev 0 2
  
/dev/XXX /home ext3 rw,nosuid,nodev 0 2
  
———————————————————————————————————————————————————
  
/etc/hostname:

DebianHostName

——————————————————————————————————————————————————–
  
/etc/resolv.conf:
  
search hqdom.local{post.abstract}0
  
nameserver 10.1.1.36
  
nameserver 192.168.9.100
  
——————————————————————————————————————————————————–
  
/etc/network/interfaces:

######################################################################

/etc/network/interfaces — configuration file for ifup(8), ifdown(8)

See the interfaces(5) manpage for information on what options are

available

######################################################################

We always want the loopback interface
  
auto lo
  
iface lo inet loopback

To use dhcp

auto eth0

iface eth0 inet dhcp

An example static IP setup: (broadcast and gateway are optional)

auto eth0

iface eth0 inet static

address 192.168.0.42

network 192.168.0.0

netmask 255.255.255.0

broadcast 192.168.0.255

gateway 192.168.0.1

将上面的样本适当修改使其适合自己的情况就可以了。

 (7) 配置好apt，如果用ppp上网，现在就把ppp装上 (否则重启后进入新的环境下就……) 。
  
 (8) 安装内核、引导程序。
  
apt-get install kernel-image-2.6.18.4-XXXX
  
apt-get install grub
  
也可以不装grub，直接exit出来修改主系统的/boot/grub/menu.lst。这里注意一点，安装的如果是initrd的内核，在/boot/menu.lst一定要加上initrd。
  
 (9) reboot，进入新系安装其他软件。

/sbin/nologin
  
[http://yingxiong.iteye.com/blog/642872](http://yingxiong.iteye.com/blog/642872)

[http://hi.baidu.com/nfubuntu/blog/item/f910a26489e612f1f63654c3.html](http://hi.baidu.com/nfubuntu/blog/item/f910a26489e612f1f63654c3.html)

[http://zebralinux.blog.51cto.com/8627088/1369301c](http://zebralinux.blog.51cto.com/8627088/1369301c)
  
[http://cn.linux.vbird.org/linux_basic/0410accountmanager.php](http://cn.linux.vbird.org/linux_basic/0410accountmanager.php)
