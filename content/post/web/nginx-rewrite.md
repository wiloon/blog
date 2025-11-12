---
title: nginx rewrite
author: "-"
date: 2012-12-08T02:46:57+00:00
url: nginx/rewrite
categories:
  - nginx
tags:
  - reprint
---
## nginx rewrite

## 理解地址重写 与 地址转发

地址重写与地址转发是两个不同的概念。

地址重写 是为了实现地址的标准化，比如我们可以在地址栏中中输入 www.baidu.com. 我们也可以输入 www.baidu.cn. 最后都会被重写到 www.baidu.com 上。浏览器的地址栏也会显示www.baidu.com。

地址转发：它是指在网络数据传输过程中数据分组到达路由器或桥接器后，该设备通过检查分组地址并将数据转发到最近的局域网的过程。

因此地址重写和地址转发有以下不同点：

1. 地址重写会改变浏览器中的地址，使之变成重写成浏览器最新的地址。而地址转发他是不会改变浏览器的地址的。
2. 地址重写会产生两次请求，而地址转发只会有一次请求。
3. 地址转发一般发生在同一站点项目内部，而地址重写且不受限制。
4. 地址转发的速度比地址重定向快。

## Rewrite 指令

该指令是通过正则表达式的使用来改变URI。可以同时存在一个或多个指令。需要按照顺序依次对URL进行匹配和处理。

该指令可以在server块或location块中配置，其基本语法结构如下：

```bash
# Context: server, location, if
server {
    # 规则：可以是字符串或者正则来表示想匹配的目标url
    rewrite {规则} {定向路径} {重写类型};
    rewrite regex replacement [flag];
}

```

- rewrite：该指令是实现URL重写的指令。
- regex：用于匹配 URI 的正则表达式。
- replacement：将regex正则匹配到的内容替换成 replacement。
- flag: flag标记。

例如客户端请求 http://foo.bar.com/foo/bar, nginx 送到 regex 匹配的字符串是 `/foo/bar`

flag有如下值：

- last: 本条规则匹配完成后，继续向下匹配新的location URI 规则。(不常用)
- break: 本条规则匹配完成即终止，不再匹配后面的任何规则(不常用)。
- redirect: 返回 302 临时重定向，浏览器地址会显示跳转新的URL地址。(默认值)
- permanent: 返回 301 永久重定向。浏览器地址会显示跳转新的URL地址。

比如如下列子：

```bash
rewrite ^/(.*) http://www.baidu.com/$1 permanent;
# 说明：
# rewrite 为固定关键字，表示开始进行rewrite匹配规则。
# regex 为 ^/(.*)。 这是一个正则表达式，匹配完整的域名和后面的路径地址。
# replacement就是 http://www.baidu.com/1这块了，其中1是取regex部分()里面的内容。如果匹配成功后跳转到的URL。
# flag 就是 permanent，代表永久重定向的含义，即跳转到 http://www.baidu.com/$1 地址上。
```

## Rewrite 指令可用的全局变量

- $host: 变量中存放了请求的URL中的主机部分字段，比如 `http://xxx.abc.com:8080/home` 中的 xxx.abc.com.

ngx_http_rewrite_module 模块用来使用正则表达式 (PCREs) 改变请求的 URI，返回重定向，并有条件地选择配置。

## nginx 指令执行顺序

首先顺序执行 server 块中的 rewrite 模块指令，得到 rewrite 后的请求 URI
然后循环执行如下指令

>如果没有遇到中断循环标志，此循环最多执行10次，但是我们可以使用break指令来中断rewrite后的新一轮的循环

执行server块的rewrite指令
执行location匹配
执行选定的location中的rewrite指令

## break

```bash
Context: server, location, if
```

停止执行 ngx_http_rewrite_module 的指令集，但是其他模块指令是不受影响的

```bash
server {
    listen 8080;
    # 此处 break 会停止执行 server 块的 return 指令(return 指令属于rewrite模块)
    # 如果把它注释掉 则所有请求进来都返回 ok
    break;
    return 200 "ok";
    location = /testbreak {
        break;
        return 200 $request_uri;
        proxy_pass http://127.0.0.1:8080/other;
    }
    location / {
        return 200 $request_uri;
    }
}

# 发送请求如下
# curl 127.0.0.1:8080/testbreak
# /other

# 可以看到 返回 `/other` 而不是 `/testbreak`，说明 `proxy_pass` 指令还是被执行了
# 也就是说 其他模块的指令是不会被 break 中断执行的
# (proxy_pass是ngx_http_proxy_module的指令)
```

## if

```bash
Context: server, location
```

依据指定的条件决定是否执行 if 块语句中的内容

if 中的几种 判断条件
一个变量名，如果变量 $variable 的值为空字符串或者字符串"0"，则为false
变量与一个字符串的比较 相等为(=) 不相等为(!=) 注意此处不要把相等当做赋值语句啊
变量与一个正则表达式的模式匹配 操作符可以是(~ 区分大小写的正则匹配， ~*不区分大小写的正则匹配， !~ !~*，前面两者的非)
检测文件是否存在 使用 -f(存在) 和 !-f(不存在)
检测路径是否存在 使用 -d(存在) 和 !-d(不存在) 后面判断可以是字符串也可是变量
检测文件、路径、或者链接文件是否存在 使用 -e(存在) 和 !-e(不存在) 后面判断可以是字符串也可是变量
检测文件是否为可执行文件 使用 -x(可执行) 和 !-x(不可执行) 后面判断可以是字符串也可是变量
注意 上面 第1，2，3条被判断的必须是 变量， 4, 5, 6, 7则可以是变量也可是字符串

```bash
set $variable "0"; 
if ($variable) {
    # 不会执行，因为 "0" 为 false
    break;            
}

# 使用变量与正则表达式匹配 没有问题
if ( $http_host ~ "^star\.igrow\.cn$" ) {
    break;            
}

# 字符串与正则表达式匹配 报错
if ( "star" ~ "^star\.igrow\.cn$" ) {
    break;            
}
# 检查文件类的 字符串与变量均可
if ( !-f "/data.log" ) {
    break;            
}

if ( !-f $filename ) {
    break;            
}
return
Context: server, location, if

return code [text];
return code URL;
return URL;
```

停止处理并将指定的code码返回给客户端。 非标准code码 444 关闭连接而不发送响应报头。

从0.8.42版本开始， return 语句可以指定重定向 url (状态码可以为如下几种 301,302,303,307),
也可以为其他状态码指定响应的文本内容，并且重定向的url和响应的文本可以包含变量。

有一种特殊情况，就是重定向的url可以指定为此服务器本地的urI，这样的话，nginx会依据请求的协议$scheme， server_name_in_redirect 和 port_in_redirect自动生成完整的 url （此处要说明的是server_name_in_redirect 和port_in_redirect 指令是表示是否将server块中的 server_name 和 listen 的端口 作为redirect用 ）

```bash
# return code [text]; 返回 ok 给客户端
location = /ok {
    return 200 "ok";
}

# return code URL; 临时重定向到 百度
location = /redirect {
    return 302 http://www.baidu.com;
}

# return URL; 和上面一样 默认也是临时重定向
location = /redirect {
    return http://www.baidu.com;
}

```

## rewrite

```bash
# Context: server, location, if
rewrite regex replacement [flag];
```

rewrite 指令是使用指定的正则表达式 regex来匹配请求的 urI，如果匹配成功，则使用 replacement更改 URI。rewrite 指令按照它们在配置文件中出现的顺序执行。可以使用 flag标志来终止指令的进一步处理。如果替换字符串 replacemen t以 http://, https:// 或 $ scheme 开头，则停止处理后续内容，并直接重定向返回给客户端。

第一种情况 重写的字符串 带 http://

```bash
location / {
    # 当匹配 正则表达式 /test1/(.*)时 请求将被临时重定向到 http://www.$1.com
    # 相当于 flag 写为 redirect
    rewrite /test1/(.*) http://www.$1.com;
    return 200 "ok";
}
# 在浏览器中输入 127.0.0.1:8080/test1/baidu 
# 则临时重定向到 www.baidu.com
# 后面的 return 指令将没有机会执行了
```

第二种情况, 重写的字符串 不带 http://

```bash
location / {
    rewrite /test1/(.*) www.$1.com;
    return 200 "ok";
}

# 发送请求如下
# curl 127.0.0.1:8080/test1/baidu
# ok

# 此处没有带 http:// 所以只是简单的重写。请求的 uri 由 /test1/baidu 重写为 www.baidu.com
# 因为会顺序执行 rewrite 指令 所以 下一步执行 return 指令 响应了 ok
```

## rewrite 的四个 flag

- last
停止处理当前的 ngx_http_rewrite_module的指令集，并开始搜索与更改后的URI相匹配的location;
- break
停止处理当前的 ngx_http_rewrite_module指令集，就像上面说的break指令一样;
- redirect
返回302临时重定向。
- permanent
返回301永久重定向。

```bash
# 没有rewrite 后面没有任何 flag 时就顺序执行 
# 当 location 中没有 rewrite 模块指令可被执行时 就重写发起新一轮location匹配
location / {
    # 顺序执行如下两条rewrite指令 
    rewrite ^/test1 /test2;
    rewrite ^/test2 /test3;  # 此处发起新一轮location匹配 uri为/test3
}

location = /test2 {
    return 200 "/test2";
}  

location = /test3 {
    return 200 "/test3";
}
# 发送如下请求
# curl 127.0.0.1:8080/test1
# /test3
```

## last 与 break 的区别

last 和 break 一样 它们都会终止此 location 中其他它rewrite模块指令的执行，
但是 last 立即发起新一轮的 location 匹配 而 break 则不会

```bash
location / {
    rewrite ^/test1 /test2;
    rewrite ^/test2 /test3 last;  # 此处发起新一轮location匹配 uri为/test3
    rewrite ^/test3 /test4;
    proxy_pass http://www.baidu.com;
}

location = /test2 {
    return 200 "/test2";
}  

location = /test3 {
    return 200 "/test3";
}
location = /test4 {
    return 200 "/test4";
}
# 发送如下请求
# curl 127.0.0.1:8080/test1
# /test3 
```

当如果将上面的 location / 改成如下代码

```bash
location / {
    rewrite ^/test1 /test2;
    # 此处 不会 发起新一轮location匹配；当是会终止执行后续rewrite模块指令 重写后的uri为 /more/index.html
    rewrite ^/test2 /more/index.html break;  
    rewrite /more/index\.html /test4; # 这条指令会被忽略

    # 因为 proxy_pass 不是rewrite模块的指令 所以它不会被 break终止
    proxy_pass https://www.baidu.com;
}
# 发送如下请求
# 浏览器输入 127.0.0.1:8080/test1 
# 代理到 百度产品大全页面 https://www.baidu.com/more/index.html;
```

友情提醒下
此处提一下 在上面的代码中即使将 proxy_pass 放在 带有 break 的 rewrite上面它也是会执行的，这就要扯到nginx的执行流程了。大家有兴趣可以了解下。

rewrite 后的请求参数
如果替换字符串replacement包含新的请求参数，则在它们之后附加先前的请求参数。如果你不想要之前的参数，则在替换字符串 replacement 的末尾放置一个问号，避免附加它们。

```bash
# 由于最后加了个 ?，原来的请求参数将不会被追加到rewrite之后的url后面 
rewrite ^/users/(.*)$ /show?user=$1? last;
```

## rewrite_log

Context: http, server, location, if

开启或者关闭 rewrite模块指令执行的日志，如果开启，则重写将记录下notice 等级的日志到nginx 的 error_log 中，默认为关闭 off

Syntax:    rewrite_log on | off;
set
Context: server, location, if

设置指定变量的值。变量的值可以包含文本，变量或者是它们的组合形式。

```bash
location / {
    set $var1 "host is ";
    set $var2 $host;
    set $var3 " uri is $request_uri";
    return 200 "response ok $var1$var2$var3";
}
# 发送如下请求
# curl 127.0.0.1:8080/test
# response ok host is 127.0.0.1 uri is /test
```

uninitialized_variable_warn
Context: http, server, location, if

控制是否记录 有关未初始化变量的警告。默认开启

>https://segmentfault.com/a/1190000008102599


四：理解防盗链及nginx配置

什么是防盗链？盗链可以理解盗图链接，也就是说把别人的图片偷过来用在自己的服务器上，那么防盗链可以理解为防止其他人把我的图片盗取过去。

防盗链的实现原理：客户端向服务器端请求资源时，为了减少网络带宽，提高响应时间，服务器一般不会一次将所有资源完整地传回客户端。比如请求一个网页时，首先会传回该网页的文本内容，当客户端浏览器在解析文本的过程中发现有图片存在时，会再次向服务器发起对该图片资源的请求，服务器将存储的图片资源再发送给客户端。但是如果这个图片是链接到其他站点的服务器上去了呢，比如在我项目中，我引用了的是淘宝中的一张图片的话，那么当我们网站重新加载的时候，就会请求淘宝的服务器，那么这就很有可能造成淘宝服务器负担。因此这个就是盗链行为。因此我们要实现防盗链。

实现防盗链：使用http协议中请求头部的Referer头域来判断当前访问的网页或文件的源地址。通过该头域的值，我们可以检测访问目标资源的源地址。如果目标源地址不是我们自己站内的URL的话，那么这种情况下，我们采取阻止措施，实现防盗链。但是注意的是：Referer头域中的值是可以被更改的。因此该方法也不能完全安全阻止防盗链。

使用Nginx服务器的Rewrite功能实现防盗链。

Nginx中有一个指令 valid_referers. 该指令可以用来获取 Referer 头域中的值，并且根据该值的情况给 Nginx全局变量 invalidreferer赋值。如果Referer头域中没有符合validreferers指令的值的话，invalid_referer变量将会赋值为1. valid_referers 指令基本语法如下：

valid_referers  none | blocked | server_names | string
none: 检测Referer头域不存在的情况。
blocked： 检测Referer头域的值被防火墙或者代理服务器删除或伪装的情况。那么在这种情况下，该头域的值不以"http://" 或 "https://" 开头。

server_names: 设置一个或多个URL，检测Referer头域的值是否是URL中的某个。

因此我们有了 valid_referers指令和$invalid_referer变量的话，我们就可以通过 Rewrite功能来实现防盗链。
下面我们介绍两种方案：第一：根据请求资源的类型。第二：根据请求目录。

1. 根据请求文件类型实现防盗链配置实列如下：

复制代码
server {
  listen 8080;
  server_name xxx.abc.com
  location ~* ^.+\.(gif|jpg|png|swf|flv|rar|zip)$ {
    valid_referers none blocked www.xxx.com www.yyy.com *.baidu.com  *.tabobao.com;
    if ($invalid_referer) {
      rewrite ^/ http://www.xxx.com/images/forbidden.png;
    }
  }
}
复制代码
如上基本配置，当有网络连接对以 gif、jpg、png为后缀的图片资源时候、当有以swf、flv为后缀的媒体资源时、或以 rar、zip为后缀的压缩资源发起请求时，如果检测到Referer头域中没有符合 valid_referers指令的话，那么说明不是本站的资源请求。

location ~* ^.+\.(gif|jpg|png|swf|flv|rar|zip)$ 该配置的含义是 设置防盗链的文件类型。

valid_referers none blocked www.xxx.com www.yyy.com *.baidu.com *.tabobao.com; 可以理解为白名单，允许文件链出的域名白名单，如果请求的资源文件不是以这些域名开头的话，就说明请求的资源文件不是该域下的请求，因此可以判断它是盗链。因此如果不是该域下的请求，就会使用 Rewrite进行重定向到 http://www.xxx.com/images/forbidden.png 这个图片，比如这张图片是一个x或其他的标识，然后其他的网站就访问不了你这个图片哦。

2. 根据请求目录实现防盗链的配置实列如下：

复制代码
server {
  listen 8080;
  server_name xxx.abc.com
  location /file/ {
    root /server/file/;
    valid_referers none blocked www.xxx.com www.yyy.com *.baidu.com  *.tabobao.com;
    if ($invalid_referer) {
      rewrite ^/ http://www.xxx.com/images/forbidden.png;
    }
  }
}
复制代码
