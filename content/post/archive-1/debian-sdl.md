---
title: 'debian & SDL'
author: "-"
date: 2013-02-13T07:33:21+00:00
url: /?p=5136
categories:
  - Linux

tags:
  - reprint
---
## 'debian & SDL'
**http://www.upubuntu.com/2012/01/how-to-install-sdl-12-simple.html**

**SDL** (**Simple DirectMedia Layer**) is a multi-platform multimedia library used by many app/game developers in creating emulators, games, MPEG playback software, etc. Also, when installing some games or software requiring SDL under Ubuntu, you may get these errors while compiling them:
  

  
**configure: error: \*** SDL version 1.2.0 not found! **
  
**configure: error: \*** SDL_image library not found! **
  
**configure: error: \*** SDL_mixer library not found!**
  
**configure: error: \*** SDL_net library not found!**

As this library is written in C++, you need to install first compiling packages under Ubuntu with this command:

**sudo apt-get install build-essential**

Now follow all these steps to install **SDL 1.2** and its related libraries:

**1. SDL Installation**

To install latest version of SDL (1.2, SDL 1.3 is still under development), run this sequence of commands from the terminal:

**wget -O SDL-1.2.14.tar.gz  http://goo.gl/ByL0B**
  
**
  
** 
  
**tar -xzvf SDL-1.2.14.tar.gz -C ~/ && cd SDL-1.2.14**
  
**
  
** 
  
**./configure && ****make**
  
**
  
** 
  
**sudo make install**

**2. SDL_image 1.2 Installation**

Via the terminal, run the following commands:

**wget -O SDL_image-1.2.11.tar.gz http://goo.gl/98zi6**
  
**
  
** 
  
**tar -xzvf SDL_image-1.2.11.tar.gz -C ~/ && cd SDL_image-1.2.11**
  
**
  
** 
  
**./configure && ****make**
  
**
  
** 
  
**sudo make install**

**3. SDL_mixer 1.2 Installation**

Run the following commands:

**wget -O SDL_mixer-1.2.12.tar.gz http://goo.gl/o0GIX**
  
**
  
** 
  
**tar -xzvf SDL_mixer-1.2.12.tar.gz -C ~/ && cd SDL_mixer-1.2.12**
  
**
  
** 
  
**./configure && ****make**
  
**
  
** 
  
**sudo make install**

**4. SDL_net 1.2 Installation**

Issue these commands:

**wget -O SDL_net-1.2.8.tar.gz http://goo.gl/AQuv5**
  
**
  
** 
  
**tar -xzvf SDL_net-1.2.8.tar.gz -C ~/ && cd SDL_net-1.2.8**
  
**
  
** 
  
**./configure && ****make**
  
**
  
** 
  
**sudo make install**

The SDL library is now compiled and installed on your system. Tested under Ubuntu 11.10/11.04.

That's it!