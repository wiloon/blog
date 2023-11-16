---
title: Netty 下载文件
author: "-"
date: 2015-09-17T10:42:40+00:00
url: /?p=8299
categories:
  - Inbox
tags:
  - reprint
---
## Netty 下载文件

[http://www.open-open.com/lib/view/open1409642102932.html](http://www.open-open.com/lib/view/open1409642102932.html)

本实例主要参考的是官网的examples: 点击这里使用场景: 客户端向Netty请求一个文件,Netty服务端下载指定位置文件到客户端。

本实例使用的是Http协议,当然,可以通过简单的修改即可换成TCP协议。

需要注意本实例的关键点是,为了更高效的传输大数据,实例中用到了ChunkedWriteHandler编码器,它提供了以zero-memory-copy方式写文件。

第一步: 先写一个HttpFileServer

?
  
package NettyDemo.file.server;

import io.netty.bootstrap.ServerBootstrap;
  
import io.netty.channel.Channel;
  
import io.netty.channel.ChannelInitializer;
  
import io.netty.channel.ChannelPipeline;
  
import io.netty.channel.EventLoopGroup;
  
import io.netty.channel.nio.NioEventLoopGroup;
  
import io.netty.channel.socket.SocketChannel;
  
import io.netty.channel.socket.nio.NioServerSocketChannel;
  
import io.netty.handler.codec.http.HttpObjectAggregator;
  
import io.netty.handler.codec.http.HttpServerCodec;
  
import io.netty.handler.logging.LogLevel;
  
import io.netty.handler.logging.LoggingHandler;
  
import io.netty.handler.stream.ChunkedWriteHandler;

/***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\****
  
* Reserved. BidPlanStructForm.java Created on 2014-8-19 Author: <a
  
* href=mailto:wanghouda@126.com>wanghouda
  
* @Title: HttpFileServer.java
  
* @Package NettyDemo.file.server Description: Version: 1.0
  
\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***/
  
public class HttpFileServer {
  
static final int PORT = 8080;
  
public static void main(String[] args) throws Exception {
  
EventLoopGroup bossGroup = new NioEventLoopGroup(1);
  
EventLoopGroup workerGroup = new NioEventLoopGroup();
  
try {
  
ServerBootstrap b = new ServerBootstrap();
  
b.group(bossGroup, workerGroup).channel(NioServerSocketChannel.class).handler(new LoggingHandler(LogLevel.INFO))
  
.childHandler(new ChannelInitializer<SocketChannel>() {// 有连接到达时会创建一个channel
  
@Override
  
protected void initChannel(SocketChannel ch) throws Exception {
  
ChannelPipeline pipeline = ch.pipeline();
  
pipeline.addLast(new HttpServerCodec());
  
pipeline.addLast(new HttpObjectAggregator(65536));
  
pipeline.addLast(new ChunkedWriteHandler());
  
pipeline.addLast(new FileServerHandler());
  
}
  
});

Channel ch = b.bind(PORT).sync().channel();
  
System.err.println("打开浏览器,输入:  " + ("http") + "://127.0.0.1:" + PORT + '/');
  
ch.closeFuture().sync();
  
} finally {
  
bossGroup.shutdownGracefully();
  
workerGroup.shutdownGracefully();
  
}
  
}
  
}
  
第二步: 再写一个FileServerHandler?
  
package NettyDemo.file.server;

import static io.netty.handler.codec.http.HttpHeaders.Names.CACHE_CONTROL;
  
import static io.netty.handler.codec.http.HttpHeaders.Names.CONTENT_TYPE;
  
import static io.netty.handler.codec.http.HttpHeaders.Names.DATE;
  
import static io.netty.handler.codec.http.HttpHeaders.Names.EXPIRES;
  
import static io.netty.handler.codec.http.HttpHeaders.Names.IF_MODIFIED_SINCE;
  
import static io.netty.handler.codec.http.HttpHeaders.Names.LAST_MODIFIED;
  
import static io.netty.handler.codec.http.HttpHeaders.Names.LOCATION;
  
import static io.netty.handler.codec.http.HttpResponseStatus.BAD_REQUEST;
  
import static io.netty.handler.codec.http.HttpResponseStatus.FORBIDDEN;
  
import static io.netty.handler.codec.http.HttpResponseStatus.FOUND;
  
import static io.netty.handler.codec.http.HttpResponseStatus.INTERNAL_SERVER_ERROR;
  
import static io.netty.handler.codec.http.HttpResponseStatus.NOT_FOUND;
  
import static io.netty.handler.codec.http.HttpResponseStatus.NOT_MODIFIED;
  
import static io.netty.handler.codec.http.HttpResponseStatus.OK;
  
import static io.netty.handler.codec.http.HttpVersion.HTTP_1_1;
  
import io.netty.buffer.ByteBuf;
  
import io.netty.buffer.Unpooled;
  
import io.netty.channel.ChannelFuture;
  
import io.netty.channel.ChannelFutureListener;
  
import io.netty.channel.ChannelHandlerContext;
  
import io.netty.channel.ChannelProgressiveFuture;
  
import io.netty.channel.ChannelProgressiveFutureListener;
  
import io.netty.channel.DefaultFileRegion;
  
import io.netty.channel.SimpleChannelInboundHandler;
  
import io.netty.handler.codec.http.DefaultFullHttpResponse;
  
import io.netty.handler.codec.http.DefaultHttpResponse;
  
import io.netty.handler.codec.http.FullHttpRequest;
  
import io.netty.handler.codec.http.FullHttpResponse;
  
import io.netty.handler.codec.http.HttpChunkedInput;
  
import io.netty.handler.codec.http.HttpHeaders;
  
import io.netty.handler.codec.http.HttpResponse;
  
import io.netty.handler.codec.http.HttpResponseStatus;
  
import io.netty.handler.codec.http.HttpVersion;
  
import io.netty.handler.codec.http.LastHttpContent;
  
import io.netty.handler.ssl.SslHandler;
  
import io.netty.handler.stream.ChunkedFile;
  
import io.netty.util.CharsetUtil;
  
import io.netty.util.internal.SystemPropertyUtil;

import java.io.File;
  
import java.io.FileNotFoundException;
  
import java.io.RandomAccessFile;
  
import java.io.UnsupportedEncodingException;
  
import java.net.URLDecoder;
  
import java.text.SimpleDateFormat;
  
import java.util.Calendar;
  
import java.util.Date;
  
import java.util.GregorianCalendar;
  
import java.util.Locale;
  
import java.util.TimeZone;
  
import java.util.regex.Pattern;

import javax.activation.MimetypesFileTypeMap;

/***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\****
  
* Created on 2014-8-19 Author:
  
* <href=mailto:wanghouda@126.com>wanghouda
  
*
  
* @Title: HttpFileServerHandler.java
  
* @Package NettyDemo.file.server Description: Version: 1.0
  
\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***/
  
public class FileServerHandler extends SimpleChannelInboundHandler<FullHttpRequest> {
  
public static final String HTTP_DATE_FORMAT = "EEE, dd MMM yyyy HH:mm:ss zzz";
  
public static final String HTTP_DATE_GMT_TIMEZONE = "GMT";
  
public static final int HTTP_CACHE_SECONDS = 60;

@Override
  
protected void channelRead0(ChannelHandlerContext ctx, FullHttpRequest request) throws Exception {
  
// 监测解码情况
  
if (!request.getDecoderResult().isSuccess()) {
  
sendError(ctx, BAD_REQUEST);
  
return;
  
}
  
final String uri = request.getUri();
  
final String path = sanitizeUri(uri);
  
if (path == null) {
  
sendError(ctx, FORBIDDEN);
  
return;
  
}
  
//读取要下载的文件
  
File file = new File(path);
  
if (file.isHidden() || !file.exists()) {
  
sendError(ctx, NOT_FOUND);
  
return;
  
}
  
if (file.isDirectory()) {
  
if (uri.endsWith("/")) {
  
sendListing(ctx, file);
  
} else {
  
sendRedirect(ctx, uri + '/');
  
}
  
return;
  
}
  
if (!file.isFile()) {
  
sendError(ctx, FORBIDDEN);
  
return;
  
}
  
// Cache Validation
  
String ifModifiedSince = request.headers().get(IF_MODIFIED_SINCE);
  
if (ifModifiedSince != null && !ifModifiedSince.isEmpty()) {
  
SimpleDateFormat dateFormatter = new SimpleDateFormat(HTTP_DATE_FORMAT, Locale.US);
  
Date ifModifiedSinceDate = dateFormatter.parse(ifModifiedSince);
  
// Only compare up to the second because the datetime format we send
  
// to the client
  
// does not have milliseconds
  
long ifModifiedSinceDateSeconds = ifModifiedSinceDate.getTime() / 1000;
  
long fileLastModifiedSeconds = file.lastModified() / 1000;
  
if (ifModifiedSinceDateSeconds == fileLastModifiedSeconds) {
  
sendNotModified(ctx);
  
return;
  
}
  
}
  
RandomAccessFile raf;
  
try {
  
raf = new RandomAccessFile(file, "r");
  
} catch (FileNotFoundException ignore) {
  
sendError(ctx, NOT_FOUND);
  
return;
  
}
  
long fileLength = raf.length();
  
HttpResponse response = new DefaultHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.OK);
  
HttpHeaders.setContentLength(response, fileLength);
  
setContentTypeHeader(response, file);
  
setDateAndCacheHeaders(response, file);
  
if (HttpHeaders.isKeepAlive(request)) {
  
response.headers().set("CONNECTION", HttpHeaders.Values.KEEP_ALIVE);
  
}

// Write the initial line and the header.
  
ctx.write(response);

// Write the content.
  
ChannelFuture sendFileFuture;
  
if (ctx.pipeline().get(SslHandler.class) == null) {
  
sendFileFuture = ctx.write(new DefaultFileRegion(raf.getChannel(), 0, fileLength), ctx.newProgressivePromise());
  
} else {
  
sendFileFuture = ctx.write(new HttpChunkedInput(new ChunkedFile(raf, 0, fileLength, 8192)), ctx.newProgressivePromise());
  
}
  
sendFileFuture.addListener(new ChannelProgressiveFutureListener() {
  
@Override
  
public void operationProgressed(ChannelProgressiveFuture future, long progress, long total) {
  
if (total < 0) { // total unknown
  
System.err.println(future.channel() + " Transfer progress: " + progress);
  
} else {
  
System.err.println(future.channel() + " Transfer progress: " + progress + " / " + total);
  
}
  
}

@Override
  
public void operationComplete(ChannelProgressiveFuture future) {
  
System.err.println(future.channel() + " Transfer complete.");
  
}
  
});

// Write the end marker
  
ChannelFuture lastContentFuture = ctx.writeAndFlush(LastHttpContent.EMPTY_LAST_CONTENT);

// Decide whether to close the connection or not.
  
if (!HttpHeaders.isKeepAlive(request)) {
  
// Close the connection when the whole content is written out.
  
lastContentFuture.addListener(ChannelFutureListener.CLOSE);
  
}
  
}

@Override
  
public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
  
cause.printStackTrace();
  
if (ctx.channel().isActive()) {
  
sendError(ctx, INTERNAL_SERVER_ERROR);
  
}
  
}

private static final Pattern INSECURE_URI = Pattern.compile(".\*[<>&\"].\*");

private static String sanitizeUri(String uri) {
  
// Decode the path.
  
try {
  
uri = URLDecoder.decode(uri, "UTF-8");
  
} catch (UnsupportedEncodingException e) {
  
throw new Error(e);
  
}

if (!uri.startsWith("/")) {
  
return null;
  
}

// Convert file separators.
  
uri = uri.replace('/', File.separatorChar);

// Simplistic dumb security check.
  
// You will have to do something serious in the production environment.
  
if (uri.contains(File.separator + '.') || uri.contains('.' + File.separator) || uri.startsWith(".") || uri.endsWith(".")
  
|| INSECURE_URI.matcher(uri).matches()) {
  
return null;
  
}

// Convert to absolute path.
  
return SystemPropertyUtil.get("user.dir") + File.separator + uri;
  
}

private static final Pattern ALLOWED_FILE_NAME = Pattern.compile("[A-Za-z0-9][-_A-Za-z0-9\\.]*");

private static void sendListing(ChannelHandlerContext ctx, File dir) {
  
FullHttpResponse response = new DefaultFullHttpResponse(HTTP_1_1, OK);
  
response.headers().set(CONTENT_TYPE, "text/html; charset=UTF-8");

StringBuilder buf = new StringBuilder();
  
String dirPath = dir.getPath();

buf.append("<!DOCTYPE html>\r\n");
  
buf.append("<html><head><title>");
  
buf.append("Listing of: ");
  
buf.append(dirPath);
  
buf.append("</title></head><body>\r\n");

buf.append("Listing of: ");
  
buf.append(dirPath);
  
buf.append("\r\n");

buf.append("");
  
buf.append("..\r\n");

for (File f : dir.listFiles()) {
  
if (f.isHidden() || !f.canRead()) {
  
continue;
  
}

String name = f.getName();
  
if (!ALLOWED_FILE_NAME.matcher(name).matches()) {
  
continue;
  
}

buf.append("<a href=\"");
  
buf.append(name);
  
buf.append("\">");
  
buf.append(name);
  
buf.append("\r\n");
  
}

buf.append("</body></html>\r\n");
  
ByteBuf buffer = Unpooled.copiedBuffer(buf, CharsetUtil.UTF_8);
  
response.content().writeBytes(buffer);
  
buffer.release();

// Close the connection as soon as the error message is sent.
  
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);
  
}

private static void sendRedirect(ChannelHandlerContext ctx, String newUri) {
  
FullHttpResponse response = new DefaultFullHttpResponse(HTTP_1_1, FOUND);
  
response.headers().set(LOCATION, newUri);

// Close the connection as soon as the error message is sent.
  
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);
  
}

private static void sendError(ChannelHandlerContext ctx, HttpResponseStatus status) {
  
FullHttpResponse response = new DefaultFullHttpResponse(HTTP_1_1, status, Unpooled.copiedBuffer("Failure: " + status + "\r\n", CharsetUtil.UTF_8));
  
response.headers().set(CONTENT_TYPE, "text/plain; charset=UTF-8");

// Close the connection as soon as the error message is sent.
  
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);
  
}

/**
  
* When file timestamp is the same as what the browser is sending up, send a
  
* "304 Not Modified"
  
*
  
* @param ctx
  
* Context
  
*/
  
private static void sendNotModified(ChannelHandlerContext ctx) {
  
FullHttpResponse response = new DefaultFullHttpResponse(HTTP_1_1, NOT_MODIFIED);
  
setDateHeader(response);

// Close the connection as soon as the error message is sent.
  
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);
  
}

/**
  
* Sets the Date header for the HTTP response
  
*
  
* @param response
  
* HTTP response
  
*/
  
private static void setDateHeader(FullHttpResponse response) {
  
SimpleDateFormat dateFormatter = new SimpleDateFormat(HTTP_DATE_FORMAT, Locale.US);
  
dateFormatter.setTimeZone(TimeZone.getTimeZone(HTTP_DATE_GMT_TIMEZONE));

Calendar time = new GregorianCalendar();
  
response.headers().set(DATE, dateFormatter.format(time.getTime()));
  
}

/**
  
* Sets the Date and Cache headers for the HTTP Response
  
*
  
* @param response
  
* HTTP response
  
* @param fileToCache
  
* file to extract content type
  
*/
  
private static void setDateAndCacheHeaders(HttpResponse response, File fileToCache) {
  
SimpleDateFormat dateFormatter = new SimpleDateFormat(HTTP_DATE_FORMAT, Locale.US);
  
dateFormatter.setTimeZone(TimeZone.getTimeZone(HTTP_DATE_GMT_TIMEZONE));

// Date header
  
Calendar time = new GregorianCalendar();
  
response.headers().set(DATE, dateFormatter.format(time.getTime()));

// Add cache headers
  
time.add(Calendar.SECOND, HTTP_CACHE_SECONDS);
  
response.headers().set(EXPIRES, dateFormatter.format(time.getTime()));
  
response.headers().set(CACHE_CONTROL, "private, max-age=" + HTTP_CACHE_SECONDS);
  
response.headers().set(LAST_MODIFIED, dateFormatter.format(new Date(fileToCache.lastModified())));
  
}

/**
  
* Sets the content type header for the HTTP Response
  
*
  
* @param response
  
* HTTP response
  
* @param file
  
* file to extract content type
  
*/
  
private static void setContentTypeHeader(HttpResponse response, File file) {
  
MimetypesFileTypeMap mimeTypesMap = new MimetypesFileTypeMap();
  
response.headers().set(CONTENT_TYPE, mimeTypesMap.getContentType(file.getPath()));
  
}

}
  
第三步: 启动Netty服务,在浏览器中输入
  
[http://127.0.0.1:8080/](http://127.0.0.1:8080/)
  
如图所示: 即可在浏览器中看到工程目录下所有文件,点击即可下载
