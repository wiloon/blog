---
title: MyBatis动态传入表名，字段名的解决办法
author: "-"
date: 2013-01-24T06:22:39+00:00
url: /?p=5069
categories:
  - DataBase
  - Java
tags:
  - MyBatis

---
## MyBatis动态传入表名，字段名的解决办法
http://springsfeng.iteye.com/blog/1634234

参考: http://luoyu-ds.iteye.com/blog/1517607


如果要动态传入表名，字段名之类的参数替换SQL语句中的占位副，需要将SQL语句执行改成非预编译的，即: 


  
    
      Xml代码  <img alt="收藏代码" src="http://springsfeng.iteye.com/images/icon_star.png" />
  
  
  
    
       statementType="STATEMENT"
    
    
      >
    
    
          <![DATA[
    
    
              updata user_info_t set ${field} = ${value}
    
    
       where id= ${id}
    
    
    
    
          ]]>
    
    
      </update>
    
  

同时参数Map中需做下面处理: 


  
    
      Java代码  <img alt="收藏代码" src="http://springsfeng.iteye.com/images/icon_star.png" />
  
  
  
    
      Map<String, Object> map = new HashMap<String, Object>();
    
    
              map.put("field", Constant.ISSUED_PLAN_COLUMN_NAME.get(field));
    
    
              map.put("value", "'"+value+"'");  
    
    
    
    
              map.put("id", id);
    
  

