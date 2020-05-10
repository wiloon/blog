---
title: docker mariadb
author: wiloon
type: post
date: 2018-12-27T04:50:21+00:00
url: /?p=13220
categories:
  - Uncategorized

---
<pre><code class="language-bash line-numbers">mkdir -p /data/mariadb
docker run -d --name mariadb -P -v /data/mariadb:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password0 mariadb
</code></pre>

https://www.jianshu.com/p/32542630c2bd