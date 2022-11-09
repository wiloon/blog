---
title: k8s
author: "-"
date: 2021-09-26 00:09:45
url: k8s
categories:
  - K8S
tags:
  - reprint
  - k8s
  - remix
---
## k8s

- commands
- kubekey <https://github.com/kubesphere/kubekey>
- Rancher <https://rancher.com/>
- archlinux install k8s
- ubuntu install k8s

## commands

```bash
kubectl get ep -n namespace0
kubectl set image deployment/kong kong=kong1.0 -n namespace0
# source file: /tmp/foo, dest file: /tmp/bar
kubectl cp namespace0/pod0:/tmp/foo /tmp/bar

# scale, 扩缩容
kubectl scale --replicas=0 deployment/deployment0
kubectl get pv,pvc
kubectl get pod -A -o wide
kubectl get pods --all-namespaces
kubectl get svc
kubectl describe svc svc0
kubectl logs <pod_name>

## 卸载服务, delete service and deployment
kubectl delete -f deployment.yaml

kubectl get configmap
# 查看 k8s 版本
kubectl version --output=yaml

systemctl status kubelet
# 重置
kubeadm reset
# 检查k8s dns svc 启动是否正常
kubectl get svc -n kube-system
# 节点的状态
kubectl get nodes -o wide
kubectl get pod
kubectl exec -it <id> bash
# 所有 Pod 信息
kubectl get pods --all-namespaces -o wide

kubectl get pods -A
kubectl get pods -n kube-system  -o wide
kubectl describe pods -n namespace0 pod0

# 重启 pod
kubectl replace --force -f  kube-flannel.yml
kubectl delete node k8s-test-2.novalocal

crictl ps

kubeadm token list
#删除节点
kubectl delete pod kube-flannel-ds-trxtz  -n kube-system

kubectl logs -f --since 5m istiod-9cbc77d98-kk98q -n istio-system

## 强制删除
kubectl delete pod pod0 -n xxx --force --grace-period=0

kubectl get svc nginx-app
kubectl describe svc nginx-app

# check status
kubectl get pods --all-namespaces
kubectl get pods --all-namespaces -o wide
kubectl describe pod -n <NAMESPACE> <NAME>
kubectl logs --namespace <NAMESPACE> <NAME>
kubectl cluster-info
kubectl get nodes
kubectl get po -n default
kubectl delete deployment deployment0
kubectl delete svc svc0

kubectl create namespace influxdb
```

## Containerd, CRI-O

Containerd 项目是从早期的Docker源码中提炼出来的，它使用CRI插件来向kubelet提供CRI接口服务。

CRI插件是一个独立的项目，在Containerd编译时，如果go build命令没有显示设置参数-tags=no_cri，那么CRI插件将自动编译集成到Containerd的二进制文件中，然后在配置文件/etc/containerd/config.toml中声明启用CRI插件，就可以在Containerd中启动CRI shim服务了。

Containerd能支持多运行时，目前它内置了runc运行时，其他运行时如果要接入Containerd，则需要实现Containerd shim v2 gRPC接口，这样Containerd就可以通过shim v2调用其他运行时。他们的调用关系如下：Containerd --> shim v2 --> runtimes

## CRI-O

CRI-O完整实现CRI接口功能，并且严格兼容OCI标准，CRI-O比Containerd更专注，它只服务于Kubernetes (而Containerd除支持Kubernetes CRI，还可用于Docker Swarm），从官网上我们可以了解到CRI-O项目的功能边界：
支持多种image格式
支持多种image下载方式
容器镜像管理
容器生命周期管理
提供CRI要求的监控、日志功能
提供CRI要求的资源隔离功能

CRI-O通过命令行调用默认运行时runC，所以runC二进制文件必须部署在目录/usr/bin/runc。CRI-O和Containerd调用runtime的方式不同，前者是通过Linux命令调用，后者是通过gRPC服务调用，所以只要符合OCI规范的runtime，都能直接接入CRI-O提供运行时服务，而除runC外的其他运行时要接入Containerd，只能走shim v2接口，因此我们看到像kata-runtime这样的运行时项目就是通过shim v2接口来适配Containerd的。

<http://dockone.io/article/8891>

```bash
# check crio state and version 
sudo crictl --runtime-endpoint unix:///var/run/crio/crio.sock version
```

## kubeadm

kubeadm 是一个工具包，可帮助您以简单，合理安全和可扩展的方式引导最佳实践Kubernetes群集。它还支持为您管理Bootstrap Tokens并升级/降级群集。

kubeadm的目标是建立一个通过Kubernetes一致性测试Kubernetes Conformance tests的最小可行集群 ，但不会安装其他功能插件。

它在设计上并未为您安装网络解决方案，需要用户自行安装第三方符合CNI的网络解决方案 (如flanal，calico，canal等）。

kubeadm可以在多种设备上运行，可以是Linux笔记本电脑，虚拟机，物理/云服务器或Raspberry Pi。这使得kubeadm非常适合与不同种类的配置系统 (例如Terraform，Ansible等）集成。

kubeadm是一种简单的方式让新用户开始尝试Kubernetes，也可能是第一次让现有用户轻松测试他们的应用程序并缝合到一起的方式，也可以作为其他生态系统中的构建块，或者具有更大范围的安装工具。

可以在支持安装deb或rpm软件包的操作系统上非常轻松地安装kubeadm。SIG集群生命周期SIG Cluster Lifecycle kubeadm的SIG相关维护者提供了预编译的这些软件包，也可以在其他操作系统上使用。

<https://github.com/kubernetes/kubeadm>

## kubelet

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
kubectl 是 Kubernetes 的命令行工具 (CLI），是 Kubernetes 用户和管理员必备的管理工具。

```bash
# install kubctl
# archlinux
pacman -S kubectl

# curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
```

### archlinux 安装  k8s

```bash
pacman -Syu
reboot
# 安装最新版本
pacman -S kubeadm kubelet kubectl cri-o
systemctl enable kubelet && systemctl enable crio
reboot

# 安装完以上的包 ip forward, nf-call会自动设置好。
sysctl -a |grep vm.swappiness && sysctl -a |grep ip_forward && sysctl -a |grep bridge-nf-call

# 把虚拟机的网关设置成有梯子的网关，kubelet 需要梯子

# 配置内网dns
192.168.50.110 k8s0
```

### 配置 /etc/containers/registries.conf

```bash
unqualified-search-registries = ["docker.io"]
[[registry]]
prefix = "docker.io"
# id 替换成你自己的id
location = "<id>.mirror.aliyuncs.com"
```

```bash
# 导出默认配置
kubeadm config print init-defaults --component-configs KubeletConfiguration > kubeadm.yaml
```

### 修改后的 kubeadm.yaml

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
# IP
  advertiseAddress: 192.168.50.110
  bindPort: 6443
nodeRegistration:
# 使用 cri-o
  criSocket: unix:///run/crio/crio.sock
  imagePullPolicy: IfNotPresent
# name
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
# 阿里云镜像仓库
imageRepository: registry.aliyuncs.com/google_containers
kind: ClusterConfiguration
# k8s 版本
kubernetesVersion: 1.23.3
networking:
  dnsDomain: cluster.local
  serviceSubnet: 10.96.0.0/12
# pod subnet
  podSubnet: 10.244.0.0/16
scheduler: {}
---
apiVersion: kubelet.config.k8s.io/v1beta1
authentication:
  anonymous:
    enabled: false
  webhook:
    cacheTTL: 0s
    enabled: true
  x509:
    clientCAFile: /etc/kubernetes/pki/ca.crt
authorization:
  mode: Webhook
  webhook:
    cacheAuthorizedTTL: 0s
    cacheUnauthorizedTTL: 0s
cgroupDriver: systemd
clusterDNS:
- 10.96.0.10
clusterDomain: cluster.local
cpuManagerReconcilePeriod: 0s
evictionPressureTransitionPeriod: 0s
fileCheckFrequency: 0s
healthzBindAddress: 127.0.0.1
healthzPort: 10248
httpCheckFrequency: 0s
imageMinimumGCAge: 0s
kind: KubeletConfiguration
logging:
  flushFrequency: 0
  options:
    json:
      infoBufferSize: "0"
  verbosity: 0
memorySwap: {}
nodeStatusReportFrequency: 0s
nodeStatusUpdateFrequency: 0s
resolvConf: /run/systemd/resolve/resolv.conf
rotateCertificates: true
runtimeRequestTimeout: 0s
shutdownGracePeriod: 0s
shutdownGracePeriodCriticalPods: 0s
staticPodPath: /etc/kubernetes/manifests
streamingConnectionIdleTimeout: 0s
syncFrequency: 0s
volumeStatsAggPeriod: 0s

```

```bash
kubeadm config images list --config kubeadm.yaml
kubeadm config images pull --config kubeadm.yaml

# init, 初始化Master节点
kubeadm init --config kubeadm.yaml --upload-certs
kubeadm init --config kubeadm.yaml --upload-certs --ignore-preflight-errors=KubeletVersion

# kubeadm 会生成kubelet配置并重启kubelet
/var/lib/kubelet/kubeadm-flags.env
# kubelet 配置
/var/lib/kubelet/config.yaml

```

### kubeadm 执行成功的回显

```bash
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

kubeadm join 192.168.50.110:6443 --token abcdef.0123456789abcdef \
        --discovery-token-ca-cert-hash sha256:6fee60dc1867c9e88a3c404e949833ab1956db85e19ee5fdfbf4aaa89712e6b6
```

### export

echo 'export KUBECONFIG=/etc/kubernetes/admin.conf' > ~/.bash_profile

### install worker node

```bash
pacman -S cri-o kubeadm kubelet kubectl
systemctl enable kubelet && systemctl enable crio
reboot
# 配置内网dns
192.168.50.111 k8s1

# 配置 /etc/containers/registries.conf

# 在 master 节点上执行，取token
kubeadm token list 
# 如果 token 过期，可以使用 kubeadm token create 命令创建新的 token


# 在worker节点 上执行
kubeadm join 192.168.50.110:6443 --token abcdef.0123456789abcdef \
        --discovery-token-ca-cert-hash sha256:7f30f55875a14cbcf2ea309ce12a2d397a9755013f37afc73f2eab7d5154d013

# 在 master 执行，查看 节点列表
kubectl get nodes
```

## CNI, flannel

```bash
curl -O https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
```

### 应用

```bash
kubectl apply -f kube-flannel.yml

# 查看 详细， 能看到pod为什么 启动失败，比如拉取镜像失败
kubectl describe pods kube-flannel-ds-fgnhq -n kube-system

# kubectl apply -f ...有可能因为拉取镜像的问题，墙的问题失败，调整好 /etc/containers/registries.conf 的配置后需要重启 crio 使配置生效
systemctl restart crio
# 然后重启pod
# 强制替换pod ，相当于重启
kubectl replace --force -f kube-flannel.yml
# 查看 pod 状态
kubectl get pods --all-namespaces
kubectl logs -f kube-flannel-ds-kp9mt
```

### ingress

```bash
curl -O https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.1/deploy/static/provider/cloud/deploy.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.1/deploy/static/provider/cloud/deploy.yaml
kubectl get pods --namespace=ingress-nginx

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

kubectl create deployment demo --image=httpd --port=80
kubectl expose deployment demo

kubectl create ingress demo-localhost --class=nginx \
  --rule=demo.localdev.me/*=demo:80

kubectl port-forward --namespace=ingress-nginx service/ingress-nginx-controller 8080:80

curl http://demo.localdev.me:8080/
```

<https://www.lixueduan.com/post/kubernetes/01-install/>

<https://wiki.archlinux.org/title/Kubernetes>

<https://kubernetes.io/zh/docs/home/>

<https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/>

<https://www.qikqiak.com/post/containerd-usage/>

<https://landscape.cncf.io/card-mode?category=container-runtime&grouping=category>

<https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/kubelet-integration/>

<https://juejin.cn/post/6894457482635116551>

### pod cidr not assgned

<https://github.com/flannel-io/flannel/issues/728>

### kubectl run

```bash
kubectl run hello --image=hello-world
kubectl run nginx --image=nginx --port=38080
curl -v http://10.85.0.3
```

<https://segmentfault.com/a/1190000020675199>

<https://imroc.cc/post/202105/why-enable-bridge-nf-call-iptables/>

## ubuntu install k8s

```bash
sudo apt update
sudo apt upgrade

# 查看是否启用了 swap, 没有输出就是没启用
swapon
# 禁用 swap
sudo swapoff -a
# 在文件中禁用 /swapfile
sudo vim /etc/fstab

# https://docs.docker.com/engine/install/ubuntu/
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    nfs-common

# nfs-common, 解决 挂载 pvc 报错的问题

sudo tee /etc/modules-load.d/containerd.conf <<EOF
overlay
br_netfilter
EOF

modprobe overlay
modprobe br_netfilter

tee /etc/sysctl.d/kubernetes.conf <<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sysctl --system

sudo apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/docker.gpg
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y containerd.io

containerd config default | sudo tee /etc/containerd/config.toml >/dev/null 2>&1
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl enable containerd
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
sudo apt update
sudo apt install -y kubelet kubeadm kubectl

# mark hold
sudo apt-mark hold kubelet kubeadm kubectl

# 编辑 /etc/hosts 加入新 host
# 复制 证书到新的 control plane

scp -rp /etc/kubernetes/pki/ca.* k8s2:/etc/kubernetes/pki
scp -rp /etc/kubernetes/pki/sa.* k8s2:/etc/kubernetes/pki
scp -rp /etc/kubernetes/pki/front-proxy-ca.* k8s2:/etc/kubernetes/pki
scp -rp /etc/kubernetes/pki/etcd/ca.* k8s2:/etc/kubernetes/pki/etcd
scp -rp /etc/kubernetes/admin.conf k8s2:/etc/kubernetes

# https://blog.csdn.net/weixin_43815140/article/details/108648756

# init control plane for k8sx, or join ...

# 在 control plan 上查看 token 是否可用 
kubeadm token list
# 如果没有输出就重新生成 token
kubeadm token create --print-join-command # 默认有效期24小时,若想久一些可以结合--ttl参数,设为0则用不过期

# init control plane
sudo kubeadm init --control-plane-endpoint=k8s0

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

kubectl cluster-info
kubectl get nodes

## install kubeadm on other vm and join
# join as control plane
ubeadm join k8s0:6443 --token 7iikfr.7b2s9q28iuhmtpvq \
        --discovery-token-ca-cert-hash sha256:97d5fe071438d0cc279078e76cf768e898ff61b75069d574eb3bef36e81723db \
        --control-plane

# join as worker
kubeadm join k8s0:6443 --token 7iikfr.7b2s9q28iuhmtpvq \
        --discovery-token-ca-cert-hash sha256:97d5fe071438d0cc279078e76cf768e898ff61b75069d574eb3bef36e81723db

## ---

kubectl cluster-info
kubectl get nodes

curl https://projectcalico.docs.tigera.io/manifests/calico.yaml -O
kubectl apply -f calico.yaml

kubectl get pods -n kube-system
kubectl get nodes


## Test Kubernetes Installation
kubectl create deployment nginx-app --image=nginx --replicas=1
kubectl get deployment nginx-app

kubectl expose deployment nginx-app --type=NodePort --port=80

kubectl get svc nginx-app
kubectl describe svc nginx-app

# check status
kubectl get pods --all-namespaces
kubectl get pods --all-namespaces -o wide
kubectl describe pod -n <NAMESPACE> <NAME>
kubectl logs --namespace <NAMESPACE> <NAME>
kubectl cluster-info
kubectl get nodes
kubectl get po -n default
kubectl delete deployment deployment0
kubectl delete svc svc0

## 卸载服务, delete service and deployment
kubectl delete -f deployment.yaml
```

<https://www.linuxtechi.com/install-kubernetes-on-ubuntu-22-04/>

## deployment

deployment 是资源控制管理器，比如动态扩缩容，滚动更新，回滚等等操作，在k8s里面有多种资源控制器，比如rs、rc、ds、job等，rc已经被rs替代，然而deployment的功能又包含rs，所以我这里用dep。

## service

service 服务代理，代理谁？pod，通过label标签匹配，为什么需要它？如果没有它的话，pod暴露的是一个个ip，如果中间一个pod挂了，dep为了满足我们的期望值，会重新创建一个pod，这时候出问题了，刚好service就是为了解决这个问题而诞生的，它通过标签匹配到集群里面对应的标签pod，监听它们的状态，然后把pod信息同步到service里面，提供外部服务。service代理模式分三种iptables、ipvs等。

## 部署服务到 k8s

### golang 服务

- 编译并推送到 docker registery
- 创建 deployment.yml

```yml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rssx-api
  namespace: default # 声明工作空间，默认为default
spec:
  replicas: 1
  selector:
    matchLabels:
      name: rssx-api
  template:
    metadata:
      labels:
        name: rssx-api
    spec:
      containers:
        - name: rssx-api-container
          image: registry.wiloon.com/rssx-api:v0.0.1 # 镜像地址
          imagePullPolicy: Always # 每次都从仓库拉取镜像, 即使版本号一样也拉取
          ports:
            - containerPort: 8080 # containerPort 是声明容器内部的端口

---
apiVersion: v1
kind: Service
metadata:
  name: rssx-api-service
  namespace: default  # 声明工作空间，默认为default
spec:
  type: NodePort
  ports:
    - name: http
      port: 18081      # Service暴露在cluster-ip上的端口，通过<cluster-ip>:port访问服务,通过此端口集群内的服务可以相互访问
      targetPort: 8080 # Pod的外部访问端口，port和nodePort的数据通过这个端口进入到Pod内部，Pod里面的containers的端口映射到这个端口，提供服务
      nodePort: 31081  # Node节点的端口，<nodeIP>:nodePort 是提供给集群外部客户访问service的入口
  selector:
    name: rssx-api
```

- 应用

```bash
kubectl create -f /tmp/deployment.yaml
```

- 卸载

```bash
kubectl delete -f /tmp/deployment.yaml
```

### vue 前端

- 编译并推送到 docker registery
- 创建 deployment.yml

```yml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rssx-ui
  namespace: default # 声明工作空间，默认为 default
spec:
  replicas: 1
  selector:
    matchLabels:
      name: rssx-ui
  template:
    metadata:
      labels:
        name: rssx-ui
    spec:
      containers:
        - name: rssx-ui-container
          image: registry.wiloon.com/rssx-ui:v0.0.1
          imagePullPolicy: Always
          ports:
            - containerPort: 80 # containerPort 是声明容器内部的port

---
apiVersion: v1
kind: Service
metadata:
  name: rssx-ui-service
  namespace: default  # 声明工作空间，默认为default
spec:
  type: NodePort
  ports:
    - name: http
      port: 18082 # Service 暴露在 cluster-ip 上的端口，通过 <cluster-ip>:port 访问服务,通过此端口集群内的服务可以相互访问
      targetPort: 80 # Pod的外部访问端口，port和nodePort的数据通过这个端口进入到Pod内部，Pod里面的containers的端口映射到这个端口，提供服务
      nodePort: 31082 # Node节点的端口，<nodeIP>:nodePort 是提供给集群外部客户访问service的入口
  selector:
    name: rssx-ui
```

- 应用

```bash
kubectl create -f /tmp/k8s-rssx-ui-deployment.yaml
```

- 卸载

```bash
kubectl delete -f /tmp/k8s-rssx-ui-deployment.yaml
```

<https://jasonkayzk.github.io/2021/10/31/%E4%BD%BF%E7%94%A8K8S%E9%83%A8%E7%BD%B2%E6%9C%80%E7%AE%80%E5%8D%95%E7%9A%84Go%E5%BA%94%E7%94%A8/>

## PV

<https://www.cnblogs.com/along21/p/10342788.html>

create nfs server <wiloon.com/nfs>

### pv.yaml

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
    name: pv0
spec:
    capacity:
      storage: 2Gi
    accessModes:
      - ReadWriteMany
    persistentVolumeReclaimPolicy: Recycle
    storageClassName: "pv0"
    nfs:
      path: "/data/nfs"
      server: 192.168.50.50
```

```bash
kubectl create -f pv.yaml
kubectl get pv pv0
```

### pvc.yaml

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: pvc0
  namespace: default
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 2Gi
  storageClassName: pv0
```

```bash
kubectl create -f pvc.yaml
kubectl get pvc pvc0
```

### 查看 pv, pvc

```bash
kubectl get pv,pvc -n default
```

## redis

### redis-config.yaml

config map

```yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: redis-config
  namespace: default
  labels:
    app: redis
data:
  redis-config: |
    dir /data
    port 6379
    bind 0.0.0.0
    appendonly yes
    protected-mode no
    pidfile /data/redis.pid
```

```bash
kubectl apply -f redis-config.yaml
kubectl get configmap
kubectl get configmap -n namespace0
kubectl edit configmap configmap0
kubectl delete configmap configmap0

```

### redis-deployment.yaml

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  labels:
    app: redis
spec:
  type: NodePort
  ports:
    - name: redis
      port: 16379
      targetPort: 6379
      nodePort: 32379
  selector:
    app: redis
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: default
  labels:
    app: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis:5.0.8
          command:
            - "sh"
            - "-c"
            - "redis-server /usr/local/etc/redis/redis.conf"
          ports:
            - containerPort: 6379
          resources:
            limits:
              cpu: 1000m
              memory: 1024Mi
            requests:
              cpu: 1000m
              memory: 1024Mi
          livenessProbe:
            tcpSocket:
              port: 6379
            initialDelaySeconds: 300
            timeoutSeconds: 1
            periodSeconds: 10
            successThreshold: 1
            failureThreshold: 3
          readinessProbe:
            tcpSocket:
              port: 6379
            initialDelaySeconds: 5
            timeoutSeconds: 1
            periodSeconds: 10
            successThreshold: 1
            failureThreshold: 3
          volumeMounts:
            - name: data
              mountPath: /data
            - name: config
              mountPath: /usr/local/etc/redis
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: pvc0
        - name: config
          configMap:
            name: redis-config
            items:
            - key: redis-config
              path: redis.conf
        - name: sys
          hostPath:
            path: /sys
```

```bash
kubectl create -f redis-deployment.yaml
```

## evicted

eviction，即驱赶的意思，意思是当节点出现异常时，kubernetes将有相应的机制驱赶该节点上的Pod。
多见于资源不足时导致的驱赶。

删除旧 evicted 的遗留

```bash
kubectl get pods | grep Evicted | awk '{print $1}' | xargs kubectl delete pod

```

## mysql

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  type: NodePort
  ports:
    - name: mysql
      port: 13306
      targetPort: 3306
      nodePort: 32306
  selector:
    app: mysql
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  selector:
    matchLabels:
      app: mysql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - image: mysql:5.6
        name: mysql
        env:
          # 在实际中使用 secret
        - name: MYSQL_ROOT_PASSWORD
          value: password0
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: pvc0
```

## 访问 mysql

```bash
kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -ppassword0
```

<https://kubernetes.io/zh-cn/docs/tasks/run-application/run-single-instance-stateful-application/>

## kubectl create, apply

kubectl create：

（1）kubectl create命令，是先删除所有现有的东西，重新根据yaml文件生成新的。所以要求yaml文件中的配置必须是完整的

（2）kubectl create命令，用同一个yaml 文件执行替换replace命令，将会不成功，fail掉。

kubectl apply：

  kubectl apply命令，根据配置文件里面列出来的内容，升级现有的。所以yaml文件的内容可以只写需要升级的属性
————————————————
版权声明：本文为CSDN博主「daiqinge」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/daiqinge/article/details/103249260>

## influxdb

```bash
kubectl create configmap influxdb-config --from-file influxdb.conf
kubectl get cm influxdb-config
#查看CM内容，内容省略
kubectl get cm influxdb-config -oyaml
```

<https://www.cnblogs.com/zhangsi-lzq/p/14457707.html>

## influxdb-dp.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: influxdb-svc
  namespace: default
spec:
  type: NodePort
  ports:
    - port: 18086
      targetPort: 8086
      nodePort: 32086
      name: influxdb
  selector:
    app: influxdb
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: influxdb-dp
  namespace: default
  labels:
spec:
  replicas: 1
  selector:
    matchLabels:
      app: influxdb
  template:
    metadata:
      labels:
        app: influxdb
    spec:
      containers:
      - name: influxdb
        image: influxdb:1.8.10-alpine
        imagePullPolicy: IfNotPresent
        ports:
        - name: influxdb
          containerPort: 8086
          protocol: TCP
        volumeMounts:
        - name: influxdb-data
          mountPath: /var/lib/influxdb
          subPath: influxdb
        - name: influxdb-config
          mountPath: /etc/influxdb
      volumes:
      - name: influxdb-data
        persistentVolumeClaim:
          claimName: pvc0
      - name: influxdb-config
        configMap:
          name: influxdb-config
```

## grafana-dp.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: grafana
  labels:
    k8s-app: grafana
spec:
  type: NodePort
  ports:
  - name: http
    port: 3000
    targetPort: 3000
    nodePort: 30300
  selector:
    k8s-app: grafana
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  labels:
    k8s-app: grafana
spec:
  selector:
    matchLabels:
      k8s-app: grafana
  template:
    metadata:
      labels:
        k8s-app: grafana
    spec:
      initContainers:             ## 初始化容器，用于修改挂载的存储的文件夹归属组与归属用户
      - name: init-file
        image: busybox:1.28
        imagePullPolicy: IfNotPresent
        securityContext:
          runAsUser: 0
        command: ['chown', '-R', "472:0", "/var/lib/grafana"]
        volumeMounts:
        - name: data
          mountPath: /var/lib/grafana
          subPath: grafana
      containers:                
      - name: grafana             ## Grafana 容器
        image: grafana/grafana:8.2.6
        ports:
        - name: http
          containerPort: 3000
        env:                      ## 配置环境变量，设置 Grafana 的默认管理员用户名/密码
        - name: GF_SECURITY_ADMIN_USER
          value: "admin"
        - name: GF_SECURITY_ADMIN_PASSWORD
          value: "password0"
        readinessProbe:           ## 就绪探针
          failureThreshold: 10
          httpGet:
            path: /api/health
            port: 3000
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 30
        livenessProbe:            ## 存活探针
          failureThreshold: 10
          httpGet:
            path: /api/health
            port: 3000
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        volumeMounts:            ## 容器挂载配置
        - name: data
          mountPath: /var/lib/grafana
          subPath: grafana
      volumes:                   ## 共享存储挂载配置
      - name: data
        persistentVolumeClaim:
          claimName: pvc0     ## 指定使用的 PVC
```

## joplin-dp.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: joplin
spec:
  type: NodePort
  ports:
    - name: joplin
      port: 12230
      targetPort: 22300
      nodePort: 32230
  selector:
    app: joplin
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: joplin
spec:
  selector:
    matchLabels:
      app: joplin
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: joplin
    spec:
      containers:
      - image: joplin/server:latest
        name: joplin
        env:
        - name: APP_BASE_URL
          value: https://joplin.wiloon.com
        - name: APP_PORT
          value: 22300
        ports:
        - containerPort: 22300
          name: joplin
        volumeMounts:
        - name: volumne0
          mountPath: /home/joplin
          subPath: joplin
      volumes:
      - name: volumne0
        persistentVolumeClaim:
          claimName: pvc0
```
