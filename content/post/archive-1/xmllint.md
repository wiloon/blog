---
title: xmllint, xml 格式化
author: "-"
date: 2013-03-05T10:00:24+00:00
url: xmllint
categories:
  - inbox
tags:
  - reprint
---
## xmllint, xml 格式化

```bash
sudo apt install libxml2-utils  
```

```bash
pacman -S libxml2
xmllint --format settings.xml > settings.xml.new

## 使用 - (“连字符/减号”)为 xmllint 的 file 参数从标准输入流而不是文件或 URL 获取其 XML 输入。
curl --silent "https://somesite.xml" | xmllint -
```
