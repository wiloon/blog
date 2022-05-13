---
date: "2020-05-15T10:16:43Z"
title: "OkHttp"
categories:
  - inbox
tags:
  - reprint
---
## "OkHttp"
https://github.com/square/okhttp

```java
    RequestBody body = RequestBody.create(MediaTypeJson, jsonStr0);
    Request request = new Request.Builder()
            .url(url0)
            .post(body)
            .build();
    String resp = null;

    try (Response response = client.newCall(request).execute()) {
        resp = response.body().string();
    } catch (IOException e) {
        e.printStackTrace();
    }

```

### proxy
```java
    static Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress("127.0.0.1", 8899));
    static OkHttpClient client = new OkHttpClient.Builder().proxy(proxy).build();
```

### 1. 历史上Http请求库优缺点

在讲述OkHttp之前, 我们看下没有OkHttp的时代, 我们是如何完成http请求的.  
 在没有OkHttp的日子, 我们使用`HttpURLConnection`或者`HttpClient`. 那么这两者都有什么优缺点呢? 为什么不在继续使用下去呢?  
 `HttpClient`是Apache基金会的一个开源网络库, 功能十分强大, API数量众多, 但是正是由于庞大的API数量使得我们很难在不破坏兼容性的情况下对它进行升级和扩展, 所以Android团队在提升和优化HttpClient方面的工作态度并不积极.  
 `HttpURLConnection`是一种多用途, 轻量极的HTTP客户端, 提供的API比较简单, 可以容易地去使用和扩展. 不过在Android 2.2版本之前, `HttpURLConnection`一直存在着一些令人厌烦的bug. 比如说对一个可读的InputStream调用close()方法时，就有可能会导致连接池失效了。那么我们通常的解决办法就是直接禁用掉连接池的功能: 

    private void disableConnectionReuseIfNecessary() {    
        // 这是一个2.2版本之前的bug    
        if (Integer.parseInt(Build.VERSION.SDK) < Build.VERSION_CODES.FROYO) {    
            System.setProperty("http.keepAlive", "false");    
        }    
    }    
    

因此, 一般的推荐是在2.2之前, 使用`HttpClient`, 因为其bug较少. 在2.2之后, 推荐使用`HttpURLConnection`, 因为API简单, 体积小, 并且有压缩和缓存机制, 并且Android团队后续会继续优化`HttpURLConnection`.

但是, 上面两个类库和`OkHttp`比起来就弱爆了, 因为OkHttp不仅具有高效的请求效率, 并且提供了很多开箱即用的网络疑难杂症解决方案.

* 支持HTTP/2, HTTP/2通过使用多路复用技术在一个单独的TCP连接上支持并发, 通过在一个连接上一次性发送多个请求来发送或接收数据
* 如果HTTP/2不可用, 连接池复用技术也可以极大减少延时
* 支持GZIP, 可以压缩下载体积
* 响应缓存可以直接避免重复请求
* 会从很多常用的连接问题中自动恢复
* 如果您的服务器配置了多个IP地址, 当第一个IP连接失败的时候, OkHttp会自动尝试下一个IP
* OkHttp还处理了代理服务器问题和SSL握手失败问题

使用 OkHttp 无需重写您程序中的网络代码。OkHttp实现了几乎和java.net.HttpURLConnection一样的API。如果你用了 Apache HttpClient，则OkHttp也提供了一个对应的okhttp-apache 模块。

还有一个好消息, 从Android 4.4起, 其`HttpURLConnection`的内部实现已经变为`OkHttp`, 您可以参考这两个网页:[爆栈网](https://link.jianshu.com?t=http://stackoverflow.com/questions/26000027/does-android-use-okhttp-internally)和[Twitter](https://link.jianshu.com?t=https://twitter.com/JakeWharton/status/482563299511250944).
  
  
作者: oncealong  
链接: [https://www.jianshu.com/p/ca8a982a116b](https://www.jianshu.com/p/ca8a982a116b "https://www.jianshu.com/p/ca8a982a116b")  
来源: 简书  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

https://zhuanlan.zhihu.com/p/338207928

