---
title: Nginx config, 配置, nginx.conf
author: "-"
date: 2013-07-09T05:59:32+00:00
url: nginx/config

categories:
  - inbox
tags:
  - reprint
---
## Nginx config, 配置, nginx.conf

```
server {
    listen       19999;
    location / {
        proxy_pass http://192.168.122.153:19999;
    }
}

```
### location>proxy_redirect
proxy_redirect：修改后端服务器返回的响应头部中的location货refresh，与proxy_pass配合使用：
### location>proxy_ssl_session_reuse on | off;
proxy_ssl_session_reuse:配置是否基于SSL协议与后端服务器建立连接
proxy_ssl_trusted_certificate指令命名的文件中的受信任CA证书用于在上游验证证书
proxy_ssl_trusted_certificate指令设置的那个可信CA证书文件是用来验证后端服务器的证书。

### nginx 414 Request-URI Too Large
    client_header_buffer_size 512k;

### worker_processes, nginx进程数，建议设置为等于CPU总核心数。
    worker_processes 8;
  
官方英文版wiki配置说明中的描述如下，个人理解为worker角色的进程个数 (nginx启动后有多少个worker处理http请求。master不处理请求，而是根据相应配置文件信息管理worker进程. master进程主要负责对外揽活 (即接收客户端的请求) ，并将活儿合理的分配给多个worker，每个worker进程主要负责干活 (处理请求) ) 。

### worker_connections

    max_clients = worker_processes * worker_connections;
  
官方解释如下，个人认为是每一个worker进程能并发处理 (发起) 的最大连接数 (包含所有连接数) 。

### worker_rlimit_nofile

#一个nginx进程打开的最多文件描述符数目，理论值应该是最多打开文件数 (系统的值ulimit -n) 与nginx进程数相除，但是nginx分配请求并不均匀，所以建议与ulimit -n的值保持一致。
  
    worker_rlimit_nofile 65535;

proxy_bind

https://pengpengxp.github.io/2017-06-27-%E4%BD%BF%E7%94%A8nginx%E7%9A%84proxy_bind%E9%80%89%E9%A1%B9%E9%85%8D%E7%BD%AE%E9%80%8F%E6%98%8E%E7%9A%84%E5%8F%8D%E5%90%91%E4%BB%A3%E7%90%86.html

#定义Nginx运行的用户和用户组
  
user www www;

#全局错误日志定义类型，[ debug | info | notice | warn | error | crit ]
  
error_log /var/log/nginx/error.log info;

#进程文件
  
pid /var/run/nginx.pid;

# worker_connections, 工作模式与连接数上限

events
  
{
  
#参考事件模型，use [ kqueue | rtsig | epoll | /dev/poll | select | poll ]; epoll模型是Linux 2.6以上版本内核中的高性能网络I/O模型，如果跑在FreeBSD上面，就用kqueue模型。
  
use epoll;
  
#单个进程最大连接数 (最大连接数=连接数*进程数) 
  
worker_connections 65535;
  
}

#设定http服务器
  
http
  
{
  
include mime.types; #文件扩展名与文件类型映射表
  
default_type application/octet-stream; #默认文件类型
  
#charset utf-8; #默认编码
  
server_names_hash_bucket_size 128; #服务器名字的hash表大小
  
client_header_buffer_size 32k; #上传文件大小限制
  
large_client_header_buffers 4 64k; #设定请求缓
  
client_max_body_size 8m; #设定请求缓

autoindex on; #开启目录列表访问，合适下载服务器，默认关闭。

sendfile on;
  
sendfile 开启高效文件传输模式，sendfile 指令指定nginx是否调用sendfile函数来输出文件，对于普通应用设为 on，如果用来进行下载等应用磁盘IO重负载应用，可设置为off，以平衡磁盘与网络I/O处理速度，降低系统的负载。注意: 如果图片显示不正常把这个改成off。
  
sendfile 配置可以提高 Nginx 静态资源托管效率。 sendfile 是一个系统调用，直接在内核空间完成文件发送，不需要先 read 再 write，没有上下文切换开销。
  
tcp_nopush on;
  
tcp_nodelay on;

TCP_NOPUSH 是 FreeBSD 的一个 socket 选项，对应 Linux 的 TCP_CORK， Nginx 里统一用 tcp_nopush 来控制它，并且只有在启用了 sendfile 之后才生效。启用它之后，数据包会累计到一定大小之后才会发送，减小了额外开销，提高网络效率。

### TCP_NODELAY
TCP_NODELAY 也是一个 socket 选项，启用后会禁用 Nagle 算法，尽快发送数据，某些情况下可以节约 200ms  
 (Nagle 算法原理是: 在发出去的数据还未被确认之前，新生成的小数据先存起来，凑满一个 MSS 或者等到收到确认后再发送) 。Nginx 只会针对处于 keep-alive 状态的 TCP 连接才会启用 tcp_nodelay。

可以看到 TCP_NOPUSH 是要等数据包累积到一定大小才发送，TCP_NODELAY 是要尽快发送，二者相互矛盾。实际上，它们确实可以一起用，最终的效果是先填满包，再尽快发送。

keepalive_timeout 120; #长连接超时时间，单位是秒

#FastCGI相关参数是为了改善网站的性能: 减少资源占用，提高访问速度。下面参数看字面意思都能理解。
  
fastcgi_connect_timeout 300;
  
fastcgi_send_timeout 300;
  
fastcgi_read_timeout 300;
  
fastcgi_buffer_size 64k;
  
fastcgi_buffers 4 64k;
  
fastcgi_busy_buffers_size 128k;
  
fastcgi_temp_file_write_size 128k;

#gzip模块设置
  
gzip on; #开启gzip压缩输出
  
gzip_min_length 1k; #最小压缩文件大小
  
gzip_buffers 4 16k; #压缩缓冲区
  
gzip_http_version 1.0; #压缩版本 (默认1.1，前端如果是squid2.5请使用1.0) 
  
gzip_comp_level 2; #压缩等级
  
gzip_types text/plain application/x-javascript text/css application/xml;
  
#压缩类型，默认就已经包含text/html，所以下面就不用再写了，写上去也不会有问题，但是会有一个warn。
  
gzip_vary on;
  
#limit_zone crawler $binary_remote_addr 10m; #开启限制IP连接数的时候需要使用

upstream blog.ha97.com {
  
#upstream的负载均衡，weight是权重，可以根据机器配置定义权重。weigth参数表示权值，权值越高被分配到的几率越大。
  
server 192.168.80.121:80 weight=3;
  
server 192.168.80.122:80 weight=2;
  
server 192.168.80.123:80 weight=3;
  
}

#虚拟主机的配置
  
server
  
{
  
#监听端口
  
listen 80;
  
#域名可以有多个，用空格隔开
  
server_name www.ha97.com ha97.com;
  
index index.html index.htm index.php;
  
root /data/www/ha97;
  
location ~ ._&#46;(php|php5)?$
  
{
  
fastcgi_pass 127.0.0.1:9000;
  
fastcgi_index index.php;
  
include fastcgi.conf;
  
}
  
#图片缓存时间设置
  
location ~ ._&#46;(gif|jpg|jpeg|png|bmp|swf)$
  
{
  
expires 10d;
  
}
  
#JS和CSS缓存时间设置
  
location ~ .*&#46;(js|css)?$
  
{
  
expires 1h;
  
}
  
#日志格式设定
  
log_format access '$remote_addr - $remote_user [$time_local] "$request" '
  
'$status $body_bytes_sent "$http_referer" '
  
'"$http_user_agent" $http_x_forwarded_for';
  
#定义本虚拟主机的访问日志
  
access_log /var/log/nginx/ha97access.log access;

#对 "/" 启用反向代理
  
location / {
  
proxy_pass http://127.0.0.1:88;
  
proxy_redirect off;
  
proxy_set_header X-Real-IP $remote_addr;
  
#后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
  
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  
#以下是一些反向代理的配置，可选。
  
proxy_set_header Host $host;
  

  
client_body_buffer_size 128k; #缓冲区代理缓冲用户端请求的最大字节数，
  
proxy_connect_timeout 90; #nginx跟后端服务器连接超时时间(代理连接超时)
  
proxy_send_timeout 90; #后端服务器数据回传时间(代理发送超时)
  
proxy_read_timeout 90; #连接成功后，后端服务器响应时间(代理接收超时)
  
proxy_buffer_size 4k; #设置代理服务器 (nginx) 保存用户头信息的缓冲区大小
  
proxy_buffers 4 32k; #proxy_buffers缓冲区，网页平均在32k以下的设置
  
proxy_busy_buffers_size 64k; #高负荷下缓冲大小 (proxy_buffers*2) 
  
proxy_temp_file_write_size 64k;
  
#设定缓存文件夹大小，大于这个值，将从upstream服务器传
  
}

#设定查看Nginx状态的地址
  
location /NginxStatus {
  
stub_status on;
  
access_log on;
  
auth_basic "NginxStatus";
  
auth_basic_user_file conf/htpasswd;
  
#htpasswd文件的内容可以用apache提供的htpasswd工具来产生。
  
}

#本地动静分离反向代理配置
  
#所有jsp的页面均交由tomcat或resin处理
  
location ~ .(jsp|jspx|do)?$ {
  
proxy_set_header Host $host;
  
proxy_set_header X-Real-IP $remote_addr;
  
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  
proxy_pass http://127.0.0.1:8080;
  
}
  
#所有静态文件由nginx直接读取不经过tomcat或resin
  
location ~ ._.(htm|html|gif|jpg|jpeg|png|bmp|swf|ioc|rar|zip|txt|flv|mid|doc|ppt|pdf|xls|mp3|wma)$
  
{ expires 15d; }
  
location ~ ._.(js|css)?$
  
{ expires 1h; }
  
}
  
}

更详细的模块参数请参考: http://wiki.nginx.org/Main

### proxy_pass结尾有无"/"的区别
转载自: http://www.cnblogs.com/naniannayue/archive/2010/08/07/1794520.html
见配置，摘自nginx.conf 里的server 段: 

server {
listen 80;
server_name abc.163.com ;
location / {
proxy_pass http://ent.163.com/ ;
}
location /star/ {
proxy_pass http://ent.163.com ;
}
}
里面有两个location，我先说第一个，/ 。其实这里有两种写法，分别是: 

location / {
proxy_pass http://ent.163.com/ ;
}
location / {
proxy_pass http://ent.163.com ;
}
出来的效果都一样的。

第二个location，/star/。同样两种写法都有，都出来的结果，就不一样了。

location /star/ {
proxy_pass http://ent.163.com ;
}
当访问 http://abc.163.com/star/ 的时候，nginx 会代理访问到 http://ent.163.com/star/ ，并返回给我们。

location /star/ {
proxy_pass http://ent.163.com/ ;
}
当访问 http://abc.163.com/star/ 的时候，nginx 会代理访问到 http://ent.163.com/ ，并返回给我们。

这两段配置，分别在于， proxy_pass http://ent.163.com/ ; 这个"/"，令到出来的结果完全不同。

前者，相当于告诉nginx，我这个location，是代理访问到http://ent.163.com 这个server的，我的location是什么，nginx 就把location 加在proxy_pass 的 server 后面，这里是/star/，所以就相当于 http://ent.163.com/star/。如果是location /blog/ ，就是代理访问到 http://ent.163.com/blog/。

后者，相当于告诉nginx，我这个location，是代理访问到http://ent.163.com/的，http://abc.163.com/star/ == http://ent.163.com/ ，可以这样理解。改变location，并不能改变返回的内容，返回的内容始终是http://ent.163.com/ 。 如果是location /blog/ ，那就是 http://abc.163.com/blog/ == http://ent.163.com/ 。

这样，也可以解释了上面那个location / 的例子，/ 嘛，加在server 的后面，仍然是 / ，所以，两种写法出来的结果是一样的。

PS: 如果是 location ~* ^/start/(.*).html 这种正则的location，是不能写"/"上去的，nginx -t 也会报错的了。因为，路径都需要正则匹配了嘛，并不是一个相对固定的locatin了，必然要代理到一个server。

### location匹配顺序
https://www.jianshu.com/p/38810b49bc29


  
    nginx.conf
  


https://blog.wiloon.com/?p=5626&embed=true#?secret=1NahDK0zlm

client_max_body_size 20m; 20m为允许最大上传的大小。
   
use epoll;
   
在Linux操作系统下，nginx使用epoll事件模型，得益于此，nginx在Linux操作系统下效率相当高。同时Nginx在OpenBSD或FreeBSD操作系统上采用类似于epoll的高效事件模型kqueue。nginx同时是一个高性能的 HTTP 和 反向代理 服务器，也是一个 IMAP/POP3/SMTP 代理服务器。

multi_accept 告诉nginx收到一个新连接通知后接受尽可能多的连接。

multi_accept
  
multi_accept可以让nginx worker进程尽可能多地接受请求。它的作用是让worker进程一次性地接受监听队列里的所有请求，然后处理。如果multi_accept的值设为off，那么worker进程必须一个一个地接受监听队列里的请求。

events {
   
multi_accept on;
   
}
  
默认Nginx没有开启multi_accept。

如果web服务器面对的是一个持续的请求流，那么启用multi_accept可能会造成worker进程一次接受的请求大于worker_connections指定可以接受的请求数。这就是overflow，这个overflow会造成性能损失，overflow这部分的请求不会受到处理。

Nginx的缓冲配置
  
请求缓冲在Nginx请求处理中扮演了重要的角色。当收到一条请求时，Nginx将请求写入缓冲当中。缓冲中的数据成为Nginx的变量，比如$request_body。如果缓冲容量比请求容量小，那么多出来的请求会被写入硬盘，这时便会有I/O操作。Nginx提供了多个directive来修改请求缓冲。

### client_body_buffer_size
  
这个参数设定了 request body 的缓冲大小。如果 body 超过了缓冲的大小，那么整个 body 或者部分 body 将被写入一个临时文件。如果 Nginx 被设置成使用文件缓冲而不使用内存缓冲，那么这个参数就无效。client_body_buffer_size 在 32 位系统上默认是8k，在 64 位系统上默认是16k。可以在 http, server 和 location 模块中指定，如下: 

```
server {
          
client_body_buffer_size 8k;
  
}
```
  
### client_max_body_size
  
这个directive设定Nginx可以处理的最大request body大小。如果收到的请求大于指定的大小，那么Nginx会回复HTTP 413错误 (Request Entity too large) 。如果web服务器提供大文件上传的话，那么设置好这个directive很重要。

Nginx默认为这个directive设定的值是1m，可以在http, server 和 location模块中定义，例如: 

server {
     
client_max_body_size 2m;
  
}
  
client_body_in_file_only
  
启用这个directive会关闭Nginx的请求缓冲，将request body存储在临时文件当中，在http, server 和 location模块中定义。它可以有三个值: 

off: 禁止文件写入
  
clean: request body将被写入文件，文件在请求处理完成后删除
  
on: request body将被写入文件，但文件在请求处理完成后不会被删除
  
默认这个directive的值是off。我们可以将它设为off，例如: 

http {
      
client_body_in_file_only clean;
  
}
  
这个directive对于错误调试很有用处，但并不建议在生产环境下使用它。

client_body_in_single_buffer
  
这个directive让Nginx将所有的request body存储在一个缓冲当中，它的默认值是off。启用它可以优化读取$request_body变量时的I/O性能。可以在http, server 和 location模块中定义。

server {
      
client_body_in_single_buffer on;
  
}
  
client_body_temp_path
  
这个directive指定存储request body的临时文件路径。另外，它可以指定目录层次。Nginx默认在Nginx的安装目录下面的client_body_temp子目录下面创建临时文件。这个directive可以在http, server 和 location 模块中定义。

server {
       
client_body_temp_pathtemp_files 1 2;
  
}
  
client_header_buffer_size
  
这个directive类似于client_body_buffer_size。它给request header分配缓冲。默认的值是1k，可以在http 和 server模块中定义。

http {
    
client_header_buffer_size 1m;
  
}
  
large_client_header_buffers
  
这个directive指定request header缓冲的数量和大小。只有当默认的缓冲不够用时，它才能被使用。当请求处理完成后或者连接进入 keep-alive 状态时，它被释放。可以在http 和 server模块中定义。

http {
     
large_client_header_buffers 4 8k;
  
}
  
如果请求的URI超过了单个缓冲的大小，那么Nginx会返回HTTP 414错误 (Request URI Too Long) 。如果有任何request header超过了单个缓冲的大小，那么Nginx会返回HTTP 400错误 (Bad Request) 。

Nginx的超时设置 (timeout) 
  
Nginx处理的每一个请求都会有相应的超时设置。如果做好这些超时的优化，就可以大大提升Nginx的性能。超时过后，系统资源被释放，用来处理其他的请求。下面，我们将讨论Nginx提供的多个关于超时的directive。

keepalive
  
HTTP是一种无状态的、基于请求+回复的协议。客户端打开一个TCP端口向服务器发送请求，服务器发送回复后断开完成的连接以释放服务器资源。

如果客户端向服务器发送多个请求，那么每个请求都要建立各自独立的连接以传输数据。在网页包含大量内容的情况下，这种方式变得效率低下，因为浏览器要为每一个内容打开一个连接。

HTTP有一个keepalive模式，keepalive告诉web服务器在处理完请求后保持TCP连接不断开。如果客户端发出另外一个请求，它可以利用这些保持打开的连接，而不必另外打开一个连接。当客户端感觉不再需要这些保持打开的连接时，或者web服务器发现经过一段时间 (timeout) 这些保持打开的连接没有任何活动，那么它们就会断开。浏览器一般会打开多个keepalive连接。

由于keepalive连接在一段时间内会保持打开状态，它们会在这段时间占用系统资源。如果web服务器流量大，而timeout的时间设置得过长，那么系统的性能会受到很大影响。

Nginx提供了多个可以用来设置keepalive连接的directive。

keepalive_timeout
  
这个directive用于设置keepalive连接的超时时间，默认为65秒。若将它设置为0，那么就禁止了keepalive连接。它在http, server 和 location模块中定义。

http {
     
keepalive_timeout 20s;
  
}
  
这个directive有另外一个可选的时间参数，例如: 

http {
      
keepalive_timeout 20s 18s;
  
}
  
第二个参数18s被包含在回复header里。

curl -I http://www.example.com

........

Connection: keep-alive

Keep-Alive: timeout=18

.....
  
keepalive_requests
  
这个directive设定了使用keepalive连接的请求数量上限。当使用keepalive连接的请求数量超过这个上限时，web服务器关闭keepalive连接。默认值为100，可以在http, server 和 location模块中定义。

http {
     
keepalive_requests 20;
  
}
  
keepalive_disabled
  
这条directive可以针对特定的浏览器关闭keepalive连接。默认值为msie6。可以在http, server 和 location模块中定义。

http {
     
keepalive_disabled msie6 safari;
  
}
  
send_timeout
  
这条directive指定了向客户端传输数据的超时时间。默认值为60秒，可以在http, server 和 location模块中定义。

server {
     
send_timeout 30s;
  
}
  
client_body_timeout
  
这条directive设定客户端与服务器建立连接后发送request body的超时时间。如果客户端在此时间内没有发送任何内容，那么Nginx返回HTTP 408错误 (Request Timed Out) 。它的默认值是60秒，在http, server 和 location模块中定义。

server {
      
client_body_timeout 30s;
  
}
  
client_header_timeout
  
这条directive设定客户端向服务器发送一个完整的request header的超时时间。如果客户端在此时间内没有发送一个完整的request header，那么Nginx返回HTTP 408错误 (Request Timed Out) 。它的默认值是60秒，在http 和 server模块中定义。

server {
     
client_header_timeout 30s;
  
}
  
Nginx的压缩配置 (compression) 
  
压缩可以减少服务器发送的数据包大小，从而加快了网页的加载速度。

ngx_http_gzip_module
  
Nginx的gzip压缩依赖于这个模块。服务器先压缩数据，然后将压缩后的数据发送给客户端。压缩的效果对于文本内容最明显，而gzip对于JPEG, GIF, MP3这些不可压缩的内容就没什么用处。另外，如果压缩水平太高，那么需要的CPU时间更多。ngx_http_gzip_module模块提供了下面的directive来配置gzip压缩。

gzip
  
这条directive可以Nginx启用gzip压缩功能，默认值为on，可以在http, server 和 location 以及if 当中定义。

http {
      
gzip on;
  
}
  
gzip_comp_level
  
这条directive设定gzip的压缩水平，压缩水平可以是1到9。太高的压缩水平对性能提升并没有太大好处，因为这需要更多的CPU时间。默认值是1，其中1到3是比较好的压缩水平，因为它们在最终的压缩数据大小和需要花费的CPU时间之间做出了很好的平衡。可以在http, server 和 location模块中定义。

http {
      
gzip_comp_level 2;
  
}
  
gzip_min_length
  
这条directive指定了压缩数据的最小长度，只有大于或等于最小长度才会对其压缩。它从Content-Length中获取数据的长度。默认值是20字节，在http, server 和 location中定义。

http {
     
gzip_min_length 1000;
  
}
  
gzip_types
  
这条directive指定了允许进行压缩的回复类型。默认值为text/html，在http, server 和 location中定义。

http {
     
gzip_types text/html text/css text/plain;
  
}
  
text/html类型总是会被压缩，text/html, text/css和text/plain这些是MIME类型。

gzip_http_version
  
这条directive指定一个HTTP版本。只有当请求的HTTP版本比这个版本更高或一样，Nginx才会压缩数据。默认值是1.1，在http, server 和 location模块中定义。

http {
     
gzip_http_versioin 1.1;
  
}
  
gzip_vary
  
这条directive可以在回复的header中添加Vary:Accept-Encoding这一栏。默认值是off，在http, server 和 location中定义。

http {
     
gzip_vary on;
  
}
  
gzip_disable
  
有些浏览器很弱智，比如IE6，它们看不懂gzip压缩后的数据。Nginx从请求header的User-Agent中确定浏览器，gzip_disable可以对弱智的浏览器关闭gzip压缩功能。在http, server, 和 location中定义。

http {
       
gzip_disable "MSIE [1-6]&#46;";
  
}
  
ngx_http_gzip_static_module
  
这个模块可以让Nginx发送一个已经压缩好的.gz文件，而不发送普通文件。Nginx并不会自己生成.gz文件，而是寻找是否有已经存在.gz文件。如果有，就发送那个.gz文件。这可以节省CPU时间。默认这个模块没有启用，可以在编译Nginx时加上–with-http_gzip_static_module选项来启用。下面是这个模块提供的directive。

gzip_static
  
这个就是让Nginx发送.gz压缩文件的directive。默认值是off。gzip_static的值设为on之后，Nginx会先判断客户端是否支持.gz文件，如果支持就发送.gz文件，不支持就发送普通文件。另外也可以将gzip_static的值设为always，这时Nginx总是发送.gz文件 (如果.gz文件存在的话) ，而不会检查客户端是否支持.gz文件。

gzip_static也会查看gzip_http_version, gzip_proxied和gzip_disable的值来确定客户端是否支持压缩。它的值在http, server 和 location中定义。

server {
      
gzip_static always;
  
}
  
ngx_http_gunzip_module
  
这个模块让Nginx发送一个经解压的文件给那些不支持gzip的客户端，并且经常与ngx_http_gzip_static_module搭配使用。后者可以让Nginx发送一个已经压缩好文件，而前者可以解压文件以让Nginx发送给不支持压缩的客户端。这个模块默认没有启用，可以在编译Nginx时加上–with-http_gunzip_module选项来启用。

gzip_proxied expired no-cache no-store private auth;
  
gzip_types text/plain application/xml;
  
以上的配置都很容易理解，看看上述官方文档就可以了，只有一个比较难理解:gzip_proxied
  
这个参数用于指定当 http请求来自代理服务器时 (如何判断？请求头里包含 VIA 这个参数就认为这个请求来自代理服务器) 
  
基于代理服务器的类型来决定是否进行压缩。如上述配置中，请求头里 包含了 expired 那么就启用压缩，其他的参数也类似。其中有两个特殊的参数，any表示全部都开启压缩，off表示全部都不压缩
  
至于为什么会存在这么一个配置？
  
官方文档是这么举例的: For example, it is reasonable to compress responses only to requests that will not be cached on the proxy server.
  
那为什么是reasonable呢？哈哈，我也不确定，但网上的一种说法是对于一些可缓存的静态内容可以不启用压缩，因为这些静态内容大多都是经过压缩优化，gzip难以对其继续压缩，即使进行了意义也不大。
  
反正，具体场景具体分析把，到时遇到了真的不用压缩的场景，我们记得有这么一个选项就好了


gunzip
  
这个directive用来解压.gz文件。默认值为off，在http, server 和 location当中定义。

location / {
       
gzip_static always;
       
gunzip on;
  
}
  
Nginx的日志配置
  
日志是一把双刃剑。一方面，它提供了很多有用的信息；另一方面，它带来了计算成本。如果Nginx产生成千上万行日志，必然会对性能产生影响。下面来讨论优化日志的几个directive。

### access_log
  
这条directive配置Nginx处理所有请求时产生的日志。它有多个参数，可以用来指定日志路径，日志格式样本，缓冲等等。syslog可以将日志传送给一个日志服务器而不写入日志文件。如果access_log的值设为off，那么Nginx不会产生任何日志。访问日志文件的默认路径是 /var/log/nginx/access.log。

    http {
        access_log /var/log/nginx/access.log;
    }
  
### error_log
  
Nginx默认启用了错误日志，error_log可以在http, server, location模块中定义。它可以有两个参数，第一个参数是错误日志的路径，第二个是错误日志的级别。级别的值可以是debug,info,notice,warn,error,crit,alert和emerg。

    http {
        error_log /var/log/nginx/error.log crit;
    }
  
大综合
  
下面的配置综合了上述讨论的所有directive。

    http {
    # configuring buffers
    client_body_buffer_size 15k;
    client_max_body_size 8m;
        # configuring timeouts
        # client_header_timeout 和 client_body_timeout设置请求头和请求体(各自)的超时时间，如果没有发送请求头和请求体，Nginx服务器会返回408错误或者request time out
        keepalive_timeout 20;
        client_body_timeout 15;
        client_header_timeout 15;
        send_timeout 10;

        ######
        # configuring gzip
        ######
        gzip on;
        gzip_comp_level 2;
        gzip_min_length 1000;
        gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
        
        #####
        # configuring logs
        #####
        access_log off;
        log_not_found off;
        error_log logs/error.log crit;
    }

NGINX配置超时时间 原
   
谢思华 谢思华 发布于 2014/02/13 18:29 字数 1181 阅读 25013 收藏 14 点赞 1 评论 0
  
一、啥时候用到
         
用来设置请求资源和服务器返回的时间，保证一个请求占用固定时间，超出后报504超时！这样可以保证一个请求占用过长时间。

二、主要参数
        
使用nginx服务器如果遇到timeou情况时可以如下设置参数，使用fastcgi: 

         fastcgi_connect_timeout 75;  链接
    
         fastcgi_read_timeout 600;   读取
    
         fastcgi_send_timeout 600;   发请求
    
     这两个选项.
         fastcgi_read_timeout是指fastcgi进程向nginx进程发送response的整个过程的超时时间
         fastcgi_send_timeout是指nginx进程向fastcgi进程发送request的整个过程的超时时间
    
     这两个选项默认都是秒(s),可以手动指定为分钟(m),小时(h)等
    

三 其他常用参数以及参数说明
          
keepalive_timeout 600; 连接超时时间，1分钟，具体时间可以根据请求 (例如后台导入) 需要的时间来设置

        proxy_connect_timeout 600;    1分钟
    
        proxy_read_timeout 600;    1分钟
    

nginx超时配置参数说明: 
  
keepalive_timeout

语法 keepalive_timeout timeout [ header_timeout ]

默认值 75s

上下文 http server location

说明 第一个参数指定了与client的keep-alive连接超时时间。服务器将会在这个时间后关闭连接。可选的第二个参数指定了在响应头Keep-Alive: timeout=time中的time值。这个头能够让一些浏览器主动关闭连接，这样服务器就不必要去关闭连接了。没有这个参数，nginx不会发送Keep-Alive响应头 (尽管并不是由这个头来决定连接是否"keep-alive") 

两个参数的值可并不相同

注意不同浏览器怎么处理"keep-alive"头

MSIE 和Opera忽略掉"Keep-Alive: timeout=<N>" header.

MSIE 保持连接大约60-65秒，然后发送TCP RST

Opera永久保持长连接

Mozilla keeps the connection alive for N plus about 1-10 seconds.

Konqueror保持长连接N秒

proxy_connect_timeout

语法 proxy_connect_timeout time

默认值 60s

上下文 http server location

说明 该指令设置与upstream server的连接超时时间，有必要记住，这个超时不能超过75秒。

这个不是等待后端返回页面的时间，那是由proxy_read_timeout声明的。如果你的upstream服务器起来了，但是hanging住了 (例如，没有足够的线程处理请求，所以把你的请求放到请求池里稍后处理) ，那么这个声明是没有用的，由于与upstream服务器的连接已经建立了。

proxy_read_timeout

语法 proxy_read_timeout time

默认值 60s

上下文 http server location

说明 该指令设置与代理服务器的读超时时间。它决定了nginx会等待多长时间来获得请求的响应。这个时间不是获得整个response的时间，而是两次reading操作的时间。

client_header_timeout

语法 client_header_timeout time

默认值 60s

上下文 http server

说明 指定等待client发送一个请求头的超时时间 (例如: GET / HTTP/1.1) .仅当在一次read中，没有收到请求头，才会算成超时。如果在超时时间内，client没发送任何东西，nginx返回HTTP状态码408("Request timed out")

client_body_timeout

语法 client_body_timeout time

默认值 60s

上下文 http server location

说明 该指令设置请求体 (request body) 的读超时时间。仅当在一次readstep中，没有得到请求体，就会设为超时。超时后，nginx返回HTTP状态码408("Request timed out")

lingering_timeout

语法 lingering_timeout time

默认值 5s

上下文 http server location

说明 lingering_close生效后，在关闭连接前，会检测是否有用户发送的数据到达服务器，如果超过lingering_timeout时间后还没有数据可读，就直接关闭连接；否则，必须在读取完连接缓冲区上的数据并丢弃掉后才会关闭连接。

resolver_timeout

语法 resolver_timeout time

默认值 30s

上下文 http server location

说明 该指令设置DNS解析超时时间

proxy_send_timeout

语法 proxy_send_timeout time

默认值 60s

上下文 http server location

说明 这个指定设置了发送请求给upstream服务器的超时时间。超时设置不是为了整个发送期间，而是在两次write操作期间。如果超时后，upstream没有收到新的数据，nginx会关闭连接

proxy_upstream_fail_timeout (fail_timeout) 

语法 server address [fail_timeout=30s]

默认值 10s

上下文 upstream

说明 Upstream模块下 server指令的参数，设置了某一个upstream后端失败了指定次数 (max_fails) 后，该后端不可操作的时间，默认为10秒

四、其他说明
     
针对这两个常用参数，还可以设置一定的规则，例如单独针对后台，设置读取超时时间。规则可以类似这: /admin/*

具体可参考这个: http://www.cnblogs.com/discuss/articles/1866851.html

五、nginx基本配置与参数说明
  
http://my.oschina.net/xsh1208/blog/492374
  
https://www.linuxdashen.com/nginx%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96%E4%B9%8B%E9%85%8D%E7%BD%AE%E7%BC%93%E5%86%B2%E3%80%81%E8%B6%85%E6%97%B6%E3%80%81%E5%8E%8B%E7%BC%A9%E5%92%8C%E6%97%A5%E5%BF%97

https://my.oschina.net/xsh1208/blog/199674
  
https://blog.51cto.com/liuqunying/1420556

作者: skyesx
  
链接: https://hacpai.com/article/1447946179819
  
来源: 黑客派
  
协议: CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/


### server_tokens off;
隐藏版本号

## client_max_body_size 10m; 
允许客户端请求的最大单文件字节数

## nginx 配置文件 单位

Sizes can be specified in bytes, kilobytes (suffixes k and K) or megabytes (suffixes m and M), for example, “1024”, “8k”, “1m”.


>http://nginx.org/en/docs/syntax.html