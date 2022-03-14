---
title: pam config
author: "-"
date: 2018-10-08T11:12:47+00:00
url: pam

categories:
  - inbox
tags:
  - reprint
---
## pam config
pam模块文件内容看,可以将pam配置文件分为四列,

第一列代表模块类型
  
第二列代表控制标记
  
第三列代表模块路径
  
第四列代表模块参数

Module_type 将为 Service_name 字段中的相应服务指定模块类型 (auth/account/session/passwd) 。
  
Control_flag 将指定模块的堆栈行为。它可以获取诸如 requisite、required、sufficient 和 optional 之类的值。
  
Module_path 将指定实现模块的库对象的路径名称。默认情况下,它将被设为 /lib/security。
  
Module_options/module_args (可选字段) 将指定可以传递给服务模块的选项或实参。

PAM模块接口(模块管理组)
  
PAM为认证任务提供四种类型可用的模块接口,它们分别提供不同的认证服务: 
  
auth 表示鉴别类接口模块类型用于检查用户和密码,并分配权限；
  
这种类型的模块为用户验证提供两方面服务。让应用程序提示用户输入密码或者其他标记,确认用户合法性；通过他的凭证许可权限,设定组成员关系或者其他优先权。
  
account 表示账户类接口,主要负责账户合法性检查,确认帐号是否过期,是否有权限登录系统等；
  
这种模块执行的是基于非验证的帐号管理。他主要用于限制/允许用户对某个服务的访问时间,当前有效的系统资源 (最多可以多少用户) ,限制用户位置 (例如: root只能通过控制台登录) 。
  
多数情况下auth和account会一起用来对用户登录和使用服务的情况进行限制。这样的限制会更加完整。比如下面是一个具体的例子: login是一个应用程序。Login要完成两件工作——首先查询用户,然后为用户提供所需的服务,例如提供一个shell程序。通常Login要求用户输入名称和密码进行验证。当用户名输入的时候,系统自然会去比对该用户是否是一个合法用户,是否在存在于本地或者远程的用户数据库中。如果该账号确实存在,那么是否过期。这些个工作是由account接口来负责。
  
如果用户满足上述登录的前提条件,那么它是否具有可登录系统的口令,口令是否过期等。这个工作就要由auth接口来负责了,他通常会将用户口令信息加密并提供给本地 (/etc/shadow) 或者远程的(ldap,kerberos等)口令验证方式进行验证。
  
如果用户能够登录成功,证明auth和account的工作已经完成。但整个验证过程并没有完全结束。因为还有一些其他的问题没有得到确认。例如,用户能够在服务器上同时开启多少个窗口登录,用户可以在登录之后使用多少终端多长时间,用户能够访问哪些资源和不能访问哪些资源等等。也就是说登录之后的后续验证和环境定义等还需要其他的接口。这就是我们下面要提到的两组接口: 
  
password 口令类接口。控制用户更改密码的全过程。也就是有些资料所说的升级用户验证标记。
  
session - 会话类接口。实现从用户登录成功到退出的会话控制；处理为用户提供服务之前/后需要做的些事情。包括: 开启/关闭交换数据的信息,监视目录等,设置用户会话环境等。也就是说这是在系统正式进行服务提供之前的最后一道关口。
  
单个PAM库模块可以提供给任何或所有模块接口使用。例如,pam_unix.so提供给四个模块接口使用。

auth        required      pam_env.so        //登录后的环境变量。
  
auth        sufficient    pam_fprintd.so     //指纹认证。
  
auth        sufficient    pam_unix.so nullok try_first_pass //验证用户密码的有效性。如果使用nullok参数,用户不输入密码就可以获得系统提供的服务。同时,也允许用户密码为空时更改用户密码。try_first_pass尝试在提示用户输入密码前,使用前面一个堆叠的auth模块提供的密码认证用户。
  
auth        requisite     pam_succeed_if.so uid >= 500 quiet //允许uid大于500的用户在通过密码验证的情况下登录。
  
auth        required      pam_deny.so     //对所有不满足上述任意条件的登录请求直接拒绝。

account     required      pam_unix.so //主要执行建立用户帐号和密码状态的任务,然后执行提示用户修改密码,用户采用新密码后才提供服务之类的任务。
  
account     sufficient    pam_localuser.so //要求将用户列于 /etc/passwd 中。
  
account     sufficient    pam_succeed_if.so uid < 500 quiet    //对用户的登录条件做一些限制,表示允许uid大于500的用户在通过密码验证的情况下登录。
  
account     required      pam_permit.so
  
 
  
password    requisite     pam_cracklib.so try_first_pass retry=3type=    //对用户密码提供强健性检测。
  
password    sufficient    pam_unix.so md5 shadow nullok try_first_pass use_authtok //让用户更改密码的任务。
  
password    required      pam_deny.so    //对所有不满足上述任意条件的登录请求直接拒绝。
  
 
  
session     optional      pam_keyinit.so revoke  //表示当用户登录的时候为其建立相应的密钥环,并在用户登出的时候予以撤销。optional表示即便该行所涉及的模块验证失败用户仍能通过认证
  
session     required      pam_limits.so     //限制用户登录时的会话连接资源,相关pam_limit.so配置文件是/etc/security/limits.conf,默认情况下对每个登录用户都没有限制。
  
session     [success=1 default=ignore]pam_succeed_if.so service in crond quiet use_uid   //success=1时执行本行。default=ignore用来设置上面的返回值是无法达的行为时,那么这个模块的返回值将被忽略,不会被应用程序知道。对用户的登录条件做一些限制
  
session     required      pam_unix.so //记录用户名和服务名到日志文件的工作,只不过最后返回错误

Control_flag 值包括: 
  
required 堆栈中的所有 Required 模块必须看作一个成功的结果。如果一个或多个 Required 模块失败,则实现堆栈中的所有 Required 模块,但是将返回第一个错误。
  
sufficient 如果标记为 sufficient 的模块成功并且先前没有 Required 或 sufficient 模块失败,则忽略堆栈中的所有其余模块并返回成功。
  
requisite表示执行错误则立即返回
  
Optional: 如果堆栈中没有一个模块是 required 并且没有任何一个 sufficient 模块成功,则服务/应用程序至少要有一个 optional 模块成功。
  
nclude - 与其他控制标志不同,include与模块结果的处理方式无关。该标志用于直接引用其他PAM模块的配置参数

pam 主要模块
  
pam_access 将使用登录名/域名,根据 /etc/security/access.conf 中的预定义规则交付日志守护进程样式的登录访问控制。
  
pam_cracklib 将根据密码规则检查密码。
  
pam_env sets/unsets 环境变量来自 /etc/security/pam_env_conf。
  
pam_debug 将调试 PAM。
  
pam_deny 将拒绝 PAM 模块,仅返回错误并防止发生任何类型的连接或验证。
  
pam_echo 将打印消息。
  
pam_exec 将执行外部命令。
  
pam_ftp 是匿名访问模块。
  
pam_localuser 要求将用户列于 /etc/passwd 中。
  
pam_unix 将通过 /etc/passwd 提供传统密码验证。
  
pam_warn.so 来记录关于正在进行的尝试的信息。

所有的PAM配置方法都在man手册中有说明,比如要查找某个程序支持PAM模块的配置,可以使用man 加模块名(去掉.so)查找说明,如# man pam_unix。(模块名可以在目录/lib/security/或/lib64/security/中找到。)

https://blog.csdn.net/jeny8221/article/details/73876066?utm_source=copy
  
http://blog.51cto.com/7424593/1924260
  
https://www.cnblogs.com/kevingrace/p/8671964.html