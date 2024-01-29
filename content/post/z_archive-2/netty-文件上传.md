---
title: netty 文件上传
author: "-"
date: 2016-05-24T12:05:33+00:00
url: /?p=9013
categories:
  - Inbox
tags:
  - reprint
---
## netty 文件上传

[http://blog.csdn.net/mcpang/article/details/41140409](http://blog.csdn.net/mcpang/article/details/41140409)

【初学与研发之NETTY】netty4之文件上传
  
标签:  netty4文件上传
  
2014-11-15 04:35 6005人阅读 评论(29) 收藏 举报
  
分类:
  
JAVA (48)  Netty (6)
  
版权声明: 本文为博主原创文章,未经博主允许不得转载。
  
客户端:

 
  
print?
  
public class UpLoadClient {
  
private StringBuffer resultBuffer = new StringBuffer();
  
private EventLoopGroup group = null;
  
private HttpDataFactory factory = null;

private Object waitObject = new Object();

private ChannelFuture future = null;

public UpLoadClient(String host, int port) throws Exception {
  
this.group = new NioEventLoopGroup();
  
this.factory = new DefaultHttpDataFactory(DefaultHttpDataFactory.MINSIZE);

Bootstrap b = new Bootstrap();
  
b.option(ChannelOption.TCP_NODELAY, true);
  
b.option(ChannelOption.SO_SNDBUF, 1048576*200);
  
b.option(ChannelOption.SO_KEEPALIVE, true);

b.group(group).channel(NioSocketChannel.class);
  
b.handler(new UpLoadClientIntializer());

this.future = b.connect(host, port).sync();
  
}

public void uploadFile(String path) {
  
if(path == null) {
  
System.out.println("上传文件的路径不能为null...");
  
return;
  
}
  
File file = new File(path);
  
if (!file.canRead()) {
  
System.out.println(file.getName() + "不可读...");
  
return;
  
}
  
if (file.isHidden() || !file.isFile()) {
  
System.out.println(file.getName() + "不存在...");
  
return;
  
}

try {
  
HttpRequest request = new DefaultHttpRequest(HttpVersion.HTTP_1_1, HttpMethod.POST, "");

HttpPostRequestEncoder bodyRequestEncoder = new HttpPostRequestEncoder(factory, request, false);

bodyRequestEncoder.addBodyAttribute("getform", "POST");
  
bodyRequestEncoder.addBodyFileUpload("myfile", file, "application/x-zip-compressed", false);

List<InterfaceHttpData> bodylist = bodyRequestEncoder.getBodyListAttributes();
  
if (bodylist == null) {
  
System.out.println("请求体不存在...");
  
return;
  
}

HttpRequest request2 = new DefaultHttpRequest(HttpVersion.HTTP_1_1, HttpMethod.POST, file.getName());
  
HttpPostRequestEncoder bodyRequestEncoder2 = new HttpPostRequestEncoder(factory, request2, true);

bodyRequestEncoder2.setBodyHttpDatas(bodylist);
  
bodyRequestEncoder2.finalizeRequest();

Channel channel = this.future.channel();
  
if(channel.isActive() && channel.isWritable()) {
  
channel.writeAndFlush(request2);

if (bodyRequestEncoder2.isChunked()) {
  
channel.writeAndFlush(bodyRequestEncoder2).awaitUninterruptibly();
  
}

bodyRequestEncoder2.cleanFiles();
  
}
  
channel.closeFuture().sync();
  
} catch (Exception e) {
  
e.printStackTrace();
  
}
  
}

public void shutdownClient() {
  
// 等待数据的传输通道关闭
  
group.shutdownGracefully();
  
factory.cleanAllHttpDatas();
  
}

public boolean isCompleted() {
  
while(waitObject != null) {
  
//当通道处于开通和活动时,处于等待
  
}
  
if(resultBuffer.length() > 0) {
  
if("200".equals(resultBuffer.toString())) {
  
resultBuffer.setLength(0);
  
return true;
  
}
  
}
  
return false;
  
}

private class UpLoadClientIntializer extends ChannelInitializer<SocketChannel> {
  
@Override
  
protected void initChannel(SocketChannel ch) throws Exception {
  
ChannelPipeline pipeline = ch.pipeline();

pipeline.addLast("decoder", new HttpResponseDecoder());
  
pipeline.addLast("encoder", new HttpRequestEncoder());
  
pipeline.addLast("chunkedWriter", new ChunkedWriteHandler());

pipeline.addLast("dispatcher", new UpLoadClientHandler());
  
}
  
}

private class UpLoadClientHandler extends SimpleChannelInboundHandler<HttpObject> {
  
private boolean readingChunks = false;
  
private int succCode = 200;

protected void channelRead0(ChannelHandlerContext ctx, HttpObject msg)
  
throws Exception {
  
if (msg instanceof HttpResponse) {
  
HttpResponse response = (HttpResponse) msg;

succCode = response.getStatus().code();

if (succCode == 200 && HttpHeaders.isTransferEncodingChunked(response)) {
  
readingChunks = true;
  
}
  
}

if (msg instanceof HttpContent) {
  
HttpContent chunk = (HttpContent) msg;
  
System.out.println("【响应】"+succCode+">>"+chunk.content().toString(CharsetUtil.UTF_8));
  
if (chunk instanceof LastHttpContent) {
  
readingChunks = false;
  
}
  
}

if (!readingChunks) {
  
resultBuffer.append(succCode);
  
ctx.channel().close();
  
}
  
}

@Override
  
public void channelInactive(ChannelHandlerContext ctx) throws Exception {
  
waitObject = null;
  
}

@Override
  
public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause)
  
throws Exception {

resultBuffer.setLength(0);
  
resultBuffer.append(500);
  
System.out.println("管道异常: " + cause.getMessage());
  
cause.printStackTrace();
  
ctx.channel().close();
  
}
  
}
  
}

服务端:

 
  
print?
  
public class DBServer extends Thread {

//单实例
  
private static DBServer dbServer = null;

//定时调度的周期实例
  
private static Scheduler sched = null;

private EventLoopGroup bossGroup = null;
  
private EventLoopGroup workerGroup = null;
  
//创建实例
  
public static DBServer newBuild() {
  
if(dbServer == null) {
  
dbServer = new DBServer();
  
}
  
return dbServer;
  
}

public void run() {
  
try {
  
startServer();
  
} catch(Exception e) {
  
System.out.println("数据服务启动出现异常: "+e.toString());
  
e.printStackTrace();
  
}
  
}

private void startServer() throws Exception {
  
bossGroup = new NioEventLoopGroup();
  
workerGroup = new NioEventLoopGroup();

try {
  
ServerBootstrap b = new ServerBootstrap();

b.group(bossGroup, workerGroup);

b.option(ChannelOption.TCP_NODELAY, true);
  
b.option(ChannelOption.SO_TIMEOUT, 60000);
  
b.option(ChannelOption.SO_SNDBUF, 1048576*200);

b.option(ChannelOption.SO_KEEPALIVE, true);

b.channel(NioServerSocketChannel.class);
  
b.childHandler(new DBServerInitializer());

// 服务器绑定端口监听
  
ChannelFuture f = b.bind(DBConfig.curHost.getIp(), DBConfig.curHost.getPort()).sync();

System.out.println("数据服务: "+DBConfig.curHost.getServerHost()+"启动完成...");
  
// 监听服务器关闭监听
  
f.channel().closeFuture().sync();
  
} finally {
  
bossGroup.shutdownGracefully();
  
workerGroup.shutdownGracefully();
  
}
  
}
  
}
  
 
  
print?
  
public class DBServerHandler extends SimpleChannelInboundHandler<HttpObject> {

private static final HttpDataFactory factory = new DefaultHttpDataFactory(DefaultHttpDataFactory.MINSIZE);

private String uri = null;

private HttpRequest request = null;

private HttpPostRequestDecoder decoder;

//message、download、upload
  
private String type = "message";

public static final String HTTP_DATE_FORMAT = "EEE, dd MMM yyyy HH:mm:ss zzz";
  
public static final String HTTP_DATE_GMT_TIMEZONE = "GMT";
  
public static final int HTTP_CACHE_SECONDS = 60;

static {
  
DiskFileUpload.baseDirectory = DBConfig.curHost.getZipPath();
  
}

@Override
  
public void channelRead0(ChannelHandlerContext ctx, HttpObject msg) throws Exception {
  
if (msg instanceof HttpRequest) {
  
request = (HttpRequest) msg;

uri = sanitizeUri(request.getUri());

if (request.getMethod() == HttpMethod.POST) {
  
if (decoder != null) {
  
decoder.cleanFiles();
  
decoder = null;
  
}
  
try {
  
decoder = new HttpPostRequestDecoder(factory, request);
  
} catch (Exception e) {
  
e.printStackTrace();
  
writeResponse(ctx.channel(), HttpResponseStatus.INTERNAL_SERVER_ERROR, e.toString());
  
ctx.channel().close();
  
return;
  
}
  
}
  
}

if (decoder != null && msg instanceof HttpContent) {
  
HttpContent chunk = (HttpContent) msg;

try {
  
decoder.offer(chunk);
  
} catch (Exception e) {
  
e.printStackTrace();
  
writeResponse(ctx.channel(), HttpResponseStatus.INTERNAL_SERVER_ERROR, e.toString());
  
ctx.channel().close();
  
return;
  
}

readHttpDataChunkByChunk();

if (chunk instanceof LastHttpContent) {
  
writeResponse(ctx.channel(), HttpResponseStatus.OK, "");
  
reset();
  
return;
  
}
  
}
  
}

private String sanitizeUri(String uri) {
  
try {
  
uri = URLDecoder.decode(uri, "UTF-8");
  
} catch(UnsupportedEncodingException e) {
  
try {
  
uri = URLDecoder.decode(uri, "ISO-8859-1");
  
} catch(UnsupportedEncodingException e1) {
  
throw new Error();
  
}
  
}

return uri;
  
}

private void reset() {
  
request = null;

//销毁decoder释放所有的资源
  
decoder.destroy();

decoder = null;
  
}

/**
  
* 通过chunk读取request,获取chunk数据
  
* @throws IOException
  
*/
  
private void readHttpDataChunkByChunk() throws IOException {
  
try {
  
while (decoder.hasNext()) {

InterfaceHttpData data = decoder.next();
  
if (data != null) {
  
try {
  
writeHttpData(data);
  
} finally {
  
data.release();
  
}
  
}
  
}
  
} catch (EndOfDataDecoderException e1) {
  
System.out.println("end chunk");
  
}
  
}

private void writeHttpData(InterfaceHttpData data) throws IOException {
  
if (data.getHttpDataType() == HttpDataType.FileUpload) {
  
FileUpload fileUpload = (FileUpload) data;
  
if (fileUpload.isCompleted()) {

StringBuffer fileNameBuf = new StringBuffer();
  
fileNameBuf.append(DiskFileUpload.baseDirectory)
  
.append(uri);

fileUpload.renameTo(new File(fileNameBuf.toString()));
  
}
  
} else if (data.getHttpDataType() == HttpDataType.Attribute) {
  
Attribute attribute = (Attribute) data;
  
if(CommonParam.DOWNLOAD_COLLECTION.equals(attribute.getName())) {
  
SynchMessageWatcher.newBuild().getMsgQueue().add(attribute.getValue());
  
}
  
}
  
}

private void writeDownLoadResponse(ChannelHandlerContext ctx, RandomAccessFile raf, File file) throws Exception {
  
long fileLength = raf.length();

//判断是否关闭请求响应连接
  
boolean close = HttpHeaders.Values.CLOSE.equalsIgnoreCase(request.headers().get(CONNECTION))
  
|| request.getProtocolVersion().equals(HttpVersion.HTTP_1_0)
  
&& !HttpHeaders.Values.KEEP_ALIVE.equalsIgnoreCase(request.headers().get(CONNECTION));

HttpResponse response = new DefaultHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.OK);
  
HttpHeaders.setContentLength(response, fileLength);

setContentHeader(response, file);

if (!close) {
  
response.headers().set(CONNECTION, HttpHeaders.Values.KEEP_ALIVE);
  
}

ctx.write(response);
  
System.out.println("读取大小: "+fileLength);

final FileRegion region = new DefaultFileRegion(raf.getChannel(), 0, 1000);
  
ChannelFuture writeFuture = ctx.write(region, ctx.newProgressivePromise());
  
writeFuture.addListener(new ChannelProgressiveFutureListener() {
  
public void operationProgressed(ChannelProgressiveFuture future, long progress, long total) {
  
if (total < 0) {
  
System.err.println(future.channel() + " Transfer progress: " + progress);
  
} else {
  
System.err.println(future.channel() + " Transfer progress: " + progress + " / " + total);
  
}
  
}

public void operationComplete(ChannelProgressiveFuture future) {
  
}
  
});

ChannelFuture lastContentFuture = ctx.writeAndFlush(LastHttpContent.EMPTY_LAST_CONTENT);
  
if(close) {
  
raf.close();
  
lastContentFuture.addListener(ChannelFutureListener.CLOSE);
  
}
  
}

private static void setContentHeader(HttpResponse response, File file) {
  
MimetypesFileTypeMap mimeTypesMap = new MimetypesFileTypeMap();
  
response.headers().set(CONTENT_TYPE, mimeTypesMap.getContentType(file.getPath()));

SimpleDateFormat dateFormatter = new SimpleDateFormat(HTTP_DATE_FORMAT, Locale.US);
  
dateFormatter.setTimeZone(TimeZone.getTimeZone(HTTP_DATE_GMT_TIMEZONE));

// Date header
  
Calendar time = new GregorianCalendar();
  
response.headers().set(DATE, dateFormatter.format(time.getTime()));

// Add cache headers
  
time.add(Calendar.SECOND, HTTP_CACHE_SECONDS);
  
response.headers().set(EXPIRES, dateFormatter.format(time.getTime()));
  
response.headers().set(CACHE_CONTROL, "private, max-age=" + HTTP_CACHE_SECONDS);
  
response.headers().set(LAST_MODIFIED, dateFormatter.format(new Date(file.lastModified())));
  
}

private void writeResponse(Channel channel, HttpResponseStatus httpResponseStatus, String returnMsg) {
  
String resultStr = "节点【"+DBConfig.curHost.getServerHost()+"】";
  
if(httpResponseStatus.code() == HttpResponseStatus.OK.code()) {
  
resultStr += "正常接收";
  
if("message".equals(type)) {
  
resultStr += "字符串。";
  
} else if("upload".equals(type)) {
  
resultStr += "上传文件。";
  
} else if("download".equals(type)) {
  
resultStr += "下载文件名。";
  
}
  
} else if(httpResponseStatus.code() == HttpResponseStatus.INTERNAL_SERVER_ERROR.code()) {
  
resultStr += "接收";
  
if("message".equals(type)) {
  
resultStr += "字符串";
  
} else if("upload".equals(type)) {
  
resultStr += "上传文件";
  
} else if("download".equals(type)) {
  
resultStr += "下载文件名";
  
}
  
resultStr += "的过程中出现异常: "+returnMsg;
  
}
  
//将请求响应的内容转换成ChannelBuffer.
  
ByteBuf buf = copiedBuffer(resultStr, CharsetUtil.UTF_8);

//判断是否关闭请求响应连接
  
boolean close = HttpHeaders.Values.CLOSE.equalsIgnoreCase(request.headers().get(CONNECTION))
  
|| request.getProtocolVersion().equals(HttpVersion.HTTP_1_0)
  
&& !HttpHeaders.Values.KEEP_ALIVE.equalsIgnoreCase(request.headers().get(CONNECTION));

//构建请求响应对象
  
FullHttpResponse response = new DefaultFullHttpResponse(
  
HttpVersion.HTTP_1_1, httpResponseStatus, buf);
  
response.headers().set(CONTENT_TYPE, "text/plain; charset=UTF-8");

if (!close) {
  
//若该请求响应是最后的响应,则在响应头中没有必要添加'Content-Length'
  
response.headers().set(CONTENT_LENGTH, buf.readableBytes());
  
}

//发送请求响应
  
ChannelFuture future = channel.writeAndFlush(response);
  
//发送请求响应操作结束后关闭连接
  
if (close) {
  
future.addListener(ChannelFutureListener.CLOSE);
  
}
  
}

@Override
  
public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
  
cause.getCause().printStackTrace();
  
writeResponse(ctx.channel(), HttpResponseStatus.INTERNAL_SERVER_ERROR, "数据文件通过过程中出现异常: "+cause.getMessage().toString());
  
ctx.channel().close();
  
}
  
}
  
 
  
print?
  
public class DBServerInitializer extends ChannelInitializer<SocketChannel> {

@Override
  
public void initChannel(SocketChannel ch) {
  
ChannelPipeline pipeline = ch.pipeline();

pipeline.addLast("decoder", new HttpRequestDecoder());
  
pipeline.addLast("encoder", new HttpResponseEncoder());

pipeline.addLast("deflater", new HttpContentCompressor());

pipeline.addLast("handler", new DBServerHandler());
  
}
  
}
