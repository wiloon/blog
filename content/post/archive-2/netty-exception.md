---
title: 'Netty 中 IOException,Connection reset by peer 与 java.nio.channels.ClosedChannelException,null'
author: "-"
date: 2016-01-07T00:48:19+00:00
url: /?p=8657
categories:
  - Inbox
tags:
  - reprint
---
## 'Netty 中 IOException,Connection reset by peer 与 java.nio.channels.ClosedChannelException,null'

<http://www.cnblogs.com/zemliu/p/3864131.html>

最近发现系统中出现了很多 IOException: Connection reset by peer 与 ClosedChannelException: null

深入看了看代码, 做了些测试, 发现 Connection reset 会在客户端不知道 channel 被关闭的情况下, 触发了 eventloop 的 unsafe.read() 操作抛出

而 ClosedChannelException 一般是由 Netty 主动抛出的, 在 AbstractChannel 以及 SSLHandler 里都可以看到 ClosedChannel 相关的代码

AbstractChannel

static final ClosedChannelException CLOSED_CHANNEL_EXCEPTION = new ClosedChannelException();

static {
    CLOSED_CHANNEL_EXCEPTION.setStackTrace(EmptyArrays.EMPTY_STACK_TRACE);
    NOT_YET_CONNECTED_EXCEPTION.setStackTrace(EmptyArrays.EMPTY_STACK_TRACE);
}

@Override
        public void write(Object msg, ChannelPromise promise) {
            ChannelOutboundBuffer outboundBuffer = this.outboundBuffer;
            if (outboundBuffer == null) {
                // If the outboundBuffer is null we know the channel was closed and so
                // need to fail the future right away. If it is not null the handling of the rest
                // will be done in flush0()
                // See <https://github.com/netty/netty/issues/2362>
                safeSetFailure(promise, CLOSED_CHANNEL_EXCEPTION);
                // release message now to prevent resource-leak
                ReferenceCountUtil.release(msg);
                return;
            }
            outboundBuffer.addMessage(msg, promise);
        }
  
    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
在代码的许多部分, 都会有这个 ClosedChannelException, 大概的意思是说在 channel close 以后, 如果还调用了 write 方法, 则会将 write 的 future 设置为 failure, 并将 cause 设置为 ClosedChannelException, 同样 SSLHandler 中也类似

------

回到 Connection reset by peer, 要模拟这个情况比较简单, 就是在 server 端设置一个在 channelActive 的时候就 close channel 的 handler. 而在 client 端则写一个 Connect 成功后立即发送请求数据的 listener. 如下

client

    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
      public static void main(String[] args) throws IOException, InterruptedException {
        Bootstrap b = new Bootstrap();
        b.group(new NioEventLoopGroup())
                .channel(NioSocketChannel.class)
                .handler(new ChannelInitializer<NioSocketChannel>() {
                    @Override
                    protected void initChannel(NioSocketChannel ch) throws Exception {
                    }
                });
        b.connect("localhost", 8090).addListener(new ChannelFutureListener() {
            @Override
            public void operationComplete(ChannelFuture future) throws Exception {
                if (future.isSuccess()) {
                    future.channel().write(Unpooled.buffer().writeBytes("123".getBytes()));
                    future.channel().flush();
                }
            }
        });
  
  
    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
server

    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
  public class SimpleServer {

    public static void main(String[] args) throws Exception {

        EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        EventLoopGroup workerGroup = new NioEventLoopGroup();
        ServerBootstrap b = new ServerBootstrap();
        b.group(bossGroup, workerGroup)
                .channel(NioServerSocketChannel.class)
                .option(ChannelOption.SO_REUSEADDR, true)
                .childHandler(new ChannelInitializer<NioSocketChannel>() {
                    @Override
                    protected void initChannel(NioSocketChannel ch) throws Exception {
                        ch.pipeline().addLast(new SimpleServerHandler());
                    }
                });
        b.bind(8090).sync().channel().closeFuture().sync();
    }
}

public class SimpleServerHandler extends ChannelInboundHandlerAdapter {
    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        ctx.channel().close().sync();
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, final Object msg) throws Exception {
        System.out.println(123);
    }

    @Override
    public void channelInactive(ChannelHandlerContext ctx) throws Exception {
        System.out.println("inactive");
    }
}
  
    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
这种情况之所以能触发 connection reset by peer 异常, 是因为 connect 成功以后, client 段先会触发 connect 成功的 listener, 这个时候 server 段虽然断开了 channel, 也触发 channel 断开的事件 (它会触发一个客户端 read 事件, 但是这个 read 会返回 -1, -1 代表 channel 关闭, client 的 channelInactive 跟 channel  active 状态的改变都是在这时发生的), 但是这个事件是在 connect 成功的 listener 之后执行, 所以这个时候 listener 里的 channel 并不知道自己已经断开, 它还是会继续进行 write 跟 flush 操作, 在调用 flush 后, eventloop 会进入 OP_READ 事件里, 这时候 unsafe.read() 就会抛出 connection reset 异常. eventloop 代码如下

NioEventLoop

    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
  private static void processSelectedKey(SelectionKey k, AbstractNioChannel ch) {
        final NioUnsafe unsafe = ch.unsafe();
        if (!k.isValid()) {
            // close the channel if the key is not valid anymore
            unsafe.close(unsafe.voidPromise());
            return;
        }

        try {
            int readyOps = k.readyOps();
            // Also check for readOps of 0 to workaround possible JDK bug which may otherwise lead
            // to a spin loop
            if ((readyOps & (SelectionKey.OP_READ | SelectionKey.OP_ACCEPT)) != 0 || readyOps == 0) {
                unsafe.read();
                if (!ch.isOpen()) {
                    // Connection already closed - no need to handle write.
                    return;
                }
            }
            if ((readyOps & SelectionKey.OP_WRITE) != 0) {
                // Call forceFlush which will also take care of clear the OP_WRITE once there is nothing left to write
                ch.unsafe().forceFlush();
            }
            if ((readyOps & SelectionKey.OP_CONNECT) != 0) {
                // remove OP_CONNECT as otherwise Selector.select(..) will always return without blocking
                // See https://github.com/netty/netty/issues/924
                int ops = k.interestOps();
                ops &= ~SelectionKey.OP_CONNECT;
                k.interestOps(ops);

                unsafe.finishConnect();
            }
        } catch (CancelledKeyException e) {
            unsafe.close(unsafe.voidPromise());
        }
    }
  
  
    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
这就是 connection reset by peer 产生的原因

------

再来看 ClosedChannelException 如何产生, 要复现他也很简单. 首先要明确, 并没有客户端主动关闭才会出现 ClosedChannelException 这么一说. 下面来看两种出现 ClosedChannelException 的客户端写法

client 1, 主动关闭 channel

    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
  public class SimpleClient {

    private static final Logger logger = LoggerFactory.getLogger(SimpleClient.class);

    public static void main(String[] args) throws IOException, InterruptedException {
        Bootstrap b = new Bootstrap();
        b.group(new NioEventLoopGroup())
                .channel(NioSocketChannel.class)
                .handler(new ChannelInitializer<NioSocketChannel>() {
                    @Override
                    protected void initChannel(NioSocketChannel ch) throws Exception {
                    }
                });
        b.connect("localhost", 8090).addListener(new ChannelFutureListener() {
            @Override
            public void operationComplete(ChannelFuture future) throws Exception {
                if (future.isSuccess()) {
                    future.channel().close();
                    future.channel().write(Unpooled.buffer().writeBytes("123".getBytes())).addListener(new ChannelFutureListener() {
                        @Override
                        public void operationComplete(ChannelFuture future) throws Exception {
                            if (!future.isSuccess()) {
                                logger.error("Error", future.cause());
                            }
                        }
                    });
                    future.channel().flush();
                }
            }
        });
    }
}
  
    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
只要在 write 之前主动调用了 close, 那么 write 必然会知道 close 是 close 状态, 最后 write 就会失败, 并且 future 里的 cause 就是 ClosedChannelException

-------

client 2. 由服务端造成的 ClosedChannelException

    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
  public class SimpleClient {

    private static final Logger logger = LoggerFactory.getLogger(SimpleClient.class);

    public static void main(String[] args) throws IOException, InterruptedException {
        Bootstrap b = new Bootstrap();
        b.group(new NioEventLoopGroup())
                .channel(NioSocketChannel.class)
                .handler(new ChannelInitializer<NioSocketChannel>() {
                    @Override
                    protected void initChannel(NioSocketChannel ch) throws Exception {
                    }
                });
        Channel channel = b.connect("localhost", 8090).sync().channel();
        Thread.sleep(3000);
        channel.writeAndFlush(Unpooled.buffer().writeBytes("123".getBytes())).addListener(new ChannelFutureListener() {
            @Override
            public void operationComplete(ChannelFuture future) throws Exception {
                if (!future.isSuccess()) {
                    logger.error("error", future.cause());
                }
            }
        });
    }
}
  
    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
服务端

    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
  public class SimpleServer {

    public static void main(String[] args) throws Exception {

        EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        EventLoopGroup workerGroup = new NioEventLoopGroup();
        ServerBootstrap b = new ServerBootstrap();
        b.group(bossGroup, workerGroup)
                .channel(NioServerSocketChannel.class)
                .option(ChannelOption.SO_REUSEADDR, true)
                .childHandler(new ChannelInitializer<NioSocketChannel>() {
                    @Override
                    protected void initChannel(NioSocketChannel ch) throws Exception {
                        ch.pipeline().addLast(new SimpleServerHandler());
                    }
                });
        b.bind(8090).sync().channel().closeFuture().sync();
    }
}
  
    <img src="http://common.cnblogs.com/images/copycode.gif" alt="复制代码" />
  
这种情况下,  服务端将 channel 关闭, 客户端先 sleep, 这期间 client 的 eventLoop 会处理客户端关闭的时间, 也就是 eventLoop 的 processKey 方法会进入 OP_READ, 然后 read 出来一个 -1, 最后触发 client channelInactive 事件, 当 sleep 醒来以后, 客户端调用 writeAndFlush, 这时候客户端 channel 的状态已经变为了 inactive, 所以 write 失败, cause 为 ClosedChannelException
