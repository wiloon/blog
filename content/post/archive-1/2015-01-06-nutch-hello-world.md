---
title: Nutch hello world
author: "-"
type: post
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

download HBase 0.94.14

http://mirrors.cnnic.cn/apache/hbase/stable/hbase-0.98.9-hadoop2-bin.tar.gz


config java_home in .bashrc

Download a source package

http://mirror.bit.edu.cn/apache/nutch/2.2.1/

cd apache-nutch-2.2.1

Run <tt class="backtick">ant</tt>

Now there is a directory <tt class="backtick">runtime/local</tt> which contains a ready to use Nutch installation.

### Customize your crawl properties {#A3.1_Customize_your_crawl_properties}

Add your agent name in the <tt class="backtick">value</tt> field of the <tt class="backtick">http.agent.name</tt> property in <tt class="backtick">conf/nutch-site.xml</tt>, for example:

<property>
<span id="line-2-1" class="anchor"> <name>http.agent.name</name>
<span id="line-3-1" class="anchor"> <value>My Nutch Spider</value>
<span id="line-4-1" class="anchor"></property>

Edit the file <tt class="backtick">conf/regex-urlfilter.txt</tt> and replace

# accept anything else
<span id="line-2-2" class="anchor">+.


  with a regular expression matching the domain you wish to crawl. For example, if you wished to limit the crawl to the <tt class="backtick">nutch.apache.org</tt> domain, the line should read:<span id="line-113" class="anchor"><span id="line-114" class="anchor">

<span id="line-1-7" class="anchor"> +^http://([a-z0-9]*\.)*nutch.apache.org/

Specify the GORA backend in $NUTCH_HOME/conf/nutch-site.xml


<property>
<span id="line-2" class="anchor"> <name>storage.data.store.class</name>
<span id="line-3" class="anchor"> <value>org.apache.gora.hbase.store.HBaseStore</value>
<span id="line-4" class="anchor"> <description>Default class for storing data</description>
<span id="line-5" class="anchor"></property>


  * Ensure the HBase gora-hbase dependency is available in $NUTCH_HOME/ivy/ivy.xml<span id="line-26" class="anchor"><span id="line-27" class="anchor">

<span id="line-1-1" class="anchor">    <!-- Uncomment this to use HBase as Gora backend. -->
<span id="line-2-1" class="anchor">    
<span id="line-3-1" class="anchor">    <dependency org="org.apache.gora" name="gora-hbase" rev="0.4" conf="*->default" />


  * 
      Ensure that HBaseStore is set as the default datastore in $NUTCH_HOME/conf/gora.properties. Other documentation for HBaseStore can be found here.<span id="line-34" class="anchor"><span id="line-35" class="anchor">
    

<span id="line-1-2" class="anchor">    gora.datastore.default=org.apache.gora.hbase.store.HBaseStore


run ant runtime

config ssh for cygwin

http://hbase.apache.org/cygwin.html

start HBase


http://wiki.apache.org/nutch/NutchTutorial

http://wiki.apache.org/nutch/Nutch2Tutorial

http://hbase.apache.org/book/quickstart.html