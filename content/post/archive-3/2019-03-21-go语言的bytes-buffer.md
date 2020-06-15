---
title: go语言的bytes.buffer
author: wiloon
type: post
date: 2019-03-21T02:43:54+00:00
url: /?p=13890
categories:
  - Uncategorized

---
##bytes.buffer是 bytes.buffer是一个缓冲byte类型的缓冲器，这个缓冲器里存放着都是byte

##创建一个缓冲器 ###NewBuffer
  
如果在使用bytes.NewBuffer的时候，参数是[]byte的slice的话
  
缓冲器里就是这个slice的内容，如果参数是nil的话，意思是New一个空的缓冲器里
  
###NewBufferString
  
还可以用bytes.NewBufferString("hello&#8221;)来建立一个内容是hello的缓冲器

buf1:=bytes.NewBufferString("hello&#8221;)
  
buf2:=bytes.NewBuffer([]byte("hello&#8221;))
  
buf3:=bytes.NewBuffer([]byte{"h&#8221;,&#8221;e&#8221;,&#8221;l&#8221;,&#8221;l&#8221;,&#8221;o&#8221;})
  
以上三者等效
  
buf4:=bytes.NewBufferString("&#8221;)
  
buf5:=bytes.NewBuffer([]byte{})
  
以上两者等效
  
如果buffer在new的时候是空的也没关系，因为可以用Write来写入，写在尾部

##写入到缓冲器（缓冲器变大） ###Write&#8212;- func (b *Buffer) Write(p []byte) (n int, err error) 使用Write方法，将一个byte类型的slice放到缓冲器的尾部

https://my.oschina.net/u/943306/blog/127981