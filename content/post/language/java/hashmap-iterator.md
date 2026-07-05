---
title: "HashMap 遍历: entrySet vs keySet"
author: "-"
date: 2014-04-02T10:26:29+08:00
lastmod: 2026-07-04T16:34:09+08:00
url: hashmap-iterator
categories:
  - Java
tags:
  - java
  - remix
  - AI-assisted
aliases:
  - /hashmap遍历/
  - /map-iterator/
  - /p3833/
---
## 两种遍历方式

`HashMap` 常见的遍历方式有两种：`entrySet()` 和 `keySet()`。两者最终都能拿到全部键值对，但性能有差别。

### entrySet（推荐）

```java
Map<String, String> map = new HashMap<>();
Iterator<Map.Entry<String, String>> iter = map.entrySet().iterator();
while (iter.hasNext()) {
    Map.Entry<String, String> entry = iter.next();
    String key = entry.getKey();
    String val = entry.getValue();
}
```

`entry` 中已经同时持有 key 和 value，取值时不需要再回查一次 map。

### keySet

```java
Map<String, String> map = new HashMap<>();
Iterator<String> iter = map.keySet().iterator();
while (iter.hasNext()) {
    String key = iter.next();
    String val = map.get(key); // extra lookup for every key
}
```

`keySet()` 只拿到 key 的集合，遍历时还要对每个 key 再调用一次 `map.get(key)` 才能取到 value。

## 性能对比

`keySet()` 版本相当于遍历了两次：一次生成 key 的迭代器，一次通过 `get(key)` 查值；`entrySet()` 版本在生成迭代器时就把 key 和 value 一起放进了 `Entry`，只需遍历一次。

可以用一个简单的基准来观察差异：

```java
Map<String, String> map = new HashMap<>();
for (int i = 0; i < 100_000; i++) {
    map.put("key" + i, "value" + i);
}

// entrySet: single pass
long start = System.nanoTime();
for (Map.Entry<String, String> entry : map.entrySet()) {
    String val = entry.getValue();
}
long entrySetCost = System.nanoTime() - start;

// keySet: extra get() per key
start = System.nanoTime();
for (String key : map.keySet()) {
    String val = map.get(key);
}
long keySetCost = System.nanoTime() - start;
```

数据量越大，`entrySet()` 相对 `keySet()` 的优势越明显。

## 结论

- 只需要 value，或者需要同时用到 key 和 value：优先用 `entrySet()`
- 只需要 key（不关心 value）：可以用 `keySet()`，此时并不会有额外的 `get()` 调用
- `Hashtable` 的遍历方式与 `HashMap` 相同，结论同样适用

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-04 | 合并 `hashmap遍历.md`（language/ 目录）与 `map-iterator.md`（other/ 目录）两篇重复文章为本文；重写为清晰对比的正文，代码注释改为英文；文件迁移至 `language/java/` 目录，文件名与 url 改为英文 `hashmap-iterator`；保留旧 url 别名 | 两篇文章内容重复（均讲 entrySet vs keySet 遍历性能），且原文包含大量乱码格式的旧代码示例 |
