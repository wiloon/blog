---
title: hash, hashCode, 哈希, 散列
author: "-"
date: 2012-09-26T06:48:17+00:00
url: hashCode
categories:
  - java

tags:
  - reprint
---
## hash, hashCode, 哈希, 散列
Hash，一般直接音译成“哈希”，按真正含义译作“散列”比较合适。通过散列算法，把任意长度的输入，转换成固定长度的输出，输出就叫做散列值 (hashCode）。这种转换是一种压缩映射，也就是说，散列值所占用的空间通常远小于输入值所占用的空间，不同的输入可能会有相同的散列值。散列的目的，在于尽量分散数据的存储位置，使数据散列在不同的哈希桶(bucket)中。

hashCode：是一串固定长度的整型的数字，hashCode可以由hash函数生成。hash函数常用的算法有：直接取余法、乘法取整法、平方取中法等。由hashCode可以得到对象在hash表中的位置

hashMap、hashTable：都是基于hash表实现的，都通过单链表解决数据通途的问题。二者很类似，但是也有很明显的区别。

hashcode() 方法返回该对象的哈希码值。

在 Java 应用程序执行期间，在同一对象上多次调用 hashCode 方法时，必须一致地返回相同的整数，前提是对象上 equals 比较中所用的信息没有被修改。从某一应用程序的一次执行到同一应用程序的另一次执行，该整数无需保持一致。
  
如果根据 equals(Object) 方法，两个对象是相等的，那么在两个对象中的每个对象上调用 hashCode 方法都必须生成相同的整数结果。
  
以下情况不 是必需的: 如果根据 equals(java.lang.Object) 方法，两个对象不相等，那么在两个对象中的任一对象上调用 hashCode 方法必定会生成不同的整数结果。但是，程序员应该知道，为不相等的对象生成不同整数结果可以提高哈希表的性能。
  
实际上，由 Object 类定义的 hashCode 方法确实会针对不同的对象返回不同的整数。 (这一般是通过将该对象的内部地址转换成一个整数来实现的，但是 JavaTM 编程语言不需要这种实现技巧。) 

当equals方法被重写时，通常有必要重写 hashCode 方法，以维护 hashCode 方法的常规协定，该协定声明相等对象必须具有相等的哈希码。

hashCode()和equals()定义在Object类中，这个类是所有java类的基类，所以所有的java类都继承这两个方法。

使用hashCode()和equals()

hashCode()方法被用来获取给定对象的唯一整数。这个整数被用来确定对象被存储在HashTable类似的结构中的位置。默认的，Object类的hashCode()方法返回这个对象存储的内存地址的编号。

重写默认的实现

如果你不重写这两个方法，将几乎不遇到任何问题，但是有的时候程序要求我们必须改变一些对象的默认实现。

来看看这个例子，让我们创建一个简单的类Employee

public class Employee
  
{
      
private Integer id;
      
private String firstname;
      
private String lastName;
      
private String department;

    public Integer getId() {
        return id;
    }
    public void setId(Integer id) {
        this.id = id;
    }
    public String getFirstname() {
        return firstname;
    }
    public void setFirstname(String firstname) {
        this.firstname = firstname;
    }
    public String getLastName() {
        return lastName;
    }
    public void setLastName(String lastName) {
        this.lastName = lastName;
    }
    public String getDepartment() {
        return department;
    }
    public void setDepartment(String department) {
        this.department = department;
    }
    

}
  
上面的Employee类只是有一些非常基础的属性和getter、setter.现在来考虑一个你需要比较两个employee的情形。

public class EqualsTest {
      
public static void main(String[] args) {
          
Employee e1 = new Employee();
          
Employee e2 = new Employee();

        e1.setId(100);
        e2.setId(100);
        //Prints false in console
        System.out.println(e1.equals(e2));
    }
    

}
  
毫无疑问，上面的程序将输出false，但是，事实上上面两个对象代表的是通过一个employee。真正的商业逻辑希望我们返回true。
  
为了达到这个目的，我们需要重写equals方法。
  
public boolean equals(Object o) {
          
if(o == null)
          
{
              
return false;
          
}
          
if (o == this)
          
{
             
return true;
          
}
          
if (getClass() != o.getClass())
          
{
              
return false;
          
}
          
Employee e = (Employee) o;
          
return (this.getId() == e.getId());
  
}
  
在上面的类中添加这个方法，EauqlsTest将会输出true。
  
So are we done?没有，让我们换一种测试方法来看看。
  
import java.util.HashSet;
  
import java.util.Set;

public class EqualsTest
  
{
      
public static void main(String[] args)
      
{
          
Employee e1 = new Employee();
          
Employee e2 = new Employee();

        e1.setId(100);
        e2.setId(100);
    
        //Prints 'true'
        System.out.println(e1.equals(e2));
    
        Set<Employee> employees = new HashSet<Employee>();
        employees.add(e1);
        employees.add(e2);
        //Prints two objects
        System.out.println(employees);
    }
    

上面的程序输出的结果是两个。如果两个employee对象equals返回true，Set中应该只存储一个对象才对，问题在哪里呢？
  
我们忘掉了第二个重要的方法hashCode()。就像JDK的Javadoc中所说的一样，如果重写equals()方法必须要重写hashCode()方法。我们加上下面这个方法，程序将执行正确。
  
@Override
   
public int hashCode()
   
{
      
final int PRIME = 31;
      
int result = 1;
      
result = PRIME * result + getId();
      
return result;
   
}
  
使用Apache Commons Lang包重写hashCode() 和equals()方法
  
Apache Commons 包提供了两个非常优秀的类来生成hashCode()和equals()方法。看下面的程序。

import org.apache.commons.lang3.builder.EqualsBuilder;
  
import org.apache.commons.lang3.builder.HashCodeBuilder;
  
public class Employee
  
{
   
private Integer id;
   
private String firstname;
   
private String lastName;
   
private String department;
  
public Integer getId() {
      
return id;
   
}
   
public void setId(Integer id) {
      
this.id = id;
   
}
   
public String getFirstname() {
      
return firstname;
   
}
   
public void setFirstname(String firstname) {
      
this.firstname = firstname;
   
}
   
public String getLastName() {
      
return lastName;
   
}
   
public void setLastName(String lastName) {
      
this.lastName = lastName;
   
}
   
public String getDepartment() {
      
return department;
   
}
   
public void setDepartment(String department) {
      
this.department = department;
   
}
  
@Override
   
public int hashCode()
   
{
      
final int PRIME = 31;
      
return new HashCodeBuilder(getId()%2==0?getId()+1:getId(), PRIME).
             
toHashCode();
   
}
  
@Override
   
public boolean equals(Object o) {
      
if (o == null)
         
return false;
      
if (o == this)
         
return true;
      
if (o.getClass() != getClass())
         
return false;
      
Employee e = (Employee) o;
         
return new EqualsBuilder().
                
append(getId(), e.getId()).
                
isEquals();
      
}
   
}
  
如果你使用Eclipse或者其他的IDE，IDE也可能会提供生成良好的hashCode()方法和equals()方法。

需要注意记住的事情

尽量保证使用对象的同一个属性来生成hashCode()和equals()两个方法。在我们的案例中,我们使用员工id。
  
eqauls方法必须保证一致 (如果对象没有被修改，equals应该返回相同的值) 
  
任何时候只要a.equals(b),那么a.hashCode()必须和b.hashCode()相等。
  
两者必须同时重写。
  
当使用ORM的时候特别要注意的
  
如果你使用ORM处理一些对象的话，你要确保在hashCode()和equals()对象中使用getter和setter而不是直接引用成员变量。因为在ORM中有的时候成员变量会被延时加载，这些变量只有当getter方法被调用的时候才真正可用。
  
例如在我们的例子中，如果我们使用e1.id == e2.id则可能会出现这个问题，但是我们使用e1.getId() == e2.getId()就不会出现这个问题。

```java
  
import org.apache.commons.lang.builder.EqualsBuilder;
  
import org.apache.commons.lang.builder.HashCodeBuilder;

public final class HttpParameterKey {

/*\* The port. */
   
private int port;

/*\* The protocol. */
   
private String protocol;

/*\* The user name. */
   
private String userName;

/*\* The password. */
   
private String password;

public HttpParameterKey(String protocol, int port, String userName,
   
String password) {
   
this.port = port;
   
this.protocol = protocol;
   
this.userName = userName;
   
this.password = password;
   
}

@Override
   
public final boolean equals(final Object obj) {
   
if (obj == null) {
   
return false;
   
}
   
if (this == obj) {
   
return true;
   
}
   
if (!(obj instanceof HttpParameterKey)) {
   
return false;
   
}
   
final HttpParameterKey key = (HttpParameterKey) obj;
   
EqualsBuilder builder = new EqualsBuilder();
   
builder.append(this.protocol, key.getProtocol());
   
builder.append(this.port, key.getPort());
   
builder.append(this.userName, key.getUserName());
   
builder.append(this.password, key.getPassword());
   
return builder.isEquals();
   
}

@Override
   
public final int hashCode() {
   
HashCodeBuilder builder = new HashCodeBuilder(17, 37);
   
builder.append(this.protocol).append(this.port);
   
builder.append(this.userName).append(this.password);
   
return builder.toHashCode();
   
}

}

```

https://www.oschina.net/question/82993_75533
  
http://blog.csdn.net/fenglibing/article/details/8905007
————————————————
版权声明：本文为CSDN博主「baigp」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u010476994/article/details/80049715
