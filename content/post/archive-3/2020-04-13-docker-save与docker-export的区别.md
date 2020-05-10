---
title: docker save与docker export的区别
author: wiloon
type: post
date: 2020-04-13T05:24:16+00:00
url: /?p=15930
categories:
  - Uncategorized

---
https://jingsam.github.io/2017/08/26/docker-save-and-docker-export.html

docker save与docker export的区别docker save和docker export的区别
  
总结一下docker save和docker export的区别：

docker save保存的是镜像（image），docker export保存的是容器（container）；
  
docker load用来载入镜像包，docker import用来载入容器包，但两者都会恢复为镜像；
  
docker load不能对载入的镜像重命名，而docker import可以为镜像指定新名称。

<pre><code class="language-bash line-numbers">docker save -o images.tar postgres:9.6
</code></pre>