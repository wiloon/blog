---
title: ubuntu install k8s
author: "-"
date: "2006-01-02 15:04:05"
url: ubuntu/k8s
categories:
  - K8S
tags:
  - Reprint
  - Remix
---
## ubuntu install k8s

```Bash
# ufw 查看当前的防火墙状态：inactive 状态是防火墙关闭状态 active 是开启状态。
ufw status
# 如果状态是 active, 使用以下命令禁用默认配置的 iptables 防火墙服务
ufw disable
# 再查一下状态
ufw status

# 查询 selinux 状态
sestatus
#禁用SELINUX, 如果显示 Command 'sestatus' not found, 说明有可能 selinux 并没有被安装
setenforce 0

# 查看是否启用了 swap, 没有输出就是没启用
swapon
# 临时禁用 swap
sudo swapoff -a
# 在文件中永久禁用 /swapfile
sudo vim /etc/fstab

# 配置多台主机 hosts
vim /etc/hosts
192.168.50.80 k8s80
192.168.50.81 k8s81
192.168.50.82 k8s82

# 重启
reboot
```

## 安装 Docker

```Bash
# 安装 Docker
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
sudo systemctl status docker

# 此文件不一定存在， 不存在创建
sudo vi /etc/docker/daemon.json

{
  "registry-mirrors": [
    "https://dockerhub.azk8s.cn",
    "https://reg-mirror.qiniu.com",
    "https://quay-mirror.qiniu.com"
  ],
  # 本文版本默认systemd，K8S最好还是配上
  "exec-opts": [ "native.cgroupdriver=systemd" ] #隔离工具systemd, k8s需要，没有k8s需求忽略此行, 可能会出现docker设置cgroup名字与kubelete的不一致
}

systemctl daemon-reload
systemctl restart docker

#查看修改后的 docker cgroup 状态
docker info | grep Cgroup

可以查看镜像是否配置成功

docker info | grep azk8s
docker info | grep qiniu

```
## 开始 K8S

1. (可选) 容器运行时配置： 转发 IPv4 并让 iptables 看到桥接流量
   中文官网参考： https://kubernetes.io/zh-cn/docs/setup/production-environment/container-runtimes/

```Bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

# 手动加载模块
sudo modprobe overlay
sudo modprobe br_netfilter

# 设置所需的 sysctl 参数，参数在重新启动后保持不变
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# 应用 sysctl 参数而不重新启动
sudo sysctl --system
```

通过运行以下指令确认 br_netfilter 和 overlay 模块被加载：

```Bash
lsmod | grep br_netfilter
lsmod | grep overlay
```

## containerd 配置

```Bash
# 复制默认的配置 > config.toml 中
containerd config default > /etc/containerd/config.toml
# 编辑配置文件
vim /etc/containerd/config.toml

SystemdCgroup = false 改为 SystemdCgroup = true
# sandbox_image = "k8s.gcr.io/pause:3.6"
改为(3.6为版本，当前是多少，则保留多少，如果是3.8，下面则是3.8)：
sandbox_image = "registry.aliyuncs.com/google_containers/pause:3.9"

# 不配置的话默认从官方源下载
# 添加 endpoint 加速器, containerd配置下载镜像
# 找到这行配置 [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
# 修改后( ttxrrkr1 为私有镜像, 我的ITian )
# 参考地址 https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors
[plugins."io.containerd.grpc.v1.cri".registry.mirrors]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
    endpoint = ["https://ttxrrkr1.mirror.aliyuncs.com"]
```

systemctl daemon-reload && systemctl restart containerd

## 安装k8s组件

```Bash
# 配置阿里云镜像站点，（阿里镜像下载）也可以用官方方式下载
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add -
cat >/etc/apt/sources.list.d/kubernetes.list <<EOF
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF

apt-get update

# 查看版本
apt-cache madison kubeadm|head
apt install -y  kubeadm=1.28.2-00 kubelet=1.28.2-00 kubectl=1.22.2-00
```

## 备份虚拟机磁盘

## 安装 master 节点

```Bash
# 生成默认配置，便于修改
kubeadm config print init-defaults > kubeadm.yaml
```

### 文件修改对应如下：

- token: abcdef.0123456789abcdef # 可以自定义，正则([a-z0-9]{6}).([a-z0-9]{16})
- advertiseAddress: 192.168.50.80 # kubernetes主节点IP
- name: k8s80 # 节点的虚拟机的 hostname
- imageRepository: registry.aliyuncs.com/google_containers # 镜像仓库
- kubernetesVersion: 1.28.0 # 指定版本
- podSubnet: 10.1.0.0/16  # 增加指定pod的网段
- # 指定 cgroup

```Bash
apiVersion: kubeadm.k8s.io/v1beta3
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: abcdef.0123456789abcdef
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 192.168.50.80
  bindPort: 6443
nodeRegistration:
  criSocket: unix:///var/run/containerd/containerd.sock
  imagePullPolicy: IfNotPresent
  name: k8s80
  taints: null
---
apiServer:
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta3
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controllerManager: {}
dns: {}
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: registry.aliyuncs.com/google_containers
kind: ClusterConfiguration
kubernetesVersion: 1.28.0
networking:
  dnsDomain: cluster.local
  serviceSubnet: 10.96.0.0/12
  podSubnet: 10.1.0.0/16
scheduler: {}
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
```

```Bash
kubeadm init --config ./kubeadm.yaml
```

output

```Bash
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.50.80:6443 --token abcdef.0123456789abcdef \
	--discovery-token-ca-cert-hash sha256:7caea0c080754eb234dbc6212ba2c808330b25b81079c85f494de997acd5f736
```


```Bash
export KUBECONFIG=/etc/kubernetes/admin.conf
```

## 查看命令

```Bash
kubectl get nodes
#查看一下集群状态，确认个组件都处于healthy状态
kubectl get cs
kubectl get pod -n kube-system
```

## master 配置安装网络组件 （calico 或者 flannel）

```Bash
# 使用flannel 当前最新
curl https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml -o kube-flannel.yml

vim /run/flannel/subnet.env
FLANNEL_NETWORK=10.244.0.0/16
FLANNEL_SUBNET=10.244.0.1/24
FLANNEL_MTU=1450
FLANNEL_IPMASQ=true

kubectl apply -f kube-flannel.yml
```

## 检查网络配置

```Bash
kubectl get pod -n kube-system
```

## todo

Warning: apt-key is deprecated. Manage keyring files in trusted.gpg.d instead (see apt-key(8)).

W: https://download.docker.com/linux/ubuntu/dists/jammy/InRelease: Key is stored in legacy trusted.gpg keyring (/etc/apt/trusted.gpg), see the DEPRECATION section in apt-key(8) for details.



作者：ITianl
链接：https://www.jianshu.com/p/4d696c8a6f41
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
