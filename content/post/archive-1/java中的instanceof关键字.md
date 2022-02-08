---
title: Java中的instanceof关键字
author: "-"
date: 2012-10-31T06:26:36+00:00
url: /?p=4585
categories:
  - Development
  - Java

tags:
  - reprint
---
## Java中的instanceof关键字
# 


  instanceof是Java的一个二元操作符，和==，>，<是同一类东西。由于它是由字母组成的，所以也是Java的保留关键字。它的作用是测试它左边的对象是否是它右边的类的实例，返回boolean类型的数据。举个例子: String s = "I AM an Object!";
 boolean isObject = s instanceof Object; 
  
    我们声明了一个String对象引用，指向一个String对象，然后用instancof来测试它所指向的对象是否是Object类的一个实例，显然，这是真的，所以返回true，也就是isObject的值为True。
 instanceof有一些用处。比如我们写了一个处理账单的系统，其中有这样三个类: 
  
  
    public class Bill {//省略细节}
 public class PhoneBill extends Bill {//省略细节}
 public class GasBill extends Bill {//省略细节}
  
  
    在处理程序里有一个方法，接受一个Bill类型的对象，计算金额。假设两种账单计算方法不同，而传入的Bill对象可能是两种中的任何一种，所以要用instanceof来判断: 
  
  
    public double calculate(Bill bill) {
 if (bill instanceof PhoneBill) {
 //计算电话账单
 }
 if (bill instanceof GasBill) {
 //计算燃气账单
 }
 ...
 }
 这样就可以用一个方法处理两种子类。
  
  
    然而，这种做法通常被认为是没有好好利用面向对象中的多态性。其实上面的功能要求用方法重载完全可以实现，这是面向对象变成应有的做法，避免回到结构化编程模式。只要提供两个名字和返回值都相同，接受参数类型不同的方法就可以了: 
  
  
    public double calculate(PhoneBill bill) {
 //计算电话账单
 }
  
  
    public double calculate(GasBill bill) {
 //计算燃气账单
 }
  
  
    所以，使用instanceof在绝大多数情况下并不是推荐的做法，应当好好利用多态。
  
