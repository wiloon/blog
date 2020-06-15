---
title: SQL Server中使用异常处理调试存储过程(转)
author: wiloon
type: post
date: 2013-04-19T07:02:21+00:00
url: /?p=5409
categories:
  - DataBase

---



<div id="content">
  异常处理被普遍认为是T-SQL脚本编程中的最弱的方面。幸运的是，这一点在SQL Server 2005中得到了改变，因为SQL Server 2005支持结构化异常处理。本文首先关注新特性“TRY……CATCH”的基本构成，然后在SQL Server 2000和SQL Server 2005中对照着看一些T-SQL的例子，这些例子中使用事务代码故意制造了一些违反约束限制的情况。将来的文章会继续探讨这一主题。　　在SQL Server之前的版本中，你需要在执行INSERT，UPDATE，DELETE之后立即检查全局变量”来处理异常，如果”变量不为零的话（表示有错误），就接着执行一些纠正动作。开发人员常常重复这种与业务逻辑无关的代码，这会导致重复代码块，而且需要与GOTO语句和RETURN语句结合使用。结构化异常处理为控制具有许多动态运行时特性的复杂程序提供了一种强有力的处理机制。目前，这种机制经实践证明是良好的，许多流行的编程语言（比如：微软的Visual Basic.Net和Visual C#）都支持这种异常处理机制。接下来你会在例子中看到，采用了这种健壮的方法以后，会使你的代码可读性和可维护性更好。TRY块包含了可能潜在失败的事务性代码，而CATCH块包含了TRY块中出现错误时执行的代码。如果TRY块中出现了任何错误，执行流程被调转到CATCH块，错误可以被处理，而出错函数可以被用来提供详细的错误信息。TRY……CATCH基本语法如下：
 BEGIN TRY
 RAISERROR （&#8217;Houston, we have a problem&#8217;, 16,1）
 END TRY
 BEGIN CATCH
 SELECT ERROR_NUMBER（） as ERROR_NUMBER,
 ERROR_SEVERITY（） as ERROR_SEVERITY,
 ERROR_STATE（） as ERROR_STATE,
 ERROR_MESSAGE（） as ERROR_MESSAGE
 END CATCH
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />注意上面脚本中函数的用法，我们可以用它们代替局部变量和（或者）全局变量。这些函数只应该被用在CATCH块中，函数功能说明如下：　　ERROR_NUMBER（） 返回错误数量。 
  
  
    ERROR_SEVERITY（） 返回错误严重等级。
  
  
  
    ERROR_STATE（） 返回错误状态号。
  
  
  
    ERROR_PROCEDURE（） 返回出错位置存储过程或者触发器的名称。
  
  
  
    ERROR_LINE（） 返回程序中引起错误的行号。
  
  
  
    ERROR_MESSAGE（） 返回错误信息的完整文本。错误内容包括可替换参数的值，比如：长度，对象名称或者时间。
  
  
  
    我会先用SQL Server 2000演示一个简单例子，然后演示一个SQL Server 2005异常处理的例子。
  
  
  
    下面是一个简单的存储过程示例，先用SQL Server 2000编写，然后改用SQL Server 2005实现。两者都从简单的表开始，我们在对这些表执行插入操作时会违反约束限制。下面是表结构：
  
  
  
    <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />create table dbo.Titles
 （TitleID int Primary Key identity,
 TitleName nvarchar（128） NOT NULL,
 Price money NULL constraint CHK_Price check （Price > 0））
 create table dbo.Authors
 （Authors_ID int primary key identity,
 au_fname nvarchar（32） NULL,
 au_lname nvarchar（64） NULL,
 TitleID int constraint FK_TitleID foreign key
 references Titles（TitleID）,
 CommissionRating int constraint CHK_ValidateCommissionRating
 Check （CommissionRating between 0 and 100））
 create table dbo.Application_Error_Log
 （tablename sysname,
 userName sysname,
 errorNumber int,
 errorSeverity int,
 errorState int,
 errorMessage varchar（4000））
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />存储过程P_Insert_New_BookTitle_2K的源代码
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/ContractedBlock.gif" width="11" height="16" /><img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/ExpandedBlockStart.gif" width="11" height="16" />Code
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />P_Insert_New_BookTitle_2K
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />create proc P_Insert_New_BookTitle_2K
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />(@TitleName nvarchar(128),
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" /> @Price money,
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" /> @au_fname nvarchar(32),
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" /> @au_name nvarchar(64),
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" /> @CommissionRating int)
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />as
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />declare     @err int,
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />        @tablename sysname
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />begin transaction
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />insert dbo.Titles (TitleName, Price)
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />values (@TitleName, @Price)
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />select @err = @@error
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />if @err <> 0
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />begin
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />    select @tablename = &#8216;titles&#8217;
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />    GOTO ERROR_HANDLER
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />end
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />insert dbo.Authors   (au_fname, au_lname, TitleID, CommissionRating)
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />values (@au_fname, @au_fname, @@IDENTITY, @CommissionRating)
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />if @err <> 0
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />begin
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />    select @tablename = &#8216;authhors&#8217;
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />    GOTO ERROR_HANDLER
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />end
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />GOTO EXIT_Proc
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />ERROR_HANDLER:
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />ROLLBACK TRANSACTION
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />&#8212; Log the error
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />insert dbo.Application_Error_Log (tableName, UserName, errorNumber, errorSeverity, errorState)
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />values (@tableName, suser_sname(), @err, 0, 0)
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />EXIT_Proc:
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />commit tran
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 你可以看到，这个存储过程包含了非结构化的错误处理代码，这是我们在SQL Server 2005之前使用的方式。　　我们已经先看到了存储过程P_Insert_New_BookTitle_2K中使用的代码。你顶多能说：“至少我们有异常处理。”下面的语句执行这个SQL Server 2000下的存储过程。
  
  
  
    <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/ContractedBlock.gif" width="11" height="16" /><img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/ExpandedBlockStart.gif" width="11" height="16" />Code
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />exec P_Insert_New_BookTitle_2K &#8216;Red Storm Rising&#8217;,16.99,
 &#8216;Tom&#8217;,&#8217;Clancy&#8217;, 200
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />在用指定的参数执行存储过程时，对Authors表的插入失败了，因为佣金费率值无效。我们的约束检查发现了该无效值，我们可以看到如下错误信息：
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/ContractedBlock.gif" width="11" height="16" /><img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/ExpandedBlockStart.gif" width="11" height="16" />Code
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />Msg 547, Level 16, State 0, Procedure P_Insert_New_BookTitle, Line 23 The INSERT statement conflicted with the CHECK constraint "CHK_ValidateCommissionRating". The conflict occurred in database "Adventureworks2005", table "dbo.Authors", column &#8216;CommissionRating&#8217;. The statement has been terminated.
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />这里的问题是我们不能阻止这些消息被送到客户端。所以判断哪里出错的重担就放到了客户端的头上。令人遗憾的是，在有些情况下，这样的结果对于一些不使用约束限制的应用程序可能足够了。　　我们再来试一次，这次我们使用TRY……CATCH代码块。
  
  
  
    存储过程P_Insert_New_BookTitle_2K5的源代码
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/ContractedBlock.gif" width="11" height="16" /><img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/ExpandedBlockStart.gif" width="11" height="16" />Code
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-P_Insert_New_BookTitle_2K5 &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-create proc P_Insert_New_BookTitle_2K5(@TitleName nvarchar(128), @Price money, @au_fname nvarchar(32), @au_name nvarchar(64), @CommissionRating int)asdeclare @err int, @tablename sysname, @errormessage nvarchar(2000)BEGIN TRY begin transaction select @errormessage = &#8216;insert into Titles table failed&#8217;, @tablename = &#8216;Titles&#8217; insert dbo.Titles (TitleName, Price) values (@TitleName, @Price) select @errormessage = &#8216;insert into Authors table failed&#8217;, @tablename = &#8216;Authors&#8217;insert dbo.Authors (au_fname, au_lname, TitleID, CommissionRating)values (@au_fname, @au_fname, @@IDENTITY, @CommissionRating) commit transactionEND TRYBEGIN CATCH ROLLBACK TRANSACTION &#8212; Log the error insert dbo.Application_Error_Log (UserName, tableName, errorNumber, errorSeverity, errorState, errorMessage) values (suser_sname(), @tableName, ERROR_NUMBER(), ERROR_SEVERITY(), ERROR_STATE(), ERROR_MESSAGE()) RAISERROR (@errormessage, 16,1)END CATCH&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-
 <img alt="" src="http://www.cnblogs.com/Images/OutliningIndicators/None.gif" />
 在这段新改进的存储过程中，我们看到使用了TRY……CATCH代码块的结构化错误处理：　　要注意SQL Server 2005异常处理代码是经过简化的，因此具有更好的可读性和可维护性。不需要剪切和粘贴异常处理代码，也不需要使用GOTO语句。执行该存储过程时，你可以看到如下结果：
  
  
  
    exec P_Insert_New_BookTitle_2K5 &#8216;Red Storm Rising&#8217;,16.99,
 &#8216;Tom&#8217;,&#8217;Clancy&#8217;, 200
 我们用指定的参数执行存储过程，同样因为佣金费率值无效，对Authors表的插入失败了。错误发生时，程序执行流程跳转到了CATCH代码块，在CATCH代码块中我们回滚了事务，然后用SQL Server 2005自带的函数给Application_Error_Log表插入一行日志。　　新的TRY……CATCH代码块无疑使编写处理错误代码更容易，它还可以在任何时候阻止错误信息发送到客户端。当然这可能需要T-SQL程序员的编程思维有一个转变，这是一个绝对有必要使用的特性。要记住迁移SQL Server 2000代码到SQL Server 2005时，如果程序的错误处理机制已经设计为旧的发送错误到客户端的方式，那你可能不得不修改应用程序了。从长远来看，我相信为这种潜在的问题付出努力重新设计是值得的。
 备注：
 http://www.searchdatabase.com.cn/ShowContent_23265.htm
  
  
  
    
  
  
  
    
  
  
  
    
  
  
  
    raiserror  是由单词 raise error 组成
 raise  增加; 提高; 提升
  
  
  
    
  
  
  
    raiserror 的作用： raiserror 是用于抛出一个错误。[ 以下资料来源于sql server 2005的帮助 ] 
    
    
    
    
    
      其语法如下：
    
    
    
      
        RAISERROR ( { msg_id | msg_str | @local_variable }
 { ,severity ,state }
 [ ,argument [ ,&#8230;n ] ]
 )
 [ WITH option [ ,&#8230;n ] ]
      
    
    
    
      
    
    
    
      
    
    
    
    
    
    
      简要说明一下：
    
    
    
      
    
    
    
    
    
    
      
    
    
    
      第一个参数：{ msg_id | msg_str | @local_variable }
 msg_id：表示可以是一个sys.messages表中定义的消息代号；
 使用 sp_addmessage 存储在 sys.messages 目录视图中的用户定义错误消息号。
 用户定义错误消息的错误号应当大于 50000。 
      
      
        msg_str：表示也可以是一个用户定义消息，该错误消息最长可以有 2047 个字符；
 （如果是常量，请使用N&#8217;xxxx&#8217;，因为是nvarchar的）
 当指定 msg_str 时，RAISERROR 将引发一个错误号为 5000 的错误消息。
      
      
      
        @local_variable：表示也可以是按照 msg_str 方式的格式化字符串变量。
      
      
      
        第二个参数：severity
 用户定义的与该消息关联的严重级别。（这个很重要）
 任何用户都可以指定 0 到 18 之间的严重级别。
 [0,10]的闭区间内，不会跳到catch；
 如果是[11,19],则跳到catch；
 如果[20,无穷)，则直接终止数据库连接；
      
      
      
        第三个参数：state
 如果在多个位置引发相同的用户定义错误，
 则针对每个位置使用唯一的状态号有助于找到引发错误的代码段。
      
      
      
        介于 1 至 127 之间的任意整数。（state 默认值为1）
 当state 值为 0 或大于 127 时会生成错误！
      
      
      
        第四个参数：argument
 用于代替 msg_str 或对应于 msg_id 的消息中的定义的变量的参数。
      
      
      
        第五个参数：option
 错误的自定义选项，可以是下表中的任一值：
 LOG ：在错误日志和应用程序日志中记录错误；
 NOWAIT：将消息立即发送给客户端；
 SETERROR：将 @@ERROR 值和 ERROR_NUMBER 值设置为 msg_id 或 50000；
      
      
      
        [SQL]代码示例
      
    
    
    
      
    
    
    
      &#8211;示例1
    
    
    
      
        DECLARE @raiseErrorCode nvarchar(50)
 SET @raiseErrorCode = CONVERT(nvarchar(50), YOUR UNIQUEIDENTIFIER KEY)
 RAISERROR(&#8216;%s INVALID ID. There is no record in table&#8217;,16,1, @raiseErrorCode)
      
    
    
    
      
    
    
    
      
    
    
    
      
    
    
    
      &#8211;示例2
    
    
    
      
        <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
      
      
      
        RAISERROR (
 N&#8217;This is message %s %d.&#8217;, &#8212; Message text,
 10,                        &#8212; Severity,
 1,                         &#8212; State,
 N&#8217;number&#8217;,                 &#8212; First argument.
 5                          &#8212; Second argument.
 );
 &#8212; The message text returned is: This is message number 5.
 GO
      
      
      
        <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
      
    
  
  
  
    
  
  
  
    &#8211;示例3
  
  
  
    
      <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
    
    
    
      RAISERROR (N'<<%*.*s>>&#8217;, &#8212; Message text.
 10,           &#8212; Severity,
 1,            &#8212; State,
 7,            &#8212; First argument used for width.
 3,            &#8212; Second argument used for precision.
 N&#8217;abcde&#8217;);    &#8212; Third argument supplies the string.
 &#8212; The message text returned is: <<    abc>>.
 GO
    
    
    
      <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
    
  
  
  
    
  
  
  
    &#8211;示例4
  
  
  
    
      RAISERROR (N'<<%7.3s>>&#8217;, &#8212; Message text.
 10,           &#8212; Severity,
 1,            &#8212; State,
 N&#8217;abcde&#8217;);    &#8212; First argument supplies the string.
 &#8212; The message text returned is: <<    abc>>.
 GO
    
  
  
  
    
  
  
  
    &#8211;示例5
  
  
  
    &#8211;A. 从 CATCH 块返回错误消息
 以下代码示例显示如何在 TRY 块中使用 RAISERROR 使执行跳至关联的 CATCH 块中。
 它还显示如何使用 RAISERROR 返回有关调用 CATCH 块的错误的信息。
  
  
  
    
      <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
    
    
    
      BEGIN TRY
 RAISERROR (&#8216;Error raised in TRY block.&#8217;, &#8212; Message text.
 16, &#8212; Severity.
 1 &#8212; State.
 );
 END TRY
 BEGIN CATCH
 DECLARE @ErrorMessage NVARCHAR(4000);
 DECLARE @ErrorSeverity INT;
 DECLARE @ErrorState INT; 
      
      
        SELECT
 @ErrorMessage = ERROR_MESSAGE(),
 @ErrorSeverity = ERROR_SEVERITY(),
 @ErrorState = ERROR_STATE();
      
      
      
        RAISERROR (@ErrorMessage,  &#8212; Message text.
 @ErrorSeverity, &#8212; Severity.
 @ErrorState     &#8212; State.
 );
 END CATCH;
      
    
    
    
      <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
    
  
  
  
    
  
  
  
    &#8211;示例6
  
  
  
    &#8211;B. 在 sys.messages 中创建即席消息
 以下示例显示如何引发 sys.messages 目录视图中存储的消息。
 该消息通过 sp_addmessage 系统存储过程，以消息号50005添加到 sys.messages 目录视图中。
  
  
  
    
      <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
    
    
    
      sp_addmessage @msgnum = 50005,
 @severity = 10,
 @msgtext = N'<<%7.3s>>&#8217;;
 GO 
      
      
        RAISERROR (50005, &#8212; Message id.
 10,    &#8212; Severity,
 1,     &#8212; State,
 N&#8217;abcde&#8217;); &#8212; First argument supplies the string.
 &#8212; The message text returned is: <<    abc>>.
 GO
      
      
      
        sp_dropmessage @msgnum = 50005;
 GO
      
    
    
    
      <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
    
  
  
  
    
  
  
  
    &#8211;示例7
 &#8211;C. 使用局部变量提供消息文本
 以下代码示例显示如何使用局部变量为 RAISERROR 语句提供消息文本。
  
  
  
    
      <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
    
    
    
      sp_addmessage @msgnum = 50005,
 @severity = 10,
 @msgtext = N'<<%7.3s>>&#8217;;
 GO 
      
      
        RAISERROR (50005, &#8212; Message id.
 10,    &#8212; Severity,
 1,     &#8212; State,
 N&#8217;abcde&#8217;); &#8212; First argument supplies the string.
 &#8212; The message text returned is: <<    abc>>.
 GO
      
      
      
        sp_dropmessage @msgnum = 50005;
 GO
      
    
    
    
      <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
    
  
  
  
    
  
  
  
    
  
  
  
    参考来源：
  
  
  
    <a title="http://msdn.microsoft.com/zh-cn/library/ms178592.aspx" href="http://msdn.microsoft.com/zh-cn/library/ms178592.aspx">http://msdn.microsoft.com/zh-cn/library/ms178592.aspx</a>
  
  
  
    <a title="ms-help://MS.SQLCC.v9/MS.SQLSVR.v9.zh-CHS/tsqlref9/html/483588bd-021b-4eae-b4ee-216268003e79.htm" href="ms-help://MS.SQLCC.v9/MS.SQLSVR.v9.zh-CHS/tsqlref9/html/483588bd-021b-4eae-b4ee-216268003e79.htm">ms-help://MS.SQLCC.v9/MS.SQLSVR.v9.zh-CHS/tsqlref9/html/483588bd-021b-4eae-b4ee-216268003e79.htm</a>
  
