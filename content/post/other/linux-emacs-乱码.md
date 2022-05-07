---
title: linux emacs 乱码
author: "-"
date: 2015-05-04T03:02:58+00:00
url: /?p=7597
categories:
  - Inbox
tags:
  - emacs

---
## linux emacs 乱码
其实就是编码字符不是utf-8的问题导致。什么年代了，这么多软件也不往通用标准靠，非要使用所谓的中文编码。射手网下载的东西几乎都是这个毛病。

在Ubuntu下用Emacs打开的时候看到的也是乱码，不过好解决，在~/.emacs.d/init.el文件中添加一行设置: 

(set-language-environment "Chinese-GB")

重新启动Emacs，打开文件，中文正确显示了。

如果只是想临时用一下，运行命令: 

M-x

set-language-environment

然后输入Chinese-GB，最后刷新缓冲区即可。


alt + x

revert-buffer

http://stackoverflow.com/questions/10500323/how-to-see-the-files-encoding-in-emacs