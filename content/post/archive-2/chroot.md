---
title: chroot
author: "-"
date: 2017-02-28T05:00:51+00:00
url: chroot
categories:
  - linux

tags:
  - reprint
---
## chroot
<https://www.ibm.com/developerworks/cn/linux/l-cn-chroot/>

什么是 chroot
  
chroot,即 change root directory (更改 root 目录)。在 linux 系统中,系统默认的目录结构都是以 \`/\`,即是以根 (root) 开始的。而在使用 chroot 之后,系统的目录结构将以指定的位置作为 \`/\` 位置。

为何使用 chroot
  
在经过 chroot 之后,系统读取到的目录和文件将不在是旧系统根下的而是新根下(即被指定的新的位置)的目录结构和文件,因此它带来的好处大致有以下3个:

增加了系统的安全性,限制了用户的权力；在经过 chroot 之后,在新根下将访问不到旧系统的根目录结构和文件,这样就增强了系统的安全性。这个一般是在登录 (login) 前使用 chroot,以此达到用户不能访问一些特定的文件。
  
建立一个与原系统隔离的系统目录结构,方便用户的开发；使用 chroot 后,系统读取的是新根下的目录和文件,这是一个与原系统根下文件不相关的目录结构。在这个新的环境中,可以用来测试软件的静态编译以及一些与系统不相关的独立开发。
  
切换系统的根目录位置,引导 Linux 系统启动以及急救系统等。chroot 的作用就是切换系统的根位置,而这个作用最为明显的是在系统初始引导磁盘的处理过程中使用,从初始 RAM 磁盘 (initrd) 切换系统的根位置并执行真正的 init。另外,当系统出现一些问题时,我们也可以使用 chroot 来切换到一个临时的系统。

## check if in chroot

```bash
if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
  echo "We are chrooted!"
else
  echo "Business as usual"
fi

```

<https://unix.stackexchange.com/questions/14345/how-do-i-tell-im-running-in-a-chroot>
