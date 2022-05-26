---
title: "letsencrypt, certbot, certbot-auto, acme.sh"
author: "-"
date: "2020-06-04T08:55:49Z"
url: ""
categories:
  - Security
tags:
  - remix

---
## "letsencrypt, certbot, certbot-auto, acme.sh"

### certbot, certbot-auto, acme.sh

certbot: recommended by the offical website.
certbot-auto: no longer supported.
acme.sh: 第三方实现的 acme 协议.

## certbot aliyun plugin

<https://github.com/tengattack/certbot-dns-aliyun>

<https://eff-certbot.readthedocs.io/en/stable/using.html#setting-up-automated-renewal>

```bash
pacman -S python-pip

pip install certbot-dns-aliyun
# certbot will be installed automaticaly

vim credentials.ini

dns_aliyun_access_key = 12345678
dns_aliyun_access_key_secret = 1234567890abcdef1234567890abcdef

certbot certonly -a dns-aliyun \
    --certbot-dns-aliyun:dns-aliyun-credentials /root/credentials.ini \
    -d wiloon.com \
    -d "*.wiloon.com"

ls /etc/letsencrypt/live/wiloon.com/
# add to crontab
0 0,12 * * * certbot renew

```

### install certbot

#### centos

```bash
dnf update
dnf remove certbot
dnf install epel-release
dnf install snapd
systemctl enable --now snapd.socket
snap install core
snap refresh core
ln -s /var/lib/snapd/snap /snap
snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot
snap set certbot trust-plugin-with-root=ok
snap install certbot-dns-google
```

#### ubuntu

```bash
    # for ubuntu snap is pre-installed
    sudo apt-get remove certbot
    sudo snap install --classic certbot
    sudo ln -s /snap/bin/certbot /usr/bin/certbot
    snap set certbot trust-plugin-with-root=ok
    snap install certbot-dns-google
```

### certonly

    certbot certonly   --dns-google   --dns-google-credentials /root/cellular-deck-280204-6455aa19691d.json -d wiloon.com -d *.wiloon.com

### Couldn't download <https://raw.githubusercontent.com/certbot/certbot/v0.39.0/letsencrypt-auto-source/letsencrypt-auto>. <urlopen error [Errno 110] Connection timed out>

如果希望将其锁定到特定版本并且不接收自动更新，只需在命令后加 --no-self-upgrade 即可。即:
certbot-auto renew --no-self-upgrade

<https://certbot.eff.org/docs/intro.html>

因为 Google Chrome 和运营商劫持干扰访问者体验的努力推动了大型网站加速应用全站 HTTPS，而 Let’s Encrypt 这个项目通过自动化把配置和维护 HTTPS 变得更加简单，Let’s Encrypt 设计了一个 ACME 协议目前版本是 v2，并在 2018 年支持通配符证书 Wildcard Certificate Support is Live。  
官网主推的客户端是Certbot，任何人都可以基于 ACME 协议实现一个客户端，比如大名鼎鼎的acme.sh。

### 安装 certbot

        sudo apt install certbot

alternatives --set python /usr/bin/python3

### ubuntu

        $ sudo apt update
        $ sudo apt install snapd
        sudo snap install core; sudo snap refresh core
        sudo apt-get remove certbo
        sudo snap install --classic certbot

### google dns

    certbot certonly   --dns-google   --dns-google-credentials /root/cellular-deck-280204-6455aa19691d.json -d wangyue.dev -d *.wangyue.dev

### aliyun
<https://github.com/tengattack/certbot-dns-aliyun>

    sudo dnf install python3
    pip3 install certbot-dns-aliyun

    certbot certonly -a dns-aliyun \
    --certbot-dns-aliyun:dns-aliyun-credentials /root/apps/credentials.ini \
    -d wiloon.com \
    -d "*.wiloon.com"

---

### dry run

        certbot-auto certonly  -d wiloon.com -d *.wiloon.com --manual --preferred-challenges dns --dry-run  --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"

### run

        certbot-auto certonly  -d wiloon.com -d *.wiloon.com --manual --preferred-challenges dns  --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"

### renew 所有证书

        certbot-auto renew --no-self-upgrade --manual-public-ip-logging-ok

        certbot-auto renew  --manual --manual-public-ip-logging-ok --preferred-challenges dns --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"

### renew 某一个证书

    certbot-auto renew --cert-name simplehttps.com  --manual-auth-hook "/脚本目录/au.sh php aly add" --manual-cleanup-hook "/脚本目录/au.sh php aly clean"

### check cert

    certbot-auto certificates --no-self-upgrade

能看到有两个证书

        /etc/letsencrypt/live/wiloon.com-0001/fullchain.pem -- *.wiloon.com 泛域名证书
        /etc/letsencrypt/live/wiloon.com/fullchain.pem -- wiloon.com blog.wiloon.com

### 加入 crontab

    1 1 */1 * * certbot-auto renew  --manual --manual-public-ip-logging-ok --preferred-challenges dns --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"

<https://certbot.eff.org/docs/install.html#certbot-auto>
<https://github.com/ywdblog/certbot-letencrypt-wildcardcertificates-alydns-au>

### acme.sh

acme.sh 实现了 `acme` 协议, 可以从 letsencrypt 生成免费的证书.

    https://github.com/acmesh-official/acme.sh/wiki/%E8%AF%B4%E6%98%8E

    sudo pacman -S socat
    curl  https://get.acme.sh | sh
    sudo ~/.acme.sh/acme.sh --issue -d mydomain.me --standalone -k ec-256
    sudo ~/.acme.sh/acme.sh --installcert -d mydomain.me --fullchainpath /etc/v2ray/v2ray.crt --keypath /etc/v2ray/v2ray.key --ecc

<https://github.com/acmesh-official/acme.sh/wiki/%E8%AF%B4%E6%98%8E>
acme.sh 实现了 acme 协议, 可以从 letsencrypt 生成免费的证书.

---
<https://wsgzao.github.io/post/certbot/>
<https://certbot-dns-google.readthedocs.io/en/stable/>
