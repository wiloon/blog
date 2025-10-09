---
title: archlinux k8s
author: "-"
date: 2012-12-23T10:37:40+00:00
url: archlinux/k8s
categories:
  - k8s
tags:
  - reprint
  - remix
---
## archlinux k8s

disable swap

```bash
# check swap usage, if no output, swap is disabled
swapon --show

# check swap status
systemctl list-units --type=swap
# disable swap
sudo swapoff -a
# disable zram swap
sudo systemctl mask dev-zram0.swap
```

```bash
sudo pacman -Syu
reboot
sudo pacman -S containerd kubeadm kubelet kubectl curl jq open-iscsi
reboot

# 如果提示 : iptables-nft-1:1.8.11-2 and iptables-1:1.8.11-2 are in conflict. Remove iptables? [y/N]
# 删除 iptables, Kubernetes，推荐使用 iptables-nft，因为 Kubernetes 自 v1.13 起支持 iptables 的 nftables 后端（iptables-nft），而且 nftables 是 Linux 内核中更现代的防火墙实现，逐渐取代传统 iptables。此外，Arch Linux 的默认配置倾向于 nftables。

# 查看 containerd 版本
ctr version

lsmod|grep br_netfilter
lsmod|grep overlay

# 在安装 kubelet 的时候 br_netfilter 已经设置 好了, k8s.conf 里不需要再加 br_netfilter
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
EOF

sudo modprobe overlay

# 安装 kubeadm 的时候这三个变量会自动设置, 输出应该都是 1
sysctl net.bridge.bridge-nf-call-iptables
sysctl net.bridge.bridge-nf-call-ip6tables
sysctl net.ipv4.ip_forward

# containerd config
sudo mkdir /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
vim /etc/containerd/config.toml
# 打开文件,找到 `[plugins.'io.containerd.cri.v1.runtime'.containerd.runtimes.runc.options]`
# 在下面加 一行 SystemdCgroup = true
# 配置 containerd 使用 systemd 作为 cgroup 驱动

# 检查  containerd 的 状态
sudo systemctl status containerd
# 重启 containerd
sudo systemctl restart containerd
sudo systemctl enable --now containerd

sudo systemctl status kubelet
systemctl enable kubelet.service
systemctl enable --now iscsid

```

## kube-vip

kube-vip 相关的命令要在每个 control plane 节点上执行

```bash
# VIP（找一个跟 control plane 在同一子网，未使用的IP）
export VIP=192.168.50.100
# 要绑定 VIP 的网卡名称
export INTERFACE=ens18
# 获取 kube-vip 最新版本
KVVERSION=$(curl -sL https://api.github.com/repos/kube-vip/kube-vip/releases | jq -r ".[0].name")
alias kube-vip="sudo ctr image pull ghcr.io/kube-vip/kube-vip:$KVVERSION && sudo ctr run --rm --net-host ghcr.io/kube-vip/kube-vip:$KVVERSION vip /kube-vip"

sudo mkdir -p /etc/kubernetes/manifests
kube-vip manifest pod \
  --interface $INTERFACE \
  --address $VIP \
  --controlplane \
  --services \
  --arp \
  --leaderElection \
  | tee /etc/kubernetes/manifests/kube-vip.yaml
```

vim /etc/kubernetes/manifests/kube-vip.yaml

在 spec.volumes 下添加 super-admin.conf 挂载卷（如果 volumes 为空，从 spec: 后添加）：

```bash
spec:
  volumes:
  - hostPath:
      path: /etc/kubernetes/super-admin.conf
      type: File
    name: kubeconfig
  # ... 其他 volumes（如 ca 等，如果有）

```

super-admin.conf, should be copy to other control plane nodes

在 spec.containers[0].volumeMounts 下添加挂载（覆盖默认 admin.conf）：

```bash
spec:
  containers:
  - name: kube-vip
    # ... 其他配置
    volumeMounts:
    - mountPath: /etc/kubernetes/admin.conf
      name: kubeconfig
      readOnly: true
    # ... 其他 volumeMounts
```

```bash
# dryrun
sudo kubeadm init --dry-run --v=10 --pod-network-cidr=10.244.0.0/16
# 测试 Kubernetes 仓库
curl -I https://registry.k8s.io/v2/
# 拉取镜像
sudo kubeadm config images pull

# 初始化 Kubernetes 集群# 一个集群里执行一次就可以了, 其它的 control plane, worker node 只需要执行 kubeadm join
sudo kubeadm init --control-plane-endpoint "$VIP:6443" --upload-certs --pod-network-cidr=10.244.0.0/16 --kubernetes-version=1.34.1 --v=5

sudo journalctl -u kubelet -f

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

kubectl get nodes

# 验证 kube-vip
kubectl get pods -n kube-system | grep kube-vip
#应 Running。

# 安装其它 k8s control plane 节点, 

# install calico
curl -O https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/tigera-operator.yaml
kubectl create -f tigera-operator.yaml
curl -O https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/custom-resources.yaml
kubectl create -f custom-resources.yaml


kubectl get pods -n kube-system
```

## kubeadm reset

```bash
# kubeadm reset 会清理 containerd 里面运行的容器
# reset 之后一般不需要重启虚拟机
sudo kubeadm reset -f
sudo rm -rf /etc/kubernetes /var/lib/etcd /var/lib/kubelet
sudo systemctl restart containerd kubelet

sudo kubeadm reset
sudo systemctl status containerd
sudo systemctl status kubelet

# ---------
sudo systemctl stop containerd
sudo systemctl stop kubelet.service
# kubeadm init 理论 上会自动 启动 kubelet
sudo systemctl enable --now kubelet.service
sudo systemctl start kubelet.service
sudo systemctl status kubelet.service

sudo systemctl restart containerd
sudo systemctl start kubelet.service
systemctl enable kubelet.service

sudo systemctl status containerd
sudo systemctl status kubelet.service

# 如果 之前执行过 init, 先用 kubeadm reset 清理
sudo kubeadm reset
sudo crictl ps -a
sudo systemctl stop kubelet
sudo systemctl stop containerd

```

## 在 control plane 上生成加入命令

```bash
kubeadm token create --print-join-command
```

Kubernetes 和 cgroup 的关系

cgroup（Control Groups） 是 Linux 内核提供的功能，用于限制和管理进程的资源（如 CPU、内存、IO 等）。Kubernetes 使用 cgroup 来为 Pod 和容器分配资源，确保隔离和资源限制。

containerd 的默认行为

containerd 默认使用 cgroupfs 作为其 cgroup 驱动，而不是 systemd。
cgroupfs 是直接操作 Linux 内核的 cgroup 文件系统，而 systemd 通过 systemd 单元来管理 cgroup 层级。Kubernetes 更倾向于使用 systemd，因为它与现代 Linux 发行版的初始化系统集成更好，且提供更细粒度的控制。
如果 containerd 使用 cgroupfs 而 Kubernetes 使用 systemd（默认情况），就会出现 cgroup driver mismatch 错误，导致 kubelet（Kubernetes 节点代理）无法与 containerd 正确通信。

其它命令

```bash
kubeadm config images pull
kubeadm version
kubectl version --client
telnet 192.168.50.67 6443
```

## 上传证书

```bash
kubectl create secret tls wiloon-tls \
  --cert=wiloon.crt \
  --key=wiloon.key \
  --namespace=default

# 验证
kubectl get secret wiloon-tls -o yaml
```
