---
title: git repo backup
author: "-"
date: 2012-04-03T02:13:21+00:00
url: /?p=2750
categories:
  - VCS
tags:
  - Git

---
## git repo backup

```bash
git bundle create /tmp/somefile master
```

然后传输这个文件包， somefile ，给某个其他参与者: 电子邮件，优盘，一个 xxd 打印品和一个OCR扫描仪，通过电话读字节，狼烟，等等。接收者通过键入如下命 令从文件包获取提交:

$ git pull somefile
  
接收者甚至可以在一个空仓库做这个。不考虑大小， somefile 可以包含整个原先 git仓库。

在较大的项目里，可以通过只打包其他仓库缺少的变更消除浪费。例如，假设提交 '\`1b6d…''是两个参与者共享的最近提交:

$ git bundle create somefile HEAD ^1b6d
  
如果做的频繁，人可能容易忘记刚发了哪个提交。帮助页面建议使用标签解决这个问题。 即，在你发了一个文件包后，键入:

$ git tag -f lastbundle HEAD
  
并创建较新文件包，使用:

$ git bundle create newbundle HEAD ^lastbundle

<http://www-cs-students.stanford.edu/~blynn/gitmagic/intl/zh_cn/ch06.html>

<http://stackoverflow.com/questions/2129214/backup-a-local-git-repository>
