---
title: docker basic, commands
author: "-"
date: 2018-01-27T08:35:04+00:00
url: docker/basic
categories:
  - container
tags:
  - reprint
  - remix
---
## docker basic, commands

## commands

```Bash
docker exec nexus3 cat /nexus-data/admin.password
docker ps --filter"name=test-nginx"
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}"
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Command}}\t{{.Status}}\t{{.Names}}"
docker ps --format "table {{.ID}}\t{{.IMAGE}}\t{{.CREATED}}\t{{.STATUS}}\t{{.NAMES}}"

docker inspect xxx
docker container update --restart=no <containername>
# 修改 docker 容器为开机启动
docker container update --restart=always <containername>
```

### 批量删除镜像

```bash
docker rmi $(docker images | grep "name0" | awk '{print $3}')
docker rmi -f $(docker images | grep "name0" | awk '{print $3}')
```

```bash
docker restart foo

# 列出所有的容器 ID
docker ps -aq
# 停止所有的容器
docker stop $(docker ps -aq)
# 删除所有的容器
docker image ls
docker rm $(docker ps -aq)
# 删除所有的镜像

docker rmi $(docker images -q)
# 复制文件

docker cp mycontainer:/opt/file.txt /opt/local/
docker cp /opt/local/file.txt mycontainer:/opt/

```

### docker port

docker port :列出指定的容器的端口映射,或者查找将PRIVATE_PORT NAT到面向公众的端口。
  
docker port [OPTIONS] CONTAINER [PRIVATE_PORT[/PROTO]]

### docker pod log

```bash
/var/log/containers/
/var/log/pods/<container id>/container-0
/var/lib/docker/containers/<container id>
```

### install docker

[https://blog.wiloon.com/docker/install](https://blog.wiloon.com/docker/install)

### image

```bash
# 列出本机的所有 image 文件
docker image ls
#显示包括中间层镜像在内的所有镜像
docker image ls -a
# 显示虚悬镜像(dangling image)
docker image ls -f dangling=true
docker image ls --digests
# 删除 image
docker image rm [image id]

# 删除未使用的映像, REPOSITORY: <none>, tag: <none>, 
docker image prune

docker rmi f8ab12e03d53
Error response from daemon: conflict: unable to delete f8ab12e03d53 (must be forced) - image is referenced in multiple repositories
docker rmi 192.168.0.1/you/tom:1.0.8
```

## archlinux install docker

```bash
sudo pacman -S docker
systemctl start docker.service

docker run -it --rm archlinux bash -c "echo hello world"

pacman -S docker-compose

docker ps -s

# docker
docker run \
-d \
--name redis \
-p 6379:6379 \
-v /etc/localtime:/etc/localtime:ro \
-e FOO="bar" \
--restart=always \
redis
```

### network

```bash
docker network ls
docker network inspect 网络ID
```

### volume

```bash
docker volume ls
docker volume create --name influxdb-config
docker volume rm influxdb-config
# 删除实例同时删除 volume
docker rm -v instance0
# 清理 无主 (dangling) 的数据卷
docker volume prune
```

容器创建后不能再新增 volume, 可以先commit到镜像, 再创建新的容器。

### 时区问题

```bash
-v /etc/localtime:/etc/localtime:ro
```

### 查看 docker 容器使用的资源, cpu, 内存, IO

```bash
docker stats
```

[https://www.cnblogs.com/sparkdev/p/7821376.html](https://www.cnblogs.com/sparkdev/p/7821376.html)

### logs

```bash
docker logs --since 10s -f influxdb
```

### docker build

```bash
# 构建镜像
# docker build [选项] <上下文路径/URL/->
# --tag, -t: 镜像的名字及标签,通常 name:tag 或者 name 格式；可以在一次构建中为一个镜像设置多个标签。
# --add-host=foo.wiloon.com:192.168.xx.xxx    # /etc/hosts

docker build -t dnsmasq:v1.0.0 .
docker tag dnsmasq:v1.0.0 swr.cn-south-1.myhuaweicloud.com/{组织名称}/dnsmasq:v1.0.0
docker push swr.cn-south-1.myhuaweicloud.com/{组织名称}/dnsmasq:v1.0.0
docker pull swr.cn-south-1.myhuaweicloud.com/{组织名称}/dnsmasq:v1.0.0

#  从 Git repo 中构建
docker build https://github.com/twang2218/gitlab-ce-zh.git#:11.1

# -f 指定 Dockerfile 路径
docker build -f /path/to/Dockerfile .
```

## docker run

创建一个新的容器并运行一个命令
  
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

```bash
docker run -it --rm ubuntu bash
docker run -d id0 sleep 6000

# sleep 6000, 6000 秒(100分钟/1小时40分)之后 关闭
# -i, --interactive=false   打开 STDIN, 用于控制台交互
# -t, --tty=false           分配 tty 设备, 该可以支持终端登录, 默认为 false
# -p 80:80 映射端口, hostPort:containerPort
# -t -a stdout              Outputs the container logs on the standard output
# -P, --publish-all=false   Docker自动分配一个未被使用的端口
# -v, --volume=[]           Bind mount a volume(挂载目录 -v /root:/opt/temp), 跟mount一样，path 里如果有文件的话，挂载之后是看不到的。
# -d, --detach=false        Run container in background and print container ID(后台运行) 并返回容器ID；
# --rm 容器退出后随之将其删除
# bash: 放在镜像名后的是命令,这里我们希望有个交互式 Shell,因此用的是 bash
# --name="nginx-lb" : 为容器指定一个名称；
# --privileged=true, 大约在0.6版,privileged被引入docker。使用该参数,container内的root拥有真正的root权限。
# --restart=always
# --cap-add=SYS_TIME
# -e, --env=[]                    Set environment variables(设置环境变量)
# --link 用来链接2个容器,使得源容器 (被链接的容器) 和接收容器 (主动去链接的容器) 之间可以互相通信,并且接收容器可以获取源容器的一些数据,如源容器的环境变量。--link <name or id>:alias 其中,name和id是源容器的name和id,alias是源容器在link下的别名。 建议使用 docker network 而不是 --link
# --cpus=2
# --cpuset-cpus="0" --cpu-shares=512
# --hostname 修改容器的 hostname, 这个参数会直接将对应主机名写入机器的/etc/hostname文件中：


docker run \
-d \
--name name0 \
-p 2000:80/tcp \
-v /etc/localtime:/etc/localtime:ro \
--cpus 1 \
-m 1024m \
--restart=always \
image0_name

```

```bash
# 进入容器
docker exec -it webserver bash
docker exec -it --user=root foo bash

#查看存储层变化
docker diff webserver

# 将容器保存为镜像
sudo docker commit webserver nginx:v2
sudo docker commit \
    --author "wiloon" \
    --message "modify index" \
    webserver \
    nginx:v2

# 查看镜像内的历史记录
docker history nginx:v2

docker volume ls
docker volume rm

sudo pacman -S docker    # install docker
sudo systemctl start docker.service

sudo pacman -S docker-compose

# search image
sudo docker search [image name]

# 查看docker 版本
docker --version #查看版本
docker-compose --version #查看版本
docker-machine --version #查看版本
docker version #查看client和server端版本,并可以查看是否开启体验功能

sudo docker-compose up

docker ps                # 列出容器
docker stop container_id # 停止容器
docker rm container_id   # 删除容器

# network
docker network ls

# start dokcer
systemctl start docker
docker pull centos
docker image pull library/hello-world
docker container run hello-world
docker container kill [containID]

# start daemon manually
dockerd
docker images
docker search seanlo

docker container ls
docker container logs 244d1663f0b7 -f
docker container stop
docker container rm
docker container prune
docker run -dit -p 5000:5000 ubuntu
docker network create -d bridge my-net
```

### macvlan, --net, --ip

```bash
    docker run \
    --name memcache \
    -d \
    --net net0 \
    --ip 192.168.1.xxx \
    -p 11211:11211 \
    -v /etc/localtime:/etc/localtime:ro \
    --restart=always \
    memcached -m 16
```

default volumn path /var/lib/docker/volumes/

---

>[https://segmentfault.com/a/1190000012063374](https://segmentfault.com/a/1190000012063374)
>[https://www.cnblogs.com/sparkdev/p/8052522.html](https://www.cnblogs.com/sparkdev/p/8052522.html)
>[https://colobu.com/2018/05/15/Stop-and-remove-all-docker-containers-and-images/](https://colobu.com/2018/05/15/Stop-and-remove-all-docker-containers-and-images/)
>[https://cizixs.com/2017/08/04/docker-resources-limit/](https://cizixs.com/2017/08/04/docker-resources-limit/)

## docker 日志

[https://kevinguo.me/2017/07/06/Docker-configuring-logging-drivers/](https://kevinguo.me/2017/07/06/Docker-configuring-logging-drivers/)

## docker 跨平台镜像

[https://cloud.tencent.com/developer/article/1543689](https://cloud.tencent.com/developer/article/1543689)

## docker-compose

docker compose up 命令基于 docker-compose.yml 文件启动一个新容器。 它类似于在彼此顺序运行时运行 docker create 和 docker start。

```Bash
# 不指定容器名称或 ID，停止所有容器
docker compose stop
docker compose stop name0
docker compose stop id0
docker-compose --help
docker-compose -f /path/to/docker-compose.yml stop
docker-compose -f /path/to/docker-compose.yml up -d
```

## docker proxy

dockerd代理 ¶
在执行docker pull时，是由守护进程dockerd来执行。 因此，代理需要配在dockerd的环境中。 而这个环境，则是受systemd所管控，因此实际是systemd的配置。

sudo mkdir -p /etc/systemd/system/docker.service.d
sudo touch /etc/systemd/system/docker.service.d/proxy.conf
在这个proxy.conf文件（可以是任意*.conf的形式）中，添加以下内容：

[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080/"
Environment="HTTPS_PROXY=http://proxy.example.com:8080/"
Environment="NO_PROXY=localhost,127.0.0.1,.example.com"
其中，proxy.example.com:8080要换成可用的免密代理。 通常使用cntlm在本机自建免密代理，去对接公司的代理。 可参考《Linux下安装配置Cntlm代理》。

Container代理 ¶
在容器运行阶段，如果需要代理上网，则需要配置~/.docker/config.json。 以下配置，只在Docker 17.07及以上版本生效。

{
"proxies":
{
"default":
{
"httpProxy": "http://proxy.example.com:8080",
"httpsProxy": "http://proxy.example.com:8080",
"noProxy": "localhost,127.0.0.1,.example.com"
}
}
}
这个是用户级的配置，除了proxies，docker login等相关信息也会在其中。 而且还可以配置信息展示的格式、插件参数等。

此外，容器的网络代理，也可以直接在其运行时通过-e注入http_proxy等环境变量。 这两种方法分别适合不同场景。 config.json非常方便，默认在所有配置修改后启动的容器生效，适合个人开发环境。 在CI/CD的自动构建环境、或者实际上线运行的环境中，这种方法就不太合适，用-e注入这种显式配置会更好，减轻对构建、部署环境的依赖。 当然，在这些环境中，最好用良好的设计避免配置代理上网。

docker build代理 ¶
虽然docker build的本质，也是启动一个容器，但是环境会略有不同，用户级配置无效。 在构建时，需要注入http_proxy等参数。

docker build . \
--build-arg "HTTP_PROXY=http://proxy.example.com:8080/" \
--build-arg "HTTPS_PROXY=http://proxy.example.com:8080/" \
--build-arg "NO_PROXY=localhost,127.0.0.1,.example.com" \
-t your/image:tag
注意：无论是docker run还是docker build，默认是网络隔绝的。 如果代理使用的是localhost:3128这类，则会无效。 这类仅限本地的代理，必须加上--network host才能正常使用。 而一般则需要配置代理的外部IP，而且代理本身要开启gateway模式。

重启生效 ¶
代理配置完成后，reboot重启当然可以生效，但不重启也行。

docker build代理是在执行前设置的，所以修改后，下次执行立即生效。 Container代理的修改也是立即生效的，但是只针对以后启动的Container，对已经启动的Container无效。

dockerd 代理的修改比较特殊，它实际上是改systemd的配置，因此需要重载systemd并重启dockerd才能生效。

sudo systemctl daemon-reload
sudo systemctl restart docker