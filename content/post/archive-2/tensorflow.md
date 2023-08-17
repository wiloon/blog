---
title: archlinux, tensorFlow, golang
author: "-"
date: 2017-04-04T17:15:15+00:00
url: /?p=10018
categories:
  - Inbox
tags:
  - reprint
---
## archlinux, tensorFlow, golang

build tensorflow

```bash
  

git clone https://github.com/tensorflow/tensorflow
  
sudo pacman -S bazel
  
sudo pacman -S python-numpy

```

```bash

docker run -it -p 8888:8888 gcr.io/tensorflow/tensorflow

docker run -it gcr.io/tensorflow/tensorflow bash

```

https://www.tensorflow.org/install/install_linux#InstallingDocker

https://www.tensorflow.org/get_started/get_started