---
title: rancher
author: "-"
date: 2018-06-09T14:32:13+00:00
url: rancher
categories:
  - k8s
tags:
  - reprint
---
## rancher

[https://rancher.com/docs/rancher/v2.6/en/](https://rancher.com/docs/rancher/v2.6/en/)

RKE: Rancher Kubernetes Engine
EKS: Amazon EKS (Elastic Kubernetes Service)
GKE: Google Kubernetes Engine

[https://github.com/rancher/rancher](https://github.com/rancher/rancher)

[https://helm.sh/](https://helm.sh/)

[https://k3s.io/](https://k3s.io/)

## k3s

k3s 将安装 Kubernetes 所需的一切打包进仅有 XXMB 大小的二进制文件中。并且，为了减少运行 k8s 所需的内存，删除了很多不必要的驱动程序，并用附加组件对其进行替换。这样，它只需要极低的资源就可以运行且安装所需的时间也非常短，因此它能够运行在树莓派等设备上面，即 master 和 agent 运行在一起的模式。

裁剪功能
过时的功能和非默认功能
过时的功能和非默认功能 Alpha 功能
过时的功能和非默认功能内置的云提供商插件
过时的功能和非默认功能内置的存储驱动
过时的功能和非默认功能 Docker

项目特点
使用 SQLite 作为默认数据存储替代 etcd，但 etcd 仍然是支持的
内置了 local storage provider、service load balancer 等
所有 k8s 控制组件如 api-server、scheduler 等封装成为一个精简二进制程序，单进程即可运行
删除内置插件，比如 cloudprovider 插件和存储插件等
减少外部依赖，操作系统只需要安装较新的内核以及支持 cgroup 即可

缺点不足
因为在高可用的场景中，其没有办法做到或很难做到。所以如果你要进行大型的集群部署，那么我建议你选择使用 K8s 来安装部署。如果你处于边缘计算等小型部署的场景或仅仅需要部署一些非核心集群进行开发/测试，那么选择 k3s 则是性价比更高的选择。
在单个 master 的 k3s 中，默认使用的是 SQLite 数据库存储数据的，这对于小型数据库十分友好，但是如果遭受重击，那么 SQLite 将成为主要痛点。但是，Kubernetes 控制平面中发生的更改更多是与频繁更新部署、调度 Pod 等有关，因此对于小型开发/测试集群而言，数据库不会造成太大负载。

## quick start

```bash
# server a, linux node, install k3s
curl -sfL https://get.k3s.io | sh -s - server
# save the server ip

# server b, workstation
mkdir -p ~/.kube/
scp root@192.168.50.140:/etc/rancher/k3s/k3s.yaml ~/.kube/config

# edit ~/.kube/config on server b, fill the ip of server a
vi ~/.kube/config

# install helm on server b
# install kubctl on server b
# Install Rancher with Helm

helm repo add rancher-latest https://releases.rancher.com/server-charts/latest

kubectl create namespace cattle-system

kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.7.2/cert-manager.crds.yaml

helm repo add jetstack https://charts.jetstack.io

helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.7.1

helm install rancher rancher-latest/rancher \
  --namespace cattle-system \
  --set hostname=tmp.wiloon.com \
  --set replicas=1 \
  --set bootstrapPassword=password0

# config dns 
# 192.168.50.140 tmp.wiloon.com
# 用浏览器打开地址 https://tmp.wiloon.com/
```

## Installing Rancher on a Single Node Using Docker

[https://rancher.com/docs/rancher/v2.6/en/installation/other-installation-methods/single-node-docker/](https://rancher.com/docs/rancher/v2.6/en/installation/other-installation-methods/single-node-docker/)

ubuntu 22.04 fix [https://github.com/rancher/rancher/issues/36238](https://github.com/rancher/rancher/issues/36238)

```bash
vim /etc/default/grub

GRUB_CMDLINE_LINUX="cgroup_memory=1 cgroup_enable=memory swapaccount=1 systemd.unified_cgroup_hierarchy=0"
sudo update-grub
sudo reboot
```

```bash
sudo docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  --privileged \
  rancher/rancher:latest
```

url: [https://192.168.50.167](https://192.168.50.167)

## create k8s cluster

rancher> cluster management> create

- name: cluster0
- Kubernetes Version: 1.23.7
