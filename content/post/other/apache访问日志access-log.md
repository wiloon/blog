---
title: Apache访问日志/access log
author: "-"
date: 2015-02-09T02:18:35+00:00
url: /?p=7333
categories:
  - Inbox
tags:
  - reprint
---
## Apache访问日志/access log

[http://blog.csdn.net/zhuying_linux/article/details/6773912](http://blog.csdn.net/zhuying_linux/article/details/6773912)

想要知道什么人在什么时候浏览了网站的哪些内容吗？查看Apache的访问日志就可以知道。访问日志是Apache的标准日志,本文详细解释了访问日志的内容以及相关选项的配置。
  
一、访问日志的格式
  
Apache内建了记录服务器活动的功能,这就是它的日志功能。这个《Apache日志》系列文章介绍的就是Apache的访问日志、错误日志,以及如何分析日志数据,如何定制Apache日志,如何从日志数据生成统计报表等内容。
  
如果Apache的安装方式是默认安装,服务器一运行就会有两个日志文件生成。这两个文件是access_log (在Windows上是access.log) 和error_log (在Windows上是error.log) 。采用默认安装方式时,这些文件可以在/usr/local/apache/logs下找到；对于Windows系统,这些日志文件将保存在Apache安装目录的logs子目录。不同的包管理器会把日志文件放到各种不同的位置,所以你可能需要找找其他的地方,或者通过配置文件查看这些日志文件配置到了什么地方。
  
正如其名字所示,访问日志access_log记录了所有对Web服务器的访问活动。下面是访问日志中一个典型的记录:
  
180.168.41.175 - - [19/Aug/2000:14:47:37 -0400] "GET / HTTP/1.0" 200 654

【216.35.116.91 - - [19/Aug/2000:14:47:37 -0400] "GET / HTTP/1.0" 200 654】【可忽略此行】
  
这行内容由7项构成,上面的例子中有两项空白,但整行内容仍旧分成了7项。
  
第一项信息是远程主机的地址,即它表明访问网站的究竟是谁。在上面的例子中,访问网站的主机是(我用我们公司的域名解析查询的结果是180.168.41.175)【216.35.116.91忽略】。随便说一句,这个地址属于一台名为si3001.inktomi.com的机器 (要找出这个信息,可以使用nslookup工具查找DNS) ,inktomi.com是一家制作Web搜索软件的公司。可以看出,仅仅从日志记录的第一项出发,我们就可以得到有关访问者的不少信息。
  
默认情况下,第一项信息只是远程主机的IP地址,但我们可以要求Apache查出所有的主机名字,并在日志文件中用主机名字来替代IP地址。然而,这种做法通常不值得推荐,因为它将极大地影响服务器记录日志的速度,从而也就减低了整个网站的效率。另外,有许多工具能够将日志文件中的IP地址转换成主机名字,因此要求Apache记录主机名字替代IP地址是得不偿失的。
  
然而,如果确实有必要让Apache找出远程主机的名字,那么我们可以使用如下指令:
  
HostNameLookups on
  
如果HostNameLookups设置成double而不是on,日志记录程序将对它找到的主机名字进行反向查找,验证该主机名字确实指向了原来出现的IP地址。默认情况下HostNameLookups设置为off。
  
上例日志记录中的第二项是空白,用一个"-"占位符替代。实际上绝大多数时候这一项都是如此。这个位置用于记录浏览者的标识,这不只是浏览者的登录名字,而是浏览者的email地址或者其他唯一标识符。这个信息由identd返回,或者直接由浏览器返回。很早的时候,那时Netscape 0.9还占据着统治地位,这个位置往往记录着浏览者的email地址。然而,由于有人用它来收集邮件地址和发送垃圾邮件,所以它未能保留多久,很久之前市场上几乎所有的浏览器就取消了这项功能。因此,到了今天,我们在日志记录的第二项看到email地址的机会已经微乎其微了。
  
日志记录的第三项也是空白。这个位置用于记录浏览者进行身份验证时提供的名字。当然,如果网站的某些内容要求用户进行身份验证,那么这项信息是不会空白的。但是,对于大多数网站来说,日志文件的大多数记录中这一项仍旧是空白的。
  
日志记录的第四项是请求的时间。这个信息用方括号包围,而且采用所谓的"公共日志格式"或"标准英文格式"。因此,上例日志记录表示请求的时间是2000年8月19日星期三14:47:37。时间信息最后的"-0400"表示服务器所处时区位于UTC之前的4小时。
  
日志记录的第五项信息或许是整个日志记录中最有用的信息,它告诉我们服务器收到的是一个什么样的请求。该项信息的典型格式是"METHOD RESOURCE PROTOCOL",即"方法资源协议"。
  
在上例中,METHOD是GET,其他经常可能出现的METHOD还有POST和HEAD。此外还有不少可能出现的合法METHOD,但主要就是这三种。
  
RESOURCE是指浏览者向服务器请求的文档,或URL。在这个例子中,浏览者请求的是"/",即网站的主页或根。大多数情况下,"/"指向DocumentRoot目录的index.html文档,但根据服务器配置的不同它也可能指向其他文件。
  
PROTOCOL通常是HTTP,后面再加上版本号。版本号或者是1.0,或者是1.1,但出现1.0的时候比较多。我们知道,HTTP协议是Web得以工作的基础,HTTP/1.0是HTTP协议的早期版本,而1.1是最近的版本。当前大多数Web客户程序仍使用1.0版本的HTTP协议。
  
日志记录的第六项信息是状态代码。它告诉我们请求是否成功,或者遇到了什么样的错误。大多数时候,这项值是200,它表示服务器已经成功地响应浏览器的请求,一切正常。此处不准备给出状态代码的完整清单以及解释它们的含义,请参考相关资料了解这方面的信息。但一般地说,以2开头的状态代码表示成功,以3开头的状态代码表示由于各种不同的原因用户请求被重定向到了其他位置,以4开头的状态代码表示客户端存在某种错误,以5开头的状态代码表示服务器遇到了某个错误。
  
日志记录的第七项表示发送给客户端的总字节数。它告诉我们传输是否被打断 (即,该数值是否和文件的大小相同) 。把日志记录中的这些值加起来就可以得知服务器在一天、一周或者一月内发送了多少数据。
  
二、配置访问日志
  
访问日志文件的位置实际上是一个配置选项。如果我们检查httpd.conf配置文件,可以看到该文件中有如下这行内容:
  
CustomLog /usr/local/apache/logs/access_log common
  
注意,对于版本较早的Apache服务器,这行内容可能略有不同。它使用的可能不是CustomLog指令,而是TransferLog指令。如果你的服务器属于这类情况,建议你尽可能地早日升级服务器。
  
CustomLog指令指定了保存日志文件的具体位置以及日志的格式。至于如何定制日志文件的格式以及内容,我们将在这个《Apache日志》系列文章的后面几篇讨论。上面这行指令指定的是common日志格式,自从有了Web服务器开始,common格式就是它的标准格式。由此我们也可以理解,虽然几乎不再有任何客户程序向服务器提供用户的标识信息,但访问日志却还保留着第二项内容。
  
CustomLog指令中的路径是日志文件的路径。注意,由于日志文件是由HTTP用户打开的 (用User指令指定) ,因此必须注意这个路径要有安全保证,防止该文件被随意改写。
  
《Apache日志》系列文章的后面几篇将继续介绍: Apache错误日志,定制日志的格式和内容,如何将日志内容写入指定的程序而不是文件,如何从日志文件获得一些非常有用的统计信息,等等。

三、进程统计
  
UNIX可以跟踪每个用户运行的每条命令,如果想知道昨晚弄乱了哪些重要的文件,进程统计子系统可以告诉你。它对还跟踪一个侵入者有帮助。与连接时间日志不同,进程统计子系统缺省不激活,它必须启动。在Linux系统中启动进程统计使用accton命令,必须用root身份来运行。Accton命令的形式accton file,file必须先存在。先使用touch命令来创建pacct文件: touch /var/log/pacct,然后运行accton:  accton /var/log/pacct。一旦accton被激活,就可以使用lastcomm命令监测系统中任何时候执行的命令。若要关闭统计,可以使用不带任何参数的accton命令。
  
lastcomm命令报告以前执行的文件。不带参数时,lastcomm命令显示当前统计文件生命周期内纪录的所有命令的有关信息。包括命令名、用户、tty、命令花费的CPU时间和一个时间戳。如果系统有许多用户,输入则可能很长。下面的例子:
  
crond F root ?? 0.00 secs Sun Aug 20 00:16
  
promisc_check.s S root ?? 0.04 secs Sun Aug 20 00:16
  
promisc_check root ?? 0.01 secs Sun Aug 20 00:16
  
grep root ?? 0.02 secs Sun Aug 20 00:16
  
tail root ?? 0.01 secs Sun Aug 20 00:16
  
sh root ?? 0.01 secs Sun Aug 20 00:15
  
ping S root ?? 0.01 secs Sun Aug 20 00:15
  
ping6.pl F root ?? 0.01 secs Sun Aug 20 00:15
  
sh root ?? 0.01 secs Sun Aug 20 00:15
  
ping S root ?? 0.02 secs Sun Aug 20 00:15
  
ping6.pl F root ?? 0.02 secs Sun Aug 20 00:15
  
sh root ?? 0.02 secs Sun Aug 20 00:15
  
ping S root ?? 0.00 secs Sun Aug 20 00:15
  
ping6.pl F root ?? 0.01 secs Sun Aug 20 00:15
  
sh root ?? 0.01 secs Sun Aug 20 00:15
  
ping S root ?? 0.01 secs Sun Aug 20 00:15
  
sh root ?? 0.02 secs Sun Aug 20 00:15
  
ping S root ?? 1.34 secs Sun Aug 20 00:15
  
locate root ttyp0 1.34 secs Sun Aug 20 00:15
  
accton S root ttyp0 0.00 secs Sun Aug 20 00:15
  
进程统计的一个问题是pacct文件可能增长的十分迅速。这时需要交互式的或经过cron机制运行sa命令来保持日志数据在系统控制内。sa命令报告、清理并维护进程统计文件。它能把/var/log/pacct中的信息压缩到摘要文件/var/log/savacct和/var/log/usracct中。这些摘要包含按命令名和用户名分类的系统统计数据。sa缺省情况下先读它们,然后读pacct文件,使报告能包含所有的可用信息。sa的输出有下面一些标记项:
  
avio-每次执行的平均I/O操作次数
  
cp-用户和系统时间总和,以分钟计
  
cpu-和cp一样
  
k-内核使用的平均CPU时间,以1k为单位
  
k*sec-CPU存储完整性,以1k-core秒
  
re-实时时间,以分钟计
  
s-系统时间,以分钟计
  
tio-I/O操作的总数
  
u-用户时间,以分钟计
  
例如:
  
842 173.26re 4.30cp 0avio 358k
  
2 10.98re 4.06cp 0avio 299k find
  
9 24.80re 0.05cp 0avio 291k \***other
  
105 30.44re 0.03cp 0avio 302k ping
  
104 30.55re 0.03cp 0avio 394k sh
  
162 0.11re 0.03cp 0avio 413k security.sh*
  
154 0.03re 0.02cp 0avio 273k ls
  
56 31.61re 0.02cp 0avio 823k ping6.pl*
  
2 3.23re 0.02cp 0avio 822k ping6.pl
  
35 0.02re 0.01cp 0avio 257k md5sum
  
97 0.02re 0.01cp 0avio 263k initlog
  
12 0.19re 0.01cp 0avio 399k promisc_check.s
  
15 0.09re 0.00cp 0avio 288k grep
  
11 0.08re 0.00cp 0avio 332k awk
  
用户还可以根据用户而不是命令来提供一个摘要报告。例如sa -m显示如下:
  
885 173.28re 4.31cp 0avk
  
root 879 173.23re 4.31cp 0avk
  
alias 3 0.05re 0.00cp 0avk
  
qmailp 3 0.01re 0.00cp 0avk
  
四、Syslog设备
  
Syslog已被许多日志函数采纳,它用在许多保护措施中-任何程序都可以通过syslog纪录事件。Syslog可以纪录系统事件,可以写到一个文件或设备中,或给用户发送一个信息。它能纪录本地事件或通过网络纪录另一个主机上的事件。
  
Syslog设备依据两个重要的文件: /etc/syslogd (守护进程) 和/etc/syslog.conf配置文件,习惯上,多数syslog信息被写到/var/adm或/var/log目录下的信息文件中 (messages.*) 。一个典型的syslog纪录包括生成程序的名字和一个文本信息。它还包括一个设备和一个优先级范围 (但不在日之中出现) 。
  
每个syslog消息被赋予下面的主要设备之一:
  
LOG_AUTH-认证系统: login、su、getty等
  
LOG_AUTHPRIV-同LOG_AUTH,但只登录到所选择的单个用户可读的文件中
  
LOG_CRON-cron守护进程
  
LOG_DAEMON-其他系统守护进程,如routed
  
LOG_FTP-文件传输协议: ftpd、tftpd
  
LOG_KERN-内核产生的消息
  
LOG_LPR-系统打印机缓冲池: lpr、lpd
  
LOG_MAIL-电子邮件系统
  
LOG_NEWS-网络新闻系统
  
LOG_SYSLOG-由syslogd (8) 产生的内部消息
  
LOG_USER-随机用户进程产生的消息
  
LOG_UUCP-UUCP子系统
  
LOG_LOCAL0~LOG_LOCAL7-为本地使用保留
  
Syslog为每个事件赋予几个不同的优先级:
  
LOG_EMERG-紧急情况
  
LOG_ALERT-应该被立即改正的问题,如系统数据库破坏
  
LOG_CRIT-重要情况,如硬盘错误
  
LOG_ERR-错误
  
LOG_WARNING-警告信息
  
LOG_NOTICE-不是错误情况,但是可能需要处理
  
LOG_INFO-情报信息
  
LOG_DEBUG-包含情报的信息,通常旨在调试一个程序时使用
  
syslog.conf文件指明syslogd程序纪录日志的行为,该程序在启动时查询配置文件。该文件由不同程序或消息分类的单个条目组成,每个占一行。对每类消息提供一个选择域和一个动作域。这些域由tab隔开: 选择域指明消息的类型和优先级；动作域指明syslogd接收到一个与选择标准相匹配的消息时所执行的动作。每个选项是由设备和优先级组成。当指明一个优先级时,syslogd将纪录一个拥有相同或更高优先级的消息。所以如果指明"crit",那所有标为crit、alert和emerg的消息将被纪录。每行的行动域指明当选择域选择了一个给定消息后应该把他发送到哪儿。例如,如果想把所有邮件消息纪录到一个文件中,如下:
  
# Log all the mail messages in on e place
  
mail.* /var/log/maillog
  
其他设备也有自己的日志。UUCP和news设备能产生许多外部消息。它把这些消息存到自己的日志 (/var/log/spooler) 中并把级别限为"err"或更高。例如:
  
# Save mail and news errors of level err and higher in aspecial file
  
uucp,news.crit /var/log/spooler
  
当一个紧急消息到来时,可能想让所有的用户都得到。也可能想让自己的日志接收并保存。
  
# Everybody gets emergency messages, plus log them on anther machine
  
\*.emerg \*
  
*.emerg @linuxaid.com.cn
  
alert消息应该写到root和tiger的个人账号中:
  
# Root and Tiger get alert and higher messages
  
*.alert root,tiger
  
有时syslogd将产生大量的消息。例如内核 ("kern"设备) 可能很冗长。用户可能想把内核消息纪录到/dev/console中。下面的例子表明内核日志纪录被注释掉了:
  
# Log all kernel messages to the console
  
# Logging much else clutters up the screen
  
# kern.* /dev/console
  
用户可以在一行中指明所有的设备。下面的例子把info或更高级别的消息送到/var/log/messages,除了mail以外。级别"none"禁止一个设备:
  
# Log anything (except mail) of level info or higher
  
# Don't log private authentication messages
  
*.info:mail.none;authpriv.none /var/log/messages
  
在有些情况下,可以把日志送到打印机,这样网络入侵者怎么修改日志都没有用了。通常要广泛纪录日志。Syslog设备是一个攻击者的显著目标。一个为其他主机维护日志的系统对于防范服务器攻击特别脆弱,因此要特别注意。
  
有个小命令logger为syslog (3) 系统日志文件提供一个shell命令接口,使用户能创建日志文件中的条目。用法: logger例如: logger This is a test！
  
它将产生一个如下的syslog纪录: Aug 19 22:22:34 tiger: This is a test!
  
注意不要完全相信日志,因为攻击者很容易修改它的。
  
五、程序日志
  
许多程序通过维护日志来反映系统的安全状态。su命令允许用户获得另一个用户的权限,所以它的安全很重要,它的文件为sulog。同样的还有sudolog。另外,想Apache有两个日志: access_log和error_log。
