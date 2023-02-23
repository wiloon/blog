---
title: Linux下查看文件编码，文件或文件名编码格式转换
author: "-"
date: 2015-05-04T03:57:24+00:00
url: /?p=7601
categories:
  - Inbox
tags:
  - Linux

---
## Linux下查看文件编码，文件或文件名编码格式转换

><http://blog.sina.com.cn/s/blog_6fe0d70d0101du41.html>

### Vim 的多字符编码工作方式

1. Vim 启动，根据 .vimrc 中设置的 encoding 的值来设置 buffer、菜单文本、消息文的字符编码方式。
2. 读取需要编辑的文件，根据 fileencodings 中列出的字符编码方式逐一探测该文件编码方式。并设置 fileencoding 为探测到的，看起来是正确的 (注1) 字符编码方式。
3. 对比 fileencoding 和 encoding 的值，若不同则调用 iconv 将文件内容转换为encoding 所描述的字符编码方式，并且把转换后的内容放到为此文件开辟的 buffer 里，此时我们就可以开始编辑这个文件了。注意，完成这一步动作需要调用外部的 iconv.dll(注2)，你需要保证这个文件存在于 $VIMRUNTIME 或者其他列在 PATH 环境变量中的目录里。
4. 编辑完成后保存文件时，再次对比 fileencoding 和 encoding 的值。若不同，再次调用 iconv 将即将保存的 buffer 中的文本转换为 fileencoding 所描述的字符编码方式，并保存到指定的文件中。同样，这需要调用 iconv.dll由于 Unicode 能够包含几乎所有的语言的字符，而且 Unicode 的 UTF-8 编码方式又是非常具有性价比的编码方式 (空间消耗比 UCS-2 小)，因此建议 encoding 的值设置为utf-8。这么做的另一个理由是 encoding 设置为 utf-8 时，Vim 自动探测文件的编码方式会更准确 (或许这个理由才是主要的 。我们在中文 Windows 里编辑的文件，为了兼顾与其他软件的兼容性，文件编码还是设置为 GB2312/GBK 比较合适，因此 fileencoding 建议设置为 chinese (chinese 是个别名，在 Unix 里表示 gb2312，在 Windows 里表示cp936，也就是 GBK 的代码页)。

chinese-gb to utf8

```bash

enconv -L zh_CN -x UTF-8 filename

```

如果你需要在Linux中操作windows下的文件，那么你可能会经常遇到文件编码转换的问题。Windows中默认的文件格式是GBK(gb2312)，而Linux一般都是UTF-8。下面介绍一下，在Linux中如何查看文件的编码及如何进行对文件进行编码转换。

**一，查看文件编码:**

在Linux中查看文件编码可以通过以下几种方式:

1. enca (如果你的系统中没有安装这个命令，可以用sudo yum install -y enca 安装 )查看文件编码

$ enca filename

filename: Universal transformation format 8 bits; UTF-8

CRLF line terminators

需要说明一点的是，enca对某些GBK编码的文件识别的不是很好，识别时会出现:

Unrecognized encoding

**二，文件编码转换**

**1.在Vim中直接进行转换文件编码,比如将一个文件转换成utf-8格式**

:set fileencoding=utf-8

**2. iconv 转换，iconv的命令格式如下:**

iconv -f encoding -t encoding inputfile

比如将一个UTF-8 编码的文件转换成GBK编码

iconv -f GBK -t UTF-8 file1 -o file2

**3. enconv 转换文件编码**

比如要将一个GBK编码的文件转换成UTF-8编码，操作如下

enconv -L zh_CN -x UTF-8 filename

**三，文件名编码转换:**

从Linux往 windows拷贝文件或者从windows往Linux拷贝文件，有时会出现中文文件名乱码的情况，出现这种问题的原因是因为，windows的文件名 中文编码默认为GBK,而Linux中默认文件名编码为UTF8,由于编码不一致，所以导致了文件名乱码的问题，解决这个问题需要对文件名进行转码。

在Linux中专门提供了一种工具**convmv**进行文件名编码的转换，可以将文件名从GBK转换成UTF-8编码，或者从UTF-8转换到GBK。

首先看一下你的系统上是否安装了convmv，如果没安装的话用:
  
yum -y install convmv 安装。

下面看一下convmv的具体用法:

convmv -f 源编码 -t 新编码 [选项] 文件名

常用参数:

-r 递归处理子文件夹

–notest 真正进行操作，请注意在默认情况下是不对文件进行真实操作的，而只是试验。

–list 显示所有支持的编码

–unescap 可以做一下转义，比如把 变成空格

比如我们有一个utf8编码的文件名，转换成GBK编码，命令如下:

convmv -f UTF-8 -t GBK –notest utf8编码的文件名

这样转换以后"utf8编码的文件名"会被转换成GBK编码 (只是文件名编码的转换，文件内容不会发生变化)

**四，vim 编码方式的设置**

和所有的流行文本编辑器一样，Vim 可以很好的编辑各种字符编码的文件，这当然包括UCS-2、UTF-8 等流行的Unicode 编码方式。然而不幸的是，和很多来自 Linux 世界的软件一样，这需要你自己动手设置。

Vim 有四个跟字符编码方式有关的选项，encoding、fileencoding、fileencodings、termencoding (这些选项可能的取值请参考 Vim 在线帮助 :help encoding-names)，它们的意义如下:

* encoding: Vim 内部使用的字符编码方式，包括 Vim 的 buffer (缓冲区)、菜单文本、消息文本等。默认是根据你的locale选择.用户手册上建议只在 .vimrc 中改变它的值，事实上似乎也只有在.vimrc 中改变它的值才有意义。你可以用另外一种编码来编辑和保存文件，如你的vim的encoding为utf-8,所编辑的文件采用cp936编码,vim会 自动将读入的文件转成utf-8(vim的能读懂的方式) ，而当你写入文件时,又会自动转回成cp936 (文件的保存编码).

* fileencoding: Vim 中当前编辑的文件的字符编码方式，Vim 保存文件时也会将文件保存为这种字符编码方式 (不管是否新文件都如此)。

* fileencodings: Vim自动探测fileencoding的顺序列表，启动时会按照它所列出的字符编码方式逐一探测即将打开的文件的字符编码方式，并且将 fileencoding 设置为最终探测到的字符编码方式。因此最好将Unicode 编码方式放到这个列表的最前面，将拉丁语系编码方式 latin1 放到最后面。

* termencoding: Vim 所工作的终端 (或者 Windows 的 Console 窗口) 的字符编码方式。如果vim所在的term与vim编码相同，则无需设置。如其不然，你可以用vim的termencoding选项将自动转换成term 的编码.这个选项在 Windows 下对我们常用的 GUI 模式的 gVim 无效，而对 Console 模式的Vim 而言就是 Windows 控制台的代码页，并且通常我们不需要改变它。

--------------------------------

查看系统当前编码 locale

查看系统支持的编码 iconv -l

查看文件的编码  file -i  (注意与type不同，查看命令的类型)

在vim中 :edit  ++enc=utf8/gb18030/gb2312... 但只是编辑时转码了，重新打开还是乱码的，最好用iconv 转码，如windows文件转到Linux下，如果使用dos2unix之后 (一般只是去掉换行^M而已) 还会乱码，则可以 iconv -f GBK -t UTF-8 file1 -o file2

系统设置的编码格式

文件创建时的编码格式

编辑器打开时使用的编码格式

终端包括连接的如putty的编码格式
