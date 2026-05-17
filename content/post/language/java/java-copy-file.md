---
title: java copy file
author: "-"
date: 2014-11-27T02:53:36+00:00
url: java-copy-file
categories:
  - Inbox
tags:
  - Java

aliases:
  - /p7049/
---
## java copy file
http://www.oschina.net/question/565065_58510

```java
  
private static void nioTransferCopy(File source, File target) {
  
FileChannel in = null;
  
FileChannel out = null;
  
FileInputStream inStream = null;
  
FileOutputStream outStream = null;
  
try {
  
inStream = new FileInputStream(source);
  
outStream = new FileOutputStream(target);
  
in = inStream.getChannel();
  
out = outStream.getChannel();
  
in.transferTo(0, in.size(), out);
  
} catch (IOException e) {
  
e.printStackTrace();
  
} finally {
  
close(inStream);
  
close(in);
  
close(outStream);
  
close(out);
  
}
  
}
  
```