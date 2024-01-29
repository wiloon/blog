---
title: vscode, code-server
author: "-"
date: 2019-05-19T01:52:15+00:00
url: code-server
categories:
  - Editor
tags:
  - reprint
---
## vscode, code-server

code server 是 coder 公司基于微软开源的 Visual Studio Code 开发的一款产品。
code server 的目标是为开发者构建一个便捷统一的开发环境，让开发者能从任意设备、任意位置通过浏览器来进行代码的编写。从而免去了常规的 IDE 开发流程中的环境搭建的问题。

code server 有哪些优点？

### 环境统一

code server 解决的第一个问题就是跨设备的环境一致性。因为 code server 始终运行在一个远程的云端环境，因此他的开发环境始终是一致的，不会出现不同平台或者不同设备运行相同的代码而出现各种问题的情况。

我相信有不少程序员遇到过类似的问题。比如，同样的代码在 MacOS 上运行正常，在 Windows 上运行报错；或者在同事 A 的电脑上运行正常，而在同事 B 的电脑上运行报错。

而 code server 解决了这个问题，对于同一个项目的代码开发，不管是谁，运行代码的环境都是 code server 所在的服务器环境，这有效的避免的环境不同带来的问题，让程序员把精力更多地放在代码编写上，而不是去解决各种平台切换带来的问题上。

```bash
podman run -d --name code-server \
-p 8080:8080 \
-v "code-server-config:/root/.config" \
-v "code-server-project:/home/coder/project" \
-v "code-server-ssh:/root/.ssh" \
-v "code-server-data:/data" \
-u "$(id -u):$(id -g)" \
-e "DOCKER_USER=root"  \
--memory=2g \
--cpus=1 \
codercom/code-server:3.12.0 --auth none
```

### nginx 配置

location / {
        proxy_pass [http://wyse5070.wiloon.com:8080](http://wyse5070.wiloon.com:8080);
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header Accept-Encoding gzip;
    }

---

[https://github.com/cdr/code-server](https://github.com/cdr/code-server)
[https://hub.docker.com/r/codercom/code-server](https://hub.docker.com/r/codercom/code-server)  

————————————————
版权声明: 本文为CSDN博主「张驰Terry」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: [https://blog.csdn.net/terrychinaz/article/details/113308263](https://blog.csdn.net/terrychinaz/article/details/113308263)
