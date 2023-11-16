---
title: KubeKey
author: "-"
date: 2012-11-14T02:38:33+00:00
url: KubeKey
categories:
  - K8S
tags:
  - reprint
---
## KubeKey

```bash
sudo apt install socat conntrack ebtables ipset ipvsadm

git clone https://github.com/kubesphere/kubekey.git
cd kubekey
./build.sh -p

cd output
./kk create cluster
```

[https://kubesphere.io/zh/docs/installing-on-linux/introduction/intro/](https://kubesphere.io/zh/docs/installing-on-linux/introduction/intro/)
