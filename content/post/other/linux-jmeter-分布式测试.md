---
title: linux jmeter 分布式测试
author: "-"
date: 2015-09-16T05:07:36+00:00
url: /?p=8270
categories:
  - Uncategorized

tags:
  - reprint
---
## linux jmeter 分布式测试
http://www.51testing.com/html/55/383255-847895.html


我将使用3台linux测试机部署jmeter,部署方法也是非常简单,打包后放在指定的目录就ok了,
  
先定义了 A服务器:控制机 B C服务器为负载机
  
主意如果要运行jmeter一定要安装1.6以上版本的jdk并正确配置环境变量,
  
首先在bin目录下 启动B C 服务器 jmeter的jmeter-server服务器,如果启动报错请根据报错内容检查对应的环境配置,我这边报错的原因是hosts没有指定地址,
  
jmeter-server正常启动会提示"创建远程服务"
  
接下来是准备测试脚本,可以在windows环境下先创建jmx文件,主意最好不要添加监听器,应为命令行启动的话监听器可能会占用资源而且有没有任何视图效果.
  
将生成好的jmx文件上传到A服务器 jmeter目录的bin目录下,然后在bin目录下创建xx.jtl文件.jtl文件用来接收测试中产生的测试结果
  
好了 现在进bin目录 打入启动命令,当然你也可以用绝对路径来运行启动命令
  
./jmeter -n -t xx.jmx -R B服务器ip,C服务器ip -l $jmeterpath/bin/xx.jtl
  
参数说明 :
  
-n 告诉jmeter使用nogui模式运行测试
  
-t 执行的测试脚本名
  
-R 后面跟随负载机的ip地址 ,注意用逗号隔开
  
-l 后面跟着测试结果记录的路径与文件名,主意这个文件jmeter不会自己创建,请预先创建好,
  
万事俱备 按下回车 ! 就开始虐待你的测试项目吧

测试完成后把xx.jtl文件下载到windows机上在不同的监听器上分析测试结果
  
如果想修改测试脚本,起始也不必把脚本在windows机上打开gui界面修改,直接编辑.jmx文件 你就可以看到许多熟悉的名字,这里就简单介绍几个

</elementProp>
  
<stringProp name="ThreadGroup.num_threads">5</stringProp>
  
<stringProp name="ThreadGroup.ramp_time">5</stringProp>
  
<longProp name="ThreadGroup.start_time">1281132211000</longProp>
  
<longProp name="ThreadGroup.end_time">1281132211000</longProp>
  
<boolProp name="ThreadGroup.scheduler">true</boolProp>
  
<stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
  
<stringProp name="ThreadGroup.duration">60</stringProp>
  
<stringProp name="ThreadGroup.delay">5</stringProp>
  
</ThreadGroup>

看吧xml格式的测试脚本,很清楚则么改了吧
  
ThreadGroup.num_threads 线程数
  
ThreadGroup.ramp_time 全部线程启动完成的时间
  
ThreadGroup.duration 测试的持续时间
  
还是很容易看明白的.哈哈

这次测试运维把tomcat的内存占用开到了36g 并发线程开到了500万
  
但是最终在jmeter800线程的压力下还是变成了僵尸进程.