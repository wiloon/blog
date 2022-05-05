---
title: size
author: "-"
date: 2012-07-12T04:17:32+00:00
url: size
categories:
  - Linux

tags:
  - reprint
---
## size
size 程序列出参数列表中各目标文件或存档库文件的段大小 — 以及总大小。默认情况下，对每个目标文件或存档库中的每个模块都会产生一行输出。
```bash
size foo
```


    wiloonwy@penguin:~/tmp$ size foo 
      text    data     bss     dec     hex filename
      1458     584       8    2050     802 foo

前三部分的内容是文本段、数据段和 bss 段及其相应的大小。然后是十进制格式和十六进制格式的总大小。最后是文件名。

```bash
size foo --format=SysV
```

```
foo  :
section              size    addr
.interp                28     792
.note.gnu.property     64     824
.note.gnu.build-id     36     888
.note.ABI-tag          32     924
.gnu.hash              28     960
.dynsym               168     992
.dynstr               130    1160
.gnu.version           14    1290
.gnu.version_r         32    1304
.rela.dyn             192    1336
.rela.plt              24    1528
.init                  27    4096
.plt                   32    4128
.text                 405    4160
.fini                  13    4568
.rodata                17    8192
.eh_frame_hdr          52    8212
.eh_frame             216    8264
.init_array             8   15848
.fini_array             8   15856
.dynamic              480   15864
.got                   40   16344
.got.plt               32   16384
.data                  16   16416
.bss                    8   16432
.comment               18       0
.debug_aranges         48       0
.debug_info           140       0
.debug_abbrev          67       0
.debug_line            86       0
.debug_str            133       0
.debug_line_str       123       0
Total                2717
```