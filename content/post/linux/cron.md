---
title: cron, crond, crontab, linux 定时任务, cronie
author: "-"
date: 2012-03-02T15:36:38+00:00
url: /cron
categories:
  - Linux
tags:
  - remix
  - reprint
---
## cron, crond, crontab, linux 定时任务, cronie

### 安装 cron

```bash
# archlinux 
#pacman -S cronie
When using the systemd init system, (persistent) timers are available as a replacement of (ana)cron. Systemd#Timer_services

Since version 197 systemd supports timers, making cron unnecessary on a systemd system. Since version 212 persistent services are supported, replacing even anacron. Persistent timers are run at the next opportunity if the system was powered down when the timer was scheduled to run.

# https://wiki.gentoo.org/wiki/Cron
# https://wiki.gentoo.org/wiki/Systemd#Timer_services

# 查看 cron 是否已经安装
# centos
yum list installed |grep cron
yum install cronie    # vixie-cron 已经不再维护, 建议安装 cronie
```

### 查看 crond 状态

```bash
# check status
systemctl status crond
service crond status
# cron log path
/var/log/cron
```

### 创建定时任务

```bash
crontab -e # 执行后会跳转到vi (依赖环境变量配置,默认一般是vi)
# vi状态下插入一行, 每三分钟插入一行数据到/tmp/foo.txt
*/3 * * * * echo "foo" >> /tmp/foo.txt
#3分钟之后查看文件  /tmp/foo.txt 应该已经有数据了.
```

```bash
service crond start # 启动服务
service crond stop # 关闭服务
service crond restart # 重启服务
service crond reload # 重新载入配置, 新建定时任务的时候,不需要reload.
crontab -l # 列出cron服务的详细内容
crontab -u root -l #列出某个用户cron服务的详细内容
crontab -e # 编辑某个用户的 cron 服务, 可以像使用 vi 编辑其他任何文件那样修改 crontab 文件并退出。如果修改了某些条目或添加了新的条目，那么在保存该文件时， cron 会对其进行必要的完整性检查。如果其中的某个域出现了超出允许范围的值，它会提示你。
crontab -e -u 用户名  # 配置指定用户 的定时任务, root 可以用 -u user name 来编辑其它使用者的 crontab 配置
crontab -u # 设定某个用户的 cron 服务，一般 root 用户在执行这个命令的时候需要此参数
crontab -r # 删除没个用户的 cron 服务
```

```bash
# Use the hash sign to prefix a comment
# +—————- minute (0 – 59)
# |  +————- hour (0 – 23)
# |  |  +———- day of month (1 – 31)
# |  |  |  +——- month (1 – 12)
# |  |  |  |  +—- day of week (0 – 7) (Sunday=0 or 7)
# |  |  |  |  |
# *  *  *  *  *  user-name command to be executed
```

```bash
# Use the hash sign to prefix a comment
### 配置自动生效
cron will then examine the modification time on all crontabs and reload those which have changed. Thus cron need not be restarted whenever a crontab file is modified
```

### 在线crontab 表达式执行时间计算

<https://www.matools.com/crontab>

### 示例

```bash
# 每天早上 5 点运行
0 5 * * * /root/bin/backup.sh
# 从 5点开始, 连续一个小时, 每分钟运行一次
* 5 * * * /root/bin/backup.sh
# 每三分钟
*/3 * * * * echo "foo" >> /tmp/foo.txt
# 每三分钟, 8点到17点
*/3 8-17 * * * echo "foo" >> /tmp/foo.txt
# 每周日 04:05
5 4 * * sun echo "run at 5 after 4 every sunday"
```

```bash
# 双数周的周一
50 9 * * 1 [ $(expr $(date +%W) \% 2) -eq 0 ] && /path/to/foo.sh
00 10 * * 1 [ $(expr $(date +%W) \% 2) -eq 0 ] && /path/to/foo.sh
# 单数周的周一
50 10 * * 1 [ $(expr $(date +%W) \% 2) -eq 1 ] && /path/to/foo.sh
00 11 * * 1 [ $(expr $(date +%W) \% 2) -eq 1 ] && /path/to/foo.sh
# 每周二,三,四,五
50 10 * * 2,3,4,5 /path/to/foo.sh
00 11 * * 2,3,4,5 /path/to/foo.sh
```

```bash
    # 每周一，三，五，13:55分
    55 13 * * 1,3,5 metting-notification.sh
```

### 每两个小时

```bash
    0 */2 * * * echo "foo" >> /tmp/foo.txt
```

run-parts

### 每个小时去执行一遍/etc/cron.hourly内的脚本

```bash
    01 * * * * root run-parts /etc/cron.hourly
```
  
02 4 ** * root run-parts /etc/cron.daily // 每天去执行一遍/etc/cron.daily内的脚本

每星期去执行一遍/etc/cron.weekly内的脚本

```bash
    22 4 * * 0 root run-parts /etc/cron.weekly
```
  
42 4 1 ** root run-parts /etc/cron.monthly //每个月去执行一遍/etc/cron.monthly内的脚本

```bash
#centos
tail /var/log/cron

#debian
#debian开启crontab日志，该日志记录状态系统默认为关闭状态。
# vi /etc/rsyslog.conf
cron.*                                /var/log/cron.log

# 重启日志服务: 
systemctl restart rsyslog
```

### crontab 执行shell脚本

```bash
crontab -e
0 1 * * * /path/to/shell/foo.sh >> /var/log/foo/foo.log
```

---

再例如，root想删除fred的cron设置:
  
引用:
  
crontab -u fred -r
  
在编辑cron服务时，编辑的内容有一些格式和约定，输入:
  
引用:
  
crontab -u root -e
  
进入vi编辑模式，编辑的内容一定要符合下面的格式:
  
引用:
  
_/1 * * * * ls >> /tmp/ls.txt
  
这个格式的前一部分是对时间的设定，后面一部分是要执行的命令，如果要执行的命令太多，可以把这些命令写到一个脚本里面，然后在这里直接调用这个脚本就可 以了，调用的时候记得写出命令的完整路径。时间的设定我们有一定的约定，前面五个_号代表五个数字，数字的取值范围和含义如下:

分钟 (0-59)
  
小时 (0-23)
  
日期 (1-31)
  
月份 (1-12)
  
星期 (0-6) //0代表星期天
  
除了数字还有几个个特殊的符号就是"_"、"/"和"-"、","，_代表所有的取值范围内的数字，"/"代表每的意思,"*/5″表示每5个单位，"-"代表从某个数字到某个数字,","分开几个离散的数字。以下举几个例子说明问题:

每天凌晨4点
  
0 4 ** * echo "Good morning." >> /tmp/test.txt //注意单纯echo，从屏幕上看不到任何输出，因为cron把任何输出都email到root的信箱了。

晚上11点到早上8点之间每两个小时，早上八点
  
0 23-7/2，8 ** * echo "Welcome to <http://beyl.cn>.: ) " >> /tmp/test.txt
  
每个月的4号和每个礼拜的礼拜一到礼拜三的早上11点
  
0 11 4 * 1-3 command line
  
1月1日早上4点
  
0 4 1 1 * command line
  
每次编辑完某个用户的cron设置后，cron自动在/var/spool/cron下生成一个与此用户同名的文件，此用户的cron信息都记录在这个文 件中，这个文件是不可以直接编辑的，只可以用crontab -e 来编辑。cron启动后每过一份钟读一次这个文件，检查是否要执行里面的命令。因此此文件修改后不需要重新启动cron服务。
  
2.编辑/etc/crontab 文件配置cron
  
cron 服务每分钟不仅要读一次/var/spool/cron内的所有文件，还需要读一次/etc/crontab,因此我们配置这个文件也能运用cron服务 做一些事情。用crontab配置是针对某个用户的，而编辑/etc/crontab是针对系统的任务。此文件的文件格式是:
  
引用:
  
SHELL=/bin/bash
  
PATH=/sbin:/bin:/usr/sbin:/usr/bin
  
MAILTO=root //如果出现错误，或者有数据输出，数据作为邮件发给这个帐号
  
HOME=/

run-parts

01 **** root run-parts /etc/cron.hourly //每个小时去执行一遍/etc/cron.hourly内的脚本
  
02 4 ** * root run-parts /etc/cron.daily //每天去执行一遍/etc/cron.daily内的脚本
  
22 4 ** 0 root run-parts /etc/cron.weekly //每星期去执行一遍/etc/cron.weekly内的脚本
  
42 4 1 ** root run-parts /etc/cron.monthly //每个月去执行一遍/etc/cron.monthly内的脚本
  
使用者 运行的路径
  
大家注意"run-parts"这个参数了，如果去掉这个参数的话，后面就可以写要运行的某个脚本名，而不是文件夹名了。
  
cron
  
定时执行指令 ( cron ):
  
crontab [_/Minute] [_/Hour] [_/Day] [_/Month] [*(/DayOfWeek)?] Command
  
Minute: 分钟，1 ~ 59
  
Hour : 小时，0 ~ 23
  
Day : 日期，1 ~ 31
  
Month : 月份，1 ~ 12 或 jan、feb…
  
DayOfWeek? : 0 (星期日) ~ 6 (星期六) ，或 mon、tue…
  
Command : 所要执行的指令，中间以 ; 来分隔多个指令。

-e : 编辑 /var/spool/cron/crontabs/UserName 这一个档案。以 # 开头代表批注。
  
-l : 列出 /var/spool/cron/crontabs/UserName 这一个档案的内容。
  
-d : 删除使用者的工作排程。
  
-r : 删除使用者的工作排程档。

Minute，Houre，Day，Month，DayOfWeek? 为条件式，需要符合所有条件的那个时刻指令才会执行。
  
用 * 来代表略过这一个条件。
  
如果同一个字段有多个条件，中间要用 , 分开。
  
如果是指连续一段时间，中间则以 – 分开。
  
如果要每隔固定时间执行，则使用 /#，指每隔 # 时刻执行。

crontab 的指令，预设是以 /bin/sh 为直译器，而以使用者的家目录为工作目录。然而使用者可以用 HOME、SHELL、PATH 的变量改变执行时的直译器、预设执行目录与路径。也可以透过设定 MAILTO 设定执行后的纪录要以电子邮件记送到何处。

use /bin/sh to run commands, no matter what /etc/passwd says

SHELL=/bin/sh

mail any output to \`paul', no matter whose crontab this is

MAILTO=paul
  
run five minutes after midnight, every day

5 0 ** * $HOME/bin/daily.job >> $HOME/tmp/out 2>&1

run at 2:15pm on the first of every month — output mailed to paul

15 14 1 ** $HOME/bin/monthly

run at 10 pm on weekdays, annoy Joe

0 22 ** 1-5 mail -s "It's 10pm" joe%Joe,%%Where are your kids?%
  
23 0-23/2 ** * echo "run 23 minutes after midn, 2am, 4am …, everyday"

<https://wiki.gentoo.org/wiki/Cron>
