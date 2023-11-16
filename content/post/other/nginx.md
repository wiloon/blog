---
title: Nginx
author: "-"
date: 2013-07-17T04:40:17+00:00
url: nginx
categories:
  - web
tags:
  - reprint
---
## Nginx

Nginx 是十分轻量级的 HTTP 服务器, Nginx, 它的发音为 "engine X", 是一个高性能的 HTTP 和反向代理服务器, 同时也是一个 IMAP/POP3/SMTP 代理服务器。 Nginx 是由俄罗斯人 Igor Sysoev 为俄罗斯访问量第二的 Rambler.ru 站点开发的。Igor Sysoev 在建立的项目时,使用基于 BSD 许可。

Nginx 以事件驱动的方式编写,所以有非常好的性能,同时也是一个非常高效的反向代理、负载平衡。其拥有匹配 Lighttpd 的性能,同时还没有 Lighttpd 的内存泄漏问题,而且 Lighttpd 的 mod_proxy 也有一些问题并且很久没有更新。

现在, Igor 将源代码以类 BSD 许可证的形式发布。Nginx 因为它的稳定性、丰富的模块库、灵活的配置和低系统资源的消耗而闻名．业界一致认为它是 Apache2.2+mod_proxy_balancer 的轻量级代替者,不仅是因为响应静态页面的速度非常快,而且它的模块数量达到 Apache 的近 2/3。对 proxy 和 rewrite 模块的支持很彻底,还支持 mod_fcgi、ssl、vhosts ,适合用来做 mongrel clusters 的前端 HTTP 响应。

Nginx 具有很高的稳定性。其它 HTTP 服务器,当遇到访问的峰值, 或者有人恶意发起慢速连接时,也很可能会导致服务器物理内存耗尽频繁交换, 失去响应,只能重启服务器。例如当前 apache 一旦上到 200 个以上进程,web响应速度就明显非常缓慢了。而 Nginx 采取了分阶段资源分配技术,使得它的 CPU 与内存占用率非常低。Nginx 官方表示保持 10,000 个没有活动的连接,它只占 2.5M 内存,所以类似 DOS 这样的攻击对 Nginx 来说基本上是毫无用处的。就稳定性而言,Nginx 比 lighthttpd 更胜一筹。
  
Nginx 支持热部署。它的启动特别容易, 并且几乎可以做到 7*24 不间断运行,即使运行数个月也不需要重新启动。你还能够在不间断服务的情况下,对软件版本进行升级。
  
Nginx 在启动后,在 unix 系统中会以 daemon 的方式在后台运行,后台进程包含一个 master 进程和多个 worker 进程。我们也可以手动地关掉后台模式,让 Nginx 在前台运行,并且通过配置让 Nginx 取消 master 进程,从而可以使 Nginx 以单进程方式运行。很显然,生产环境下我们肯定不会这么做,所以关闭后台模式,一般是用来调试用的,在后面的章节里面,我们会详细地讲解如何调试 Nginx。所以,我们可以看到,Nginx 是以多进程的方式来工作的,当然 Nginx 也是支持多线程的方式的,只是我们主流的方式还是多进程的方式,也是 Nginx 的默认方式。Nginx 采用多进程的方式有诸多好处
  
Nginx 在启动后,会有一个 master 进程和多个 worker 进程。master 进程主要用来管理 worker 进程,包含: 接收来自外界的信号,向各 worker 进程发送信号,监控 worker 进程的运行状态,当 worker 进程退出后(异常情况下),会自动重新启动新的 worker 进程。而基本的网络事件,则是放在 worker 进程中来处理了。多个 worker 进程之间是对等的,他们同等竞争来自客户端的请求,各进程互相之间是独立的。一个请求,只可能在一个 worker 进程中处理,一个 worker 进程,不可能处理其它进程的请求。worker 进程的个数是可以设置的,一般我们会设置与机器cpu核数一致,这里面的原因与 Nginx 的进程模型以及事件处理模型是分不开的。
  
在 Nginx 启动后,如果我们要操作 Nginx,要怎么做呢？从上文中我们可以看到,master 来管理 worker 进程,所以我们只需要与 master 进程通信就行了。master 进程会接收来自外界发来的信号,再根据信号做不同的事情。所以我们要控制 Nginx,只需要通过 kill 向 master 进程发送信号就行了。比如kill -HUP pid,则是告诉 Nginx,从容地重启 Nginx,我们一般用这个信号来重启 Nginx,或重新加载配置,因为是从容地重启,因此服务是不中断的。master 进程在接收到 HUP 信号后是怎么做的呢？首先 master 进程在接到信号后,会先重新加载配置文件,然后再启动新的 worker 进程,并向所有老的 worker 进程发送信号,告诉他们可以光荣退休了。新的 worker 在启动后,就开始接收新的请求,而老的 worker 在收到来自 master 的信号后,就不再接收新的请求,并且在当前进程中的所有未处理完的请求处理完成后,再退出。当然,直接给 master 进程发送信号,这是比较老的操作方式,Nginx 在 0.8 版本之后,引入了一系列命令行参数,来方便我们管理。

比如, ./nginx -s reload, 就是来重新加载 Nginx 配置, ./nginx -s stop, 就是来停止 Nginx 的运行。 如何做到的呢？ 我们还是拿 reload 来说, 我们看到,执行命令时,我们是启动一个新的 Nginx 进程,而新的 Nginx 进程在解析到 reload 参数后,就知道我们的目的是控制 Nginx 来重新加载配置文件了,它会向 master 进程发送信号,然后接下来的动作,就和我们直接向 master 进程发送信号一样了。

worker 进程之间是平等的,每个进程,处理请求的机会也是一样的。当我们提供 80 端口的 http 服务时,一个连接请求过来,每个进程都有可能处理这个连接,怎么做到的呢？首先,每个 worker 进程都是从 master 进程 fork 过来,在 master 进程里面,先建立好需要 listen 的 socket (listenfd) 之后,然后再 fork 出多个 worker 进程。所有 worker 进程的 listenfd 会在新连接到来时变得可读,为保证只有一个进程处理该连接,所有 worker 进程在注册 listenfd 读事件前抢 accept_mutex,抢到互斥锁的那个进程注册 listenfd 读事件,在读事件里调用 accept 接受该连接。当一个 worker 进程在 accept 这个连接之后,就开始读取请求,解析请求,处理请求,产生数据后,再返回给客户端,最后才断开连接,这样一个完整的请求就是这样的了。我们可以看到,一个请求,完全由 worker 进程来处理,而且只在一个 worker 进程中处理。

对于每个 worker 进程来说,独立的进程,不需要加锁,所以省掉了锁带来的开销,同时在编程以及问题查找时,也会方便很多。其次,采用独立的进程,可以让互相之间不会影响,一个进程退出后,其它进程还在工作,服务不会中断,master 进程则很快启动新的 worker 进程。当然,worker 进程的异常退出,肯定是程序有 bug 了,异常退出,会导致当前 worker 上的所有请求失败,不过不会影响到所有请求,所以降低了风险。

Nginx 也是可以作为客户端来请求其它 server 的数据的 (如 upstream 模块)

centos install nginx
  
emacs /etc/yum.repos.d/nginx.repo

[nginx]
  
name=nginx repo
  
baseurl=[http://nginx.org/packages/mainline/centos/7/$basearch/](http://nginx.org/packages/mainline/centos/7/$basearch/)
  
gpgcheck=0
  
enabled=1

yum install nginx

下载 地址: [http://nginx.org/packages/centos/7/x86_64/RPMS/](http://nginx.org/packages/centos/7/x86_64/RPMS/)
