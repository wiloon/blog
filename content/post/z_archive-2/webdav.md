---
title: WebDAV
author: "-"
date: 2019-01-22T15:14:01+00:00
url: /?p=13452
categories:
  - Inbox
tags:
  - reprint
---
## WebDAV
Web 分布式创作和版本管理 (WebDAV) 是 HTTP 协议的扩展,支持将 Web 服务器显示为标准的网络驱动器。WebDAV 客户端默认安装在大部分常见的操作系统上,可用于直接装载和访问 QNAP NAS 上的共享文件夹。WebDAV 访问具有以下好处: 

256 位 AES SSL 加密
  
绕过防火墙和代理
  
速度比使用 VPN 的 Microsoft 网络连接 (SMB/CIFS) 更快

https://www.qnap.com/zh-cn/how-to/tutorial/article/%E5%A6%82%E4%BD%95%E9%80%8F%E8%BF%87-webdav-%E8%BF%9C%E7%A8%8B%E8%AE%BF%E9%97%AE%E6%82%A8%E7%9A%84-nas/

windows挂栽webdav

```bash
# run in cmd
net use * https://xxx.wiloon.com/remote.php/webdav/
```

Error 0x800700DF: The file size exceeds the limit allowed and cannot be saved.
  
Regedit
  
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WebClient\Parameters
  
image
  
FileSizeLimitInBytes
  
Set to the following Decimal: 4294967295
  
Click OK
  
Restart the WebClient service
  
Refresh the Windows Explorer WebDAV window
  
Authenticate again
  
Voila!


  
    WebDAV Download Error: 0x800700DF File Size Exceeds Limit Allowed
  


