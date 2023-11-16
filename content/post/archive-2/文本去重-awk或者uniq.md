---
title: linux shell 文本 去重 – awk或者uniq
author: "-"
date: 2016-08-09T00:07:48+00:00
url: /?p=9168
categories:
  - shell
tags:
  - reprint
---
## linux shell 文本 去重 – awk或者uniq

uniq
  
不带参数时, 默认合并重复的行. 类似MySQL的 distinct

```bash
 -c, --count             //在每行前加上表示相应行目出现次数的前缀编号
 -d, --repeated          //只输出重复的行
 -D, --all-repeated      //只输出重复的行,不过有几行输出几行
 -f, --skip-fields=N     //-f 忽略的段数,-f 1 忽略第一段
 -i, --ignore-case       //不区分大小写
 -s, --skip-chars=N      //根-f有点像,不过-s是忽略,后面多少个字符 -s 5就忽略后面5个字符
 -u, --unique            //只显示不重复的行
 -z, --zero-terminated   end lines with 0 byte, not newline
 -w, --check-chars=N      //对每行第N 个字符以后的内容不作对照
 --help              //显示此帮助信息并退出
 --version              //显示版本信息并退出
```

对于awk '!a[$3]++',需要了解3个知识点
  
1. awk数组知识,不说了
  
2. awk的基本命令格式 awk 'pattern{action}'
  
省略action时,默认action是{print},如awk '1'就是awk '1{print}'
  
3. var++的形式: 先读取var变量值,再对var值+1

以数据
  
1 2 3
  
1 2 3
  
1 2 4
  
1 2 5
  
为例,对于awk '!a[$3]++'
  
awk处理第一行时:  先读取a[$3]值再自增,a[$3]即a[3]值为空(0),即为awk '!0',即为awk '1',即为awk '1{print}'
  
awk处理第二行时:  先读取a[$3]值再自增,a[$3]即a[3]值为1,即为awk '!1',即为awk '0',即为awk '0{print}'
  
.............

最后实现的效果就是对于$3是第一次出现的行进行打印,也就是去除$3重复的行

转自: [http://bbs.chinaunix.net/forum.php?mod=viewthread&tid=1672726#pid11904888](http://bbs.chinaunix.net/forum.php?mod=viewthread&tid=1672726#pid11904888)
  
sort和uniq

重复行通常不会造成问题,但是有时候它们的确会引起问题。此时,不必花上一个下午的时间来为它们编制过滤器,uniq 命令便是唾手可得的好工具。

了解一下它是如何节省您的时间和精力的。进行排序之后,您会发现有些行是重复的。有时候该重复信息是不需要的,可以将它除去以节省磁盘空间。不必对文本行进行排序,但是您应当记住 uniq 在读取行时会对它们进行比较并将只除去两个或更多的连续行。下面的示例说明了它实际上是如何工作的:

  1. 用 uniq 除去重复行

$ cat happybirthday.txt
  
Happy Birthday to You!
  
Happy Birthday to You!
  
Happy Birthday Dear Tux!
  
Happy Birthday to You!

$ sort happybirthday.txt
  
Happy Birthday Dear Tux!
  
Happy Birthday to You!
  
Happy Birthday to You!
  
Happy Birthday to You!

$ sort happybirthday.txt | uniq
  
Happy Birthday Dear Tux!
  
Happy Birthday to You!

警告: 请不要使用 uniq 或任何其它工具从包含财务或其它重要数据的文件中除去重复行。在这种情况下,重复行几乎总是表示同一金额的另一个交易,将它除去会给会计部造成许多困难。千万别这么干！

    使用 -u 和 -d 选项
  
$ sort happybirthday.txt | uniq -u
  
Happy Birthday Dear Tux!

$ sort happybirthday.txt | uniq -d
  
Happy Birthday to You!
  
您还可以用 -c 选项从 uniq 中获取一些统计信息:

清单

    使用 -c 选项
  
$ sort happybirthday.txt | uniq -uc
  
1 Happy Birthday Dear Tux!

$ sort happybirthday.txt | uniq -dc
  
3 Happy Birthday to You!
  
就算 uniq 对完整的行进行比较,它仍然会很有用,但是那并非该命令的全部功能。特别方便的是: 使用 -f 选项,后面跟着要跳过的字段数,它能够跳过给定数目的字段。当您查看系统日志时这非常有用。通常,某些项要被复制许多次,这使得查看日志很难。使用简单的 uniq 无法完成任务,因为每一项都以不同的时间戳记开头。但是如果您告诉它跳过所有的时间字段,您的日志一下子就会变得更加便于管理。试一试 uniq -f 3 /var/log/messages ,亲眼看看。

还有另一个选项 -s ,它的功能就像 -f 一样,但是跳过给定数目的字符。您可以一起使用 -f 和 -s 。 uniq 先跳过字段,再跳过字符。如果您只想使用一些预先设置的字符进行比较,那么该怎么办呢？试试看 -w 选项。

转自: [http://weiyingjun.blog.hexun.com/55766273_d.html](http://weiyingjun.blog.hexun.com/55766273_d.html)
