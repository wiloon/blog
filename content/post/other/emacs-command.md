---
title: emacs command
author: "-"
date: 2014-03-08T08:34:47+00:00
url: /?p=6370
categories:
  - Inbox
tags:
  - emacs

---
## emacs command

M-x artist-mode
  
M-x artist-mode-off


跳转到行
  
(define-key global-map "\C-c\C-g" 'goto-line)

`C-x C-f 文件名' — 打开文件`C-x C-s' — 保存文件
  
`C-x C-c' — 退出Emacs`C-x u' — 取消上一次操作
  
C-x C-w 按提示输入文件名,另存为

窗格
  
C-x 2 M-x split-window-vertically 分隔出两个垂直窗格,水平分隔线
  
C-x 3 M-x split-window-horizontally 分隔出两个水平窗格,垂直分隔线
  
C-x 1 M-x delete-other-window 只保留当前窗格
  
ESC ESC ESC M-x keyboard-escape-quit 只保留当前窗格
  
C-x 0 M-x delete-window 关闭当前窗格
  
C-x o M-x other-window 在下一个窗格中激活光标
  
C-M-v M-x scroll-other-window 向下卷动下一个窗格,使用负参数可以向上卷动

缓冲区
  
C-x C-b M-x list-buffers 查看缓冲区列表
  
C-x b M-x switch-to-buffer 切换到其它缓冲区
  
C-x k M-x kill-buffer 关闭当前缓冲区

to archive all done item c-c c-x c-s

M-x occur 统计该表达式在buffer中出现的次数,显示在哪些地方出现了这个表达式.

ALT+X hexl-mode 进入16进制模式

`C-'开头的是`Ctrl'键加上后面的键一块按下,例如 \`C-x 0′就是Ctrl键和 x键一块按下, 然后再按下0;

以 \`M-'开头的就是META键, 一般就是 Alt键.

http://hi.baidu.com/gz_gzhao/item/0090f3bfdeca95442bebe37d
  
https://i.linuxtoy.org/docs/guide/ch25s10.html
  
http://www.cnblogs.com/robertzml/archive/2010/03/24/1692737.html

## emacs 慢

emacs 总是在启动的时候停顿两三秒钟。用 emacs -q 也是一样,so 不是扩展或者设置造成的启动速度慢的问题。strace 了一下,发现居然是在 poll nameserver。
感觉很奇怪且不正常。往前看log发现emacs扫了一堆的系统文件,再看 poll 之前,居然是发送了一个怪怪的包含我 hostname 的字符串给 nameserver。
结果很简单,就是因为 emacs 没在 /etc/hosts 里面找到 hostname 对应的 ip,所以向 nameserver 发请求解析。解决方式很简单,给 /etc/hosts 里面 localhost 后面加上 hostname 即可。

[http://blog.chinaunix.net/uid-20228521-id-3032489.html](http://blog.chinaunix.net/uid-20228521-id-3032489.html)
