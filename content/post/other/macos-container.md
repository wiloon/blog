---
title: macos container
author: "-"
date: 2013-03-04T09:25:20+00:00
url: macos-container
categories:
  - container
tags:
  - reprint
  - remix
---
## macos container

在 macos 应用商店安装 xcode

```bash
brew install container
container system start
container run --rm -it docker.io/library/hello-world:latest
```

### 从源码编译

```bash
git clone https://github.com/apple/container.git
cd container
swift build
sudo cp .build/debug/container /usr/local/bin/container
```
