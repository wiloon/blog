---
title: Install GUI on debian 7 wheezy
author: "-"
date: 2014-03-29T05:06:31+00:00
url: /?p=6446

categories:
  - inbox
tags:
  - reprint
---
## Install GUI on debian 7 wheezy

<http://namhuy.net/1085/install-gui-on-debian-7-wheezy.html>

This article will show you how to install GUI (Graphical User Interface) of your choice (gnome, kde, Cinnamon, mate, enlightenment, xfce, or lxde) on debian 7. The two biggest players in the game are Gnome and KDE, but there are also many smaller GUIs, like Xfce and LXDE that have just as much to offer.

Download Debian 7 wheezy

For leaner and better control of what you install on your machine, I highly recommend you to download and install debian minimal CD or netinst.

x32 <http://cdimage.debian.org/debian-cd/7.4.0/i386/iso-cd/debian-7.4.0-i386-netinst.iso>

x64 <http://cdimage.debian.org/debian-cd/7.4.0/amd64/iso-cd/debian-7.4.0-amd64-netinst.iso>

When you are at "Software selection" screen, \*unselect\* all the option.

If you already have debian installed and you want to find out what your debian version is, you can use this command

$ cat /etc/debian_version

Gnome

GNU Object Model Environment (Gnome) is a desktop environment and graphical user interface that runs on top of a computer operating system, user-friendly desktop for Unix operating systems, based entirely on free software.

You will need to install aptitude and tasksel before install gnome

Aptitude is an Ncurses based FrontEnd to Apt, the debian package manager.

Tasksel is a tool that installs multiple related packages as a co-ordinated "task" onto your system.

# apt-get install aptitude tasksel

Install gnome on debian

# tasksel install gnome-desktop -new-install

KDE

K Desktop Environment (KDE) is a free desktop environment and development platform built with Trolltech's Qt toolkit. It runs on most Unix and Unix-like systems, such as Linux, BSD and Solaris.

# apt-get install aptitude tasksel

# aptitude -without-recommends install ~t^standard$ ~t^desktop$ ~t^kde-desktop$

Or install KDE from the default repositorie

# apt-get install kde-standard

Compiz

Compiz is truly one of the original compositing window managers for the X Window System which is capable to make use of OpenGL-acceleration. The integration enables it to run compositing effects in window management, for example a minimization effect and a cube workspace. Compiz conforms to the ICCCM standard together with replacement for the main Metacity in GNOME or KWin in KDE.

# echo "deb <http://ftp.us.debian.org/debian/> sid main non-free contrib" >> /etc/apt/sources.list

# echo 'APT::Default-Release "testing";' >> /etc/apt/apt.conf

# apt-get update

# apt-get -t sid install compiz compiz-fusion-plugins-extra compizconfig-settings-manager

# compiz -replace

You can configure Compiz via CCSM utility. located in System -> Preferences -> CompizConfig

Cinnamon

Cinnamon is a Linux desktop which provides advanced innovative features and a traditional user experience. The desktop layout is similar to Gnome 2. The underlying technology is forked from Gnome Shell. The emphasis is put on making users feel at home and providing them with an easy to use and comfortable desktop experience.Cinnamon has rich visual effects enabled by new graphical technologies.

Edit /etc/apt/sources.list

# nano /etc/apt/sources.list

Add these to the file

deb <http://packages.linuxmint.com/> debian main upstream import

deb <http://debian.linuxmint.com/latest> testing main contrib non-free

deb <http://debian.linuxmint.com/latest/security> testing/updates main contrib non-free

deb <http://debian.linuxmint.com/latest/multimedia> testing main non-free

Change the content of /etc/apt/preferences like this

Package: *

Pin: release o=linuxmint

Pin-Priority: 700

Package: *

Pin: origin packages.linuxmint.com

Pin-Priority: 700

Package: *

Pin: release o=Debian

Pin-Priority: 500

Install linuxmint-keyring package or GnuPG key from Linux Mint repository

# apt-get install linuxmint-keyring

After that change /etc/apt/apt.conf.d/80mintupdate-debian

# nano /etc/apt/apt.conf.d/80mintupdate-debian

To

Acquire::Check-Valid-Until "false";

Finally we can install cinnamon on debian 7 wheezy now

# apt-get dist-upgrade

# apt-get install mint-debian-mirrors inxi mint-meta-debian-cinnamon mint-info-debian-cinnamon

MATE

The MATE Desktop Environment, a non-intuitive and unattractive desktop for users, using traditional computing desktop metaphor. MATE is based on old Gnome 2, which is stable, tried and true. Because of it has been around for so much longer, tools have been developed for it which makes Gnome 2 highly compatible with most software and also highly configurable (for example, you can run Compiz on it).

Add one of MATE repositories to your source.list

# nano /etc/apt/sources.list

# main repository

deb <http://repo.mate-desktop.org/debian> wheezy main

# mirrors

deb <http://packages.mate-desktop.org/repo/debian> wheezy main

deb <http://mirror1.mate-desktop.org/debian> wheezy main

Install MATE on debian

# apt-get update

# apt-get install mate-archive-keyring

# apt-get update

# Now to install MATE choose 1 of the 3 apt-get lines below

# this installs the base packages

# apt-get install mate-core

# or this to install mate-core and more extras

# apt-get install mate-desktop-environment

# or this to install mate-core + mate-desktop-environment and even more extras

# apt-get install mate-desktop-environment-extra

Enlightenment

Enlightenment is not only one desktop environment for Linux, but it has an entirely libraries to assist you to produce gorgeous end user interfaces together with a lesser amount of computer resource as compared to doing it the particular traditional way, it also helping together with classic toolkits, not forgetting an old-fashioned window manager.

# wget -c www.debe17.com/debian/debe17-svn_1.1.1-0_all.deb

# dpkg -i debe17-svn_1.1.1-0_all.deb

XFCE

Xfce is a lightweight desktop environment for UNIX-like operating systems. It aims to be fast and low on system resources, while still being visually appealing and user friendly.

To install Xfce on debian 7 wheezy

# apt-get install xorg xfce4 xfce4-goodies thunar-archive-plugin synaptic gdebi wicd

To install extra XFCE packages

# apt-get install xdg-utils xfce4-power-manager xfce4-goodies htop bzip2 zip unzip unrar-free

To start xfce

Once the xfce installation is done, reboot your sytem, login with your username and password, then type

$ startx

or

$ startxfce4

To start xfce automatically when you login to tty1

edit .bashrc in your user directory

$ cd /home/yourusername

$ nano .bashrc

add these code to the end of the .bashrc file

if [ "$(tty)" = "/dev/tty1" -o "$(tty)" = "/dev/vc/1" ] ; then

startxfce4

fi

LXDE

The LXDE or "Lightweight X11 Desktop Environment" is an extremely fast-performing and energy-saving desktop environment. LXDE uses less CPU and less RAM than other environments. It is especially designed for cloud computers with low hardware specifications, such as netbooks, mobile devices (e.g. MIDs) or older computers. LXDE can be installed on many Linux distributions including Debian, Fedora, OpenSUSE and Ubuntu.

minimum set of elements

# apt-get install lxde-core

complete set of elements

# apt-get install lxde

complete Debian LXDE desktop environment

# apt-get install task-lxde-desktop

FluxBox

Fluxbox is a extremely minimalistic and fast window manager for Linux and Unix systems. Based on the Blackbox 0.61.1 code, FluxBox uses very little resources and memory compare to KDE or Gnome which is great for older or low-powered machines. To install FluxBox on debian 7 wheezy.

You will need to install X before FluxBox

$ su -

# apt-get update && apt-get install xorg

After you installed X, you now can install FluxBox on debian wheezy.

# apt-get install fluxbox

The fluxbox package from debian contains:

fluxbox: window manager

fbsetbg: setup script for rootwindow's background

fbrun: small RunApplication tool

startfluxbox: Fluxbox starter that reads session information from ~/.fluxbox/startup
