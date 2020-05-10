---
title: Java cpu占用调查
author: wiloon
type: post
date: 2015-12-23T01:44:52+00:00
url: /?p=8587
categories:
  - Uncategorized

---
  1. jps 获取Java进程的PID。

<pre><code class="language-bash line-numbers">jcmd -l
</code></pre>

<ol start="2">
  <li>
    导出CPU占用高进程的线程栈。
  </li>
</ol>

<pre><code class="language-bash line-numbers">jstack &lt;PID&gt; stack.txt
# 或
jcmd &lt;PID&gt; Thread.print &gt;&gt; stack.txt
</code></pre>

<ol start="3">
  <li>
    查看对应进程的哪个线程占用CPU过高.
  </li>
</ol>

<pre><code class="language-bash line-numbers">top -H -p &lt;PID&gt;
ps -mp &lt;PID&gt; -o THREAD,tid,time | sort -rn | head -n 10
</code></pre>

<ol start="4">
  <li>
    将线程的PID转换为16进制。
  </li>
</ol>

<pre><code class="language-bash line-numbers">echo "obase=16; PID" | bc
printf "%x\n" 73658
</code></pre>

<ol start="5">
  <li>
    在第二步导出的 stack.txt 中查找转换成为16进制的线程PID。找到对应的线程栈。
  </li>
  <li>
    分析负载高的线程栈都是什么业务操作。优化程序并处理问题。
  </li>
</ol>

SystemTap，LatencyTOP，vmstat, sar, iostat, top, tcpdump
  
iftop, iptraf, ntop, tcpdump
  
Java的JProfiler/TPTP/CodePro Profiler

<blockquote class="wp-embedded-content" data-secret="sGuaIXdcl5">
  <p>
    <a href="https://coolshell.cn/articles/7490.html">性能调优攻略</a>
  </p>
</blockquote>

<iframe title="《性能调优攻略》—酷 壳 - CoolShell" class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="https://coolshell.cn/articles/7490.html/embed#?secret=sGuaIXdcl5" data-secret="sGuaIXdcl5" width="600" height="338" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>
  
<https://www.linuxhot.com/java-cpu-used-high.html>
  
<https://linux.cn/article-5633-1.html>