---
title: ibatis 升级到mybatis
author: "-"
date: 2019-12-12T10:05:39+00:00
url: /?p=15204
categories:
  - Uncategorized

tags:
  - reprint
---
## ibatis 升级到mybatis
https://blog.csdn.net/u010856276/article/details/82146607

ibatis升级到mybatis，不是简单的升级包就OK了，为什么这么说呢？因为升级后，调用接口变了，配置文件的写法也变了，所以从某种程度来说，

mybatis不是ibatis的升级版，只是一个家族出来的，长得像而已，升级的工作量还是很大的。

下面我们就来实际升级一下，毕竟ibatis最终是要淘汰的，同时mybatis也给我们在日常开发中提高了工作效率。

升级流程如下: 

1. 移出项目中的ibatis相关包: 

ibatis相关包其实只有一个包，即: ibatis-sqlmap-x.x.x.jar，各项目因版本而；如果项目同时使用了spring集成包spring-orm-x.x.x.jar，也一并移出。

2. 引入mybatis相关包依赖到项目中: 

mybatis相关包其实只有一个包，即: mybatis-x.x.x.jar，但我们一般是和spring一起集成使用mybatis的，这样能方便使用spring提供的事务管理特性，所以还需要引入mybatis-spring-x.x.x.jar

在maven的pom,xml引入配置如下

<dependency>
    
<groupId>org.mybatis</groupId>
    
mybatis</artifactId>
    
<version>3.4.6</version>
   
</dependency>
   
<dependency>
    
<groupId>org.mybatis</groupId>
    
mybatis-spring</artifactId>
    
<version>1.3.2</version>
   
</dependency>
  
3. 移出项目中的ibatis相关配置及文件 (与spring集成为样例) : 

<bean id="sqlMapClient" class="com.common.sqlmap.DynSqlMapClientFactoryBean"> <property name="configLocations">  <value>classpath:common-sqlmap-config.xml</value>
      
<value>classpath*:ibatis-sqlmap-config.xml</value> </list> </property> <property name="dynamicDataSource" ref="dataSource_dyn"> </property> </bean>
  
同时移出common-sqlmap-config.xml和ibatis-sqlmap-config.xml

4. 在项目中添加mybatis的相关配置及文件: 

    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="dataSource" />
        <property name="configLocation" value="classpath:mybatis-config.xml" />
        <property name="mapperLocations" value="classpath*:mapper/**/*.xml" />
    </bean>
    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="sqlSessionFactoryBeanName" value="sqlSessionFactory" />
        <property name="basePackage" value="com.demo.dao" />
    </bean>
    

同时在项目资源根目录下添加mybatis-config.xml，新建mapper目录用于存放SQL映射文件

mybatis-config.xml样例
  
<?xml version="1.0" encoding="UTF-8"?>
  
  
<configuration>
   
<typeAliases>
    
<typeAlias type="com.feidee.demo.entity.SyncLabel" alias="SyncLabel" />
   
</typeAliases>
  
</configuration>
  
5. 创建mybatis的SQL映射文件: 

mybatis的SQL映射文件可以从原来ibatis的SQL映射文件拷贝过来，做如下升级修改: 

1.  变为
  
2. sqlMap 变为 mapper
  
3. mapper标签命名空间namespace最好是全类名，这样方便扫描配置使用 (通过MapperScannerConfigurer) 
  
4. typeAlias标签在mybatis的已不支持，可放入公共配置文件的typeAliases标签中
  
5. resultMap标签中的属性变化 class 变为 type
  
6. jdbcType值在mybatis不支持LONG 变为 BIGINT，Boolean 变为 BOOLEAN
  
7. resultMap标签中result标签移出属性nullValue
  
8. insert select、update、delete标签中的属性 parameterClass 变为 parameterType，resultClass 变为 resultType
  
9. #appName:VARCHAR# 变为 #{appName,jdbcType=VARCHAR} ，自己领悟^=^
  
10. #appName# 变为 #{appName} ，自己领悟^=^
  
11.  变为 会自动处理所有条件的第一个and，即切掉
  
12. … 变为 and …， 要放在where标签里才能处理条件的第一个and
  
13. … 变为 and …，mybatis是基于OGNL表达试比较的
  
14. userIds[]userIds[] 变为 ${item}

以上列举的只是涵盖大部分的修改，如有有未提及需要进一步完善总结。

不过，mybatis的官方文档还是需要再学习的，这是解决问题的根本，以下是学习链接

XML 映射配置文件 http://www.mybatis.org/mybatis-3/zh/configuration.html
  
Mapper XML 文件 http://www.mybatis.org/mybatis-3/zh/sqlmap-xml.html
  
动态 SQL http://www.mybatis.org/mybatis-3/zh/dynamic-sql.html

6. 删除dao的实现类及配置

升级mybatis后是可以不需要dao的实现类的，使用MapperScannerConfigurer扫描加载 (见步骤4中的配置) ，等价升级完dao在service中的使用后，删除dao实现类。

注意: dao接口中的方法不支持方法重载，等价升级完dao在service中的使用要注意dao的参数问题，如果接口是多参数，可以转换接口参数为map或对参数使用注解。

多参数接口方法使用注解样例如下: 

import org.apache.ibatis.annotations.Param;
  
import com.backup_restore.entity.BackupLog;
  
import com.backup_restore.entity.RestoreLog;

public interface DataDao {
      
void insertBackupLog(BackupLog log);
      
int deleteBackupLog(@Param("bookId") long bookId, @Param("id") long id);
      
void insertRestoreLog(RestoreLog log);
      
int resetSyncLabel(long bookId);
  
}
  
以下给出升级前后的样例文件: 

在ibatis中是这样的

<?xml version="1.0" encoding="UTF-8" ?>
  
  
<sqlMap namespace="SyncLabel">
   
<typeAlias alias="syncLabelClass" type="com.demo.entity.SyncLabel" />
   
<resultMap id="syncLabelResult" class="syncLabelClass">
       
<result column="FID" jdbcType="INTEGER" property="id" nullValue="0" />
       
<result column="FUserName" jdbcType="VARCHAR" property="userName" />
       
<result column="FBookId" jdbcType="LONG" property="bookId" />
       
<result column="FRestored" jdbcType="INTEGER" property="restored" />
       
<result column="FLabel" jdbcType="VARCHAR" property="label" />
       
<result column="FMirror" jdbcType="VARCHAR" property="mirror" />       
<result column="FLastModifyTime" jdbcType="TIMESTAMP" property="lastModifyTime" />
   
</resultMap>

<sql id="selectSyncLabelForm">
    
 select FID, FUserName, FBookId, FRestored, FLabel, FMirror, FLastModifyTime from t_sync_label 
   
</sql>

<insert id="addSyncLabel" parameterClass="syncLabelClass">
      
<![CDATA[
         
insert into t_sync_label (FUserName, FBookId, FRestored, FLabel, FMirror, FLastModifyTime)
         
values (#userName:VARCHAR#, #bookId:LONG#, #restored#, #label:VARCHAR#, #mirror#, #syncCount#, #lastModifyTime:TIMESTAMP#)
      
]]>
      
<selectKey keyProperty="id" resultClass="int">
         
SELECT LAST_INSERT_ID() as value
      
</selectKey>
   
</insert>

<select id="listSyncLabel" parameterClass="java.util.Map" resultMap="syncLabelResult">
 <include refid="selectSyncLabelForm"/>
 <dynamic prepend="WHERE">
 <isNotEmpty property="appName" prepend="AND">
 FAppName = #appName#
 </isNotEmpty>
 <isNotEmpty property="udid" prepend="AND">
 FUDID = #udid#
 </isNotEmpty>
 <isNotEmpty property="bookId" prepend="AND">
 FBookId = #bookId#
 </isNotEmpty>
 </dynamic>
 </select>

<select id="getSyncLabelByLabel" parameterClass="String" resultMap="syncLabelResult">
 <include refid="selectSyncLabelForm"/>
 where FLabel = #label# limit 0,1
 </select>

<update id="modifySyncLabel" parameterClass="syncLabelClass">
    
update t_sync_label
    
set FLabel = #label:VARCHAR#, FTimestamp = #timestamp:LONG#,
    
FLastModifyTime = #lastModifyTime:TIMESTAMP#,
    
FVersion = #version#,
    
fmirror = #mirror#,
FBookId = #bookId#, FRestored = #restored#
    
where FID = #id:INTEGER#
   
</update>

<update id="resetSyncLabel" parameterClass="java.util.Map">
    
update t_sync_label set FLabel = "", FTimestamp = 0 ,fmirror = null
    
<dynamic prepend="WHERE">
     
<isNotEmpty property="appName" prepend="AND">
      
FAppName = #appName#
     
</isNotEmpty>
     
<isNotEmpty property="udid" prepend="AND">
      
FUDID = #udid#
     
</isNotEmpty>
     
<isNotEmpty property="bookId" prepend="AND">
      
FBookId = #bookId#
     
</isNotEmpty>
    
</dynamic>
   
</update>

<insert id="insertBookSyncCount" parameterClass="java.util.Map">
       
insert into t_sync_book (FSyncCount, FSyncType, FTradingEntity, FCreateTime, FLastModifyTime)
       
values (#syncCount#, #syncType#, #bookId#, now(), now())
   
</insert>

<delete id="deleteLabel" parameterClass="java.lang.Long">
    
DELETE FROM t_sync_label WHERE FID = #labelId#
   
</delete>
  
</sqlMap>
  
在mybatis中是这样的

<?xml version="1.0" encoding="UTF-8"?>
  
  
<mapper namespace="com.money.movedata.mapper.SyncLabelDao"> <resultMap id="syncLabelResult" type="com.money.movedata.entity.SyncLabel">
       
<result column="FID" jdbcType="INTEGER" property="id" />
       
<result column="FUserName" jdbcType="VARCHAR" property="userName" />
       
<result column="FBookId" jdbcType="BIGINT" property="bookId" />
       
<result column="FRestored" jdbcType="INTEGER" property="restored" />
       
<result column="FLabel" jdbcType="VARCHAR" property="label" />
       
<result column="FMirror" jdbcType="VARCHAR" property="mirror" />
       
<result column="FSyncCount" jdbcType="INTEGER" property="syncCount" />
       
<result column="FLastModifyTime" jdbcType="TIMESTAMP" property="lastModifyTime" />
   
</resultMap>

<sql id="selectSyncLabelForm">
    
 select FID, FUserName, FBookId, FRestored, FLabel, FMirror, FSyncCount, FLastModifyTime from t_sync_label 
   
</sql>

<!-- 添加同步标签 -->

   
<insert id="addSyncLabel" parameterType="SyncLabel">
       
<![CDATA[
         
insert into t_sync_label (FUserName, FBookId,
         
FRestored, FLabel, FMirror, FSyncCount, FLastModifyTime)
         
values (#{userName,jdbcType=VARCHAR}, #{bookId,jdbcType=BIGINT},
          
#{restored}, #{label,jdbcType=VARCHAR}, #{mirror}, #{syncCount}, #{lastModifyTime,jdbcType=TIMESTAMP})
       
]]>
       
<selectKey keyProperty="id" resultType="int">
         
SELECT LAST_INSERT_ID() as value
       
</selectKey>
   
</insert>

<select id="listSyncLabel" parameterType="java.util.Map" resultMap="syncLabelResult">
 <include refid="selectSyncLabelForm"/>
 <where>
 <if test="appName != null and appName != ''">
 FAppName = #{appName}
 </if>
 <if test="udid != null and udid != ''">
 and FUDID = #{udid}
 </if>
 <if test="bookId != null and bookId != ''">
 and FBookId = #{bookId}
 </if>
 </where>
 </select>

<select id="getSyncLabelByLabel" parameterType="String" resultMap="syncLabelResult">
 <include refid="selectSyncLabelForm"/>
 where FLabel = #{label} limit 0,1
 </select>

<update id="modifySyncLabel" parameterType="SyncLabel">
    
update t_sync_label
    
set FLabel = #{label,jdbcType=VARCHAR}, FTimestamp = #{timestamp,jdbcType=BIGINT},
    
FLastModifyTime = #{lastModifyTime,jdbcType=TIMESTAMP},
    
FVersion = #{version},
    
fmirror = #{mirror},
    
FSyncCount = #{syncCount},
    
FBookId = #{bookId}, FRestored = #{restored}
    
where FID = #{id,jdbcType=INTEGER}
   
</update>
   
<update id="resetSyncLabel" parameterType="java.util.Map">
    
update t_sync_label set FLabel = "", FTimestamp = 0 ,fmirror = null
    
<where>
     
<if test="appName != null and appName != ''">
      
FAppName = #{appName}
     
</if>
     
<if test="udid != null and udid != ''">
      
and FUDID = #{udid}
     
</if>
     
<if test="bookId != null and bookId != ''">
      
and FBookId = #{bookId}
     
</if>
    
</where>
   
</update>

<insert id="insertBookSyncCount" parameterType="java.util.Map">
       
insert into t_sync_book (FSyncCount, FSyncType,
       
FTradingEntity, FCreateTime, FLastModifyTime)
       
values (#{syncCount}, #{syncType}, #{bookId}, now(), now())
   
</insert>

<delete id="deleteLabel" parameterType="java.lang.Long">
    
DELETE FROM t_sync_label WHERE FID = #{labelId}
   
</delete>
  
</mapper> ————————————————
  
版权声明: 本文为CSDN博主「码类人生」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/u010856276/article/details/82146607