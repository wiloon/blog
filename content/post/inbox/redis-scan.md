---
title: "redis scan"
author: "-"
date: "2021-07-21 22:27:27"
url: "redis-scan"
categories:
  - cache
tags:
  - redis
---
## "redis scan"
### redis用scan代替keys
众所周知，当redis中key数量越大，keys 命令执行越慢，而且最重要的会阻塞服务器，对单线程的redis来说，简直是灾难，且在生产环境，keys命令一般是被禁止的。scan可用来替换keys请求。

所以说官方的建议是: 生产环境屏蔽掉 keys 命令。

在对键进行增量式迭代的过程中， 键可能会被修改， 所以增量式迭代命令只能对被返回的元素提供有限的保证 。

### scan用法
    SCAN cursor [MATCH pattern] [COUNT count]
    scan 0  match *news* count 3

scan是一个增量迭代式的命令，这意味着每次调用这个命令都会返回一个游标cursor，该游标用于下次查询。查询开始时，cursor值为0；当查询结束时，cursor的值也回归到0。

举个例子: 

# 开始查询，scan cursor为0，返回的cursor为17
redis 127.0.0.1:6379> scan 0
1) "17"
2)  1) "key:12"
    2) "key:8"
    3) "key:4"
    4) "key:14"
    5) "key:16"
    6) "key:17"
    7) "key:15"
    8) "key:10"
    9) "key:3"
   10) "key:7"
   11) "key:1"
# 下一次查询，以上一次查询返回的cursor为起始位置
redis 127.0.0.1:6379> scan 17
# 查询返回cursor为0，标志查询结束
1) "0"
2) 1) "key:5"
   2) "key:18"
   3) "key:0"
   4) "key:2"
   5) "key:19"
   6) "key:13"
   7) "key:6"
   8) "key:9"
   9) "key:11"
count
count可理解为迭代过程中的步长，指每次调用scan时应执行的工作量，该值默认为10。每次调用count的值可以随意指定，只要下一次传递cursor是上一次调用返回的cursor就行。

match
需要注意的是，match操作时在元素被检出后执行的。假设redis中只有少量元素符合pattern条件，那么很可能在多次调用中scan返回的数据为空，例如: 

# 查找key中包含11的键，因为这里没有指定count，所以默认为10
redis 127.0.0.1:6379> scan 0 MATCH *11*
1) "288"
2) 1) "key:911"
# 在这次调用中，count为10，起始cursor为288，返回的结果中并没有满足*11*条件的key
redis 127.0.0.1:6379> scan 288 MATCH *11*
1) "224"
2) (empty list or set)
redis 127.0.0.1:6379> scan 224 MATCH *11*
1) "80"
2) (empty list or set)
redis 127.0.0.1:6379> scan 80 MATCH *11*
1) "176"
2) (empty list or set)
# count指定为1000，找到了。
redis 127.0.0.1:6379> scan 176 MATCH *11* COUNT 1000
1) "0"
2)  1) "key:611"
    2) "key:711"
    3) "key:118"
    4) "key:117"
    5) "key:311"
    6) "key:112"
    7) "key:111"
    8) "key:110"
    9) "key:113"
   10) "key:211"
   11) "key:411"
   12) "key:115"
   13) "key:116"
   14) "key:114"
   15) "key:119"
   16) "key:811"
   17) "key:511"
   18) "key:11"
redis 127.0.0.1:6379>
scan的优缺点
可以看出，Redis的SCAN操作由于其整体的数据设计，无法提供特别准的scan操作，仅仅是一个“can ‘ t guarantee ， just do my best”的实现: 

提供键空间的遍历操作，支持游标，复杂度O(1), 整体遍历一遍只需要O(N)；
提供结果模式匹配；
支持一次返回的数据条数设置，但仅仅是个hints，有时候返回的会多；
弱状态，所有状态只需要客户端需要维护一个游标；
无法提供完整的快照遍历，也就是中间如果有数据修改，可能有些涉及改动的数据遍历不到；
每次返回的数据条数不一定，极度依赖内部实现；
返回的数据可能有重复，应用层必须能够处理重入逻辑；上面的示例代码中，redisTemplate.execute方法是个Set，相当于已经对于返回的key去重
count是每次扫描的key个数，并不是结果集个数。count要根据扫描数据量大小而定，Scan虽然无锁，但是也不能保证在超过百万数据量级别搜索效率；count不能太小，网络交互会变多，count要尽可能的大。在搜索结果集1万以内，建议直接设置为与所搜集大小相同
spring中使用scan实现keys
    /** * 以count为步长查找符合pattern条件的keys * * @param redisTemplate 指定redis * @param pattern 匹配条件 * @param count 一次在count条记录中match符合pattern条件的记录。若count<=0,使用1000 * @return Set<String> 若limit<= 0,返回所有;否则返回查找结果 */
    public Set<String> scanKeys(RedisTemplate<String, Object> redisTemplate, String pattern, int count) {

        log.info("pattern:{}, count:{}", pattern, count);
        return redisTemplate.execute(new RedisCallback<Set<String>>() {
            @Override
            public Set<String> doInRedis(RedisConnection connection) throws DataAccessException {
                Set<String> tmpKeys = new HashSet<>();
                ScanOptions options;
                if (count <= 0) {
                    options = ScanOptions.scanOptions().match(pattern).count(1000).build();
                } else {
                    options = ScanOptions.scanOptions().match(pattern).count(count).build();
                }
                // 迭代一直查找，直到找到redis中所有满足条件的key为止(cursor变为0为止)
                Cursor<byte[]> cursor = connection.scan(options);
                while (cursor.hasNext()) {
                    tmpKeys.add(new String(cursor.next()));
                }
                return tmpKeys;
            }
        });
    }
Jedis使用scan实现keys
    /** * 扫描keys方法，替代Keys接口 * @param jedis * @param keyPattern * @return */
    public static Set<String> scanKeys(Jedis jedis, String keyPattern) {
        Set<String> keys = new HashSet<>();
        String cursor = ScanParams.SCAN_POINTER_START;
        ScanParams sp = new ScanParams();
        sp.match(keyPattern);
        sp.count(1000);
        do{
            ScanResult<String> ret = jedis.scan(cursor, sp);
            List<String> result = ret.getResult();
            if(result!=null && result.size() > 0){
                keys.addAll(result);
            }
            //再处理cursor
            cursor = ret.getCursor();
            // 迭代一直到cursor变为0为止
        }while(!cursor.equals(ScanParams.SCAN_POINTER_START));
        return keys;
    }
参考链接
https://redis.io/commands/scan

https://blog.csdn.net/qq_27623337/article/details/53201202

https://my.oschina.net/u/3747772/blog/1588983


https://horizonliu.github.io/2019/07/25/Redis%E7%94%A8scan%E4%BB%A3%E6%9B%BFkeys/
