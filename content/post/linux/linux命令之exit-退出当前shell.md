---
title: Linux命令之exit – 退出当前shell
author: "-"
date: 2011-12-26T07:52:53+00:00
url: /?p=2017
categories:
  - Linux
tags:
  - Shell

---
## Linux命令之exit – 退出当前shell
本文链接: http://codingstandards.iteye.com/blog/836625  (转载请注明出处) 

用途说明
  
exit命令用于退出当前shell，在shell脚本中可以终止当前脚本执行。

常用参数
  
格式: exit n
  
退出。设置退出码为n。 (Cause the shell to exit with a status of n.) 

格式: exit
  
退出。退出码不变，即为最后一个命令的退出码。 (If n is omitted, the exit status is that of the last command executed. ) 

格式: $?
  
上一个命令的退出码。

格式: trap "commands" EXIT
  
退出时执行commands指定的命令。 ( A trap on EXIT is executed before the shell terminates.) 

退出码 (exit status，或exit code) 的约定: 
  
0表示成功 (Zero - Success) 
  
非0表示失败 (Non-Zero - Failure) 
  
2表示用法不当 (Incorrect Usage) 
  
127表示命令没有找到 (Command Not Found) 
  
126表示不是可执行的 (Not an executable) 
  
>=128 信号产生

man 3 exit 写道
  
The C standard specifies two constants, EXIT_SUCCESS and EXIT_FAILURE, that may be passed to exit() to indicate
  
successful or unsuccessful termination, respectively.

以下摘自/usr/include/stdlib.h
  
C代码
  
#define EXIT_FAILURE 1 /* Failing exit status. */
  
#define EXIT_SUCCESS 0 /* Successful exit status. */

BSD试图对退出码标准化。
  
man 3 exit 写道
  
BSD has attempted to standardize exit codes; see the file <sysexits.h>.

以下摘自/usr/include/sysexits.h
  
C代码
  
#define EX_OK 0 /* successful termination */

#define EX__BASE 64 /* base value for error messages */

#define EX_USAGE 64 /* command line usage error */
  
#define EX_DATAERR 65 /* data format error */
  
#define EX_NOINPUT 66 /* cannot open input */
  
#define EX_NOUSER 67 /* addressee unknown */
  
#define EX_NOHOST 68 /* host name unknown */
  
#define EX_UNAVAILABLE 69 /* service unavailable */
  
#define EX_SOFTWARE 70 /* internal software error */
  
#define EX_OSERR 71 /* system error (e.g., can't fork) */
  
#define EX_OSFILE 72 /* critical OS file missing */
  
#define EX_CANTCREAT 73 /* can't create (user) output file */
  
#define EX_IOERR 74 /* input/output error */
  
#define EX_TEMPFAIL 75 /* temp failure; user is invited to retry */
  
#define EX_PROTOCOL 76 /* remote error in protocol */
  
#define EX_NOPERM 77 /* permission denied */
  
#define EX_CONFIG 78 /* configuration error */

#define EX__MAX 78 /* maximum listed value */

使用示例
  
示例一 退出当前shell
  
[root@new55 ~]#
  
[root@new55 ~]# exit
  
logout

示例二 在脚本中，进入脚本所在目录，否则退出
  
Bash代码
  
cd $(dirname $0) || exit 1

示例三 在脚本中，判断参数数量，不匹配就打印使用方式，退出
  
Bash代码
  
if [ "$#" -ne "2" ]; then
      
echo "usage: $0 


<hours>"

      
exit 2
  
fi 

示例四 在脚本中，退出时删除临时文件
  
Bash代码
  
trap "rm -f tmpfile; echo Bye." EXIT

示例五 检查上一命令的退出码
  
Bash代码
  
./mycommand.sh
  
EXCODE=$?
  
if [ "$EXCODE" == "0" ]; then
      
echo "O.K"
  
fi