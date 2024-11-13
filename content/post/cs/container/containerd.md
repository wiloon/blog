---
title: containerd
author: "-"
date: 2020-03-02T02:45:30+00:00
url: containerd
categories:
  - Container
tags:
  - reprint
  - remix
---
## containerd

https://gist.github.com/Faheetah/4baf1e413691bc4e7784fad16d6275a9
https://www.techrepublic.com/article/install-containerd-ubuntu/

```Bash
sudo apt-get update
sudo apt-get install containerd
# download latest version of nerdctl from https://github.com/containerd/nerdctl/releases
tar zxvf nerdctl-2.0.0-linux-amd64.tar.gz
sudo mv nerdctl /usr/bin/nerdctl
# download latest version of CNI plugins from https://github.com/containernetworking/plugins/releases/
sudo mkdir -p /opt/cni/bin/
sudo tar -zxf cni-plugins-linux-amd64-v1.3.0.tgz -C /opt/cni/bin/

# buildkit
# download latest version of buildkit from https://github.com/moby/buildkit/releases
tar zxvf buildkit-v0.17.1.linux-amd64.tar.gz
sudo mv bin/* /usr/local/bin/
sudo curl -L https://raw.githubusercontent.com/moby/buildkit/refs/heads/master/examples/systemd/system/buildkit.service -o /etc/systemd/system/buildkit.service
# edit buildkit.service, add --oci-worker=false --containerd-worker=true after buildkitd
sudo vim /etc/systemd/system/buildkit.service
sudo curl -L https://raw.githubusercontent.com/moby/buildkit/refs/heads/master/examples/systemd/system/buildkit.socket -o /etc/systemd/system/buildkit.socket
sudo systemctl daemon-reload
sudo systemctl enable --now buildkit

# containerd config
sudo mkdir /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
sudo curl -L https://raw.githubusercontent.com/containerd/containerd/main/containerd.service -o /etc/systemd/system/containerd.service
sudo systemctl daemon-reload
sudo systemctl enable --now containerd
sudo nerdctl pull hello-world
sudo nerdctl run hello-world
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