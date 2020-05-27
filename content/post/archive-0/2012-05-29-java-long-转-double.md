---
title: java 各种数据类型转换
author: wiloon
type: post
date: 2012-05-29T03:05:36+00:00
url: /?p=3285
categories:
  - Java

---
### String > Double
```java
String str="122.202";
double dnum = Double.parseDouble(str);
```

### hex > int

```bash// 默认hex 大端字节序
int decimal = Integer.parseInt(hexNumber, 16);
```

### list > array>set

```java
Set&lt;T&gt; mySet = new HashSet&lt;&gt;(Arrays.asList(someArray));
```

### array > set, jdk 9+

```java
Set&lt;T&gt; mySet = Set.of(someArray);
```

### array > set, jdk 10+

```java
var mySet = Set.of(someArray);
```

### int > double

```java
Double d = new Double(i)
```

### double > int

```java
int i = d.intValue();
```

### byte to binary string

```java
byte b1 = (byte) 129;
String s1 = String.format("%8s", Integer.toBinaryString(b1 & 0xFF)).replace(' ', '0');
System.out.println(s1); // 10000001
```

### date localdatetime

```java
Instant instant = date.toInstant();
ZoneId zoneId = ZoneId.systemDefault();
instant.atZone(zoneId).toLocalDateTime();
```

### int > bytes

```java
byte[] bytes = ByteBuffer.allocate(4).putInt(i).array();
```

### LocalDateTime > mills

```java 
   public static long localDateTimeToMills(LocalDateTime localDateTime) {
        ZonedDateTime zdt = localDateTime.atZone(ZoneId.systemDefault());
        return zdt.toInstant().toEpochMilli();
    }
```

long   l=10;
  
double   db;
  
String   s;
  
double   db=(double)l;
  
s=String.valueOf(db);

double   d=new   Double(l).doubleValue();

double 转 int

double   d   =   1.23;
  
int   i   =   (int)   d;