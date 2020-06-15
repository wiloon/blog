---
title: sqlserver 存储过程 try catch TRANSACTION
author: wiloon
type: post
date: 2013-04-19T07:59:36+00:00
url: /?p=5412
categories:
  - DataBase

---
本文来自CSDN博客，转载请标明出处：[http://blog.csdn.net/WeiZhang\_son\_Ding/archive/2010/02/05/5291732.aspx][1]

CREATE PROCEDURE YourProcedure <wbr /> <wbr /> <wbr /> <wbr />

AS
  
BEGIN
  
<wbr /> <wbr /> <wbr /> SET NOCOUNT ON;

<wbr /> <wbr /> <wbr /> BEGIN TRY&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;开始捕捉异常
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> BEIN TRAN&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;开始事务
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> UPDATE A SET A.names = B.names FROM 表1 AS A INNER JOIN 表2 AS B ON A.id = B.id

<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> UPDATE A SET A.names = B.names FROM 表1 AS A INNER JOIN 表2 AS B ON A.TEST = B.TEST

<wbr /> <wbr /> <wbr /> COMMIT TRAN &#8212;&#8212;-提交事务
  
<wbr /> <wbr /> <wbr /> END TRY&#8212;&#8212;&#8212;&#8211;结束捕捉异常
  
<wbr /> <wbr /> <wbr /> BEGIN CATCH&#8212;&#8212;&#8212;&#8212;有异常被捕获
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> IF @@TRANCOUNT > 0&#8212;&#8212;&#8212;&#8212;&#8212;判断有没有事务
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> BEGIN
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ROLLBACK TRAN&#8212;&#8212;&#8212;-回滚事务
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> END <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> EXEC YourLogErrorProcedure&#8212;&#8212;&#8212;&#8211;执行存储过程将错误信息记录在表当中
  
<wbr /> <wbr /> <wbr /> END CATCH&#8212;&#8212;&#8211;结束异常处理
  
END

<wbr />

&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;记录操作错信息的存储过程&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8211;

CREATE PROCEDURE YourLogErrorProcedure
  
<wbr /> <wbr /> <wbr /> @ErrorLogID [int] = 0 OUTPUT &#8212; contains the ErrorLogID of the row inserted
  
AS <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8212; by uspLogError in the ErrorLog table
  
BEGIN
  
<wbr /> <wbr /> <wbr /> SET NOCOUNT ON;

<wbr /> <wbr /> <wbr /> &#8212; Output parameter value of 0 indicates that error <wbr />
  
<wbr /> <wbr /> <wbr /> &#8212; information was not logged
  
<wbr /> <wbr /> <wbr /> SET @ErrorLogID = 0;

<wbr /> <wbr /> <wbr /> BEGIN TRY
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8212; Return if there is no error information to log
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> IF ERROR_NUMBER() IS NULL
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> RETURN;

<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8212; Return if inside an uncommittable transaction.
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8212; Data insertion/modification is not allowed when <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8212; a transaction is in an uncommittable state.
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> IF XACT_STATE() = -1
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> BEGIN
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> PRINT &#8216;Cannot log error since the current transaction is in an uncommittable state. &#8216; <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> + &#8216;Rollback the transaction before executing uspLogError in order to successfully log error information.&#8217;;
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> RETURN;
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> END

<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> INSERT [dbo].[OperateErrorLog] <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> (
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> [OperateName], <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> [ErrorNumber], <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> [ErrorSeverity], <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> [ErrorState], <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> [ErrorProcedure], <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> [ErrorLine], <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> [ErrorMessage]
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ) <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> VALUES <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> (
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> CONVERT(sysname, CURRENT_USER), <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ERROR_NUMBER(),
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ERROR_SEVERITY(),
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ERROR_STATE(),
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ERROR_PROCEDURE(),
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ERROR_LINE(),
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> ERROR_MESSAGE()
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> );
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> SET @ErrorLogID = @@IDENTITY;
  
<wbr /> <wbr /> <wbr /> END TRY
  
<wbr /> <wbr /> <wbr /> BEGIN CATCH
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> PRINT &#8216;An error occurred in stored procedure uspLogError: &#8216;;
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> EXECUTE YourPrintErrorProcedure;&#8212;&#8212;&#8212;&#8212;&#8212;&#8211;打印错误信息的存储过程
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> RETURN -1;
  
<wbr /> <wbr /> <wbr /> END CATCH
  
END;

<wbr />

CREATE PROCEDURE YourPrintErrorProcedure
  
AS
  
BEGIN
  
<wbr /> <wbr /> <wbr /> SET NOCOUNT ON;

<wbr /> <wbr /> <wbr /> &#8212; Print error information. <wbr />
  
<wbr /> <wbr /> <wbr /> PRINT &#8216;Error &#8216; + CONVERT(varchar(50), ERROR_NUMBER()) +
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216;, Severity &#8216; + CONVERT(varchar(5), ERROR_SEVERITY()) +
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216;, State &#8216; + CONVERT(varchar(5), ERROR_STATE()) + <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216;, Procedure &#8216; + ISNULL(ERROR_PROCEDURE(), &#8216;-&#8216;) + <wbr />
  
<wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> &#8216;, Line &#8216; + CONVERT(varchar(5), ERROR_LINE());
  
<wbr /> <wbr /> <wbr /> PRINT ERROR_MESSAGE();
  
END;

CREATE TABLE \[dbo].[ErrorLog\](
  
<wbr /> <wbr /> <wbr /> \[ErrorLogID\] \[int\] IDENTITY(1,1) NOT NULL,
  
<wbr /> <wbr /> <wbr /> \[ErrorTime\] \[datetime\] NOT NULL CONSTRAINT [DF\_ErrorLog\_ErrorTime] <wbr /> DEFAULT (getdate()),
  
<wbr /> <wbr /> <wbr /> \[UserName\] \[sysname\] COLLATE Chinese\_PRC\_CI_AS NOT NULL,
  
<wbr /> <wbr /> <wbr /> \[ErrorNumber\] \[int\] NOT NULL,
  
<wbr /> <wbr /> <wbr /> \[ErrorSeverity\] \[int\] NULL,
  
<wbr /> <wbr /> <wbr /> \[ErrorState\] \[int\] NULL,
  
<wbr /> <wbr /> <wbr /> \[ErrorProcedure] [nvarchar\](126) COLLATE Chinese\_PRC\_CI_AS NULL,
  
<wbr /> <wbr /> <wbr /> \[ErrorLine\] \[int\] NULL,
  
<wbr /> <wbr /> <wbr /> \[ErrorMessage] [nvarchar\](4000) COLLATE Chinese\_PRC\_CI_AS NOT NULL,
  
<wbr />CONSTRAINT [PK\_ErrorLog\_ErrorLogID] PRIMARY KEY CLUSTERED <wbr />
  
(
  
<wbr /> <wbr /> <wbr /> [ErrorLogID] ASC
  
)WITH (IGNORE\_DUP\_KEY = OFF) ON [PRIMARY]
  
) ON [PRIMARY]



<wbr />

下面系统函数在CATCH块有效.可以用来得到更多的错误信息:

<table>
  <tr>
    <th>
      函数
    </th>
    
    <th>
      描述
    </th>
  </tr>
  
  <tr>
    <td>
      ERROR_NUMBER()
    </td>
    
    <td>
      返回导致运行 CATCH 块的错误消息的错误号。
    </td>
  </tr>
  
  <tr>
    <td>
      ERROR_SEVERITY()
    </td>
    
    <td>
      返回导致 CATCH 块运行的错误消息的严重级别
    </td>
  </tr>
  
  <tr>
    <td>
      ERROR_STATE()
    </td>
    
    <td>
      返回导致 CATCH 块运行的错误消息的状态号
    </td>
  </tr>
  
  <tr>
    <td>
      ERROR_PROCEDURE()
    </td>
    
    <td>
      返回出现错误的存储过程名称
    </td>
  </tr>
  
  <tr>
    <td>
      ERROR_LINE()
    </td>
    
    <td>
      返回发生错误的行号
    </td>
  </tr>
  
  <tr>
    <td>
      ERROR_MESSAGE()
    </td>
    
    <td>
      返回导致 CATCH 块运行的错误消息的完整文本
    </td>
  </tr>
</table>

 [1]: http://blog.csdn.net/WeiZhang_son_Ding/archive/2010/02/05/5291732.aspx