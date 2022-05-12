---
title: Java JAXB Unmarshaller
author: lcf
date: 2012-09-26T07:05:26+00:00
url: /?p=4318
categories:
  - Java
tags:$
  - reprint
---
## Java JAXB Unmarshaller
```java

import java.io.IOException;
  
import java.io.InputStream;

import javax.xml.bind.JAXBContext;
  
import javax.xml.bind.JAXBElement;
  
import javax.xml.bind.Unmarshaller;
  
import javax.xml.parsers.DocumentBuilder;
  
import javax.xml.parsers.DocumentBuilderFactory;

import org.springframework.context.support.GenericApplicationContext;
  
import org.w3c.dom.Document;

public class ConfigReader {
   
public final <T>T read(Class<T> t, String filePath) throws ISException {
   
InputStream input;
   
try {
   
input = new GenericApplicationContext()
   
.getResource(filePath).getInputStream();
   
} catch (IOException e) {
   
throw new ISException(e);
   
}
   
return read(input, t);
   
}

public final <T>T read(InputStream inputStream, Class<T> t) throws ISException {
   
T root = null;
   
synchronized (this) {
   
try {
   
if (inputStream != null) {
   
final DocumentBuilderFactory dbf = DocumentBuilderFactory
   
.newInstance();
   
dbf.setNamespaceAware(true);
   
final JAXBContext context = JAXBContext.newInstance(t);
   
final Unmarshaller unmarshaller = context
   
.createUnmarshaller();
   
final DocumentBuilder documentBuilder = dbf
   
.newDocumentBuilder();
   
final Document doc = documentBuilder.parse(inputStream);

final JAXBElement<T> rootElement = unmarshaller.unmarshal(
   
doc, t);

root = rootElement.getValue();
   
}
   
} catch (Exception e) {
   
throw new ISException(e);
   
}
   
}
   
return root;
   
}
  
}

```