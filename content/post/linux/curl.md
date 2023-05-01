---
title: curl
author: "-"
date: 2022-04-18 22:48:04
url: curl
categories:
  - Commands
tags:
  - reprint
  - remix
---
## curl

curl [kɜrl]

## options

```bash
-s, --silent, 不显示下载进度
-C, --continue-at, 断点续传
-o, --output <file>, write  output to <file> instead of stdout
--connect-timeout <fractional seconds>, 建连接超时, 比如 tcp 三次握手
-m, --max-time <fractional seconds>, 传输超时, 比如 http 请求发送之后长时间没有响应, tcp 的 ack 收到了, 但是长时间没收到 http response.
-G/--get 以 get 的方式来发送数据
-i, --include 输出时包括 protocol 头信息, 显示 response header
-v, verbos
-N, Disables the buffering of the output stream
-H, --header LINE Custom header to pass to server (H)
-d, --data # DATA HTTP POST data, 如果使用 -d 命令，curl 会以 application/x-www-url-encoded 格式上传参数。 从文件中读取数据 -d @/path/to/foo.json
--retry, 重试次数
# 如果使用了 -F 参数，curl 会以 multipart/form-data 的方式发送 POST 请求。-F 以 key=value 的形式指定要上传的参数，如果是文件，则需要使用 key=@file 的形式。
-k, --insecure flag to skip certificate validation.
-L, --location: 追踪重定向, 如果服务器报告请求的页面已移动到其他位置（用 location: header 和 3xx 响应代码），此选项将使 curl 在新位置上重新执行请求。
-X, --request <method>   Specify request method to use
-w, 完成请求传输后，使 curl 在 stdout 上显示自定义信息
--cacert, curl 用来验证对端的 CA 证书
-E, --cert, 客户端证书
--key, 客户端私钥
--pass, 客户端私钥的密码
--trace-ascii /tmp/curl.log, 把交互的数据打印到日志里, https 协议也能把明文打在日志里
```

## -w

-w 的作用
完成请求传输后，使 curl 在 stdout 上显示自定义信息
格式是一个字符串，可以包含纯文本和任意数量的变量

输出格式
输出格式中的变量会被 curl 用对应的值替换掉
所有变量的格式为： %{variable name}
要输出一个普通的 % 只需将它们写为 %%
可以使用 \n、带 \r 的回车符和带 \t 的制表符来输出换行符
如果想通过文件来传入变量，可以用 @filename 的格式

### -w 参数对应的一些变量

url_effective 最终获取的url地址，尤其是当你指定给curl的地址存在301跳转，且通过-L继续追踪的情形。
http_code http状态码，如200成功,301转向,404未找到,500服务器错误等。(The numerical response code that was found in the last retrieved HTTP(S) or FTP(s) transfer. In 7.18.2 the alias response_code was added to show the same info.)
http_connect The numerical code that was found in the last response (from a proxy) to a curl CONNECT request. (Added in 7.12.4)
time_total 总时间，按秒计。精确到小数点后三位。 （The total time, in seconds, that the full operation lasted. The time will be displayed with millisecond resolution.）
time_namelookup DNS解析时间,从请求开始到DNS解析完毕所用时间。(The time, in seconds, it took from the start until the name resolving was completed.)
time_connect 连接时间,从开始到建立TCP连接完成所用时间,包括前边DNS解析时间，如果需要单纯的得到连接时间，用这个time_connect时间减去前边time_namelookup时间。以下同理，不再赘述。(The time, in seconds, it took from the start until the TCP connect to the remote host (or proxy) was completed.)
time_appconnect 连接建立完成时间，如SSL/SSH等建立连接或者完成三次握手时间。(The time, in seconds, it took from the start until the SSL/SSH/etc connect/handshake to the remote host was completed. (Added in 7.19.0))
time_pretransfer 从开始到准备传输的时间。(The time, in seconds, it took from the start until the file transfer was just about to begin. This includes all pre-transfer commands and negotiations that are specific to the particular protocol(s) involved.)
time_redirect 重定向时间，包括到最后一次传输前的几次重定向的DNS解析，连接，预传输，传输时间。(The time, in seconds, it took for all redirection steps include name lookup, connect, pretransfer and transfer before the final transaction was started. time_redirect shows the complete execution time for multiple redirections. (Added in 7.12.3))
time_starttransfer 开始传输时间。在发出请求之后，Web 服务器返回数据的第一个字节所用的时间(The time, in seconds, it took from the start until the first byte was just about to be transferred. This includes time_pretransfer and also the time the server needed to calculate the result.)
size_download 下载大小。(The total amount of bytes that were downloaded.)
size_upload 上传大小。(The total amount of bytes that were uploaded.)
size_header 下载的header的大小(The total amount of bytes of the downloaded headers.)
size_request 请求的大小。(The total amount of bytes that were sent in the HTTP request.)
speed_download 下载速度，单位-字节每秒。(The average download speed that curl measured for the complete download. Bytes per second.)
speed_upload 上传速度,单位-字节每秒。(The average upload speed that curl measured for the complete upload. Bytes per second.)
content_type 就是content-Type，不用多说了，这是一个访问我博客首页返回的结果示例(text/html; charset=UTF-8)；(The Content-Type of the requested document, if there was any.)
num_connects 最近的的一次传输中创建的连接数目。Number of new connects made in the recent transfer. (Added in 7.12.3)
num_redirects 在请求中跳转的次数。Number of redirects that were followed in the request. (Added in 7.12.3)
redirect_url When a HTTP request was made without -L to follow redirects, this variable will show the actual URL a redirect would take you to. (Added in 7.18.2)
ftp_entry_path 当连接到远程的ftp服务器时的初始路径。The initial path libcurl ended up in when logging on to the remote FTP server. (Added in 7.15.4)
ssl_verify_result ssl认证结果，返回0表示认证成功。( The result of the SSL peer certificate verification that was requested. 0 means the verification was successful. (Added in 7.19.0))
————————————————
版权声明：本文为CSDN博主「weifangan」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/weifangan/article/details/80741981>

```bash
curl -w http_code: %{http_code} wiloon.com
curl -o /dev/null -s -w "time_connect: %{time_connect}\ntime_starttransfer: %{time_starttransfer}\ntime_nslookup:%{time_namelookup}\ntime_total: %{time_total}\n" "https://api.weixin.qq.com"
```

## 断点续传

```bash
# -C -, curl 自动检测续传位置
curl -C - "http://foo.bar"
```

## cookie

### cookie, 发送请求时附带 cookie, cookie 值从登录请求返回的 `Set-Cookie:` 里取

```bash
curl -v -d "name=admin&password=admin" -b cookie.txt "http://localhost:8080/user/login"
curl -v --cookie "JSESSIONID=C62172C780C581AE8212836C5F4A13EB" "http://localhost:8080/get"
```

#### 保存 cookie 到文件

```bash
curl -v -d "name=admin&password=admin" -b cookie.txt -c cookie.txt "http://localhost:8080/user/login"
```

#### 从文件读取 cookie

```bash
curl -v --cookie cookie.txt "http://localhost:8080/get"
curl -v -b cookie.txt "http://localhost:8080/get"
```

#### 完整版本

```bash
curl -v -d "name=admin&password=admin" -b cookie.txt -c cookie.txt "http://localhost:8080/user/login" && curl -v -b cookie.txt "http://localhost:8080/get"
```

<https://stackoverflow.com/questions/30760213/save-cookies-between-two-curl-requests/37127263>

## POST

用 -d 传 POST 参数  
可以用 -X POST 来声明请求方法, 使用 -d 时, 默认为 POST 请求, -X POST 可以省略  
发送 POST 请求时 Content-Type 默认是 application/x-www-form-urlencoded  

```bash
curl -d "user=admin&passwd=12345678" http://127.0.0.1:8080/login
# 把请求参数放到文件里, foo 是一个包含请求数据的文件, --data-binary 参数可以从磁盘读 post body, --data-raw 不行.
curl -i -XPOST 'http://localhost:8186/write?db=db0' --data-binary @foo

curl -X POST https://reqbin.com/echo/post/json -H "Content-Type: application/json" -d '{"productId": 123456, "quantity": 100}'  

curl -X POST --cookie "session=61122afb-8aae-4125-b6fa-da6919e6fb67" -H "Content-Type: application/json"  "http://localhost/api/foo/" --data-binary '{"productId": 123456, "quantity": 100}'   | jq .

```

## header

```bash
curl -H "Content-Type: application/json"  \
-d "user=nickwolfe&password=12345" http://www.yahoo.com/login.cgi
```

## use proxy

### 用 -x 参数

```bash
-x, --proxy [protocol://]host[:port]
curl -x http://127.0.0.1:8899 http://www.baidu.com
```

#### 或者在环境变量里设置 proxy

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
# socks5(本地解析hostname), socks5h(由socks server解析hostname)
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

<https://unix.stackexchange.com/questions/86729/any-way-to-encode-the-url-in-curl-command>

### 格式化返回的json数据

```bash
    curl http://foo.com/bar | jq .
```

### 限制下载速率

```bash
curl "http://toutiao.sogoucdn.com/ykvideo/20181130/0575139af28f38c336912739acf33a88.mp4" -o video --limit-rate 100k
```

```bash
curl http://foo.wiloon.com -v --retry 0 --connect-timeout 1

# dns, 不依赖 /etc/hosts
curl --resolve 'test.com:9443:127.0.0.1' https://test.com:9443/hello

# -x 代理服务器
curl -x 123.45.67.89:1080 -o page.html http://www.yahoo.com

# 下载文件
# 指定文件名
curl -o foo.txt http://foo.com/foo.txt
# 从 URL里取文件名
curl -O http://foo.com/foo.txt
# 从 Content-Disposition 里取文件名
curl -O -J  "http://localhost:63005/file-server?name=foo.txt"

curl -v --socks5-hostname 127.0.0.1:1080 https://www.google.com/

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

<http://www.ruanyifeng.com/blog/2011/09/curl.html>
  
<http://blog.51cto.com/xoyabc/1950743>
  
<https://blog.csdn.net/dreamer2020/article/details/52050001>

## libcurl error codes

- CURLE_COULDNT_RESOLVE_HOST (6) Could not resolve host. The given remote host was not resolved. 无法解析主机
- CURLE_COULDNT_CONNECT (7) Failed to connect() to host or proxy. 无法连接到主机或代理, 在服务器端, 目标端口没有监听.
- CURLE_OPERATION_TIMEDOUT (28) Operation timeout. The specified time-out period was reached according to the conditions. 建立连接时 tcp SYN 没有响应超过 n秒, 服务器响应时间超过 `-m, --max-time`
- CURLE_RECV_ERROR (56), Failure with receiving network data. 户端向服务器发送POST请求，服务器未响应，6 次TCP重传无响应后，【libcurl】判定HTTP数据接收失败。 <https://blog.csdn.net/wjb123sw99/article/details/103946046>

<https://curl.se/libcurl/c/libcurl-errors.html>

<https://curl.se>

<https://curl.se/docs/manpage.html>

## 双向验证

```bash
curl --cert client.crt --key client.key --pass password0 "https://test.wiloon.com/foo"
curl --cacert server.crt --cert client.crt --key client.key --pass password0 "https://test.wiloon.com/foo"
```

## --trace-ascii

```bash
# - 打印到 std
curl --trace-ascii - https://www.wiloon.com
# 打印到文件
curl --trace-ascii /tmp/foo.txt https://www.wiloon.com
```
