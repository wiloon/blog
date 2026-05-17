---
title: java zip
author: "-"
date: 2011-09-06T06:57:02+00:00
url: java-zip
categories:
  - Java
tags:
  - reprint
aliases:
  - /p321/
  - /p680/
  - /p736/
  - /p765/
  - /p1469/
  - /p3083/
  - /p3336/
  - /p3674/
  - /p3689/
  - /p3918/
  - /p4093/
  - /p4278/
  - /p4284/
  - /p4352/
  - /p5973/
  - /p6653/
  - /p8109/
  - /p8830/
  - /p8890/
  - /p9660/
  - /p9992/
  - /p10375/
  - /p12879/
  - /p13563/
---
## java zip
package com.wiloon.et;

import java.io.BufferedInputStream;
  
import java.io.BufferedOutputStream;
  
import java.io.File;
  
import java.io.FileInputStream;
  
import java.io.FileOutputStream;
  
import java.util.zip.ZipEntry;
  
import java.util.zip.ZipOutputStream;

public class ZipTest {
      
static final int BUFFER = 2048;
      
static String source = "D:/exported/";
      
static String destinationPath = "//x.x.x.x/share/xxx/";
      
static String fileName = "0000-0999.zip";

public static void main(String argv[]) {
          
try {
              
BufferedInputStream origin = null;
              
FileOutputStream dest = new FileOutputStream(destinationPath
                      
+ fileName);
              
ZipOutputStream out = new ZipOutputStream(new BufferedOutputStream(
                      
dest));
              
byte data[] = new byte[BUFFER];
              
File f = new File(source);
              
File files[] = f.listFiles();
              
for (int i = 0; i < files.length; i++) { FileInputStream fi = new FileInputStream(files[i]); origin = new BufferedInputStream(fi, BUFFER); ZipEntry entry = new ZipEntry(files[i].getName()); out.putNextEntry(entry); int count; while ((count = origin.read(data, 0, BUFFER)) != -1) { out.write(data, 0, count); } origin.close(); System.out.println("zip... " + files[i].getName()); files[i].delete(); } out.close(); } catch (Exception e) { e.printStackTrace(); } System.out.println("end"); } }