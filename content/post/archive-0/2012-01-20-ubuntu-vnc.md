---
title: ubuntu 10.04 vnc
author: w1100n
type: post
date: 2012-01-20T01:41:20+00:00
url: /?p=2165
categories:
  - Linux

---
第一步，获取安装文件

sudo apt-get install vnc4server

第二步，修改VNC Password，不能太短
  
＃ vncpasswd

Password: \***\***

Verify:\*****

第三步，检查防火墙，这个就不详细说明了

第四步，启动VNC server

\# vncserver

第五步，通过客户端连接

地址后面加:1

启动完vnc4server后在你的主目录下将会产生一个.vnc的目录。
  
此时就可以通过vnc客户端链接到服务器了。
  
4、停止一个vnc4server
  
vnc4server -kill :3
  
根据你启动时获得的数字替换此处的3。
  
5、打开 .vnc/xstartup 文件并编辑：
  
gedit /.vnc/xstartup
  
文件看起来将是这样的：

```bash
   
#!/bin/sh
   
\# Uncomment the following two lines for normal desktop:
   
\# unset SESSION_MANAGER
   
\# exec /etc/X11/xinit/xinitrc
   
[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
   
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
   
xsetroot -solid grey
   
vnccon** -iconic &
   
x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
   
x-window-manager &

```

6、修改 .vnc/xstartup文件并保存
  
取消unset和exec开始的行的注释，注释以xsetroot，vnccon**，xterm和twm开始的行。执行后看起来像这样：

```bash
   
#!/bin/sh
   
\# Uncomment the following two lines for normal desktop:
   
unset SESSION_MANAGER
   
exec /etc/X11/xinit/xinitrc
   
[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
   
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
   
#xsetroot -solid grey
   
#vnccon** -iconic &
   
#x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
   
#x-window-manager &

```

7、修改/etc/X11/xinit/xinitrc文件的许可，使其可执行：
  
sudo chmod 755 /etc/X11/xinit/xinitrc
  
8、启动vncserver：vncserver

设置分辨率:  vncserver -geometry 1280x1024

(vncserver is a link for vnc4server)
  
注意：记住此处冒号后提示的数字
  
9、从另外的电脑登录这台服务器：
  
vncviewer remote-server:3
  
按照提示输入你在第三部输入的密码，成功进入远程桌面。
  
10、若前面执行失败导致在VNC下看不到图形界面，鼠标变成"X"形状，请查看第七条是否执行过，同时将刚建过的VNCServer删掉，vncserver -kill :1(1代表前面启动的vncserver序号)
  
11、Ubuntu 10.10下增添了对Windows键的定义，在里面被定义为Super键，当用户在VNC下按下字母"d"时，会被错误的当做返回桌面的快捷方式导致d无法被输入，此时可修改快捷键方式来避免此bug，新打开一个终端，在里面输入：gconf-editor，这样会弹出一个对话框，到"Apps->Metacity->Global keybingdings"中找"show desktop"，将其默认值D改为D即可。
  
[自]http://hi.baidu.com/zht7216/blog/item/a30912cab1350456f01fe76e.html