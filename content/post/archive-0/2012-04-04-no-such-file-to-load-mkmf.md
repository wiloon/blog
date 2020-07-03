---
title: no such file to load — mkmf
author: wiloon
type: post
date: 2012-04-04T10:08:23+00:00
url: /?p=2800
categories:
  - Development
  - Linux

---
[shell]
  
Building native extensions. This could take a while...
  
ERROR: Error installing rails:
	  
ERROR: Failed to build gem native extension.

/usr/bin/ruby1.8 extconf.rb
  
extconf.rb:1:in \`require': no such file to load - mkmf (LoadError)
	  
from extconf.rb:1
  
[/shell]

For some reason, mkmf.rb is part of the ruby1.8-dev package, and initially I hadn't installed that.

#install ruby1.8-dev
  
[shell]
  
sudo apt-get install ruby1.8-dev
  
[/shell]
  
and everything trotted along happily after that.