---
title: java中byte数组与int类型的转换 (两种方式) 
author: "-"
date: 2015-10-12T08:58:05+00:00
url: /?p=8392
categories:
  - Uncategorized

tags:
  - reprint
---
## java中byte数组与int类型的转换 (两种方式)
http://blog.csdn.net/zhouyong0/article/details/8078619

java中byte数组与int类型的转换,在网络编程中这个算法是最基本的算法,我们都知道,在socket传输中,发送、者接收的数据都是 byte数组,但是int类型是4个byte组成的,如何把一个整形int转换成byte数组,同时如何把一个长度为4的byte数组转换为int类型。下面有两种方式。


 

public static byte[] int2byte(int res) {
  
byte[] targets = new byte[4];

targets[0] = (byte) (res & 0xff);// 最低位
  
targets[1] = (byte) ((res >> 8) & 0xff);// 次低位
  
targets[2] = (byte) ((res >> 16) & 0xff);// 次高位
  
targets[3] = (byte) (res >>> 24);// 最高位,无符号右移。
  
return targets;
  
}
  
 

public static int byte2int(byte[] res) {
  
// 一个byte数据左移24位变成0x??000000,再右移8位变成0x00??0000

int targets = (res[0] & 0xff) | ((res[1] << 8) & 0xff00) // | 表示安位或
  
| ((res[2] << 24) >>> 8) | (res[3] << 24);
  
return targets;
  
}
  
第二种

 

public static void main(String[] args) {
  
ByteArrayOutputStream baos = new ByteArrayOutputStream();
  
DataOutputStream dos = new DataOutputStream(baos);
  
try {
  
dos.writeByte(4);
  
dos.writeByte(1);
  
dos.writeByte(1);
  
dos.writeShort(217);
  
} catch (IOException e) {
  
e.printStackTrace();
  
}

byte[] aa = baos.toByteArray();
  
ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
  
DataInputStream dis = new DataInputStream(bais);

try {
  
System.out.println(dis.readByte());
  
System.out.println(dis.readByte());
  
System.out.println(dis.readByte());
  
System.out.println(dis.readShort());
  
} catch (IOException e) {
  
e.printStackTrace();
  
}
  
try {
  
dos.close();
  
dis.close();
  
} catch (IOException e) {
  
e.printStackTrace();
  
}
  
}