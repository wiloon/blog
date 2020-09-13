+++
author = "w1100n"
date = "2020-06-04T08:55:49Z"
title = "letsencrypt, certbot, acme.sh"

+++
因为 Google Chrome 和运营商劫持干扰访问者体验的努力推动了大型网站加速应用全站 HTTPS，而 Let’s Encrypt 这个项目通过自动化把配置和维护 HTTPS 变得更加简单，Let’s Encrypt 设计了一个 ACME 协议目前版本是 v2，并在 2018 年支持通配符证书 Wildcard Certificate Support is Live。官网主推的客户端是Certbot，任何人都可以基于 ACME 协议实现一个客户端，比如大名鼎鼎的acme.sh。

### 安装 certbot
        sudo dnf install certbot

### 安装 certbot-auto
        wget https://dl.eff.org/certbot-auto
        sudo mv certbot-auto /usr/local/bin/certbot-auto
        sudo chown root /usr/local/bin/certbot-auto
        sudo chmod 0755 /usr/local/bin/certbot-auto
        /usr/local/bin/certbot-auto --help

alternatives --set python /usr/bin/python3

### dry run
        certbot-auto certonly  -d wiloon.com -d *.wiloon.com --manual --preferred-challenges dns --dry-run  --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"

### run
        certbot-auto certonly  -d wiloon.com -d *.wiloon.com --manual --preferred-challenges dns  --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"

### renew 所有证书
        certbot-auto renew  --manual --manual-public-ip-logging-ok --preferred-challenges dns --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"

### renew 某一个证书
    certbot-auto renew --cert-name simplehttps.com  --manual-auth-hook "/脚本目录/au.sh php aly add" --manual-cleanup-hook "/脚本目录/au.sh php aly clean"
### check cert
    certbot-auto certificates
能看到有两个证书

        /etc/letsencrypt/live/wiloon.com-0001/fullchain.pem -- *.wiloon.com 泛域名证书
        /etc/letsencrypt/live/wiloon.com/fullchain.pem -- wiloon.com blog.wiloon.com

### 加入 crontab
    1 1 */1 * * certbot-auto renew  --manual --manual-public-ip-logging-ok --preferred-challenges dns --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"


https://certbot.eff.org/docs/install.html#certbot-auto
https://github.com/ywdblog/certbot-letencrypt-wildcardcertificates-alydns-au

**acme.sh** 实现了 `acme` 协议, 可以从 letsencrypt 生成免费的证书.

    https://github.com/acmesh-official/acme.sh/wiki/%E8%AF%B4%E6%98%8E

    sudo pacman -S socat
    curl  https://get.acme.sh | sh
    sudo ~/.acme.sh/acme.sh --issue -d mydomain.me --standalone -k ec-256
    sudo ~/.acme.sh/acme.sh --installcert -d mydomain.me --fullchainpath /etc/v2ray/v2ray.crt --keypath /etc/v2ray/v2ray.key --ecc
    
https://github.com/acmesh-official/acme.sh/wiki/%E8%AF%B4%E6%98%8E
acme.sh 实现了 acme 协议, 可以从 letsencrypt 生成免费的证书.

---
https://wsgzao.github.io/post/certbot/
