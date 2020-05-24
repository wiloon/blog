---
title: java.io.tmpdir
author: wiloon
type: post
date: 2011-10-08T08:42:47+00:00
url: /?p=1003
views:
  - 27
bot_views:
  - 9
categories:
  - Java

---
<div id="csuid2_wpcpcd">
  操作系统不同 这个系统属性所表示的目录也不同
</div>

<div>
  On Windows: java.io.tmpdir:[C:DOCUME~1joshuaLOCALS~1Temp]</p> 
  
  <p>
    On Solaris: java.io.tmpdir:[/var/tmp/]
  </p>
  
  <p>
    On Linux: java.io.tmpdir: [/tmp]
  </p>
  
  <p>
    On Mac OS X: java.io.tmpdir: [/tmp]
  </p>
</div>

<div>
  <blockquote>
    <p>
      The default temporary-file directory is specified by the system property java.io.tmpdir. On UNIX systems the default value of this property is typically &#8220;/tmp&#8221; or &#8220;/var/tmp&#8221;; on Microsoft Windows systems it is typically &#8220;c:temp&#8221;. A different value may be given to this system property when the Java virtual machine is invoked, but programmatic changes to this property are not guaranteed to have any effect upon the the temporary directory used by this method.
    </p>
  </blockquote>
  
  <p>
    To specify the <code>java.io.tmpdir</code> System property, you can invoke the JVM as follows:
  </p>
  
  <pre><code>java -Djava.io.tmpdir=/path/to/tmpdir  ```
  
  <p>
    <strong>By default this value should come from the <code>TMP</code> environment variable on Windows systems</strong>
  </p>
</div>