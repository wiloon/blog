---
title: nginx command, docker
author: wiloon
type: post
date: 2017-10-26T06:17:15+00:00
url: /?p=11308
categories:
  - Uncategorized

---
<pre><code class="language-bash line-numbers"># Do not run, just test the configuration file.
sudo nginx -t

nginx -s signal

# stop — fast shutdown
# quit — graceful shutdown
# reload — reloading the configuration file
# reopen — reopening the log files
</code></pre>

<pre><code class="language-bash line-numbers"># install
# docker
docker run -d \
--name nginx \
-p 80:80 \
-p 443:443 \
-v nginx-config:/etc/nginx \
-v certbot-conf:/etc/letsencrypt \
-v nginx-www:/var/www \
-v /etc/localtime:/etc/localtime:ro \
--restart=always \
nginx

# podman
podman run -d \
--name nginx \
-p 80:80 \
-p 443:443 \
-v nginx-config:/etc/nginx \
-v certbot-conf:/etc/letsencrypt \
-v nginx-www:/var/www \
-v /etc/localtime:/etc/localtime:ro \
nginx

# nginx config text
docker run --name nginx-config-test --rm -t -a stdout -v nginx-conf:/etc/nginx:ro nginx nginx -c /etc/nginx/nginx.conf -t

# archlinux, mainline branch: new features, updates, bugfixes
sudo pacman -S nginx-mainline

# start
sudo systemctl start nginx

# restart
kill -HUP pid

#stop
kill -s QUIT 1628
</code></pre>