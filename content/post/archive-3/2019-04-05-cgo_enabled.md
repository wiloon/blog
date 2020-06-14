---
title: golang CGO_ENABLED
author: wiloon
type: post
date: 2019-04-05T14:23:16+00:00
url: /?p=14106
categories:
  - Uncategorized

---
CGO_ENABLED=0的情况下，Go采用纯静态编译；
  
如果CGO_ENABLED=1，但依然要强制静态编译，需传递-linkmode=external给cmd/link。

<blockquote class="wp-embedded-content" data-secret="w5uCEbc4UP">
  <p>
    <a href="https://johng.cn/cgo-enabled-affect-go-static-compile/">CGO_ENABLED环境变量对Go静态编译机制的影响</a>
  </p>
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="https://johng.cn/cgo-enabled-affect-go-static-compile/embed/#?secret=w5uCEbc4UP" data-secret="w5uCEbc4UP" width="600" height="338" title=""CGO_ENABLED环境变量对Go静态编译机制的影响&#8221; &#8212; 碎言碎语" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>