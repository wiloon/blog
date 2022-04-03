---
title: Retained Heap
author: "-"
date: 2017-02-07T00:10:18+00:00
url: /?p=9739
categories:
  - Uncategorized

tags:
  - reprint
---
## Retained Heap
http://supercharles888.blog.51cto.com/609344/1347144

为了开始研究,我们希望在memory 溢出时候能自动生成heap dump文件,为此,我们在运行时候添加JVM 参数: -XX:+HeapDumpOnOutOfMemoryError
  
然后,我们来做一系列实验来逐步研究各个有趣的问题。
  
实验1: 

我们先来研究最简单的memory leak例子。我们先构造一个POJO类Person,这个Person类就是一般的java 类,然后我们构造一个ArrayList,然后在一个无限循环中一直放这个Person类的实例,因为Person类和ArrayList都在堆上,而ArrayList因为是强引用,所以无法被GC回收, (因为我们List一直在用并没有摧毁) 所以一旦ArrayList所占用的堆内存填满整个heap size时候,heap就溢出了。
  
POJO类代码是: 

package com.charles.research;
  
/**
  
*
  
* 这是一个Person类,我用它来撑满heap
  
* @author charles.wang
  
*
  
*/
  
public class Person {

private String name;
  
private String sex;
  
private int age;

public Person( String name,String sex,int age){
  
this.name=name;
  
this.sex=sex;
  
this.age=age;

}

public String getName() {
  
return name;
  
}
  
public void setName(String name) {
  
this.name = name;
  
}
  
public String getSex() {
  
return sex;
  
}
  
public void setSex(String sex) {
  
this.sex = sex;
  
}
  
public int getAge() {
  
return age;
  
}
  
public void setAge(int age) {
  
this.age = age;
  
}

}

然后我们创建ArrayList,并且无限向其中添加Person类对象的方法是: 

/**
  
* 造成内存溢出,这次重复添加一个Person对象到一个列表中,因为列表是强引用,所以无法被回收,
  
* 从而最终导致内存溢出
  
*/
  
public static void makeOutOfMemory1(){

//无限往一个List中加对象,因为List是强引用,所以不会被GC,从而导致memory溢出
  
List<Person> persons = new ArrayList<Person> ();
  
while( 1>0){
  
persons.add( new Person("fakeperson","male",25));
  
}
  
}
  
当运行上述代码时候,堆溢出了,产生了heap dump文件 (因为在准备工作部分,我们用VM参数指定了如果堆溢出则产生heap dump)
  
用MAT(Memory Analyze Tool)工具分析这个hprof文件,我们发现了,它的确探测出了memory leak问题,如下: 

如图所示,这里很清楚的表示,main()方法中有一个集合类型,,然后集合中的每一个元素都是com.charles.research.Person的对象,并且每个对象的Shallow Heap和Retained Heap大小都为24byte.

因为ArrayList一直存在,所以当对象足够多时候,就把heap弄满并且溢出了。

看到没,这里创建了2261945个Person对象,每个对象占据了24个byte,所以一共占据了

24 * 2261945=54286680字节,差不多约为51.77M大小的堆空间。
  
好了,我们关注点来了, 为什么这里Person对象的Shallow Size和Retained Size都为24byte呢？

为了解决这个问题,我们要看下Shallow Size和Retained Size各是什么？

知识补充: 

Shallow Size是对象本身占据的内存的大小,不包含其引用的对象。对于常规对象 (非数组) 的Shallow Size由其成员变量的数量和类型来定,而数组的ShallowSize由数组类型和数组长度来决定,它为数组元素大小的总和。

Retained Size=当前对象大小+当前对象可直接或间接引用到的对象的大小总和。(间接引用的含义: A->B->C,C就是间接引用) ,并且排除被GC Roots直接或者间接引用的对象
  
有一篇文章非常好,这里给出链接,它非常直观的讲解了这2个概念: http://blog.csdn.net/kingzone_2008/article/details/9083327
  
所以,我们这里的Person类,因为我们机器是32位 WIN XP系统,所以对象头占据8byte,它包含String对象引用(name),占据4byte,包含String对象引用 (sex),占据4byte,包含一个int类型(age),占据4byte,所以一共占据8+4+4+4=20byte, 因为要补齐位数,所以最后尺寸为24byte. 这就是这个对象的本身大小(Shallow Heap)的大小。
  
小知识: 为了说明补齐,大家也可以做实验,如果我们Person中加一个String成员,那么Person类大小仍然为24byte,因为这个新String对象的引用4byte刚好去填了补齐的那个坑,如果再加一个String成员,那么Person类大小就直接从24byte升到32byte了,因为又产生了一个坑需要补齐。

而我们的Person类中没有引入其他的类(不包括String,因为String直接被Root GC引用) ,所以回收Person占据的内存就是回收Person自身,所以Retained Heap大小等同于Shallow Heap大小。

实验2: 

我们现在来研究类引用其他类的例子,比如我们现在再定义新的POJO类,比如叫CompanyPerson,这个CompanyPerson类引用Person类作为其成员变量 (原谅我没用继承,我这里只是为了说明问题) ,还加了一些其他成员变量,这个新的类如下: 

package com.charles.research;
  
/**
  
*
  
* 这是一个CompanyPerson类,它会引用到Person类,并且加入了一些额外属性,比如员工号,收入,职位
  
* @author charles.wang
  
*
  
*/
  
public class CompanyPerson {

//引用Person类
  
private Person person;

private String employeeId;
  
private double salary;
  
private String position;

public CompanyPerson( Person person, String employeeId, double salary,String position){
  
this.person = person;
  
this.employeeId = employeeId;
  
this.salary = salary;
  
this.position = position;
  
}

public Person getPerson() {
  
return person;
  
}
  
public void setPerson(Person person) {
  
this.person = person;
  
}
  
public String getEmployeeId() {
  
return employeeId;
  
}
  
public void setEmployeeId(String employeeId) {
  
this.employeeId = employeeId;
  
}
  
public double getSalary() {
  
return salary;
  
}
  
public void setSalary(double salary) {
  
this.salary = salary;
  
}
  
public String getPosition() {
  
return position;
  
}
  
public void setPosition(String position) {
  
this.position = position;
  
}

}
  
然后,我们按照与实验一相同的方式,在无限循环中创建CompanyPerson类,然后将他们的实例添加到一个ArrayList中从而让其堆内存溢出: 

/**
  
* 造成内存溢出,这次重复添加一个CompanyPerson对象到一个列表中,而CompanyPerson对象是引用Person对象的,因为列表是强引用,所以无法被回收,
  
* 从而最终导致内存溢出
  
*/
  
public static void makeOutOfMemory2(){

//无限往一个List中加对象,因为List是强引用,所以不会被GC,从而导致memory溢出
  
List<CompanyPerson> companyPersons = new ArrayList<CompanyPerson> ();
  
while( 1>0){
  
Person person = new Person("fackperson","male",25);
  
CompanyPerson cp = new CompanyPerson(person,"emp123",20000L,"SSE");
  
companyPersons.add( cp);
  
}

}
  
我们在分析heap dump文件: 

发现,它这次Shallow Heap为32byte,这是正确的因为它包含对象头(8byte),对象引用person(4byte),一个 String对象引用  employeeId(4byte),一个double类型的salary (8byte) ,一个String对象引用 position(4byte), 所以一共占据8+4+4+8+4=28字节,补位后为32字节。
  
但是,这次我们发现Retained Heap和Shallow Heap不同了,因为按照我们上面的结论,一个Retained Heap的大小为回收它时候能回收的heap大小,其中还包括回收它能直接/间接引用到的对象大小的总和 (不包括被GC Root直接间接引用的)  ,这里CompanyPerson直接引用了Person,而Person的Shallow Heap是24byte,所以CompanyPerson的Retained Heap大小为其自身Shallow Heap(32byte) ,加上它引用到的Person对象的24byte,所以最后是 24+32=56byte.
  
实验3: 

最后我们看下不会造成memory leak的例子,比如我们就在一个无限循环中一直创建Person对象,而不吧这些新建的Person对象添加到 List中: 

/**
  
* 这个不会造成内存溢出,因为我们每次都在Heap上创建对象,但是这个对象是弱引用对象,所以会被回收
  
*/
  
public static void makeOutOfMemory3(){

//无限创建一个Person对象
  
while( 1>0){
  
Person person = new Person("fackperson","male",25);
  
}
  
}
  
我们运行这个例子,运行了20分钟,依然在执行而不会出现 OutOfMemoryError,这是因为,这里的person都是弱引用的,所以很容易被GC回收,一旦堆到达某个阀值,则GC进程就开始回收,为了观察这个过程,我们首先获得当前运行的例子的进程PID: 

然后我们打开JConsole,本地连接到这个PID上,我们去观察Heap Memory Usage的变化半个小时:

这里很清楚的看到波浪图,说明一边在创建新对象,一边GC在回收,所以heap内存有如此波动。
  
总结: 

通过以上3个实验,我们有如下结论: 

(1)只有强引用的对象 (比如集合类型) ,在其对象中不断引用其他对象,这样才会导致memory leak.弱引用的对象会被GC回收从而不会导致memory leak.

(2)对于一个不引用其他自定义类对象的对象,它的Shallow Heap大小和Retained Heap大小相等,并且这个大小为这个对象的对象头 (取决于平台是32位还是64位)  和所有成员变量的按照类型计算出的大小 (如果是对象引用就是4个byte或者8个byte,也取决于平台是32位还是64位,这决定了你寻址用的地址的尺寸) 的总和,并且做补位操作。

(3)对于一个引用其他自定义类对象的对象,它的Shallow Heap大小和Retained Heap大小不相等,Retained Heap尺寸为该对象自己的Shallow Heap大小加上它所有直接或者间接引用到的对象的大小的总和 (不包括被GC Root直接间接引用的对象) 