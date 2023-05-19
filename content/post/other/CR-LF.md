---
title: 回车, 换行符, CRLF, LF
author: "-"
date: 2012-09-27T05:15:21+00:00
url: crlf
categories:
  - cs
tags:
  - reprint
---
## 回车, 换行符

- 换行, line feed, LF, newline, \n
- 回车, carriage return, CR, return, \r
- CRLF, Carriage return & line feed

- unix: 换行, \n
- windows: 换行(回车+换行), \r\n, Unix/Mac 下打开会显示成 `^M`
- macos: Line Feed, LF

<https://blog.csdn.net/wjcquking/article/details/6634504>

回车符号和换行符号产生背景

关于"回车" (carriage return) 和"换行" (line feed) 这两个概念的来历和区别。
  
在计算机还没有出现之前，有一种叫做电传打字机 (Teletype Model 33) 的玩意，每秒钟可以打10个字符。但是它有一个问题，就是打完一行换行的时候，要用去0.2秒，正好可以打两个字符。要是在这0.2秒里面，又有新的字符传过来，那么这个字符将丢失。
  
     于是，研制人员想了个办法解决这个问题，就是在每行后面加两个表示结束的字符。一个叫做"回车"，告诉打字机把打印头定位在左边界；另一个叫做"换行"，告诉打字机把纸向下移一行。
  
这就是"换行"和"回车"的来历，从它们的英语名字上也可以看出一二。
  
      后来，计算机发明了，这两个概念也就被般到了计算机上。那时，存储器很贵，一些科学家认为在每行结尾加两个字符太浪费了，加一个就可以。于是，就出现了分歧。
  
Unix系统里，每行结尾只有"<换行>"，即"\n"；Windows系统里面，每行结尾是" <回车><换行>"，即"\r\n"；Mac系统里，每行结尾是"<回车>"。一个直接后果是，Unix/Mac系统下的文件在Windows里打开的话，所有文字会变成一行；而Windows里的文件在 Unix/Mac 下打开的话，在每行的结尾可能会多出一个`^M`符号

windows创建的文件是 `\n\r` 结束的， 而linux，mac这种unix类系统是\n结束的。

所以unix的文本到windows会出现换行丢失 (ultraedit这种软件可以正确识别) ； 而反过来就会出现^M的符号了

Windows等操作系统用的文本换行符和UNIX/Linux操作系统用的不同，Windows系统下输入的换行符在UNIX/Linux下不会显示为"换行"，而是显示为 ^M 这个符号 (这是Linux等系统下规定的特殊标记，占一个字符大小，不是 ^ 和 M 的组合，打印不出来的) 。Linux下很多文本编辑器 (命令行) 会在显示这个标记之后，补上一个自己的换行符，以避免内容混乱 (只是用于显示，补充的换行符不会写入文件，有专门的命令将Windows换行符替换为Linux换行符) 。 UNIX/Linux系统下的换行符在Windows系统的文本编辑器中会被忽略，整个文本会乱成一团。

windows换行是\r\n，十六进制数值是: 0D0A。
  
LINUX换行是\n，十六进制数值是: 0A
  
所以在linux保存的文件在windows上用记事本看的话会出现黑点，我们可以在LINUX下用命令把linux的文件格式转换成win格式的。
  
unix2dos 是把linux文件格式转换成windows文件格式
  
dos2unix 是把windows格式转换成linux文件格式。

linux下删除windows换行符^M

OJ判题时发现一个问题: 用%c读入的代码都会报wa。后来发现跟scanf有关。在linux下使用%c会读到\n和\r两个字符。所以需要将^M (也就是\r) 字符删掉
  
删除方法不少。找了一个比较简单的。
  
要将a.txt里的^M去掉并写入b.txt，则使用如下指令cat a.txt | tr -d "^M" > b.txt
  
注意: 语句中的^M是通过ctrl+V, ctrl+M输入的。特指/r字符

unix   下换行符只有:   \r
  
Dos   下换行符有: \r\n
  
具体的，   \r的ascii   码是: 14

## \n的ascii   码是: 10

作者: wjcquking
  
来源: CSDN
  
原文: <https://blog.csdn.net/wjcquking/article/details/6634504>
  
版权声明: 本文为博主原创文章，转载请附上博文链接！

换行符'n'和回车符'r'

顾名思义，换行符就是另起一行，回车符就是回到一行的开头，所以我们平时编写文件的回车符应该确切来说叫做回车换行符

'n' 10 换行 (newline)
  
'r' 13 回车 (return)
  
也可以表示为'x0a'和'x0d'.(16进制)

在windows系统下，回车换行符号是"rn".但是在Linux等系统下是没有"r"符号的。

在解析文本或其他格式的文件内容时，常常要碰到判定回车换行的地方，这个时候就要注意既要判定"rn"又要判定"n"。

写程序时可能得到一行,将其进行trim掉'r',这样能得到你所需要的string了。
