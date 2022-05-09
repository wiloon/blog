---
title: JUnit中按照顺序执行测试
author: "-"
date: 2016-01-27T06:34:42+00:00
url: /?p=8714
categories:
  - Inbox
tags:
  - reprint
---
## JUnit中按照顺序执行测试
@FixMethodOrder(MethodSorters.NAME_ASCENDING)

MethodSorters.NAME_ASCENDING  (推荐) 
  
按方法名称的进行排序,由于是按字符的字典顺序,所以以这种方式指定执行顺序会始终保持一致；
  
不过这种方式需要对测试方法有一定的命名规则,如 测试方法均以testNNN开头 (NNN表示测试方法序列号 001-999) 

JUnit中按照顺序执行测试方式
  
很多情况下,写了一堆的test case,希望某一些test case必须在某个test case之后执行。比如,测试某一个Dao代码,希望添加的case在最前面,然后是修改或者查询,最后才是删除,以前的做法把所有的方法都集中到某一个方法去执行,一个个罗列好,比较麻烦。比较幸福的事情就是JUnit4.11之后提供了MethodSorters,可以有三种方式对test执行顺序进行指定,如下: 
  
/**
  
* Sorts the test methods by the method name, in lexicographic order, with {@link Method#toString()} used as a tiebreaker
  
*/
  
NAME_ASCENDING(MethodSorter.NAME_ASCENDING),

/**
  
* Leaves the test methods in the order returned by the JVM. Note that the order from the JVM may vary from run to run
  
*/
  
JVM(null),

/**
  
* Sorts the test methods in a deterministic, but not predictable, order
  
*/
  
DEFAULT(MethodSorter.DEFAULT);

可以小试牛刀一下: 

使用DEFAULT方式: 
  
package com.netease.test.junit;

import org.apache.log4j.Logger;
  
import org.junit.FixMethodOrder;
  
import org.junit.Test;
  
import org.junit.runners.MethodSorters;

/**
  
* User: hzwangxx
  
* Date: 14-3-31
  
* Time: 15:35
  
*/
  
@FixMethodOrder(MethodSorters.DEFAULT)
  
public class TestOrder {
  
private static final Logger LOG = Logger.getLogger(TestOrder.class);
  
@Test
  
public void testFirst() throws Exception {
  
LOG.info("——1——–");
  
}

@Test
  
public void testSecond() throws Exception {
  
LOG.info("——2——–");

}

@Test
  
public void testThird() throws Exception {
  
LOG.info("——3——–");
  
}

}
  
/*
  
output:
  
2014-03-31 16:04:15,984 0 [main] INFO – ——1——–
  
2014-03-31 16:04:15,986 2 [main] INFO – ——3——–
  
2014-03-31 16:04:15,987 3 [main] INFO – ——2——–
  
*/

换成按字母排序
  
package com.netease.test.junit;

import org.apache.log4j.Logger;
  
import org.junit.FixMethodOrder;
  
import org.junit.Test;
  
import org.junit.runners.MethodSorters;

/**
  
* User: hzwangxx
  
* Date: 14-3-31
  
* Time: 15:35
  
*/
  
@FixMethodOrder(MethodSorters.NAME_ASCENDING)
  
public class TestOrder {
  
private static final Logger LOG = Logger.getLogger(TestOrder.class);
  
@Test
  
public void testFirst() throws Exception {
  
LOG.info("——1——–");
  
}

@Test
  
public void testSecond() throws Exception {
  
LOG.info("——2——–");

}

@Test
  
public void testThird() throws Exception {
  
LOG.info("——3——–");
  
}

}
  
/*
  
2014-03-31 16:10:25,360 0 [main] INFO – ——1——–
  
2014-03-31 16:10:25,361 1 [main] INFO – ——2——–
  
2014-03-31 16:10:25,362 2 [main] INFO – ——3——–
  
*/