---
title: Java Singleton
author: lcf
date: 2012-09-26T06:50:45+00:00
url: /?p=4308
categories:
  - Java
tags:
  - reprint
---
## Java Singleton
public class ConnEnv {

/*\* The instance. */
  
private static ConnEnv instance;

private ConnEnv(){

}

public static ConnEnv getInstance(){
  
if (instance == null) {
  
createInstance();
  
}
  
return instance;
  
}

/**
  
* Creates the instance.
  
*/
  
private static synchronized void createInstance() {
  
if (instance==null) {
  
try {
  
instance = new ConnEnv();
  
} catch (Exception e) {
  
// throw e;
  
}
  
}
  
}

}