---
title: 'java 读文件到Byte[]数组'
author: "-"
date: 2016-03-17T09:23:41+00:00
url: /?p=8806
categories:
  - Inbox
tags:
  - reprint
---
## 'java 读文件到Byte[]数组'
http://blog.sina.com.cn/s/blog_ae48aad6010177ns.html

```java
public class Test {  
   public static void main(String[] args){  
       String filePath = "E:\\softoon\\workspace_softoon\\TestMobile\\src\\1.docx";  
       String outFilePath = "E:\\softoon\\workspace_softoon\\TestMobile\\src";  
       String outFileName = "2.docx";  

       getFile(getBytes(filePath),outFilePath,outFileName);  
   }  

   //获得指定文件的byte数组 
   public static byte[] getBytes(String filePath){  
       byte[] buffer = null;  
       try {  
           File file = new File(filePath);  
           FileInputStream fis = new FileInputStream(file);  
           ByteArrayOutputStream bos = new ByteArrayOutputStream(1000);  
           byte[] b = new byte[1000];  
           int n;  
           while ((n = fis.read(b)) != -1) {  
               bos.write(b, 0, n);  
           }  
           fis.close();  
           bos.close();  
           buffer = bos.toByteArray();  
       } catch (FileNotFoundException e) {  
           e.printStackTrace();  
       } catch (IOException e) {  
           e.printStackTrace();  
       }  
       return buffer;  
   }  

   //根据byte数组,生成文件 
   public static void getFile(byte[] bfile, String filePath,String fileName) {  
       BufferedOutputStream bos = null;  
       FileOutputStream fos = null;  
       File file = null;  
       try {  
           File dir = new File(filePath);  
           if(!dir.exists()&&dir.isDirectory()){//判断文件目录是否存在  
               dir.mkdirs();  
           }  
           file = new File(filePath+"\\"+fileName);  
           fos = new FileOutputStream(file);  
           bos = new BufferedOutputStream(fos);  
           bos.write(bfile);  
       } catch (Exception e) {  
           e.printStackTrace();  
       } finally {  
           if (bos != null) {  
               try {  
                   bos.close();  
               } catch (IOException e1) {  
                  e1.printStackTrace();  
               }  
           }  
           if (fos != null) {  
               try {  
                   fos.close();  
               } catch (IOException e1) {  
                   e1.printStackTrace();  
               }  
           }  
       }  
   } 
}
```