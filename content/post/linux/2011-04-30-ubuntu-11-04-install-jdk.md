---
title: ubuntu 11.04 install JDK
author: w1100n
type: post
date: 2011-04-30T05:35:15+00:00
url: /?p=128
bot_views:
  - 25
views:
  - 2
categories:
  - Java
  - Linux

---
down load latest jdk from oracle.
  
open a terminal.
  
sh jdk-6u25-linux-i586.bin

sudo gedit /etc/environment
  
add /\***/jdk1.6.0_25/bin to path

add ...
  
JAVA_HOME=/\***/jdk1.6.0_25
  
CLASSPATH=.:/\***/jdk1.6.0_25/lib

sudo update-alternatives -install /usr/bin/java java /\***/jdk1.6.0_25/bin/java 300
  
sudo update-alternatives -install /usr/bin/javac javac /\***/jdk1.6.0_25/bin/javac 300

udo update-alternatives -config java