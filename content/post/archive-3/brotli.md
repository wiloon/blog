---
title: Brotli
author: "-"
date: 2019-05-15T01:03:38+00:00
url: /?p=14340
categories:
  - Uncategorized

tags:
  - reprint
---
## Brotli
https://segmentfault.com/a/1190000009374437

使用Brotli提高网站访问速度
  
在优化网站打开速度上，我们有很多的方法，而其中一个就是减少诸如Javascript和CSS等资源文件的大小，而减少文件大小的方法除了在代码上下功夫外，最常用的方法就是使用压缩算法对文件进行压缩。

目前，网站普遍使用的是gzip压缩算法，当然你可能还知道deflate和sdch算法，但是最近两年新兴了一个新的压缩算法: Brotli，下面我将会对这个算法进行简单的介绍。

什么是Brotli
  
Brotli最初发布于2015年，用于网络字体的离线压缩。Google软件工程师在2015年9月发布了包含通用无损数据压缩的Brotli增强版本，特别侧重于HTTP压缩。其中的编码器被部分改写以提高压缩比，编码器和解码器都提高了速度，流式API已被改进，增加更多压缩质量级别。新版本还展现了跨平台的性能改进，以及减少解码所需的内存。

与常见的通用压缩算法不同，Brotli使用一个预定义的120千字节字典。该字典包含超过13000个常用单词、短语和其他子字符串，这些来自一个文本和HTML文档的大型语料库。预定义的算法可以提升较小文件的压缩密度。

使用brotli取代deflate来对文本文件压缩通常可以增加20%的压缩密度，而压缩与解压缩速度则大致不变。

浏览器支持情况
  
图片描述

Chrome从版本49开始支持，但是完整的支持是在版本50 (2016年5月27日开始支持) 。

Firefox从版本52开始支持。

IE全版本不支持，但是Edge从版本15开始支持。

Safari全系不支持。

Opera从版本44开始支持。

支持Brotli压缩算法的浏览器使用的内容编码类型为br，例如以下是Chrome浏览器请求头里Accept-Encoding的值: 

Accept-Encoding: gzip, deflate, sdch, br
  
如果服务端支持Brotli算法，则会返回以下的响应头: 

Content-Encoding: br
  
需要注意的是，只有在HTTPS的情况下，浏览器才会发送br这个Accept-Encoding。

关于性能
  
下面是LinkedIn做的一个性能测试结果: 

enter image description here

Algorithm Quality Compression Time (ms) Decompression Time (ms)
  
gzip 6 169 35
  
gzip 9 284 27
  
zopfli 15 37,847 32
  
zopfli 100 194,460 38
  
zopfli 1000 1,855,480 29
  
brotli 4 109 24
  
brotli 5 193 20
  
brotli 5 517 23
  
brotli 11 11,913 22
  
可以看到，Brotli的压缩率更高，意味着通过Brotli算法压缩的文件，文件大小更小，但是由表格可以看到，Brotli的压缩时间比gzip要多，而解压时间则相当。所以在运行中 (on-the-fly) 使用Brotli算法压缩文件可能并不是一个很好的方案，下面我们再探讨下。

更多的评测可以看以下两个链接: 

https://cran.r-project.org/we...

https://hacks.mozilla.org/201...

使用Brotli
  
Brotli有更高的压缩率，但是同时也需要更长的压缩时间，所以在请求的时候实时进行压缩并不是一个很好的实践 (当然你可以这么做) 。我们可以预先对静态文件进行压缩，然后直接提供给客户端，这样我们就避免了Brotli压缩效率低的问题，同时使用这个方式，我们可以使用压缩质量最高的等级去压缩文件，最大程度的去减小文件的大小。

另外，由于不是所有浏览器都支持Brotli算法，所以在服务端，我们需要同时提供两种文件，一个是经过Brotli压缩的文件，一个是原始文件，在浏览器不支持Brotli的情况下，我们可以使用gzip去压缩原始文件提供给客户端。

具体的实现可以参照下Linkin的这篇文章: https://engineering.linkedin....。

在Nginx上启用Brotli
  
nginx目前并不支持Brotli算法，需要使用第三方模块，例如ngx_brotli进行实现。下面是简单的安装步骤。

安装及配置
  
下载ngx_brotli模块及其依赖: 

$ git clone https://github.com/google/ngx_brotli
  
$ cd ngx_brotli
  
$ git submodule update -init
  
编译Nginx时加入ngx_brotli模块: 

$ cd /path/to/nginx_source/
  
$ ./configure -add-module=/path/to/ngx_brotli
  
$ make && make install
  
在Nginx配置文件的http块下增加以下指令: 

brotli on;
  
brotli_comp_level 6;
  
brotli_buffers 16 8k;
  
brotli_min_length 20;
  
brotli_types *;
  
以上是on-the-fly的配置方式，如果是要响应已经使用Brotli压缩过的文件，则使用brotli_static指令。下面是ngx_brotli模块相关指令的一些简单解析。

模块指令解析
  
brotli_static
  
启用后将会检查是否存在带有br扩展的预先压缩过的文件。如果值为always，则总是使用压缩过的文件，而不判断浏览器是否支持。

brotli
  
是否启用在on-the-fly方式压缩文件，启用后，将会在响应时对文件进行压缩并返回。

brotli_types
  
指定对哪些内容编码类型进行压缩。text/html内容总是会被进行压缩。

brotli_buffers
  
设置缓冲的数量和大小。大小默认为一个内存页的大小，也就是4k或者8k。

brotli_comp_level
  
设置压缩质量等级。取值范围是0到11.

brotli_window
  
设置窗口大小。

brotli_min_length
  
设置需要进行压缩的最小响应大小。

具体信息请参看: https://github.com/google/ngx...

参考
  
https://en.wikipedia.org/wiki...

https://engineering.linkedin....

https://github.com/google/ngx...

http://caniuse.com/#search=br...