---
title: java 各种数据类型转换
author: wiloon
type: post
date: 2012-05-29T03:05:36+00:00
url: /?p=3285
categories:
  - Java

---
### hex > int

<pre><code class="language-bash line-numbers">// 默认hex 大端字节序
int decimal = Integer.parseInt(hexNumber, 16);
</code></pre>

### list > array>set

<pre><code class="language-java line-numbers">Set&lt;T&gt; mySet = new HashSet&lt;&gt;(Arrays.asList(someArray));
</code></pre>

### array > set, jdk 9+

<pre><code class="language-java line-numbers">Set&lt;T&gt; mySet = Set.of(someArray);
</code></pre>

### array > set, jdk 10+

<pre><code class="language-java line-numbers">var mySet = Set.of(someArray);
</code></pre>

### int > double

<pre><code class="language-java line-numbers">Double d = new Double(i)
</code></pre>

### double > int

<pre><code class="language-java line-numbers">int i = d.intValue();
</code></pre>

### byte to binary string

<pre><code class="language-java line-numbers">byte b1 = (byte) 129;
String s1 = String.format("%8s", Integer.toBinaryString(b1 & 0xFF)).replace(' ', '0');
System.out.println(s1); // 10000001
</code></pre>

### date localdatetime

<pre><code class="language-java line-numbers">Instant instant = date.toInstant();
ZoneId zoneId = ZoneId.systemDefault();
instant.atZone(zoneId).toLocalDateTime();
</code></pre>

### int > bytes

<pre><code class="language-java line-numbers">byte[] bytes = ByteBuffer.allocate(4).putInt(i).array();
</code></pre>

### LocalDateTime > mills

<pre><code class="language-java line-numbers">    public static long localDateTimeToMills(LocalDateTime localDateTime) {
        ZonedDateTime zdt = localDateTime.atZone(ZoneId.systemDefault());
        return zdt.toInstant().toEpochMilli();
    }
</code></pre>

long   l=10;
  
double   db;
  
String   s;
  
double   db=(double)l;
  
s=String.valueOf(db);

double   d=new   Double(l).doubleValue();

double 转 int

double   d   =   1.23;
  
int   i   =   (int)   d;