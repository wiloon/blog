---
title: Guava cache
author: "-"
date: 2017-03-31T06:58:32+00:00
url: /?p=10004
categories:
  - Inbox
tags:
  - reprint
---
## Guava cache
http://www.cnblogs.com/peida/p/Guava_Cache.html

缓存,在我们日常开发中是必不可少的一种解决性能问题的方法。简单的说,cache 就是为了提升系统性能而开辟的一块内存空间。

缓存的主要作用是暂时在内存中保存业务系统的数据处理结果,并且等待下次访问使用。在日常开发的很多场合,由于受限于硬盘IO的性能或者我们自身业务系统的数据处理和获取可能非常费时,当我们发现我们的系统这个数据请求量很大的时候,频繁的IO和频繁的逻辑处理会导致硬盘和CPU资源的瓶颈出现。缓存的作用就是将这些来自不易的数据保存在内存中,当有其他线程或者客户端需要查询相同的数据资源时,直接从缓存的内存块中返回数据,这样不但可以提高系统的响应时间,同时也可以节省对这些数据的处理流程的资源消耗,整体上来说,系统性能会有大大的提升。

缓存在很多系统和架构中都用广泛的应用,例如: 

1.CPU缓存
  
2.操作系统缓存
  
3.本地缓存
  
4.分布式缓存
  
5.HTTP缓存
  
6.数据库缓存
  
等等,可以说在计算机和网络领域,缓存无处不在。可以这么说,只要有硬件性能不对等,涉及到网络传输的地方都会有缓存的身影。

Guava Cache是一个全内存的本地缓存实现,它提供了线程安全的实现机制。整体上来说Guava cache 是本地缓存的不二之选,简单易用,性能好。

Guava Cache有两种创建方式: 

1. cacheLoader
  
2. callable callback

通过这两种方法创建的cache,和通常用map来缓存的做法比,不同在于,这两种方法都实现了一种逻辑——从缓存中取key X的值,如果该值已经缓存过了,则返回缓存中的值,如果没有缓存过,可以通过某个方法来获取这个值。但不同的在于cacheloader的定义比较宽泛,是针对整个cache定义的,可以认为是统一的根据key值load value的方法。而callable的方式较为灵活,允许你在get的时候指定。

cacheLoader方式实现实例: 
  
@Test
  
public void TestLoadingCache() throws Exception{
  
LoadingCache<String,String> cahceBuilder=CacheBuilder
  
.newBuilder()
  
.build(new CacheLoader<String, String>(){
  
@Override
  
public String load(String key) throws Exception {
  
String strProValue="hello "+key+"!";
  
return strProValue;
  
}

});

System.out.println("jerry value:"+cahceBuilder.apply("jerry"));
  
System.out.println("jerry value:"+cahceBuilder.get("jerry"));
  
System.out.println("peida value:"+cahceBuilder.get("peida"));
  
System.out.println("peida value:"+cahceBuilder.apply("peida"));
  
System.out.println("lisa value:"+cahceBuilder.apply("lisa"));
  
cahceBuilder.put("harry", "ssdded");
  
System.out.println("harry value:"+cahceBuilder.get("harry"));
  
}

输出: 
  
jerry value:hello jerry!
  
jerry value:hello jerry!
  
peida value:hello peida!
  
peida value:hello peida!
  
lisa value:hello lisa!
  
harry value:ssdded

callable callback的实现: 
  
@Test
  
public void testcallableCache()throws Exception{
  
Cache<String, String> cache = CacheBuilder.newBuilder().maximumSize(1000).build();
  
String resultVal = cache.get("jerry", new Callable<String>() {
  
public String call() {
  
String strProValue="hello "+"jerry"+"!";
  
return strProValue;
  
}
  
});
  
System.out.println("jerry value : " + resultVal);

resultVal = cache.get("peida", new Callable<String>() {
  
public String call() {
  
String strProValue="hello "+"peida"+"!";
  
return strProValue;
  
}
  
});
  
System.out.println("peida value : " + resultVal);
  
}

输出: 
  
jerry value : hello jerry!
  
peida value : hello peida!

cache的参数说明: 

回收的参数: 
  
1. 大小的设置: CacheBuilder.maximumSize(long)  CacheBuilder.weigher(Weigher)  CacheBuilder.maxumumWeigher(long)
  
2. 时间: expireAfterAccess(long, TimeUnit) expireAfterWrite(long, TimeUnit)
  
3. 引用: CacheBuilder.weakKeys() CacheBuilder.weakValues()  CacheBuilder.softValues()
  
4. 明确的删除: invalidate(key)  invalidateAll(keys)  invalidateAll()
  
5. 删除监听器: CacheBuilder.removalListener(RemovalListener)
  
refresh机制: 
  
1. LoadingCache.refresh(K)  在生成新的value的时候,旧的value依然会被使用。
  
2. CacheLoader.reload(K, V) 生成新的value过程中允许使用旧的value
  
3. CacheBuilder.refreshAfterWrite(long, TimeUnit) 自动刷新cache

基于泛型的实现: 
  
/**
  
* 不需要延迟处理(泛型的方式封装)
  
* @return
  
*/
  
public <K , V> LoadingCache<K , V> cached(CacheLoader<K , V> cacheLoader) {
  
LoadingCache<K , V> cache = CacheBuilder
  
.newBuilder()
  
.maximumSize(2)
  
.weakKeys()
  
.softValues()
  
.refreshAfterWrite(120, TimeUnit.SECONDS)
  
.expireAfterWrite(10, TimeUnit.MINUTES)
  
.removalListener(new RemovalListener<K, V>(){
  
@Override
  
public void onRemoval(RemovalNotification<K, V> rn) {
  
System.out.println(rn.getKey()+"被移除");

}})
  
.build(cacheLoader);
  
return cache;
  
}

/**
  
* 通过key获取value
  
* 调用方式 commonCache.get(key) ; return String
  
* @param key
  
* @return
  
* @throws Exception
  
*/

public LoadingCache<String , String> commonCache(final String key) throws Exception{
  
LoadingCache<String , String> commonCache= cached(new CacheLoader<String , String>(){
  
@Override
  
public String load(String key) throws Exception {
  
return "hello "+key+"!";
  
}
  
});
  
return commonCache;
  
}

@Test
  
public void testCache() throws Exception{
  
LoadingCache<String , String> commonCache=commonCache("peida");
  
System.out.println("peida:"+commonCache.get("peida"));
  
commonCache.apply("harry");
  
System.out.println("harry:"+commonCache.get("harry"));
  
commonCache.apply("lisa");
  
System.out.println("lisa:"+commonCache.get("lisa"));
  
}

输出: 

peida:hello peida!
  
harry:hello harry!
  
peida被移除
  
lisa:hello lisa!
  
基于泛型的Callable Cache实现: 
  
private static Cache<String, String> cacheFormCallable = null;
  
/**
  
* 对需要延迟处理的可以采用这个机制；(泛型的方式封装)
  
* @param <K>
  
* @param <V>
  
* @param key
  
* @param callable
  
* @return V
  
* @throws Exception
  
*/
  
public static <K,V> Cache<K , V> callableCached() throws Exception {
  
Cache<K, V> cache = CacheBuilder
  
.newBuilder()
  
.maximumSize(10000)
  
.expireAfterWrite(10, TimeUnit.MINUTES)
  
.build();
  
return cache;
  
}
  
private String getCallableCache(final String userName) {
  
try {
  
//Callable只有在缓存值不存在时,才会调用
  
return cacheFormCallable.get(userName, new Callable<String>() {
  
@Override
  
public String call() throws Exception {
  
System.out.println(userName+" from db");
  
return "hello "+userName+"!";
  
}
  
});
  
} catch (ExecutionException e) {
  
e.printStackTrace();
  
return null;
  
}
  
}

@Test
  
public void testCallableCache() throws Exception{
  
final String u1name = "peida";
  
final String u2name = "jerry";
  
final String u3name = "lisa";
  
cacheFormCallable=callableCached();
  
System.out.println("peida:"+getCallableCache(u1name));
  
System.out.println("jerry:"+getCallableCache(u2name));
  
System.out.println("lisa:"+getCallableCache(u3name));
  
System.out.println("peida:"+getCallableCache(u1name));

}

输出: 
  
peida from db
  
peida:hello peida!
  
jerry from db
  
jerry:hello jerry!
  
lisa from db
  
lisa:hello lisa!
  
peida:hello peida!

说明: Callable只有在缓存值不存在时,才会调用,比如第二次调用getCallableCache(u1name)直接返回缓存中的值

guava Cache数据移除: 

guava做cache时候数据的移除方式,在guava中数据的移除分为被动移除和主动移除两种。
  
被动移除数据的方式,guava默认提供了三种方式: 
  
1.基于大小的移除:看字面意思就知道就是按照缓存的大小来移除,如果即将到达指定的大小,那就会把不常用的键值对从cache中移除。
  
定义的方式一般为 CacheBuilder.maximumSize(long),还有一种一种可以算权重的方法,个人认为实际使用中不太用到。就这个常用的来看有几个注意点,
  
其一,这个size指的是cache中的条目数,不是内存大小或是其他；
  
其二,并不是完全到了指定的size系统才开始移除不常用的数据的,而是接近这个size的时候系统就会开始做移除的动作；
  
其三,如果一个键值对已经从缓存中被移除了,你再次请求访问的时候,如果cachebuild是使用cacheloader方式的,那依然还是会从cacheloader中再取一次值,如果这样还没有,就会抛出异常
  
2.基于时间的移除: guava提供了两个基于时间移除的方法
  
expireAfterAccess(long, TimeUnit)  这个方法是根据某个键值对最后一次访问之后多少时间后移除
  
expireAfterWrite(long, TimeUnit)  这个方法是根据某个键值对被创建或值被替换后多少时间移除
  
3.基于引用的移除: 
  
这种移除方式主要是基于java的垃圾回收机制,根据键或者值的引用关系决定移除
  
主动移除数据方式,主动移除有三种方法: 
  
1.单独移除用 Cache.invalidate(key)
  
2.批量移除用 Cache.invalidateAll(keys)
  
3.移除所有用 Cache.invalidateAll()
  
如果需要在移除数据的时候有所动作还可以定义Removal Listener,但是有点需要注意的是默认Removal Listener中的行为是和移除动作同步执行的,如果需要改成异步形式,可以考虑使用RemovalListeners.asynchronous(RemovalListener, Executor)