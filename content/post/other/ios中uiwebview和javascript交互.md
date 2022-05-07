---
title: Java Object Layout(jol)
author: "-"
date: 2015-05-21T05:59:42+00:00
url: /?p=7701
categories:
  - Inbox
tags:
  - reprint
---
## Java Object Layout(jol)
http://bboniao.com/openjdk/2014-06/java-object-layoutjol.htm
  
http://openjdk.java.net/projects/code-tools/jol/

hg clone http://hg.openjdk.java.net/code-tools/jol/ jol
  
cd jol
  
mvn clean install
  
pom.xml添加依赖

<dependency>
      
<groupId>org.openjdk.jol</groupId>
      
<artifactId>jol-core</artifactId>
      
<version>1.0-SNAPSHOT</version>
  
</dependency>
  
代码

public static void main(String[] args) {
          
int size = 10;
          
List<Integer> list = new ArrayList<Integer>(size);
          
for (int i = 0; i < size; i++) {
              
list.add(i);
          
}
          
//虚拟机信息
          
out.println(VMSupport.vmDetails());
          
//打印类内部的占用
          
out.println(ClassLayout.parseClass(ArrayList.class).toPrintable());
          
//打印实例内部的占用
          
out.println(ClassLayout.parseClass(ArrayList.class).toPrintable(list));
          
//打印实例外部的占用
          
out.println(GraphLayout.parseInstance(list).toPrintable());
          
//打印实例各个依赖的占用,并汇总
          
out.println(GraphLayout.parseInstance(list).toFootprint());
      
}
  
输出

Running 64-bit HotSpot VM.
  
Using compressed references with 3-bit shift.
  
Objects are 8 bytes aligned.
  
Field sizes by type: 4, 1, 1, 2, 2, 4, 4, 8, 8 [bytes]
  
Array element sizes: 4, 1, 1, 2, 2, 4, 4, 8, 8 [bytes]

java.util.ArrayList object internals:
   
OFFSET SIZE TYPE DESCRIPTION VALUE
        
0 12 (object header) N/A
       
12 4 int AbstractList.modCount N/A
       
16 4 int ArrayList.size N/A
       
20 4 Object[] ArrayList.elementData N/A
  
Instance size: 24 bytes (estimated, the sample instance is not available)
  
Space losses: 0 bytes internal + 0 bytes external = 0 bytes total

java.util.ArrayList object internals:
   
OFFSET SIZE TYPE DESCRIPTION VALUE
        
0 4 (object header) 19 00 00 00 (0001 1001 0000 0000 0000 0000 0000 0000)
        
4 4 (object header) 00 00 00 00 (0000 0000 0000 0000 0000 0000 0000 0000)
        
8 4 (object header) 31 32 00 f8 (0011 0001 0011 0010 0000 0000 1111 1000)
       
12 4 int AbstractList.modCount 10
       
16 4 int ArrayList.size 10
       
20 4 Object[] ArrayList.elementData [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  
Instance size: 24 bytes (estimated, add this JAR via -javaagent: to get accurate result)
  
Space losses: 0 bytes internal + 0 bytes external = 0 bytes total

java.util.ArrayList object externals:
            
ADDRESS SIZE TYPE PATH VALUE
          
74002ca98 16 java.lang.Integer .elementData[9] 9
          
74002caa8 16 java.lang.Integer .elementData[8] 8
          
74002cab8 16 java.lang.Integer .elementData[7] 7
          
74002cac8 16 java.lang.Integer .elementData[6] 6
          
74002cad8 16 java.lang.Integer .elementData[5] 5
          
74002cae8 16 java.lang.Integer .elementData[4] 4
          
74002caf8 16 java.lang.Integer .elementData[3] 3
          
74002cb08 16 java.lang.Integer .elementData[2] 2
          
74002cb18 16 java.lang.Integer .elementData[1] 1
          
74002cb28 16 java.lang.Integer .elementData[0] 0
          
74002cb38 491560 (something else) (somewhere else) (something else)
          
7400a4b60 56 [Ljava.lang.Object; .elementData [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
          
7400a4b98 1432458504 (something else) (somewhere else) (something else)
          
7956be0a0 24 java.util.ArrayList (object)

java.util.ArrayList instance footprint:
   
COUNT AVG SUM DESCRIPTION
       
1 56 56 [Ljava.lang.Object;
      
10 16 160 java.lang.Integer
       
1 24 24 java.util.ArrayList
      
12 240 (total)