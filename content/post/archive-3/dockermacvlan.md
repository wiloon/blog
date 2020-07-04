https://ctimbai.github.io/2019/04/14/tech/docker-macvlan/
https://mp.weixin.qq.com/s?__biz=MzI1OTY2MzMxOQ==&mid=2247485246&idx=1&sn=c42a3618c357ebf5f6b7b7ce78ae568f&chksm=ea743386dd03ba90ad65940321385f68f9315fec16d82a08efa12c18501d8cadf95cf9e614a2&scene=21#wechat_redirect

```bash
# docker network create -d macvlan --subnet=172.16.10.0/24 --gateway=172.16.10.1 -o parent=enp0s8 mac1
podman network create --subnet=192.168.50.0/24 --gateway=192.168.50.1 --macvlan=enp1s0 mac1

-d 指定 Docker 网络 driver
--subnet 指定 macvlan 网络所在的网络
--gateway 指定网关
-o parent 指定用来分配 macvlan 网络的物理网卡
 cat /etc/cni/net.d/mac1.conflist
```

在 host1 运行容器 c1，并指定使用 macvlan 网络：
```bash
podman run -itd --name c1 --ip=192.168.50.99 --network mac1 busybox
```

https://stackoverflow.com/questions/59515026/how-do-i-replicate-a-docker-macvlan-network-with-podman

### podman 
http://docs.podman.io/en/latest/


---

https://github.com/containernetworking/plugins
