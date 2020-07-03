---
title: linux tail
author: wiloon
type: post
date: 2016-08-14T15:41:25+00:00
url: /?p=9182
categories:
  - Uncategorized

---
<div class="line number10 index9 alt1">
  <code class="bash plain">http://www.qttc.net/201304311.html</code>

<div class="line number10 index9 alt1">

<div class="line number10 index9 alt1">
  <code class="bash plain">-f, --follow[={name|descriptor}]</code>

<div class="line number11 index10 alt2">
  <code class="bash spaces">                </code><code class="bash plain">即时输出文件变化后追加的数据。</code>

<div class="line number12 index11 alt1">
  <code class="bash spaces">                        </code><code class="bash plain">-f, --follow 等于--follow=descriptor </code>

<div class="line number13 index12 alt2">
  <code class="bash spaces">  </code><code class="bash plain">-F            即--follow=name --retry</code>

<div class="line number14 index13 alt1">
  <code class="bash spaces">  </code><code class="bash plain">-n, --lines=K            output the last K lines, instead of the last 10;</code>

<div class="line number15 index14 alt2">
  <code class="bash spaces">                           </code><code class="bash plain">or use -n +K to output lines starting with the Kth</code>

<div class="line number16 index15 alt1">
  <code class="bash spaces">      </code><code class="bash plain">--max-unchanged-stats=N</code>

<div class="line number17 index16 alt2">
  <code class="bash spaces">                           </code><code class="bash plain">with --follow=name, reopen a FILE </code><code class="bash functions">which</code> <code class="bash plain">has not</code>

<div class="line number18 index17 alt1">
  <code class="bash spaces">                           </code><code class="bash plain">changed size after N (default 5) iterations</code>

<div class="line number19 index18 alt2">
  <code class="bash spaces">                           </code><code class="bash plain">to see </code><code class="bash keyword">if</code> <code class="bash plain">it has been unlinked or renamed</code>

<div class="line number20 index19 alt1">
  <code class="bash spaces">                           </code><code class="bash plain">(this is the usual </code><code class="bash keyword">case</code> <code class="bash plain">of rotated log files).</code>

<div class="line number21 index20 alt2">
  <code class="bash spaces">                           </code><code class="bash plain">With inotify, this option is rarely useful.</code>

<div class="line number22 index21 alt1">
  <code class="bash spaces">      </code><code class="bash plain">--pid=PID         同 -f 一起使用，当 PID 所对应的进程死去后终止</code>
