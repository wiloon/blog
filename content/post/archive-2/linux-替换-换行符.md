---
title: linux 替换 换行符
author: "-"
date: 2018-10-10T02:14:03+00:00
url: /?p=12776

categories:
  - inbox
tags:
  - reprint
---
## linux 替换 换行符

```bash
  
cat out | python -c "import sys; print sys.stdin.read().replace('.\n','.')"
  
```

---

<http://slash4.net/blog/python/sed-replace-newline-or-python-awk-tr-perl-xargs.html>
<http://slash4.net/blog/python/sed-replace-newline-or-python-awk-tr-perl-xargs.html/embed#?secret=fepFl2MtVM>
