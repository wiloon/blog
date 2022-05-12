---
title: SuperCSV
author: "-"
date: 2012-08-28T02:31:24+00:00
url: /?p=3956
categories:
  - Java
tags:$
  - reprint
---
## SuperCSV



  Super CSV是一个速度奇快、免费跨平台的 CVS 格式数据的读写库，可以方便的处理对象、Map、列表的读写操作，以及自动化的类型转换和数据检查功能。

  ```java
 InputStreamReader freader = new InputStreamReader(new FileInputStream(
 new File("csv/test1.csv")), "GB2312"); 
  
    ICsvBeanReader reader = new CsvBeanReader(freader,
 CsvPreference.EXCEL_PREFERENCE);
  
  
    //获取头部信息
 String[] headers = reader.getCSVHeader(true);
  
  
    //获取数据部分
 UserBean bean = null;
 while ((bean = reader.read(UserBean.class, headers, UserBean.readProcessors)) != null) {
 System.out.print(bean.getName() + "t");
 System.out.print(bean.getAge() + "t");
 System.out.print(bean.getBirthday() + "t");
 System.out.println(bean.getAddress());
 }
 ```
  
  
    java csv: 
    
    
      
        Commons CSV (Sandbox)
      
      
        Skife CSV
      
      
        opencsv
      
      
        GenJava-CSV
      
      
        Super Csv
      
      
        JavaCSV
      
      
        CSVBeans
      
    