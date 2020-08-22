+++
author = "w1100n"
date = "2020-08-22 23:05:10" 
title = "certbot"

+++

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
        certbot-auto certonly  -d *.wiloon.com --manual --preferred-challenges dns --dry-run  --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"

### run
        certbot-auto certonly  -d *.wiloon.com --manual --preferred-challenges dns  --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"

### renew 所有证书
        certbot-auto renew  --manual --manual-public-ip-logging-ok --preferred-challenges dns --manual-auth-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly add" --manual-cleanup-hook "/root/certbot-letencrypt-wildcardcertificates-alydns-au/au.sh python aly clean"

### renew 某一个证书
    certbot-auto renew --cert-name simplehttps.com  --manual-auth-hook "/脚本目录/au.sh php aly add" --manual-cleanup-hook "/脚本目录/au.sh php aly clean"
### check cert
    certbot-auto certificates

### 加入 crontab
    1 1 */1 * * root certbot-auto renew --manual --preferred-challenges dns  --manual-auth-hook "/脚本目录/au.sh php aly add" --manual-cleanup-hook "/脚本目录/au.sh php aly clean"
    
https://certbot.eff.org/docs/install.html#certbot-auto
https://github.com/ywdblog/certbot-letencrypt-wildcardcertificates-alydns-au