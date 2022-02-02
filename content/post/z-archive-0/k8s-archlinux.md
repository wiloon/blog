---
title: archlinux, k8s
author: "-"
date: 2021-09-26 00:09:45
url: k8s
categories:
  - k8s

---
## archlinux, k8s
## Containerd, CRI-O
Containerd 项目是从早期的Docker源码中提炼出来的，它使用CRI插件来向kubelet提供CRI接口服务。

CRI插件是一个独立的项目，在Containerd编译时，如果go build命令没有显示设置参数-tags=no_cri，那么CRI插件将自动编译集成到Containerd的二进制文件中，然后在配置文件/etc/containerd/config.toml中声明启用CRI插件，就可以在Containerd中启动CRI shim服务了。

Containerd能支持多运行时，目前它内置了runc运行时，其他运行时如果要接入Containerd，则需要实现Containerd shim v2 gRPC接口，这样Containerd就可以通过shim v2调用其他运行时。他们的调用关系如下：Containerd --> shim v2 --> runtimes
## CRI-O
CRI-O完整实现CRI接口功能，并且严格兼容OCI标准，CRI-O比Containerd更专注，它只服务于Kubernetes（而Containerd除支持Kubernetes CRI，还可用于Docker Swarm），从官网上我们可以了解到CRI-O项目的功能边界：
支持多种image格式
支持多种image下载方式
容器镜像管理
容器生命周期管理
提供CRI要求的监控、日志功能
提供CRI要求的资源隔离功能

CRI-O通过命令行调用默认运行时runC，所以runC二进制文件必须部署在目录/usr/bin/runc。CRI-O和Containerd调用runtime的方式不同，前者是通过Linux命令调用，后者是通过gRPC服务调用，所以只要符合OCI规范的runtime，都能直接接入CRI-O提供运行时服务，而除runC外的其他运行时要接入Containerd，只能走shim v2接口，因此我们看到像kata-runtime这样的运行时项目就是通过shim v2接口来适配Containerd的。
>http://dockone.io/article/8891

```bash
# check crio state and version 
sudo crictl --runtime-endpoint unix:///var/run/crio/crio.sock version
```
## kubeadm
kubeadm 是一个工具包，可帮助您以简单，合理安全和可扩展的方式引导最佳实践Kubernetes群集。它还支持为您管理Bootstrap Tokens并升级/降级群集。

kubeadm的目标是建立一个通过Kubernetes一致性测试Kubernetes Conformance tests的最小可行集群 ，但不会安装其他功能插件。

它在设计上并未为您安装网络解决方案，需要用户自行安装第三方符合CNI的网络解决方案（如flanal，calico，canal等）。

kubeadm可以在多种设备上运行，可以是Linux笔记本电脑，虚拟机，物理/云服务器或Raspberry Pi。这使得kubeadm非常适合与不同种类的配置系统（例如Terraform，Ansible等）集成。

kubeadm是一种简单的方式让新用户开始尝试Kubernetes，也可能是第一次让现有用户轻松测试他们的应用程序并缝合到一起的方式，也可以作为其他生态系统中的构建块，或者具有更大范围的安装工具。

可以在支持安装deb或rpm软件包的操作系统上非常轻松地安装kubeadm。SIG集群生命周期SIG Cluster Lifecycle kubeadm的SIG相关维护者提供了预编译的这些软件包，也可以在其他操作系统上使用。
>https://github.com/kubernetes/kubeadm

##  kubelet 
Kubelet 是 kubernetes 工作节点上的一个代理组件，运行在每个节点上。


Kubelet是工作节点上的主要服务，定期从kube-apiserver组件接收新的或修改的Pod规范，并确保Pod及其容器在期望规范下运行。同时该组件作为工作节点的监控组件，向kube-apiserver汇报主机的运行状况。

架构
Kubelet 的组件架构图，如下所示，Kubelet 由许多内部组件构成

Kubelet API，包括 10250 认证API、4194 端口的 cAdvisor API、10255 端口的只读 API 以及 10248 端口的健康检查 API
syncLoop：从 API 或者 manifest 目录接收 Pod 更新，发送到 podWorkers 处理，大量使用 channel 处理来处理异步请求
辅助的 manager，如 Volume Manager 等，处理 syncLoop 以外的其他工作
CRI：遵循CRI规范，通过封装的两个服务(Remote Runtime Service 和 Remote Image Service)以CRI gRPC Client角色与高级容器运行时进行交互

### kubectl
可以使用 Kubectl 命令行工具管理 Kubernetes 集群
kubectl 是 Kubernetes 的命令行工具（CLI），是 Kubernetes 用户和管理员必备的管理工具。

```bash
pacman -S kubeadm kubelet kubectl cri-o podman jq

systemctl enable kubelet
systemctl enable  crio

# 安装完以上的包 ip forward nf-call会自动设置好。
sysctl -a |grep vm.swappiness
sysctl -a |grep ip_forward
sysctl -a |grep bridge-nf-call

reboot
systemctl status kubelet
systemctl status crio


kubeadm config print init-defaults --kubeconfig ClusterConfiguration > kubeadm.yml
kubeadm config images list --config kubeadm.yml
kubeadm config images pull --config kubeadm.yml
kubeadm init --config=kubeadm.yml --upload-certs



```

```yaml
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
  advertiseAddress: 192.168.50.118 
  bindPort: 6443
nodeRegistration:
  criSocket: 'unix:///run/crio/crio.sock' 
  imagePullPolicy: IfNotPresent
  name: k8s0
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
kubernetesVersion: 1.23.0
networking:
  dnsDomain: cluster.local
  serviceSubnet: 10.96.0.0/12
scheduler: {}

```

### kubelet config
    /var/lib/kubelet/config.yaml
>https://www.lixueduan.com/post/kubernetes/01-install/


>https://wiki.archlinux.org/title/Kubernetes
>https://kubernetes.io/zh/docs/home/
>https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/

>https://www.qikqiak.com/post/containerd-usage/
>https://landscape.cncf.io/card-mode?category=container-runtime&grouping=category
