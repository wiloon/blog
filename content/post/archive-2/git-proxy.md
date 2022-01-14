---
title: git proxy
author: "-"
date: 2017-12-06T04:56:26+00:00
url: git-proxy
categories:
  - git

---
### git proxy
```bash
# http proxy
git config http.proxy 'http://192.168.50.xx:80'
git config --global http.proxy http://proxy.mycompany:80
# socks5 proxy
git config http.proxy 'socks5://192.168.50.13:1080'
git config --global http.proxy 'socks5://192.168.50.13:1080'
```

```bash
git config --global --unset http.proxy

git config --global --unset https.proxy

npm config delete proxy
```

https://gist.github.com/laispace/666dd7b27e9116faece6