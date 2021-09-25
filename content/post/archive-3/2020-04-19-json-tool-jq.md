---
title: json tool, jq
author: "-"
type: post
date: 2020-04-19T13:17:58+00:00
url: /?p=16004
categories:
  - Uncategorized

---
### json格式化

```bash
echo '{"kind": "Service", "apiVersion": "v1", "status": {"loadBalancer": true}}'|jq .
{
  "kind": "Service",
  "apiVersion": "v1",
  "status": {
    "loadBalancer": true
  }
}

作者: 网易云
链接: https://www.zhihu.com/question/20057446/answer/489588448
来源: 知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```