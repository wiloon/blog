---
title: "MySQL 显示行号，以及分组排序"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "MySQL 显示行号，以及分组排序"

    CREATE TABLE my_tb (
    id int(11) NOT NULL AUTO_INCREMENT,
    parent_code varchar(255) DEFAULT NULL,
    code varchar(255) DEFAULT NULL,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
    
    INSERT INTO `my_tb` (  `parent_code`, `code`) VALUES ('01', '001');
    INSERT INTO `my_tb` (  `parent_code`, `code`) VALUES ('01', '002');
    INSERT INTO `my_tb` (  `parent_code`, `code`) VALUES ('02', '001');
    INSERT INTO `my_tb` (  `parent_code`, `code`) VALUES ('01', '003');
    INSERT INTO `my_tb` (  `parent_code`, `code`) VALUES ('02', '002');
    INSERT INTO `my_tb` (  `parent_code`, `code`) VALUES ('03', '001');
    INSERT INTO `my_tb` (  `parent_code`, `code`) VALUES ('04', '001');
    
    -- 生成 行号
    select @r:=@r+1 as row_num , a.* from  my_tb a ,(select @r:=0) b
    
    
    
    -- 生成 分组排序号
    
    select  
         @group_row:=CASE when @parent_code=a.parent_code then  @group_row+1 else 1 end as groupRow,
         @parent_code:=a.parent_code as parent_code,
         a.code  
    
      from  my_tb a ,( select @group_row:=1, @parent_code:='') as b
     ORDER BY   a.parent_code , a.code

### 查询结果 

    "groupRow"    "parent_code"    "code"
    "1"    "01"    "001"
    "2"    "01"    "002"
    "3"    "01"    "003"
    "1"    "02"    "001"
    "2"    "02"    "002"
    "1"    "03"    "001"
    "1"    "04"    "001"
    

https://blog.csdn.net/kxjrzyk/article/details/58588000