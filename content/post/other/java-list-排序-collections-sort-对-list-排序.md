---
title: java List 排序 Collections.sort() 对 List 排序
author: "-"
date: 2012-09-16T07:34:25+00:00
url: /?p=4047
categories:
  - Java
tags:$
  - reprint
---
## java List 排序 Collections.sort() 对 List 排序
java.util.Comparator 接口。要实现里面的函数
  
int compare(Object o1, Object o2) 返回一个基本类型的整型，返回负数表示o1 小于o2，返回0 表示o1和o2相等，返回正数表示o1大于o2。

```java
  
class User {

String name;

String age;

public User(String name,String age){

this.name=name;

this.age=age;

}

public String getAge() {

return age;

}

public void setAge(String age) {

this.age = age;

}

public String getName() {

return name;

}

public void setName(String name) {

this.name = name;

}

}

//具体的比较类，实现Comparator接口

import java.util.Comparator;

import java.util.List;

import java.util.ArrayList;

import java.util.Collections;

public class ComparatorUser implements Comparator{

public int compare(Object arg0, Object arg1) {

User user0=(User)arg0;

User user1=(User)arg1;

//首先比较年龄，如果年龄相同，则比较名字

int flag=user0.getAge().compareTo(user1.getAge());

if(flag==0){

return user0.getName().compareTo(user1.getName());

}else{

return flag;

}

}

}

//测试类

public class SortTest {

public static void main(String[] args){

List userlist=new ArrayList();

userlist.add(new User("dd","4″));

userlist.add(new User("aa","1″));

userlist.add(new User("ee","5″));

userlist.add(new User("bb","2″));

userlist.add(new User("ff","5″));

userlist.add(new User("cc","3″));

userlist.add(new User("gg","6″));

ComparatorUser comparator=new ComparatorUser();

Collections.sort(userlist, comparator);

for (int i=0;i<userlist.size();i++){

User user_temp=(User)userlist.get(i);

System.out.println(user_temp.getAge()+","+user_temp.getName());

}

}

}
  
//首先年龄排序，如果年龄相同，则按名字排序
  
"\`java

结果:
  
1, aa
  
2, bb
  
3, cc
  
4, dd
  
5, ee //注意:同样是5岁的人，则比较名字(ee,ff)，然后排序
  
5, ff
  
6, gg

http://www.blogjava.net/zygcs/archive/2008/01/17/176032.html

http://muscle-liu.iteye.com/blog/157261