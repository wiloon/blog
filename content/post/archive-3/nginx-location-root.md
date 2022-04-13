---
title: nginx location, root
author: "-"
date: 2019-04-29T02:13:46+00:00
url: nginx/location
categories:
  - nginx
tags:
  - reprint
---
## nginx location, root

## location 语法

Location 块通过指定模式来与客户端请求的URI相匹配。
Location 基本语法：

匹配 URI 类型，有四种参数可选，当然也可以不带参数。
命名 location，用@来标识，类似于定义goto语句块。
location [ = | ~ | ~* | ^~ ] /URI { … }
location @/name/ { … }
location 匹配命令解释

- `空` location 后没有参数直接跟标准 URI， 表示前缀匹配，代表跟请求中的 URI 从头开始匹配。
- `=` 用于标准 URI 前，要求请求字符串与其精准匹配，成功则立即处理，nginx 停止搜索其他匹配。
- `^~` 用于标准 URI 前，并要求一旦匹配到就会立即处理，不再去匹配其他的正则 URI，一般用来匹配目录
- `~` 用于正则 URI 前，表示 URI 包含正则表达式，区分大小写
- `~*` 用于正则 URI 前， 表示 URI 包含正则表达式，不区分大小写
- `@` @ 定义一个命名的 location，@ 定义的locaiton名字一般用在内部定向，例如error_page, try_files命令中。它的功能类似于编程中的goto。

location 匹配顺序
nginx 有两层指令来匹配请求 URI。第一个层次是 server 指令，它通过域名、ip 和端口来做第一层级匹配，当找到匹配的 server 后就进入此 server 的 location 匹配。

location 的匹配并不完全按照其在配置文件中出现的顺序来匹配，请求URI 会按如下规则进行匹配：

先精准匹配 =，精准匹配成功则会立即停止其他类型匹配；
没有精准匹配成功时，进行前缀匹配。先查找带有 `^~` 的前缀匹配，带有 `^~` 的前缀匹配成功则立即停止其他类型匹配，普通前缀匹配（不带参数 ^~ ）成功则会暂存，继续查找正则匹配；
= 和 `^~` 均未匹配成功前提下，查找正则匹配 `~` 和 `~*`。当同时有多个正则匹配时，按其在配置文件中出现的先后顺序优先匹配，命中则立即停止其他类型匹配；
所有正则匹配均未成功时，返回步骤 2 中暂存的普通前缀匹配（不带参数 ^~ ）结果
以上规则简单总结就是优先级从高到低依次为（序号越小优先级越高）：

1. location =    # 精准匹配
2. location ^~   # 带参前缀匹配
3. location ~    # 正则匹配（区分大小写）
4. location ~*   # 正则匹配（不区分大小写）
5. location /a   # 普通前缀匹配，优先级低于带参数前缀匹配。
6. location /    # 任何没有匹配成功的，都会匹配这里处理

案例分析
接下来，让我们通过一些实际案例来验证上述规则。

- 案例 1

```bash
server {
    server_name website.com;
    location /doc {
        return 701; # 用这样的方式，可以方便的知道请求到了哪里
    }
    location ~* ^/document$ {
        return 702; 

    }
}
```

curl -I website.com:8080/document 返回 返回 HTTP/1.1 702

说明：按照上述的规则，显然第二个正则匹配会有更高的优先级

- 案例 2

```bash
server {
    server_name website.com;
    location /document {
        return 701;
    }
    location ~* ^/document$ {
        return 702;
    }
}
```

curl -I website.com:8080/document 返回 HTTP/1.1 702

说明：第二个匹配了正则表达式，优先级高于第一个普通前缀匹配

- 案例 3

```bash
server {
    server_name website.com;
    location ^~ /doc {
        return 701;
    }
    location ~* ^/document$ {
        return 702;
    }
}
```

```bash
curl http://website.com/document 返回 HTTP/1.1 701
```

说明：第一个前缀匹配 ^~ 命中以后不会再搜寻正则匹配，所以会第一个命中。

案例 4
server {
    server_name website.com;
    location /docu {
        return 701;
    }
    location /doc {
        return 702;
    }
}
curl -I website.com:8080/document 会返回 HTTP/1.1 701

server {
    server_name website.com;
    location /doc {
        return 702;
    }
    location /docu {
        return 701;
    }
}
curl -I website.com:8080/document 依然返回 HTTP/1.1 701

说明：前缀匹配下，返回最长匹配的 location，与 location 所在位置顺序无关

案例 5
server {
    listen 8080;
    server_name website.com;

    location ~ ^/doc[a-z]+ {
        return 701;
    }

    location ~ ^/docu[a-z]+ {
        return 702;
    }
}
curl -I website.com:8080/document 返回 HTTP/1.1 701

把顺序换一下

server {
    listen 8080;
    server_name website.com;

    location ~ ^/docu[a-z]+ {
        return 702;
    }
    
    location ~ ^/doc[a-z]+ {
        return 701;
    }
}
curl -I website.com:8080/document 返回 HTTP/1.1 702

说明：可见正则匹配是使用文件中的顺序，先匹配成功的返回。

案例 6
最后我们对一个官方文档中提到例子做一些补充，来看一个相对较完整的例子，假设我们有如下几个请求等待匹配：

/
/index.html
/documents/document.html
/documents/abc
/images/a.gif
/documents/a.jpg
以下是 location 配置及其匹配情况


location  = / {
    # 只精准匹配 / 的查询.
  [ configuration A ] 
}
# 匹配成功： / 

location / {
    # 匹配任何请求，因为所有请求都是以”/“开始
    # 但是更长字符匹配或者正则表达式匹配会优先匹配
  [ configuration B ] 
}
#匹配成功：/index.html

location /documents {
    # 匹配任何以 /documents/ 开头的地址，匹配符合以后，还要继续往下搜索/
    # 只有后面的正则表达式没有匹配到时，这一条才会采用这一条/
  [ configuration C ] 
}
# 匹配成功：/documents/document.html
# 匹配成功：/documents/abc

location ~ /documents/ABC {
    # 区分大小写的正则匹配
    # 匹配任何以 /documents/ 开头的地址，匹配符合以后，还要继续往下搜索/
    # 只有后面的正则表达式没有匹配到时，这一条才会采用这一条/
  [ configuration CC ] 
}

location ^~ /images/ {
    # 匹配任何以 /images/ 开头的地址，匹配符合以后，立即停止往下搜索正则，采用这一条。/
  [ configuration D ] 
}
# 成功匹配：/images/a.gif

location ~* \.(gif|jpg|jpeg)$ {
    # 匹配所有以 .gif、.jpg 或 .jpeg 结尾的请求，不区分大小写
    # 然而，所有请求 /images/ 下的图片会被 [ config D ]  处理，因为 ^~ 到达不了这一条正则/
    [ configuration E ] 
}
# 成功匹配：/documents/a.jpg

location /images/ {
    # 字符匹配到 /images/，继续往下，会发现 ^~ 存在/
  [ configuration F ] 
}

location /images/abc {
    # 最长字符匹配到 /images/abc，继续往下，会发现 ^~ 存在/
    # F与G的放置顺序是没有关系的/
  [ configuration G ] 
}

location ~ /images/abc/ {
    # 只有去掉 [ config D ] 才有效：先最长匹配 [ config G ] 开头的地址，继续往下搜索，匹配到这一条正则，采用/
    [ configuration H ] 
}

<https://segmentfault.com/a/1190000022315733>
<https://blog.csdn.net/u011510825/article/details/50531864>

nginx指定文件路径有两种方式 root 和 alias，主要区别在于 nginx 如何解释 location 后面的 uri，这会使两者分别以不同的方式将请求映射到服务器文件上。

## root

语法: root path  
默认值: root html  
配置段: http、server、location、if  

root 示例:

```bash
location ^~ /foo/ {
  root /www/root/html/;
}
```

如果一个请求的 URI 是 /t/a.html 时，web服务器将会返回服务器上的 /www/root/html/foo/a.html 的文件。

## alias
  
语法: alias path  
配置段: location  

alias实例:

```bash
location ^~ /foo/ {
  alias /www/root/html/bar/;
}
```

如果一个请求的 URI 是 /foo/a.html 时，web 服务器将会返回服务器上的 /www/root/html/bar/a.html 的文件。注意这里是 bar, 因为 alias 会把 location 后面配置的路径丢弃掉，把当前匹配到的目录指向到指定的目录。

alias 别名, /foo/ 是 /www/root/html/bar/ 的别名, 客户端访问 /foo/a.html, 服务器返回 /www/root/html/bar/a.html

注意:

1. 使用alias时，目录名后面一定要加"/"。
2. alias在使用正则匹配时，必须捕捉要匹配的内容并在指定的内容处使用。

## 4. alias只能位于location块中。 (root可以不放在location中)

## Nginx 虚拟目录 alias 和 root 目录

nginx 是通过 alias 设置虚拟目录，在 nginx 的配置中，alias 目录和 root 目录是有区别的：

1. alias 指定的目录是准确的，即 location 匹配访问的 path 目录下的文件直接是在 alias 目录下查找的;
2. root 指定的目录是 location 匹配访问的 path 目录的上一级目录, 这个 path 目录一定要是真实存在root指定目录下的;
3. 使用 alias 标签的目录块中不能使用 rewrite 的 break (具体原因不明）；另外，alias指定的目录后面必须要加上"/"符号！！
4）alias虚拟目录配置中，location匹配的path目录如果后面不带"/"，那么访问的url地址中这个path目录后面加不加"/"不影响访问，访问时它会自动加上"/"；
    但是如果location匹配的path目录后面加上"/"，那么访问的url地址中这个path目录必须要加上"/"，访问时它不会自动加上"/"。如果不加上"/"，访问就会失败！
5）root目录配置中，location匹配的path目录后面带不带"/"，都不会影响访问。

<https://www.cnblogs.com/kevingrace/p/6187482.html>

作者: 果汁华  
来源: CSDN  
原文: <https://blog.csdn.net/u011510825/article/details/50531864>  
版权声明: 本文为博主原创文章，转载请附上博文链接！  
