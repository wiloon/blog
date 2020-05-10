---
title: linux modprobe
author: wiloon
type: post
date: 2011-08-20T20:06:06+00:00
url: /?p=471
bot_views:
  - 5
views:
  - 1
categories:
  - Linux

---
modprobe可载入指定的个别模块，或是载入一组相依的模块。modprobe会根据depmod所产生的相依关系，决定要载入哪些模块。若在载入过程中发生错误，在modprobe会卸载整组的模块

https://blog.csdn.net/future_fighter/article/details/3862795

# 列出内核已载入模块的状态

lsmod
  
功能：
  
用法：lsmod
  
描述:
      
lsmod 以美观的方式列出/proc/modules的内容。
      
输出为：
      
Module(模块名) Size(模块大小) Used by(被&#8230;使用)

<pre><code class="language-shell line-numbers">modinfo module_name
systool -v -m module_name

modprobe --show-depends

手动加载卸载
控制内核模块载入/移除的命令是kmod 软件包提供的, 要手动装入模块的话，执行:

# modprobe module_name
如果要移除一个模块：

# modprobe -r module_name
或者:

# rmmod module_name
</code></pre>

https://wiki.archlinux.org/index.php/Kernel\_modules\_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)