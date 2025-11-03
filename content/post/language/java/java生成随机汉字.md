---
title: JAVA生成随机汉字
author: "-"
date: 2013-11-17T09:53:42+00:00
url: /?p=5981
categories:
  - Inbox
tags:
  - Java

---
## JAVA生成随机汉字
[http://blog.csdn.net/smilememory/article/details/8053599](http://blog.csdn.net/smilememory/article/details/8053599)

首先我们得知道汉字编码的原理。
  
在国标GB2312-80中规定，所有的国标汉字及符号分配在一个94行、94列的方阵中，方阵的每一行称为一个"区"，编号为01区到94区，每一列称为一个"位"，编号为01位到94位，方阵中的每一个汉字和符号所在的区号和位号组合在一起形成的四个阿拉伯数字就是它们的"区位码"。区位码的前两位是它的区号，后两位是它的位号。用区位码就可以唯一地确定一个汉字或符号，反过来说，任何一个汉字或符号也都对应着一个唯一的区位码。例如，汉字"辉"字的区位码是2752，表明它在方阵的27区52位。
  
所有的汉字和符号所在的区分为一下4个组。
  
 (1) 01区到15区
  
图形符号区，其中01区到09区为标准符号区，10区到15区为自定义符号区。
  
 (2) 16区到55区
  
一级常用汉字区，包括了3755个一级汉字。这40个区中的汉字是按汉语拼音排序的，同音字按笔画顺序。其中55区的90~94位未定义汉字。
  
 (3) 56区到87区
  
二级汉字区，包括了3008个二级汉字，按部首排序。
  
 (4) 88区到94区
  
自定义汉字区
  
其中，第10区到15区的自定义符号区和第88区到第94区的自定义汉字区可由用户自定义国标码中未定义的符号和汉字。
  
与汉字的区位码类似的还有汉字机内码，汉字机内码是在汉字的区码和位码上分别加上A0H (这里的Ｈ表示前两位数字为十六进制数) 而得到的。使用机内码表示的一个汉字占用两个字节，分别称为高位节和低位节，这两位字节的机内码按以下规则表示。
  
高位字节＝区码+20H+80H(或区码+A0H)
  
地位字节＝位码+20H+80H(或位码+A0H)
  
例如，汉字"啊"的区位码为1601， 区码和位码分别用十六进制表示即为1001H，它的机内码的高位字节为B0H，地位字节为A1H， 机内码就是B0A1H。

注意: 汉字的机内码都从第十六区B0开始，并且从区位D7开始以后的汉字都是很难见到的复杂汉字，可以将这些汉字排除掉。所以随机生成的汉字机内码的第一位范围在B C D 之间， 如果第 1 为 是D， 则第二位区位码就不能是7以后的十六进制数。由于每个区的第一个位置和最后一个位置是空的，没有汉字，因此随机生成的区位码的第 3 为如果是A， 第4位就不能是0；第三位如果是F，第四位就不能是F。
  
(以上来自《java web 程序开发范例宝典》明日科技 王国辉  陈丹丹 潘凯华编著 人民邮电出版社)

获得随机汉字的java代码
  
//获得随机的汉字
  
private String getRandomChinese(){
  
Random random = new Random();
  
int code1,code2,code3,code4;//分别代表四个位码
  
String checkCode = "";
  
String[] rBase = {"0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"};

code1 = random.nextInt(3) +11;
  
String str_r1 = rBase[code1];//获得第一个位码

if(code1 == 13) {
  
code2 = random.nextInt(7);
  
}
  
else {
  
code2 = random.nextInt(16);
  
}
  
String str_r2 = rBase[code2];//第二个位码

code3 = random.nextInt(6) + 10;
  
String str_r3 = rBase[code3];//第三个位码

if(code3 == 10) {
  
code4 = random.nextInt(15) + 1;
  
}
  
else if(code3 ==15) {
  
code4 = random.nextInt(15);
  
}
  
else {
  
code4 = random.nextInt(16);
  
}
  
String str_r4 = rBase[code4];//第四个位码

byte[] bytes = new byte[2];
  
String str_r12 = str_r1 + str_r2;
  
int tempLow = Integer.parseInt(str_r12, 16);
  
bytes[0] = (byte) tempLow;//低位字节

String str_r34 = str_r3 + str_r4;
  
int tempHigh = Integer.parseInt(str_r34, 16);
  
bytes[1] = (byte) tempHigh;//高位字节

checkCode = new String(bytes);//生成汉字
  
return checkCode;
  
}