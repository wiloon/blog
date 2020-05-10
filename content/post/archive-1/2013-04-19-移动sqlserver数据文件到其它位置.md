---
title: 移动SQLSERVER数据文件到其它位置
author: wiloon
type: post
date: 2013-04-19T09:31:31+00:00
url: /?p=5414
categories:
  - DataBase

---
### 

<div>
  <div id="main-content">
    <div>
      <p>
        Follow the steps outlined below to move the SQL Server Data File(s):
      </p>
      
      <ol>
        <li>
          Make a backup of all current databases, and the current master databases.
        </li>
        <li>
          Must have System Administrator permissions (SA).
        </li>
        <li>
          Make sure the SQL Server Agent service is not currently running.
        </li>
        <li>
          Run the Detach statement on the desired database: <ul>
            <li>
              Use Master
            </li>
            <li>
              GO
            </li>
            <li>
              sp_detach_db &#8216;database name&#8217;
            </li>
            <li>
              GO
            </li>
          </ul>
        </li>
        
        <li>
          Now, copy the data files and the log files from the correct location to the new location. <p>
            <b>NOTE:</b> If the database that you are moving has more then one data file or log file, specify the files in comma-delimited list in the sp_attach_db stored procedure step.</li> 
            
            <li>
              Re-attach the database. Point to the files in the new location <ul>
                <li>
                  Use Master
                </li>
                <li>
                  GO
                </li>
                <li>
                  sp_attach_db &#8216;database name&#8217;, &#8216;D:SQLDATADatabaseName.mdf&#8217;, &#8216;D:SQLDATADatabaseName.ldf&#8217;
                </li>
                <li>
                  GO
                </li>
              </ul>
            </li></ol> 
            
            <p>
              See, Microsoft knowledge base article for further information on how to Detach and Attach databases in SQL Server.<br /> 参考：
            </p>
            
            <p>
              <a href="http://support.microsoft.com/kb/965095/en-us">http://support.microsoft.com/kb/965095/en-us</a>
            </p>
            
            <p>
              <a href="http://server.chinabyte.com/216/11420716.shtml">http://server.chinabyte.com/216/11420716.shtml</a>
            </p>
            
            <p>
              <a href="http://support.microsoft.com/?scid=kb;zh-cn;224071&spid=2852&sid=521">http://support.microsoft.com/?scid=kb;zh-cn;224071&spid=2852&sid=521</a>
            </p></div> </div> </div>