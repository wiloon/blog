---
title: java 中的内省 introspector
author: "-"
date: 2020-01-10T07:45:25+00:00
url: /?p=15309
categories:
  - Uncategorized

tags:
  - reprint
---
## java 中的内省 introspector
概述
  
经常需要使用java对象的属性来封装程序的数据，每次都使用反射技术完成此类操作过于麻烦，所以sun公司开发了一套API，专门用于操作java对象的属性。

内省(IntroSpector)是Java语言对JavaBean 类属性、事件的一种处理方法。 例如类A中有属性name,那我们可以通过getName,setName 来得到其值或者设置新的值。 通过getName/setName 来访问name属性，这就是默认的规则。

Java中提供了一套API 用来访问某个属性的getter/setter方法，通过这些API可以使你不需要了解这个规则，这些API存放于包java.beans 中。

一般的做法是通过类Introspector的getBeanInfo方法获取某个对象的BeanInfo信息,然后通过BeanInfo来获取属性的描述器(PropertyDescriptor),通过这个属性描述器就可以获取某个属性对应的getter/setter方法,然后我们就可以通过反射机制来调用这些方法。

我们又通常把javabean的实例对象称之为值对象，因为这些bean中通常只有一些信息字段和存储方法，没有功能性方法。

一个JavaBean类可以不当JavaBean用，而当成普通类用。JavaBean实际就是一种规范，当一个类满足这个规范，这个类就能被其它特定的类调用。一个类被当作javaBean使用时，JavaBean的属性是根据方法名推断出来的，它根本看不到java类内部的成员变量。去掉set前缀，然后取剩余部分，如果剩余部分的第二个字母是小写的，则把剩余部分的首字母改成小的。

内省访问JavaBean有两种方法: 
  
通过PropertyDescriptor来操作Bean对象
  
public static void demo1() throws Exception {
      
User user = new User("zhangsan", 21);
      
String propertyName = "name";
      
// 直接指定要访问的属性
      
PropertyDescriptor pd = new PropertyDescriptor(propertyName, user.getClass());
      
// 获取到读方法
      
Method readMethod = pd.getReadMethod();
      
// 反射机制调用
      
Object invoke = readMethod.invoke(user, null);
      
System.out.println("名字: " + invoke);
      
pd.getWriteMethod().invoke(user, "lisi");
      
invoke = readMethod.invoke(user, null);
      
System.out.println("名字: " + invoke);
      
}
  
}
  
通过Introspector类获得Bean对象的 BeanInfo，然后通过 BeanInfo 来获取属性的描述器 ( PropertyDescriptor ) ，通过这个属性描述器就可以获取某个属性对应的 getter/setter 方法，然后通过反射机制来调用这些方法。
  
public static void demo2() throws Exception {
      
// 获取整个Bean的信息
      
// BeanInfo beanInfo= Introspector.getBeanInfo(user.getClass());
      
// 在Object类时候停止检索，可以选择在任意一个父类停止
      
BeanInfo beanInfo = Introspector.getBeanInfo(user.getClass(), Object.class);

    System.out.println("所有属性描述: ");
    // 获取所有的属性描述
    PropertyDescriptor[] pds = beanInfo.getPropertyDescriptors();
    for (PropertyDescriptor propertyDescriptor : pds) {
        System.out.println(propertyDescriptor.getName());
    }
    System.out.println("所有方法描述: ");
    for (MethodDescriptor methodDescriptor : beanInfo.getMethodDescriptors()) {
        System.out.println(methodDescriptor.getName());
        // Method method = methodDescriptor.getMethod();
    }
    

}
  
User.java

public class User {
      
private String name;
      
private int age;
      
public User(String name, int age) {
          
this.name = name;
          
this.age = age;
      
}
      
public String getName() {
          
return name;
      
}
      
public void setName(String name) {
          
this.name = name;
      
}
      
public int getAge() {
          
return age;
      
}
      
public void setAge(int age) {
          
this.age = age;
      
}
  
}

作者: jijs
  
链接: https://www.jianshu.com/p/604d411067c8
  
来源: 简书
  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。