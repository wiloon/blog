---
title: 移动SQLSERVER数据文件到其它位置
author: "-"
date: 2013-04-19T09:31:31+00:00
url: /?p=5414
categories:
  - DataBase

tags:
  - reprint
---
## 移动SQLSERVER数据文件到其它位置
### 

  
    
      
        Follow the steps outlined below to move the SQL Server Data File(s):
      
      
      
        
          Make a backup of all current databases, and the current master databases.
        
        
          Must have System Administrator permissions (SA).
        
        
          Make sure the SQL Server Agent service is not currently running.
        
        
          Run the Detach statement on the desired database: 
            
              Use Master
            
            
              GO
            
            
              sp_detach_db 'database name'
            
            
              GO
            
          
        
        
        
          Now, copy the data files and the log files from the correct location to the new location. 
            NOTE: If the database that you are moving has more then one data file or log file, specify the files in comma-delimited list in the sp_attach_db stored procedure step. 
            
            
              Re-attach the database. Point to the files in the new location 
                
                  Use Master
                
                
                  GO
                
                
                  sp_attach_db 'database name', 'D:SQLDATADatabaseName.mdf', 'D:SQLDATADatabaseName.ldf'
                
                
                  GO
                
              
             
            
            
              See, Microsoft knowledge base article for further information on how to Detach and Attach databases in SQL Server.
 参考: 
            
            
            
              http://support.microsoft.com/kb/965095/en-us
            
            
            
              http://server.chinabyte.com/216/11420716.shtml
            
            
            
              http://support.microsoft.com/?scid=kb;zh-cn;224071&spid=2852&sid=521
              