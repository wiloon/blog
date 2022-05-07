---
title: SAX 解析和生成XML文档
author: "-"
date: 2014-04-01T01:16:55+00:00
url: /?p=6458
categories:
  - Inbox
tags:
  - Java
  - Xml

---
## SAX解析和生成XML文档

SAX解析和生成XML文档

分类:  【xml】 2013-09-24 22:37 2207人阅读 评论(6) 收藏 举报

生成解析xmljavasax

目录[?](+)

原创作品，允许转载，转载时请务必以超链接形式标明文章 原始出处 、作者信息和本人声明。否则将追究法律责任。

作者: 永恒の_☆ 地址: <http://blog.csdn.net/chenghui0317/article/details/11990891>

一、前言

SAX操作xml是基于事件来完成的，自己只负责调用解析的方法，然后具体解析操作都是交给DefaultHandler处理者来完成的，总的来说使用SAX解析和生成xml文档还是比较方便的 。

二、准备条件

因为SAX是jdk自带的解析方式，所以不用添加jar包引用。

三、使用SAX实战

1. 解析xml文档

实现思路:

<1>先由SAXParserFactory这个工厂的实例生产一个SAXParser解析器；

<2>然后根据读取的xml路径，传递给SAXParser这个解析器，再调用parse()方法；

<3>在parse()方法中需要传递DefaultHandler这个类的扩展类的实例，因为它才会真正去一步步去解析xml文档的；

<4>在DefaultHandler扩展类中需要重写startDocument()，endDocument()等等方法，因为他们方法内部有返回的具体文档的结果。

具体代码如下:

 print?

import java.io.BufferedOutputStream;

import java.io.File;

import java.io.FileInputStream;

import java.io.FileNotFoundException;

import java.io.FileOutputStream;

import java.io.IOException;

import java.io.InputStream;

import java.util.ArrayList;

import java.util.List;

import javax.xml.parsers.ParserConfigurationException;

import javax.xml.parsers.SAXParser;

import javax.xml.parsers.SAXParserFactory;

import javax.xml.transform.OutputKeys;

import javax.xml.transform.Result;

import javax.xml.transform.Transformer;

import javax.xml.transform.TransformerConfigurationException;

import javax.xml.transform.sax.SAXTransformerFactory;

import javax.xml.transform.sax.TransformerHandler;

import javax.xml.transform.stream.StreamResult;

import org.xml.sax.Attributes;

import org.xml.sax.InputSource;

import org.xml.sax.SAXException;

import org.xml.sax.helpers.AttributesImpl;

import org.xml.sax.helpers.DefaultHandler;

/**

* 使用SAX操作xml的简单例子

* @author Administrator

*

*/

public class SAXOperateXmlDemo {

public void parseXml01(){

String xmlPath = "D:\\project\\dynamicWeb\\src\\resource\\user01.xml";

String xmlName = xmlPath.substring(xmlPath.lastIndexOf("\\"));

try {

//获取SAX分析器的工厂实例，专门负责创建SAXParser分析器

SAXParserFactory saxParserFactory = SAXParserFactory.newInstance();

//获取SAXParser分析器的实例

SAXParser saxParser = saxParserFactory.newSAXParser();

//和其他解析方式一样，也要间接通过InputStream输入流对象获取xml信息

//1、直接指定绝对路径获取文件输入流对象

//InputStream inputStream = new FileInputStream(xmlPath);

//2、使用类的相对路径查找xml路径

//InputStream inputStream = this.getClass().getResourceAsStream(xmlName);

//3、也可以指定路径完成InputStream输入流的实例化操作

InputStream inputStream = new FileInputStream(new File(xmlPath));

//4、使用InputSource输入源作为参数也可以转换xml

//InputSource inputSource = new InputSource(inputStream);

//解析xml文档

saxParser.parse(inputStream, new XmlSAXHandler01());//这里传递了自定义的XmlSAXHandler()管理者参数来解析xml,不像以前都是直接调用返回的Document对象

} catch (ParserConfigurationException e) {

e.printStackTrace();

} catch (SAXException e) {

e.printStackTrace();

} catch (FileNotFoundException e) {

e.printStackTrace();

} catch (IOException e) {

e.printStackTrace();

}

}

public static void main(String[] args) {

SAXOperateXmlDemo demo = new SAXOperateXmlDemo();

demo.parseXml01();

}

}

/**

* 解析SAX的处理者01

* @author Administrator

*

*/

class XmlSAXHandler01 extends DefaultHandler {

@Override

public void startDocument() throws SAXException {

System.out.println("-->startDocument() is invoked...");

super.startDocument();

}

@Override

public void endDocument() throws SAXException {

System.out.println("-->endDocument() is invoked...");

super.endDocument();

}

@Override

public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {

System.out.println("--->startElement() is invoked...");

super.startElement(uri, localName, qName, attributes);

}

@Override

public void endElement(String uri, String localName, String qName) throws SAXException {

System.out.println("--->endElement() is invoked...");

super.endElement(uri, localName, qName);

}

@Override

public void characters(char[] ch, int start, int length) throws SAXException {

System.out.println("---->characters() is invoked...");

super.characters(ch, start, length);

}

}

上面代码简单解析了一个xml，user01.xml文件的内容如下:

```html``` print?

<?xml version="1.0" encoding="utf-8" ?>

<Root>Content</Root>

接下来执行该类的main方法，console效果如下:

根据控制台的显示可知:

<1>解析类必须继承DefaultHandler这个类，重写自己需要获取节点信息的方法，不重写的情况下会调用父类的对应方法，所以不影响程序；

<2>XmlSAXHandler01这个处理者来完成xml的解析工作，并且调用方式是按照xml层级关系来处理的，比如最开始调用startDocument()获取Document对象，然后再递归调用startElement()获取根节点以及子节点的信息，其中的characters()用于获取节点文本内容信息，待节点解析完毕之后会调用endElement()，同样整个xml解析完毕之后会调用endDocument()结束。

上面只是简单的获取了xml的根目录的元素，接下来使用DefaultHandler这个处理者怎么获取节点内的信息。

具体代码如下:

 print?

public void parseXml02(){

String xmlPath = "D:\\project\\dynamicWeb\\src\\resource\\user02.xml";

try {

//获取SAX分析器的工厂实例，专门负责创建SAXParser分析器

SAXParserFactory saxParserFactory = SAXParserFactory.newInstance();

//获取SAXParser分析器的实例

SAXParser saxParser = saxParserFactory.newSAXParser();

InputStream inputStream = new FileInputStream(new File(xmlPath));

//解析xml文档

saxParser.parse(inputStream, new XmlSAXHandler02());

} catch (ParserConfigurationException e) {

e.printStackTrace();

} catch (SAXException e) {

e.printStackTrace();

} catch (FileNotFoundException e) {

e.printStackTrace();

} catch (IOException e) {

e.printStackTrace();

}

}

对应的XMLSAXHandler02的代码如下:

 print?

/**

* 解析SAX的处理者02

* @author Administrator

*

*/

class XmlSAXHandler02 extends DefaultHandler {

@Override

public void startDocument() throws SAXException {

System.out.println("-->startDocument() is invoked...");

}

@Override

public void endDocument() throws SAXException {

System.out.println("-->endDocument() is invoked...");

}

@Override

public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {

System.out.println("--->startElement() is invoked...");

System.out.println("uri的属性值: " + uri);

System.out.println("localName的属性值: " + localName);

System.out.println("qName的属性值: " + qName);

if(attributes.getLength()>0){

System.out.println("element属性值->" + attributes.getQName(0) + ": " + attributes.getValue(0)); //根据下标获取属性name和value，也可以直接传递属性name获取属性值: attributes.getValue("id")

}

}

@Override

public void endElement(String uri, String localName, String qName) throws SAXException {

System.out.println("--->endElement() is invoked...");

System.out.println("uri的属性值: " + uri);

System.out.println("localName的属性值: " + localName);

System.out.println("qName的属性值: " + qName);

}

@Override

public void characters(char[] ch, int start, int length) throws SAXException {

System.out.println("---->characters() is invoked...");

System.out.println("节点元素文本内容: " + new String(ch, start, length));

}

}

上面的xml在src下面，user02.xml具体如下:

```html``` print?

<?xml version="1.0" encoding="utf-8" ?>

<Root>

这个是根节点的内容

<user id="001">用户信息</user>

</Root>

接下来执行该类的main方法，console效果如下:

根据控制台的显示可知:

<1>XMLSAXHandler02在解析的时候执行方法是从最外层往内、从上往下依次解析的，并且每一次解析节点都是startElement()和endElement()成对出现的；

<2>图中显示了每一个节点解析的信息，并且startElement()和endElement()的区别在于前面方法有携带属性，而后面方法没有；

<3>图中之所以出现三个"节点元素文本内容"是XMLSAXHandler02也是把非标签的文本当前一个节点了，所以在解析的时候要排除这种情况，以免影响最终想要的结果。

另外发现:

<1>查看父类的方法发现它们的方法体什么都没做；

<2>SAX不支持重新修改XML的结构；

<3>如果正常业务需求，解析xml之后不可能只是简单输出下内容，而是要返回成一个集合或者其他形式返回，目前情况可以使用全局的ArrayList集合来完成解析之后节点内容的封装。

接下来需要实现如何封装SAX解析完毕的XML文档，都知道java是面向对象编程的，那么这个时候可以把文档中的每一个节点都看成一个对象，包括节点里面的属性也是一样，那么在解析XML的时候直接使用javabean封装一下，思路就非常清晰了，但是现在还有还一个问题:  如何在SAXParser调用parse()方法之后返回最终的结果集呢？就目前肯定不行的，其一方法没有返回值，其二解析操作完全交给DefaultHandler去做了，所以这种情况下肯定不能使用普通变量或者全局变量，因为使用了之后会随着当前操作类的实例化生命周期而存在，并且DefaultHandler在调用的时候又需要产生一个新的实例，这样前后就没有关联性了。 所以只能使用静态ArrayList来完成了。

具体操作如下:

1. 前面说了构建节点对象和属性对象，具体代码如下:

 print?

import java.util.List;

/**

* Xml节点对象

* @author Administrator

*

*/

public class Node {

private Long id;

private String name;

private String text;

private List attributeList;

private List<Node> nodeList;

public Long getId() {

return id;

}

public void setId(Long id) {

this.id = id;

}

public String getName() {

return name;

}

public void setName(String name) {

this.name = name;

}

public String getText() {

return text;

}

public void setText(String text) {

this.text = text;

}

public List getAttributeList() {

return attributeList;

}

public void setAttributeList(List attributeList) {

this.attributeList = attributeList;

}

public List<Node> getNodeList() {

return nodeList;

}

public void setNodeList(List<Node> nodeList) {

this.nodeList = nodeList;

}

}

 print?

/**

* Xml属性对象

* @author Administrator

*

*/

public class Attribute {

private String name;

private String value;

public String getName() {

return name;

}

public void setName(String name) {

this.name = name;

}

public String getValue() {

return value;

}

public void setValue(String value) {

this.value = value;

}

}

2. 在SAXOperateXmlDemo这个操作类中添加两个常量，具体如下:

 print?

public static List<Node> nodeList = null;

public static Node node = null;

不光集合需要全局静态化，节点对象也要全局静态化，因为解析过程中获取标签名称和标签内文本是分开操作的，如果不这样对象的属性值无法完整获取。

3. 定义xml文档解析方法，具体如下:

 print?

public void parseXml03(){

String xmlPath = "D:\\project\\dynamicWeb\\src\\resource\\user03.xml";

try {

//获取SAX分析器的工厂实例，专门负责创建SAXParser分析器

SAXParserFactory saxParserFactory = SAXParserFactory.newInstance();

//获取SAXParser分析器的实例

SAXParser saxParser = saxParserFactory.newSAXParser();

InputStream inputStream = new FileInputStream(new File(xmlPath));

//解析xml文档

saxParser.parse(inputStream, new XmlSAXHandler03());

//迭代list

if(SAXOperateXmlDemo.nodeList.size() > 0){

for (Node node : SAXOperateXmlDemo.nodeList) {

System.out.println("--------------");

System.out.println("【节点】" + node.getName() + ": " + node.getText());

List attributeList = node.getAttributeList();

if (attributeList != null) {

for (Attribute attribute : attributeList) {

System.out.println("【属性】" + attribute.getName() + ": " + attribute.getValue());

}

}

}

}

} catch (ParserConfigurationException e) {

e.printStackTrace();

} catch (SAXException e) {

e.printStackTrace();

} catch (FileNotFoundException e) {

e.printStackTrace();

} catch (IOException e) {

e.printStackTrace();

}

}

4. 对应的解析处理者代码如下:

 print?

/**

* 解析SAX的处理者03

* @author Administrator

*

*/

class XmlSAXHandler03 extends DefaultHandler {

@Override

public void startDocument() throws SAXException {

SAXOperateXmlDemo.nodeList = new ArrayList<Node>();

}

@Override

public void endDocument() throws SAXException {

}

@Override

public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {

SAXOperateXmlDemo.node = new Node();

SAXOperateXmlDemo.node.setId(null);

SAXOperateXmlDemo.node.setName(qName);

//封装当前节点的属性

List attributeList = new ArrayList();

if(attributes.getLength()>0){

for (int i = 0; i < attributes.getLength(); i++) {

Attribute attribute = new Attribute();

attribute.setName(attributes.getQName(i));

attribute.setValue(attributes.getValue(i));

attributeList.add(attribute);

}

}

SAXOperateXmlDemo.node.setAttributeList(attributeList);

}

@Override

public void endElement(String uri, String localName, String qName) throws SAXException {

}

@Override

public void characters(char[] ch, int start, int length) throws SAXException {

if(SAXOperateXmlDemo.node != null){

SAXOperateXmlDemo.node.setText(new String(ch, start, length));

//因为startElement()在characters()的前面调用，所以必须放在后面才能把文本添加进去

SAXOperateXmlDemo.nodeList.add(SAXOperateXmlDemo.node);

SAXOperateXmlDemo.node = null;

//在这里之所以重新置为null是在解析标签的时候节点与节点之间的回车符、Tab符或者空格以及普通文本等等这些字符串也算一个节点

//如果不这样，那么解析的时候会把之前添加成功的节点内的文本给替换掉。

}

}

}

5. 代码中解析的user03.xml的结构如下:

```html``` print?

<?xml version="1.0" encoding="utf-8" ?>

<Root>

<user id="001">UserInfo_1</user>

<user id="002">UserInfo_2</user>

</Root>

接下来执行该解析xml的方法，控制台显示效果如下:

根据控制台的显示可知:

<1>使用全局静态变量完成完成了对Xml解析之后的封装工作，并且在输出的时候没有问题，但是需要注意的是去掉空文本节点这种特殊情况，否则会出现获取的节点内的内容为"\n\t" 等等结果；

<2>虽然功能是完成了，但是如果Xml文档中录入的不是文本，而是添加的详细的子节点呢？这样每一个节点就是一个Node对象，在查询和使用的时候非常的不方便。

所以为了避免这种情况，作出如下改动:

因为需求只需要获取User信息，那么不用每一个解析的节点都封装成一个对象，并且属性对象和节点对象可以合并，不用分太开这样不易于后期维护。

具体操作如下:

假设现在需要解析的xml文档如下:

```html``` print?

<?xml version="1.0" encoding="utf-8" ?>

<Users>

<user id="9527">

<name>admin</name>

40</age>

<hobby>manage someone!</hobby>

</user>

<user id="9632">

<name>chenghui</name>

110</age>

<hobby>code something!</hobby>

</user>

</Users>

然后创建User实体类封装，具体如下:

 print?

/**

* xml节点对象

* @author Administrator

*

*/

public class User {

private Long id;

private String name;

private Long age;

private String hobby;

public Long getId() {

return id;

}

public void setId(Long id) {

this.id = id;

}

public String getName() {

return name;

}

public void setName(String name) {

this.name = name;

}

public Long getAge() {

return age;

}

public void setAge(Long age) {

this.age = age;

}

public String getHobby() {

return hobby;

}

public void setHobby(String hobby) {

this.hobby = hobby;

}

}

解析当前xml的方法具体如下:

 print?

public void parseXml04(){

String xmlPath = "D:\\project\\dynamicWeb\\src\\resource\\user04.xml";

try {

//获取SAX分析器的工厂实例，专门负责创建SAXParser分析器

SAXParserFactory saxParserFactory = SAXParserFactory.newInstance();

//获取SAXParser分析器的实例

SAXParser saxParser = saxParserFactory.newSAXParser();

InputStream inputStream = new FileInputStream(new File(xmlPath));

//解析xml文档

saxParser.parse(inputStream, new XmlSAXHandler04());

//迭代list

if(SAXOperateXmlDemo.userList.size() > 0){

for (User user : SAXOperateXmlDemo.userList) {

System.out.println("--------------");

System.out.println("【Id】" + user.getId());

System.out.println("【姓名】" + user.getName());

System.out.println("【年龄】" + user.getAge());

System.out.println("【爱好】" + user.getHobby());

}

}

} catch (ParserConfigurationException e) {

e.printStackTrace();

} catch (SAXException e) {

e.printStackTrace();

} catch (FileNotFoundException e) {

e.printStackTrace();

} catch (IOException e) {

e.printStackTrace();

}

}

并且当前解析类需要添加两个全局静态变量，具体如下:

 print?

public static List<User> userList = null;

public static User user = null;

对应的解析xml处理者代码如下:

 print?

/**

* 解析SAX的处理者04

* @author Administrator

*

*/

class XmlSAXHandler04 extends DefaultHandler {

private String currentQName; //因为startElement()才能获取到标签名称，但是标签的内容在characters()获取，而且他们的执行顺序一直是顺序的，所以可以使用currentQName来过渡一下获取上一次的标签名

@Override

public void startDocument() throws SAXException {

SAXOperateXmlDemo.userList = new ArrayList<User>();

}

@Override

public void endDocument() throws SAXException {

}

@Override

public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {

if(qName.equals("user")){

SAXOperateXmlDemo.user = new User(); //每次解析到user标签了才会创建user对象的实例

//添加user标签中的id属性

if(attributes.getLength() > 0){

SAXOperateXmlDemo.user.setId(Long.valueOf(attributes.getValue("id")));

}

}

this.currentQName = qName;

}

@Override

public void endElement(String uri, String localName, String qName) throws SAXException {

//需要说明的是，因为每一个非空标签都有characters(),那么无法知道user子标签循环完了

//但是可以这样，如果不考虑子标签顺序可以判断是否解析到了最后一个子标签来判断

//或者直接在user标签的endElement()中添加即可。

if(qName.equals("user")){

SAXOperateXmlDemo.userList.add(SAXOperateXmlDemo.user);

SAXOperateXmlDemo.user = null;

}

this.currentQName = null;

}

@Override

public void characters(char[] ch, int start, int length) throws SAXException {

String content = new String(ch, start, length);

//System.out.println(currentQName + ": " + content);

if(SAXOperateXmlDemo.user != null && currentQName != null){

if(currentQName.equals("name")){

SAXOperateXmlDemo.user.setName(content);

}else if(currentQName.equals("age")){

SAXOperateXmlDemo.user.setAge(Long.valueOf(content));

}else if(currentQName.equals("hobby")){

SAXOperateXmlDemo.user.setHobby(content);

}

}

}

}

直接运行该解析方法，控制台显示效果如下:

好了，现在满足需求了 解析自己需要的节点然后封装成集合展示出来。

2. 生成xml文档

SAX能够解析xml，同样肯定能生成xml，而且使用起来也不是很复杂。

实现思路:

<1>创建保存xml的结果流对象StreamResult；

<2>然后利用SAXTransformerFactory这个工厂创建TransformerHandler这个操作者；

<3>操作这个TransformerHandler获取Transformer，利用Transformer创建节点信息；

具体代码如下:

 print?

public void buildXml01(){

try {

//创建保存xml的结果流对象

Result reultXml = new StreamResult(new FileOutputStream(new File("c:\\user.xml")));

//获取sax生产工厂对象实例

SAXTransformerFactory saxTransformerFactory = (SAXTransformerFactory) SAXTransformerFactory.newInstance();

//获取sax生产处理者对象实例

TransformerHandler transformerHandle = saxTransformerFactory.newTransformerHandler();

transformerHandle.setResult(reultXml);

//获取sax生产器

Transformer transformer = transformerHandle.getTransformer();

//transformer.setOutputProperty(OutputKeys.ENCODING,"UTF-8");//xml的编码格式

transformer.setOutputProperty(OutputKeys.INDENT,"yes");//换行

//开始封装document文档对象，这里和解析一样都是成双成对的构造标签

transformerHandle.startDocument();

AttributesImpl attrImple = new AttributesImpl();

transformerHandle.startElement("", "", "Users",attrImple);

attrImple.addAttribute("", "", "id", "string", "123");

transformerHandle.startElement("", "", "user", attrImple);

transformerHandle.characters("这个是用户的信息".toCharArray(), 0, "这个是用户的信息".length());

transformerHandle.endElement("", "", "user");

transformerHandle.endElement("", "", "Users");

//因为没有appendChild等等添加子元素的方法，sax提供的是构造在startElement()和endElement()区间内的标签为包含的节点的父节点

transformerHandle.endDocument();

System.out.println("xml文档生成成功！");

} catch (FileNotFoundException e) {

e.printStackTrace();

} catch (TransformerConfigurationException e) {

e.printStackTrace();

} catch (SAXException e) {

e.printStackTrace();

}

}

执行该生成方法，控制台显示效果如下:

然后看看生成的XML，结构如下:

结果显示达到了期望，但是有一个问题:

如果使用transformer.setOutputProperty(OutputKeys.ENCODING,"UTF-8"); 重新指定了编码，插入的中文会变成乱码，现在没有想到解决方案。。

但是如果不指定编码 却没有问题，显示结果是上图中的默认的UTF-8。
