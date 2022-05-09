---
title: 静态页面html调用静态页面html的内容几种方法
author: "-"
date: 2014-02-12T03:13:08+00:00
url: /?p=6252
categories:
  - Inbox
tags:
  - HTML

---
## 静态页面html调用静态页面html的内容几种方法
静态页面html调用静态页面html的内容几种方法

简介: 在论坛中常常有网友问到,可以在一个html的文件当中读取另一个html文件的内容吗？答案是确定的,而且方法不只一种,在以前我只会使用iframe来引用,后来发现了另外的几种方法,那今天就总结这几种方法让大家参考一下,本人觉得第三种方式较好！

1.IFrame引入,看看下面的代码






你会看到一个外部引入的文件,但会发现有一个类似外框的东西将其包围,可使用





但你会发现还会有点问题,就是背景色不同,你只要在引入的文件import.htm中使用相同的背景色也可以,但如果你使用的是IE5.5的话,可以看看这篇关于透明色的文章 如果想引入的文件过长时不出现滚动条的话在import.htm中的body中加入scroll=no


2.方式


 </object>


3.Behavior的download方式








<script>

function onDownloadDone(downDate){

showImport.innerHTML=downDate

}

oDownload.startDownload('import.htm',onDownloadDone)

</script>