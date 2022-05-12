---
title: JDBC
author: "-"
date: 2012-03-27T08:05:36+00:00
url: jdbc
categories:
  - DataBase
tags:$
  - reprint
---
## JDBC

JDBC 是阻塞的、同步的

jdbc (java database connection) 就是java数据库链接的api，是java标准类库的扩展，用它可以应用sql访问数据库，完成对数据库的查找，更新。
  
与其它数据库编程环境相比，jdbc有java语言的特性，使用jdbc开发的程序可以跨平台运行，而且不受数据库供应商的限制。

为什么不受数据库供应商的限制呢？

就在于jdbc的设计。
  
一、sun公司为sql访问数据库提供一套"纯"java api；
  
二、同时提供一个驱动管理器，以允许第三方驱动程序可以链接到特定的数据库，这样数据库供应商就可以提供自己的驱动程序，并插入到驱动管理器中，关键是所有的驱动程序都必须满足驱动管理器api提出的要求。
  
三、需要一套简单的机制，以使得第三方驱动程序可以向驱动管理器注册。

### jdbc的典型用法
在传统的客户服务器模式中， 通常在服务器端配置数据库，jdbc驱动程序部署在客户。发展到后来的三层 ， 甚至更高层的应用模式时，客户端不直接调用数据库，而是调用服务器上的中间层，再由中间层完成数据库查询操作。这种三层模式的优点是: 它将可视化表示 (位于客户端) 从业务逻辑 (中间件层) 和原始数据 (位于数据库) 中分离出来。因此，我们就可以从不同的客户端，如java应用，applet或web表单，访问相通的数据库和相通的业务规则。
  
客户端和中间层之间的通信可以通过http (web浏览器用作客户端时) ，rmi (当使用应用或applet) 或其他机制来完成。jdbc负责在中间层和后台数据库之间进行通讯。
  
JDBC (Java Data Base Connectivity,java数据库连接) 是一种用于执行SQL语句的Java API，可以为多种关系数据库提供统一访问，它由一组用Java语言编写的类和接口组成。JDBC为工具/数据库开发人员提供了一个标准的API，据此可以构建更高级的工具和接口，使数据库开发人员能够用纯 Java API 编写数据库应用程序，同时，JDBC也是个商标名。

有了JDBC，向各种关系数据发送SQL语句就是一件很容易的事。换言之，有了JDBC API，就不必为访问Sybase数据库专门写一个程序，为访问Oracle数据库又专门写一个程序，或为访问Informix数据库又编写另一个程序等等，程序员只需用JDBC API写一个程序就够了，它可向相应数据库发送SQL调用。同时，将Java语言和JDBC结合起来使程序员不必为不同的平台编写不同的应用程序，只须写一遍程序就可以让它在任何平台上运行，这也是Java语言"编写一次，处处运行"的优势。

Java数据库连接体系结构是用于Java应用程序连接数据库的标准方法。JDBC对Java程序员而言是API，对实现与数据库连接的服务提供商而言是接口模型。作为API，JDBC为程序开发提供标准的接口，并为数据库厂商及第三方中间件厂商实现与数据库的连接提供了标准方法。JDBC使用已有的SQL标准并支持与其它数据库连接标准，如ODBC之间的桥接。JDBC实现了所有这些面向标准的目标并且具有简单、严格类型定义且高性能实现的接口。
Java 具有坚固、安全、易于使用、易于理解和可从网络上自动下载等特性，是编写数据库应用程序的杰出语言。所需要的只是 Java应用程序与各种不同数据库之间进行对话的方法。而 JDBC 正是作为此种用途的机制。

  
JDBC 扩展了 Java 的功能。例如，用 Java 和 JDBC API 可以发布含有 applet 的网页，而该 applet 使用的信息可能来自远程数据库。企业也可以用 JDBC 通过 Intranet 将所有职员连到一个或多个内部数据库中 (即使这些职员所用的计算机有 Windows、 Macintosh 和UNIX 等各种不同的操作系统) 。随着越来越多的程序员开始使用Java 编程语言，对从 Java 中便捷地访问数据库的要求也在日益增加。
  
  
  
MIS 管理员们都喜欢 Java 和 JDBC 的结合，因为它使信息传播变得容易和经济。企业可继续使用它们安装好的数据库，并能便捷地存取信息，即使这些信息是储存在不同数据库管理系统上。新程序的开发期很短。安装和版本控制将大为简化。程序员可只编写一遍应用程序或只更新一次，然后将它放到服务器上，随后任何人就都可得到最新版本的应用程序。对于商务上的销售信息服务， Java 和JDBC 可为外部客户提供获取信息更新的更好方法。
  
  
  
简单地说，JDBC 可做三件事: 与数据库建立连接、发送 操作数据库的语句并处理结果。下列代码片段给出了以上三步的基本示例: 
  
  
```java
 Connection con = DriverManager.getConnection("jdbc:odbc:wombat","login","password");
 Statement stmt = con.createStatement();
 ResultSet rs = stmt.executeQuery("SELECT a, b, c FROM Table1");
 while (rs.next()) {
 int x = rs.getInt("a");
 String s = rs.getString("b");
 float f = rs.getFloat("c");
 }
 ```
  
  
上述代码对基于JDBC的数据库访问做了经典的总结，当然，在本小节的后续部分会对它做详尽的分析讲解。
  
  
  
API
  
  
JDBC 是个"低级"接口，也就是说，它用于直接调用 SQL 命令。在这方面它的功能极佳，并比其它的数据库连接 API 易于使用，但它同时也被设计为一种基础接口，在它之上可以建立高级接口和工具。高级接口是"对用户友好的"接口，它使用的是一种更易理解和更为方便的 API，这种API在幕后被转换为诸如 JDBC 这样的低级接口。

在关系数据库的"对象/关系"映射中，表中的每行对应于类的一个实例，而每列的值对应于该实例的一个属性。于是，程序员可直接对 Java 对象进行操作；存取数据所需的 SQL 调用将在"掩盖下"自动生成。此外还可提供更复杂的映射，例如将多个表中的行结合进一个 Java 类中。

随着人们对 JDBC 的兴趣日益增涨，越来越多的开发人员一直在使用基于 JDBC 的工具，以使程序的编写更加容易。程序员也一直在编写力图使最终用户对数据库的访问变得更为简单的应用程序。例如应用程序可提供一个选择数据库任务的菜单。任务被选定后，应用程序将给出提示及空白供填写执行选定任务所需的信息。所需信息输入应用程序将自动调用所需的 SQL 命令。在这样一种程序的协助下，即使用户根本不懂 SQL 的语法，也可以执行数据库任务。
  
目前，Microsoft 的 ODBC API 可能是使用最广的、用于访问关系数据库的编程接口。它能在几乎所有平台上连接几乎所有的数据库。为什么 Java 不使用 ODBC？对这个问题的回答是: Java 可以使用 ODBC，但最好是在 JDBC 的帮助下以 JDBC-ODBC 桥的形式使用，这一点我们稍后再说。现在的问题已变成: "为什么需要 JDBC"？答案是显然的: ODBC 不适合直接在 Java 中使用，因为它使用 C 语言接口。从Java 调用本地 C 代码在安全性、实现、坚固性和程序的自动移植性方面都有许多缺点。从 ODBC C API 到 Java API 的字面翻译是不可取的。例如，Java 没有指针，而 ODBC 却对指针用得很广泛 (包括很容易出错的指针"void *") 。您可以将 JDBC 想象成被转换为面向对象接口的 ODBC，而面向对象的接口对 Java 程序员来说较易于接受。

ODBC 很难学。它把简单和高级功能混在一起，而且即使对于简单的查询，其选项也极为复杂。相反，JDBC 尽量保证简单功能的简便性，而同时在必要时允许使用高级功能。启用"纯 Java "机制需要象 JDBC 这样的 Java API。如果使用ODBC，就必须手动地将 ODBC 驱动程序管理器和驱动程序安装在每台客户机上。如果完全用 Java 编写 JDBC 驱动程序则 JDBC 代码在所有 Java 平台上 (从网络计算机到大型机) 都可以自 动安装、移植并保证安全性。

总之，JDBC API 对于基本的 SQL 抽象和概念是一种自然的 Java 接口。它建立在 ODBC 上而不是从零开始。因此，熟悉 ODBC 的程序员将发现 JDBC 很容易使用。JDBC 保留了 ODBC 的基本设计特征；事实上，两种接口都基于 X/Open SQL CLI (调用级接口) 。它们之间最大的区别在于: JDBC 以 Java 风格与优点为基础并进行优化，因此更加易于使用。

目前，Microsoft 又引进了 ODBC 之外的新 API: RDO、 ADO 和OLE DB。这些设计在许多方面与 JDBC 是相同的，即它们都是面向对象的数据库接口且基于可在 ODBC 上实现的类。但在这些接口中，我们未看见有特别的功能使我们要转而选择它们来替代 ODBC，尤其是在 ODBC 驱动程序已建立起较为完善的市场的情况下。它们最多也就是在 ODBC 上加了一种装饰而已。

JDBC API 既支持数据库访问的两层模型 (C/S) ，同时也支持三层模型 (B/S) 。在两层模型中，Java applet或应用程序将直接与数据库进行对话。这将需要一个JDBC驱动程序来与所访问的特定数据库管理系统进行 通讯。用户的SQL语句被送往数据库中，而其结果将被送回给用户。数据库可以位于另一台计算机上，用户通过网络连接到上面。这就叫做客户机/服务器配置，其中用户的计算机为客户机，提供数据库的计算机为服务器。网络可以是 Intranet (它可将公司职员连接起来) ，也可以是 Internet。

在三层模型中，命令先是被发送到服务的"中间层"，然后由它将SQL 语句发送给数据库。数据库对 SQL 语句进行处理并将结果送回到中间层，中间层再将结果送回给用户。MIS 主管们都发现三层模型很吸引人，因为可用中间层来控制对公司数据的访问和可作的的更新的种类。中间层的另一个好处是，用户可以利用易于使用的高级API，而中间层将把它转换为相应的低级调用。最后，许多情况下三层结构可提供一些性能上的好处。

到目前为止，中间层通常都用 C 或 C++ 这类语言来编写，这些语言执行速度较快。然而，随着最优化编译器 (它把 Java 字节代码转换为高效的特定于机器的代码) 的引入，用 Java 来实现中间层将变得越来越实际。这将是一个很大的进步，它使人们可以充分利用 Java 的诸多优点 (如坚固、多线程和安全等特征) 。JDBC 对于从Java的中间层来访问数据库非常重要。

结构化查询语言  (SQL)  是访问关系数据库的标准语言。困难之处在于: 虽然大多数的 DBMS  (数据库管理系统) 对其基本功能都使用了标准形式的 SQL，但它们却不符合最近为更高级的功能定义的标准 SQL 语法或语义。例如，并非所有的数据库都支持储存程序或外部连接，那些支持这一功能的数据库又相互不一致。人们希望 SQL 中真正标准的那部份能够进行扩展以包括越来越多的功能。但同时 JDBC API 又必须支持现有的 SQL。

JDBC API 解决这个问题的一种方法是允许将任何查询字符串一直传到所涉及的 DBMS 驱动程序上。这意味着应用程序可以使用任意多的 SQL 功能，但它必须冒这样的风险: 有可能在某些 DBMS 上出错。事实上，应用程序查询甚至不一定要是 SQL，或者说它可以是个为特定的 DBMS 设计的 SQL 的专用派生物 (例如，文档或图象查询) 。

JDBC 处理 SQL 一致性问题的第二种方法是提供 ODBC 风格的转义子句，这将在后续部分中讨论。转义语法为几个常见的 SQL 分歧提供了一种标准的 JDBC 语法。例如，对日期文字和已储存过程的调用都有转义语法。

对于复杂的应用程序，JDBC 用第三种方法来处理 SQL 的一致性问题它利用 DatabaseMetaData 接口来提供关于 DBMS 的描述性信息，从而使应用程序能适应每个 DBMS 的要求和功能。

由于 JDBC API 将用作开发高级数据库访问工具和 API 的基础 API，因此它还必须注意其所有上层建筑的一致性。"符合JDBC标准TM" 代表用户可依赖的 JDBC 功能的标准级别。要使用这一说明，驱动程序至少必须支持 ANSI SQL-2 Entry Level (ANSI SQL-2 代表美国国家标准局 1992 年所采用的标准。Entry Level代表SQL功能的特定清单) 。驱动程序开发人员可用 JDBC API 所带的测试工具包来确定他们的驱动程序是否符合这些标准。

"符合 JDBC 标准TM" 表示提供者的 JDBC 实现已经通过了JavaSoft 提供的一致性测试。这些一致性测试将检查 JDBC API中定义的所有类和方法是否都存在，并尽可能地检查程序是否具有SQL Entry Level 功能。当然，这些测试并不完全，而且 JavaSoft 目前也无意对各提供者的实现进行标级。但这种一致性定义的确可对JDBC实现提供一定的可信度。随着越来越多的数据库提供者、连接提供者、Internet 提供者和应用程序编程员对 JDBC API 的接受，JDBC 也正迅速成为 Java 数据库访问的标准。

装载驱动程序

你需要做的第一事情是你与想要使用的 DBMS 建立一个连接。这包含 2 个步骤: 装载驱动程序并建立连接。

装载驱动程序只需要非常简单的一行代码。例如，你想要使用 JDBC-ODBC 桥驱动程序, 可以用下列代码装载它: 


Class.forName("sun.jdbc.odbc.JdbcOdbcDriver");


你的驱动程序文档将告诉你应该使用的类名。例如， 如果类名是 jdbc.DriverXYZ ，你将用代码以下的代码装载驱动程序: 


Class.forName("jdbc.DriverXYZ");


你不需要创建一个驱动程序类的实例并且用 DriverManager 登记它，因为调用 Class.forName 将自动加载驱动程序类。如果你曾自己创建实例，你将创建一个不必要的副本，但它不会带来什么坏处。


加载 Driver 类后，它们即可用来与数据库建立连接。


建立连接


第二步就是用适当的驱动程序类与 DBMS 建立一个连接。下列代码是一般的做法: 


Connection con = DriverManager.getConnection(url, "myLogin", "myPassword");


这个步骤也非常简单，最难的是怎么提供 url。如果你正在使用 JDBC-ODBC 桥， JDBC URL 将以 jdbc:odbc 开始: 余下 URL 通常是你的数据源名字或数据库系统。因此，假设你正在使用 ODBC 存取一个叫 "Fred" 的 ODBC 数据源，你的 JDBC URL 是 jdbc:odbc:Fred 。把 "myLogin" 及 "myPassword" 替换为你登陆 DBMS 的用户名及口令。如果你登陆数据库系统的用户名为 "Fernanda" 口令为 "J8"，只需下面的 2 行代码就可以建立一个连接: 


String url = "jdbc:odbc:Fred";


Connection con = DriverManager.getConnection(url,"Fernanda", "J8");


如果你使用的是第三方开发了的 JDBC驱动程序，文档将告诉你该使用什么 subprotocol， 就是在 JDBC URL 中放在 jdbc 后面的部分。例如, 如果驱动程序开发者注册了 acme 作为 subprotocol， JDBC URL 的第一和第二部分将是 jdbc:acme。驱动程序文档也会告诉你余下 JDBC URL 的格式。JDBC URL 最后一部分提供了定位数据库的信息。


如果你装载的驱动程序识别了提供给 DriverManager.getConnection 的 JDBC URL ，那个驱动程序将根据 JDBC URL 建立一个到指定 DBMS 的连接。正如名称所示，DriverManager 类在幕后为你管理建立连接的所有细节。除非你是正在写驱动程序，你可能无需使用此类的其它任何方法，一般程序员需要在此类中直接使用的唯一方法是 DriverManager.getConnection。



DriverManager.getConnection 方法返回一个打开的连接，你可以使用此连接创建 JDBC statements 并发送 SQL 语句到数据库。在前面的例子里，con 对象是一个打开的连接，并且我们要在以后的例子里使用它。



创建表


首先，我们在我们的示例数据库创建其中一张表 COFFEES，包含在咖啡店所卖咖啡的必要的信息，包括咖啡名字，他们的价格，本星期卖了多少磅及迄今为止卖的数目。关于 COFFEES 表我们以后会详细描述，如下: 



我们写了创建 COFFEES 表的 SQL 语句。现在我们在它外面加上引号 (使它成为字符串) ，并且字符串赋值给变量 createTableCoffees，在以后的 JDBC 代码中我们可以使用此变量。正如看到的，DBMS 并不在意分行，但对 Java 语言来，String 对象分行是通不过编译的。因而，我们可以用加号 (+) 把每一行的串连接。



String createTableCoffees = "CREATE TABLE COFFEES " +



"(COF_NAME VARCHAR(32), SUP_ID INTEGER, PRICE FLOAT, " +



"SALES INTEGER, TOTAL INTEGER)";



我们在 CREATE TABLE 语句中使用的数据类型是通用的 SQL 类型 (也称 JDBC 类型) 它们在类 java.sql.Types 中定义。DBMSs 通常使用这些标准的类型，因此，当你要尝试一些 JDBC 应用程序时，你可以直接使用 CreateCoffees.java 应用程序，它使用了 CREATE TABLE 语句。如果你的 DBMS 使用了它的自己的本地的类型名字，我们为你供应其它的应用程序，我们将在后面详细解释。



在运用任何应用程序前，当然，我们将让你了解 JDBC 的基础。


创建对象


Statement 对象用于把 SQL 语句发送到 DBMS 。你只须简单地创建一个 Statement 对象并且然后执行它，使用适当的方法执行你发送的 SQL 语句。对 SELECT 语句来说，可以使用 executeQuery。要创建或修改表的语句，使用的方法是 executeUpdate。



需要一个活跃的连接的来创建 Statement 对象的实例。在下面的例子中，我们使用我们的 Connection 对象 con 创建 Statement 对象 stmt: 



Statement stmt = con.createStatement();



到此 stmt 已经存在了，但它还没有把 SQL 语句传递到 DBMS。我们需要提供 SQL 语句作为参数提供给我们使用的 Statement 的方法。例如，在下面的代码片段里，我们使用上面例子中的 SQL 语句作为 executeUpdate 的参数: 



stmt.executeUpdate("CREATE TABLE COFFEES " +



"(COF_NAME VARCHAR(32), SUP_ID INTEGER, PRICE FLOAT, " +



"SALES INTEGER, TOTAL INTEGER)");



因为我们已经把 SQL 语句赋给了 createTableCoffees 变量，我们可以如下方式书写代码: 



stmt.executeUpdate(createTableCoffees);


执行语句


我们使用 executeUpdate 方法是因为在 createTableCoffees 中的 SQL 语句是 DDL  (数据定义语言) 语句。创建表，改变表，删除表都是 DDL 语句的例子，要用 executeUpdate 方法来执行。你也可以从它的名字里看出，方法 executeUpdate 也被用于执行更新表 SQL 语句。实际上，相对于创建表来说，executeUpdate 用于更新表的时间更多，因为表只需要创建一次，但经常被更新。



被使用最多的执行 SQL 语句的方法是 executeQuery。这个方法被用来执行 SELECT 语句，它几乎是使用最多的 SQL 语句。马上你将看到如何使用这个方法。


在表中输入数据


我们已经显示了如何通过指定列名、数据类型来创建表 COFFEES，但是这仅仅建立表的结构。表还没有任何数据。我们将次输入一行数据到表中，提供每列的信息，注意插入的数据显示顺序跟表创建时候是一样的，既缺省顺序。



下列代码插入一个行数据，COF_NAME 的值为 Colombian，SUP_ID 为 101，PRICE 为 7.99，SALES 0，TOTAL 0。就象创建 COFFEES 表一样，我们创建一 Statement 对象，并执行 executeUpdate 方法。



因为 SQL 语句一行显示不下，因此我们把它分为两行，并用加号 (+) 相连。特别要注意的是，在 COFFEES 和 VALUES 之间要有空格。这个空格必须在引号之内并且要在 COFFEES 跟 VALUES 之间；没有这个空格，SQL 语句将被错误地被读作为 "INSERT INTO COFFEESVALUES ..."，并且 DBMS 将寻找表 COFFEESVALUES。还要注意的是在 coffee name 上我们使用了单引号。



Statement stmt = con.createStatement();



stmt.executeUpdate(



"INSERT INTO COFFEES " +



"VALUES ('Colombian', 101, 7.99, 0, 0)");



下面的代码把第二行插入到表 COFFEES 中。我们可以在使用 Statement 对象而无须为每次执行创建一个新的。



stmt.executeUpdate("INSERT INTO COFFEES " +



"VALUES ('French_Roast', 49, 8.99, 0, 0)");



剩下行的数据如下: 



stmt.executeUpdate("INSERT INTO COFFEES " +



"VALUES ('Espresso', 150, 9.99, 0, 0)");



stmt.executeUpdate("INSERT INTO COFFEES " +



"VALUES ('Colombian_Decaf', 101, 8.99, 0, 0)");



stmt.executeUpdate("INSERT INTO COFFEES " +



"VALUES ('French_Roast_Decaf', 49, 9.99, 0, 0)");


从表中取得数据


既然表 COFFEES 中已经有数据了，我们就可以写一个 SELECT 语句来取得这些值。下面的 SQL 语句中星号 (*) 表示选择所有的列。因为没有用 WHERE 子句来限制所选的行，因此下面的 SQL 语句选择的是整个表。



SELECT * FROM COFFEES



结果是整个表的数据，如下: 



COF_NAME SUP_ID PRICE SALES TOTAL



----- -- -- -- --



Colombian 101 7.99 0 0



French_Roast 49 8.99 0 0



Espresso 150 9.99 0 0



Colombian_Decaf 101 8.99 0 0



French_Roast_Decaf 49 9.99 0 0



如果你直接在数据库系统里输入 SQL 查询语句，你将在你的终端上看到如上的结果。当我们通过一个 Java 应用程序存取一个数据库时，正如我们马上要做的一样，我们需要检索结果以便我们能使用他们。你将在下一节看到如何实现。



这是 SELECT 语句的另一个例子，这将得到咖啡及其各自每磅单价的列表。



SELECT COF_NAME, PRICE FROM COFFEES



查询的结果集将具有如下形式: 



COF_NAME PRICE



--- ---- --



Colombian 7.99



French_Roast 8.99



Espresso 9.99



Colombian_Decaf 8.99



French_Roast_Decaf 9.99



上面 SELECT 语句取得了所有咖啡的名字及价格。而下面的 SELECT 语句限制那些每磅价格低于 .00 的咖啡才被选择。



SELECT COF_NAME, PRICE



FROM COFFEES



WHERE PRICE < 9.00



结果集将具有如下形式: 



COF_NAME PRICE



--- --- --



Colombian 7.99



French_Roast 8.99



Colombian Decaf 8.99


建立JDBC


综述


Connection 对象代表与数据库的连接。连接过程包括所执行的 SQL 语句和在该连接上所返回的结果。一个应用程序可与单个数据库有一个或多个连接，或者可与许多数据库有连接。


打开连接


与数据库建立连接的标准方法是调用DriverManager.getConnection方法。该方法接受含有某个URL的字符串。DriverManager类 (即所谓的JDBC管理层) 将尝试找到可与那个URL所代表的数据库进行连接的驱动程序。DriverManager类存有已注册的Driver类的清单。当调用方法getConnection时，它将检查清单中的每个驱动程序，直到找到可与URL中指定的数据库进行连接的驱动程序为止。Driver的方法connect使用这个URL来建立实际的连接。



用户可绕过JDBC管理层直接调用Driver方法。这在以下特殊情况下将很有用: 当两个驱动器可同时连接到数据库中，而用户需要明确地选用其中特定的驱动器。但一般情况下，让DriverManager类处理打开连接这种事将更为简单。



下述代码显示如何打开一个与位于URL"jdbc: odbc: wombat"的数据库的连接。所用的用户标识符为"freely"，口令为"ec": 



String url = "jdbc: odbc: wombat"； Connection con = DriverManager.getConnection (url， "freely"， "ec") ；


一般用法的URL


由于URL常引起混淆，我们将先对一般URL作简单说明，然后再讨论JDBCURL。URL (统一资源定位符) 提供在Internet上定位资源所需的信息。可将它想象为一个地址。URL的第一部份指定了访问信息所用的协议，后面总是跟着冒号。常用的协议有"ftp" (代表"文件传输协议") 和"http" (代表"超文本传输协议") 。如果协议是"file"，表示资源是在某个本地文件系统上而非在Internet上 (下例用于表示我们所描述的部分；它并非URL的组成部分) 。



URL的其余部份 (冒号后面的) 给出了数据资源所处位置的有关信息。如果协议是file，则URL的其余部份是文件的路径。对于ftp和http协议，URL的其余部份标识了主机并可选地给出某个更详尽的地址路径。例如，以下是JavaSoft主页的URL。该URL只标识了主机，从该主页开始浏览，就可以进到许多其它的网页中，其中之一就是JDBC主页。


JDBC URL


JDBC URL提供了一种标识数据库的方法，可以使相应的驱动程序能识别该数据库并与之建立连接。实际上，驱动程序编程员将决定用什么JDBC URL来标识特定的驱动程序。用户不必关心如何来形成JDBC URL；他们只须使用与所用的驱动程序一起提供的URL即可。JDBC的作用是提供某些约定，驱动程序编程员在构造他们的JDBC URL时应该遵循这些约定。



由于JDBC URL要与各种不同的驱动程序一起使用，因此这些约定应非常灵活。首先，它们应允许不同的驱动程序使用不同的方案来命名数据库。例如，odbc子协议允许 (但并不是要求) URL含有属性值。



其次，JDBC URL应允许驱动程序编程员将一切所需的信息编入其中。这样就可以让要与给定数据库对话的applet打开数据库连接，而无须要求用户去做任何系统管理工作。



最后，JDBC URL应允许某种程度的间接性。也就是说，JDBC URL可指向逻辑主机或数据库名，而这种逻辑主机或数据库名将由网络命名系统动态地转换为实际的名称。这可以使系统管理员不必将特定主机声明为JDBC名称的一部份。网络命名服务 (例如DNS、NIS和DCE) 有多种，而对于使用哪种命名服务并无限制。 JDBC URL的标准语法如下所示。它由三部分组成，各部分间用冒号分隔。



JDBC URL的三个部分可分解如下: 



 (1) jdbc协议: JDBC URL中的协议总是jdbc。



 (2) <子协议>: 驱动程序名或数据库连接机制 (这种机制可由一个或多个驱动程序支持) 的名称。子协议名的典型示例是"odbc"，该名称是为用于指定ODBC风格的数据资源名称的URL专门保留的。例如，为了通过JDBC-ODBC桥来访问某个数据库，可以用如下所示的URL: jdbc: odbc: book。本例中，子协议为"odbc"，子名称"book"是本地ODBC数据资源。如果要用网络命名服务 (这样JDBC URL中的数据库名称不必是实际名称) ，则命名服务可以作为子协议。例如，可用如下所示的URL: jdbc: dcenaming: accounts。本例中，该URL指定了本地DCE命名服务应该将数据库名称"accounts"解析为更为具体的可用于连接真实数据库的名称。



 (3) <子名称>: 种标识数据库的方法。子名称可以依不同的子协议而变化。它还可以有子名称的子名称 (含有驱动程序编程员所选的任何内部语法) 。使用子名称的目的是为定位数据库提供足够的信息。前例中，因为ODBC将提供其余部份的信息，因此用"book"就已足够。然而，位于远程服务器上的数据库需要更多的信息。例如，如果数据库是通过Internet来访问的，则在JDBC URL中应将网络地址作为子名称的一部份包括进去，且必须遵循如下所示的标准URL命名约定: //主机名: 端口/子协议。



假设"dbnet"是个用于将某个主机连接到Internet上的协议，则JDBC URL应为: jdbc: dbnet: //wombat: 356/fred。


"odbc"子协议


子协议odbc是一种特殊情况。它是为用于指定ODBC风格的数据资源名称的URL而保留的，并具有下列特性: 允许在子名称 (数据资源名称) 后面指定任意多个属性值。odbc子协议的完整语法为: 



jdbc: odbc: <数据资源名称>【；<属性名>=<属性值>】，因此，以下都是合法的jdbc: odbc名称:  jdbc: odbc: qeor7 jdbc: odbc: wombat jdbc: odbc: wombat；CacheSize=20；ExtensionCase=LOWER jdbc: odbc: qeora；UID=kgh；PWD=fooey



1. 注??称以将之用作JDBC URL的子协议名。当DriverManager类将此名称加到已注册的驱动程序清单中时，为之保留该名称的驱动程序应能识别该名称并与它所标识的数据库建立连接。例如，odbc是为JDBC-ODBC桥而保留的。假设有个Miracle公司，它可能会将"miracle"注册为连接到其Miracle DBMS上的JDBC驱动程序的子协议，从而使其他人都无法使用这个名称。



JavaSoft目前作为非正式代理负责注册JDBC子协议名称。


发送SQL语句


连接一旦建立，就可用来向它所涉及的数据库传送SQL语句。JDBC对可被发送的SQL语句类型不加任何限制。这就提供了很大的灵活性，即允许使用特定的数据库语句或甚至于非SQL语句。然而，它要求用户自己负责确保所涉及的数据库可以处理所发送的SQL语句，否则将自食其果。例如，如果某个应用程序试图向不支持储存程序的DBMS发送储存程序调用，就会失败并将抛出异常。JDBC要求驱动程序应至少能提供ANSI SQL-2 Entry Level功能才可算是符合JDBC标准TM的。这意味着用户至少可信赖这一标准级别的功能。



JDBC提供了三个类，用于向数据库发送SQL语句。Connection接口中的三个方法可用于创建这些类的实例。下面列出这些类及其创建方法: 



 (1) Statement: 由方法createStatement所创建。Statement对象用于发送简单的SQL语句。



 (2) PreparedStatement: 由方法prepareStatement所创建。PreparedStatement对象用于发送带有一个或多个输入参数 (IN参数) 的SQL语句。PreparedStatement拥有一组方法，用于设置IN参数的值。执行语句时，这些IN参数将被送到数据库中。PreparedStatement的实例扩展了Statement，因此它们都包括了Statement的方法。PreparedStatement对象有可能比Statement对象的效率更高，因为它已被预编译过并存放在那以供将来使用。



 (3) CallableStatement: 由方法prepareCall所创建。CallableStatement对象用于执行SQL储存程序─一组可通过名称来调用 (就象函数的调用那样) 的SQL语句。CallableStatement对象从PreparedStatement中继承了用于处理IN参数的方法，而且还增加了用于处理OUT参数和INOUT参数的方法。



不过通常来说createStatement方法用于简单的SQL语句 (不带参数) 、prepareStatement方法用于带一个或多个IN参数的SQL语句或经常被执行的简单SQL语句，而prepareCall方法用于调用已储存过程。


事务


事务由一个或多个这样的语句组成: 这些语句已被执行、完成并被提交或还原。当调用方法commit或rollback时，当前事务即告就结束，另一个事务随即开始。缺省情况下，新连接将处于自动提交模式。也就是说，当执行完语句后，将自动对那个语句调用commit方法。这种情况下，由于每个语句都是被单独提交的，因此一个事务只由一个语句组成。如果禁用自动提交模式，事务将要等到commit或rollback方法被显式调用时才结束，因此它将包括上一次调用commit或rollback方法以来所有执行过的语句。对于第二种情况，事务中的所有语句将作为组来提交或还原。



方法commit使SQL语句对数据库所做的任何更改成为永久性的，它还将释放事务持有的全部锁。而方法rollback将弃去那些更改。有时用户在另一个更改生效前不想让此更改生效。这可通过禁用自动提交并将两个更新组合在一个事务中来达到。如果两个更新都是成功，则调用commit方法，从而使两个更新结果成为永久性的；如果其中之一或两个更新都失败了，则调用rollback方法，以将值恢复为进行更新之前的值。



大多数JDBC驱动程序都支持事务。事实上，符合JDBC的驱动程序必须支持事务。DatabaseMetaData给出的信息描述DBMS所提供的事务支持水平。


事务隔离级别


如果DBMS支持事务处理，它必须有某种途径来管理两个事务同时对一个数据库进行操作时可能发生的冲突。用户可指定事务隔离级别，以指明DBMS应该花多大精力来解决潜在冲突。例如，当事务更改了某个值而第二个事务却在该更改被提交或还原前读取该值时该怎么办。



假设第一个事务被还原后，第二个事务所读取的更改值将是无效的，那么是否可允许这种冲突？JDBC用户可用以下代码来指示DBMS允许在值被提交前读取该值 ("dirty读取") ，其中con是当前连接:  con.setTransactionIsolation (TRANSACTION_READ_UNCOMMITTED) ；



事务隔离级别越高，为避免冲突所花的精力也就越多。Connection接口定义了五级，其中最低级别指定了根本就不支持事务，而最高级别则指定当事务在对某个数据库进行操作时，任何其它事务不得对那个事务正在读取的数据进行任何更改。通常，隔离级别越高，应用程序执行的速度也就越慢 (由于用于锁定的资源耗费增加了，而用户间的并发操作减少了) 。在决定采用什么隔离级别时，开发人员必须在性能需求和数据一致性需求之间进行权衡。当然，实际所能支持的级别取决于所涉及的DBMS的功能。



当创建Connection对象时，其事务隔离级别取决于驱动程序，但通常是所涉及的数据库的缺省值。用户可通过调用setIsolationLevel方法来更改事务隔离级别。新的级别将在该连接过程的剩余时间内生效。要想只改变一个事务的事务隔离级别，必须在该事务开始前进行设置，并在该事务结束后进行复位。我们不提倡在事务的中途对事务隔离级别进行更改，因为这将立即触发commit方法的调用，使在此之前所作的任何更改变成永久性的。



综述


DriverManager 类是 JDBC 的管理层，作用于用户和驱动程序之间。它跟踪可用的驱动程序，并在数据库和相应驱动程序之间建立连接。另外，DriverManager类也处理诸如驱动程序登录时间限制及登录和跟踪消息的显示等事务。 对于简单的应用程序，一般程序员需要在此类中直接使用的唯一方法是DriverManager.getConnection。正如名称所示，该方法将建立与数据库的连接。JDBC允许用户调用DriverManager的方法getDriver、getDrivers和registerDriver及Driver的方法connect。但多数情况下，让DriverManager类管理建立连接的细节为上策。


跟踪可用驱动程序


DriverManager类包含一列Driver类，它们已通过调用方法DriverManager.registerDriver对自己进行了注册。所有Driver类都必须包含有一个静态部分。它创建该类的实例，然后在加载该实例时DriverManager类进行注册。这样，用户正常情况下将不会直接调用DriverManager.registerDriver；而是在加载驱动程序时由驱动程序自动调用。加载Driver类，然后自动在DriverManager中注册的方式有两种: 



 (1) 调用方法Class.forName



这将显式地加载驱动程序类。由于这与外部设置无关，因此推荐使用这种加载驱动程序的方法。以下代码加载类acme.db.Driver: Class.forName ("acme.db.Driver") 。



如果将acme.db.Driver编写为加载时创建实例，并调用以该实例为参数的DriverManager.registerDriver (本该如此) ，则它在DriverManager的驱动程序列表中，并可用于创建连接。



 (2) 将驱动程序添加到Java.lang.System的属性jdbc.drivers中



这是一个由DriverManager类加载的驱动程序类名的列表，由冒号分隔: 初始化DriverManager类时，它搜索系统属性jdbc.drivers，如果用户已输入了一个或多个驱动程序，则DriverManager类将试图加载它们。以下代码说明程序员如何在~/.hotJava/properties中输入三个驱动程序类 (启动时，HotJava将ivers=foo.bah.Driver: wombat.sql.Driver: bad.test.ourDriver；



对DriverManager方法的第一次调用将自动加载这些驱动程序类。注意: 加载驱动程序的第二种方法需要持久的预设环境。如果对这一点不能保证，则调用方法Class.forName显式地加载每个驱动程序就显得更为安全。这也是引入特定驱动程序的方法，因为一旦DriverManager类被初始化，它将不再检查jdbc.drivers属性列表。



在以上两种情况中，新加载的Driver类都要通过调用DriverManager.registerDriver类进行自我注册。如上所述，加载类时将自动执行这一过程。



由于安全方面的原因，JDBC管理层将跟踪哪个类加载器提供哪个驱动程序。这样，当DriverManager类打开连接时，它仅使用本地文件系统或与发出连接请求的代码相同的类加载器提供的驱动程序。


建立连接


加载Driver类并在DriverManager类中注册后，它们即可用来与数据库建立连接。当调用DriverManager.getConnection方法发出连接请求时，DriverManager将检查每个驱动程序，查看它是否可以建立连接。



有时可能有多个JDBC驱动程序可以与给定的URL连接。例如，与给定远程数据库连接时，可以使用JDBC-ODBC桥驱动程序、JDBC到通用网络协议驱动程序或数据库厂商提供的驱动程序。在这种情况下测试驱动程序的顺序至关重要，因为DriverManager将使用它所找到的第一个可以成功连接到给定URL的驱动程序。



首先DriverManager试图按注册的顺序使用每个驱动程序 (jdbc.drivers中列出的驱动程序总是先注册) 。它将跳过代码不可信任的驱动程序，除非加载它们的源与试图打开连接的代码的源相同。它通过轮流在每个驱动程序上调用方法Driver.connect，并向它们传递用户开始传递给方法DriverManager.getConnection的URL来对驱动程序进行测试，然后连接第一个认出该URL的驱动程序。这种方法初看起来效率不高，但由于不可能同时加载数十个驱动程序，因此每次连接实际只需几个过程调用和字符串比较。



以下代码是通常情况下用驱动程序 (例如JDBC-ODBC桥驱动程序) 建立连接所需所有步骤的示例: 



Class.forName ("sun.jdbc.odbc.JdbcOdbcDriver") ；//加载驱动程序 String url = "jdbc: odbc: fred"； DriverManager.getConnection (url，"userID"，"passwd") ；




发送语句


综述


Statement对象用于将SQL语句发送到数据库中。实际上有三种Statement对象，它们都作为在给定连接上执行SQL语句的包容器: Statement、PreparedStatement (它从Statement继承而来) 和CallableStatement (它从PreparedStatement继承而来) 。它们都专用于发送特定类型的SQL语句: Statement对象用于执行不带参数的简单SQL语句；PreparedStatement对象用于执行带或不带IN参数的预编译SQL语句；CallableStatement对象用于执行对数据库已存储过程的调用。 Statement接口提供了执行语句和获取结果的基本方法；PreparedStatement接口添加了处理IN参数的方法；而CallableStatement添加了处理OUT参数的方法。


创建Statement对象


建立了到特定数据库的连接之后，就可用该连接发送SQL语句。Statement对象用Connection的方法createStatement创建，如下列代码片段中所示: 



Connection con = DriverManager.getConnection (url，"sunny"，"") ； Statement stmt = con.createStatement () ；



为了执行Statement对象，被发送到数据库的SQL语句将被作为参数提供给Statement的方法: 



ResultSet rs = stmt.executeQuery ("SELECT a，b，c FROM Table2") ；


使用Statement对象执行语句


Statement接口提供了三种执行SQL语句的方法: executeQuery、executeUpdate和execute。使用哪一个方法由SQL语句所产生的内容决定。



方法executeQuery用于产生单个结果集的语句，例如SELECT语句。方法executeUpdate用于执行INSERT、UPDATE或DELETE语句以及SQL DDL (数据定义语言) 语句，例如CREATE TABLE和DROP TABLE。INSERT、UPDATE或DELETE语句的效果是修改表中零行或多行中的一列或多列。executeUpdate的返回值是一个整数，指示受影响的行数 (即更新计数) 。对于CREATE TABLE或DROP TABLE等不操作行的语句，executeUpdate的返回值总为零。



执行语句的所有方法都将关闭所调用的Statement对象的当前打开结果集 (如果存在) 。这意味着在重新执行Statement对象之前，需要完成对当前ResultSet对象的处理。应注意，继承了Statement接口中所有方法的PreparedStatement接口都有自己的executeQuery、executeUpdate和execute方法。Statement对象本身不包含SQL语句，因而必须给Statement.execute方法提供SQL语句作为参数。PreparedStatement对象并不需要SQL语句作为参数提供给这些方法，因为它们已经包含预编译SQL语句。



CallableStatement对象继承这些方法的PreparedStatement形式。对于这些方法的PreparedStatement或CallableStatement版本，使用查询参数将抛出SQLException。


语句完成


当连接处于自动提交模式时，其中所执行的语句在完成时将自动提交或还原。语句在已执行且所有结果返回时，即认为已完成。对于返回一个结果集的executeQuery方法，在检索完ResultSet对象的所有行时该语句完成。对于方法executeUpdate，当它执行时语句即完成。但在少数调用方法execute的情况中，在检索所有结果集或它生成的更新计数之后语句才完成。



有些DBMS将已存储过程中的每条语句视为独立的语句；而另外一些则将整个过程视为一个复合语句。在启用自动提交时，这种差别就变得非常重要，因为它影响什么时候调用commit方法。在前一种情况中，每条语句单独提交；在后一种情况中，所有语句同时提交。


关闭Statement对象


Statement对象将由Java垃圾收集程序自动关闭。而作为一种好的编程风格，应在不需要Statement对象时显式地关闭它们。这将立即释放DBMS资源，有助于避免潜在的内存问题。


使用方法execute


execute方法应该仅在语句能返回多个ResultSet对象、多个更新计数或ResultSet对象与更新计数的组合时使用。当执行某个已存储过程或动态执行未知SQL字符串 (即应用程序程序员在编译时未知) 时，有可能出现多个结果的情况，尽管这种情况很少见。例如，用户可能执行一个已存储过程，并且该已存储过程可执行更新，然后执行选择，再进行更新，再进行选择，等等。通常使用已存储过程的人应知道它所返回的内容。



因为方法execute处理非常规情况，所以获取其结果需要一些特殊处理并不足为怪。例如，假定已知某个过程返回两个结果集，则在使用方法execute执行该过程后，必须调用方法getResultSet获得第一个结果集，然后调用适当的getXXX方法获取其中的值。要获得第二个结果集，需要先调用getMoreResults方法，然后再调用getResultSet方法。如果已知某个过程返回两个更新计数，则首先调用方法getUpdateCount，然后调用getMoreResults，并再次调用getUpdateCount。



对于不知道返回内容，则情况更为复杂。如果结果是ResultSet对象，则方法execute返回true；如果结果是Javaint，则返回false。如果返回int，则意味着结果是更新计数或执行的语句是DL命令。在调用方法execute之后要做的第一件事情是调用getResultSet或getUpdateCount。调用方法getResultSet可以获得两个或多个ResultSet对象中第一个对象；或调用方法getUpdateCount可以获得两>



当SQL语句的结果不是结果集时，则方法getResultSet将返回null。这可能意味着结果是一个更新计数或没有其它结果。在这种情况下，判断null真正含义的唯一方法是调用方法getUpdateCount，它将返回一个整数。这个整数为调用语句所影响的行数；如果为-1则表示结果是结果集或没有结果。如果方法getResultSet已返回null (表示结果不是ResultSet对象) ，则返回值-1表示没有其它结果。也就是说，当下列条件为真时表示没有结果 (或没有其它结果) : 



 ( (stmt.getResultSet () ==null) && (stmt.getUpdateCount () ==-1) ) 



如果已经调用方法getResultSet并处理了它返回的ResultSet对象，则有必要调用方法getMoreResults以确定是否有其它结果集或更新计数。如果getMoreResults返回true，则需要再次调用getResultSet来检索下一个结果集。如上所述，如果getResultSet返回null，则需要调用getUpdateCount来检查null是表示结果为更新计数还是表示没有其它结果。



当getMoreResults返回false时，它表示该SQL语句返回一个更新计数或没有其它结果。因此需要调用方法getUpdateCount来检查它是哪一种情况。在这种情况下，当下列条件为真时表示没有其它结果: 



 ( (stmt.getMoreResults () ==false) && (stmt.getUpdateCount () ==-1) ) 


访问


通用数据库Bean设计


本实例中对数据库连接和执行SQL语句等通用数据库操作进行了封装，通过实现DBConnBean和DBQueryBean两个JavaBean来完成上述功能。其中DBConnBean负责Java应用程序和数据库的连接；DBQueryBean提供了一组执行标准SQL的功能，可以实现标准SQL完成的所有功能。


数据库表结构


本实例中主要出现了三个数据库表，表名和字段分别如下所示: 



计划采购表: jhcg_table



字段名称 中文名称 类型 长度 Goods_no 物品编号 vchar 10 Goods_name 物品名称 Vchar 50 Amount 采购数量 Int Price 采购单价 float Gold 币种 Vchar 15 Units 单位 Vchar 10 Date 时间 Date Remark 备注 vchar 100



库存统计表: kctj_table



字段名称 中文名称 类型 长度 Goods_no 物品编号 Vchar 10 Goods_name 物品名称 Vchar 50 amount 库存数量 Int Date 时间 Date



remark 备注 Vchar 100



实际采购表: sjcg_table



字段名称 中文名称 类型 长度 Goods_no 物品编号 Vchar 10 Goods_name 物品名称 Vchar 50 Amount 采购数量 Int Price Price 采购单价 Float Gold 币种 Vchar 15 Units 采购单位 Vchar 10 Date 时间 Date Remark 备注 vchar 100



其中业务逻辑非常简单，即根据计划采购表和库存统计表生成实际采购表。同时，对各表完成数据库的增、删、改、查等通用操作。


JSP设计


① 插入操作



完成对数据库表的记录插入功能，



② 查询操作



该查询主页面主要提供对三个数据库表的条件查询功能，



③ 生成实际采购表



生成数据库表是一个隐式操作，程序根据计划采购表和库存统计表的相应字段生成实际采购表，不需要用户的任何输入。



上述的开发工具综合应用介绍了基于Java开发电子商务应用系统的全过程，包括应用开发平台搭建、业务流程分析、JavaBean封装和JSP开发等内容，其中JSP开发中涉及到了通用SQL (查询和插入数据库表) 和游标操作 (生成实际采购表) ，基本可以完成任何网络数据库应用的需求。本实例基本上可以将前面介绍的基于Java的电子商务开发技术串接起来，指导读者进行电子商务应用开发。




分页


分页显示是Web数据库应用中经常需要遇到的问题，当用户的数据库查询结果远远超过了计算机屏幕的显示能力的时候，我们该如何合理的将数据呈现给用户呢？答案就是数据库分页显示，可以完美的解决上述问题。下面是一个数据库分页操作的通用实例，对任何数据库平台上的分页功能都有很好的借鉴意义。




选择


JavaSoft框架


JavaSoft提供三种JDBC产品组件，它们是Java开发工具包 (JDK) 的组成部份: JDBC驱动程序管理器、JDBC驱动程序测试工具包和JDBC-ODBC桥。



JDBC驱动程序管理器是JDBC体系结构的支柱。它实际上很小，也很简单；其主要作用是把Java应用程序连接到正确的JDBC驱动程序上，然后即退出。



JDBC驱动程序测试工具包为使JDBC驱动程序运行您的程序提供一定的可信度。只有通过JDBC驱动程序测试的驱动程序才被认为是符合JDBC标准TM的。



JDBC-ODBC桥使ODBC驱动程序可被用作JDBC驱动程序。它的实现为JDBC的快速发展提供了一条途径，其长远目标提供一种访问某些不常见的DBMS (如果对这些不常见的DBMS未实现JDBC) 的方法。


JDBC驱动程序的类型


目前比较常见的JDBC驱动程序可分为以下四个种类: 



 (1) JDBC-ODBC桥加ODBC驱动程序



JavaSoft桥产品利用ODBC驱动程序提供JDBC访问。注意，必须将ODBC二进制代码 (许多情况下还包括数据库客户机代码) 加载到使用该驱动程序的每个客户机上。因此，这种类型的驱动程序最适合于企业网 (这种网络上客户机的安装不是主要问题) ，或者是用Java编写的三层结构的应用程序服务器代码。



 (2) 本地API



这种类型的驱动程序把客户机API上的JDBC调用转换为Oracle、Sybase、Informix、DB2或其它DBMS的调用。注意，象桥驱动程序一样，这种类型的驱动程序要求将某些二进制代码加载到每台客户机上。



 (3) JDBC网络纯Java驱动程序



这种驱动程序将JDBC转换为与DBMS无关的网络协议，之后这种协议又被某个服务器转换为一种DBMS协议。这种网络服务器中间件能够将它的纯Java客户机连接到多种不同的数据库上。所用的具体协议取决于提供者。通常，这是最为灵活的JDBC驱动程序。有可能所有这种解决方案的提供者都提供适合于Intranet用的产品。为了使这些产品也支持Internet访问，它们必须处理Web所提出的安全性、通过防火墙的访问等方面的额外要求。几家提供者正将JDBC驱动程序加到他们现有的数据库中间件产品中。



 (4) 本地协议纯Java驱动程序



这种类型的驱动程序将JDBC调用直接转换为DBMS所使用的网络协议。这将允许从客户机机器上直接调用DBMS服务器，是Intranet访问的一个很实用的解决方法。由于许多这样的协议都是专用的，因此数据库提供者自己将是主要来源，有几家提供者已在着手做这件事了。


JDBC驱动程序的获取


目前已有几十个 (1) 类的驱动程序，即可与Javasoft桥联合使用的ODBC驱动程序的驱动程序。有大约十多个属于种类 (2) 的驱动程序是以DBMS的本地API为基础编写的。只有几个属于种类 (3) 的驱动程序，其首批提供者是SCO、OpenHorizon、Visigenic和WebLogic。此外，JavaSoft和数据库连接的领先提供者Intersolv还合作研制了JDBC-ODBC桥和JDBC驱动程序测试工具包。



有关JDBC最新的信息，有兴趣的读者可以查阅JDBC的官方网站-即JavaSoft的主页
 
不足
 

尽管JDBC在JAVA语言层面实现了统一，但不同数据库仍旧有许多差异。为了更好地实现跨数据库操作，于是诞生了Hibernate项目，Hibernate是对JDBC的再封装，实现了对数据库操作更宽泛的统一和更好的可移植性。

### ADBA
ADBA 是 Oracle 主导的 Java 异步数据库访问的标准 API 。它的目的性是集成于未来 Java 的标准发行版中，目前发展比较慢，目前只提供OpenJDK的沙盒特性供开发者研究之用。它不打算作为 JDBC 的扩展或替代，而是一个完全独立的 API，该 API 提供对 JDBC 相同数据库的完全无阻塞访问。

On Wednesday, September 18, at Oracle CodeOne Oracle announced that Oracle will stop work on ADBA (Asynchronous Database Access)

>https://mail.openjdk.java.net/pipermail/jdbc-spec-discuss/2019-September/000529.html


### R2DBC
pring 官方在 Spring 5 发布了响应式 Web 框架 Spring WebFlux 之后急需能够满足异步响应的数据库交互 API 。 由于缺乏标准和驱动，Pivotal (Spring 官方） 团队开始研究反应式关系型数据库连接 (Reactive Relational Database Connectivity），并提出了 R2DBC 规范 API 以评估可行性并讨论数据库厂商是否有兴趣支持反应式的异步非阻塞驱动程序。最开始只有 PostgreSQL 、H2、MSSQL 三家，现在 MySQL 也加入了进来。R2DBC 最新版本是0.8.1.RELEASE。除了驱动实现外还提供了 R2DBC 连接池 和 R2DBC 代理。除此之外还支持云原生应用。

---

>https://segmentfault.com/a/1190000022042952
http://sharryjava.iteye.com/blog/325872


