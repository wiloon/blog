---
title: nextcloud
author: wiloon
type: post
date: 2019-01-26T05:27:32+00:00
url: /?p=13451
categories:
  - Uncategorized

---
<pre><code class="language-bash line-numbers">docker run -d \
--name nextcloud \
-p 2000:80 \
-v /etc/localtime:/etc/localtime:ro \
-v nextcloud:/var/www/html \
--restart=always \
nextcloud

#podman
podman run -d \
--name nextcloud \
-p 2000:80 \
-v /etc/localtime:/etc/localtime:ro \
-v nextcloud:/var/www/html \
nextcloud

</code></pre>

home-port: 63585

nginx代理nextcloud时， nextcloud需要配置

<pre><code class="language-bash line-numbers">'trusted_proxies'   =&gt; ['127.0.0.1'],
'overwritehost'     =&gt; 'xxx.wiloon.com',
'overwriteprotocol' =&gt; 'https',
'overwritewebroot'  =&gt; '/',
'overwritecondaddr' =&gt; '^127\.0\.0\.1$',
</code></pre>