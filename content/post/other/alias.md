---
title: alias 别名
author: "-"
date: 2013-07-27T11:23:52+00:00
url: alias
categories:
  - Linux
tags:
  - reprint
---
## alias 别名

### 查看所有的alias

```bash
    alias
    alias -p
```

### 显示已定义的别名 (假设当前环境存在以下别名)

```bash
    alias ls
    alias ls grep
```

### 在命令行直接输入后缀为 html 的文件名,会在 vim 中打开 (zsh)

```bash
    alias -s html=vim
    alias -s gz='tar -xzvf'
```

```bash
alias ll='ls -l --color=auto'
alias la='ls -la --color=auto'
```

```bash
  
#查看命令别名
  
type ll

#取消别名
  
unalias ll

```

我们在使用linux过程中,每个命令后都要跟一些参数,可是对于常用的参数假如每次都是手动的添加就是显得麻烦些了。linux 可能通过命令别名的功能来减少您的输入,请下面操作就明白了。
  
ls -l 列出文档目录周详信息
  
ls -hl 列出文档大小,以K为单位显示
  
ls -hlt 列出文档按时间排序

对于上面三个显示需要我们只要配置alias ll='ls -lht' 这样以后,只要输入ll 就能够了。

对于此alias ll='ls -lht' 配置在哪个配置文档下呢？这个就要根据自己的需要而定了。
  
比如: 您只希望jack这个用户名具备上面功能,因为您只经常使用这个用户。修改此用户家目录下.barsh_profile 将alias ll='ls -lht' 添加进去就能够了。

假如您要对系统全局进行修改,就是任何用户都具备上面的功能,就要修改/etc/.bashrc 文档,将alias ll='ls -lht' 添加进去就行了。

假如更有其他命令也要这样做就依次添加就能够了。

alias ll='ls -lht'
  
alias df='df -h'

原文地址:
  
<http://www.idcnews.net/html/edu/linux/20080425/301436.html>
