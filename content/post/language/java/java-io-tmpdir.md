---
title: java.io.tmpdir
author: "-"
date: 2011-10-08T08:42:47+00:00
url: /?p=1003
categories:
  - Java
tags:
  - reprint
---
## java.io.tmpdir

  操作系统不同 这个系统属性所表示的目录也不同


  On Windows: java.io.tmpdir:[C:DOCUME~1joshuaLOCALS~1Temp] 
  
    On Solaris: java.io.tmpdir:[/var/tmp/]
  
  
    On Linux: java.io.tmpdir: [/tmp]
  
  
    On Mac OS X: java.io.tmpdir: [/tmp]
  


  
    
      The default temporary-file directory is specified by the system property java.io.tmpdir. On UNIX systems the default value of this property is typically "/tmp" or "/var/tmp"; on Microsoft Windows systems it is typically "c:temp". A different value may be given to this system property when the Java virtual machine is invoked, but programmatic changes to this property are not guaranteed to have any effect upon the the temporary directory used by this method.
    
  
  
    To specify the java.io.tmpdir System property, you can invoke the JVM as follows:
  
  java -Djava.io.tmpdir=/path/to/tmpdir  ```
  
    By default this value should come from the TMP environment variable on Windows systems
  
