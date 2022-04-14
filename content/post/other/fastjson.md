---
title: Fastjson
author: "-"
date: 2015-08-13T07:49:03+00:00
url: /?p=8107
categories:
  - Uncategorized

tags:
  - reprint
---
## Fastjson

```java
// 序列化
String text = JSON.toJSONString(obj);
// 反序列化
 Map<String, Object> foo = JSON.parseObject(jsonStr0, Map.class);
```

### fastjson 对象转换时重命名字段名

    @JSONField(name="total_count")
    private int totalCount;

    @JSONField(name="incomplete_results")
    private boolean incompleteResults = false;

Map<String, Object> userMap =

JSON.parseObject(o, new TypeReference<Map<String, Object>>() {});
  
使用Fastjson序列化与反序列化对象

public class JSONobject {

private String obj;
  
private String color;

public String getObj() { return obj; }
  
public void setObj(String obj) { this.obj = obj; }
  
public String getcolor() { return color; }
  
public void setcolor(String color) { this.color = color; }

}

public class fastjson {

public static void main(String[] args) {
  
// TODO Auto-generated method stub
  
JSONobject ins = new JSONobject();
  
ins.setColor("red");
  
ins.setObj("s");
  
//序列化
  
String text = JSON.toJSONString(ins);
  
System.out.println(text);
  
//反序列化
  
JSONobject ins1 = JSON.parseObject(text, JSONobject.class);
  
System.out.println(ins1.getColor());
  
System.out.println(ins1.getObj());
  
}

}
  
显示的结果是:

{"color":"red","obj":"s"}
  
red
  
s
  
先建立JSONobject类，对于类里面的每个变量分别都有两个配套函数，一个都不可以少，一个是set，一个是get,其中set,与get后面的字母必须以大写字母开头

如果解析List<object[]>类型的话，需要新版本的fastjson,旧版本的会出错，而且一定要有默认的构造函数

public class part {
  
public String attr;
  
public String value;
  
public String obj;

part(String obj,String attr,String value){
  
this.obj = obj;
  
this.attr = attr;
  
this.value = value;
  
}
  
part(){

}
  
public String getObj() { return obj; }
  
public void setObj(String obj) { this.obj = obj; }
  
public String getAttr() { return attr; }
  
public void setAttr(String attr) { this.attr = attr; }
  
public String getValue() { return value; }
  
public void setValue(String value) { this.value = value; }
  
}

import java.util.ArrayList;
  
import java.util.List;

public class JSONobject {

private String obj;
  
private String color;
  
private List<part> parts = new ArrayList<part>();

public List<part> getPart() { return parts; }
  
public void setPart(List<part> parts) { this.parts = parts; }

public String getObj() { return obj; }
  
public void setObj(String obj) { this.obj = obj; }

public String getColor() { return color; }
  
public void setColor(String color) { this.color = color; }

}

import com.alibaba.fastjson.JSON;

public class fastjson {

public static void main(String[] args) {
  
// TODO Auto-generated method stub
  
JSONobject ins = new JSONobject();
  
ins.setColor("red");
  
ins.setObj("s");

part p1 = new part("head","color","red");
  
part p2 = new part("foot","color","green");

ins.getPart().add(p1);
  
ins.getPart().add(p2);
  
//序列化
  
String text = JSON.toJSONString(ins);
  
System.out.println(text);
  
//反序列化
  
JSONobject ins1 = JSON.parseObject(text, JSONobject.class);
  
System.out.println(ins1.getColor());
  
System.out.println(ins1.getObj());
  
}

}

<http://code.alibabatech.com/wiki/display/FastJSON/Tutorial>  
<https://blog.csdn.net/quan20111992/article/details/88918585>  
