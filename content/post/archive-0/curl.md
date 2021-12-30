---
title: curl
author: "-"
date: 2011-11-24T12:47:12+00:00
url: curl
categories:
  - Linux
  - Web
tags:
  - remix

---
## curl
### 追踪重定向 -L
    curl -L xxx
### post request
可以用 -X POST 来声明请求方法，用 -d 参数传送参数, 使用 -d 时, 默认为POST请求, -X POST 可以省略

    curl -d "user=admin&passwd=12345678" http://127.0.0.1:8080/login
    # 把请求参数放到文件里, foo 是一个包含请求数据的文件
    curl -i -XPOST 'http://localhost:8186/write?db=db0' --data-binary @foo  

### with header
    curl -H "Content-Type: application/json"  \
    -d "user=nickwolfe&password=12345" http://www.yahoo.com/login.cgi

### use proxy
#### 用 -x 参数 
```bash
-x, --proxy [protocol://]host[:port]
curl -x http://127.0.0.1:8899 http://www.baidu.com
```
#### 或者在环境变量里设置proxy
```bash
http_proxy=http://127.0.0.1:1080 curl -v http://www.baidu.com

# todo, export之后 curl 不会走这个代理....
export http_proxy=http://127.0.0.1:1080
curl -v http://www.baidu.com

```
#### socks5 proxy
```bash
curl -x socks5h://localhost:8001 http://www.google.com/
curl -x socks5://localhost:8888 http://google.com
```

### url encoding

```bash
# --data-urlencode 要跟 -G 配合使用
curl -G -v "http://localhost:30001/data" --data-urlencode "msg=hello world" --data-urlencode "msg2=hello world2"

> GET /data?msg=hello%20world&msg2=hello%20world2 HTTP/1.1
> User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu)
> Host: localhost
> Accept: */*
```

https://unix.stackexchange.com/questions/86729/any-way-to-encode-the-url-in-curl-command

### 格式化返回的json数据
    curl http://foo.com/bar | jq .
    
### 限制下载速率
    curl "http://toutiao.sogoucdn.com/ykvideo/20181130/0575139af28f38c336912739acf33a88.mp4" -o video --limit-rate 100k


```bash
curl http://foo.wiloon.com -v --retry 0 --connect-timeout 1

# dns, 不依赖/etc/hosts
curl --resolve 'test.com:9443:127.0.0.1' https://test.com:9443/hello

# -x 代理服务器
curl -x 123.45.67.89:1080 -o page.html http://www.yahoo.com

# 下载文件
curl -o foo.txt http://foo.com/foo.txt
curl -v --socks5-hostname 127.0.0.1:1080 https://www.google.com/

# --connect-timeout <seconds>
# -G/--get 以get的方式来发送数据
# -i, --include 输出时包括protocol头信息, 显示response header
# -v, verbos
# -N, Disables the buffering of the output stream
# -H, --header LINE Custom header to pass to server (H)
# -d, --data DATA HTTP POST data, 如果使用-d命令，curl会以application/x-www-url-encoded格式上传参数。
# -o, --output <file>, write  output to <file> instead of stdout.
# --retry, 重试次数

如果使用了-F参数，curl会以multipart/form-data的方式发送POST请求。-F以key=value的形式指定要上传的参数，如果是文件，则需要使用key=@file的形式。

```
### websocket

```bash
curl --include \
     --no-buffer \
     --header "Connection: Upgrade" \
     --header "Upgrade: websocket" \
     --header "Host: example.com:80" \
     --header "Origin: http://example.com:80" \
     --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
     --header "Sec-WebSocket-Version: 13" \
     http://example.com:80/

```

```bash
curl -v -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: 127.0.0.1:8088" -H "Sec-WebSocket-Key: lkUx3lTpjFwO5OI7xY3+1Q==" -H "Sec-WebSocket-Version: 13" http://127.0.0.1:8088/

```

Upgrade 表示升级到 WebSocket 协议，
  
Connection 表示这个 HTTP 请求是一次协议升级，
  
Origin 表示发请求的来源。

* * *

作者: sd2131512
  
来源: CSDN
  
原文: https://blog.csdn.net/sd2131512/article/details/74996577
  
版权声明: 本文为博主原创文章，转载请附上博文链接！


4)
  
访问有些网站的时候比较讨厌，他使用cookie来记录session信息。
  
像IE/NN这样的浏览器，当然可以轻易处理cookie信息，但我们的curl呢？…..
  
我们来学习这个option: -D <– 这个是把http的response里面的cookie信息存到一个特别的文件中去

curl -x 123.45.67.89:1080 -o page.html -D cookie0001.txt http://www.yahoo.com
  
这样，当页面被存到page.html的同时，cookie信息也被存到了cookie0001.txt里面了

5) 
  
那么，下一次访问的时候，如何继续使用上次留下的cookie信息呢？要知道，很多网站都是靠监视你的cookie信息，
  
来判断你是不是不按规矩访问他们的网站的。
  
这次我们使用这个option来把上次的cookie信息追加到http request里面去:  -b

curl -x 123.45.67.89:1080 -o page1.html -D cookie0002.txt -b cookie0001.txt http://www.yahoo.com
  
这样，我们就可以几乎模拟所有的IE操作，去访问网页了！

6) 
  
稍微等等~~~~~我好像忘记什么了~~~~~
  
对了！是浏览器信息~~~~

有些讨厌的网站总要我们使用某些特定的浏览器去访问他们，有时候更过分的是，还要使用某些特定的版本~~~~
  
NND，哪里有时间为了它去找这些怪异的浏览器呢！？

好在curl给我们提供了一个有用的option，可以让我们随意指定自己这次访问所宣称的自己的浏览器信息:  -A

curl -A "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)" -x 123.45.67.89:1080 -o page.html -D cookie0001.txt http://www.yahoo.com
  
这样，服务器端接到访问的要求，会认为你是一个运行在Windows 2000上的IE6.0，嘿嘿嘿，其实也许你用的是苹果机呢！

而"Mozilla/4.73 [en] (X11; U; Linux 2.2; 15 i686″则可以告诉对方你是一台PC上跑着的Linux，用的是Netscape 4.73，呵呵呵

7) 
  
另外一个服务器端常用的限制方法，就是检查http访问的referer。比如你先访问首页，再访问里面所指定的下载页，这第二次访问的referer地址就是第一次访问成功后的页面地址。这样，服务器端只要发现对下载页面某次访问的referer地址不 是首页的地址，就可以断定那是个盗连了~~~~~

讨厌讨厌~~~我就是要盗连~~~~~！！
  
幸好curl给我们提供了设定referer的option:  -e

curl -A "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)" -x 123.45.67.89:1080 -e "mail.yahoo.com" -o page.html -D cookie0001.txt http://www.yahoo.com
  
这样，就可以骗对方的服务器，你是从mail.yahoo.com点击某个链接过来的了，呵呵呵

8) 
  
写着写着发现漏掉什么重要的东西了！—– 利用curl 下载文件

刚才讲过了，下载页面到一个文件里，可以使用 -o ，下载文件也是一样。
  
比如，

curl -o 1.jpg http://cgi2.tky.3web.ne.jp/~zzh/screen1.JPG
  
这里教大家一个新的option:  -O
  
大写的O，这么用: 

curl -O http://cgi2.tky.3web.ne.jp/~zzh/screen1.JPG
  
这样，就可以按照服务器上的文件名，自动存在本地了！

再来一个更好用的。
  
如果screen1.JPG以外还有screen2.JPG、screen3.JPG、….、screen10.JPG需要下载，难不成还要让我们写一个script来完成这些操作？
  
不干！
  
在curl里面，这么写就可以了: 

curl -O http://cgi2.tky.3web.ne.jp/~zzh/screen[1-10].JPG
  
呵呵呵，厉害吧？！~~~

9) 
  
再来，我们继续讲解下载！

curl -O http://cgi2.tky.3web.ne.jp/~{zzh,nick}/[001-201].JPG
  
这样产生的下载，就是
  
~zzh/001.JPG
  
~zzh/002.JPG
  
…
  
~zzh/201.JPG
  
~nick/001.JPG
  
~nick/002.JPG
  
…
  
~nick/201.JPG

够方便的了吧？哈哈哈

咦？高兴得太早了。
  
由于zzh/nick下的文件名都是001，002…，201，下载下来的文件重名，后面的把前面的文件都给覆盖掉了~~~

没关系，我们还有更狠的！

curl -o #2_#1.jpg http://cgi2.tky.3web.ne.jp/~{zzh,nick}/[001-201].JPG
  
–这是…..自定义文件名的下载？
  
–对头，呵呵！

#1是变量，指的是{zzh,nick}这部分，第一次取值zzh，第二次取值nick
  
#2代表的变量，则是第二段可变部分—[001-201]，取值从001逐一加到201
  
这样，自定义出来下载下来的文件名，就变成了这样: 
  
原来:  ~zzh/001.JPG —> 下载后:  001-zzh.JPG
  
原来:  ~nick/001.JPG —> 下载后:  001-nick.JPG

这样一来，就不怕文件重名啦，呵呵

9) 
  
继续讲下载
  
我们平时在windows平台上，flashget这样的工具可以帮我们分块并行下载，还可以断线续传。
  
curl在这些方面也不输给谁，嘿嘿

比如我们下载screen1.JPG中，突然掉线了，我们就可以这样开始续传

curl -c -O http://cgi2.tky.3wb.ne.jp/~zzh/screen1.JPG
  
当然，你不要拿个flashget下载了一半的文件来糊弄我~~~~别的下载软件的半截文件可不一定能用哦~~~

分块下载，我们使用这个option就可以了:  -r
  
举例说明
  
比如我们有一个http://cgi2.tky.3web.ne.jp/~zzh/zhao1.mp3 要下载
  
我们就可以用这样的命令: 

curl -r 0-10240 -o "zhao.part1" http:/cgi2.tky.3web.ne.jp/~zzh/zhao1.mp3 &
  
curl -r 10241-20480 -o "zhao.part1" http:/cgi2.tky.3web.ne.jp/~zzh/zhao1.mp3 &
  
curl -r 20481-40960 -o "zhao.part1" http:/cgi2.tky.3web.ne.jp/~zzh/zhao1.mp3 &
  
curl -r 40961- -o "zhao.part1" http:/cgi2.tky.3web.ne.jp/~zzh/zhao1.mp3
  
这样就可以分块下载啦。
  
不过你需要自己把这些破碎的文件合并起来
  
如果你用UNIX或苹果，用 cat zhao.part* > zhao.mp3就可以
  
如果用的是Windows，用copy /b 来解决吧，呵呵

上面讲的都是http协议的下载，其实ftp也一样可以用。
  
用法嘛，

curl -u name:passwd ftp://ip:port/path/file
  
或者大家熟悉的

curl ftp://name:passwd@ip:port/path/file
  
10)
  
说完了下载，接下来自然该讲上传咯
  
上传的option是 -T

比如我们向ftp传一个文件: 

curl -T localfile -u name:passwd ftp://upload_site:port/path/
  
当然，向http服务器上传文件也可以
  
比如

curl -T localfile http://cgi2.tky.3web.ne.jp/~zzh/abc.cgi
  
注意，这时候，使用的协议是HTTP的PUT method

刚才说到PUT，嘿嘿，自然让老服想起来了其他几种methos还没讲呢！
  
GET和POST都不能忘哦。

http提交一个表单，比较常用的是POST模式和GET模式

GET模式什么option都不用，只需要把变量写在url里面就可以了
  
比如: 

curl http://www.yahoo.com/login.cgi?user=nickwolfe&password=12345
  
而POST模式的option则是 -d

curl -d "user=nickwolfe&password=12345" http://www.yahoo.com/login.cgi
  
就相当于向这个站点发出一次登陆申请~~~~~

到底该用GET模式还是POST模式，要看对面服务器的程序设定。

一点需要注意的是，POST模式下的文件上的文件上传，比如

这样一个HTTP表单，我们要用curl进行模拟，就该是这样的语法: 

curl -F upload=@localfile -F nick=go http://cgi2.tky.3web.ne.jp/~zzh/up_file.cgi
  
罗罗嗦嗦讲了这么多，其实curl还有很多很多技巧和用法
  
比如 https的时候使用本地证书，就可以这样

curl -E localcert.pem https://remote_server
  
再比如，你还可以用curl通过dict协议去查字典~~~~~

curl dict://dict.org/d:computer
  
今天就先讲到这里吧，呵呵。疯狂的curl功能，需要你—一起来发掘。

---

http://www.ruanyifeng.com/blog/2011/09/curl.html
  
http://blog.51cto.com/xoyabc/1950743
  
https://blog.csdn.net/dreamer2020/article/details/52050001