---
title: HashMap遍历的两种方式
author: "-"
date: 2021-03-17 09:53:33
draft: true
url: /?p=3833
categories:
  - Uncategorized

tags:
  - reprint
---
## HashMap遍历的两种方式
### 第一种:
```java
 Map map = new HashMap();
 Iterator iter = map.entrySet().iterator();
 while (iter.hasNext()) {
 Map.Entry entry = (Map.Entry) iter.next();
 Object key = entry.getKey();
 Object val = entry.getValue();
 }
 ```
 效率高,以后一定要使用此种方式！
 第二种:
 ```java
 Map map = new HashMap();
 Iterator iter = map.keySet().iterator();
 while (iter.hasNext()) {
 Object key = iter.next();
 Object val = map.get(key);
 }
 ```
 效率低,以后尽量少使用！例: 
 HashMap的遍历有两种常用的方法，那就是使用keyset及entryset来进行遍历，但两者的遍历速度是有差别的，下面请看实例:  
  
    public class HashMapTest {
 public static void main(String[] args) ...{
 HashMap hashmap = new HashMap();
 for (int i = 0; i < 1000; i ) ...{
 hashmap.put("" i, "thanks");
 }
  
  
    long bs = Calendar.getInstance().getTimeInMillis();
 Iterator iterator = hashmap.keySet().iterator();
 while (iterator.hasNext()) ...{
 System.out.print(hashmap.get(iterator.next()));
 }
 System.out.println();
 System.out.println(Calendar.getInstance().getTimeInMillis() - bs);
 listHashMap();
 }
  
  
    public static void listHashMap() ...{
 java.util.HashMap hashmap = new java.util.HashMap();
 for (int i = 0; i < 1000; i ) ...{
 hashmap.put("" i, "thanks");
 }
 long bs = Calendar.getInstance().getTimeInMillis();
 java.util.Iterator it = hashmap.entrySet().iterator();
 while (it.hasNext()) ...{
 java.util.Map.Entry entry = (java.util.Map.Entry) it.next();
 // entry.getKey() 返回与此项对应的键
 // entry.getValue() 返回与此项对应的值
 System.out.print(entry.getValue());
 }
 System.out.println();
 System.out.println(Calendar.getInstance().getTimeInMillis() - bs);
 }
 }
  
  
    对于keySet其实是遍历了2次，一次是转为iterator，一次就从hashmap中取出key所对于的value。而entryset只是遍历了第一次，他把key和value都放到了entry中，所以就快了。
  
