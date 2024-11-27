---
title: RSSX
author: "-"
date: 2019-02-17T06:40:06+00:00
url: rssx
categories:
  - Inbox
tags:
  - reprint
---
## RSSX

A RSS Reader

## redis key

### 某一个feed的 所有 news id，按时间排序的

key: feed_news:feedId0
type: sort set， zset
value: newsId

### 文章内容

key: news:newsId0
type: hash
value: 文章内容， 数据量最大

## 记录用户阅读位置

用已读索引和已读集合记录用户阅读位置
已读索引 用于记录用户feed已读和未读的边界， 记录连续的已读未读位置
已读集合 用于记录已读边界外，用户分散阅读的文章，记录不连续的已读集合

### 已读索引

key: read_index:userId0:feedId0
type: string
value: feed_news（zset）的score值

### 已读集合， 已读文章标记为灰色

key: read_mark:userId0:feedId0
type: set
value: newsId

###

- 显示feed 列表时，显示未读文章数，feed总数-索引=未读数量
- 按feed id 加载一页未读文章时，按索引range取
- 标记某一页为已读时，取上一次的已读索引位置， 加每页显示数，记录新的已读索引
- 加载某个feed的一页未读文章时，查询大于等于某一个 score 的第一条数据的索引

### ZSCORE， 成员member的score值

### ZRANGE, 返回指定区间内的成员

### ZRANGEBYSCORE, 返回有序集合中指定分数区间的成员列表 - 正序

### ZRANK, 返回指定成员的排名(位置值,0表示第一个成员) - 正序

### 移除有序集中，指定排名(rank)区间内的所有成员

### 移除有序集中，指定分数（score）区间内的所有成员

### 部署

### redis

### sql

db: sqlite3

```sql
CREATE TABLE if not exists users (  id char(36) PRIMARY KEY NOT NULL,  name varchar(50) DEFAULT NULL,  create_time timestamp DEFAULT NULL);

create table feeds
(
    id UNSIGNED BIG INT
        constraint feed_pk
            primary key,
    title   varchar(256),
    url     varchar(1024),
    deleted TINYINT
);


INSERT INTO `users` VALUES
                       (0,'wiloon','2017-12-07 22:10:49'),
                       (1,'foo','2017-12-09 13:16:15');

INSERT INTO feeds VALUES
                       (1,'InfoQ','https://www.infoq.cn/feed',0),
                       (3,'CoolShell','https://coolshell.cn/feed',0),
                       (4,'Solidot','https://www.solidot.org/index.rss',0),
                       (7,'Engadget-CN','https://chinese.engadget.com/rss.xml',0),
                       (8,'Infozm','https://node2.feed43.com/infzmnews.xml',0),
                       (9,'Engadget-EN','https://www.engadget.com/rss.xml',0),
                       (10,'36ke','https://www.36kr.com/feed',0),
                       (11,'FT','https://www.ftchinese.com/rss/news',0),
                       (12,'OS China','https://www.oschina.net/news/rss',0),
                       (13,'draveness','https://draveness.me/feed.xml',0);

CREATE TABLE IF NOT EXISTS `user_feeds` (
                                           `user_id` bigint(20) NOT NULL,
                                           `feed_id` bigint(20) NOT NULL,
                                           PRIMARY KEY (`user_id`,`feed_id`)
);

INSERT INTO user_feeds VALUES
                            (0,0),
                            (0,1),
                            (0,2),
                            (0,3),
                            (0,4),
                            (0,5),
                            (0,6),
                            (0,7),
                            (0,8),
                            (0,9),
                            (0,10),
                            (0,11),
                            (0,12),
                            (0,13),
                            (1,0),
                            (1,1);

```
