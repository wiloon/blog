---
title: java 各种数据类型转换
author: "-"
date: 2012-05-29T03:05:36+00:00
url: java/convert
categories:
  - Java
tags:$
  - reprint
---
## java 各种数据类型转换
### String > Double
```java
String str="122.202";
double dnum = Double.parseDouble(str);
```

### hex > int

```bash
// 默认hex 大端字节序
int decimal = Integer.parseInt(hexNumber, 16);
```

### list > array>set

```java
Set<T> mySet = new HashSet<>(Arrays.asList(someArray));
```

### array > set, java 9+
```java
Set<T> mySet = Set.of(someArray);
```

### array > set, java 10+

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

```java
    public static byte[] int2Bytes(int value) {
        byte[] out = new byte[4];
        for (int i = 0; i < 4; i++) {
            out[i] = (byte) (value >> (8 * (4 - i - 1)));
        }
        return out;
    }

    public static int bytes2Int(byte[] value) {
        int out = 0;
        if (value != null && value.length == 4) {
            for (int i = 0; i < 4; i++) {
                out |= (value[i] & 0xFF) << (8 * (4 - i - 1));
            }
        }
        return out;
    }
```

### value & 0xFF
It sets result to the (unsigned) value resulting from putting the 8 bits of value in the lowest 8 bits of result.

The reason something like this is necessary is that byte is a signed type in Java. If you just wrote:

int result = value;
then result would end up with the value ff ff ff fe instead of 00 00 00 fe. A further subtlety is that the & is defined to operate only on int values1, so what happens is:

value is promoted to an int (ff ff ff fe).
0xff is an int literal (00 00 00 ff).
The & is applied to yield the desired value for result.
(The point is that conversion to int happens before the & operator is applied.)

1Well, not quite. The & operator works on long values as well, if either operand is a long. But not on byte. See the Java Language Specification, sections 15.22.1 and 5.6.2.

### LocalDateTime > mills

```java 
   public static long localDateTimeToMills(LocalDateTime localDateTime) {
        ZonedDateTime zdt = localDateTime.atZone(ZoneId.systemDefault());
        return zdt.toInstant().toEpochMilli();
    }
```

### LocalDateTime > Instant
```java
    LocalDate date = LocalDate.now();
    Instant instant = date.atStartOfDay(ZoneId.systemDefault()).toInstant();
```
### string > LocalDateTime
```java
LocalDateTime.parse("2022-01-05 15:16", DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"))
```
### string > Instant
```java
    LocalDateTime.parse(                   // Parse as an indeterminate `LocalDate`, devoid of time zone or offset-from-UTC. NOT a moment, NOT a point on the timeline.
        "04:30 PM, Sat 5/12/2018" ,        // This input uses a poor choice of format. Whenever possible, use standard ISO 8601 formats when exchanging date-time values as text. Conveniently, the java.time classes use the standard formats by default when parsing/generating strings.
        DateTimeFormatter.ofPattern( "hh:mm a, EEE M/d/uuuu" , Locale.US )  // Use single-character `M` & `d` when the number lacks a leading padded zero for single-digit values.
    )                                      // Returns a `LocalDateTime` object.
    .atZone(                               // Apply a zone to that unzoned `LocalDateTime`, giving it meaning, determining a point on the timeline.
        ZoneId.of( "America/Toronto" )     // Always specify a proper time zone with `Contintent/Region` format, never a 3-4 letter pseudo-zone such as `PST`, `CST`, or `IST`. 
    )                                      // Returns a `ZonedDateTime`. `toString` → 2018-05-12T16:30-04:00[America/Toronto].
    .toInstant()                           // Extract a `Instant` object, always in UTC by definition.   
```

### LocalDateTime > String
```java
// Get current date time
LocalDateTime currentDateTime = LocalDateTime.now();
// Inbuilt format
static DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE_TIME;
// Custom format
//DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
// Format LocalDateTime
String formattedDateTime = currentDateTime.format(formatter);
//Verify
System.out.println("Formatted LocalDateTime : " + formattedDateTime);       
//Output:
//Formatted LocalDateTime : 2018-07-14T17:45:55.9483536
```


### array > list
```java
List list = Arrays.asList(strArray);

        private void testArrayCastToListError() {
                String[] strArray = new String[2];
                List list = Arrays.asList(strArray);
                //对转换后的list插入一条数据
                list.add("1");
                System.out.println(list);
            }
ArrayList<String> list = new ArrayList<String>(Arrays.asList(strArray)) ;

        private void testArrayCastToListRight() {
                String[] strArray = new String[2];
                ArrayList<String> list = new ArrayList<String>(Arrays.asList(strArray)) ;
                list.add("1");
                System.out.println(list);
            }

```
### list > array
```java
ArrayList.toArray
```


#### Collections.addAll()方法(最高效)

private void testArrayCastToListEfficient(){
        String[] strArray = new String[2];
        ArrayList< String> arrayList = new ArrayList<String>(strArray.length);
        Collections.addAll(arrayList, strArray);
        arrayList.add("1");
        System.out.println(arrayList);
    }

### Instant > Date
```java
Instant foo = Instant.now()
Date.from(foo)
```

---

https://blog.csdn.net/x541211190/article/details/79597236
https://howtodoinjava.com/java/date-time/format-localdatetime-to-string/
>https://javadeveloperzone.com/java-basic/java-convert-int-to-byte-array/