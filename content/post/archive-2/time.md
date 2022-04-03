---
title: time command
author: "-"
date: 2018-02-13T04:33:45+00:00
url: time
categories:
  - linux

tags:
  - reprint
---
## time command
time — 执行命令并计时

【格式】time [-p] command [arguments...]

【说明】

执行命令行"command [arguments...]",命令行执行结束时在标准输出中打印执行该命令行的时间统计结果,其统计结果包含以下数据: 

1)实际时间(real time): 从command命令行开始执行到运行终止的消逝时间；

2)用户CPU时间(user CPU time): 命令执行完成花费的用户CPU时间,即命令在用户态中执行时间总和；

3)系统CPU时间(system CPU time): 命令执行完成花费的系统CPU时间,即命令在核心态中执行时间总和。

其中,用户CPU时间和系统CPU时间之和为CPU时间,即命令占用CPU执行的时间总和。实际时间要大于CPU时间,因为Linux是多任务操作系统,往往在执行一条命令时,系统还要处理其它任务。

另一个需要注意的问题是即使每次执行相同命令,但所花费的时间也是不一样,其花费时间是与系统运行相关的。

例1: 

            1. # time date
            2. Sun Mar 26 22:45:34 GMT-8 2006
            3. 
            4. real    0m0.136s
            5. user    0m0.010s
            6. sys     0m0.070s
            7. #
    

在例1中,执行命令"time date"(见第1行)。系统先执行命令"date",第2行为命令"date"的执行结果。第3-6行为执行命令"date"的时间统计结果,其中第4行"real"为实际时间,第5行"user"为用户CPU时间,第6行"sys"为系统CPU时间。以上三种时间的显示格式均为MMmNN[.FFF]s。

在例1中,CPU时间 = 用户CPU时间 + 系统CPU时间 = 0m0.010s + 0m0.070s = 0m0.080s,实际时间大于CPU时间,说明在date命令运行的同时,还有其它任务在运行。

【参数说明】

-p 以POSIX缺省的时间格式打印时间统计结果,单位为秒。详细的输出格式见例2。

例2: 

            1. # time -p date
            2. Wed Mar 27 00:33:11 GMT-8 2006
            3. real 0.11
            4. user 0.00
            5. sys 0.02
            6. #
    

在例2中,同样执行命令"time date"(见第1行)。系统先执行命令 "date",第2行为该命令的执行结果。第3-5行为执行命令"date"的时间统计结果。注意本例的时间格式与例1中的时间格式差别,使用-p 参数后的时间显示格式为NN.FF,其单位为秒。

【相关环境变量说明】

TIMEFORMAT 自定义输出的时间格式。

我们也可以通过环境变量TIMEFORMAT来自定义输出的时间格式[1]。格式中使用和标准C中的函数printf一致的转义符,以及使用以下的转义序列来指定输出的时间格式: 

%[prec][l][RUS]
  
其中,选项prec为指定时间精度,即小数点后面的位数；选项l表示使用分秒(具体格式为: MMmNN[.FFF]s)的格式；最后一个字符表示时间的类型,其中R表示实际时间,U表示用户CPU时间,S表示系统CPU 时间,它们的单位均为秒。

time命令缺省输出的时间格式同 TIMEFORMAT=$'/nreal/t%3lR/nuser/t%3lU/nsys/t%3lS'。

使用-p参数的time命令输出的时间格式同 TIMEFORMAT=$'real %2R/nuser %2U/nsys %2S'。

例3: 

            1. # export TIMEFORMAT=$'real %2R/nuser %2U/nsys %2S'
            2. # time date
            3. Wed Mar 27 00:52:03 GMT-8 2006
            4. real 0.04
            5. user 0.00
            6. sys 0.01
            7. #
    

比较例2和例3显示结果,很容易发现例3虽然没有使用参数-p,但其输出的结果和例2一模一样。

当然,我们也可以修改为任何自己喜欢的时间格式。

例4: 

            1. # export TIMEFORMAT=$'/nHello, ThinkerABC!/nreal time :       %lR/nuser CUP time :   %lU/nsystem CPU time : %lS'
            2. # time date
            3. Wed Mar 27 01:09:26 GMT-8 2006
            4.
            5. Hello, ThinkerABC!
            6. real time :       0m0.016s
            7. user CUP time :   0m0.006s
            8. system CPU time : 0m0.008s
            9. #
    

例4的第4-8行正是我们自定义的输出格式。

从以上介绍了三种指定时间格式的方法,即缺省的时间格式、使用参数-p的POSIX缺省的时间格式和设定环境变量TIMEFORMAT自定义的时间格式,Linux系统使用的先后顺序如下: 

1.参数-p的POSIX缺省时间格式；

2.环境变量TIMEFORMAT自定义的时间格式；

3.缺省的时间格式。

【退出状态说明】

如果能执行command命令,则返回该命令的退出状态,否则返回如下的退出状态值: 

127 命令未找到

126 命令找到,但不能执行

1-125 其它错误

参考文献: 

[1] bash-2.05b源程序, http://ftp.gnu.org/gnu/bash/bash-2.05b.tar.gz , 2002.07

[2] Linux man pages