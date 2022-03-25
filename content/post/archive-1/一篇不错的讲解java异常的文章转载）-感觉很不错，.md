---
title: 'Java 异常处理'
author: "-"
date: 2013-01-16T10:23:13+00:00
url: /?p=5041
categories:
  - Java
tags:
  - Exception
  - Java

---
## 'Java 异常处理'
## Java 异常处理

异常捕捉的确是对性能有影响的,那是因为一旦异常被抛出,函数也就跟着 return 了。而程序在执行时需要处理 函数栈 的上下文,这会导致性能变得很慢,尤其是线程栈比较深的时候。但从另一方面来说,异常的抛出基本上表明程序的错误。程序在绝大多数情况下,应该是在没有异常的情况下运行的, 所以,有异常的情况应该是少数的情况,不会影响正常处理的性能问题。

对于我们并不期望会发生的事,我们可以使用异常捕捉；对于我们觉得可能会发生的事,使用返回码。

https://time.geekbang.org/column/article/675



你觉得自己是一个Java专家吗？是否肯定自己  已经全面掌握了Java的异常处理机制？在下面这段代码中,你能够迅速找出异常处理的六个问题吗？


1 OutputStreamWriter out = ...
  
2 java.sql.Connection conn = ...
  
3 try { // ⑸
  
4 Statement stat = conn.createStatement();
  
5 ResultSet rs = stat.executeQuery(
  
6 "select uid, name from user");
  
7 while (rs.next())
  
8 {
  
9 out.println("ID: " + rs.getString("uid") // ⑹
  
10 ",姓名: " + rs.getString("name"));
  
11 }
  
12 conn.close(); // ⑶
  
13 out.close();
  
14 }
  
15 catch(Exception ex) // ⑵
  
16 {
  
17 ex.printStackTrace(); //⑴,⑷
  
18 }
  
作为一个Java程序员,你至少应该能够找出两个问题。但是,如果你不能找出全部六个问题,请继续阅读本文。

本文讨论的不是Java异常处理的一般性原则,因为这些原则已经被大多数人熟知。我们要做的是分析各种可称为"反例" (anti-pattern) 的违背优秀编码规范的常见坏习惯,帮助读者熟悉这些典型的反面例子,从而能够在实际工作中敏锐地察觉和避免这些问题。

反例之一: 丢弃异常

代码: 15行-18行。

这段代码捕获了异常却不作任何处理,可以算得上Java编程中的杀手。从问题出现的频繁程度和祸害程度来看,它也许可以和C/C++程序的一个恶名远播的问题相提并论??不检查缓冲区是否已满。如果你看到了这种丢弃 (而不是抛出) 异常的情况,可以百分之九十九地肯定代码存在问题 (在极少数情况下,这段代码有存在的理由,但最好加上完整的注释,以免引起别人误解) 。

这段代码的错误在于,异常 (几乎) 总是意味着某些事情不对劲了,或者说至少发生了某些不寻常的事情,我们不应该对程序发出的求救信号保持沉默和无动于衷。调用一下printStackTrace算不上"处理异常"。不错,调用printStackTrace对调试程序有帮助,但程序调试阶段结束之后,printStackTrace就不应再在异常处理模块中担负主要责任了。

丢弃异常的情形非常普遍。打开JDK的ThreadDeath类的文档,可以看到下面这段说明: "特别地,虽然出现ThreadDeath是一种'正常的情形',但ThreadDeath类是Error而不是Exception的子类,因为许多应用会捕获所有的Exception然后丢弃它不再理睬。"这段话的意思是,虽然ThreadDeath代表的是一种普通的问题,但鉴于许多应用会试图捕获所有异常然后不予以适当的处理,所以JDK把ThreadDeath定义成了Error的子类,因为Error类代表的是一般的应用不应该去捕获的严重问题。可见,丢弃异常这一坏习惯是如此常见,它甚至已经影响到了Java本身的设计。

那么,应该怎样改正呢？主要有四个选择: 

1. 处理异常。针对该异常采取一些行动,例如修正问题、提醒某个人或进行其他一些处理,要根据具体的情形确定应该采取的动作。再次说明,调用printStackTrace算不上已经"处理好了异常"。

2. 重新抛出异常。处理异常的代码在分析异常之后,认为自己不能处理它,重新抛出异常也不失为一种选择。

3. 把该异常转换成另一种异常。大多数情况下,这是指把一个低级的异常转换成应用级的异常 (其含义更容易被用户了解的异常) 。

4. 不要捕获异常。

结论一: 既然捕获了异常,就要对它进行适当的处理。不要捕获异常之后又把它丢弃,不予理睬。

反例之二: 不指定具体的异常

代码: 15行。

许多时候人们会被这样一种"美妙的"想法吸引: 用一个catch语句捕获所有的异常。最常见的情形就是使用catch(Exception ex)语句。但实际上,在绝大多数情况下,这种做法不值得提倡。为什么呢？

要理解其原因,我们必须回顾一下catch语句的用途。catch语句表示我们预期会出现某种异常,而且希望能够处理该异常。异常类的作用就是告诉Java编译器我们想要处理的是哪一种异常。由于绝大多数异常都直接或间接从java.lang.Exception派生,catch(Exception ex)就相当于说我们想要处理几乎所有的异常。

再来看看前面的代码例子。我们真正想要捕获的异常是什么呢？最明显的一个是SQLException,这是JDBC操作中常见的异常。另一个可能的异常是IOException,因为它要操作OutputStreamWriter。显然,在同一个catch块中处理这两种截然不同的异常是不合适的。如果用两个catch块分别捕获SQLException和IOException就要好多了。这就是说,catch语句应当尽量指定具体的异常类型,而不应该指定涵盖范围太广的Exception类。

另一方面,除了这两个特定的异常,还有其他许多异常也可能出现。例如,如果由于某种原因,executeQuery返回了null,该怎么办？答案是让它们继续抛出,即不必捕获也不必处理。实际上,我们不能也不应该去捕获可能出现的所有异常,程序的其他地方还有捕获异常的机会??直至最后由JVM处理。

结论二: 在catch语句中尽可能指定具体的异常类型,必要时使用多个catch。不要试图处理所有可能出现的异常。

反例之三: 占用资源不释放

代码: 3行-14行。

异常改变了程序正常的执行流程。这个道理虽然简单,却常常被人们忽视。如果程序用到了文件、Socket、JDBC连接之类的资源,即使遇到了异常,也要正确释放占用的资源。为此,Java提供了一个简化这类操作的关键词finally。

finally是样好东西: 不管是否出现了异常,Finally保证在try/catch/finally块结束之前,执行清理任务的代码总是有机会执行。遗憾的是有些人却不习惯使用finally。

当然,编写finally块应当多加小心,特别是要注意在finally块之内抛出的异常??这是执行清理任务的最后机会,尽量不要再有难以处理的错误。

结论三: 保证所有资源都被正确释放。充分运用finally关键词。

反例之四: 不说明异常的详细信息

代码: 3行-18行。

仔细观察这段代码: 如果循环内部出现了异常,会发生什么事情？我们可以得到足够的信息判断循环内部出错的原因吗？不能。我们只能知道当前正在处理的类发生了某种错误,但却不能获得任何信息判断导致当前错误的原因。

printStackTrace的堆栈跟踪功能显示出程序运行到当前类的执行流程,但只提供了一些最基本的信息,未能说明实际导致错误的原因,同时也不易解读。

因此,在出现异常时,最好能够提供一些文字信息,例如当前正在执行的类、方法和其他状态信息,包括以一种更适合阅读的方式整理和组织printStackTrace提供的信息。

结论四: 在异常处理模块中提供适量的错误原因信息,组织错误信息使其易于理解和阅读。

反例之五: 过于庞大的try块

代码: 3行-14行。

经常可以看到有人把大量的代码放入单个try块,实际上这不是好习惯。这种现象之所以常见,原因就在于有些人图省事,不愿花时间分析一大块代码中哪几行代码会抛出异常、异常的具体类型是什么。把大量的语句装入单个巨大的try块就象是出门旅游时把所有日常用品塞入一个大箱子,虽然东西是带上了,但要找出来可不容易。

一些新手常常把大量的代码放入单个try块,然后再在catch语句中声明Exception,而不是分离各个可能出现异常的段落并分别捕获其异常。这种做法为分析程序抛出异常的原因带来了困难,因为一大段代码中有太多的地方可能抛出Exception。

结论五: 尽量减小try块的体积。

反例之六: 输出数据不完整

代码: 7行-11行。

不完整的数据是Java程序的隐形杀手。仔细观察这段代码,考虑一下如果循环的中间抛出了异常,会发生什么事情。循环的执行当然是要被打断的,其次,catch块会执行??就这些,再也没有其他动作了。已经输出的数据怎么办？使用这些数据的人或设备将收到一份不完整的 (因而也是错误的) 数据,却得不到任何有关这份数据是否完整的提示。对于有些系统来说,数据不完整可能比系统停止运行带来更大的损失。

较为理想的处置办法是向输出设备写一些信息,声明数据的不完整性；另一种可能有效的办法是,先缓冲要输出的数据,准备好全部数据之后再一次性输出。

结论六: 全面考虑可能出现的异常以及这些异常对执行流程的影响。

改写后的代码

根据上面的讨论,下面给出改写后的代码。也许有人会说它稍微有点?嗦,但是它有了比较完备的异常处理机制。


OutputStreamWriter out = ...
  
java.sql.Connection conn = ...
  
try {
  
Statement stat = conn.createStatement();
  
ResultSet rs = stat.executeQuery(
  
"select uid, name from user");
  
while (rs.next())
  
{
  
out.println("ID: " + rs.getString("uid") + ",姓名: " + rs.getString("name"));
  
}
  
}
  
catch(SQLException sqlex)
  
{
  
out.println("警告: 数据不完整");
  
throw new ApplicationException("读取数据时出现SQL错误", sqlex);
  
}
  
catch(IOException ioex)
  
{
  
throw new ApplicationException("写入数据时出现IO错误", ioex);
  
}
  
finally
  
{
  
if (conn != null) {
  
try {
  
conn.close();
  
}
  
catch(SQLException sqlex2)
  
{
  
System.err(this.getClass().getName() + ".mymethod - 不能关闭数据库连接: " + sqlex2.toString());
  
}
  
}if (out != null) {
  
try {
  
out.close();
  
}
  
catch(IOException ioex2)
  
{
  
System.err(this.getClass().getName() + ".mymethod - 不能关闭输出文件" + ioex2.toString());
  
}
  
}
  
}
  
本文的结论不是放之四海皆准的教条,有时常识和经验才是最好的老师。如果你对自己的做法没有百分之百的信心,务必加上详细、全面的注释。

另一方面,不要笑话这些错误,不妨问问你自己是否真地彻底摆脱了这些坏习惯。即使最有经验的程序员偶尔也会误入歧途,原因很简单,因为它们确确实实带来了"方便"。所有这些反例都可以看作Java编程世界的恶魔,它们美丽动人,无孔不入,时刻诱惑着你。也许有人会认为这些都属于鸡皮蒜毛的小事,不足挂齿,但请记住: 勿以恶小而为之,勿以善小而不为。

----------------------下面是一些java异常集-------------------------------
  
算术异常类: ArithmeticExecption

空指针异常类: NullPointerException

类型强制转换异常: ClassCastException

数组负下标异常: NegativeArrayException

数组下标越界异常: ArrayIndexOutOfBoundsException

违背安全原则异常: SecturityException

文件已结束异常: EOFException

文件未找到异常: FileNotFoundException

字符串转换为数字异常: NumberFormatException
  
操作数据库异常: SQLException
  
输入输出异常: IOException
  
方法未找到异常: NoSuchMethodException

java.lang.AbstractMethodError

抽象方法错误。当应用试图调用抽象方法时抛出。

java.lang.AssertionError

断言错。用来指示一个断言失败的情况。

java.lang.ClassCircularityError

类循环依赖错误。在初始化一个类时,若检测到类之间循环依赖则抛出该异常。

java.lang.ClassFormatError

类格式错误。当Java虚拟机试图从一个文件中读取Java类,而检测到该文件的内容不符合类的有效格式时抛出。

java.lang.Error

错误。是所有错误的基类,用于标识严重的程序运行问题。这些问题通常描述一些不应被应用程序捕获的反常情况。

java.lang.ExceptionInInitializerError

初始化程序错误。当执行一个类的静态初始化程序的过程中,发生了异常时抛出。静态初始化程序是指直接包含于类中的static语句段。

java.lang.IllegalAccessError

违法访问错误。当一个应用试图访问、修改某个类的域 (Field) 或者调用其方法,但是又违反域或方法的可见性声明,则抛出该异常。

java.lang.IncompatibleClassChangeError

不兼容的类变化错误。当正在执行的方法所依赖的类定义发生了不兼容的改变时,抛出该异常。一般在修改了应用中的某些类的声明定义而没有对整个应用重新编译而直接运行的情况下,容易引发该错误。

java.lang.InstantiationError

实例化错误。当一个应用试图通过Java的new操作符构造一个抽象类或者接口时抛出该异常.

java.lang.InternalError

内部错误。用于指示Java虚拟机发生了内部错误。

java.lang.LinkageError

链接错误。该错误及其所有子类指示某个类依赖于另外一些类,在该类编译之后,被依赖的类改变了其类定义而没有重新编译所有的类,进而引发错误的情况。

java.lang.NoClassDefFoundError

未找到类定义错误。当Java虚拟机或者类装载器试图实例化某个类,而找不到该类的定义时抛出该错误。

java.lang.NoSuchFieldError

域不存在错误。当应用试图访问或者修改某类的某个域,而该类的定义中没有该域的定义时抛出该错误。

java.lang.NoSuchMethodError

方法不存在错误。当应用试图调用某类的某个方法,而该类的定义中没有该方法的定义时抛出该错误。

java.lang.OutOfMemoryError

内存不足错误。当可用内存不足以让Java虚拟机分配给一个对象时抛出该错误。

java.lang.StackOverflowError

堆栈溢出错误。当一个应用递归调用的层次太深而导致堆栈溢出时抛出该错误。

java.lang.ThreadDeath

线程结束。当调用Thread类的stop方法时抛出该错误,用于指示线程结束。

java.lang.UnknownError

未知错误。用于指示Java虚拟机发生了未知严重错误的情况。

java.lang.UnsatisfiedLinkError

未满足的链接错误。当Java虚拟机未找到某个类的声明为native方法的本机语言定义时抛出。

java.lang.UnsupportedClassVersionError

不支持的类版本错误。当Java虚拟机试图从读取某个类文件,但是发现该文件的主、次版本号不被当前Java虚拟机支持的时候,抛出该错误。

java.lang.VerifyError

验证错误。当验证器检测到某个类文件中存在内部不兼容或者安全问题时抛出该错误。

java.lang.VirtualMachineError

虚拟机错误。用于指示虚拟机被破坏或者继续执行操作所需的资源不足的情况。
  
java.lang.ArithmeticException

算术条件异常。譬如: 整数除零等。

java.lang.ArrayIndexOutOfBoundsException

数组索引越界异常。当对数组的索引值为负数或大于等于数组大小时抛出。

java.lang.ArrayStoreException

数组存储异常。当向数组中存放非数组声明类型对象时抛出。

java.lang.ClassCastException

类造型异常。假设有类A和B (A不是B的父类或子类) ,O是A的实例,那么当强制将O构造为类B的实例时抛出该异常。该异常经常被称为强制类型转换异常。

java.lang.ClassNotFoundException

找不到类异常。当应用试图根据字符串形式的类名构造类,而在遍历CLASSPAH之后找不到对应名称的class文件时,抛出该异常。

java.lang.CloneNotSupportedException

不支持克隆异常。当没有实现Cloneable接口或者不支持克隆方法时,调用其clone()方法则抛出该异常。

java.lang.EnumConstantNotPresentException

枚举常量不存在异常。当应用试图通过名称和枚举类型访问一个枚举对象,但该枚举对象并不包含常量时,抛出该异常。

java.lang.Exception

根异常。用以描述应用程序希望捕获的情况。

java.lang.IllegalAccessException

违法的访问异常。当应用试图通过反射方式创建某个类的实例、访问该类属性、调用该类方法,而当时又无法访问类的、属性的、方法的或构造方法的定义时抛出该异常。

java.lang.IllegalMonitorStateException

违法的监控状态异常。当某个线程试图等待一个自己并不拥有的对象 (O) 的监控器或者通知其他线程等待该对象 (O) 的监控器时,抛出该异常。

java.lang.IllegalStateException

违法的状态异常。当在Java环境和应用尚未处于某个方法的合法调用状态,而调用了该方法时,抛出该异常。

java.lang.IllegalThreadStateException

违法的线程状态异常。当县城尚未处于某个方法的合法调用状态,而调用了该方法时,抛出异常。

java.lang.IndexOutOfBoundsException

索引越界异常。当访问某个序列的索引值小于0或大于等于序列大小时,抛出该异常。

java.lang.InstantiationException

实例化异常。当试图通过newInstance()方法创建某个类的实例,而该类是一个抽象类或接口时,抛出该异常。

java.lang.InterruptedException

被中止异常。当某个线程处于长时间的等待、休眠或其他暂停状态,而此时其他的线程通过Thread的interrupt方法终止该线程时抛出该异常。

java.lang.NegativeArraySizeException

数组大小为负值异常。当使用负数大小值创建数组时抛出该异常。

java.lang.NoSuchFieldException

属性不存在异常。当访问某个类的不存在的属性时抛出该异常。

java.lang.NoSuchMethodException

方法不存在异常。当访问某个类的不存在的方法时抛出该异常。

java.lang.NullPointerException

空指针异常。当应用试图在要求使用对象的地方使用了null时,抛出该异常。譬如: 调用null对象的实例方法、访问null对象的属性、计算null对象的长度、使用throw语句抛出null等等。

java.lang.NumberFormatException

数字格式异常。当试图将一个String转换为指定的数字类型,而该字符串确不满足数字类型要求的格式时,抛出该异常。

java.lang.RuntimeException

运行时异常。是所有Java虚拟机正常操作期间可以被抛出的异常的父类。

java.lang.SecurityException

安全异常。由安全管理器抛出,用于指示违反安全情况的异常。

java.lang.StringIndexOutOfBoundsException

字符串索引越界异常。当使用索引值访问某个字符串中的字符,而该索引值小于0或大于等于序列大小时,抛出该异常。

java.lang.TypeNotPresentException

类型不存在异常。当应用试图以某个类型名称的字符串表达方式访问该类型,但是根据给定的名称又找不到该类型是抛出该异常。该异常与ClassNotFoundException的区别在于该异常是unchecked (不被检查) 异常,而ClassNotFoundException是checked (被检查) 异常。

java.lang.UnsupportedOperationException

不支持的方法异常。指明请求的方法不被支持情况的异常。

异常
  
javax.servlet.jsp.JspException: Cannot retrieve mapping for action /Login  (/Login是你的action名字) 

可能原因
  
action没有再struts-config.xml 中定义,或没有找到匹配的action,例如在JSP文件中使用 <html:form action="Login.do".将表单提交给Login.do处理,如果出现上述异常,请查看struts-config.xml中的定义部分,有时可能是打错了字符或者是某些不符合规则,可以使用strutsconsole工具来检查。
  
--------------------------------------
  
异常
  
org.apache.jasper.JasperException: Cannot retrieve definition for form bean null

可能原因

这个异常是因为Struts根据struts-config.xml中的mapping没有找到action期望的form bean。大部分的情况可能是因为在form-bean中设置的name属性和action中设置的name属性不匹配所致。换句话说,action和form都应该各自有一个name属性,并且要精确匹配,包括大小写。这个错误当没有name属性和action关联时也会发生,如果没有在action中指定name属性,那么就没有name属性和action相关联。当然当action制作某些控制时,譬如根据参数值跳转到相应的jsp页面,而不是处理表单数据,这是就不用name属性,这也是action的使用方法之一。
  
--------------------------------------
  
异常
  
No action instance for path /xxxx could be created

可能原因
  
特别提示: 因为有很多中情况会导致这个错误的发生,所以推荐大家调高你的web服务器的日志/调试级别,这样可以从更多的信息中看到潜在的、在试图创建action类时发生的错误,这个action类你已经在struts-config.xml中设置了关联 (即添加了标签) 。

在struts-config.xml中通过action标签的class属性指定的action类不能被找到有很多种原因,例如: 定位编译后的.class文件失败。Failure to place compiled .class file for the action in the classpath (在web开发中,class的的位置在r WEB-INF/classes,所以你的action class必须要在这个目录下。例如你的action类位于WEB-INF/classes/action/Login.class,那么在struts-config.xml中设置action的属性type时就是action.Login).
  
拼写错误,这个也时有发生,并且不易找到,特别注意第一个字母的大小写和包的名称。
  
--------------------------------------
  
异常
  
javax.servlet.jsp.JspException: No getter method for property username of bean org.apache.struts.taglib.html.BEAN

可能原因
  
没有位form bean中的某个变量定义getter 方法

这个错误主要发生在表单提交的FormBean中,用struts标记<html:text property="username">时,在FormBean中必须有一个getUsername()方法。注意字母"U"。
  
--------------------------------------
  
异常
  
java.lang.NoClassDefFoundError: org/apache/struts/action/ActionForm

可能原因
  
这个错误主要发生在在classpath中找不到相应的Java .class文件。如果这个错误发生在web应用程序的运行时,主要是因为指定的class文件不在web server的classpath中 (/WEB-INF/classes 和 /WEB-INF/lib) 。在上面的错误中,原因是找不到ActionForm类。
  
--------------------------------------
  
异常
  
javax.servlet.jsp.JspException: Exception creating bean of class org.apache.struts.action.ActionForm: {1}

可能原因
  
Instantiating Struts-provided ActionForm class directly instead of instantiating a class derived off ActionForm. This mightoccur implicitly if you specify that a form-bean is this Struts ActionForm class rather than specifying a child of this classfor the form-bean.

Not associating an ActionForm-descended class with an action can also lead to this error.
  
--------------------------------------
  
异常
  
javax.servlet.jsp.JspException: Cannot find ActionMappings or ActionFormBeans collection

可能原因
  
不是标识Struts actionServlet的<servlet>标记就是映射.do扩展名的<sevlet-mapping>标记或者两者都没有在web.xml中声明。

在struts-config.xml中的打字或者拼写错误也可导致这个异常的发生。例如缺少一个标记的关闭符号/>。最好使用struts console工具检查一下。

另外,load-on-startup必须在web.xml中声明,这要么是一个空标记,要么指定一个数值,这个数值用来表servlet运行的优先级,数值越大优先级越低。

还有一个和使用load-on-startup有关的是使用Struts预编译JSP文件时也可能导致这个异常。
  
--------------------------------------
  
异常
  
java.lang.NullPointerException at org.apache.struts.util.RequestUtils.forwardURL(RequestUtils.java:1223)

可能原因
  
在struts-config.xml中的forward元素缺少path属性。例如应该是如下形式: 
  
<forward name="userhome" path="/user/userhome.jsp"/>
  
--------------------------------------
  
异常
  
javax.servlet.jsp.JspException: Cannot find bean org.apache.struts.taglib.html.BEAN in any scope
  
Probable Causes
  
试图在Struts的form标记外使用form的子元素。这常常发生在你在</html:form>后面使用Struts的html标记。另外要注意可能你不经意使用的无主体的标记,如<html:form … />,这样web 服务器解析时就当作一个无主体的标记,随后使用的所有<html>标记都被认为是在这个标记之外的,如又使用了<html:text property="id">还有就是在使用taglib引入HTML标记库时,你使用的prefix的值不是html。
  
--------------------------------------
  
异常
  
javax.servlet.jsp.JspException: Missing message for key xx.xx.xx

Probable Causes
  
这个key的值对没有在资源文件ApplicationResources.properties中定义。如果你使用eclipse时经常碰到这样的情况,当项目重新编译时,eclipse会自动将classes目录下的资源文件删除。

资源文件ApplicationResources.properties 不在classpath中应将资源文件放到 WEB-INF/classes 目录下,当然要在struts-config.xml中定义)
  
--------------------------------------
  
异常
  
Cannot find message resources under key org.apache.struts.action.MESSAGE

可能原因
  
很显然,这个错误是发生在使用资源文件时,而Struts没有找到资源文件。

Implicitly trying to use message resources that are not available (such as using empty html:options tag instead of specifyingthe options in its body - this assumes options are specified in ApplicationResources.properties file)

XML parser issues - too many, too few, incorrect/incompatible versions
  
--------------------------------------
  
异常
  
Strange and seemingly random characters in HTML and on screen, but not in original JSP or servlet.

可能原因
  
混和使用Struts的html:form标记和标准的HTML标记不正确。

使用的编码样式在本页中不支持。
  
--------------------------------------
  
异常
  
"Document contained no data" in Netscape

No data rendered (completely empty) page in Microsoft Internet Explorer

可能原因
  
使用一个Action的派生类而没有实现perform()方法或execute()方法。在Struts1.0中实现的是perform()方法,在Struts1.1中实现的是execute()方法,但Struts1.1向后兼容perform()方法。但你使用Struts1.1创建一个Action的派生类,并且实现了execute()方法,而你在Struts1.0中运行的话,就会得到"Document contained nodata" error message in Netscape or a completely empty (no HTML whatsoever) page rendered in Microsoft Internet Explorer."的错误信息。

-----------------------------------------
  
异常
  
ServletException: BeanUtils.populate
  
解决方案
  
在用Struts上传文件时,遇到了javax.servlet.ServletException: BeanUtils.populate异常。
  
我的ActionServlet并没有用到BeanUtils这些工具类。后来仔细检查代码发现是在jsp文件里的form忘了加enctype=&quot;multipart/form-data&quot; 了。所以写程序遇到错误或异常应该从多方面考虑问题存在的可能性,想到系统提示信息以外的东西。
  
------------------------------------------
  
1. 定义Action后, 如果指定了name, 那么必须要定义一个与它同名的FormBean才能进行form映射.2. 如果定义Action后, 提交页面时出现 "No input attribute for mapping path..." 错误, 则需要在其input属性中定义转向的页面.3. 如果插入新的数据时出现 "Batch update row count wrong:..." 错误, 则说明XXX.hbm.xml中指定的key的类型为原始类型(int, long),因为这种类型会自动分配值, 而这个值往往会让系统认为已经存在该记录, 正确的方法是使用java.lang.Integer或java.lang.Long对象.4. 如果插入数据时出现 "argument type mismatch" 错误, 可能是你使用了Date等特殊对象, 因为struts不能自动从String型转换成Date型,所以, 你需要在Action中手动把String型转换成Date型.5. Hibernate中, Query的iterator()比list()方法快很多.6. 如果出现 "equal symbol expected" 错误, 说明你的strtus标签中包含另一个标签或者变量, 例如:
  
<html:select property="test" onchange="<%=test%>"/>
  
或者
  
<html:hidden property="test" value="<bean:write name="t" property="p"/>"/>
  
这样的情况...
  
-----------------------------------------
  
错误: Exception in thread "main" org.hibernate.exception.SQLGrammarException: Could not execute JDBC batch update原因与解决:       因为Hibernate Tools (或者Eclipse本身的Database Explorer) 生成\*.hbn.xml工具中包含有catalog="\**\*" (\*表示数据库名称) 这样的属性,将该属性删除就可以了
  
-----------------------------------------
  
错误: org.hibernate.ObjectDeletedException: deleted object would be re-saved by cascade (remove deleted object from associations)
  
原因与解决: 
  
方法1 删除Set方的cascade
  
方法2 解决关联关系后,再删除
  
方法3 在many-to-one方增加cascade 但值不能是none
  
最后一招: 
  
检查一下hashCode equals是否使用了id作为唯一标示的选项了；我用uuid.hex时是没有问题的；但是用了native,就不行了,怎么办？删除啊！
  
------------------------------------------
  
问题: 今天用Tomcat 5.5.12,发现原来很好用的系统不能用了,反复测试发现页面中不能包含 taglib,否则会出现以下提示: HTTP Status 500 -type Exception reportMessage description The server encountered an internal error () that prevented it from fulfilling this request.exceptionorg.apache.jasper.JasperException: /index.jsp(1,1) Unable to read TLD "META-INF/tlds/struts-bean.tld" from JAR file"file:\*****/WEB-INF/lib/struts.jar":原因: 更新了工程用的lib文件夹下的jar,发布时也发布了servlet.jar和jsp-api.jar。解决: 把jsp-api.jar删除就解决这个问题了。------------------------------------------
  
错误:  java.lang.NullPointerException
  
原因:  发现 dao 实例、 manage 实例等需要注入的东西没有被注入 (俗称空指针异常) 解决: 这个时候,你应该查看日志文件；默认是应用服务器的 log 文件,比如 Tomcat 就是 [Tomcat 安装目录 ]/logs ；你会发现提示你: 可能是: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'sf' defined in ServletContextresource [/WEB-INF/applicationContext.xml]: Initialization of bean failed; nested exception isorg.hibernate.HibernateException: could not configure from URL: file:src/hibernate.cfg.xmlorg.hibernate.HibernateException: could not configure from URL: file:src/hibernate.cfg.xml……………………….Caused by: java.io.FileNotFoundException: srchibernate.cfg.xml可能是: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'sessionFactory' defined inServletContext resource [/WEB-INF/applicationContext.xml]: Initialization of bean failed; nested exception isorg.hibernate.MappingException: Resource: com/mcc/coupon/model/UserRole.hbm.xml not foundorg.hibernate.MappingException: Resource: com/mcc/coupon/model/UserRole.hbm.xml not found然后你就知道原因是因为配置文件的解析出了错误,这个通过 Web 页面是看不出来的。更多的是持久化影射文件出的错误；导致了没有被解析；当然你需要的功能就无法使用了。
  
------------------------------------------
  
错误: StandardWrapperValve[action]: Servlet.service() for servlet action threw exception
  
javax.servlet.jsp.JspException: Cannot retrieve mapping for action /settlementTypeManage
  
或者:       type Status report      message Servlet action is not available      description The requested resource (Servlet action is not available) is not available.
  
原因:  同 上
  
------------------------------------------
  
错误StandardWrapperValve[jsp]: Servlet.service() for servlet jsp threw exceptionjava.lang.ClassNotFoundException: org.apache.struts.taglib.bean.CookieTei界面错误具体描述: 
  
org.apache.jasper.JasperException: Failed to load or instantiate TagExtraInfo class: org.apache.struts.taglib.bean.CookieTei
  
原因与解决:     <方案一>你的"html:"开头的标签没有放在一个<html:form>中       <方案二>重新启动你的应用服务器,自动就没有这个问题