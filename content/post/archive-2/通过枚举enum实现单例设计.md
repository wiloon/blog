---
title: 通过枚举enum实现单例设计
author: "-"
date: 2017-03-25T09:11:32+00:00
url: /?p=9951
categories:
  - Uncategorized

tags:
  - reprint
---
## 通过枚举enum实现单例设计

默认枚举实例的创建是线程安全的

通过enum关键字来实现枚举,在枚举中需要注意的有: 

1. 枚举中的属性必须放在最前面,一般使用大写字母表示

2. 枚举中可以和java类一样定义方法

3. 枚举中的构造方法必须是私有的

通过一个java类来模拟枚举的功能: 
  
package org.lkl.imitate_enum;

public abstract class WeekDay {
  
public static final WeekDay SUN = new WeekDay() {

@Override
  
public WeekDay nextDay() {
  
return MON;
  
}
  
};
  
public static final WeekDay MON = new WeekDay() {

@Override
  
public WeekDay nextDay() {
  
return SUN;
  
}

};

@Override
  
public String toString() {
  
return this == SUN ?"SUN星期天":"MON星期一" ;
  
}

public abstract WeekDay nextDay();

public static void main(String[] args) {
  
System.out.println(WeekDay.SUN.nextDay());
  
System.out.println(WeekDay.MON.nextDay());
  
}
  
}

4.可以在枚举属性后面添加()来调用指定参数的构造方法,添加{}来实现其对应的匿名内部类,例如: 
  
package org.lkl.imitate_enum;
  
public enum TrafficLamp {
  
RED(30){
  
public TrafficLamp nextLamp() {
  
return GREEN ;
  
}
  
},
  
GREEN(20){
  
public TrafficLamp nextLamp() {
  
return YELLOW ;
  
}
  
},
  
YELLOW(10){
  
public TrafficLamp nextLamp() {
  
return RED ;
  
}
  
} ;
  
public abstract TrafficLamp nextLamp() ;
  
private int time ;
  
private TrafficLamp(int time){
  
this.time = time ;
  
System.out.println(time);
  
}

public static void main(String[] args) {
  
System.out.println(TrafficLamp.GREEN);
  
}
  
}

二、通过枚举来实现单例

实现单例的核心在于private私有化类中的构造方法,在枚举中的构造方法必须是私有的,这就为枚举来实现单例奠定了基础。下面以数据源中获得Connection连接来举例: 

在开发中经常是通过数据源来获得数据库的Connection,数据源的实现方式有多种,最典型的有两种,一种是C3P0,另外一种是DBCP (以后有机会再针对两种数据源进行讨论) ,这里以C3P0数据源为例。由于数据源的创建与销毁都是十分消耗性能的,并且系统中有一个数据源一般就能满足开发的要求,因此要将数据源设计为单例。

采用分散配置,创建一个jdbc.propertis文件,其内容如下: 


driverClass = com.MySQL.jdbc.Driver
  
jdbcUrl = jdbc:MySQL://localhost:3306/liaokailin
  
user = root
  
password = MySQLadmin
  
maxPoolSize = 20
  
minPoolSize = 5
  
创建一个MyDataBaseSource的枚举: 
  
package org.lkl.imitate_enum;

import java.sql.Connection;
  
import java.sql.SQLException;
  
import java.util.ResourceBundle;

import com.mchange.v2.c3p0.ComboPooledDataSource;

public enum MyDataBaseSource {
  
DATASOURCE;
  
private ComboPooledDataSource cpds = null;

private MyDataBaseSource() {
  
try {

/*---获取properties文件内容----*/
  
// 方法一:
  
/*
  
* InputStream is =
  
* MyDBSource.class.getClassLoader().getResourceAsStream("jdbc.properties");
  
* Properties p = new Properties(); p.load(is);
  
* System.out.println(p.getProperty("driverClass") );
  
*/

// 方法二: (不需要properties的后缀)
  
/*
  
* ResourceBundle rb = PropertyResourceBundle.getBundle("jdbc") ;
  
* System.out.println(rb.getString("driverClass"));
  
*/

// 方法三: (不需要properties的后缀)
  
ResourceBundle rs = ResourceBundle.getBundle("jdbc");
  
cpds = new ComboPooledDataSource();
  
cpds = new ComboPooledDataSource();
  
cpds.setDriverClass(rs.getString("driverClass"));
  
cpds.setJdbcUrl(rs.getString("jdbcUrl"));
  
cpds.setUser(rs.getString("user"));
  
cpds.setPassword(rs.getString("password"));
  
cpds.setMaxPoolSize(Integer.parseInt(rs.getString("maxPoolSize")));
  
cpds.setMinPoolSize(Integer.parseInt(rs.getString("minPoolSize")));
  
System.out.println("--调用了构造方法--");
  
;
  
} catch (Exception e) {
  
e.printStackTrace();
  
}
  
}

public Connection getConnection() {
  
try {
  
return cpds.getConnection();
  
} catch (SQLException e) {
  
return null;
  
}
  
}

}

测试代码: 
  
package org.lkl.imitate_enum;

public class Test {
  
public static void main(String[] args) {
  
MyDataBaseSource.DATASOURCE.getConnection() ;
  
MyDataBaseSource.DATASOURCE.getConnection() ;
  
MyDataBaseSource.DATASOURCE.getConnection() ;
  
}
  
}

结果如下: 
  
--调用了构造方法--
  
2013-7-17 17:10:57 com.mchange.v2.c3p0.impl.AbstractPoolBackedDataSource getPoolManager
  
信息: Initializing c3p0 pool... com.mchange.v2.c3p0.ComboPooledDataSource [ acquireIncrement -> 3, acquireRetryAttempts -> 30, acquireRetryDelay -> 1000, autoCommitOnClose -> false, automaticTestTable -> null, breakAfterAcquireFailure -> false, checkoutTimeout -> 0, connectionCustomizerClassName -> null, connectionTesterClassName -> com.mchange.v2.c3p0.impl.DefaultConnectionTester, dataSourceName -> 1hge16d8v1tgb0wppydrzz|2c1e6b, debugUnreturnedConnectionStackTraces -> false, description -> null, driverClass -> com.MySQL.jdbc.Driver, factoryClassLocation -> null, forceIgnoreUnresolvedTransactions -> false, identityToken -> 1hge16d8v1tgb0wppydrzz|2c1e6b, idleConnectionTestPeriod -> 0, initialPoolSize -> 3, jdbcUrl -> jdbc:MySQL://localhost:3306/kaoqin, maxAdministrativeTaskTime -> 0, maxConnectionAge -> 0, maxIdleTime -> 0, maxIdleTimeExcessConnections -> 0, maxPoolSize -> 20, maxStatements -> 0, maxStatementsPerConnection -> 0, minPoolSize -> 5, numHelperThreads -> 3, preferredTestQuery -> null, properties -> {user=\***\*\\*\*, password=\*\*\****}, propertyCycle -> 0, statementCacheNumDeferredCloseThreads -> 0, testConnectionOnCheckin -> false, testConnectionOnCheckout -> false, unreturnedConnectionTimeout -> 0, usesTraditionalReflectiveProxies -> false ]

很显然获得了三个Connection连接,但是只调用了一次枚举的构造方法,从而通过枚举实现了单例的设计


http://www.cnblogs.com/liaokailin/p/3196253.html