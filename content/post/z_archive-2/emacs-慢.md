---
title: emacs 慢
author: "-"
date: 2016-01-06T02:01:28+00:00
url: /?p=8648
categories:
  - Inbox
tags:
  - reprint
---
## emacs 慢

emacs 总是在启动的时候停顿两三秒钟。用 emacs -q 也是一样,so 不是扩展或者设置造成的启动速度慢的问题。strace 了一下,发现居然是在 poll nameserver。感觉很奇怪且不正常。往前看log发现emacs扫了一堆的系统文件,再看 poll 之前,居然是发送了一个怪怪的包含我 hostname 的字符串给 nameserver。结果很简单,就是因为 emacs 没在 /etc/hosts 里面找到 hostname 对应的 ip,所以向 nameserver 发请求解析。解决方式很简单,给 /etc/hosts 里面 localhost 后面加上 hostname 即可。

[http://blog.chinaunix.net/uid-20228521-id-3032489.html](http://blog.chinaunix.net/uid-20228521-id-3032489.html)
