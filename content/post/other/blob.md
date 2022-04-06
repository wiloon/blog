---
title: BLOB
author: "-"
date: 2013-01-15T15:22:28+00:00
url: /?p=5020
categories:
  - DataBase

tags:
  - reprint
---
## BLOB

  BLOB (binary large object)，二进制大对象，是一个可以存储二进制文件的容器。


  在计算机中，BLOB常常是数据库中用来存储二进制文件的字段类型。


  BLOB是一个大文件，典型的BLOB是一张图片或一个声音文件，由于它们的尺寸，必须使用特殊的方式来处理 (例如: 上传、下载或者存放到一个数据库) 。


  根据Eric Raymond的说法，处理BLOB的主要思想就是让文件处理器 (如数据库管理器) 不去理会文件是什么，而是关心如何去处理它。


  但也有专家强调，这种处理大数据对象的方法是把双刃剑，它有可能引发一些问题，如存储的二进制文件过大，会使数据库的性能下降。在数据库中存放体积较大的多媒体对象就是应用程序处理BLOB的典型例子。 
  
    大型对象
  
  
    BLOB就是使用二进制保存数据。
  
  
    如: 保存位图。
  
  
    CLOB使用CHAR来保存数据。
  
  
    如: 保存XML文档。
  
  
    
      Oracle中的BLOB和CLOB
  
  
    
      LONG: 可变长的字符串数据，最长2G，LONG具有VARCHAR2列的特性，可以存储长文本一个表中最多一个LONG列
 LONG RAW: 可变长二进制数据，最长2G
 CLOB:  字符大对象Clob 用来存储单字节的字符数据
 NCLOB: 用来存储多字节的字符数据
 BLOB: 用于存储二进制数据
 BFILE: 存储在文件中的二进制数据，这个文件中的数据只能被只读访。但该文件不包含在数据库内。
    
    
    
      bfile字段实际的文件存储在文件系统中,字段中存储的是文件定位指针.bfile对oracle来说是只读的,也不参与事务性控制和数据恢复.
    
    
    
      CLOB，NCLOB，BLOB都是内部的LOB(Large Object)类型，最长4G，没有LONG只能有一列的限制
    
    
    
      要保存图片、文本文件、Word文件各自最好用哪种数据类型?
 -BLOB最好，LONGRAW也不错，但Long是oracle将要废弃的类型，因此建议用BLOB。
  
  
    Blob是指二进制大对象也就是英文Binary Large Object的所写，而Clob是指大字符对象也就是英文Character Large Object的所写。由此可见这辆个类型都是用来存储大量数据而设计的，其中BLOB是用来存储大量二进制数据的；CLOB用来存储大量文本数据。
 那么有人肯定要问既然已经有VARCHAR和VARBINARY两中类型，为什么还要再使用另外的两种类型呢？其实问题很简单，VARCHAR和VARBINARY两种类型是有自己的局限性的。首先说这两种类型的长度还是有限的不可以超过一定的限额，以VARCHAR再ORA中为例长度不可以超过4000；那么有人又要问了，LONGVARCHAR类型作为数据库中的一种存储字符的类型可以满足要求，存储很长的字符，那为什么非要出现CLOB类型呢？其实如果你用过LONGVARCHAR类型就不难发现，该类型的一个重要缺陷就是不可以使用LIKE这样的条件检索。 (稍候将介绍在CLOB中如何实现类似LIKE的模糊查找) 另外除了上述的问题外，还又一个问题，就是在数据库中VARCHAR和VARBINARY的存取是将全部内容从全部读取或写入，对于100K或者说更大数据来说这样的读写方式，远不如用流进行读写来得更现实一些。
 在JDBC中有两个接口对应数据库中的BLOB和CLOB类型，java.sql.Blob和java.sql.Clob。和你平常使用数据库一样你可以直接通过ResultSet.getBlob()方法来获取该接口的对象。与平时的查找唯一不同的是得到Blob或Clob的对象后，我们并没有得到任何数据，但是我们可以这两个接口中的方法得到数据
 例如: 
 Blob b=resultSet.getBlob(1);
 InputStream bin=b.getBinaryStryeam();
 Clob c=resultSet.getClob(2);
 Reader cReader=c.getCharacterStream():
 关于Clob类型的读取可以使用更直接的方法，就是直接通过ResultSet.getCharacterStream();方法获得字符流，但该方法并不安全，所以建议还是使用上面例子的方法获取Reader。
 另外还有一种获取方法，不使用数据流，而是使用数据块。
 例如
 Blob b=resultSet.getBlob(1);
 byte data=b.getByte(0,b.length());
 Clob c=resultSet.getClob(2);
 String str=c.getSubString(0,c.length()):
 在这里我要说明一下，这个方法其实并不安全，如果你很细心的话，那很容易就能发现getByte()和getSubString()两个方法中的第二个参数都是int类型的，而BLOB和CLOB是用来存储大量数据的。而且Bolb.length()和Clob.length()的返回值都是long类型的，所以很不安全。这里不建议使用。但为什么要在这里提到这个方法呢？稍候告诉你答案，这里你需要记住使用数据块是一种方法。 
    
    
      在存储的时候也同样的在PreparedStatement和CallableStatememt中，以参数的形式使用setBlob()和setClob方法把Blob和Clob对象作为参数传递给SQL。这听起来似乎很简单对吧，但是并非我们想象的这样，很不幸由于这两个类型的特殊，JDBC并没有提供独立于数据库驱动的Blob和Clob建立对象。因此需要自己编写与驱动有关的代码，但这样又牵掣到移植性。怎样才是解决办法呢？这就要用到前面说过的思想了使用数据块进行写操作。同样用PreparedStatement和CallableStatememt类，但参数的设置可以换为setAsciiStream、setBinaryStream、setCharacterStream、setObject (当然前3个同样存在长度的问题) 
 下面给大家个例子以方便大家理解
 public void insertFile(File f)  throws Exception{
 FileInputStream fis=new FileInputStream(f,Connection conn);
 byte[] buffer=new byte[1024];
 data=null;
 int sept=0;int len=0;
    
    
    
      while((sept=fis.read(buffer))!=-1){
 if(data==null){
 len=sept;
 data=buffer;
 }else{
 byte[] temp;
 int tempLength;
    
    
    
      tempLength=len+sept;
 temp=new byte[tempLength];
 System.arraycopy(data,0,temp,0,len);
 System.arraycopy(buffer,0,temp,len,sept);
 data=temp;
 len=tempLength;
 }
 if(len!=data.length()){
 byte temp=new byte[len];
 System.arraycopy(data,0,temp,0,len);
 data=temp;
 }
 }
 String sql="insert into fileData (filename,blobData) value(?,?)";
 PreparedStatement ps=conn.prepareStatement(sql);
 ps.setString(1,f.getName());
 ps.setObject(2,data);
 ps.executeUpdate();
    
    
    
      }
    
    
    
      最后由于刚刚说过Clob类型读取字符的长度问题，这里再给大家一段代码，希望对你有帮助
 public static String getClobString(ResultSet rs, int col) {
 try {
 Clob c=resultSet.getClob(2);
 Reader reader=c.getCharacterStream():
 if (reader == null) {
 return null;
 }
 StringBuffer sb = new StringBuffer();
 char[] charbuf = new char[4096];
 for (int i = reader.read(charbuf); i > 0; i = reader.read(charbuf)) {
 sb.append(charbuf, 0, i);
 }
 return sb.toString();
 } catch (Exception e) {
 return "";
 }
 }
    
    
    
      另外似乎前面还提到过LIKE检索的问题。LONGVARCHAR类型中不可以用LIKE查找 (至少ORA中不可以使用，其他的数据库我没有试过) ，在ORA中我们可以使用这样一个函数dbms_lob.instr来代替LIKE来个例子吧
    
    
    
      select docid,dat0 from text where dbms_lob.instr(dat0,'魏',1,1)>0
    
    
    
      在text表中有两个字段docid用来放文档编号dat0为clob类型存放文章内容；这句话的意思就是检索第一条dat0中出现第一次"魏"字的数据。听起来这个检索的数据有点象google的"手气不错"
    
    
    
      以上只是对数据库中比较特殊的两个类型做了简单的说明，希望能对你有所帮助，如果有什么不对的地方也请各位指出，可以通过邮件联系我zuyingwei@hotmail.com
  
  
  
  
    http://jelly.iteye.com/blog/65796
  
  
    http://whycloud.iteye.com/blog/26483
  
