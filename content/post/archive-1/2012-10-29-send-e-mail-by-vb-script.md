---
title: golang 读系统环境变量
author: lcf
type: post
date: 2012-10-29T03:18:33+00:00
url: /?p=4561
categories:
  - Uncategorized

---
# golang 读系统环境变量
http://studygolang.com/articles/3387

```java
  
package system

import "os"

func GetSystemEnv(key string) (value string) {
      
return os.Getenv(key)
  
}
  
```