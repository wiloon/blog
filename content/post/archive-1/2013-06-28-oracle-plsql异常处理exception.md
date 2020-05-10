---
title: ORACLE PL/SQL异常处理(Exception)
author: wiloon
type: post
date: 2013-06-28T01:44:07+00:00
url: /?p=5591
categories:
  - DataBase

---
<http://blog.csdn.net/wh62592855/article/details/4736501>

1、PL/SQL错误类型

错误类型

报告者

处理方法

编译时错误

PL/SQL编译器

交互式地处理：编译器报告错误，你必须更正这些错误

运行时错误

PL/SQL运行时引擎

程序化地处理：异常由异常处理子程序引发并进行捕获

&nbsp;

&nbsp;

2、异常的声明

有两种异常：用户自定义异常和预定义异常

&nbsp;

用户自定义异常就是由程序员自己定义的一个错误。该错误还不是非常重要，所以并没有将整个错误包含在Oracle的错误中。例如，它可能是一个与数据有关的错误。而预定义异常则对应于一般的SQL和PL/SQL错误。

&nbsp;

用户自定义异常是在PL/SQL块的声明部分声明的。像变量一样，异常也有一个类型（EXCEPTION）和有效范围。例如：

&nbsp;

\[php\]\[/php\] view plaincopy

DECLARE

&nbsp;

Exception_name EXCEPTION;

&nbsp;

…

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

3、异常的引发

与异常相关联的错误发生的时候，就会引发相应的异常。用户自定义异常是通过RAISE语句显式引发的，而预定义异常则是在它们关联的ORACLE错误发生的时候隐式引发的。如果发生了一个还没有和异常进行关联的ORACLE错误的时候，也会引发一个异常。该异常可以使用OTHERS子程序进行捕获。预定义的异常也可以使用RAISE进行显式地引发，如果需要这样做的话。

&nbsp;

&nbsp;

\[php\]\[/php\] view plaincopy

…

&nbsp;

RAISE exception_name;

&nbsp;

…

&nbsp;

&nbsp;

4、异常的处理

发生异常的时候，程序的控制就会转移到代码块的异常处理部分。异常处理部分是由异常处理子程序组成的，这些异常处理子程序可以是针对某些异常的，也可以是针对所有异常的。与该异常相关联的错误发生，并引发了该异常的时候，就会执行异常处理部分的代码。

&nbsp;

异常处理部分的语法如下：

&nbsp;

&nbsp;

\[php\]\[/php\] view plaincopy

EXCEPTION

&nbsp;

WHEN exception_name THEN

&nbsp;

Sequence\_of\_statements1;

&nbsp;

WHEN exception_name THEN

&nbsp;

Sequence\_of\_statements2;

&nbsp;

[WHEN OTHERS THEN

&nbsp;

Sequence\_of\_statements3;]

&nbsp;

END;

&nbsp;

&nbsp;

每一个异常处理部分都是由WHEN子句和引发异常以后要执行的语句组成的。WHEN标识这个处理子程序是针对哪个异常的。

&nbsp;

OTHERS异常处理子程序

PL/SQL定义了一个异常处理子程序，即OTHERS。当前异常处理部分定义的所有WHEN语句都没有处理的任意一个已引发的异常，都会导致执行这个OTHERS异常处理子程序。该异常处理子程序应该总是作为代码块的最后一个异常处理子程序，这样就会首先扫描前面的异常处理子程序。WHEN OTHERS会捕获所有异常，不管这些异常是预定义的，还是用户自定义的。

&nbsp;

检查错误堆栈—SQLCODE和SQLERRM

PL/SQL使用两个内置函数SQLCODE和SQLERRM提供错误信息。SQLCODE返回的是当前的错误代号，而SQLERRM返回的是当前的错误信息文本。如果是用户自定义的异常，SQLCODE就会返回值1，SQLERRM就会返回“ User-defined Exception”。

&nbsp;

下面是一个使用SQLCODE和SQLERRM的例子

&nbsp;

\[php\]\[/php\] view plaincopy

DECLARE

&nbsp;

&#8212; Exception to indicate an error condition

&nbsp;

e_DuplicateAuthors EXCEPTION;

&nbsp;

&nbsp;

&nbsp;

&#8212; IDs for three authors

&nbsp;

v_Author1 books.author1%TYPE;

&nbsp;

v_Author2 books.author2%TYPE;

&nbsp;

v_Author3 books.author3%TYPE;

&nbsp;

&nbsp;

&nbsp;

&#8212; Code and text of other runtime errors

&nbsp;

v\_ErrorCode log\_table.code%TYPE;

&nbsp;

v\_ErrorText log\_table.message%TYPE;

&nbsp;

BEGIN

&nbsp;

/\* Find the IDs for the 3 authors of &#8216;Oracle9i DBA 101&#8217; \*/

&nbsp;

SELECT author1, author2, author3

&nbsp;

INTO v\_Author1, v\_Author2, v_Author3

&nbsp;

FROM books

&nbsp;

WHERE title = &#8216;Oracle9i DBA 101&#8217;;

&nbsp;

&nbsp;

&nbsp;

/\* Ensure that there are no duplicates \*/

&nbsp;

IF (v\_Author1 = v\_Author2) OR (v\_Author1 = v\_Author3) OR

&nbsp;

(v\_Author2 = v\_Author3) THEN

&nbsp;

RAISE e_DuplicateAuthors;

&nbsp;

END IF;

&nbsp;

EXCEPTION

&nbsp;

WHEN e_DuplicateAuthors THEN

&nbsp;

/* Handler which executes when there are duplicate authors for

&nbsp;

Oracle9i DBA 101. We will insert a log message recording

&nbsp;

what has happened. */

&nbsp;

INSERT INTO log_table (info)

&nbsp;

VALUES (&#8216;Oracle9i DBA 101 has duplicate authors&#8217;);

&nbsp;

WHEN OTHERS THEN

&nbsp;

/\* Handler which executes for all other errors. \*/

&nbsp;

v_ErrorCode := SQLCODE;

&nbsp;

&#8212; Note the use of SUBSTR here.

&nbsp;

v_ErrorText := SUBSTR(SQLERRM, 1, 200);

&nbsp;

INSERT INTO log_table (code, message, info) VALUES

&nbsp;

(v\_ErrorCode, v\_ErrorText, &#8216;Oracle error occurred&#8217;);

&nbsp;

END;

&nbsp;

/

&nbsp;

&nbsp;

由于该堆栈上每一条错误消息文本的最大长度均为512个字节，但是堆栈中可能会有多条消息文本。在上面的例子中，v_ErrorText只有200个字符。如果该错误消息文本长度大于200个字符，那么赋值语句

&nbsp;

v_ErrorText := SQLERRM;

就会引发预定义的异常VALUE_ERROR。为了防止发生这种异常，我们使用了内置函数SUBSTR。

&nbsp;

注意，SQLCODE和SQLERRM的返回值首先会被分配给局部变量，然后再在SQL语句中使用这些局部变量。因为这些函数都是过程化的函数，所以不能直接在SQL语句中使用它们。

&nbsp;

通过下面这个例子我们看看错误号和相应的错误消息文本之间的关系

&nbsp;

\[php\]\[/php\] view plaincopy

set serveroutput on

&nbsp;

BEGIN

&nbsp;

DBMS\_OUTPUT.PUT\_LINE(&#8216;SQLERRM(0): &#8216; || SQLERRM(0));

&nbsp;

DBMS\_OUTPUT.PUT\_LINE(&#8216;SQLERRM(100): &#8216; || SQLERRM(100));

&nbsp;

DBMS\_OUTPUT.PUT\_LINE(&#8216;SQLERRM(10): &#8216; || SQLERRM(10));

&nbsp;

DBMS\_OUTPUT.PUT\_LINE(&#8216;SQLERRM: &#8216; || SQLERRM);

&nbsp;

DBMS\_OUTPUT.PUT\_LINE(&#8216;SQLERRM(-1): &#8216; || SQLERRM(-1));

&nbsp;

DBMS\_OUTPUT.PUT\_LINE(&#8216;SQLERRM(-54): &#8216; || SQLERRM(-54));

&nbsp;

END;

&nbsp;

/

&nbsp;

&#8211;运行结果如下

&nbsp;

SQL> @SQLERRM.sql

&nbsp;

SQLERRM(0): ORA-0000: normal, successful completion

&nbsp;

SQLERRM(100): ORA-01403: no data found

&nbsp;

SQLERRM(10): -10: non-ORACLE exception

&nbsp;

SQLERRM: ORA-0000: normal, successful completion

&nbsp;

SQLERRM(-1): ORA-00001: unique constraint (.) violated

&nbsp;

SQLERRM(-54): ORA-00054: resource busy and acquire with NOWAIT specified

&nbsp;

&nbsp;

&nbsp;

PL/SQL procedure successfully completed.

&nbsp;

&nbsp;

EXCEPTION_INIT pragma

&nbsp;

你可以将一个经过命名的异常和一个特别的ORACLE错误相关联。这会使你专门能够捕获此错误，而不是通过WHEN OTHERS处理器来进行捕获。EXCEPTION_INIT pragma的语法如下：

&nbsp;

PRAGMA EXCEPTION\_INIT(exception\_name,Oracle\_error\_number);

&nbsp;

这里，exception\_name是在PRAGMA前面声明的异常的名字，而Oracle\_error_number是与此命名异常相关的所需错误代码。这个PRAGMA必须在声明部分。

&nbsp;

下面这个例子在运行时刻如果遇到“ORA-1400:mandatory NOT NULL column missing or NULL during insert”错误时将引发e_MissingNull&#8211;用户定义的异常。

&nbsp;

\[php\]\[/php\] view plaincopy

DECLARE

&nbsp;

e_MissingNull EXCEPTION;

&nbsp;

PRAGMA EXCEPTION\_INIT(e\_MissingNull, -1400);

&nbsp;

BEGIN

&nbsp;

INSERT INTO students (id) VALUES (NULL);

&nbsp;

EXCEPTION

&nbsp;

WHEN e_MissingNull then

&nbsp;

INSERT INTO log_table (info) VALUES (&#8216;ORA-1400 occurred&#8217;);

&nbsp;

END;

&nbsp;

/

&nbsp;

&nbsp;

每次发生PRAGMA EXCEPTION_INIT时，一个Oracle错误只能和一个用户自定义异常相关联。在异常处理内部，SQLCODE和SQLERRM将会返回发生Oracle错误的代码和错误消息，但是不会返回用户定义的消息。

&nbsp;

&nbsp;

使用RAISE\_APPLICATION\_ERROR

你可以使用内置函数RAISE\_APPLICATION\_ERROR以创建自己的错误消息，这可能要比已命名的异常更具说明性。用户定义消息从块中传递到调用环境中的方式和ORACLE错误是一样的。语法如下：

&nbsp;

RAISE\_APPLICATION\_ERROR(error\_number,error\_message,[keep_errors]);

&nbsp;

error\_number是从-200000到-20999之间的参数，error\_message是与此错误相关的正文，不能多于512个字节。而keep_errors是一个布尔值，是可选的，如果为TRUE，那么新的错误将被添加到已经引发的错误列表中（如果有的话）。如果为FALSE（这是缺省的设置），那么新的错误将替换错误的当前列表。

&nbsp;

例如下面的这个例子将在为一个新的学生注册以前检查是否在班级中有足够的地方容纳他。

&nbsp;

\[php\]\[/php\] view plaincopy

CREATE OR REPLACE PROCEDURE Register (

&nbsp;

/* Registers the student identified by the p_StudentID parameter in the class

&nbsp;

identified by the p\_Department and p\_Course parameters. Before calling

&nbsp;

ClassPackage.AddStudent, which actually adds the student to the class, this

&nbsp;

procedure verifies that there is room in the class, and that the class

&nbsp;

exists. */

&nbsp;

p_StudentID IN students.id%TYPE,

&nbsp;

p_Department IN classes.department%TYPE,

&nbsp;

p_Course IN classes.course%TYPE) AS

&nbsp;

&nbsp;

&nbsp;

v_CurrentStudents NUMBER; &#8212; Current number of students in the class

&nbsp;

v_MaxStudents NUMBER; &#8212; Maximum number of students in the class

&nbsp;

&nbsp;

&nbsp;

BEGIN

&nbsp;

/* Determine the current number of students registered, and the maximum

&nbsp;

number of students allowed to register. */

&nbsp;

SELECT current\_students, max\_students

&nbsp;

INTO v\_CurrentStudents, v\_MaxStudents

&nbsp;

FROM classes

&nbsp;

WHERE course = p_Course

&nbsp;

AND department = p_Department;

&nbsp;

&nbsp;

&nbsp;

/\* Make sure there is enough room for this additional student. \*/

&nbsp;

IF v\_CurrentStudents + 1 > v\_MaxStudents THEN

&nbsp;

RAISE\_APPLICATION\_ERROR(-20000, &#8216;Can&#8221;t add more students to &#8216; ||

&nbsp;

p\_Department || &#8216; &#8216; || p\_Course);

&nbsp;

END IF;

&nbsp;

&nbsp;

&nbsp;

/\* Add the student to the class. \*/

&nbsp;

ClassPackage.AddStudent(p\_StudentID, p\_Department, p_Course);

&nbsp;

&nbsp;

&nbsp;

EXCEPTION

&nbsp;

WHEN NO\_DATA\_FOUND THEN

&nbsp;

/* Class information passed to this procedure doesn&#8217;t exist. Raise an error

&nbsp;

to let the calling program know of this. */

&nbsp;

RAISE\_APPLICATION\_ERROR(-20001, p\_Department || &#8216; &#8216; || p\_Course ||

&nbsp;

&#8216; doesn&#8221;t exist!&#8217;);

&nbsp;

END Register;

&nbsp;

/

&nbsp;

&nbsp;

5、异常的传播

&nbsp;

1）在执行部分引发的异常

当一个异常是在块的执行部分引发的，PL/SQL使用下面的方法决定要激活哪个异常处理器：

如果当前块对该异常设置了处理器，那么执行它并成功完成该块的执行，然后控制会转给包含块。

如果当前块没有对当前异常定义处理器，那么通过在包含块中引发它来传播异常。然后对包含块执行步骤一。

&nbsp;

2）在声明部分引发的异常

如果在声明部分的赋值操作引发了一个异常，那么该异常将立即传播给包含块。发生这种情况以后，在前面给出的法则将进一步被应用到异常的传播上。尽管在当前块中有一个处理器，它也不会被执行。

&nbsp;

3）在异常处理部分引发的异常

在异常处理器中也可能引发异常，这可以是通过RAISE语句显式引发的，也可以是由运行时刻错误隐含引发的。无论怎样，异常都立即被传播给包含块，这和声明部分引发的异常相类似。

&nbsp;

&nbsp;

6、使用异常的准则

&nbsp;

1）异常的范围

异常像变量一样，也是有一定范围的。如果用户自定义异常传播到它的范围之外，就不能再通过名称引用它。

&nbsp;

\[php\]\[/php\] view plaincopy

BEGIN

&nbsp;

DECLARE

&nbsp;

e_UserDefinedException EXCEPTION;

&nbsp;

BEGIN

&nbsp;

RAISE e_UserDefinedException;

&nbsp;

END;

&nbsp;

EXCEPTION

&nbsp;

/* e_UserDefinedException is out of scope here &#8211; can only be

&nbsp;

handled by an OTHERS handler */

&nbsp;

WHEN OTHERS THEN

&nbsp;

/* Just re-raise the exception, which will be propagated to the

&nbsp;

calling environment */

&nbsp;

RAISE;

&nbsp;

END;

&nbsp;

/

&nbsp;

&nbsp;

一般而言，如果打算将用户自定义的错误传播到代码块之外，最好的方法就是在包中定义该异常，以使其在该代码块之外仍可见，或使用RAISE\_APPLICATION\_ERROR引发该异常。如果创建一个成为GLOBALS的包，并在其中定义了一个e_UserDefinedException异常，那么这个异常在外部块中仍然可见。

&nbsp;

如下例所示

&nbsp;

\[php\]\[/php\] view plaincopy

CREATE OR REPLACE PACKAGE Globals AS

&nbsp;

/* This package contains global declarations. Objects declared here will

&nbsp;

be visible via qualified references for any other blocks or procedures.

&nbsp;

Note that this package does not have a package body. */

&nbsp;

&nbsp;

&nbsp;

/\* A user-defined exception. \*/

&nbsp;

e_UserDefinedException EXCEPTION;

&nbsp;

END Globals;

&nbsp;

/

&nbsp;

&nbsp;

&nbsp;

&#8211;有了这个和GLOBALS包以后，就可以重写前面的代码：

&nbsp;

&nbsp;

&nbsp;

BEGIN

&nbsp;

BEGIN

&nbsp;

RAISE Globals.e_UserDefinedException;

&nbsp;

END;

&nbsp;

EXCEPTION

&nbsp;

/* Since e_UserDefinedException is still visible, we can handle it

&nbsp;

explicitly */

&nbsp;

WHEN Globals.e_UserDefinedException THEN &#8211;引用包中定义异常

&nbsp;

/* Just re-raise the exception, which will be propagated to the

&nbsp;

calling environment */

&nbsp;

RAISE;

&nbsp;

END;

&nbsp;

/

&nbsp;

&nbsp;

2）避免未处理的异常

优秀的编程经验是在整个程序中避免出现任何未经过处理的异常。这可以通过在程序的最顶层使用一个OTHERS子程序来实现。该处理子程序可以只登记错误并登记错误发生的位置，通过这种方法，就可以保证每个错误都会得到检查。

&nbsp;

如下例所示

&nbsp;

\[php\]\[/php\] view plaincopy

DECLARE

&nbsp;

v_errornumber number;

&nbsp;

v_errortext varchar2(200);

&nbsp;

Begin

&nbsp;

…

&nbsp;

EXCEPTION

&nbsp;

WHEN OTHERS THEN

&nbsp;

v_errornumber:=SQLCODE;

&nbsp;

v_errortext:=SUBSTR(SQLERRM,1,200);

&nbsp;

INSERT INTO log_table(code,message,info)

&nbsp;

VALUES

&nbsp;

(v\_errornumber,v\_errortext,’Oracle error occurred at’||TO_CHAR(SYSDATE,’DD-MON-YY HH24:MI:SS’));

&nbsp;

END;

&nbsp;

&nbsp;

3）标识错误发生的位置

由于整个代码块都使用同一个异常处理部分检查并处理异常，所以很难确定引发这个错误的是哪一条SQL语句。考虑下面示例

&nbsp;

\[python\]\[/python\] view plaincopy

BEGIN

&nbsp;

SELECT…

&nbsp;

SELECT..

&nbsp;

SELECT…

&nbsp;

EXCEPTION

&nbsp;

WHEN NO\_DATA\_FOUND THEN

&nbsp;

&#8211;which select statement raised the exception?

&nbsp;

END;

&nbsp;

&nbsp;

&nbsp;

&#8211;解决上述问题的方法有两种。第一种是添加一个标识该SQL语句的计数器：

&nbsp;

&nbsp;

&nbsp;

DECLARE

&nbsp;

V_selectcounter NUMBER:=1;

&nbsp;

BEGIN

&nbsp;

SELECT…

&nbsp;

V_selectcounter NUMBER:=2;

&nbsp;

SELECT…

&nbsp;

V_selectcounter NUMBER:=3;

&nbsp;

SELECT…

&nbsp;

EXCEPTION

&nbsp;

WHEN NO\_DATA\_FOUND THEN

&nbsp;

INSERT INTO log\_table(info) VALUES(‘NO DATA FOUND IN SELECT’||v\_selectcounter);

&nbsp;

END;

&nbsp;

&nbsp;

&nbsp;

&#8211;另一种方法是将每一条语句都放置在它自己的子块中：

&nbsp;

&nbsp;

&nbsp;

BEGIN

&nbsp;

BEGIN

&nbsp;

SELECT…

&nbsp;

EXCEPTION

&nbsp;

WHEN NO\_DATA\_FOUND THEN

&nbsp;

INSERT INTO log_table(info) VALUES(‘NO DATA FOUND IN SELECT 1’);

&nbsp;

END;

&nbsp;

BEGIN

&nbsp;

SELECT…

&nbsp;

EXCEPTION

&nbsp;

WHEN NO\_DATA\_FOUND THEN

&nbsp;

INSERT INTO log_table(info) VALUES(‘NO DATA FOUND IN SELECT 2’);

&nbsp;

END;

&nbsp;

BEGIN

&nbsp;

SELECT…

&nbsp;

EXCEPTION

&nbsp;

WHEN NO\_DATA\_FOUND THEN

&nbsp;

INSERT INTO log_table(info) VALUES(‘NO DATA FOUND IN SELECT 3’);

&nbsp;

END;

&nbsp;

END;

&nbsp;

&nbsp;

7、异常代码的编写风格

&nbsp;

1）RAISE\_APPLICATION\_ERROR和RAISE的比较

&nbsp;

RAISE\_APPLICATION\_ERROR

RAISE

允许我们填写自己的错误消息文本，该文本可以包含应用程序专用的数据

不允许包含消息文本

不能使用已命名的异常处理子程序进行捕获，只能使用OTHERS处理子程序进行捕获

可以使用已命名的处理子程序捕获该异常，只要该异常在它自己的异常范围内即可

&nbsp;

通常而言，推荐对设计给终端用户看的错误，使用RAISE\_APPLICATION\_ERROR。因为对于他们而言，具体的错误编号和描述性文本非常有用。而另一方面，对设计为由程序直接进行处理的异常，推荐使用RAISE。

&nbsp;

2）将异常作为控制语句

因为引发异常会将程序的控制逻辑转移到代码块的异常处理部分，所以可以将RAISE语句用作控制语句，就像GOTO语句一样。例如，如果我们有很深的嵌套循环，并需要立即从中退出的时候，这可能会非常有用。