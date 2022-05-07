---
title: netty http client
author: "-"
date: 2015-12-17T01:29:08+00:00
url: /?p=8569
categories:
  - Inbox
tags:
  - reprint
---
## netty http client

<http://www.cnblogs.com/luxiaoxun/p/3959450.html>

基于Netty4的HttpServer和HttpClient的简单实现

Netty的主页: <http://netty.io/index.html>

使用的Netty的版本: netty-4.0.23.Final.tar.bz2 ‐ 15-Aug-2014 (Stable, Recommended)

Http 消息格式:

Http request:

Method path-to-resource HTTPVersion-number
  
Header-name-1: value1
  
Header-name-2: value2

Optional request body
  
Http response:

HTTP/Version-number response-code response-phrase
  
Header-name-1: value1
  
Header-name-2: value2

Optional response body
  
实现一个简单的Http请求及响应过程:

1. Client向Server发送http请求。

2. Server端对http请求进行解析。

3. Server端向client发送http响应。

4. Client对http响应进行解析。

Netty中Http request消息格式:

Netty中Http response消息格式:

代码实例:

Http Server:
  
package com.netty.test;

import org.apache.commons.logging.Log;
  
import org.apache.commons.logging.LogFactory;

import io.netty.bootstrap.ServerBootstrap;
  
import io.netty.channel.ChannelFuture;
  
import io.netty.channel.ChannelInitializer;
  
import io.netty.channel.ChannelOption;
  
import io.netty.channel.EventLoopGroup;
  
import io.netty.channel.nio.NioEventLoopGroup;
  
import io.netty.channel.socket.SocketChannel;
  
import io.netty.channel.socket.nio.NioServerSocketChannel;
  
import io.netty.handler.codec.http.HttpRequestDecoder;
  
import io.netty.handler.codec.http.HttpResponseEncoder;

public class HttpServer {

private static Log log = LogFactory.getLog(HttpServer.class);

public void start(int port) throws Exception {
  
EventLoopGroup bossGroup = new NioEventLoopGroup();
  
EventLoopGroup workerGroup = new NioEventLoopGroup();
  
try {
  
ServerBootstrap b = new ServerBootstrap();
  
b.group(bossGroup, workerGroup).channel(NioServerSocketChannel.class)
  
.childHandler(new ChannelInitializer<SocketChannel>() {
  
@Override
  
public void initChannel(SocketChannel ch) throws Exception {
  
// server端发送的是httpResponse,所以要使用HttpResponseEncoder进行编码
  
ch.pipeline().addLast(new HttpResponseEncoder());
  
// server端接收到的是httpRequest,所以要使用HttpRequestDecoder进行解码
  
ch.pipeline().addLast(new HttpRequestDecoder());
  
ch.pipeline().addLast(new HttpServerInboundHandler());
  
}
  
}).option(ChannelOption.SO_BACKLOG, 128)
  
.childOption(ChannelOption.SO_KEEPALIVE, true);

ChannelFuture f = b.bind(port).sync();

f.channel().closeFuture().sync();
  
} finally {
  
workerGroup.shutdownGracefully();
  
bossGroup.shutdownGracefully();
  
}
  
}

public static void main(String[] args) throws Exception {
  
HttpServer server = new HttpServer();
  
log.info("Http Server listening on 8844 ...");
  
server.start(8844);
  
}
  
}

响应请求的HttpServerInboundHandler:
  
package com.netty.test;

import static io.netty.handler.codec.http.HttpHeaders.Names.CONNECTION;
  
import static io.netty.handler.codec.http.HttpHeaders.Names.CONTENT_LENGTH;
  
import static io.netty.handler.codec.http.HttpHeaders.Names.CONTENT_TYPE;
  
import static io.netty.handler.codec.http.HttpResponseStatus.OK;
  
import static io.netty.handler.codec.http.HttpVersion.HTTP_1_1;

import org.apache.commons.logging.Log;
  
import org.apache.commons.logging.LogFactory;

import io.netty.buffer.ByteBuf;
  
import io.netty.buffer.Unpooled;
  
import io.netty.channel.ChannelHandlerContext;
  
import io.netty.channel.ChannelInboundHandlerAdapter;
  
import io.netty.handler.codec.http.DefaultFullHttpResponse;
  
import io.netty.handler.codec.http.FullHttpResponse;
  
import io.netty.handler.codec.http.HttpContent;
  
import io.netty.handler.codec.http.HttpHeaders;
  
import io.netty.handler.codec.http.HttpHeaders.Values;
  
import io.netty.handler.codec.http.HttpRequest;

public class HttpServerInboundHandler extends ChannelInboundHandlerAdapter {

private static Log log = LogFactory.getLog(HttpServerInboundHandler.class);

private HttpRequest request;

@Override
  
public void channelRead(ChannelHandlerContext ctx, Object msg)
  
throws Exception {
  
if (msg instanceof HttpRequest) {
  
request = (HttpRequest) msg;

String uri = request.getUri();
  
System.out.println("Uri:" + uri);
  
}
  
if (msg instanceof HttpContent) {
  
HttpContent content = (HttpContent) msg;
  
ByteBuf buf = content.content();
  
System.out.println(buf.toString(io.netty.util.CharsetUtil.UTF_8));
  
buf.release();

String res = "I am OK";
  
FullHttpResponse response = new DefaultFullHttpResponse(HTTP_1_1,
  
OK, Unpooled.wrappedBuffer(res.getBytes("UTF-8")));
  
response.headers().set(CONTENT_TYPE, "text/plain");
  
response.headers().set(CONTENT_LENGTH,
  
response.content().readableBytes());
  
if (HttpHeaders.isKeepAlive(request)) {
  
response.headers().set(CONNECTION, Values.KEEP_ALIVE);
  
}
  
ctx.write(response);
  
ctx.flush();
  
}
  
}

@Override
  
public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
  
ctx.flush();
  
}

@Override
  
public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
  
log.error(cause.getMessage());
  
ctx.close();
  
}

}

Http Client:

按 Ctrl+C 复制代码
  
按 Ctrl+C 复制代码
  
处理Server响应的HttpClientInboundHandler:

按 Ctrl+C 复制代码
  
按 Ctrl+C 复制代码
  
log4j的配置:

# Root logger option
  
log4j.rootLogger=INFO, stdout, file

# Direct log messages to stdout
  
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
  
log4j.appender.stdout.Target=System.out
  
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
  
log4j.appender.stdout.layout.ConversionPattern=%d{ABSOLUTE} %5p %c{1}:%L - %m%n

log4j.appender.file = org.apache.log4j.DailyRollingFileAppender
  
log4j.appender.file.File = logs/log.log
  
log4j.appender.file.Append = true
  
log4j.appender.file.Threshold = INFO
  
log4j.appender.file.layout = org.apache.log4j.PatternLayout
  
log4j.appender.file.layout.ConversionPattern = %-d{yyyy-MM-dd HH:mm:ss} %5p %c{1}:%L - %m%n
