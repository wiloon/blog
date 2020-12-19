---
title: golang CGO_ENABLED
author: w1100n
type: post
date: 2019-04-05T14:23:16+00:00
url: /?p=14106
categories:
  - Uncategorized

---
CGO_ENABLED=0的情况下，Go采用纯静态编译；
  
如果CGO_ENABLED=1，但依然要强制静态编译，需传递-linkmode=external给cmd/link。

<blockquote class="wp-embedded-content" data-secret="w5uCEbc4UP">
  
    <a href="https://johng.cn/cgo-enabled-affect-go-static-compile/">CGO_ENABLED环境变量对Go静态编译机制的影响</a>
  
</blockquote>

https://johng.cn/cgo-enabled-affect-go-static-compile/embed/#?secret=w5uCEbc4UP