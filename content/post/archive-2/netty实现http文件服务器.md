---
title: netty http文件服务器
author: "-"
date: 2016-03-20T05:58:13+00:00
url: /?p=8815
categories:
  - Inbox
tags:
  - reprint
---
## netty http文件服务器

<http://krisjin.github.io/2015/02/14/netty-file-server/>

Http介绍
  
Http(超文本传输协议)协议是建立在TCP传输协议之上的应用成协议,Http由于便捷、快速的方式,适用于分布式超媒体信息系统。Http是目前Web开发的主流协议,基于Http的应用非常广泛,因此掌握HTTP的开发非常重要。由于netty的HTTP协议栈是基于netty的NIO通信框架开发的,所以netty的HTTP协议也是异步非阻塞的。

具体的关于HTTP及Netyy的实现细节在以后的章节在写,先上实例代码:

实例代码
  
服务端:
  
public class HttpFileServer {

public void run(final int port, final String url) throws InterruptedException {

EventLoopGroup bossGroup = new NioEventLoopGroup();
  
EventLoopGroup workerGroup = new NioEventLoopGroup();

try {
  
ServerBootstrap boot = new ServerBootstrap();

boot.group(bossGroup, workerGroup).channel(NioServerSocketChannel.class)
  
.childHandler(new ChannelInitializer<SocketChannel>() {

@Override
  
protected void initChannel(SocketChannel ch) throws Exception {
  
ch.pipeline().addLast("http-decoder", new HttpRequestDecoder());
  
ch.pipeline().addLast("http-aggregator", new HttpObjectAggregator(65536));
  
ch.pipeline().addLast("http-encoder", new HttpResponseEncoder());
  
ch.pipeline().addLast("http-chunked", new ChunkedWriteHandler());
  
ch.pipeline().addLast("fileServerHandler", new HttpFileServerHandler(url));
  
}

});
  
ChannelFuture cf =boot.bind("127.0.0.1",port).sync();
  
System.out.println("Http文件目录服务器启动: <http://127.0.0.1>:"+port+url);
  
cf.channel().closeFuture().sync();

} finally {
  
bossGroup.shutdownGracefully();
  
workerGroup.shutdownGracefully();

}

}

public static void main(String[] args) throws InterruptedException {
  
String url="/src/main/java/";

new HttpFileServer().run(8080, url);

}

}

服务端handler

public class HttpFileServerHandler extends SimpleChannelInboundHandler<FullHttpRequest> {

HttpMethod GET = new HttpMethod("GET");

private String url;

private final Pattern ALLOWED_FILE_NAME = Pattern.compile("[A-Za-z0-9][-_A-Za-z0-9\\.]*");

private final Pattern INSECURE_URI = Pattern.compile(".\*[<>&\"].\*");

public HttpFileServerHandler(String url) {
  
this.url = url;
  
}

@Override
  
protected void messageReceived(ChannelHandlerContext ctx, FullHttpRequest request) throws Exception {

if (!request.getDecoderResult().isSuccess()) {
  
sendError(ctx, HttpResponseStatus.BAD_REQUEST);
  
return;
  
}

if (request.getMethod() != HttpMethod.GET) {
  
sendError(ctx, HttpResponseStatus.METHOD_NOT_ALLOWED);
  
return;
  
}
  
final String uri = request.getUri();
  
final String path = sanitizeUri(uri);
  
if (path == null) {
  
sendError(ctx, HttpResponseStatus.FORBIDDEN);
  
return;
  
}

File file = new File(path);

if (file.isHidden() || !file.exists()) {
  
sendError(ctx, HttpResponseStatus.NOT_FOUND);
  
return;
  
}

if (file.isDirectory()) {
  
if (uri.endsWith("/")) {
  
sendList(ctx, file);
  
} else {
  
sendRedirect(ctx, uri + '/');
  
}
  
return;
  
}

if (!file.isFile()) {
  
sendError(ctx, HttpResponseStatus.FORBIDDEN);
  
return;
  
}

RandomAccessFile randomAccessFile = null;

try {
  
randomAccessFile = new RandomAccessFile(file, "r");
  
} catch (FileNotFoundException e) {
  
sendError(ctx, HttpResponseStatus.NO_CONTENT);
  
return;
  
}
  
long fileLength = randomAccessFile.length();
  
HttpResponse response = new DefaultHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.OK);
  
HttpHeaders.setContentLength(response, fileLength);
  
setContentTypeHeader(response, file);

if (HttpHeaders.isKeepAlive(request)) {
  
response.headers().set(HttpHeaders.Names.CONNECTION, HttpHeaders.Values.KEEP_ALIVE);
  
}
  
ctx.write(response);
  
ChannelFuture sendFileFuture;

sendFileFuture = ctx.write(new ChunkedFile(randomAccessFile, 0, fileLength, 8192), ctx.newProgressivePromise());
  
sendFileFuture.addListener(new ChannelProgressiveFutureListener() {

@Override
  
public void operationComplete(ChannelProgressiveFuture future) throws Exception {

System.err.println(future.channel() + " transfer complete");

}

@Override
  
public void operationProgressed(ChannelProgressiveFuture future, long progress, long total)
  
throws Exception {
  
if (total < 0) {
  
System.err.println(future.channel() + " transfer progress : " + progress);
  
} else {
  
System.err.println(future.channel() + " transfer progress : " + progress + " / " + total);
  
}
  
}
  
});

ChannelFuture lastContentFuture = ctx.writeAndFlush(LastHttpContent.EMPTY_LAST_CONTENT);
  
if (!HttpHeaders.isKeepAlive(request)) {
  
lastContentFuture.addListener(ChannelFutureListener.CLOSE);
  
}

}

@Override
  
public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {

cause.printStackTrace();
  
if (ctx.channel().isActive()) {
  
sendError(ctx, HttpResponseStatus.INTERNAL_SERVER_ERROR);
  
}
  
}

private void sendError(ChannelHandlerContext ctx, HttpResponseStatus status) {
  
FullHttpResponse response = new DefaultFullHttpResponse(HttpVersion.HTTP_1_1, status, Unpooled.copiedBuffer(
  
"Failure :" + status + "\r\n", CharsetUtil.UTF_8));
  
response.headers().set(HttpHeaders.Names.CONTENT_TYPE, "text/plain; charset=UTF-8");
  
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);
  
}

public String sanitizeUri(String uri) {

// Decode the path.
  
try {
  
uri = URLDecoder.decode(uri, "UTF-8");
  
} catch (UnsupportedEncodingException e) {
  
throw new Error(e);
  
}

if (uri.isEmpty() || uri.charAt(0) != '/') {
  
return null;
  
}

// Convert file separators.
  
uri = uri.replace('/', File.separatorChar);

// Simplistic dumb security check.
  
// You will have to do something serious in the production environment.
  
if (uri.contains(File.separator + '.') || uri.contains('.' + File.separator) || uri.charAt(0) == '.'
  
|| uri.charAt(uri.length() - 1) == '.' || INSECURE_URI.matcher(uri).matches()) {
  
return null;
  
}

// Convert to absolute path.
  
return System.getProperty("user.dir") + File.separator + uri;
  
}

public final void sendList(ChannelHandlerContext ctx, File file) {
  
FullHttpResponse response = new DefaultFullHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.OK);
  
response.headers().set(HttpHeaders.Names.CONTENT_TYPE, "text/html; charset=UTF-8");
  
StringBuilder sb = new StringBuilder();

String dirPath = file.getPath();

sb.append("<!DOCTYPE html>\r\n");
  
sb.append("<html><head><title>");
  
sb.append(dirPath);
  
sb.append("目录: ");
  
sb.append("</title></head><body>\r\n");
  
sb.append("");
  
sb.append(dirPath).append("目录: ");
  
sb.append("\r\n");

sb.append("");
  
sb.append("..\r\n");

for (File f : file.listFiles()) {
  
if (f.isHidden() || !f.canRead()) {
  
continue;
  
}
  
String name = f.getName();
  
if (!ALLOWED_FILE_NAME.matcher(name).matches()) {
  
continue;
  
}

sb.append("<a href=\"");
  
sb.append(name);
  
sb.append("\">");
  
sb.append(name);
  
sb.append("\r\n");

}

sb.append("</body></html>\r\n");

ByteBuf buffer = Unpooled.copiedBuffer(sb, CharsetUtil.UTF_8);
  
response.content().writeBytes(buffer);
  
buffer.release();

// Close the connection as soon as the error message is sent.
  
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);
  
}

public void sendRedirect(ChannelHandlerContext ctx, String newUri) {
  
FullHttpResponse response = new DefaultFullHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.FOUND);
  
response.headers().set(HttpHeaders.Names.LOCATION, newUri);
  
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);

}

private void setContentTypeHeader(HttpResponse response, File file) {

MimetypesFileTypeMap mimeTypeMap = new MimetypesFileTypeMap();
  
response.headers().set(HttpHeaders.Names.CONTENT_TYPE, mimeTypeMap.getContentType(file.getPath()));
  
}

}
