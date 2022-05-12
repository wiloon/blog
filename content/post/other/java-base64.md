---
title: Java Base64
author: lcf
date: 2012-09-26T06:52:18+00:00
url: /?p=4310
categories:
  - Java
tags:$
  - reprint
---
## Java Base64
```java
// encode
byte[] in;
byte[] out=java.util.Base64.getEncoder().encode(in);
System.out.println(new String(out));

// decode
        byte[] byteArray = Base64.getDecoder().decode(value.getBytes());
        String base64Decode = new String(byteArray, StandardCharsets.UTF_8);

        System.out.println("base64 decode: " + base64Decode);
```