---
title: netty实现http文件服务器
author: wiloon
type: post
date: 2016-03-20T05:58:13+00:00
url: /?p=8815
categories:
  - Uncategorized

---
http://krisjin.github.io/2015/02/14/netty-file-server/

Http介绍
  
Http(超文本传输协议)协议是建立在TCP传输协议之上的应用成协议,Http由于便捷、快速的方式，适用于分布式超媒体信息系统。Http是目前Web开发的主流协议，基于Http的应用非常广泛，因此掌握HTTP的开发非常重要。由于netty的HTTP协议栈是基于netty的NIO通信框架开发的，所以netty的HTTP协议也是异步非阻塞的。

具体的关于HTTP及Netyy的实现细节在以后的章节在写，先上实例代码：

实例代码
  
服务端：
  
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
  
ch.pipeline().addLast("http-decoder&#8221;, new HttpRequestDecoder());
  
ch.pipeline().addLast("http-aggregator&#8221;, new HttpObjectAggregator(65536));
  
ch.pipeline().addLast("http-encoder&#8221;, new HttpResponseEncoder());
  
ch.pipeline().addLast("http-chunked&#8221;, new ChunkedWriteHandler());
  
ch.pipeline().addLast("fileServerHandler&#8221;, new HttpFileServerHandler(url));
  
}

});
  
ChannelFuture cf =boot.bind("127.0.0.1&#8221;,port).sync();
  
System.out.println("Http文件目录服务器启动：http://127.0.0.1:&#8221;+port+url);
  
cf.channel().closeFuture().sync();

} finally {
  
bossGroup.shutdownGracefully();
  
workerGroup.shutdownGracefully();

}

}

public static void main(String[] args) throws InterruptedException {
  
String url=&#8221;/src/main/java/&#8221;;

new HttpFileServer().run(8080, url);

}

}

服务端handler

public class HttpFileServerHandler extends SimpleChannelInboundHandler<FullHttpRequest> {

HttpMethod GET = new HttpMethod("GET&#8221;);

private String url;

private final Pattern ALLOWED\_FILE\_NAME = Pattern.compile("\[A-Za-z0-9\]\[-_A-Za-z0-9\\.\]*&#8221;);

private final Pattern INSECURE_URI = Pattern.compile(".\*[<>&\&#8221;].\*&#8221;);

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
  
sendError(ctx, HttpResponseStatus.METHOD\_NOT\_ALLOWED);
  
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
  
if (uri.endsWith("/&#8221;)) {
  
sendList(ctx, file);
  
} else {
  
sendRedirect(ctx, uri + &#8216;/&#8217;);
  
}
  
return;
  
}

if (!file.isFile()) {
  
sendError(ctx, HttpResponseStatus.FORBIDDEN);
  
return;
  
}

RandomAccessFile randomAccessFile = null;

try {
  
randomAccessFile = new RandomAccessFile(file, "r&#8221;);
  
} catch (FileNotFoundException e) {
  
sendError(ctx, HttpResponseStatus.NO_CONTENT);
  
return;
  
}
  
long fileLength = randomAccessFile.length();
  
HttpResponse response = new DefaultHttpResponse(HttpVersion.HTTP\_1\_1, HttpResponseStatus.OK);
  
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

System.err.println(future.channel() + &#8221; transfer complete&#8221;);

}

@Override
  
public void operationProgressed(ChannelProgressiveFuture future, long progress, long total)
  
throws Exception {
  
if (total < 0) {
  
System.err.println(future.channel() + &#8221; transfer progress : &#8221; + progress);
  
} else {
  
System.err.println(future.channel() + &#8221; transfer progress : &#8221; + progress + &#8221; / &#8221; + total);
  
}
  
}
  
});

ChannelFuture lastContentFuture = ctx.writeAndFlush(LastHttpContent.EMPTY\_LAST\_CONTENT);
  
if (!HttpHeaders.isKeepAlive(request)) {
  
lastContentFuture.addListener(ChannelFutureListener.CLOSE);
  
}

}

@Override
  
public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {

cause.printStackTrace();
  
if (ctx.channel().isActive()) {
  
sendError(ctx, HttpResponseStatus.INTERNAL\_SERVER\_ERROR);
  
}
  
}

private void sendError(ChannelHandlerContext ctx, HttpResponseStatus status) {
  
FullHttpResponse response = new DefaultFullHttpResponse(HttpVersion.HTTP\_1\_1, status, Unpooled.copiedBuffer(
  
"Failure :&#8221; + status + "\r\n&#8221;, CharsetUtil.UTF_8));
  
response.headers().set(HttpHeaders.Names.CONTENT_TYPE, "text/plain; charset=UTF-8&#8221;);
  
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);
  
}

public String sanitizeUri(String uri) {

// Decode the path.
  
try {
  
uri = URLDecoder.decode(uri, "UTF-8&#8221;);
  
} catch (UnsupportedEncodingException e) {
  
throw new Error(e);
  
}

if (uri.isEmpty() || uri.charAt(0) != &#8216;/&#8217;) {
  
return null;
  
}

// Convert file separators.
  
uri = uri.replace(&#8216;/&#8217;, File.separatorChar);

// Simplistic dumb security check.
  
// You will have to do something serious in the production environment.
  
if (uri.contains(File.separator + &#8216;.&#8217;) || uri.contains(&#8216;.&#8217; + File.separator) || uri.charAt(0) == &#8216;.&#8217;
  
|| uri.charAt(uri.length() &#8211; 1) == &#8216;.&#8217; || INSECURE_URI.matcher(uri).matches()) {
  
return null;
  
}

// Convert to absolute path.
  
return System.getProperty("user.dir&#8221;) + File.separator + uri;
  
}

public final void sendList(ChannelHandlerContext ctx, File file) {
  
FullHttpResponse response = new DefaultFullHttpResponse(HttpVersion.HTTP\_1\_1, HttpResponseStatus.OK);
  
response.headers().set(HttpHeaders.Names.CONTENT_TYPE, "text/html; charset=UTF-8&#8221;);
  
StringBuilder sb = new StringBuilder();

String dirPath = file.getPath();

sb.append("<!DOCTYPE html>\r\n&#8221;);
  
sb.append("<html><head><title>&#8221;);
  
sb.append(dirPath);
  
sb.append("目录：&#8221;);
  
sb.append("</title></head><body>\r\n&#8221;);
  
sb.append("&#8221;);
  
sb.append(dirPath).append("目录：&#8221;);
  
sb.append("\r\n&#8221;);

sb.append("<ul>&#8221;);
  
sb.append("<li><a href=\&#8221;../\&#8221;>..</a></li>\r\n&#8221;);

for (File f : file.listFiles()) {
  
if (f.isHidden() || !f.canRead()) {
  
continue;
  
}
  
String name = f.getName();
  
if (!ALLOWED\_FILE\_NAME.matcher(name).matches()) {
  
continue;
  
}

sb.append("<li><a href=\&#8221;&#8221;);
  
sb.append(name);
  
sb.append("\&#8221;>&#8221;);
  
sb.append(name);
  
sb.append("</a></li>\r\n&#8221;);

}

sb.append("</ul></body></html>\r\n&#8221;);

ByteBuf buffer = Unpooled.copiedBuffer(sb, CharsetUtil.UTF_8);
  
response.content().writeBytes(buffer);
  
buffer.release();

// Close the connection as soon as the error message is sent.
  
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);
  
}

public void sendRedirect(ChannelHandlerContext ctx, String newUri) {
  
FullHttpResponse response = new DefaultFullHttpResponse(HttpVersion.HTTP\_1\_1, HttpResponseStatus.FOUND);
  
response.headers().set(HttpHeaders.Names.LOCATION, newUri);
  
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);

}

private void setContentTypeHeader(HttpResponse response, File file) {

MimetypesFileTypeMap mimeTypeMap = new MimetypesFileTypeMap();
  
response.headers().set(HttpHeaders.Names.CONTENT_TYPE, mimeTypeMap.getContentType(file.getPath()));
  
}

}