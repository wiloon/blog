---
title: Nutch hello world
author: "-"
date: 2015-01-06T04:00:00+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: nutch-hello-world
categories:
  - Tools
tags:
  - Crawler
  - Nutch
  - remix
  - AI-assisted
aliases:
  - /p7187/
---
## Nutch hello world

download and install ant

download and install Cygwin

download HBase 0.94.14

http://mirrors.cnnic.cn/apache/hbase/stable/hbase-0.98.9-hadoop2-bin.tar.gz

config java_home in .bashrc

Download a source package

http://mirror.bit.edu.cn/apache/nutch/2.2.1/

```bash
cd apache-nutch-2.2.1
```

Run `ant`

Now there is a directory `runtime/local` which contains a ready to use Nutch installation.

### Customize your crawl properties {#A3.1_Customize_your_crawl_properties}

Add your agent name in the `value` field of the `http.agent.name` property in `conf/nutch-site.xml`, for example:

```xml
<property>
 <name>http.agent.name</name>
 <value>My Nutch Spider</value>
</property>
```

Edit the file `conf/regex-urlfilter.txt` and replace

```text
# accept anything else
+.
```

with a regular expression matching the domain you wish to crawl. For example, if you wished to limit the crawl to the `nutch.apache.org` domain, the line should read:

```text
+^http://([a-z0-9]*\.)*nutch.apache.org/
```

Specify the GORA backend in `$NUTCH_HOME/conf/nutch-site.xml`

```xml
<property>
 <name>storage.data.store.class</name>
 <value>org.apache.gora.hbase.store.HBaseStore</value>
 <description>Default class for storing data</description>
</property>
```

- Ensure the HBase gora-hbase dependency is available in `$NUTCH_HOME/ivy/ivy.xml`

  ```xml
  <!-- Uncomment this to use HBase as Gora backend. -->
  <dependency org="org.apache.gora" name="gora-hbase" rev="0.4" conf="*->default" />
  ```

- Ensure that HBaseStore is set as the default datastore in `$NUTCH_HOME/conf/gora.properties`. Other documentation for HBaseStore can be found here.

  ```properties
  gora.datastore.default=org.apache.gora.hbase.store.HBaseStore
  ```

run ant runtime

config ssh for cygwin

http://hbase.apache.org/cygwin.html

start HBase

http://wiki.apache.org/nutch/NutchTutorial

http://wiki.apache.org/nutch/Nutch2Tutorial

http://hbase.apache.org/book/quickstart.html

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Tools | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
