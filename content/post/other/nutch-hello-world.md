---
title: Nutch hello world
author: "-"
date: 2015-01-06T04:00:00+00:00
url: /?p=7187
categories:
  - Uncategorized
tags:
  - Crawler
  - Nutch

---
## Nutch hello world
download and install ant

download and install Cygwin

download HBase 0.94.14

http://mirrors.cnnic.cn/apache/hbase/stable/hbase-0.98.9-hadoop2-bin.tar.gz


config java_home in .bashrc

Download a source package

http://mirror.bit.edu.cn/apache/nutch/2.2.1/

cd apache-nutch-2.2.1

Run <tt class="backtick">ant

Now there is a directory <tt class="backtick">runtime/local which contains a ready to use Nutch installation.

### Customize your crawl properties {#A3.1_Customize_your_crawl_properties}

Add your agent name in the <tt class="backtick">value field of the <tt class="backtick">http.agent.name property in <tt class="backtick">conf/nutch-site.xml, for example:

<property>
 <name>http.agent.name</name>
 <value>My Nutch Spider</value>
</property>

Edit the file <tt class="backtick">conf/regex-urlfilter.txt and replace

# accept anything else
+.


  with a regular expression matching the domain you wish to crawl. For example, if you wished to limit the crawl to the <tt class="backtick">nutch.apache.org domain, the line should read:

 +^http://([a-z0-9]*\.)*nutch.apache.org/

Specify the GORA backend in $NUTCH_HOME/conf/nutch-site.xml


<property>
 <name>storage.data.store.class</name>
 <value>org.apache.gora.hbase.store.HBaseStore</value>
 <description>Default class for storing data</description>
</property>


  * Ensure the HBase gora-hbase dependency is available in $NUTCH_HOME/ivy/ivy.xml

    <!-- Uncomment this to use HBase as Gora backend. -->
    
    <dependency org="org.apache.gora" name="gora-hbase" rev="0.4" conf="*->default" />


  * 
      Ensure that HBaseStore is set as the default datastore in $NUTCH_HOME/conf/gora.properties. Other documentation for HBaseStore can be found here.
    

    gora.datastore.default=org.apache.gora.hbase.store.HBaseStore


run ant runtime

config ssh for cygwin

http://hbase.apache.org/cygwin.html

start HBase


http://wiki.apache.org/nutch/NutchTutorial

http://wiki.apache.org/nutch/Nutch2Tutorial

http://hbase.apache.org/book/quickstart.html