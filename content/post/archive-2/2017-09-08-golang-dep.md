---
title: 'golang  dep'
author: "-"
type: post
date: 2017-09-08T02:03:27+00:00
url: /?p=11132
categories:
  - Uncategorized

---
# 'golang  dep'
```bash
  
dep status -dot | dot -T png | display

go get -u github.com/golang/dep/cmd/dep
  
dep init
  
dep status
  
dep ensure
  
dep help ensure

init Initialize a new project with manifest and lock files
  
status Report the status of the project's dependencies
  
ensure Ensure a dependency is safely vendored in the project
  
prune Prune the vendor tree of unused packages

```

http://tonybai.com/2017/06/08/first-glimpse-of-dep/
  
https://github.com/golang/dep
  
http://tonybai.com/2017/06/08/first-glimpse-of-dep/