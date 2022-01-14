---
title: sqlserver 存储过程 try catch TRANSACTION
author: "-"
date: 2013-04-19T07:59:36+00:00
url: /?p=5412
categories:
  - DataBase

---
## sqlserver 存储过程 try catch TRANSACTION
本文来自CSDN博客，转载请标明出处: [http://blog.csdn.net/WeiZhang_son_Ding/archive/2010/02/05/5291732.aspx][1]

CREATE PROCEDURE YourProcedure    

AS
  
BEGIN
  
   SET NOCOUNT ON;

   BEGIN TRY-------开始捕捉异常
  
      BEIN TRAN------开始事务
  
       UPDATE A SET A.names = B.names FROM 表1 AS A INNER JOIN 表2 AS B ON A.id = B.id

       UPDATE A SET A.names = B.names FROM 表1 AS A INNER JOIN 表2 AS B ON A.TEST = B.TEST

   COMMIT TRAN ---提交事务
  
   END TRY----结束捕捉异常
  
   BEGIN CATCH----有异常被捕获
  
       IF @@TRANCOUNT > 0-----判断有没有事务
  
       BEGIN
  
           ROLLBACK TRAN----回滚事务
  
       END 
  
       EXEC YourLogErrorProcedure----执行存储过程将错误信息记录在表当中
  
   END CATCH---结束异常处理
  
END



---------------记录操作错信息的存储过程---------------

CREATE PROCEDURE YourLogErrorProcedure
  
   @ErrorLogID [int] = 0 OUTPUT - contains the ErrorLogID of the row inserted
  
AS                               - by uspLogError in the ErrorLog table
  
BEGIN
  
   SET NOCOUNT ON;

   - Output parameter value of 0 indicates that error 
  
   - information was not logged
  
   SET @ErrorLogID = 0;

   BEGIN TRY
  
       - Return if there is no error information to log
  
       IF ERROR_NUMBER() IS NULL
  
           RETURN;

       - Return if inside an uncommittable transaction.
  
       - Data insertion/modification is not allowed when 
  
       - a transaction is in an uncommittable state.
  
       IF XACT_STATE() = -1
  
       BEGIN
  
           PRINT 'Cannot log error since the current transaction is in an uncommittable state. ' 
  
               + 'Rollback the transaction before executing uspLogError in order to successfully log error information.';
  
           RETURN;
  
       END

       INSERT [dbo].[OperateErrorLog] 
  
           (
  
           [OperateName], 
  
           [ErrorNumber], 
  
           [ErrorSeverity], 
  
           [ErrorState], 
  
           [ErrorProcedure], 
  
           [ErrorLine], 
  
           [ErrorMessage]
  
           ) 
  
       VALUES 
  
           (
  
           CONVERT(sysname, CURRENT_USER), 
  
           ERROR_NUMBER(),
  
           ERROR_SEVERITY(),
  
           ERROR_STATE(),
  
           ERROR_PROCEDURE(),
  
           ERROR_LINE(),
  
           ERROR_MESSAGE()
  
           );
  
       SET @ErrorLogID = @@IDENTITY;
  
   END TRY
  
   BEGIN CATCH
  
       PRINT 'An error occurred in stored procedure uspLogError: ';
  
       EXECUTE YourPrintErrorProcedure;------打印错误信息的存储过程
  
       RETURN -1;
  
   END CATCH
  
END;



CREATE PROCEDURE YourPrintErrorProcedure
  
AS
  
BEGIN
  
   SET NOCOUNT ON;

   - Print error information. 
  
   PRINT 'Error ' + CONVERT(varchar(50), ERROR_NUMBER()) +
  
         ', Severity ' + CONVERT(varchar(5), ERROR_SEVERITY()) +
  
         ', State ' + CONVERT(varchar(5), ERROR_STATE()) + 
  
         ', Procedure ' + ISNULL(ERROR_PROCEDURE(), '-') + 
  
         ', Line ' + CONVERT(varchar(5), ERROR_LINE());
  
   PRINT ERROR_MESSAGE();
  
END;

CREATE TABLE [dbo].[ErrorLog](
  
   [ErrorLogID] [int] IDENTITY(1,1) NOT NULL,
  
   [ErrorTime] [datetime] NOT NULL CONSTRAINT [DF_ErrorLog_ErrorTime]  DEFAULT (getdate()),
  
   [UserName] [sysname] COLLATE Chinese_PRC_CI_AS NOT NULL,
  
   [ErrorNumber] [int] NOT NULL,
  
   [ErrorSeverity] [int] NULL,
  
   [ErrorState] [int] NULL,
  
   [ErrorProcedure] [nvarchar](126) COLLATE Chinese_PRC_CI_AS NULL,
  
   [ErrorLine] [int] NULL,
  
   [ErrorMessage] [nvarchar](4000) COLLATE Chinese_PRC_CI_AS NOT NULL,
  
CONSTRAINT [PK_ErrorLog_ErrorLogID] PRIMARY KEY CLUSTERED 
  
(
  
   [ErrorLogID] ASC
  
)WITH (IGNORE_DUP_KEY = OFF) ON [PRIMARY]
  
) ON [PRIMARY]




下面系统函数在CATCH块有效.可以用来得到更多的错误信息:


  
    <th>
      函数
    </th>
    
    <th>
      描述
    </th>
  
  
  
    
      ERROR_NUMBER()
    
    
    
      返回导致运行 CATCH 块的错误消息的错误号。
    
  
  
  
    
      ERROR_SEVERITY()
    
    
    
      返回导致 CATCH 块运行的错误消息的严重级别
    
  
  
  
    
      ERROR_STATE()
    
    
    
      返回导致 CATCH 块运行的错误消息的状态号
    
  
  
  
    
      ERROR_PROCEDURE()
    
    
    
      返回出现错误的存储过程名称
    
  
  
  
    
      ERROR_LINE()
    
    
    
      返回发生错误的行号
    
  
  
  
    
      ERROR_MESSAGE()
    
    
    
      返回导致 CATCH 块运行的错误消息的完整文本
    
  


 [1]: http://blog.csdn.net/WeiZhang_son_Ding/archive/2010/02/05/5291732.aspx