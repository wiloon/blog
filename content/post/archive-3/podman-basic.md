---
title: podman basic
author: "-"
date: 2020-01-19T15:30:35+00:00
url: podman
tags:
  - podman

---
## podman basic
### install
https://podman.io/getting-started/installation
### ubuntu
    . /etc/os-release
    echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
    curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key | sudo apt-key add -

    sudo apt-get update
    sudo apt-get -y upgrade
    sudo apt-get -y install podman

### centos
    dnf install podman
### archlinux
```bash
pacman -S podman
```

### podman command
```bash
podman version
podman info --debug

podman ps
podman ps -f  name=zookeeper
podman ps -a --format "{{.ID}} {{.Names}}"
podman ps -a
podman inspect -l

podman top <container_id>
podman container checkpoint <container_id>
podman container restore <container_id>

podman stop --latest
podman rm --latest
podman --log-level=debug pull dockerhub.azk8s.cn/library/golang
```
### 查看 cpu 内存占用
```bash
podman stats
```

### 配置driver
    vim /etc/containers/storage.conf
    [storage]

    # Default Storage Driver, Must be set for proper operation.
    driver = "overlay2"

### logs
    podman logs --since 1m -f conter_id_0
    podman logs --latest
### registry config, mirror
/etc/containers/registries.conf

```
[registries.search]
registries = ['docker-registries.wiloon.com']
[registries.insecure]
registries = ['docker-registries.wiloon.com']
[registries.block]
registries = []
```

```bash
unqualified-search-registries = ["docker.io"]
[[registry]]
prefix = "docker.io"
location = "******.mirror.aliyuncs.com"

[[registry-insecure]]
prefix = "docker.io"
location = "docker-registries.wiloon.com"
```
#### 另外一种配置文件
    unqualified-search-registries = ["docker.io"]
    [[registry]]
    prefix = "docker.io"
    location = "xxxxxx.mirror.aliyuncs.com"

### run
限制cpu, 内存
```bash
podman run \
-d \
--name name0 \
-p 2000:80/tcp \
-v /etc/localtime:/etc/localtime:ro \
--memory=2g \
--cpus=1 \
image0_name

```

### generate systemd script

```bash
export service_name=foo
podman generate systemd $service_name > /usr/lib/systemd/system/$service_name.service
systemctl enable $service_name && systemctl start $service_name
```

### network

```bash
podman network create --driver bridge net0
podman network create --driver bridge \
--subnet 172.22.16.0/24 \
--gateway 172.22.16.1 net0

podman network ls
podman network inspect net0

podman run -it --network=net0 busybox
# 指定ip
podman run -it --network=net0 --ip 172.22.16.8 busybox
```

### centos 8 install podman

Install EPEL Repository on RHEL / CentOS 8

```bash
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
```

Ensure PowerTools repo is enabled as well – CentOS 8 only

```bash
sudo dnf config-manager --set-enabled PowerTools
```

Install Podman

```bash
sudo dnf -y update
sudo systemctl reboot

sudo dnf module list | grep container-tools
sudo dnf install -y @container-tools
podman version
```

### volume

```bash
podman volume ls
podman volume create volume0
podman volume rm volume0
```

## pod
    podman pod create -n pod_0 -p 8086:8086 -p 3000:3000 -p 8888:8888
    # 使用pod, 端口映射要配置到pod上，pod内的容器不配端口

#### 创建容器并加入pod
    podman run -d --pod pod_name_0 influxdb

https://www.hangge.com/blog/cache/detail_2475.html
  
https://www.mankier.com/1/podman-unshare
  
https://opensource.com/article/19/2/how-does-rootless-podman-work
  
https://www.mankier.com/1/podman-generate-systemd
https://computingforgeeks.com/how-to-install-epel-repository-on-rhel-8-centos-8/"
https://computingforgeeks.com/how-to-install-epel-repository-on-rhel-8-centos-8/embed/#?secret=Vw63QL1LVb"
https://computingforgeeks.com/how-to-install-and-use-podman-on-centos-rhel/"
https://computingforgeeks.com/how-to-install-and-use-podman-on-centos-rhel/embed/#?secret=kP3lpS51yS"

### podman pod
    podman pod --help
    podman pod create --help
    podman pod ps
    podman pod rm pod0
    
### rootless
```bash
pacman  -S crun
usr/share/containers/libpod.conf -- runtime="crun"

sudo touch /etc/subuid
sudo touch /etc/subgid
sudo usermod --add-subuids 10000-65536 user0
sudo usermod --add-subgids 10000-65536 user0
getcap /usr/bin/newuidmap
getcap /usr/bin/newgidmap
```

### macvlan
https://ctimbai.github.io/2019/04/14/tech/docker-macvlan/

```bash
# docker network create -d macvlan --subnet=172.16.10.0/24 --gateway=172.16.10.1 -o parent=enp0s8 mac1
podman network create \
--subnet=192.168.50.0/24 \
--gateway=192.168.50.1 \
--macvlan=enp1s0 mac1

-d 指定 Docker 网络 driver
--subnet 指定 macvlan 网络所在的网络
--gateway 指定网关
-o parent 指定用来分配 macvlan 网络的物理网卡
 cat /etc/cni/net.d/mac1.conflist
```

在 host1 运行容器 c1，并指定使用 macvlan 网络: 
```bash
podman run -itd --name c1 --ip=192.168.50.99 --network mac1 busybox
```

https://stackoverflow.com/questions/59515026/how-do-i-replicate-a-docker-macvlan-network-with-podman

### podman 
http://docs.podman.io/en/latest/

### VFS , fuse-overlayfs
Our first recommendation in these cases is usually to avoid using VFS, and instead use fuse-overlayfs.

### image, images
    podman images -a
    podman image prune
    podman image rm image-id-0
    
---

https://github.com/containernetworking/plugins


### other 
    podman unshare cat /proc/self/uid_map
    unshare -U


### reset, 执行工厂重置
    podman system reset

### podman history, 查看构建命令
    podman history image0

### filter
    podman ps -a -f "status=exited"

>https://docs.podman.io/en/latest/markdown/podman-ps.1.html
