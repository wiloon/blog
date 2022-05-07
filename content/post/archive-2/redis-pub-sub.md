---
title: redis pub sub
author: "-"
date: 2017-12-18T13:47:16+00:00
url: /?p=11635
categories:
  - Inbox
tags:
  - reprint
---
## redis pub sub
PubSub 的缺点
尽管 Redis 实现了 PubSub 模式来达到了 多播消息队列 的目的,但在实际的消息队列的领域,几乎 找不到特别合适的场景,因为它的缺点十分明显: 

- 没有 Ack 机制,也不保证数据的连续:  PubSub 的生产者传递过来一个消息,Redis 会直接找到相应的消费者传递过去。如果没有一个消费者,那么消息会被直接丢弃。如果开始有三个消费者,其中一个突然挂掉了,过了一会儿等它再重连时,那么重连期间的消息对于这个消费者来说就彻底丢失了。
- 不持久化消息:  如果 Redis 停机重启,PubSub 的消息是不会持久化的,毕竟 Redis 宕机就相当于一个消费者都没有,所有的消息都会被直接丢弃。
基于上述缺点,Redis 的作者甚至单独开启了一个 Disque 的项目来专门用来做多播消息队列,不过该项目目前好像都没有成熟。不过后来在 2018 年 6 月,Redis 5.0 新增了 Stream 数据结构,这个功能给 Redis 带来了 持久化消息队列,从此 PubSub 作为消息队列的功能可以说是就消失了

```bash
redis-cli -h redis.wiloon.com
SUBSCRIBE channel0
publish channel0 message0
```

http://redisbook.readthedocs.io/en/latest/feature/pubsub.html

在消费者下线的情况下,生产的消息会丢失,得使用专业的消息队列如RocketMQ等。


http://blog.csdn.net/lihao21/article/details/48370687

Redis为我们提供了publish/subscribe(发布/订阅)功能。我们可以对某个channel(频道)进行subscribe(订阅),当有人在这个channel上publish(发布)消息时,redis就会通知我们,这样我们可以收到别人发布的消息。
  
作为Java的redis客户端,Jedis提供了publish/subscribe的接口。本文讲述如何使用Jedis来实现redis的publish/subscribe。

定义Subscriber类
  
Jedis定义了抽象类JedisPubSub,在这个类中,定义publish/subsribe的回调方法。通过继承JedisPubSub类并重新实现这些回调方法,当publish/subsribe事件发生时,我们可以定制自己的处理逻辑。

在以下例子中,我们定义了Subscriber类,这个类继承了JedisPubSub类,并重新实现了其中的回调方法。

Subscriber.java

import redis.clients.jedis.JedisPubSub;
  
public class Subscriber extends JedisPubSub {
  
public Subscriber() {
  
}

public void onMessage(String channel, String message) {
  
System.out.println(String.format("receive redis published message, channel %s, message %s", channel, message));
  
}

public void onSubscribe(String channel, int subscribedChannels) {
  
System.out.println(String.format("subscribe redis channel success, channel %s, subscribedChannels %d",
  
channel, subscribedChannels));
  
}

public void onUnsubscribe(String channel, int subscribedChannels) {
  
System.out.println(String.format("unsubscribe redis channel, channel %s, subscribedChannels %d",
  
channel, subscribedChannels));

}
  
}
  
定义SubThread线程类
  
由于Jedis的subscribe操作是阻塞的,因此,我们另起一个线程来进行subscribe操作。

SubThread.java

import redis.clients.jedis.Jedis;
  
import redis.clients.jedis.JedisPool;
  
public class SubThread extends Thread {
  
private final JedisPool jedisPool;
  
private final Subscriber subscriber = new Subscriber();

private final String channel = "mychannel";

public SubThread(JedisPool jedisPool) {
  
super("SubThread");
  
this.jedisPool = jedisPool;
  
}

@Override
  
public void run() {
  
System.out.println(String.format("subscribe redis, channel %s, thread will be blocked", channel));
  
Jedis jedis = null;
  
try {
  
jedis = jedisPool.getResource();
  
jedis.subscribe(subscriber, channel);
  
} catch (Exception e) {
  
System.out.println(String.format("subsrcibe channel error, %s", e));
  
} finally {
  
if (jedis != null) {
  
jedis.close();
  
}
  
}
  
}
  
}
  
在上面的代码中,我们从JedisPool获取一个Jedis实例,并使用这个Jedis实例进行subscribe的操作。
  
Jedis的subscribe的声明如下: 

public void subscribe(final JedisPubSub jedisPubSub, final String… channels)
  
第一个参数接受一个JedisPubSub对象,第二个参数指定对哪个频道进行订阅。上例中,我们把我们定义的Subscriber对象传给subscribe方法。
  
当publish/subscribe的事件发生时,会自动调用我们Subscriber的方法。

定义Publisher类
  
Publisher类接受用户的输入,并将输入发布到channel。当用户输入"quit"后,输入结束。

Publisher.java

import java.io.BufferedReader;
  
import java.io.IOException;
  
import java.io.InputStreamReader;

import redis.clients.jedis.Jedis;
  
import redis.clients.jedis.JedisPool;

public class Publisher {
  
private final JedisPool jedisPool;

public Publisher(JedisPool jedisPool) {
  
this.jedisPool = jedisPool;
  
}

public void start() {
  
BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
  
Jedis jedis = jedisPool.getResource();
  
while (true) {
  
String line = null;
  
try {
  
line = reader.readLine();
  
if (!"quit".equals(line)) {
  
jedis.publish("mychannel", line);
  
} else {
  
break;
  
}
  
} catch (IOException e) {
  
e.printStackTrace();
  
}
  
}
  
}
  
}
  
定义入口代码
  
如下是我们的程序入口代码。

PubSubDemo.java

import redis.clients.jedis.JedisPool;
  
import redis.clients.jedis.JedisPoolConfig;
  
public class PubSubDemo
  
{
  
public static void main( String[] args )
  
{
  
// 替换成你的reids地址和端口
  
String redisIp = "192.168.229.154";
  
int reidsPort = 6379;
  
JedisPool jedisPool = new JedisPool(new JedisPoolConfig(), redisIp, reidsPort);
  
System.out.println(String.format("redis pool is starting, redis ip %s, redis port %d", redisIp, reidsPort));

SubThread subThread = new SubThread(jedisPool);
  
subThread.start();

Publisher publisher = new Publisher(jedisPool);
  
publisher.start();
  
}
  
}
  
在上面的代码中,我们首先生成了一个JedisPool的redis连接池,这是由于Jedis不是线程安全的,JedisPool是线程安全的。而我们的程序在主线程和订阅线程(SubThread)均需要使用Jedis,故在程序中我们使用JedisPool。具体也可以参考在多线程环境中使用Jedis。
  
由于Jedis的subcribe操作是阻塞的,故我们另起了一个线程来进行subcribe操作。
  
通过调用Publisher::start()方法,接受用户的输入,并publish到指定的channel。

输出
  
redis pool is starting, redis ip 192.168.229.154, redis port 6379
  
subscribe redis, channel mychannel, thread will be blocked
  
subscribe redis channel success, channel mychannel, subscribedChannels 1
  
这时输入

hello
  
控制窗口中输出

receive redis published message, channel mychannel, message hello
  
参考资料
  
https://github.com/xetorthio/jedis/wiki/AdvancedUsage
  
http://basrikahveci.com/a-simple-jedis-publish-subscribe-example/


