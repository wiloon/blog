+++
author = "w1100n"
date = "2020-07-08 13:04:06"
title = "apisix"

+++

### Create a network apisix
    podman network create \
    --driver=bridge \
    --subnet=172.18.0.0/16 \
    --ip-range=172.18.5.0/24 \
    --gateway=172.18.5.254 \
    apisix

### Run etcd server with apisix network

    podman run -it --name etcd-server \
    -v `pwd`/example/etcd_conf/etcd.conf.yml:/opt/bitnami/etcd/conf/etcd.conf.yml \
    -p 2379:2379 \
    -p 2380:2380  \
    --network apisix \
    --ip 172.18.5.10 \
    --env ALLOW_NONE_AUTHENTICATION=yes bitnami/etcd:3.3.13-r80