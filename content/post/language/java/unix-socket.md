---
title: Java Unix Socket
author: "-"
date: 2015-08-26T07:50:44+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: java-unix-socket
categories:
  - Java
tags:
  - java
  - socket
  - remix
  - AI-assisted
aliases:
  - /p8161/
---
## Java Unix Socket
http://www.oschina.net/p/juds/similar_projects?lang=0&sort=view

Java Unix Domain Sockets (JUDS) 提供了 Java 的方法用来访问 Unix domain sockets  socket 。

```xml
<dependency>
   <groupId>uk.co.caprica</groupId>
   <artifactId>juds</artifactId>
   <version>0.94.1</version>
</dependency>
```

示例代码: 

```java
package com.google.code.juds.test;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import com.google.code.juds.*;
public class TestUnixDomainSocket {
        public static void main(String[] args) throws IOException {
                if (args.length != 1) {
System.out
                                        .println("usage: java TestUnixDomainSocket socketfilename");
                        System.exit(1);
                }
                String socketFile = args[0];
                byte[] b = new byte[128];
                // Testcase 1.1: Test UnixDomainSocketClient with a stream socket
                UnixDomainSocketClient socket = new UnixDomainSocketClient(socketFile,
                                UnixDomainSocket.SOCK_STREAM);
                InputStream in = socket.getInputStream();
                OutputStream out = socket.getOutputStream();
                in.read(b);
                System.out.println("Text received: \"" + new String(b) + "\"");
                String text = "[2] Hello! I'm the client!";
                out.write(text.getBytes());
                System.out.println("Text sent: " + "\"" + text + "\"");
                socket.close();
                // Testcase 1.2: Test UnixDomainSocketClient with a datagram socket
                socket = new UnixDomainSocketClient(socketFile,
                                UnixDomainSocket.SOCK_DGRAM);
                System.out.println("Provoke and catch an "
                                + "UnsupportedOperationException:");
                try {
                        in = socket.getInputStream();
                } catch (UnsupportedOperationException e) {
                        System.out.println("UnsupportedOperationException has been "
                                        + "thrown as expected.");
                }
                out = socket.getOutputStream();
                text = "[3] Hello! I'm the client!";
                out.write(text.getBytes());
                System.out.println("Text sent: \"" + text + "\"");
                socket.close();
                // Testcase 2.1: Test UnixDomainSocketServer with a stream socket
                System.out.println("\nTest #2: Test UnixDomainSocketServer\nTestcase "
                                + "2.1: Test UnixDomainSocketServer with a stream socket...");
                UnixDomainSocketServer ssocket = new UnixDomainSocketServer(socketFile,
                                UnixDomainSocket.SOCK_STREAM);
                in = ssocket.getInputStream();
                out = ssocket.getOutputStream();
                in.read(b);
                System.out.println("Text received: \"" + new String(b) + "\"");
                text = "[5] Hello! I'm the server!";
                out.write(text.getBytes());
                System.out.println("Text sent: " + "\"" + text + "\"");
                ssocket.close();
                ssocket.unlink();
                // Testcase 2.2: Test UnixDomainSocketServer with a datagram socket
                System.out.println("Testcase 2.2: Test UnixDomainSocketServer with "
                                + "a datagram socket...");
                ssocket = new UnixDomainSocketServer(socketFile,
                                UnixDomainSocket.SOCK_DGRAM);
                System.out.println("Provoke and catch an "
                                + "UnsupportedOperationException:");
                in = ssocket.getInputStream();
                try {
                        out = ssocket.getOutputStream();
                } catch (UnsupportedOperationException e) {
                        System.out.println("UnsupportedOperationException has been "
                                        + "thrown as expected.");
                }
                in.read(b);
                System.out.println("Text received: \"" + new String(b) + "\"");
                ssocket.close();
                ssocket.unlink();
        }
}
```

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `unix-socket.md`；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
