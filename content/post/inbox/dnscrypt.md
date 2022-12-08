---
title: dnscrypt
author: "-"
date: 2017-10-14T08:57:31+00:00
url: /?p=11265
categories:
  - Inbox
tags:
  - reprint
---
## dnscrypt
# Server

```bash
  
# https://github.com/Cofyc/dnscrypt-wrapper
  
# https://github.com/jedisct1/libsodium
  
# https://jedisct1.gitbooks.io/libsodium/content/
  
yum install gcc
  
# Install libsodium
  
wget https://download.libsodium.org/libsodium/releases/libsodium-1.0.16.tar.gz

./configure
  
make && make check
  
sudo make install

ln -s /usr/local/lib/libsodium.so.23.1.0 /usr/lib/libsodium.so.23
  
ldconfig # if you install libsodium from source

# install libevent
  
# http://libevent.org/
  
# https://geeksww.com/tutorials/operating_systems/linux/installation/how_to_install_libevent_on_debianubuntucentos_linux.php

wget https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz
  
tar xzf libevent-2.1.8-stable.tar.gz
  
cd libevent-2.1.8-stable
  
./configure -prefix=/opt/libevent
  
make
  
make install

# install dnscrypt-wrapper
  
git clone git://github.com/cofyc/dnscrypt-wrapper.git
  
cd dnscrypt-wrapper
  
make configure
  
./configure
  
make install

# set ip:port for dnscrypt on archlinux
  
systemctl edit dnscrypt-proxy.socket
  
https://wiki.archlinux.org/index.php/DNSCrypt_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

#start
  
sudo systemctl start dnscrypt-proxy.service

#stop
  
sudo systemctl stop dnscrypt-proxy.socket

#key, crt expired, recreate key, crt
  
dnscrypt-wrapper -gen-crypt-keypair -crypt-secretkey-file=1.key
  
dnscrypt-wrapper -gen-cert-file -crypt-secretkey-file=1.key -provider-cert-file=1.cert -provider-publickey-file=public.key -provider-secretkey-file=secret.key

dnscrypt-wrapper -gen-crypt-keypair -crypt-secretkey-file=1.key -cert-file-expire-days=365
  
dnscrypt-wrapper -gen-cert-file -crypt-secretkey-file=1.key -provider-cert-file=1.cert -provider-publickey-file=public.key -provider-secretkey-file=secret.key -cert-file-expire-days=365
  
#restart dnscrypt server
  
#restart dnscrypt client
  
```

sample config file for client
  
https://github.com/jedisct1/dnscrypt-proxy/blob/master/dnscrypt-proxy.conf

wget https://download.libsodium.org/libsodium/releases/libsodium-stable-2017-10-14.tar.gz
  
wget https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz

yum groupinstall "Development tools"

./configure
  
make && make check
  
sudo make install

echo "/usr/local/lib" >> /etc/ld.so.conf

# Client

dnscrypt-proxy

https://github.com/Cofyc/dnscrypt-wrapper
  
http://blog.csdn.net/sahusoft/article/details/7388617

http://www.jianshu.com/p/20b583c35f82
  
http://blog.hotwill.cn/2016/05/22/dnscrypt-proxy+dnsmasq搭建无污染DNS服务器.html
  
https://03k.org/dnscrypt-wrapper-usage.html
  
https://dnscrypt.org/#install-dnscrypt
  
https://03k.org/centos-make-dnscrypt-wrapper.html