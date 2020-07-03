---
title: A记录、MX记录、CNAME记录、TXT记录、AAAA记录、NS记录
author: wiloon
type: post
date: 2017-11-16T08:21:04+00:00
url: /?p=11442
categories:
  - Uncategorized

---
https://www.ezloo.com/2011/04/a\_mx\_cname\_txt\_aaaa_ns.html

A记录

A记录是用来创建到IP地址的记录。

A记录设置技巧

1、如果想创建不带www的记录，即ezloo.com，在主机记录中填写@或者留空，不同的注册商可能不一样。

2、创建多个域名到同一个IP，比如给博客建了二级域名，可以使用*.blog.ezloo.com来指向一个IP，这样的话，不管是访问a.blog.ezloo.com还是b.blog.ezloo.com都能到同一个IP。

3、如果你给同一个二级域名设置了多个A记录，比如你建了两个blog的A记录，其中一个指向了111.111.111.111，另一个指向了111.111.111.112，那么在查询的时候，每次返回的数据包含了两个IP地址，但是在返回的过程中数据排列的顺序每次都不相同。由于大 部分的客户端只选择第一条记录所以通过这种方式可以实现一定程度的负载均衡。

在命令行下可以通过nslookup -qt=a www.ezloo.com来查看A记录。

MX记录

在命令行下可以通过 nslookup -qt=mx ezloo.com 来查看MX记录。

mx 记录的权重对 Mail 服务是很重要的，当发送邮件时，Mail 服务器先对域名进行解析，查找 mx 记录。先找权重数最小的服务器（比如说是 10），如果能连通，那么就将服务器发送过去；如果无法连通 mx 记录为 10 的服务器，那么才将邮件发送到权重为 20 的 mail 服务器上。

这里有一个重要的概念，权重 20 的服务器在配置上只是暂时缓存 mail ，当权重 20 的服务器能连通权重为 10 的服务器时，仍会将邮件发送的权重为 10 的 Mail 服务器上。当然，这个机制需要在 Mail 服务器上配置。（http://blog.ixpub.net/viewthread-1308142）

CNAME记录

CNAME记录也成别名记录，它允许你将多个记录映射到同一台计算机上。比如你建了如下几条记录：

a1 CNAME a.ezloo.com
  
a2 CNAME a.ezloo.com
  
a3 CNAME a.ezloo.com
  
a A 111.222.111.222

我们访问a1（a2，a3）.ezloo.com的时候，域名解析服务器会返回一个CNAME记录，并且指向a.ezloo.com，然后我们的本地电脑会再发送一个请求，请求a.ezloo.com的解析，返回IP地址。

当我们要指向很多的域名到一台电脑上的时候，用CNAME比较方便，就如上面的例子，我们如果服务器更换IP了，我们只要更换a.ezloo.com的A记录即可。

在命令行下可以使用nslookup -qt=cname a.ezloo.com来查看CNAME记录。

TXT记录

TXT记录一般是为某条记录设置说明，比如你新建了一条a.ezloo.com的TXT记录，TXT记录内容"this is a test TXT record."，然后你用 nslookup -qt=txt a.ezloo.com ，你就能看到"this is a test TXT record"的字样。

除外，TXT还可以用来验证域名的所有，比如你的域名使用了Google的某项服务，Google会要求你建一个TXT记录，然后Google验证你对此域名是否具备管理权限。

在命令行下可以使用nslookup -qt=txt a.ezloo.com来查看TXT记录。

AAAA记录

AAAA记录是一个指向IPv6地址的记录。

可以使用nslookup -qt=aaaa a.ezloo.com来查看AAAA记录。

NS记录

NS记录是域名服务器记录，用来指定域名由哪台服务器来进行解析。可以使用nslookup -qt=ns ezloo.com来查看。

TTL值

TTL=time to live，表示解析记录在DNS服务器中的缓存时间。比如当我们请求解析www.ezloo.com的时候，DNS服务器发现没有该记录，就会下个NS服务器发出请求，获得记录之后，该记录在DNS服务器上保存TTL的时间长度。当我们再次发出请求解析www.ezloo.com 的时候，DNS服务器直接返回刚才的记录，不去请求NS服务器。TTL的时间长度单位是秒，一般为3600秒。