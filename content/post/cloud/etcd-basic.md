+++
author = "w1100n"
date = "2020-06-14T05:25:48Z"
title = "etcd basic"

+++

### 单节点的etcd
    export NODE1=192.168.97.1
    export DATA_DIR="etcd-data"
    podman volume create etcd-data
    
    REGISTRY=gcr.io/etcd-development/etcd

    podman run -d \
    -p 2379:2379 \
    -p 2380:2380 \
    --volume=${DATA_DIR}:/etcd-data \
    --name etcd ${REGISTRY}:latest \
    /usr/local/bin/etcd \
    --data-dir=/etcd-data --name node1 \
    --initial-advertise-peer-urls http://${NODE1}:2380 --listen-peer-urls http://0.0.0.0:2380 \
    --advertise-client-urls http://${NODE1}:2379 --listen-client-urls http://0.0.0.0:2379 \
    --initial-cluster node1=http://${NODE1}:2380


### set, get
    etcdctl ls
    etcdctl set /testdir/testkey "foo"
    etcdctl get /testdir/testkey
    etcdctl update /testdir/testkey "Hello"
    etcdctl rm /testdir/testkey
    etcdctl mk /testdir/testkey "Hello world"
    etcdctl mkdir testdir2


https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/container.md

