---
title:  "etcd basic"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "etcd basic"

### 单节点的etcd

    podman run -d \
    -p 2379:2379 \
    -v etcd-data:/etcd-data \
    --add-host=localhost:127.0.0.1 \
    -e ETCD_DATA_DIR="/etcd-data" \
    -e ETCD_ENABLE_V2="true" \
    -e ALLOW_NONE_AUTHENTICATION="yes" \
    -e ETCD_ADVERTISE_CLIENT_URLS="http://0.0.0.0:2379" \
    -e ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379" \
    --name etcd bitnami/etcd:latest

### set, get

    etcdctl ls
    etcdctl set /testdir/testkey "foo"
    etcdctl get /testdir/testkey
    etcdctl update /testdir/testkey "Hello"
    etcdctl rm /testdir/testkey
    etcdctl mk /testdir/testkey "Hello world"
    etcdctl mkdir testdir2

[https://etcd.io/docs/v3.4.0/op-guide/container/](https://etcd.io/docs/v3.4.0/op-guide/container/)
[https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/container.md](https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/container.md)
