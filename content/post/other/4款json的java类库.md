---
title: 4款json的java类库, FastJson
author: "-"
date: 2014-03-31T02:14:35+00:00
url: /?p=6454
tags:
  - Java
  - Json
categories:
  - inbox
---
## 4款json的java类库, FastJson

JSON(JavaScript Object Notation) 是一种轻量级的数据交换格式。 易于人阅读和编写。同时也易于机器解析和生成。 它基于JavaScript Programming Language, Standard ECMA-262 3rd Edition - December 1999的一个子集。 JSON采用完全独立于语言的文本格式，这些特性使JSON成为理想的数据交换语言。

下面介绍四款处理json的java类库: Json-lib、Gson、Jackson、Fastjson

### FastJson

Fastjson是一个Java语言编写的JSON处理器,由阿里巴巴公司开发。网址: <https://github.com/alibaba/fastjson>

maven依赖配置:

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>1.2.79</version>
</dependency>

```

示例:

复制代码

```java

public static String bean2Json(Object obj){

return JSON.toJSONString(obj);

}

```

```java
  
VO vo = JSON.parseObject("...", VO.class);```
  
  
```

### Json-lib

JSON-lib is a java library for transforming beans, maps, collections, java arrays and XML to JSON and back again to beans and DynaBeans. 官网: <http://json-lib.sourceforge.net/>

maven依赖配置:

复制代码

<dependency>

<groupId>net.sf.json-lib</groupId>

<artifactId>json-lib</artifactId>

<version>2.4</version>

<classifier>jdk15</classifier>

</dependency>

复制代码

示例:

复制代码

/**

* 将对象序列化成json字符串

* @param obj

* @return

*/

public static String bean2Json(Object obj){

JSONObject jsonObject=JSONObject.fromObject(obj);

return jsonObject.toString();

}

/**

* 将json字符串反序列化为对象

* @param jsonStr

* @param objClass 反序列化为该类的对象

* @return

*/

@SuppressWarnings("unchecked")

public static <T> T json2Bean(String jsonStr,Class<T> objClass){

return (T)JSONObject.toBean(JSONObject.fromObject(jsonStr), objClass);

}

复制代码

### Gson

Gson is a Java library that can be used to convert Java Objects into their JSON representation. It can also be used to convert a JSON string to an equivalent Java object. Gson can work with arbitrary Java objects including pre-existing objects that you do not have source-code of.

官网: <https://code.google.com/p/google-gson/>

maven依赖:

<dependency>

<groupId>com.google.code.gson</groupId>

<artifactId>gson</artifactId>

<version>2.2.4</version>

</dependency>

示例:

复制代码

public static String bean2Json(Object obj){

Gson gson = new GsonBuilder().create();

return gson.toJson(obj);

}

public static <T> T json2Bean(String jsonStr,Class<T> objClass){

Gson gson = new GsonBuilder().create();

return gson.fromJson(jsonStr, objClass);

}

/**

* 把混乱的json字符串整理成缩进的json字符串

* @param uglyJsonStr

* @return

*/

public static String jsonFormatter(String uglyJsonStr){

Gson gson = new GsonBuilder().setPrettyPrinting().create();

JsonParser jp = new JsonParser();

JsonElement je = jp.parse(uglyJsonStr);

String prettyJsonString = gson.toJson(je);

return prettyJsonString;

}

复制代码

### Jackson

Jackson is a high-performance JSON processor (parser, generator)。官网: <http://jackson.codehaus.org/Home>

maven依赖:

<dependency>

<groupId>org.codehaus.jackson</groupId>

<artifactId>jackson-mapper-asl</artifactId>

<version>1.9.13</version>

</dependency>

示例:

复制代码

public static String bean2Json(Object obj) throws IOException {

ObjectMapper mapper = new ObjectMapper();

StringWriter sw = new StringWriter();

JsonGenerator gen = new JsonFactory().createJsonGenerator(sw);

mapper.writeValue(gen, obj);

gen.close();

return sw.toString();

}

public static <T> T json2Bean(String jsonStr, Class<T> objClass)

throws JsonParseException, JsonMappingException, IOException {

ObjectMapper mapper = new ObjectMapper();

return mapper.readValue(jsonStr, objClass);

}

复制代码

五、性能测试

1. Java对象序列化为Json字符串:

执行100 0000次转换，各个类库的耗时如下:  (以秒为单位)

Gson 48.891s

Json-lib 311.446s

Jackson 19.439s

FastJson 21.706

2. Json字符串 反序列化为Java对象

执行100 0000次转换，各个类库的耗时如下:  (以秒为单位)

Gson 39.280s

Json-lib 使用该类库的方法进行转换时 (测试代码见下面) ，抛出异常。其原因是Person类的属性: List<Person> friends，其List中的对象不是Person类型的对象，而是net.sf.ezmorph.bean.MorphDynaBean类型的对象。说明，Json-lib对嵌套的自定义类支持的很差，或许是我写的方法有问题。

Jackson 26.427s

FastJson 40.556

3. 总结:

Java Bean序列化为Json，性能: Jackson > FastJson > Gson > Json-lib。这4中类库的序列化结构都正确。

Json字符串反序列化为Java Bean时，性能: Jackson > Gson > FastJson >Json-lib。并且Jackson、Gson、FastJson可以很好的支持复杂的嵌套结构定义的类，而Json-lib对于复制的反序列化会出错。

Jackson、FastJson、Gson类库各有优点，各有自己的专长，都具有很高的可用性。

4. 测试用例

1) Java Bean

复制代码

public class Person {

private String name;

private FullName fullName;

private int age;

private Date birthday;

private List<String> hobbies;

private Map<String, String> clothes;

private List<Person> friends;

//getter setter 方法。略

@Override

public String toString() {

String str= "Person [name=" + name + ", fullName=" + fullName + ", age="

* age + ", birthday=" + birthday + ", hobbies=" + hobbies

* ", clothes=" + clothes + "]\n";

if(friends!=null){

str+="Friends:\n";

for (Person f : friends) {

str+="\t"+f;

}

}

return str;

}

}

class FullName {

private String firstName;

private String middleName;

private String lastName;

//构造方法、getter setter 方法，略

@Override

public String toString() {

return "[firstName=" + firstName + ", middleName="

* middleName + ", lastName=" + lastName + "]";

}

}

复制代码

2) Json-lib、Gson、Jackson、FastJson类库:

复制代码

import net.sf.json.JSONObject;

public class JsonObjectUtil {

public static String bean2Json(Object obj){

JSONObject jsonObject=JSONObject.fromObject(obj);

return jsonObject.toString();

}

@SuppressWarnings("unchecked")

public static <T> T json2Bean(String jsonStr,Class<T> objClass){

return (T)JSONObject.toBean(JSONObject.fromObject(jsonStr), objClass);

}

}

复制代码

复制代码

import com.google.gson.Gson;

import com.google.gson.GsonBuilder;

import com.google.gson.JsonElement;

import com.google.gson.JsonParser;

public class GsonUtil {

private static Gson gson = new GsonBuilder().create();

public static String bean2Json(Object obj){

return gson.toJson(obj);

}

public static <T> T json2Bean(String jsonStr,Class<T> objClass){

return gson.fromJson(jsonStr, objClass);

}

public static String jsonFormatter(String uglyJsonStr){

Gson gson = new GsonBuilder().setPrettyPrinting().create();

JsonParser jp = new JsonParser();

JsonElement je = jp.parse(uglyJsonStr);

String prettyJsonString = gson.toJson(je);

return prettyJsonString;

}

}

复制代码

复制代码

import java.io.IOException;

import java.io.StringWriter;

import org.codehaus.jackson.JsonFactory;

import org.codehaus.jackson.JsonGenerator;

import org.codehaus.jackson.JsonParseException;

import org.codehaus.jackson.map.JsonMappingException;

import org.codehaus.jackson.map.ObjectMapper;

public class JacksonUtil {

private static ObjectMapper mapper = new ObjectMapper();

public static String bean2Json(Object obj) throws IOException {

StringWriter sw = new StringWriter();

JsonGenerator gen = new JsonFactory().createJsonGenerator(sw);

mapper.writeValue(gen, obj);

gen.close();

return sw.toString();

}

public static <T> T json2Bean(String jsonStr, Class<T> objClass)

throws JsonParseException, JsonMappingException, IOException {

return mapper.readValue(jsonStr, objClass);

}

}

复制代码

复制代码

public class FastJsonUtil {

public static String bean2Json(Object obj){

return JSON.toJSONString(obj);

}

public static <T> T json2Bean(String jsonStr,Class<T> objClass){

return JSON.parseObject(jsonStr, objClass);

}

}

复制代码

3) Java对象序列化为Json字符串 测试类:

复制代码

public class TestBean2Json {

private Person p;

private Person createAPerson(String name,List<Person> friends) {

Person newPerson=new Person();

newPerson.setName(name);

newPerson.setFullName(new FullName("xxx_first", "xxx_middle", "xxx_last"));

newPerson.setAge(24);

List<String> hobbies=new ArrayList<String>();

hobbies.add("篮球");

hobbies.add("游泳");

hobbies.add("coding");

newPerson.setHobbies(hobbies);

Map<String,String> clothes=new HashMap<String, String>();

clothes.put("coat", "Nike");

clothes.put("trousers", "adidas");

clothes.put("shoes", "安踏");

newPerson.setClothes(clothes);

newPerson.setFriends(friends);

return newPerson;

}

@Before

public void init(){

List<Person> friends=new ArrayList<Person>();

friends.add(createAPerson("小明",null));

friends.add(createAPerson("Tony",null));

friends.add(createAPerson("陈小二",null));

p=createAPerson("邵同学",friends);

}

// @Test

public void testGsonBean2Json(){

System.out.println(GsonUtil.bean2Json(p));

for (int i = 0; i < 1000000; i++) {

GsonUtil.bean2Json(p);

}

}

//@Test

public void testJsonObjectBean2Json(){

System.out.println(JsonlibUtil.bean2Json(p));

for (int i = 0; i < 1000000; i++) {

JsonlibUtil.bean2Json(p);

}

}

// @Test

public void testJacksonBean2Json() throws Exception{

System.out.println(JacksonUtil.bean2Json(p));

for (int i = 0; i < 1000000; i++) {

JacksonUtil.bean2Json(p);

}

}

@Test

public void testFastJsonBean2Json() throws Exception{

System.out.println(FastJsonUtil.bean2Json(p));

for (int i = 0; i < 1000000; i++) {

FastJsonUtil.bean2Json(p);

}

}

}

复制代码

4) Json字符串 反序列化为Java对象 测试类:

复制代码

public class TestJson2Bean {

private String jsonStr;

@Before

public void init(){

jsonStr="{\"name\":\"邵同学\",\"fullName\":{\"firstName\":\"xxx_first\",\"middleName\":\"xxx_middle\",\"lastName\":\"xxx_last\"},\"age\":24,\"birthday\":null,\"hobbies\":[\"篮球\",\"游泳\",\"coding\"],\"clothes\":{\"shoes\":\"安踏\",\"trousers\":\"adidas\",\"coat\":\"Nike\"},\"friends\":[{\"name\":\"小明\",\"fullName\":{\"firstName\":\"xxx_first\",\"middleName\":\"xxx_middle\",\"lastName\":\"xxx_last\"},\"age\":24,\"birthday\":null,\"hobbies\":[\"篮球\",\"游泳\",\"coding\"],\"clothes\":{\"shoes\":\"安踏\",\"trousers\":\"adidas\",\"coat\":\"Nike\"},\"friends\":null},{\"name\":\"Tony\",\"fullName\":{\"firstName\":\"xxx_first\",\"middleName\":\"xxx_middle\",\"lastName\":\"xxx_last\"},\"age\":24,\"birthday\":null,\"hobbies\":[\"篮球\",\"游泳\",\"coding\"],\"clothes\":{\"shoes\":\"安踏\",\"trousers\":\"adidas\",\"coat\":\"Nike\"},\"friends\":null},{\"name\":\"陈小二\",\"fullName\":{\"firstName\":\"xxx_first\",\"middleName\":\"xxx_middle\",\"lastName\":\"xxx_last\"},\"age\":24,\"birthday\":null,\"hobbies\":[\"篮球\",\"游泳\",\"coding\"],\"clothes\":{\"shoes\":\"安踏\",\"trousers\":\"adidas\",\"coat\":\"Nike\"},\"friends\":null}]}";

}

// @Test

public void testGsonjson2Bean() throws Exception{

Person pp=GsonUtil.json2Bean(jsonStr, Person.class);

System.out.println(pp);

for (int i = 0; i < 1000000; i++) {

GsonUtil.json2Bean(jsonStr, Person.class);

}

}

// @Test

public void testJsonlibJson2Bean() throws Exception{

Person pp=JsonlibUtil.json2Bean(jsonStr, Person.class);

System.out.println(pp);

for (int i = 0; i < 1000000; i++) {

JsonlibUtil.json2Bean(jsonStr, Person.class);

}

}

// @Test

public void testJacksonJson2Bean() throws Exception{

Person pp=JacksonUtil.json2Bean(jsonStr, Person.class);

System.out.println(pp);

for (int i = 0; i < 1000000; i++) {

JacksonUtil.json2Bean(jsonStr, Person.class);

}

}

@Test

public void testFastJsonJson2Bean() throws Exception{

Person pp=FastJsonUtil.json2Bean(jsonStr, Person.class);

System.out.println(pp);

for (int i = 0; i < 1000000; i++) {

FastJsonUtil.json2Bean(jsonStr, Person.class);

}

}

}

复制代码

参考: <http://www.json.org/json-zh.html>

<http://www.oschina.net/code/snippet_1156226_26432>
