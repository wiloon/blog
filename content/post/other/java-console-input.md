---
title: Java Console Input
author: lcf
date: 2012-09-26T03:19:55+00:00
url: /?p=4295
categories:
  - Java
tags:$
  - reprint
---
## Java Console Input
```java

import java.io.Console;

public class ConsoleInput {

public static void main(String[] args) {
   
Console console = System.console();
   
String titleUser = "Please enter value";
   
String label = "[Encrypted value]:";
   
String titlePWD = "password:";
   
String description = "Please enter a Digit:: 0: Start encrypt words 1: Exit";
   
String flag ="0";
   
if(console!=null){
   
while("0".equals(flag.trim())) {
   
String srcWord = console.readLine("[%s]:", titleUser);

console.printf("%s", label + srcWord);
   
console.flush();
   
System.out.println();
   
System.out.println(description);
   
flag =console.readLine();
   
System.out.println();

char[] password = console.readPassword("[%s]", titlePWD);
   
String strPassword = String.valueOf(password);
   
java.util.Arrays.fill(password, '*');

console.printf("%s", titlePWD + String.valueOf(password));
   
console.flush();
   
System.out.println();
   
}
   
}
   
}
  
}

```