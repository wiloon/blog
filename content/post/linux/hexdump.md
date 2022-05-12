---
title: linux hexdump
author: "-"
date: 2012-01-02T10:42:27+00:00
url: /?p=2092
categories:
  - Linux
tags:$
  - reprint
---
## linux hexdump

### 
    hexdump -e '16/1 "%02X " "\n"'
    hexdump -C

hexdump命令一般用来查看"二进制"文件的十六进制编码，但实际上它的用途不止如此，手册页上的说法是"ascii, decimal, hexadecimal, octal dump"，这也就是本文标题为什么要将"十六"给引起来的原因，而且它能查看任何文件，而不只限于二进制文件了。另外还有xxd和od也可以做类似的事情，但是我从未用过。在程序输出二进制格式的文件时，常用hexdump来检查输出是否正确。当然也可以使用Windows上的UltraEdit32之类的工具查看文件的十六进制编码，但Linux上有现成的工具，何不拿来用呢。

## 参数

如果要看到较理想的结果，使用-C参数，显示结果分为三列 (文件偏移量、字节的十六进制、ASCII字符) 。

格式: hexdump -C binfile

一般文件都不是太小，最好用less来配合一下。

格式: hexdump -C binfile | less

## 使用示例

### 示例一 比较各种参数的输出结果

[root@new55 ~]# echo /etc/passwd | hexdump
  
0000000 652f 6374 702f 7361 7773 0a64
  
000000c
  
[root@new55 ~]# echo /etc/passwd | od -x
  
0000000 652f 6374 702f 7361 7773 0a64
  
0000014
  
[root@new55 ~]# echo /etc/passwd | xxd
  
0000000: 2f65 7463 2f70 6173 7377 640a            /etc/passwd.
  
[root@new55 ~]# echo /etc/passwd | hexdump -C      <== 规范的十六进制和ASCII码显示 (Canonical hex+ASCII display ) 
  
00000000  2f 65 74 63 2f 70 61 73  73 77 64 0a              |/etc/passwd.|
  
0000000c
  
[root@new55 ~]# echo /etc/passwd | hexdump -b      <== 单字节八进制显示 (One-byte octal display) 
  
0000000 057 145 164 143 057 160 141 163 163 167 144 012
  
000000c
  
[root@new55 ~]# echo /etc/passwd | hexdump -c      <== 单字节字符显示 (One-byte character display) 
  
0000000   /   e   t   c   /   p   a   s   s   w   d  n
  
000000c
  
[root@new55 ~]# echo /etc/passwd | hexdump -d      <== 双字节十进制显示 (Two-byte decimal display) 
  
0000000   25903   25460   28719   29537   30579   02660
  
000000c
  
[root@new55 ~]# echo /etc/passwd | hexdump -o       <== 双字节八进制显示 (Two-byte octal display) 
  
0000000  062457  061564  070057  071541  073563  005144
  
000000c
  
[root@new55 ~]# echo /etc/passwd | hexdump -x       <== 双字节十六进制显示 (Two-byte hexadecimal display) 
  
0000000    652f    6374    702f    7361    7773    0a64
  
000000c
  
[root@new55 ~]# echo /etc/passwd | hexdump -v
  
0000000 652f 6374 702f 7361 7773 0a64
  
000000c

比较来比较去，还是hexdump -C的显示效果更好些。

### 示例二 确认文本文件的格式

文本文件在不同操作系统上的行结束标志是不一样的，经常会碰到由此带来的问题。比如Linux的许多命令不能很好的处理DOS格式的文本文件。Windows/DOS下的文本文件是以rn作为行结束的，而Linux/Unix下的文本文件是以n作为行结束的。

[root@new55 ~]# cat test.bc
  
123*321
  
123/321
  
scale=4;123/321

[root@new55 ~]# hexdump -C test.bc
  
00000000  31 32 33 2a 33 32 31 0a   31 32 33 2f 33 32 31 0a  |123*321.123/321.|
  
00000010  73 63 61 6c 65 3d 34 3b  31 32 33 2f 33 32 31 0a  |scale=4;123/321.|
  
00000020  0a                                                |.|
  
00000021
  
[root@new55 ~]#

注: 常见的ASCII字符的十六进制表示

r      0D

n     0A

t      09

DOS/Windows的换行符 rn 即十六进制表示 0D 0A

Linux/Unix的换行符      n    即十六进制表示 0A

### 示例三 查看wav文件

有些IVR系统需要8K赫兹8比特的语音文件，可以使用hexdump看一下具体字节编码。

[root@web186 root]# ls -l tmp.wav
  
-rw-r-r-    1 root     root        32381 2010-04-19  tmp.wav
  
[root@web186 root]# file tmp.wav
  
tmp.wav: RIFF (little-endian) data, WAVE audio, ITU G.711 a-law, mono 8000 Hz

[root@web186 root]# hexdump -C tmp.wav | less
  
00000000  52 49 46 46 75 7e 00 00  57 41 56 45 66 6d 74 20  |RIFFu~..WAVEfmt |
  
00000000  52 49 46 46 75 7e 00 00  57 41 56 45 66 6d 74 20  |RIFFu~..WAVEfmt |
  
00000010  12 00 00 00 06 00 01 00  40 1f 00 00 40 1f 00 00  |........@...@...|
  
00000020  01 00 08 00 00 00 66 61  63 74 04 00 00 00 43 7e  |......fact....C~|
  
00000030  00 00 64 61 74 61 43 7e  00 00 d5 d5 d5 d5 d5 d5  |..dataC~........|
  
00000040  d5 d5 d5 d5 d5 d5 d5 d5  d5 d5 d5 d5 d5 d5 d5 d5  |................|
  
*
  
000000a0  d5 d5 d5 d5 d5 d5 d5 d5  d5 55 d5 55 d5 d5 55 d5  |.........U.U..U.|
  
000000b0  55 d5 d5 55 d5 55 d5 d5  55 d5 55 55 55 55 55 55  |U..U.U..U.UUUUUU|
  
000000c0  55 55 55 55 55 55 55 d5  d5 d5 d5 d5 d5 d5 d5 d5  |UUUUUUU.........|
  
000000d0  d5 55 55 55 55 55 55 55  55 55 55 55 55 55 55 55  |.UUUUUUUUUUUUUUU|
  
000000e0  55 55 55 55 55 55 55 55  55 d5 d5 d5 d5 d5 d5 d5  |UUUUUUUUU.......|
  
000000f0  d5 d5 d5 d5 55 55 55 55  55 55 55 55 55 55 55 55  |....UUUUUUUUUUUU|
  
00000100  55 55 55 55 55 55 55 55  55 55 55 55 d5 d5 d5 d5  |UUUUUUUUUUUU....|
  
00000110  d5 d5 d5 d5 d5 d5 55 55  55 55 55 55 55 55 55 55  |......UUUUUUUUUU|
  
00000120  55 55 55 55 55 55 55 55  55 55 55 55 55 55 d5 d5  |UUUUUUUUUUUUUU..|
  
00000130  d5 d5 d5 d5 d5 d5 d5 d5  d5 55 55 55 55 55 55 55  |.........UUUUUUU|
  
00000140  55 55 d5 55 55 55 55 55  55 55 55 55 55 55 55 55  |UU.UUUUUUUUUUUUU|
  
00000150  55 d5 d5 d5 d5 d5 d5 d5  d5 d5 d5 55 55 55 55 55  |U..........UUUUU|
  
00000160  55 55 55 55 55 55 55 55  55 55 55 55 55 55 55 55  |UUUUUUUUUUUUUUUU|
  
00000170  55 55 55 55 d5 d5 d5 d5  d5 d5 d5 d5 d5 55 d5 55  |UUUU.........U.U|
  
00000180  55 55 55 55 55 55 55 55  55 55 55 55 55 55 55 55  |UUUUUUUUUUUUUUUU|
  
00000190  55 55 55 55 55 55 55 d5  d5 d5 d5 d5 d5 d5 d5 55  |UUUUUUU........U|
  
000001a0  55 55 55 55 55 55 55 d5  d5 55 55 55 55 55 55 55  |UUUUUUU..UUUUUUU|
  
000001b0  55 55 55 55 55 55 55 d5  55 55 d5 55 55 55 55 55  |UUUUUUU.UU.UUUUU|
  
000001c0  55 55 d5 55 d5 d5 55 d5  55 55 55 55 55 55 55 55  |UU.U..U.UUUUUUUU|
  
000001d0  55 55 55 55 55 55 55 55  55 55 55 55 55 55 55 d5  |UUUUUUUUUUUUUUU.|
  
000001e0  55 d5 d5 d5 d5 55 55 55  55 55 55 55 55 55 55 55  |U....UUUUUUUUUUU|
  
000001f0  55 55 55 55 55 55 55 55  55 55 55 55 d5 55 55 d5  |UUUUUUUUUUUU.UU.|
  
00000200  55 55 55 55 55 55 55 55  55 d5 d5 d5 d5 d5 55 55  |UUUUUUUUU.....UU|
  
00000210  55 55 55 55 55 55 55 55  55 55 55 55 55 55 55 d5  |UUUUUUUUUUUUUUU.|
  
00000220  55 55 d5 55 d5 55 55 d5  55 d5 55 55 d5 55 d5 d5  |UU.U.UU.U.UU.U..|
  
00000230  d5 d5 d5 d5 d5 d5 d5 d5  d5 d5 d5 d5 d5 d5 d5 d5  |................|
  
*
  
00000ba0  d5 d5 d5 d5 d5 d5 d5 d5  d5 d5 d5 55 55 d5 55 d5  |...........UU.U.|
  
00000bb0  55 55 d5 55 d5 55 d5 d5  55 d5 55 55 55 55 55 55  |UU.U.U..U.UUUUUU|
  
00000bc0  55 55 55 55 55 55 55 55  55 d5 d5 55 55 55 55 55  |UUUUUUUUU..UUUUU|
  
00000bd0  55 55 55 55 55 55 55 d5  55 55 55 55 55 55 d5 55  |UUUUUUU.UUUUUU.U|
  
00000be0  55 55 55 55 55 55 55 55  55 55 55 d5 55 55 55 55  |UUUUUUUUUUU.UUUU|
  
00000bf0  55 55 55 55 55 55 55 55  d5 d5 55 55 55 55 55 d5  |UUUUUUUU..UUUUU.|
  
00000c00  d5 55 55 55 55 d5 d5 d5  55 55 55 55 55 d5 d5 55  |.UUUU...UUUUU..U|
  