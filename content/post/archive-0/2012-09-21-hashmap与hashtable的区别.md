---
title: HashMap,Hashtable
author: wiloon
type: post
date: 2012-09-21T05:24:11+00:00
url: /?p=4144
categories:
  - Java

---
<div>
  HashTable的应用非常广泛，HashMap是新框架中用来代替HashTable的类，也就是说建议使用HashMap，不要使用HashTable。可能你觉得HashTable很好用，为什么不用呢？这里简单分析他们的区别。
</div>

<div id="blog_content">
  <p>
    1.HashTable的方法是同步的，HashMap未经同步，所以在多线程场合要手动同步HashMap这个区别就像Vector和ArrayList一样。2.HashTable不允许null值(key和value都不可以),HashMap允许null值(key和value都可以)。3.HashTable有一个contains(Object value)，功能和containsValue(Object value)功能一样。4.HashTable使用Enumeration，HashMap使用Iterator。以上只是表面的不同，它们的实现也有很大的不同。5.HashTable中hash数组默认大小是11，增加的方式是 old*2+1。HashMap中hash数组的默认大小是16，而且一定是2的指数。
  </p>
  
  <p>
    6.哈希值的使用不同，HashTable直接使用对象的hashCode，代码是这样的：
  </p>
  
  <p>
    [java]
  </p>
  
  <p>
    int hash = key.hashCode();<br /> int index = (hash & 0x7FFFFFFF) % tab.length;<br /> //而HashMap重新计算hash值，而且用与代替求模：<br /> int hash = hash(k);<br /> int i = indexFor(hash, table.length);
  </p>
  
  <p>
    static int hash(Object x) {<br /> int h = x.hashCode();
  </p>
  
  <p>
    h += ~(h << 9);<br /> h ^= (h >>> 14);<br /> h += (h << 4);<br /> h ^= (h >>> 10);<br /> return h;<br /> }<br /> static int indexFor(int h, int length) {<br /> return h & (length-1);<br /> }
  </p>
  
  <p>
    [/java]
  </p>
  
  <p>
    以上只是一些比较突出的区别，当然他们的实现上还是有很多不同的，比如<br /> HashMap对null的操作
  </p>
</div>

<div id="bottoms">
  <p>
    HashMap可以看作三个视图：key的Set，value的Collection，Entry的Set。 这里HashSet就是其实就是HashMap的一个视图。HashSet内部就是使用Hashmap实现的，和Hashmap不同的是它不需要Key和Value两个值。
  </p>
  
  <p>
    往hashset中插入对象其实只不过是内部做了
  </p>
  
  <p>
    public boolean add(Object o) {
  </p>
  
  <p>
    return map.put(o, PRESENT)==null;<br /> }<br /> HashMap为散列映射,它是基于hash table的一个实现,它可在常量时间内安插元素,或找出一组key-value pair.HashSet为散列集,它把查找时间看的很重要,其中所有元素必须要有hashCode()
  </p>
  
  <p>
    <a href="http://oznyang.iteye.com/blog/30690">http://oznyang.iteye.com/blog/30690</a>
  </p>
  
  <p>
    <a href="http://zhaosoft.iteye.com/blog/243587">http://zhaosoft.iteye.com/blog/243587</a>
  </p>
  
  <blockquote data-secret="NbrQHz1OQo" class="wp-embedded-content">
    <p>
      <a href="http://coolshell.cn/articles/9606.html">疫苗：Java HashMap的死循环</a>
    </p>
  </blockquote>
  
  <p>
    <iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://coolshell.cn/articles/9606.html/embed#?secret=NbrQHz1OQo" data-secret="NbrQHz1OQo" width="600" height="338" title="《疫苗：Java HashMap的死循环》—酷 壳 - CoolShell" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>
  </p>
</div>