---
title: 'database DDL > puml'
author: wiloon
type: post
date: 2019-04-29T08:14:42+00:00
url: /?p=14270
categories:
  - Uncategorized

---
https://github.com/wangyuheng/ddl2plantuml

<pre><code class="language-bash line-numbers">java -jar ~/apps/ddl2plantuml.jar foo.sql er.puml
</code></pre>

<pre><code class="language-bash line-numbers">docker run \
-e DDL='/mnt/data/ddl.sql' \
-e PLANTUML='/mnt/data/er_by_docker.puml' \
-v ddl2plantuml-data:'/mnt/data' \
wangyuheng/ddl2plantuml:latest
</code></pre>