---
title: java zip
author: "-"
date: 2011-09-06T06:57:02+00:00
url: /?p=680
categories:
  - Java
tags:$
  - reprint
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