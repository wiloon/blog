---
title: Java 压缩字符串
author: "-"
date: 2019-02-09T15:17:20+00:00
url: /?p=13563
categories:
  - Uncategorized

tags:
  - reprint
---
## Java 压缩字符串
https://www.cnblogs.com/EasonJim/p/8256906.html

说明: 

1. 一般来说要实现压缩,那么返回方式一般是用byte[]数组。
2. 研究发现byte[]数组在转成可读的String时,大小会还原回原来的。
3. 如果采用压缩之后不可读的String时,互相转换大小会变小,唯一缺点就是转出的String不可读,需要再次解码之后才可读。
4. 对于压缩一般最近常听的应该就是gzip这些。

实现一: 

复制代码
  
/***
    
* 压缩GZip
    
*
    
* @param data
    
* @return
    
*/
   
public static byte[] gZip(byte[] data) {
    
byte[] b = null;
    
try {
     
ByteArrayOutputStream bos = new ByteArrayOutputStream();
     
GZIPOutputStream gzip = new GZIPOutputStream(bos);
     
gzip.write(data);
     
gzip.finish();
     
gzip.close();
     
b = bos.toByteArray();
     
bos.close();
    
} catch (Exception ex) {
     
ex.printStackTrace();
    
}
    
return b;
   
}

/***
    
* 解压GZip
    
*
    
* @param data
    
* @return
    
*/
   
public static byte[] unGZip(byte[] data) {
    
byte[] b = null;
    
try {
     
ByteArrayInputStream bis = new ByteArrayInputStream(data);
     
GZIPInputStream gzip = new GZIPInputStream(bis);
     
byte[] buf = new byte[1024];
     
int num = -1;
     
ByteArrayOutputStream baos = new ByteArrayOutputStream();
     
while ((num = gzip.read(buf, 0, buf.length)) != -1) {
      
baos.write(buf, 0, num);
     
}
     
b = baos.toByteArray();
     
baos.flush();
     
baos.close();
     
gzip.close();
     
bis.close();
    
} catch (Exception ex) {
     
ex.printStackTrace();
    
}
    
return b;
   
}

/***
    
* 压缩Zip
    
*
    
* @param data
    
* @return
    
*/
   
public static byte[] zip(byte[] data) {
    
byte[] b = null;
    
try {
     
ByteArrayOutputStream bos = new ByteArrayOutputStream();
     
ZipOutputStream zip = new ZipOutputStream(bos);
     
ZipEntry entry = new ZipEntry("zip");
     
entry.setSize(data.length);
     
zip.putNextEntry(entry);
     
zip.write(data);
     
zip.closeEntry();
     
zip.close();
     
b = bos.toByteArray();
     
bos.close();
    
} catch (Exception ex) {
     
ex.printStackTrace();
    
}
    
return b;
   
}

/***
    
* 解压Zip
    
*
    
* @param data
    
* @return
    
*/
   
public static byte[] unZip(byte[] data) {
    
byte[] b = null;
    
try {
     
ByteArrayInputStream bis = new ByteArrayInputStream(data);
     
ZipInputStream zip = new ZipInputStream(bis);
     
while (zip.getNextEntry() != null) {
      
byte[] buf = new byte[1024];
      
int num = -1;
      
ByteArrayOutputStream baos = new ByteArrayOutputStream();
      
while ((num = zip.read(buf, 0, buf.length)) != -1) {
       
baos.write(buf, 0, num);
      
}
      
b = baos.toByteArray();
      
baos.flush();
      
baos.close();
     
}
     
zip.close();
     
bis.close();
    
} catch (Exception ex) {
     
ex.printStackTrace();
    
}
    
return b;
   
}

/***
    
* 压缩BZip2
    
*
    
* @param data
    
* @return
    
*/
   
public static byte[] bZip2(byte[] data) {
    
byte[] b = null;
    
try {
     
ByteArrayOutputStream bos = new ByteArrayOutputStream();
     
CBZip2OutputStream bzip2 = new CBZip2OutputStream(bos);
     
bzip2.write(data);
     
bzip2.flush();
     
bzip2.close();
     
b = bos.toByteArray();
     
bos.close();
    
} catch (Exception ex) {
     
ex.printStackTrace();
    
}
    
return b;
   
}

/***
    
* 解压BZip2
    
*
    
* @param data
    
* @return
    
*/
   
public static byte[] unBZip2(byte[] data) {
    
byte[] b = null;
    
try {
     
ByteArrayInputStream bis = new ByteArrayInputStream(data);
     
CBZip2InputStream bzip2 = new CBZip2InputStream(bis);
     
byte[] buf = new byte[1024];
     
int num = -1;
     
ByteArrayOutputStream baos = new ByteArrayOutputStream();
     
while ((num = bzip2.read(buf, 0, buf.length)) != -1) {
      
baos.write(buf, 0, num);
     
}
     
b = baos.toByteArray();
     
baos.flush();
     
baos.close();
     
bzip2.close();
     
bis.close();
    
} catch (Exception ex) {
     
ex.printStackTrace();
    
}
    
return b;
   
}

/**
    
* 把字节数组转换成16进制字符串
    
*
    
* @param bArray
    
* @return
    
*/
   
public static String bytesToHexString(byte[] bArray) {
    
StringBuffer sb = new StringBuffer(bArray.length);
    
String sTemp;
    
for (int i = 0; i < bArray.length; i++) {
     
sTemp = Integer.toHexString(0xFF & bArray[i]);
     
if (sTemp.length() < 2)
      
sb.append(0);
     
sb.append(sTemp.toUpperCase());
    
}
    
return sb.toString();
   
}

/**
    
*jzlib 压缩数据
    
*
    
* @param object
    
* @return
    
* @throws IOException
    
*/
   
public static byte[] jzlib(byte[] object) {
    
byte[] data = null;
    
try {
     
ByteArrayOutputStream out = new ByteArrayOutputStream();
     
ZOutputStream zOut = new ZOutputStream(out,
       
JZlib.Z_DEFAULT_COMPRESSION);
     
DataOutputStream objOut = new DataOutputStream(zOut);
     
objOut.write(object);
     
objOut.flush();
     
zOut.close();
     
data = out.toByteArray();
     
out.close();
    
} catch (IOException e) {
     
e.printStackTrace();
    
}
    
return data;
   
}
   
/**
    
*jzLib压缩的数据
    
*
    
* @param object
    
* @return
    
* @throws IOException
    
*/
   
public static byte[] unjzlib(byte[] object) {
    
byte[] data = null;
    
try {
     
ByteArrayInputStream in = new ByteArrayInputStream(object);
     
ZInputStream zIn = new ZInputStream(in);
     
byte[] buf = new byte[1024];
     
int num = -1;
     
ByteArrayOutputStream baos = new ByteArrayOutputStream();
     
while ((num = zIn.read(buf, 0, buf.length)) != -1) {
      
baos.write(buf, 0, num);
     
}
     
data = baos.toByteArray();
     
baos.flush();
     
baos.close();
     
zIn.close();
     
in.close();

} catch (IOException e) {
     
e.printStackTrace();
    
}
    
return data;
   
}
   
public static void main(String[] args) {
    
String s = "this is a test";

byte[] b1 = zip(s.getBytes());
    
System.out.println("zip:" + bytesToHexString(b1));
    
byte[] b2 = unZip(b1);
    
System.out.println("unZip:" + new String(b2));
    
byte[] b3 = bZip2(s.getBytes());
    
System.out.println("bZip2:" + bytesToHexString(b3));
    
byte[] b4 = unBZip2(b3);
    
System.out.println("unBZip2:" + new String(b4));
    
byte[] b5 = gZip(s.getBytes());
    
System.out.println("bZip2:" + bytesToHexString(b5));
    
byte[] b6 = unGZip(b5);
    
System.out.println("unBZip2:" + new String(b6));
    
byte[] b7 = jzlib(s.getBytes());
    
System.out.println("jzlib:" + bytesToHexString(b7));
    
byte[] b8 = unjzlib(b7);
    
System.out.println("unjzlib:" + new String(b8));
   
}
  
}
  
复制代码
  
实现二: 

复制代码
  
import java.io.ByteArrayInputStream;
  
import java.io.ByteArrayOutputStream;
  
import java.io.IOException;
  
import java.util.zip.GZIPInputStream;
  
import java.util.zip.GZIPOutputStream;

// 将一个字符串按照zip方式压缩和解压缩
  
public class ZipUtil {

// 压缩
    
public static String compress(String str) throws IOException {
      
if (str == null || str.length() == 0) {
        
return str;
      
}
      
ByteArrayOutputStream out = new ByteArrayOutputStream();
      
GZIPOutputStream gzip = new GZIPOutputStream(out);
      
gzip.write(str.getBytes());
      
gzip.close();
      
return out.toString("ISO-8859-1");
    
}

// 解压缩
    
public static String uncompress(String str) throws IOException {
      
if (str == null || str.length() == 0) {
        
return str;
      
}
      
ByteArrayOutputStream out = new ByteArrayOutputStream();
      
ByteArrayInputStream in = new ByteArrayInputStream(str
          
.getBytes("ISO-8859-1"));
      
GZIPInputStream gunzip = new GZIPInputStream(in);
      
byte[] buffer = new byte[256];
      
int n;
      
while ((n = gunzip.read(buffer)) >= 0) {
        
out.write(buffer, 0, n);
      
}
      
// toString()使用平台默认编码,也可以显式的指定如toString("GBK")
      
return out.toString();
    
}

// 测试方法
    
public static void main(String[] args) throws IOException {
      
System.out.println(ZipUtil.uncompress(ZipUtil.compress("中国China")));
    
}

}
  
复制代码
  
实现三: 

复制代码
  
import java.io.ByteArrayInputStream;
  
import java.io.ByteArrayOutputStream;
  
import java.io.IOException;
  
import java.util.zip.ZipEntry;
  
import java.util.zip.ZipInputStream;
  
import java.util.zip.ZipOutputStream;

public class StringCompress {
      
public static final byte[] compress(String paramString) {
          
if (paramString == null)
              
return null;
          
ByteArrayOutputStream byteArrayOutputStream = null;
          
ZipOutputStream zipOutputStream = null;
          
byte[] arrayOfByte;
          
try {
              
byteArrayOutputStream = new ByteArrayOutputStream();
              
zipOutputStream = new ZipOutputStream(byteArrayOutputStream);
              
zipOutputStream.putNextEntry(new ZipEntry("0"));
              
zipOutputStream.write(paramString.getBytes());
              
zipOutputStream.closeEntry();
              
arrayOfByte = byteArrayOutputStream.toByteArray();
          
} catch (IOException localIOException5) {
              
arrayOfByte = null;
          
} finally {
              
if (zipOutputStream != null)
                  
try {
                      
zipOutputStream.close();
                  
} catch (IOException localIOException6) {
              
}
              
if (byteArrayOutputStream != null)
                  
try {
                      
byteArrayOutputStream.close();
                  
} catch (IOException localIOException7) {
              
}
          
}
          
return arrayOfByte;
      
}

    @SuppressWarnings("unused")    
    public static final String decompress(byte[] paramArrayOfByte) {    
        if (paramArrayOfByte == null)    
            return null;    
        ByteArrayOutputStream byteArrayOutputStream = null;    
        ByteArrayInputStream byteArrayInputStream = null;    
        ZipInputStream zipInputStream = null;    
        String str;    
        try {    
            byteArrayOutputStream = new ByteArrayOutputStream();    
            byteArrayInputStream = new ByteArrayInputStream(paramArrayOfByte);    
            zipInputStream = new ZipInputStream(byteArrayInputStream);    
            ZipEntry localZipEntry = zipInputStream.getNextEntry();    
            byte[] arrayOfByte = new byte[1024];    
            int i = -1;    
            while ((i = zipInputStream.read(arrayOfByte)) != -1)    
                byteArrayOutputStream.write(arrayOfByte, 0, i);    
            str = byteArrayOutputStream.toString();    
        } catch (IOException localIOException7) {    
            str = null;    
        } finally {    
            if (zipInputStream != null)    
                try {    
                    zipInputStream.close();    
                } catch (IOException localIOException8) {    
                }    
            if (byteArrayInputStream != null)    
                try {    
                    byteArrayInputStream.close();    
                } catch (IOException localIOException9) {    
                }    
            if (byteArrayOutputStream != null)    
                try {    
                    byteArrayOutputStream.close();    
                } catch (IOException localIOException10) {    
            }    
        }    
        return str;    
    }    
    

}
  
复制代码

参考: 

https://www.cnblogs.com/dongzhongwei/p/5964758.html (以上内容部分转自此篇文章) 

http://www.blogjava.net/fastunit/archive/2008/04/25/195932.html (以上内容部分转自此篇文章) 

http://blog.csdn.net/xyw591238/article/details/51720016 (以上内容部分转自此篇文章) 