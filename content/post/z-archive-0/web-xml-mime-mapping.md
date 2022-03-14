---
title: web.xml – mime-mapping
author: "-"
date: 2012-06-10T04:44:26+00:00
url: /?p=3474
categories:
  - Java
  - Web
tags:
  - Servlet

---
## web.xml – mime-mapping
关联文件与MIME类型

服务器一般都具有一种让Web站点管理员将文件扩展名与媒体相关联的方法。例如，将会自动给予名为mom.jpg的文件一个image/jpeg的MIME 类型。但是，假如你的Web应用具有几个不寻常的文件，你希望保证它们在发送到客户机时分配为某种MIME类型。mime-mapping元素 (具有 extension和mime-type子元素) 可提供这种保证。例如，下面的代码指示服务器将application/x-fubar的MIME类型分配给所有以.foo结尾的文件。
  
<mime-mapping>
  
<extension>foo</extension>
  
<mime-type>application/x-fubar</mime-type>
  
</mime-mapping>
  
或许，你的Web应用希望重载 (override) 标准的映射。例如，下面的代码将告诉服务器在发送到客户机时指定.ps文件作为纯文本 (text/plain) 而不是作为PostScript (application/postscript) 。
  
<mime-mapping>
  
<extension>ps</extension>
  
<mime-type>application/postscript</mime-type>
  
</mime-mapping>


TOMCAT在默认情况下下载.rar的文件是把文件当作text打开,以至于IE打开RAR文件为乱码,如果遇到这种情况时不必认为是浏览器的问题,大多数浏览器应该不会死皮赖脸地把二进制文件当作文本打开,一般都是服务器给什么浏览器就开什么.解决方法:

打开conf/web.xml,加入下面的代码.

<mime-mapping>
  
<extension>doc</extension>
  
<mime-type>application/msword</mime-type>
  
</mime-mapping>
  
<mime-mapping>
  
<extension>xls</extension>
  
<mime-type>application/msexcel</mime-type>
  
</mime-mapping>
  
<mime-mapping>
  
<extension>pdf</extension>
  
<mime-type>application/pdf</mime-type>
  
</mime-mapping>
  
<mime-mapping>
  
<extension>zip</extension>
  
<mime-type>application/zip</mime-type>
  
</mime-mapping>
  
<mime-mapping>
  
<extension>rar</extension>
  
<mime-type>application/rar</mime-type>
  
</mime-mapping>
  
<mime-mapping>
  
<extension>txt</extension>
  
<mime-type>application/txt</mime-type>
  
</mime-mapping>
  
<mime-mapping>
  
<extension>chm</extension>
  
<mime-type>application/mshelp</mime-type>
  
</mime-mapping>
  
<mime-mapping>
  
<extension>mp3</extension>
  
<mime-type>audio/x-mpeg</mime-type>
  
</mime-mapping>

重启TOMCAT,清除IE缓存,再打开RAR的文件时就可以正常下载了.

常见的MIME类型

超文本标记语言文本 .htm,.html text/html
  
普通文本 .txt text/plain
  
RTF文本 .rtf application/rtf
  
GIF图形 .gif image/gif
  
JPEG图形 .ipeg,.jpg image/jpeg
  
au声音文件 .au audio/basic
  
MIDI音乐文件 mid,.midi audio/midi,audio/x-midi
  
RealAudio音乐文件 .ra, .ram audio/x-pn-realaudio
  
MPEG文件 .mpg,.mpeg video/mpeg
  
AVI文件 .avi video/x-msvideo
  
GZIP文件 .gz application/x-gzip
  
TAR文件 .tar application/x-tar