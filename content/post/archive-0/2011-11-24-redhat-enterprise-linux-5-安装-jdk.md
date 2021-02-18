---
title: RedHat Enterprise Linux 5 安装 JDK
author: w1100n
type: post
date: 2011-11-24T06:24:24+00:00
url: /?p=1584
views:
  - 2
bot_views:
  - 7
categories:
  - Java
  - Linux
tags:
  - RedHat

---
将JDK安装文件jdk-6u21-linux-x64-rpm.bin拷贝到Redhat任意目录下。例如：/opt/jdk（目录jdk需要手动新建）

执行   chmod  +x  jdk-6u21-linux-x64-rpm.bin

执行   ./jdk-6u21-linux-x64-rpm.bin

此时会出现JDK安装授权协议。可以一路按Enter浏览。如果等的不耐烦可以直接按Ctrl+C,直接会出现Do you agree to the above license terms? [yes or no]的字样。

键入yes，同意该授权协议。

此时系统会开始解压jdk-6u21-linux-x64-rpm.bin

解压完毕后，回到/opt/jdk目录，键入dir。会发现多出了一个解压好的安装文件：jdk-6u21-linux-amd64.rpm

执行   rpm  -ivh  jdk-1_5_0_17-linux-i586.rpm

此时，系统会开始安装JDK。安装结束后可以在/usr目录下发现新增了一个名为java的文件夹。该文件夹就是安装好的JDK目录。

设置环境变量

进入/etc文件夹（具体操作命令忽略），找到文件profile并打开。

[注意：profile是指文件不是指文件夹]

找到export PATH USER LOGNAME MAIL HOSTNAME HISTSIZE INPUTRC，在该语句的**上面**添加以下语句：

set  JAVA_HOME="/usr/java/jdk1.5.0_17"

export   JAVA_HOME

[注意："="两侧不能有空格]

export  CLASSPATH="/usr/java/jdk1.5.0_17/lib:/usr/java/jdk1.5.0_17/jre/lib"

[注意："="两侧不能有空格；":"是冒号，同样不要有空格出现]

pathmunge $JAVA_HOME

[注意：无引号]

9.      设置完毕后，保存文件。重启Redhat后登录控制终端，键入：java  -version;

如果出现java version "1.5.0.17"等字样，说明您的JDK已经安装成功了