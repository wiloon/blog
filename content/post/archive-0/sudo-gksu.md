---
title: sudo gksu
author: "-"
date: 2012-03-13T03:31:57+00:00
url: /?p=2546
categories:
  - Linux

---
## sudo gksu
GKSu is a library that provides a Gtk+ frontend to su and sudo. It supports login shells and preserving environment when acting as a su frontend. It is useful to menu items or other graphical programs that need to ask a user's password to run another program as another user.

sudo 用来执行命令行（CLI) 程序
  
gksu 用来执行图形的（GUI) 程序

GUI = Graphical User Interface
  
CLI = Command Line Interface

sudo 是当前用户的home目录，gksu 是root 用户的home目录

sudo gvim 和 gksu gvim 明显不同，
  
sudo gvim 读取当前用户下的 ~/.gvim 配置文件，
  
gksu 读取 root 用户的配置文件，因为当前用户配置文件里设置字体没起作用，:cd 后 :pwd 结果是 /root

所以在系统或程序启动时，没有运行终端CLI，可以用gksu来实行root权限。

su/sudo for CLI commands, and gksu/gksudo for running GUI applications (launched from the command line).

In ubuntu gksudo is just a link to gksu, so your always running gksu anyways. You can check for yourself> nautilus /usr/bin

Here's a little known tip, if you run just "gksu" you will get a root run dialog, to run any app as root or other user.

  1. In Ubuntu (I suppose in most unix/linux systems), there is a user called root (also called superuser) that has the necessary rights (privileges) to do anything that he wants. 
  2. In Ubuntu, they have chosen to disable the root user, because any user that belongs to the admin group is able to execute commands as if he was the root user. To execute a command with the same privileges as the root user, he has to put the word "sudo" before the command. (I suppose, sudo stands for SuperUserDO)

  3. There is also the command su, that stands for switch user. It is intended to switch from one user to another user in the terminal; the syntax is "su name_of_the_other_user".

  4. If you call su without indicating the name_of_the_other_user, su assumes that the other user is the root user. So Ubuntu edgy and feisty simply replaces sudo with su without the name_of_the_other_user, which corresponds to su root.
  
    (Question: how can su switch to the root user if the root user is disabled?)

  5. gksu and gksudo are in the graphical environments what su and sudo are in the terminal.
  
    By the way, I have read in another thread: people should use gksudo in the terminal to launch a graphical application with root privileges; for example "gksudo gedit". It is also possible to use "sudo gedit", but it is not a good way to do it, because gksudo sets up things for a graphical environment, but sudo sets them up for a text environment. (or something like this)

http://www.nongnu.org/gksu/