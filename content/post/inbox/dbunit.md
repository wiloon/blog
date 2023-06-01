---
title: DbUnit
author: "-"
date: 2016-04-13T01:54:26+00:00
url: /?p=8888
categories:
  - Inbox
tags:
  - reprint
---
## DbUnit

<http://yangzb.iteye.com/blog/947292>
  
博客分类: QC
  
单元测试XML数据结构OraclePostgreSQL
  
相信做过单元测试的人都会对JUnit 非常的熟悉了,今天要介绍的DbUnit(<http://dbunit.sourceforge.net/> ) 则是专门针对数据库测试的对JUnit 的一个扩展,它可以将测试对象数据库置于一个测试轮回之间的状态。鉴于目前国内介绍DbUnit 的系统教程比较少见,本文将分从理论和实例两个方面带你领略DbUnit 的精彩世界。

DbUnit 设计理念
  
熟悉单元测试的开发人员都知道,在对数据库进行单元测试时候,通常采用的方案有运用模拟对象(mock objects)和stubs 两种。通过隔离关联的数据库访问类,比如JDBC 的相关操作类,来达到对数据库操作的模拟测试。然而某些特殊的系统,比如利用了EJB 的CMP(container-managed persistence) 的系统,数据库的访问对象是在最底层而且很隐蔽的,那么这两种解决方案对这些系统就显得力不从心了。

DBUnit 的设计理念就是在测试之前,备份数据库,然后给对象数据库植入我们需要的准备数据,最后,在测试完毕后,读入备份数据库,回溯到测试前的状态；
  
而且又因为DBUnit 是对JUnit 的一种扩展,开发人员可以通过创建测试用例代码,在这些测试用例的生命周期内来对数据库的操作结果进行比较。

DbUnit 测试基本概念和流程
  
基于DbUnit 的测试的主要接口是IDataSet 。IDataSet 代表一个或多个表的数据。
  
可以将数据库模式的全部内容表示为单个IDataSet 实例。这些表本身由Itable 实例来表示。
  
IDataSet 的实现有很多,每一个都对应一个不同的数据源或加载机制。最常用的几种 IDataSet 实现为:
  
FlatXmlDataSet : 数据的简单平面文件 XML 表示
  
QueryDataSet : 用 SQL 查询获得的数据
  
DatabaseDataSet : 数据库表本身内容的一种表示
  
XlsDataSet : 数据的excel 表示

一般而言,使用DbUnit 进行单元测试的流程如下:
  
1 根据业务,做好测试用的准备数据和预想结果数据,通常准备成xml 格式文件。
  
2 在setUp() 方法里边备份数据库中的关联表。
  
3 在setUp() 方法里边读入准备数据。
  
4 对测试类的对应测试方法进行实装: 执行对象方法,把数据库的实际执行结果和预想结果进行比较。
  
5 在tearDown() 方法里边, 把数据库还原到测试前状态。

DbUnit 开发实例
  
下面通过一个实例来说明DbUnit 的实际运用。

实例准备
  
比如有一个学生表[student] ,结构如下:
  
---------------------------
  
id char(4) pk 学号
  
name char(50) 姓名
  
sex char(1) 性别
  
birthday date 出生日期

---------------------------
  
准备数据如下:

---------------------------
  
id name sex birthday
  
0001 翁仔 m 1979-12-31
  
0002 王翠花 f 1982-08-09
  
---------------------------
  
测试对象类为StudentOpe.java ,里边有2 个方法:
  
findStudent(String id) : 根据主键id 找记录
  
addStudent(Student student) : 添加一条记录

在测试addStudent 方法时候,我们准备添加如下一条数据

---------------------------
  
id name sex birthday
  
0088 王耳朵 m 1982-01-01

---------------------------
  
那么在执行该方法后,数据库的student 表里的数据是这样的:

---------------------------
  
id name sex birthday
  
0001 翁仔 m 1979-12-31
  
0002 王翠花 f 1982-08-09
  
0088 王耳朵 m 1982-01-01

---------------------------

然后我们说明如何对这2 个方法进行单元测试。

实例展开
  
1 把准备数据和预想数据转换成xml 文件
  
student_pre.xml
  
---------------------------
  
<?xml version='1.0' encoding="gb2312"?>
  
<dataset>
  
<student id="0001" name=" 翁仔" sex="m" birthday="1979-12-31"/>
  
<student id="0002" name=" 王翠花" sex="f" birthday="1982-08-09"/>
  
</dataset>

---------------------------

student_exp.xml

---------------------------
  
<?xml version='1.0' encoding="gb2312"?>
  
<dataset>
  
<student id="0001" name=" 翁仔" sex="m" birthday="1979-12-31"/>
  
<student id="0002" name=" 王翠花" sex="f" birthday="1982-08-09"/>
  
<student id="0088" name=" 王耳朵" sex="m" birthday="1982-01-01"/>
  
</dataset>

---------------------------

2 实装setUp 方法,详细见代码注释。
  
---------------------------
  
protected void setUp() {
  
IDatabaseConnection connection =null;
  
try{
  
super.setUp();
  
// 本例使用postgresql 数据库
  
Class.forName("org.postgresql.Driver");
  
// 连接DB
  
Connection conn=DriverManager.getConnection("jdbc:postgresql:testdb.test","postgres","postgres");
  
// 获得DB 连接
  
connection =new DatabaseConnection(conn);

// 对数据库中的操作对象表student 进行备份
  
QueryDataSet backupDataSet = new QueryDataSet(connection);
  
backupDataSet.addTable("student");
  
file=File.createTempFile("student_back",".xml");// 备份文件
  
FlatXmlDataSet.write(backupDataSet,new FileOutputStream(file));

// 准备数据的读入
  
IDataSet dataSet = new FlatXmlDataSet( new FileInputStream("student_pre.xml"));
  
DatabaseOperation.CLEAN_INSERT.execute(connection,dataSet);

}catch(Exception e){
  
e.printStackTrace();
  
}finally{
  
try{
  
if(connection!=null) connection.close();
  
}catch(SQLException e){}
  
}
  
}

---------------------------
  
3 实装测试方法,详细见代码注释。

* 检索类方法,可以利用assertEquals() 方法,拿表的字段进行比较。

---------------------------
  
// findStudent
  
public void testFindStudent() throws Exception{
  
// 执行findStudent 方法
  
StudentOpe studentOpe=new StudentOpe();
  
Student result = studentOpe.findStudent("0001");

// 预想结果和实际结果的比较
  
assertEquals(" 翁仔",result.getName());
  
assertEquals("m",result.getSex());
  
assertEquals("1979-12-31",result.getBirthDay());
  
}

---------------------------

* 更新,添加,删除等方法,可以利用Assertion.assertEquals() 方法,拿表的整体来比较。

---------------------------
  
public void testAddStudent() throws Exception{
  
// 执行addStudent 方法
  
StudentOpe studentOpe=new StudentOpe();
  
// 被追加的记录
  
Student newStudent = new Student("0088"," 王耳朵","m","1982-01-01");
  
// 执行追加方法
  
Student result = studentOpe.addStudent(newStudent);

// 预想结果和实际结果的比较
  
IDatabaseConnection connection=null;

try{

// 预期结果取得
  
IDataSet expectedDataSet = new FlatXmlDataSet(new FileInputStream("student_exp.xml"));
  
ITable expectedTable = expectedDataSet.getTable("student");

// 实际结果取得
  
Connection conn=getConnection();
  
connection =new DatabaseConnection(conn);

IDataSet databaseDataSet = connection.createDataSet();
  
ITable actualTable = databaseDataSet.getTable("student");

// 比较
  
Assertion.assertEquals(expectedTable, actualTable);

}finally{
  
if(connection!=null) connection.close();
  
}
  
}

---------------------------

* 如果在整体比较表的时候,有个别字段不需要比较,可以用DefaultColumnFilter.excludedColumnsTable() 方法,
  
将指定字段给排除在比较范围之外。比如上例中不需要比较birthday 这个字段的话,那么可以如下代码所示进行处理:

---------------------------
  
ITable filteredExpectedTable = DefaultColumnFilter.excludedColumnsTable(expectedTable, new String[]{"birthday"});
  
ITable filteredActualTable = DefaultColumnFilter.excludedColumnsTable(actualTable,new String[]{"birthday"});
  
Assertion.assertEquals(filteredExpectedTable, filteredActualTable);

---------------------------

4 在tearDown() 方法里边, 把数据库还原到测试前状态

---------------------------
  
protected void tearDown() throws Exception{

IDatabaseConnection connection =null;
  
try{
  
super.tearDown();
  
Connection conn=getConnection();
  
connection =new DatabaseConnection(conn);

IDataSet dataSet = new FlatXmlDataSet(file);
  
DatabaseOperation.CLEAN_INSERT.execute(connection,dataSet);

}catch(Exception e){
  
e.printStackTrace();
  
}finally{
  
try{
  
if(connection!=null) connection.close();
  
}catch(SQLException e){}
  
}

}

曾经一直把Dbunit当做是测试数据库的东西(其实本来也就是),最近在研究Appfuse是 时候发现Dbunit对数据库的数据进行load和export非常方便,尤其是在自动填充数据库,或者导出数据的时候(两个可以反向进行了),或者是 WebTest测试的时候,尤为重要了,简单的几句话,就能完成数据的装载,导出,或者是查询了,下面有个例子可以说明这情况.不过注意的一点就是,配置 路径了.在Eclipse中在设置Ant的ClassPath时候就要把Dbunit和数据库的驱动程序Jar包加进去,然后别的都通过下面的例子就OK 了

<project name="SimpleTest" basedir="." default="load">
  
<property name="dbDriver" value="oracle.jdbc.driver.OracleDriver" />
  
<property name="dbUrl" value="jdbc:oracle:thin:@192.168.104.47:1521:esample" />
  
<property name="dbUser" value="esample" />
  
<property name="dbPassword" value="esample" />
  
<taskdef name="dbunit" classname="org.dbunit.ant.DbUnitTask"  />
  
<target name="load" description="Loads the database with sample data">
  
<property name="operation" value="CLEAN_INSERT" />
  
<property name="file" value="partial.xml" />
  
<dbunit driver="${dbDriver}"  url="${dbUrl}"
  
userid="${dbUser}" password="${dbPassword}">
  
<operation type="${operation}" src="${file}" format="xml" />
  
</dbunit>
  
</target>
  
<target name="export">
  
<dbunit driver="${dbDriver}" url="${dbUrl}" userid="${dbUser}" password="${dbPassword}">
  
<export dest="partial.xml"  format="xml">
  
<query name="QueryExhibtion" sql="SELECT Exhibition_Id FROM Ex_exhibition " />
  
</export>
  
</dbunit>
  
</target>
  
</project>
  
要先执行export,这样就会自动生成一个数据导出文件,如果有的话就会覆盖,然后在用load方法就可以让数据库加载刚才生成的那些数据了,具体的加 载方式要设置dbunit中的operation属性了,有UPDATE, INSERT, DELETE, DELETE_ALL, REFRESH, CLEAN_INSERT, MSSQL_INSERT, MSSQL_REFRESH, MSSQL_CLEAN_INSERT等参数了
  
这样的话项目在持续集成的时候就方便多了,关于数据库的东西都是有Dbunit自动生成了,也算是Xp方法的一个数据库的实践把.注dbunit的地址是:<http://www.dbunit.org/,上面的例子是在DBunit2.1中测试通过>.
