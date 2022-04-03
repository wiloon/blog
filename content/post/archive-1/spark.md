---
title: Spark
author: "-"
date: 2015-08-28T10:00:55+00:00
url: /?p=8184
categories:
  - Uncategorized

tags:
  - reprint
---
## Spark
http://www.cnblogs.com/jerrylead/archive/2012/08/13/2636115.html
  
摘要: Spark是继Hadoop之后的新一代大数据分布式处理框架，由UC Berkeley的Matei Zaharia主导开发。我只能说是神一样的人物造就的神器，详情请猛击http://www.spark-project.org/
  
Created 2012-05-09

Modified 2012-08-13

1 Scala安装
  
当前，Spark最新版本是0.5，由于我写这篇文档时，版本还是0.4，因此本文下面的所有描述基于0.4版本。

不过淘宝的达人已经尝试了0.5，并写了相关安装文档在此http://rdc.taobao.com/team/jm/archives/tag/spark。

~~~~~~~~~~~~~~~以下开始我的安装文档~~~~~~~~~~~~~~

我使用的Spark的版本是0.4，只存在于github上，该版本使用的Scala版本是0.9.1.final。所以先到http://www.scala-lang.org/node/165下载scala-2.9.1.final.tar.gz。解压后放到本地 /opt 下面，在 /etc/profile 里添加

export SCALA_HOME=/opt/scala-2.9.1.final

export PATH=$SCALA_HOME/bin:$PATH

2 git安装
  
由于下载Spark和编译Spark需要git，因此先安装git，安装方法可以到Ubuntu软件中心直接装，也可以apt-get装。装好后需要到https://github.com 去注册一个帐号，我注册的是JerryLead，注册邮箱和密码，然后根据网站上的get-start提示生成RSA密码。

注意: 如果本地之前存在rsa_id.pub，authorized_keys等，将其保存或着将原来的密码生成为dsa形式，这样git和原来的密码都不冲突。

3 Spark安装
  
首先下载最新的源代码

git clone git://github.com/mesos/spark.git
  
得到目录spark后，进入spark目录，进入conf子目录，将 spark-env.sh-template 重命名为spark-env.sh，并添加以下代码行: 

export SCALA_HOME=/opt/scala-2.9.1.final
  
回到spark目录，开始编译，运行

$ sbt/sbt update compile
  
这条命令会联网下载很多jar，然后会对spark进行编译，编译完成会提示success

[success] Total time: 1228 s, completed May 9, 2012 3:42:11 PM
  
可以通过运行spark-shell来和spark进行交互。

也可以先运行测试用例./run <class> <params>

./run spark.examples.SparkLR local[2]
  
在本地启动两个线程运行线性回归。

./run spark.examples.SparkPi local
  
在本地启动运行Pi估计器。

更多的例子在examples/src/main/scala里面

3 Spark导出
  
在使用Spark之前，先将编译好的classes导出为jar比较好，可以

$ sbt/sbt assembly
  
将Spark及其依赖包导出为jar，放在

core/target/spark-core-assembly-0.4-SNAPSHOT.jar
  
可以将该jar添加到CLASSPATH里，开发Spark应用了。

一般在开发Spark应用时需要导入Spark一些类和一些隐式的转换，需要再程序开头加入

import spark.SparkContext

import SparkContext._
  
4 使用Spark交互模式
  
1. 运行./spark-shell.sh

2. scala> val data = Array(1, 2, 3, 4, 5) //产生data

data: Array[Int] = Array(1, 2, 3, 4, 5)

3. scala> val distData = sc.parallelize(data) //将data处理成RDD

distData: spark.RDD[Int] = spark.ParallelCollection@7a0ec850  (显示出的类型为RDD) 

4. scala> distData.reduce(_+_) //在RDD上进行运算，对data里面元素进行加和

12/05/10 09:36:20 INFO spark.SparkContext: Starting job...

5. 最后运行得到

12/05/10 09:36:20 INFO spark.SparkContext: Job finished in 0.076729174 s

res2: Int = 15
  
5 使用Spark处理Hadoop Datasets
  
Spark可以从HDFS/local FS/Amazon S3/Hypertable/HBase等创建分布式数据集。Spark支持text files，SequenceFiles和其他Hadoop InputFormat。

比如从HDFS上读取文本创建RDD

scala> val distFile = sc.textFile("hdfs://m120:9000/user/LijieXu/Demo/file01.txt")

12/05/10 09:49:01 INFO mapred.FileInputFormat: Total input paths to process : 1

distFile: spark.RDD[String] = spark.MappedRDD@59bf8a16
  
然后可以统计该文本的字符数，map负责处理文本每一行map(_size)得到每一行的字符数，多行组成一个List，reduce负责将List中的所有元素相加。

scala> distFile.map(_.size).reduce(_+_)

12/05/10 09:50:02 INFO spark.SparkContext: Job finished in 0.139610772 s

res3: Int = 79
  
textFile可以通过设置第二个参数来指定slice个数 (slice与Hadoop里的split/block概念对应，一个task处理一个slice) 。Spark默认将Hadoop上一个block对应为一个slice，但可以调大slice的个数，但不能比block的个数小，这就需要知道HDFS上一个文件的block数目，可以通过50070的dfs的jsp来查看。

对于SequenceFile，可以使用SparkContext的sequenceFile[K,V]方法生成RDD，其中K和V肯定要是SequenceFile存放时的类型了，也就是必须是Writable的子类。Spark也允许使用native types去读取，如sequenceFile[Int, String]。

对于复杂的SequenceFile，可以使用SparkContext.hadoopRDD方法去读取，该方法传入JobConf参数，包含InputFormat，key class，value class等，与Hadoop Java客户端读取方式一样。

6 分布式数据集操作
  
分布式数据集支持两种类型的操作: transformation和action。transformation的意思是从老数据集中生成新的数据集，action是在数据集上进行计算并将结果返回给driver program。每一个Spark应用包含一个driver program用来执行用户的main函数，比如，map就是一个transformation，将大数据集划分处理为小数据集，reduce是action，将数据集上内容进行聚合并返回给driver program。有个例外是reduceByKey应该属于transformation，返回的是分布式数据集。

需要注意的是，Spark的transformation是lazy的，transformation先将操作记录下来，直到接下来的action需要将处理结果返回给driver program的时候。

另一个特性是caching，如果用户指定cache一个数据集RDD，那么该数据集中的不同slice会按照partition被存放到相应不同节点的内存中，这样重用该数据集的时候，效率会高很多，尤其适用于迭代型和交互式的应用。如果cache的RDD丢失，那么重新使用transformation生成。

7 共享变量
  
与Hadoop的MapReduce不同的是，Spark允许共享变量，但只允许两种受限的变量: broadcast和accumulators。

Broadcast顾名思义是"广播"，在每个节点上保持一份read-only的变量。比如，Hadoop的map task需要一部只读词典来处理文本时，由于不存在共享变量，每个task都需要加载一部词典。当然也可以使用DistributedCache来解决。在Spark中，通过broadcast，每个节点存放一部词典就够了，这样从task粒度上升到node粒度，节约的资源可想而知。Spark的broadcast路由算法也考虑到了通信开销。

通过使用SparkContext.broadcast(v)来实现对变量v的包装和共享。
