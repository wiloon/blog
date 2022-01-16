---
title: ORACLE PL/SQL异常处理(Exception)
author: "-"
date: 2013-06-28T01:44:07+00:00
url: /?p=5591
categories:
  - DataBase

---
## ORACLE PL/SQL异常处理(Exception)
<http://blog.csdn.net/wh62592855/article/details/4736501>

1. PL/SQL错误类型

错误类型

报告者

处理方法

编译时错误

PL/SQL编译器

交互式地处理: 编译器报告错误,你必须更正这些错误

运行时错误

PL/SQL运行时引擎

程序化地处理: 异常由异常处理子程序引发并进行捕获

2. 异常的声明

有两种异常: 用户自定义异常和预定义异常


用户自定义异常就是由程序员自己定义的一个错误。该错误还不是非常重要,所以并没有将整个错误包含在Oracle的错误中。例如,它可能是一个与数据有关的错误。而预定义异常则对应于一般的SQL和PL/SQL错误。


用户自定义异常是在PL/SQL块的声明部分声明的。像变量一样,异常也有一个类型（EXCEPTION) 和有效范围。例如: 


[php][/php] 

DECLARE


Exception_name EXCEPTION;


…


3. 异常的引发

与异常相关联的错误发生的时候,就会引发相应的异常。用户自定义异常是通过RAISE语句显式引发的,而预定义异常则是在它们关联的ORACLE错误发生的时候隐式引发的。如果发生了一个还没有和异常进行关联的ORACLE错误的时候,也会引发一个异常。该异常可以使用OTHERS子程序进行捕获。预定义的异常也可以使用RAISE进行显式地引发,如果需要这样做的话。

[php][/php] 

…


RAISE exception_name;


…

4. 异常的处理

发生异常的时候,程序的控制就会转移到代码块的异常处理部分。异常处理部分是由异常处理子程序组成的,这些异常处理子程序可以是针对某些异常的,也可以是针对所有异常的。与该异常相关联的错误发生,并引发了该异常的时候,就会执行异常处理部分的代码。


异常处理部分的语法如下: 

[php][/php] 

EXCEPTION


WHEN exception_name THEN


Sequence_of_statements1;


WHEN exception_name THEN


Sequence_of_statements2;


[WHEN OTHERS THEN


Sequence_of_statements3;]


END;

每一个异常处理部分都是由WHEN子句和引发异常以后要执行的语句组成的。WHEN标识这个处理子程序是针对哪个异常的。


OTHERS异常处理子程序

PL/SQL定义了一个异常处理子程序,即OTHERS。当前异常处理部分定义的所有WHEN语句都没有处理的任意一个已引发的异常,都会导致执行这个OTHERS异常处理子程序。该异常处理子程序应该总是作为代码块的最后一个异常处理子程序,这样就会首先扫描前面的异常处理子程序。WHEN OTHERS会捕获所有异常,不管这些异常是预定义的,还是用户自定义的。


检查错误堆栈—SQLCODE和SQLERRM

PL/SQL使用两个内置函数SQLCODE和SQLERRM提供错误信息。SQLCODE返回的是当前的错误代号,而SQLERRM返回的是当前的错误信息文本。如果是用户自定义的异常,SQLCODE就会返回值1,SQLERRM就会返回" User-defined Exception"。


下面是一个使用SQLCODE和SQLERRM的例子


[php][/php] 

DECLARE


- Exception to indicate an error condition


e_DuplicateAuthors EXCEPTION;


- IDs for three authors


v_Author1 books.author1%TYPE;


v_Author2 books.author2%TYPE;


v_Author3 books.author3%TYPE;


- Code and text of other runtime errors


v_ErrorCode log_table.code%TYPE;


v_ErrorText log_table.message%TYPE;


BEGIN


/* Find the IDs for the 3 authors of 'Oracle9i DBA 101' */


SELECT author1, author2, author3


INTO v_Author1, v_Author2, v_Author3


FROM books


WHERE title = 'Oracle9i DBA 101';


/* Ensure that there are no duplicates */


IF (v_Author1 = v_Author2) OR (v_Author1 = v_Author3) OR


(v_Author2 = v_Author3) THEN


RAISE e_DuplicateAuthors;


END IF;


EXCEPTION


WHEN e_DuplicateAuthors THEN


/* Handler which executes when there are duplicate authors for


Oracle9i DBA 101. We will insert a log message recording


what has happened. */


INSERT INTO log_table (info)


VALUES ('Oracle9i DBA 101 has duplicate authors');


WHEN OTHERS THEN


/* Handler which executes for all other errors. */


v_ErrorCode := SQLCODE;


- Note the use of SUBSTR here.


v_ErrorText := SUBSTR(SQLERRM, 1, 200);


INSERT INTO log_table (code, message, info) VALUES


(v_ErrorCode, v_ErrorText, 'Oracle error occurred');


END;


/

由于该堆栈上每一条错误消息文本的最大长度均为512个字节,但是堆栈中可能会有多条消息文本。在上面的例子中,v_ErrorText只有200个字符。如果该错误消息文本长度大于200个字符,那么赋值语句


v_ErrorText := SQLERRM;

就会引发预定义的异常VALUE_ERROR。为了防止发生这种异常,我们使用了内置函数SUBSTR。


注意,SQLCODE和SQLERRM的返回值首先会被分配给局部变量,然后再在SQL语句中使用这些局部变量。因为这些函数都是过程化的函数,所以不能直接在SQL语句中使用它们。


通过下面这个例子我们看看错误号和相应的错误消息文本之间的关系


[php][/php] 

set serveroutput on


BEGIN


DBMS_OUTPUT.PUT_LINE('SQLERRM(0): ' || SQLERRM(0));


DBMS_OUTPUT.PUT_LINE('SQLERRM(100): ' || SQLERRM(100));


DBMS_OUTPUT.PUT_LINE('SQLERRM(10): ' || SQLERRM(10));


DBMS_OUTPUT.PUT_LINE('SQLERRM: ' || SQLERRM);


DBMS_OUTPUT.PUT_LINE('SQLERRM(-1): ' || SQLERRM(-1));


DBMS_OUTPUT.PUT_LINE('SQLERRM(-54): ' || SQLERRM(-54));


END;


/


-运行结果如下


SQL> @SQLERRM.sql


SQLERRM(0): ORA-0000: normal, successful completion


SQLERRM(100): ORA-01403: no data found


SQLERRM(10): -10: non-ORACLE exception


SQLERRM: ORA-0000: normal, successful completion


SQLERRM(-1): ORA-00001: unique constraint (.) violated


SQLERRM(-54): ORA-00054: resource busy and acquire with NOWAIT specified


PL/SQL procedure successfully completed.

EXCEPTION_INIT pragma


你可以将一个经过命名的异常和一个特别的ORACLE错误相关联。这会使你专门能够捕获此错误,而不是通过WHEN OTHERS处理器来进行捕获。EXCEPTION_INIT pragma的语法如下: 


PRAGMA EXCEPTION_INIT(exception_name,Oracle_error_number);


这里,exception_name是在PRAGMA前面声明的异常的名字,而Oracle_error_number是与此命名异常相关的所需错误代码。这个PRAGMA必须在声明部分。


下面这个例子在运行时刻如果遇到"ORA-1400:mandatory NOT NULL column missing or NULL during insert"错误时将引发e_MissingNull-用户定义的异常。


[php][/php] 

DECLARE


e_MissingNull EXCEPTION;


PRAGMA EXCEPTION_INIT(e_MissingNull, -1400);


BEGIN


INSERT INTO students (id) VALUES (NULL);


EXCEPTION


WHEN e_MissingNull then


INSERT INTO log_table (info) VALUES ('ORA-1400 occurred');


END;


/

每次发生PRAGMA EXCEPTION_INIT时,一个Oracle错误只能和一个用户自定义异常相关联。在异常处理内部,SQLCODE和SQLERRM将会返回发生Oracle错误的代码和错误消息,但是不会返回用户定义的消息。

使用RAISE_APPLICATION_ERROR

你可以使用内置函数RAISE_APPLICATION_ERROR以创建自己的错误消息,这可能要比已命名的异常更具说明性。用户定义消息从块中传递到调用环境中的方式和ORACLE错误是一样的。语法如下: 


RAISE_APPLICATION_ERROR(error_number,error_message,[keep_errors]);


error_number是从-200000到-20999之间的参数,error_message是与此错误相关的正文,不能多于512个字节。而keep_errors是一个布尔值,是可选的,如果为TRUE,那么新的错误将被添加到已经引发的错误列表中（如果有的话) 。如果为FALSE（这是缺省的设置) ,那么新的错误将替换错误的当前列表。


例如下面的这个例子将在为一个新的学生注册以前检查是否在班级中有足够的地方容纳他。


[php][/php] 

CREATE OR REPLACE PROCEDURE Register (


/* Registers the student identified by the p_StudentID parameter in the class


identified by the p_Department and p_Course parameters. Before calling


ClassPackage.AddStudent, which actually adds the student to the class, this


procedure verifies that there is room in the class, and that the class


exists. */


p_StudentID IN students.id%TYPE,


p_Department IN classes.department%TYPE,


p_Course IN classes.course%TYPE) AS


v_CurrentStudents NUMBER; - Current number of students in the class


v_MaxStudents NUMBER; - Maximum number of students in the class


BEGIN


/* Determine the current number of students registered, and the maximum


number of students allowed to register. */


SELECT current_students, max_students


INTO v_CurrentStudents, v_MaxStudents


FROM classes


WHERE course = p_Course


AND department = p_Department;


/* Make sure there is enough room for this additional student. */


IF v_CurrentStudents + 1 > v_MaxStudents THEN


RAISE_APPLICATION_ERROR(-20000, 'Can"t add more students to ' ||


p_Department || ' ' || p_Course);


END IF;


/* Add the student to the class. */


ClassPackage.AddStudent(p_StudentID, p_Department, p_Course);


EXCEPTION


WHEN NO_DATA_FOUND THEN


/* Class information passed to this procedure doesn't exist. Raise an error


to let the calling program know of this. */


RAISE_APPLICATION_ERROR(-20001, p_Department || ' ' || p_Course ||


' doesn"t exist!');


END Register;


/

5. 异常的传播


1) 在执行部分引发的异常

当一个异常是在块的执行部分引发的,PL/SQL使用下面的方法决定要激活哪个异常处理器: 

如果当前块对该异常设置了处理器,那么执行它并成功完成该块的执行,然后控制会转给包含块。

如果当前块没有对当前异常定义处理器,那么通过在包含块中引发它来传播异常。然后对包含块执行步骤一。


2) 在声明部分引发的异常

如果在声明部分的赋值操作引发了一个异常,那么该异常将立即传播给包含块。发生这种情况以后,在前面给出的法则将进一步被应用到异常的传播上。尽管在当前块中有一个处理器,它也不会被执行。


3) 在异常处理部分引发的异常

在异常处理器中也可能引发异常,这可以是通过RAISE语句显式引发的,也可以是由运行时刻错误隐含引发的。无论怎样,异常都立即被传播给包含块,这和声明部分引发的异常相类似。

6. 使用异常的准则


1) 异常的范围

异常像变量一样,也是有一定范围的。如果用户自定义异常传播到它的范围之外,就不能再通过名称引用它。


[php][/php] 

BEGIN


DECLARE


e_UserDefinedException EXCEPTION;


BEGIN


RAISE e_UserDefinedException;


END;


EXCEPTION


/* e_UserDefinedException is out of scope here - can only be


handled by an OTHERS handler */


WHEN OTHERS THEN


/* Just re-raise the exception, which will be propagated to the


calling environment */


RAISE;


END;


/

一般而言,如果打算将用户自定义的错误传播到代码块之外,最好的方法就是在包中定义该异常,以使其在该代码块之外仍可见,或使用RAISE_APPLICATION_ERROR引发该异常。如果创建一个成为GLOBALS的包,并在其中定义了一个e_UserDefinedException异常,那么这个异常在外部块中仍然可见。


如下例所示


[php][/php] 

CREATE OR REPLACE PACKAGE Globals AS


/* This package contains global declarations. Objects declared here will


be visible via qualified references for any other blocks or procedures.


Note that this package does not have a package body. */


/* A user-defined exception. */


e_UserDefinedException EXCEPTION;


END Globals;


/


-有了这个和GLOBALS包以后,就可以重写前面的代码: 


BEGIN


BEGIN


RAISE Globals.e_UserDefinedException;


END;


EXCEPTION


/* Since e_UserDefinedException is still visible, we can handle it


explicitly */


WHEN Globals.e_UserDefinedException THEN -引用包中定义异常


/* Just re-raise the exception, which will be propagated to the


calling environment */


RAISE;


END;


/

2) 避免未处理的异常

优秀的编程经验是在整个程序中避免出现任何未经过处理的异常。这可以通过在程序的最顶层使用一个OTHERS子程序来实现。该处理子程序可以只登记错误并登记错误发生的位置,通过这种方法,就可以保证每个错误都会得到检查。


如下例所示


[php][/php] 

DECLARE


v_errornumber number;


v_errortext varchar2(200);


Begin


…


EXCEPTION


WHEN OTHERS THEN


v_errornumber:=SQLCODE;


v_errortext:=SUBSTR(SQLERRM,1,200);


INSERT INTO log_table(code,message,info)


VALUES


(v_errornumber,v_errortext,'Oracle error occurred at'||TO_CHAR(SYSDATE,'DD-MON-YY HH24:MI:SS'));


END;

3) 标识错误发生的位置

由于整个代码块都使用同一个异常处理部分检查并处理异常,所以很难确定引发这个错误的是哪一条SQL语句。考虑下面示例


[python][/python] 

BEGIN


SELECT…


SELECT..


SELECT…


EXCEPTION


WHEN NO_DATA_FOUND THEN


-which select statement raised the exception?


END;


-解决上述问题的方法有两种。第一种是添加一个标识该SQL语句的计数器: 


DECLARE


V_selectcounter NUMBER:=1;


BEGIN


SELECT…


V_selectcounter NUMBER:=2;


SELECT…


V_selectcounter NUMBER:=3;


SELECT…


EXCEPTION


WHEN NO_DATA_FOUND THEN


INSERT INTO log_table(info) VALUES('NO DATA FOUND IN SELECT'||v_selectcounter);


END;


-另一种方法是将每一条语句都放置在它自己的子块中: 


BEGIN


BEGIN


SELECT…


EXCEPTION


WHEN NO_DATA_FOUND THEN


INSERT INTO log_table(info) VALUES('NO DATA FOUND IN SELECT 1');


END;


BEGIN


SELECT…


EXCEPTION


WHEN NO_DATA_FOUND THEN


INSERT INTO log_table(info) VALUES('NO DATA FOUND IN SELECT 2');


END;


BEGIN


SELECT…


EXCEPTION


WHEN NO_DATA_FOUND THEN


INSERT INTO log_table(info) VALUES('NO DATA FOUND IN SELECT 3');


END;


END;

7. 异常代码的编写风格


1) RAISE_APPLICATION_ERROR和RAISE的比较


RAISE_APPLICATION_ERROR

RAISE

允许我们填写自己的错误消息文本,该文本可以包含应用程序专用的数据

不允许包含消息文本

不能使用已命名的异常处理子程序进行捕获,只能使用OTHERS处理子程序进行捕获

可以使用已命名的处理子程序捕获该异常,只要该异常在它自己的异常范围内即可


通常而言,推荐对设计给终端用户看的错误,使用RAISE_APPLICATION_ERROR。因为对于他们而言,具体的错误编号和描述性文本非常有用。而另一方面,对设计为由程序直接进行处理的异常,推荐使用RAISE。


2) 将异常作为控制语句

因为引发异常会将程序的控制逻辑转移到代码块的异常处理部分,所以可以将RAISE语句用作控制语句,就像GOTO语句一样。例如,如果我们有很深的嵌套循环,并需要立即从中退出的时候,这可能会非常有用。