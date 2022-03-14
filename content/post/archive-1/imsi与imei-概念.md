---
title: IMSI, IMEI
author: "-"
date: 2015-08-05T08:47:25+00:00
url: /?p=8062
categories:
  - Uncategorized

tags:
  - reprint
---
## IMSI, IMEI
http://cuisuqiang.iteye.com/blog/2067254


IMSI与IMEI 概念
  
博客分类: 理论知识
  
IMSIIMEI网络码运营商MNC
  
IMSI是相对手机卡而言的
  
国际移动用户识别码 (IMSI: International Mobile Subscriber Identification Number) 


IMSI共有15位，其结构如下
  
MCC+MNC+MSIN
  
MCC: Mobile Country Code，移动国家码，MCC的资源由国际电联 (ITU) 统一分配和管理，唯一识别移动用户所属的国家，共3位，中国为460;
  
MNC:Mobile Network Code，移动网络码，2~3位，中国移动系统使用00、02、07，中国联通GSM系统使用01、06，中国电信CDMA系统使用03、05，中国铁通系统使用20。
  
MSIN:Mobile Subscriber Identification Number, 移动用户识别号码,共有10位，其结构如下: 
  
EF+M0M1M2M3+ABCD
  
其中的M0M1M2M3和MDN号码中的H0H1H2H3可存在对应关系，ABCD四位为自由分配。
  
可以看出IMSI在NMSI号码前加了MCC，可以区别出每个用户的来自的国家，因此可以实现国际漫游。在同一个国家内，如果有多个移动网络运营商，可以通过MNC来进行区别.
  
IMSI与手机号码绑定关系，在网络侧网元HLR (Home Location Register)内定义。

作用
  
当你的手机开机后在接入网络的过程中有一个注册登记的过程，系统通过控制信道将经加密算法后的参数组传送给客户，手机中的SIM卡收到参数后，与SIM卡存储的客户鉴权参数经同样算法后对比，结果相同就允许接入，否则为非法客户，网络拒绝为此客户服务。


手机对应的是IMEI
  
IMEI (International Mobile Equipment Identity) 是移动设备国际身份码的缩写，移动装备国际辨识码，是由15位数字组成的"电子串号"，它与每台手机一一对应，而且该码是全世界唯一的。每一部手机在组装完成后都将被赋予一个全球唯一的一组号码，这个号码从生产到交付使用都将被制造生产的厂商所记录。

IMEI由15位数字组成，其组成为
  
1. 前6位数 (TAC，Type ApprovalCode)是"型号核准号码"，一般代表机型。
  
2. 接着的2位数 (FAC，Final Assembly Code)是"最后装配号"，一般代表产地。
  
3. 之后的6位数 (SNR)是"串号"，一般代表生产顺序号。
  
4. 最后1位数 (SP)通常是"0"，为检验码，备用。
  
IMEI码具有唯一性，贴在手机背面的标志上，并且读写于手机内存中。它也是该手机在厂家的"档案"和"身份证号"。

作用
  
它与每台手机一一对应，而且该码是全世界唯一的。每一只手机在组装完成后都将被赋予一个全球唯一的一组号码，这个号码从生产到交付使用都将被制造生产的厂商所记录。
  
当手机被盗的时候，如知道IMEI码，可以通过手机供应商进行手机锁定，即: 获知被盗之后的手机号码，中止手机的通话功能，获知手机的方位。


代码里，怎么知道手机是那个通信商的

Java代码
  
public class Test {
  
public static void main(String[] args) {
  
String imsi = "460030912121001";
  
if("46002,46000,46007".contains(imsi.subSequence(0,5))){
  
System.out.println("移动用户");
  
}else if("46001,46006".contains(imsi.subSequence(0,5))){
  
System.out.println("联通用户");
  
}else if("46003,46005".contains(imsi.subSequence(0,5))){
  
System.out.println("电信用户");
  
}else if("46020".contains(imsi.subSequence(0,5))){
  
System.out.println("铁通用户");
  
}else{
  
System.out.println("非法用户");
  
}
  
}
  
}

至于在手机上怎么获得IMSI，那是个技术活了，不懂Android开发，暂不发言！


请您到ITEYE看我的原创: http://cuisuqiang.iteye.com

或支持我的个人博客，地址: http://www.javacui.com