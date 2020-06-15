---
title: Nutch hello world
author: wiloon
type: post
date: 2015-01-06T04:00:00+00:00
url: /?p=7187
categories:
  - Uncategorized
tags:
  - Crawler
  - Nutch

---
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

<pre>&lt;property&gt;
<span id="line-2-1" class="anchor"></span> &lt;name&gt;http.agent.name&lt;/name&gt;
<span id="line-3-1" class="anchor"></span> &lt;value&gt;My Nutch Spider&lt;/value&gt;
<span id="line-4-1" class="anchor"></span>&lt;/property&gt;

Edit the file <tt class="backtick">conf/regex-urlfilter.txt</tt> and replace</pre>

<pre># accept anything else
<span id="line-2-2" class="anchor"></span>+.</pre>

<p class="line862">
  with a regular expression matching the domain you wish to crawl. For example, if you wished to limit the crawl to the <tt class="backtick">nutch.apache.org</tt> domain, the line should read:<span id="line-113" class="anchor"></span><span id="line-114" class="anchor"></span>
</p>

<pre><span id="line-1-7" class="anchor"></span> +^http://([a-z0-9]*\.)*nutch.apache.org/


Specify the GORA backend in $NUTCH_HOME/conf/nutch-site.xml

</pre>

<pre>&lt;property&gt;
<span id="line-2" class="anchor"></span> &lt;name&gt;storage.data.store.class&lt;/name&gt;
<span id="line-3" class="anchor"></span> &lt;value&gt;org.apache.gora.hbase.store.HBaseStore&lt;/value&gt;
<span id="line-4" class="anchor"></span> &lt;description&gt;Default class for storing data&lt;/description&gt;
<span id="line-5" class="anchor"></span>&lt;/property&gt;

</pre>

  * Ensure the HBase gora-hbase dependency is available in $NUTCH_HOME/ivy/ivy.xml<span id="line-26" class="anchor"></span><span id="line-27" class="anchor"></span>

<pre><span id="line-1-1" class="anchor"></span>    &lt;!-- Uncomment this to use HBase as Gora backend. --&gt;
<span id="line-2-1" class="anchor"></span>    
<span id="line-3-1" class="anchor"></span>    &lt;dependency org="org.apache.gora" name="gora-hbase" rev="0.4" conf="*-&gt;default" /&gt;

</pre>

  * <p class="line862">
      Ensure that HBaseStore is set as the default datastore in $NUTCH_HOME/conf/gora.properties. Other documentation for HBaseStore can be found <a class="http" href="http://gora.apache.org/current/gora-hbase.html">here</a>.<span id="line-34" class="anchor"></span><span id="line-35" class="anchor"></span>
    </p>

<pre><span id="line-1-2" class="anchor"></span>    gora.datastore.default=org.apache.gora.hbase.store.HBaseStore

</pre>

<pre>run ant runtime

config ssh for cygwin

http://hbase.apache.org/cygwin.html</pre>

start HBase



http://wiki.apache.org/nutch/NutchTutorial

http://wiki.apache.org/nutch/Nutch2Tutorial

http://hbase.apache.org/book/quickstart.html