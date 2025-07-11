---
title: podman basic
author: "-"
date: 2023-04-06 12:25:16
url: podman
categories:
  - container
tags:
  - podman
  - remix
---
## podman basic

## install

[https://podman.io/getting-started/installation](https://podman.io/getting-started/installation)

```bash
# archlinux install podman
pacman -S podman
# 提示选择 crun, runc, 选 crun
# netavark aardvark-dns 会默认安装
# 正常情况，安装 podman 之后不需要重启系统, 但是如果有异常，比如 CNI 之类 的问题，可以考虑重启一下...
```

### `Netavark`

`Netavark` 是一个 用 rust 实现的 配置 linux 容器网络的工具。

In addition to the existing CNI Out of the stack,
Podman Now it also supports based on  Netavark  and  Aardvark New network stack. 
The new stack features improved support for containers in multiple networks 、 improvement IPv6 Support, 
And improve performance. To ensure that there is no impact on existing users, 
used CNI The stack will keep the default value of the existing installation, 
The new installation will use `Netvark`.

[https://github.com/containers/netavark](https://github.com/containers/netavark)

### crun, runc

runc 和 crun 是容器运行时，可以互换使用，因为二者都实现 OCI 运行时规范。
与 runc 相比，crun 容器运行时有一些优点，因为它速度更快，且需要较少的内存。
因此，crun 容器运行时是推荐使用的容器运行时。

runc 运行时与 Docker 共享大量低级代码，但不依赖于 Docker 平台的任何组件。

crun 是一个快速、占用内存少的 OCI 容器运行时，是用 C 语言编写的。crun 二进制文件比 runc 二进制文件小多达 50 倍，快两倍。使用 crun，也可以在运行容器时设置最少的进程数。crun 运行时也支持 OCI hook。

### ubuntu install podman

```bash
sudo apt-get -y update
sudo apt-get -y install podman

# ------
. /etc/os-release
echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key | sudo apt-key add -

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install podman
```

### centos install podman

```bash
dnf install podman
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

### hello world

测试一下 podman 环境

```bash
podman run --rm hello-world
# 能打印 Hello from Docker! 就是成功了
```

### podman command

```bash
podman version
podman info --debug

podman ps

# 按名字过滤
podman ps -f  name=zookeeper

# 显示指定的列
podman ps -a --format "{{.ID}} {{.Names}}"

# 查看元数据, env, volume...
sudo podman inspect postgres

# 查看一部分元数据
sudo podman inspect --format "{{.Mounts}}" postgres

podman ps -a
podman inspect -l

podman top <container_id>
podman container checkpoint <container_id>
podman container restore <container_id>

podman stop --latest
podman rm --latest
podman --log-level=debug pull dockerhub.azk8s.cn/library/golang

# 显示虚悬镜像(dangling image)
podman image ls -f dangling=true

# 删除无效镜像
podman image prune
```

### 虚悬镜像 (dangling image)

为什么会有 `<none>` 这样命名的镜像？这些镜像 docker 称为 虚悬镜像，当镜像被新的镜像覆盖时候，老版本镜像名称会变成 `<none>`。

### env

使用 env 命令来查看容器的环境变量

```bash
podman run --rm hello-world env
```

### podman 查看 cpu 内存占用

```bash
podman stats
```

### 配置 driver

```bash
vim /etc/containers/storage.conf
[storage]

# Default Storage Driver, Must be set for proper operation.
driver = "overlay2"
```

修改driver之后 要删除 文件 sudo rm -rf ~/.local/share/containers/, 否则会报错: User-selected graph driver "overlay2" overwritten by graph driver "overlay" from database - delete libpod local files to resolve

[https://github.com/containers/podman/issues/5114](https://github.com/containers/podman/issues/5114)

## logs

```bash
podman logs --since 1m -f conter_id_0
podman logs --latest
```

### registry config, mirror

配置文件有两种版本格式，v1 和 v2，两种格式的配置不能混用，混用会提示错误。

vim /etc/containers/registries.conf

## podman registry config

```bash
vim /etc/containers/registries.conf

# content
unqualified-search-registries = ["docker.io"]

[[registry]]
prefix = "docker.io"
location = "registry-1.docker.io"
```

#### v2

```bash
# 例：使用 podman pull registry.access.redhat.com/ubi8-minimal 时，
# 仅仅会从registry.access.redhat.com去获取镜像。
# 如果直接使用 podman pull ubuntu 时，没有明确指明仓库的时候，使用以下配置的仓库顺序去获取
unqualified-search-registries = ["docker.io", "registry.access.redhat.com"]
 
# 配置仓库的地址，可以直接在location里配置国内镜像例如：docker.mirrors.ustc.edu.cn
# 直接在location里配置的时候，可以不需要后面的 [[registry.mirror]] 内容，
# 但是这样只能配置一个镜像地址，这个镜像挂了就没法尝试其它镜像
[[registry]]
prefix = "docker.io"
location = "docker.io"
 
# 在这里可以配置多个镜像地址，前提是至少有一个[[registry]]配置。
# 需要注意的是，无论 unqualified-search-registries 选择了哪个仓库，
# 都会先从这里的上下顺序开始去拉取镜像，最后才会去匹配上 prefix 的 [[registry]]
# 配置的 location 位置拉取镜像。所以这里需要注意，上面配置的不同仓库类型，这里配置的镜像并不
# 能是通用的，所以 unqualified-search-registries 配置了多个仓库的时候，就最好直接使用
# [[registry]] 的 location 指定镜像地址，不要配置 [[registry.mirror]] 了。
# redhat 的国内镜像暂未发现。
[[registry.mirror]]
location = "docker.mirrors.ustc.edu.cn"
[[registry.mirror]]
location = "registry.docker-cn.com"
```

[https://blog.csdn.net/leave00608/article/details/114156354](https://blog.csdn.net/leave00608/article/details/114156354)

```Bash
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

```bash
unqualified-search-registries = ["docker.io"]
[[registry]]
prefix = "docker.io"
location = "xxxxxx.mirror.aliyuncs.com"
```

## run

限制 cpu, 内存

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

## podman systemd

podman-systemd 已被弃用，请参考使用 Quadlet 的新方法
现在使用 podman generate systemd，会提示 DEPRECATED command: It is recommended to use Quadlets for running containers and pods under systemd.

generate systemd script

```bash
# 容器名跟服务名一致
export service_name=foo
podman generate systemd $service_name > /usr/lib/systemd/system/$service_name.service
# enable service
systemctl enable $service_name
# enable and start service
systemctl --now enable $service_name
```

## podman Quadlets

```Bash

yay -S podlet

mkdir -p /etc/containers/systemd/

podlet podlet podman run -d --name bitwarden -v bitwarden-data:/data/ -p 8000:80 vaultwarden/server:1.28.1-alpine > /etc/containers/systemd/bitwarden.container

# content
# bitwarden.container
[Container]
ContainerName=bitwarden
Image=vaultwarden/server:1.28.1-alpine
PublishPort=8000:80
Volume=bitwarden-data:/data/

[Install]
WantedBy=multi-user.target default.target

systemctl daemon-reload
systemctl start bitwarden
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

## volume

```bash
podman volume ls
podman volume create volume0
podman volume rm volume0
podman volume volume0
```

```bash
# backup
podman run --rm \
  --volume volume0:/tmp \
  --volume $(pwd):/backup \
  alpine \
  tar cvf /backup/volume0.tar /tmp

# restore
podman run --rm \
  --volume volume0:/tmp \
  --volume $(pwd):/backup \
  alpine \
  tar xvf /backup/volume0.tar -C /tmp --strip 1
```

## 备份 volume

```bash
#!/bin/sh
workdir=/data/bitwarden/backup
find $workdir -mtime +30 -type f -name "*.*" -exec rm -f {} \;

timestamp=$(date '+%Y%m%d%H%M%S')
filename=bitwarden-data-${timestamp}.tar 

container_path=/backup
podman run --rm \
  --volume bitwarden-data:/tmp \
  --volume $workdir:$container_path \
  alpine \
  tar cvf $container_path/$filename /tmp
```

```bash
workdir=/data/bitwarden/backup
find $workdir -mtime +30 -type f -name "*.*" -exec rm -f {} \;

timestamp=$(date '+%Y%m%d%H%M%S')
filename=bitwarden-data-${timestamp}.tar 

container_path=/backup

docker run --rm \
  --volume bitwarden-data:/tmp \
  --volume $workdir:$container_path \
  alpine \
  tar xvf $container_path/$filename -C /tmp --strip 1
```

## pod

### podman pod

```bash
podman pod --help
podman pod create --help
podman pod ps
podman pod rm pod0

podman pod create -n pod_0 -p 8086:8086 -p 3000:3000 -p 8888:8888
# 使用pod, 端口映射要配置到pod上，pod内的容器不配端口
```

#### 创建容器并加入 pod

```bash
podman run -d --pod pod_name_0 influxdb
```

[https://www.hangge.com/blog/cache/detail_2475.html](https://www.hangge.com/blog/cache/detail_2475.html)
  
[https://www.mankier.com/1/podman-unshare](https://www.mankier.com/1/podman-unshare)
  
[https://opensource.com/article/19/2/how-does-rootless-podman-work](https://opensource.com/article/19/2/how-does-rootless-podman-work)
  
[https://www.mankier.com/1/podman-generate-systemd](https://www.mankier.com/1/podman-generate-systemd)

[https://computingforgeeks.com/how-to-install-epel-repository-on-rhel-8-centos-8/](https://computingforgeeks.com/how-to-install-epel-repository-on-rhel-8-centos-8/)"

[https://computingforgeeks.com/how-to-install-epel-repository-on-rhel-8-centos-8/embed/#?secret=Vw63QL1LVb](https://computingforgeeks.com/how-to-install-epel-repository-on-rhel-8-centos-8/embed/#?secret=Vw63QL1LVb)"

[https://computingforgeeks.com/how-to-install-and-use-podman-on-centos-rhel/](https://computingforgeeks.com/how-to-install-and-use-podman-on-centos-rhel/)"

[https://computingforgeeks.com/how-to-install-and-use-podman-on-centos-rhel/embed/#?secret=kP3lpS51yS](https://computingforgeeks.com/how-to-install-and-use-podman-on-centos-rhel/embed/#?secret=kP3lpS51yS)"

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

[https://ctimbai.github.io/2019/04/14/tech/docker-macvlan/](https://ctimbai.github.io/2019/04/14/tech/docker-macvlan/)

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

[https://stackoverflow.com/questions/59515026/how-do-i-replicate-a-docker-macvlan-network-with-podman](https://stackoverflow.com/questions/59515026/how-do-i-replicate-a-docker-macvlan-network-with-podman)

### podman

[http://docs.podman.io/en/latest/](http://docs.podman.io/en/latest/)

### VFS , fuse-overlayfs

Our first recommendation in these cases is usually to avoid using VFS, and instead use fuse-overlayfs.

### image, images

```bash
podman images -a
podman image prune
podman image rm image-id-0
```

[https://github.com/containernetworking/plugins](https://github.com/containernetworking/plugins)

### other

```bash
podman unshare cat /proc/self/uid_map
unshare -U
```

### reset, 执行工厂重置

```bash
podman system reset
```

### podman history, 查看构建命令

```bash
podman history image0
```

### filter

```bash
podman ps -a -f "status=exited"
```

[https://docs.podman.io/en/latest/markdown/podman-ps.1.html](https://docs.podman.io/en/latest/markdown/podman-ps.1.html)

## 导出镜像, podman save

podman save will save parent layers of the image(s)

```bash
# 如果执行 podman save 时磁盘上已经存在 kafka.tar 会提示: docker-archive doesn't support modifying existing images
# --format=docker-archiv, podman save 保存成兼容 docker 的文件格式
sudo podman save --format=docker-archive -o kafka.tar 5701259bb69a bitnami/kafka:3.4.0
podman save be96e19ac6ef > pingd-proxy.tar
```

>wangyue.dev/docker/save

## template

```bash
podman run \
-d \
--name foo \
-p 1234:80 \
-v /etc/localtime:/etc/localtime:ro \
project0:0.0.1
```

## podman-compose

```bash
sudo pacman -S podman-compose

podman-compose --help
podman-compose up --help
podman-compose up
```

## 默认 volumes 目录

/var/lib/containers/storage/volumes

## uninstall

```bash
pacman -R podman
pacman -R crun
pacman -R containers-common
pacman -R netavark
pacman -R aardvark-dns
```
