---
title: 'Java Hex To Byte & CRCChecker'
author: lcf
date: 2012-09-26T03:27:15+00:00
url: /?p=4299
categories:
  - Java
tags:
  - reprint
---
## 'Java Hex To Byte & CRCChecker'
```java

public final String byte2Hex(final byte[] btSrc) throws Exception {
   
final StringBuffer sbuffer = new StringBuffer();
   
if (btSrc != null) {
   
for (int n = 0; n < btSrc.length; n++) {
   
String stmp = "00" + Integer.toHexString(btSrc[n] & 0XFF);
   
stmp = stmp.substring(stmp.length() - 2);
   
sbuffer.append(stmp.toUpperCase());
   
}
   
}
   
return sbuffer.toString();
   
}

/**
   
* Hex2 byte.
   
*
   
* @param src
   
* the src
   
* @return the byte[]
   
*/
   
public final byte[] hex2Byte(final String src) throws Exception {
   
byte[] btRtn = new byte[0];
   
String srcTmp = src;
   
if (isHex(srcTmp)) {
   
int len = srcTmp.length();
   
if (len % 2 != 0) {
   
len++;
   
srcTmp = "0" + srcTmp;
   
}
   
len = len / 2;
   
btRtn = new byte[len];
   
for (int n = 0; n < len; n++) {
   
final int index = 2 * n;
   
final String strTemp = String.valueOf(srcTmp.charAt(index))
   
+ String.valueOf(srcTmp.charAt(index + 1));
   
final byte btTemp = (byte) Integer.parseInt(strTemp, 16);
   
btRtn[n] = btTemp;
   
}
   
}
   
return btRtn;
   
}

/**
   
* Checks if is hex.
   
*
   
* @param src
   
* the src
   
* @return true, if is hex
   
*/
   
public final boolean isHex(final String src) {
   
boolean blRtn = false;
   
if (src != null) {
   
final String pattern = "([0-9a-fA-F])*";
   
blRtn = src.matches(pattern);
   
}
   
return blRtn;
   
}

```


CRCChecker.java

```java

import java.io.File;
  
import java.io.FileInputStream;
  
import java.io.IOException;
  
import java.io.InputStream;
  
import java.util.zip.CRC32;
  
import java.util.zip.CheckedInputStream;

public class CRCChecker {

public static long getCRC(File file) throws Exception{
   
long lngRtn = 0;
   
if (file != null && file.isFile() && file.exists()) {
   
InputStream input = null;
   
CheckedInputStream checkedInput = null;
   
try {
   
input = MagicBoxHelper.validate(new FileInputStream(file));
   
CRC32 crc32 = new CRC32();
   
checkedInput = new CheckedInputStream(
   
input, crc32);
   
int intRtn = checkedInput.read();
   
while (intRtn != -1) {
   
intRtn = checkedInput.read();
   
}
   
lngRtn = crc32.getValue();
   
} catch (Exception e) {
   
throw e;
   
} finally {
   
if (checkedInput != null) {
   
try {
   
checkedInput.close();
   
} catch (IOException e) {
   
throw e;
   
}
   
}
   
if (input != null) {
   
try {
   
input.close();
   
} catch (IOException e) {
   
throw e;
   
}
   
}
   
}
   
}
   
return lngRtn;
   
}

}

```

