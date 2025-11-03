---
title: Java GenNode结构
author: lcf
date: 2012-09-24T08:48:33+00:00
url: /?p=4229
categories:
  - Inbox
tags:
  - reprint
---
## Java GenNode结构
GenNode.java

```java

package com.http;

import java.io.Serializable;
  
import java.util.ArrayList;
  
import java.util.HashMap;
  
import java.util.HashSet;
  
import java.util.List;
  
import java.util.Map;
  
import java.util.Set;

import org.w3c.dom.NamedNodeMap;
  
import org.w3c.dom.Node;

/**
   
* The Class Node.
   
*/
  
public class GenNode implements Serializable {

/**
   
* The Constant serialVersionUID.
   
*/
   
private static final long serialVersionUID = 1L;

public static final String ATTRIBUTE = "attribute";

/**
   
* The name.
   
*/
   
private String name;

/**
   
* The parent.
   
*/
   
private GenNode parent;

/**
   
* The value.
   
*/
   
private String value;

/**
   
* The attribute map.
   
*/
   
private Map<String, String> attributes;

/**
   
* The elements.
   
*/
   
private Map<String, List<GenNode>> elements = new HashMap<String, List<GenNode>>();

/**
   
* Instantiates a new node.
   
*
   
* @param parent the parent
   
* @param name the name
   
*/
   
public GenNode(GenNode parent, String name) {
   
this.parent = parent;
   
this.name = name;

}

/**
   
* Instantiates a new node.
   
*
   
* @param parent the parent
   
* @param name the name
   
* @param value the value
   
*/
   
public GenNode(GenNode parent, String name, String value) {
   
this.name = name;
   
this.parent = parent;
   
this.value = value;
   
}

/**
   
* Instantiates a new node.
   
*
   
* @param parent the parent
   
* @param name the name
   
* @param value the value
   
*/
   
public GenNode(GenNode parent, String name, String value, NamedNodeMap atts) {
   
this.name = name;
   
this.parent = parent;
   
this.value = value;
   
this.setAttributes(atts);
   
}

/**
   
* Adds the child.
   
*
   
* @param name the name
   
* @param value the value
   
* @return the node
   
*/
   
public GenNode addChild(String name, String value) {
   
GenNode child = new GenNode(this, name, value);
   
List<GenNode> list = null;
   
if (!elements.containsKey(name)) {
   
list = new ArrayList<GenNode>();
   
elements.put(name, list);
   
} else {
   
list = elements.get(name);
   
}
   
list.add(child);
   
return child;
   
}

public GenNode addChild(GenNode node) {
   
String name = node.getName();
   
List<GenNode> list = null;
   
if (!elements.containsKey(name)) {
   
list = new ArrayList<GenNode>();
   
elements.put(name, list);
   
} else {
   
list = elements.get(name);
   
}
   
list.add(node);
   
return node;
   
}

/**
   
* Gets the name.
   
*
   
* @return the name
   
*/
   
public String getName() {
   
return name;
   
}

/**
   
* Sets the name.
   
*
   
* @param name the new name
   
*/
   
public void setName(String name) {
   
this.name = name;
   
}

/**
   
* Gets the parent.
   
*
   
* @return the parent
   
*/
   
public GenNode getParent() {
   
return parent;
   
}

/**
   
* Sets the parent.
   
*
   
* @param parent the new parent
   
*/
   
public void setParent(GenNode parent) {
   
this.parent = parent;
   
}

/**
   
* Gets the value.
   
*
   
* @return the value
   
*/
   
public String getValue() {
   
return value;
   
}

/**
   
* Sets the value.
   
*
   
* @param value the new value
   
*/
   
public void setValue(String value) {
   
this.value = value;
   
}

/**
   
* Gets the attributes of this GenNode.
   
*
   
* @return the Map
   
*/
   
public Map<String, String> getAttributes() {
   
return this.attributes;
   
}

/**
   
* Sets the attributes.
   
*
   
* @param atts
   
*/
   
public void setAttributes(NamedNodeMap atts) {
   
if (attributes == null) {
   
attributes = new HashMap<String, String>();
   
}
   
attributes.clear();
   
for (int i = 0; i < atts.getLength(); i++) {
   
Node attrNode = atts.item(i);
   
this.attributes
   
.put(attrNode.getNodeName(), attrNode.getNodeValue());
   
}
   
}

/**
   
* Gets the attributes of this GenNode.
   
*
   
* @return the Map
   
*/
   
public List<GenNode> getAttributeNodes() {
   
return getChildren(ATTRIBUTE);
   
}

/**
   
* Gets the attribute key set.
   
*
   
* @return the attribute key set
   
*/
   
public Set<String> getAttributesKeySet() {
   
Set<String> set = new HashSet<String>();
   
List<GenNode> list = getAttributeNodes();
   
if (list != null && !list.isEmpty()) {
   
for (GenNode node : list) {
   
set.add(node.getName());
   
}
   
}
   
return set;
   
}

/**
   
* Gets the attribute.
   
*
   
* @param name the name
   
* @return the attribute
   
*/
   
public GenNode getAttribute(String name) {
   
return getChild(ATTRIBUTE + "_" + name);
   
}

/**
   
* Gets the attribute value.
   
*
   
* @param name the name
   
* @return the attribute value
   
*/
   
public String getAttributeValue(String name) {
   
GenNode node = getChild(ATTRIBUTE + "_" + name);
   
return node != null ? node.getValue() : null;
   
}

/**
   
* Size.
   
*
   
* @return the int
   
*/
   
public int size() {
   
return elements.size();
   
}

/**
   
* Gets the elements.
   
*
   
* @param name the name
   
* @return the elements
   
*/
   
protected List<GenNode> getElements(String name) {
   
return elements.get(name);
   
}

/**
   
* Gets the children.
   
*
   
* @param name the name
   
* @return the children
   
*/
   
public List<GenNode> getChildren(String name) {
   
List<NodePath> list = NodeUtil.getNodePaths(name);
   
List<GenNode> children = null;
   
int len = list.size();
   
if (len > 0) {
   
int index = 0;
   
GenNode tmpNode = this;
   
for (NodePath path : list) {
   
index++;
   
children = tmpNode.getElements(path.getKey());
   
if (children == null) {
   
return null;
   
}
   
if (children.isEmpty()) {
   
tmpNode = null;
   
break;
   
} else if (index < len) {
   
if (path.getIndex() < children.size()) {
   
tmpNode = children.get(path.getIndex());
   
} else {
   
tmpNode = null;
   
}
   
}
   
if (tmpNode == null) {
   
children = null;
   
break;
   
}
   
}
   
}
   
return children;
   
}

/**
   
* Gets the child.
   
*
   
* @param name the name
   
* @return the child
   
*/
   
public GenNode getChild(String name) {
   
List<NodePath> list = NodeUtil.getNodePaths(name);
   
GenNode tmpNode = null;
   
int len = list.size();
   
if (len > 0) {
   
int index = list.get(len - 1).getIndex();
   
tmpNode = getChild(name, index);
   
}
   
return tmpNode;
   
}

/**
   
* Gets the child value.
   
*
   
* @param name the name
   
* @return the child value
   
*/
   
public String getChildValue(String name) {
   
String value = null;
   
GenNode node = getChild(name);
   
if (node != null) {
   
value = node.getValue();
   
}
   
return value;
   
}

/**
   
* Gets the child.
   
*
   
* @param name the name
   
* @param index the index
   
* @return the child
   
*/
   
public GenNode getChild(String name, int index) {
   
GenNode rtnNode = null;
   
List<GenNode> children = getChildren(name);
   
if (children != null && !children.isEmpty() && children.size() > index) {
   
rtnNode = children.get(index);
   
}
   
return rtnNode;
   
}

/**
   
* Gets the child value.
   
*
   
* @param name the name
   
* @param index the index
   
* @return the child value
   
*/
   
public String getChildValue(String name, int index) {
   
String value = null;
   
GenNode node = getChild(name, index);
   
if (node != null) {
   
value = node.getValue();
   
}
   
return value;
   
}

/**
   
* Gets the full name.
   
*
   
* @return the full name
   
*/
   
public String getFullName() {
   
String fullName = this.name;
   
int index = 0;
   
if (parent != null) {
   
fullName = NodeUtil.makePath(parent.getFullName(), fullName);
   
List<GenNode> list = parent.getElements(this.name);
   
index = list.indexOf(this);
   
}
   
fullName = NodeUtil.makePath(fullName, index);
   
return fullName;
   
}

/*
   
* (non-Javadoc)
   
*
   
* @see java.lang.Object#toString()
   
*/
   
public String toString() {
   
StringBuffer sb = new StringBuffer();
   
sb.append("FullName = " + getFullName());
   
sb.append("; Name = " + getName());
   
sb.append("; Value = " + getValue());
   
return sb.toString();
   
}

public Map getElements() {
   
return elements;
   
}
  
}

```
  
NodePath.java
  
```java
  
package com.http;

/**
   
* The Class NodePath.
   
*/
  
public class NodePath {

/*\* The key. */
   
private String key;

/*\* The index. */
   
private int index;

/**
   
* Gets the key.
   
*
   
* @return the key
   
*/
   
public String getKey() {
   
return key;
   
}

/**
   
* Sets the key.
   
*
   
* @param key
   
* the new key
   
*/
   
public void setKey(String key) {
   
this.key = key;
   
}

/**
   
* Gets the index.
   
*
   
* @return the index
   
*/
   
public int getIndex() {
   
return index;
   
}

/**
   
* Sets the index.
   
*
   
* @param index
   
* the new index
   
*/
   
public void setIndex(int index) {
   
this.index = index;
   
}

}
  
```
  
NodeUtil.java
  
```java
  
package com.http;

import java.util.ArrayList;
  
import java.util.List;

/**
   
* The Class NodeUtil.
   
*/
  
public class NodeUtil {

/*\* The Constant SEPARATOR. */
   
public static final String SEPARATOR = "_";

/*\* The Constant LEFT_BRACKETS. */
   
public static final String LEFT_BRACKETS = "[";

/*\* The Constant RIGHT_BRACKETS. */
   
public static final String RIGHT_BRACKETS = "]";

/**
   
* Gets the node paths.
   
*
   
* @param name the name
   
* @return the node paths
   
*/
   
public static List<NodePath> getNodePaths(String name) {
   
List<NodePath> list = new ArrayList<NodePath>();
   
String path = name==null?"":name.trim();
   
String[] arr = path.split(SEPARATOR);
   
for (String key : arr) {
   
if(!key.isEmpty()) {
   
list.add(getNodePath(key));
   
}
   
}
   
return list;
   
}

/**
   
* Gets the node path.
   
*
   
* @param key the key
   
* @return the node path
   
*/
   
protected static NodePath getNodePath(String key){
   
NodePath path = new NodePath();
   
String tmpKey = key.replaceAll("\" + RIGHT_BRACKETS, "");
   
String[] arr = tmpKey.split("\" + LEFT_BRACKETS);
   
path.setKey(arr[0]);
   
if (arr.length > 1) {
   
int index = 0;
   
try {
   
index = Integer.parseInt(arr[1].trim(), 10);
   
} catch (Exception e) {
   
index = -1;
   
}
   
path.setIndex(index);
   
}
   
return path;
   
}

/**
   
* Make path.
   
*
   
* @param name the name
   
* @param index the index
   
* @return the string
   
*/
   
public static String makePath(String name, int index) {
   
String path = "";
   
if(index<0) {
   
index = 0;
   
}
   
if(name!=null && !name.trim().isEmpty()){
   
path = name + LEFT_BRACKETS + index + RIGHT_BRACKETS;
   
}
   
return path;
   
}

/**
   
* Make path.
   
*
   
* @param firstNode the first node
   
* @param lastNode the last node
   
* @return the string
   
*/
   
public static String makePath(String firstNode, String lastNode) {
   
String path = "";
   
if(firstNode!=null && !firstNode.trim().isEmpty()){
   
path = firstNode;
   
}
   
if(lastNode!=null && !lastNode.trim().isEmpty()){
   
if(path.isEmpty()){
   
path = lastNode;
   
} else {
   
path = path + SEPARATOR + lastNode;
   
}
   
}
   
return path;
   
}

/**
   
* Make path.
   
*
   
* @param firstNode the first node
   
* @param firstIndex the first index
   
* @param lastNode the last node
   
* @return the string
   
*/
   
public static String makePath(String firstNode, int firstIndex, String lastNode) {
   
String path = makePath(firstNode, firstIndex);
   
if(lastNode!=null && !lastNode.trim().isEmpty()){
   
path = path + SEPARATOR + lastNode;
   
}
   
return path;
   
}

}
  
```
  
GenNodeHandler.java
  
```java
  
package com.http;

import org.xml.sax.Attributes;
  
import org.xml.sax.SAXException;
  
import org.xml.sax.helpers.DefaultHandler;

/**
   
* The Class GenNodeHandler. SAX Handler that will read in the input XML.
   
*
   
*/
  
public class GenNodeHandler extends DefaultHandler {

private GenNode node;

private boolean isBeginning = true;

public GenNodeHandler(GenNode root) {
   
super();
   
this.node = root;
   
}

/**
   
* be invoked whenever a new element is encountered.
   
*
   
* @param uri
   
* the uri
   
* @param localName
   
* the local name
   
* @param qName
   
* the q name
   
* @param attributes
   
* the attributes
   
* @throws org.xml.sax.SAXException
   
* the sAX exception
   
*/
   
public final void startElement(final String uri, final String localName,
   
final String qName, final Attributes attributes)
   
throws SAXException {
   
if(isBeginning){
   
node.setName(qName);
   
isBeginning = false;
   
} else {
   
node = node.addChild(qName, null);
   
}
   
int length = attributes.getLength();
   
if(length > 0) {
   
GenNode attrNode = node.addChild(GenNode.ATTRIBUTE, null);
   
for(int i=0; i<length; i++){
   
attrNode.addChild(attributes.getQName(i), attributes.getValue(i));
   
}
   
}
   
}

/**
   
* be invoked whenever an end element is encountered.
   
*
   
* @param uri
   
* the uri
   
* @param localName
   
* the local name
   
* @param qName
   
* the q name
   
* @throws org.xml.sax.SAXException
   
* the sAX exception
   
*/
   
public final void endElement(final String uri, final String localName,
   
final String qName) throws SAXException {
   
node = node.getParent();
   
}

/**
   
* be invoked whenever any open characters are encountered.
   
*
   
* @param chr
   
* the character
   
* @param start
   
* the start
   
* @param length
   
* the length
   
* @throws org.xml.sax.SAXException
   
* the sAX exception
   
*/
   
public final void characters(final char[] chr, final int start,
   
final int length) throws SAXException {
   
String value = new String(chr, start, length);
   
node.setValue(value);
   
}

}
  
```
  
XMLParser.java
  
```java
  
package com.http;

import java.io.ByteArrayInputStream;
  
import java.io.InputStream;

import org.apache.xerces.parsers.SAXParser;
  
import org.xml.sax.InputSource;

/**
   
* The Class XMLBaseParser.
   
*
   
*/
  
public class XMLParser {

/**
   
* Parsers xml.
   
*
   
* @param xml the xml
   
* @return the gen node
   
* @throws Exception the exception
   
*/
   
public GenNode parsersXml(String xml) throws Exception {
   
GenNode node = null;
   
try {
   
node = new GenNode(null, "");
   
GenNodeHandler hander = new GenNodeHandler(node);
   
SAXParser sp = new SAXParser();
   
sp.setContentHandler(hander);
   
InputStream input = new ByteArrayInputStream(xml.getBytes("utf-8"));
   
sp.parse(new InputSource(input));
   
} catch (Exception e) {
   
throw e;
   
}
   
return node;
   
}
  
}
  
```