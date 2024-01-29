---
title: sed 截取文本段
author: "-"
date: 2019-03-15T05:23:40+00:00
url: /?p=13845
categories:
  - Inbox
tags:
  - reprint
---
## sed 截取文本段

[https://yhz61010.iteye.com/blog/1565984](https://yhz61010.iteye.com/blog/1565984)

假设文件 text.txt 内容如下:

......
  
xxxxxxxxxxxxxx
  
yyyyyyyyyyyyyyyy
  
zzzzzzzzzzzzzzzzzzz
  
start_mark xxxxxx
  
10aaaaabbbbcccc
  
20aaaaabbbbcccc
  
30aaaaabbbbcccc
  
40aaaaabbbbcccc
  
......
  
yyyyy end_mark
  
......

现要截取 start_mark 所在行与 end_mark 所在行之间的文本。注意，最终截取的文本不包括 start_mark 行和 end_mark 行。

可以使用如下 sed 命令:

sed -n '/^start_mark/,/end_mark$/p' text.txt | grep -Ev '(^start_mark|end_mark$)' | cut -f 1,2

通过上述命令，我们完成了截取一段文本，并且还过滤出了所要列的内容。其结果是得到了如下内容:

10aaaaa
  
20aaaaa
  
30aaaaa
  
40aaaaa

说明:
  
sed 的常见用法是:

sed -n '20,30p' text.txt

上述代码可取出 text.txt 中，20 至 30 行之间的内容。但是也可以使用正则来表示行的开始和结束。

当然，也可以使用如下方法来截取文本段，不过下面这种方法没有上面的方法智能:
  
1. 首先，取出文本中开始文本处的行号。
  
2. 然后，取出文本中结束文本处的行号。
  
3. 最后，使用 sed 截取内容。

例如:
  
cat -n text.txt | grep 'start_mark ' | awk '{print $1}'
  
cat -n text.txt | grep 'end_mark ' | awk '{print $1}'
  
sed -n '10, 20p' text.txt
