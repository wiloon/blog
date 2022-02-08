---
title: dex2jar
author: "-"
date: 2014-04-10T01:42:28+00:00
url: /?p=6504
categories:
  - Uncategorized

tags:
  - reprint
---
## dex2jar
https://code.google.com/p/dex2jar/

http://blog.csdn.net/kesenhoo/article/details/6544094

dex2jar contains following compment

  1. dex-reader is designed to read the Dalvik Executable (.dex/.odex) format. It has a light weight API similar with ASM. An example here
  2. dex-translator is designed to do the convert job. It reads the dex instruction to dex-ir format, after some optimize, convert to ASM format.
  3. dex-ir used by dex-translator, is designed to represent the dex instruction
  4. dex-tools tools to work with .class files. here are examples: 
      * [Modify a apk][1]
      * [DeObfuscate a jar][2]
  5. d2j-smali [To be published] disassemble dex to smali files and assemble dex from smali files. different implementation to smali/baksmali, same syntax, but we support escape in type desc "Lcom/dex2jar\t\u1234;"
  6. dex-writer [To be published] write dex same way as dex-reader.

 [1]: https://code.google.com/p/dex2jar/wiki/ModifyApkWithDexTool
 [2]: https://code.google.com/p/dex2jar/wiki/DeObfuscateJarWithDexTool