---
title: containerd
author: "-"
date: 2025-06-03 14:37:21
url: containerd
categories:
  - Container
tags:
  - reprint
  - remix
---
## containerd

## archlinux install containerd

```bash
# archlinux install containerd
pacman -S containerd runc nerdctl cni-plugins

# containerd config
sudo mkdir /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
#sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
sudo systemctl daemon-reload

sudo systemctl enable --now containerd
sudo nerdctl pull hello-world
sudo nerdctl run --rm hello-world

# 如果需要编译镜像
pacman -S buildkit
sudo systemctl enable --now buildkit\
nerdctl build -t foo:v1.0.0 .
```

## almalinux install containerd

```Bash
# cni plugin
mkdir -p /opt/cni/bin
tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.1.1.tgz
```

## ubuntu install containerd

https://gist.github.com/Faheetah/4baf1e413691bc4e7784fad16d6275a9
https://www.techrepublic.com/article/install-containerd-ubuntu/

```Bash
# install runc
curl -LO https://github.com/opencontainers/runc/releases/download/v1.3.0/runc.amd64
sudo install -m 755 runc.amd64 /usr/local/sbin/runc

# 验证安装
runc --version

# install cni plugin
# 创建插件目录, 容器运行时默认期望插件在这个目录：
sudo mkdir -p /opt/cni/bin

# 设置版本
VERSION="v1.7.1"

# 下载
curl -LO https://github.com/containernetworking/plugins/releases/download/${VERSION}/cni-plugins-linux-amd64-${VERSION}.tgz

# 解压到目标目录
sudo tar -C /opt/cni/bin -xzf cni-plugins-linux-amd64-${VERSION}.tgz

# 查看是否安装成功
ls /opt/cni/bin
# 确认 CNI 配置文件是否存在
ls /etc/cni/net.d/

# 使用 nerdctl 运行容器测试网络
nerdctl run -it --rm busybox

# 在容器中执行
ping -c 2 baidu.com

# install containerd
# apt 仓库里的包版本太旧， 2025-06-03 13:17:05， apt里的 containerd 1.7.27, 官网最新的 2.1.1
sudo tar Cxzvf /usr/local containerd-1.6.2-linux-amd64.tar.gz

# containerd config
sudo mkdir /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
# sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml

# config systemd
sudo curl -L https://raw.githubusercontent.com/containerd/containerd/main/containerd.service -o /etc/systemd/system/containerd.service
sudo systemctl daemon-reload
sudo systemctl enable --now containerd

# download latest version of nerdctl from https://github.com/containerd/nerdctl/releases
sudo tar Cxzvf /usr/bin/ nerdctl-2.0.0-linux-amd64.tar.gz

sudo nerdctl pull hello-world
sudo nerdctl run hello-world

# buildkit
# download latest version of buildkit from https://github.com/moby/buildkit/releases
tar zxvf buildkit-v0.17.1.linux-amd64.tar.gz
sudo mv bin/* /usr/local/bin/
# buildkit service
sudo curl -L https://raw.githubusercontent.com/moby/buildkit/refs/heads/master/examples/systemd/system/buildkit.service -o /etc/systemd/system/buildkit.service
# buildkit socket
sudo curl -L https://raw.githubusercontent.com/moby/buildkit/refs/heads/master/examples/systemd/system/buildkit.socket -o /etc/systemd/system/buildkit.socket

# edit buildkit.service, add --oci-worker=false --containerd-worker=true after buildkitd
# 禁用了本地 runc worker（oci-worker）
# 启用了 containerd worker
sudo vim /etc/systemd/system/buildkit.service

sudo systemctl daemon-reload
sudo systemctl enable --now buildkit

```

## CNI（Container Network Interface）

CNI（Container Network Interface）插件是独立的可执行文件，遵循 CNI 规范。Kubernetes 通过 kubelet 调用这些插件来创建和管理容器的网络接口。CNI 插件的主要职责包括网络接口的创建和删除、IP 地址的分配和回收、以及相关网络资源的配置和清理。

```Bash
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/docker/buildx/releases/latest)
VERSION=${VERSION##*/}

mkdir -p $HOME/.docker/cli-plugins
wget https://github.com/docker/buildx/releases/download/$VERSION/buildx-$VERSION.linux-amd64 -O $HOME/.docker/cli-plugins/docker-buildx
```

https://www.zhangjiee.com/blog/2021/container-runtime.html
https://www.zhangjiee.com/blog/2018/different-from-docker-and-vm.html
https://www.zhangjiee.com/blog/2018/an-overall-view-on-docker-ecosystem-containers-moby-swarm-linuxkit-containerd-kubernete.html
https://www.zhangjiee.com/blog/2021/kubernetes-vs-docker.html

## containerd

```Bash
# check containerd version
containerd --version
```

### containerd config

sudo vim /etc/containerd/config.toml

```Bash
[plugins.'io.containerd.cri.v1.images'.registry]
  config_path = '/etc/containerd/certs.d'
```

/etc/containerd/certs.d/192.168.50.10:5000/hosts.toml

```
server = "http://192.168.50.10:5000"

[host."http://192.168.50.10:5000"]
  capabilities = ["pull", "resolve", "push"]
  skip_verify = true
```

## nerdctl

```Bash
sudo nerdctl --insecure-registry push 127.0.0.1:5000/image_0:1.4
nerdctl network ls
nerdctl run --rm --network=kong-net busybox ping postgresql
```
