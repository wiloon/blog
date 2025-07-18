---
title: find command
author: "-"
date: 2011-04-30T08:20:38+00:00
url: find
categories:
  - Linux
tags:
  - reprint
  - remix
  - command

---
## find command

- find 命令默认会递归遍历子目录

```bash
# find pathname -options
find / -name '*task*.log'

# find by file size
# >100MB
find . -type f -size +102400k
```

- -name 按文件名查找文件

```Bash
# -name 按文件名查找文件
find . -name t.sql

# 使用通配符时要加引号(单引号/双引号)
find . -name 'bookmark*'

# . 当前目录
# / 根目录

# 查 3 分钟前修改的文件
find . -mmin +3
```

- -a, and
- -o, or
- -type f 表示查找文件而不是目录
- -type d 目录类型

## -prune

prune 的功能就是当遇到某个文件夹的时候，跳过这个文件夹，不进去继续查找。

```bash
├── folder1
├── folder2
│   ├── sub1
│   │   └── file1
│   └── sub2
│       └── file2
└── folder3
    └── file3

find . -path ./folder3 -prune -o -type f -print

# find 后面的第一个英文点号 . 表示当前根路径，-path ./folder3表示匹配路径为./folder3的文件夹，-prune 表示把前面命令所匹配到的路径排除，
# 不再进入该路径下面继续查找，-o表示或，-type f 表示查找文件，-print表示打印查找结果到命令行终端。 有几个需要注意的点
            
# -path 后面需要跟绝对路径或者是相对路径，不能只有文件夹名称
            
find . -path folder3 -prune -o -type f -print  
./folder2/sub1/file1
./folder2/sub2/file2
./folder3/file3

# 这样是错误的。把 -path 改成 -name 就对了。
# find . -name folder3 -prune -o -type f -print
./folder2/sub1/file1
./folder2/sub2/file2
            
# -o 一开始让我感到很疑惑。它的意思是 OR，那就是既匹配了前面的 ./folder3，又匹配了后面的 -type f，可为什么打印出来的没有./folder3呢？
# 原来是因为-print只对离自己最近的一个匹配条件起作用，在这个例子里也就是只打印-o后面的匹配条件所匹配的文件，
# 对-o前面的-path folder3 -prune所匹配的东西不起作用

# -path ./folder3 -prune 的值是 false

find ./path0/ -path './path0/sub0' -o -path './path0/sub1' -o -path './path0/sub2' -a -prune -o   \( -name '*.py'  ! -name '__init__.py'  ! -name 'foo.py'  ! -name 'bar.py'  \)  -type f -print -exec rm -rf {}  \;

# 在 path0 里查找文件, 排除掉 ./path0/sub0, ./path0/sub1, ./path0/sub2, 匹配 *.py, 但是排除掉 __init__.py, foo.py, bar.py, 删除匹配的文件
```

作者：武斌
链接：[https://juejin.cn/post/6844904166305841160](https://juejin.cn/post/6844904166305841160)
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

## 查找然后在查找结果上执行命令

### 将 dir0 目录下修改时间一天以内的文件复制到 dir1 下

```bash
find /dir0 -mtime -1 -type f -exec cp {} /dir1 \;
# 参数 -type f 不能省, 不限定文件类型的话,会把代表当前目录的 "." 也查出来, 然后就会列出所有文件
# -exec 表示需要执行的命令, {} 代表 find 找到的内容
# "\;" 是固定写法表示 -exec 的结束 
```

### 删除7天以前修改过的文件

```bash
find . -type f -mtime +7 -exec ls -ltr {} \;
find . -type f -mtime +7 -exec mv {} tmp \;
find . -mtime +7 -type f -exec rm -f {} \;
# 参数 -type f 不能省, 不限定文件类型的话,会把代表当前目录的 "." 也查出来, 然后就会列出所有文件
# -exec 表示需要执行的命令, {} 代表 find 找到的内容
# "\;" 是固定写法表示 -exec 的结束 
```

### 按时间查

File's data was last modified (n+1)*24 hours ago

```bash
# 当前时间 2021-11-11 13:53

# 24小时内更改过内容的文件
# 1 天之内被修改过的文件, 2021-11-10 13:53 - 2021.11.11 13:53
find / -mtime 0

# 2021-11-09 13:53 - 2021-11-10 13:53
find / -mtime 1
# 2021-11-10 13:53 - 2021.11.11 13:53
find / -mtime -1
# 2021-11-08 13:53 - 2021-11-09 13:53
find / -mtime 2
# 2021-11-09 13:53 - 2021.11.11 13:53
find / -mtime -2
# 5 天之内被修改过的文件, 2021-11-6 13:53 - 2021.11.11 13:53
find / -mtime -5
# 5天前的那一天修改过的文件, 2021-11-05 13:53 - 2021.11.06 13:53
find / -mtime 5
# 7 天之前修改过的文件, -∞ - 2021-11-05 13:53
find / -mtime +7
```

```block
-ctime -n 查找距现在 n_24H 内修改过的文件
-ctime n 查找距现在 n_24H 前, (n+1)_24H 内修改过的文件
-ctime +n 查找距现在 (n+1)_24H 前修改过的文件

[a|c|m]min  [最后访问|最后状态修改|最后内容修改]min
[a|c|m]time [最后访问|最后状态修改|最后内容修改]time
```

linux 文件的几种时间 (以 find 为例):
  
- `atime` 最后一次访问时间, 如 ls, more 等, 但 chmod, `chown`, ls, stat 等不会修改些时间, 使用 ls -utl 可以按此时间顺序查看;
- `ctime` 最后一次状态修改时间, 如 chmod, `chown` 等状态时间改变但修改时间不会改变, 使用 stat file 可以查看;
- `mtime` 最后一次内容修改时间, 如 vi 保存后等, 修改时间发生改变的话, `atime` 和 `ctime` 也相应跟着发生改变.

注意: linux 里是不会记录文件的创建时间的, 除非这个文件自创建以来没有发生改变, 那么它的创建时间就是它的最后一次修改时间.
  
```bash
# ls -lt ./ 按修改时间顺序查看
# ls -lut ./ 按访问时间顺序查看
```
  
(如果想反序查看的话需要加一个选项 -r)
  
以上出自 "ShawOnline" 博客，请务必保留此出处[http://shawonline.blog.51cto.com/304978/199674](http://shawonline.blog.51cto.com/304978/199674)
  
[acm]time 计量单位是天，即24H
  
[acm]min 计量单位是分钟

```bash
# 20天内修改过的
find . -mtime -20 -type f -name "*.zip"
find ./ -mtime 0  #查找一天内修改的文件
find ./ -mtime -2 #查找2天内修改的文件，多了一个减号
find ./ -mmin  -10  #查找距离现在10分钟内修改的文件
```

### 查找深度

find 命令默认会递归遍历子目录, 要控制查找深度的话用 `-maxdepth` 参数。

```bash
#  find all files that have been modified after a certain number of days.
# -maxdepth 和 -mindepth 选项允许您指定您希望 find 搜索深入到目录树的哪一级别。如果您希望 find 只在目录的一个级别中查找，您可以使用 maxdepth 选项。
find . -maxdepth 1 -mtime -1

```

### 正则表达式

使用上面的-name测试项能解决许多问题，但是有些还是不太好办，比如: 查找当前目录下名称全部为数字的c源代码文件，这时就该'-regex'出手了。正则表达式绝对值得你去好好研究一下，在unix系统下太有用了，这里不做过多说明，请读者自行学习。
  
-regex同样属于测试项。使用-regex时有一点要注意: -regex不是匹配文件名，而是匹配完整的文件名 (包括路径) 。例如，当前目录下有一个文件"abar9"，如果你用"ab._9"来匹配，将查找不到任何结果，正确的方法是使用"._ab._9"或者"._/ab.*9"来匹配。
  
针对上面的那个查找c代码的问题，可以这么写:

```bash
find . -regex ".*/[0-9]*/.c" -print
./2234.c
```

还有一个设置项(option) `-regextype`，可以让你根据自己的喜好选择使用得正则表达式类型，大家可以试试。

查找时间

mtime 和 atime 的含义都是很容易理解的，而 ctime 则需要更多的解释。由于 inode 维护着每个文件上的元数据，因此，如果与文件有关的元数据发生变化，则 inode 数据也将变化。这可能是由一系列操作引起的，包括创建到文件的符号链接、更改文件权限或移动了文件等。由于在这些情况下，文件内容不会被读取或修改，因此 mtime 和 atime 不会改变，但 ctime 将发生变化。

这些时间选项都需要与一个值 n 结合使用，指定为 -n、n 或 +n。

• -n 返回项小于 n
  
• +n 返回项大于 n
  
• n 返回项正好与 n 相等

下面，我们来看几个例子，以便于理解。以下命令将查找在最近 1 小时内修改的所有文件:

find . -mtime -1
  
./plsql/FORALLSample
  
./plsql/RegExpDNASample
  
/plsql/RegExpSample
  
用 1 取代 -1 运行同一命令将查找恰好在 1 小时以前修改的所有文件:

find . -mtime 1
  
上述命令不会生成任何结果，因为它要求完全吻合。以下命令查找 1 个多小时以前修改的所有文件:

find . -mtime +1
  
默认情况下，-mtime、-atime 和 -ctime 指的是最近 24 小时。但是，如果它们前面加上了开始时间选项，则 24 小时的周期将从当日的开始时间算起。您还可以使用 mmin、amin 和 cmin 查找在不到 1 小时的时间内变化了的时间戳。
  
如果您在登录到您的账号后立即运行以下命令，您将找到在不到 1 分钟以前读取的所有文件:

find . -amin -1
  
./.bashrc
  
/.bash_history
  
./.xauthj5FCx1
  
应该注意的是，使用 find 命令查找文件本身将更改该文件的访问时间作为其元数据的一部分。

您还可以使用 -newer、-anewer 和 –cnewer 选项查找已修改或访问过的文件与特定的文件比较。这类似于 -mtime、-atime 和 –ctime。

- -newer 指内容最近被修改的文件
- -anewer 指最近被读取过的文件
- -cnewer 指状态最近发生变化的文件

[https://www.modb.pro/db/27010](https://www.modb.pro/db/27010)

## -path

[https://unix.stackexchange.com/questions/200344/further-questions-about-path-for-find?noredirect=1#comment337661_200344](https://unix.stackexchange.com/questions/200344/further-questions-about-path-for-find?noredirect=1#comment337661_200344)

[https://man7.org/linux/man-pages/man1/find.1.html](https://man7.org/linux/man-pages/man1/find.1.html)

```bash
find . -path "*/src/*"
```
