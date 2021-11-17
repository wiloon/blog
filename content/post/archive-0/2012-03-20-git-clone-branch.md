---
title: git clone branch
author: "-"
date: 2012-03-20T02:15:08+00:00
url: /?p=2582
categories:
  - VCS
tags:
  - Git

---
## git clone branch
<http://wangliping.net/git-clone-spec-branch>

有时git clone下来会出现很多branch，更麻烦的是如果主分支没代码那你就只能看到.git目录了。如下面的这个:

> `$ git clone git://gitorious.org/android-eeepc/mesa.git`

发现本地就只有一个.git目录，那么这个时候就需要checkout了。

进入你的本地目录，如这个是mesa，利用

> $ git branch –r

查看branch信息（当然你也可以用git show-branch查看，不过有时并不好用) ，获得如下branch信息: 

> origin/android
  
> origin/mesa-es
  
> origin/mesa-es-dri

此时我们需要的是android分支的代码，那么此时就要进行checkout了。

> $ git checkout origin/android

你再看你的目录（mesa) 下是不是有了代码了？其它的branch同理。