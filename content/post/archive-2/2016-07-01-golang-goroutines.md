---
title: Golang goroutines
author: wiloon
type: post
date: 2016-07-01T09:20:33+00:00
url: /?p=9101
categories:
  - Uncategorized

---
http://eleme.io/blog/2014/goroutine-1/



goroutine

Go语言中有个概念叫做goroutine, 这类似我们熟知的线程，但是更轻。

以下的程序，我们串行地去执行两次`loop`函数:

<div class="highlight">
  <pre><code class="language-go" data-lang="go">&lt;span class="kd">func&lt;/span> &lt;span class="nx">loop&lt;/span>&lt;span class="p">()&lt;/span> &lt;span class="p">{&lt;/span>
    &lt;span class="k">for&lt;/span> &lt;span class="nx">i&lt;/span> &lt;span class="o">:=&lt;/span> &lt;span class="mi">0&lt;/span>&lt;span class="p">;&lt;/span> &lt;span class="nx">i&lt;/span> &lt;span class="p">&lt;&lt;/span> &lt;span class="mi">10&lt;/span>&lt;span class="p">;&lt;/span> &lt;span class="nx">i&lt;/span>&lt;span class="o">++&lt;/span> &lt;span class="p">{&lt;/span>
        &lt;span class="nx">fmt&lt;/span>&lt;span class="p">.&lt;/span>&lt;span class="nx">Printf&lt;/span>&lt;span class="p">(&lt;/span>&lt;span class="s">"%d "&lt;/span>&lt;span class="p">,&lt;/span> &lt;span class="nx">i&lt;/span>&lt;span class="p">)&lt;/span>
    &lt;span class="p">}&lt;/span>
&lt;span class="p">}&lt;/span>


&lt;span class="kd">func&lt;/span> &lt;span class="nx">main&lt;/span>&lt;span class="p">()&lt;/span> &lt;span class="p">{&lt;/span>
    &lt;span class="nx">loop&lt;/span>&lt;span class="p">()&lt;/span>
    &lt;span class="nx">loop&lt;/span>&lt;span class="p">()&lt;/span>
&lt;span class="p">}&lt;/span>
```
</div>

毫无疑问，输出会是这样的:

<div class="highlight">
  <pre><code class="language-text" data-lang="text">0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9
```
</div>

下面我们把一个loop放在一个goroutine里跑，我们可以使用关键字`go`来定义并启动一个goroutine:

<div class="highlight">
  <pre><code class="language-go" data-lang="go">&lt;span class="kd">func&lt;/span> &lt;span class="nx">main&lt;/span>&lt;span class="p">()&lt;/span> &lt;span class="p">{&lt;/span>
    &lt;span class="k">go&lt;/span> &lt;span class="nx">loop&lt;/span>&lt;span class="p">()&lt;/span> &lt;span class="c1">// 启动一个goroutine&lt;/span>
    &lt;span class="nx">loop&lt;/span>&lt;span class="p">()&lt;/span>
&lt;span class="p">}&lt;/span>
```
</div>

这次的输出变成了:

<div class="highlight">
  <pre><code class="language-text" data-lang="text">0 1 2 3 4 5 6 7 8 9
```
</div>

可是为什么只输出了一趟呢？明明我们主线跑了一趟，也开了一个goroutine来跑一趟啊。

原来，在goroutine还没来得及跑loop的时候，主函数已经退出了。

main函数退出地太快了，我们要想办法阻止它过早地退出，一个办法是让main等待一下:

<div class="highlight">
  <pre><code class="language-go" data-lang="go">&lt;span class="kd">func&lt;/span> &lt;span class="nx">main&lt;/span>&lt;span class="p">()&lt;/span> &lt;span class="p">{&lt;/span>
    &lt;span class="k">go&lt;/span> &lt;span class="nx">loop&lt;/span>&lt;span class="p">()&lt;/span>
    &lt;span class="nx">loop&lt;/span>&lt;span class="p">()&lt;/span>
    &lt;span class="nx">time&lt;/span>&lt;span class="p">.&lt;/span>&lt;span class="nx">Sleep&lt;/span>&lt;span class="p">(&lt;/span>&lt;span class="nx">time&lt;/span>&lt;span class="p">.&lt;/span>&lt;span class="nx">Second&lt;/span>&lt;span class="p">)&lt;/span> &lt;span class="c1">// 停顿一秒&lt;/span>
&lt;span class="p">}&lt;/span>
```
</div>

这次确实输出了两趟，目的达到了。



同步并发的原理是利用进程或者线程，由操作系统调度；异步并发的原理是DMA，即不经过CPU直接把IO的某一快copy到memory上或者反之



https://www.zhihu.com/question/20862617