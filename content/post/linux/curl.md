---
title: curl
author: "-"
date: 2022-04-18 22:48:04
url: curl
categories:
  - Linux
  - Web
tags:
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
-m, --max-time <fractional seconds>, 传输超时, 比如 http请求发送之后长时间没有响应, tcp 的 ack收到了, 但是长时间没收到 http response.
-G/--get 以get的方式来发送数据
-i, --include 输出时包括 protocol 头信息, 显示 response header
-v, verbos
-N, Disables the buffering of the output stream
-H, --header LINE Custom header to pass to server (H)
-d, --data DATA HTTP POST data, 如果使用-d命令，curl会以application/x-www-url-encoded格式上传参数。
--retry, 重试次数
# 如果使用了-F参数，curl会以multipart/form-data的方式发送POST请求。-F以key=value的形式指定要上传的参数，如果是文件，则需要使用key=@file的形式。
-k or --insecure flag to skip certificate validation.
-L,--location:如果服务器报告请求的页面已移动到其他位置（用location:header和3xx 响应代码），此选项将使curl在新位置上重新执行请求。
-X, --request <method>   Specify request method to use

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

### 追踪重定向 -L

```bash
curl -L xxx
```

## POST

用 -d 传 POST 参数  
可以用 -X POST 来声明请求方法, 使用 -d 时, 默认为 POST 请求, -X POST 可以省略  
发送 POST 请求时 Content-Type 默认是 application/x-www-form-urlencoded  

```bash
curl -d "user=admin&passwd=12345678" http://127.0.0.1:8080/login
# 把请求参数放到文件里, foo 是一个包含请求数据的文件
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
