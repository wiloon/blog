+++
author = "w1100n"
date = "2020-06-04T08:55:49Z"
title = "encletsrypt"

+++
**acme.sh** 实现了 `acme` 协议, 可以从 letsencrypt 生成免费的证书.

[https://github.com/acmesh-official/acme.sh/wiki/%E8%AF%B4%E6%98%8E](https://github.com/acmesh-official/acme.sh/wiki/%E8%AF%B4%E6%98%8E "https://github.com/acmesh-official/acme.sh/wiki/%E8%AF%B4%E6%98%8E")

    sudo pacman -S socat
    curl  https://get.acme.sh | sh
    sudo ~/.acme.sh/acme.sh --issue -d mydomain.me --standalone -k ec-256
    sudo ~/.acme.sh/acme.sh --installcert -d mydomain.me --fullchainpath /etc/v2ray/v2ray.crt --keypath /etc/v2ray/v2ray.key --ecc
    