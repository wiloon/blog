---
title: debian installation
author: "-"
type: post
date: 2012-11-28T14:26:30+00:00
url: /?p=4797
categories:
  - Linux

---
##click the icon "open this note in a new window

#tuo.. terminal icon to the task bar

#delete icons of the default mail and browser

#######################comment out cdrom... from source list

su -

#input root password

gedit /etc/apt/source.list

#comment out the line contains cdrom...

########################chinese support

#install locals, maybe already installed

sudo apt-get install locales

#configure locales, select item which start with zh

sudo dpkg-reconfigure locales

#select all lines start with zh_... , select OK move to  next screen.

#select en_US as default language of the system

#double check the language setting

sudo locale

########################chrome

#install chrome, download a deb file from web site .. do not install from software center.

#http://www.google.cn/chrome/

#chrome will not be added to start menu automaticlly,

#add a launcher for chrome manually,the command is google-chrome

###########################install wqy font

sudo apt-get install xfonts-wqy

sudo apt-get install xfonts-intl-chinese wqy*

#set chrome's font as wqy micro hei, size 16, set font "fix width" with micro hei mono, set encoding as utf8, restart the chrome

#restart chrome,


#######################input method

#go to System>Administration>Software Center

#Search ibus

#install IBUS Preferences

#install wubi input method

  #search "wubi" in software center


  #install wubi input method base on table engine of ibus


  #right click the ibus icon and select restart, restart the ibus


  #select wubi in ibus...


  #install pinyin engine for ibus

#start ibus, goto System>Preferences>IBUS... ,,, maybe need restart the system to enable the wubi and pinyin...

  #there will be a alert, "if can not use ibus add follow lines to .bashrc


  #export GTK_IM_MODULE=ibus


  #export XMODIFIERS=@im=ibus


  #export QT_IM_MODULE=ibus


#######################system monitor

#add system monitor to tool bar

#######################terminal's color

#update terminal's color config, select gray and black

#edit ~./.bashrc

#remove the comments for

alias ll='ls -l'

#######################sudoer

#edit sudoer

su -

#input root password

chmod u+w /etc/sudoers

vi /etc/sudoers

#find line root ALL=(ALL) ALL

#add a new line

xxx ALL=(ALL) ALL

#xxx is your user name

#save and exit

chmod u-w /etc/sudoers

#########################update source list to 163

http://ubuntu.cn99.com/.help/debian.html
