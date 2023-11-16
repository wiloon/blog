---
title: golang MySQL
author: "-"
date: 2016-11-23T07:03:04+00:00
url: /?p=9415
categories:
  - Inbox
tags:
  - reprint
---
## golang MySQL

[http://www.cnblogs.com/hupengcool/p/4143238.html](http://www.cnblogs.com/hupengcool/p/4143238.html)

Golang操作数据库

基本概念

```go
Open() – creates a DB
Close() - closes the DB
Query() - 查询
QueryRow() -查询行
Exec() -执行操作,update,insert,delete
Row - A row is not a hash map, but an abstraction of a cursor
Next()
Scan()
```

注意: DB并不是指的一个connection

连接到数据库
  
我们以MySQL为例,使用github.com/go-sql-driver/MySQL,首先我们需要导入我们需要的包

import (
  
"database/sql"
  
_ "github.com/go-sql-driver/MySQL"
  
)
  
注意我们导入github.com/go-sql-driver/MySQL 前面用了一个"_",_操作其实是引入该包,而不直接使用包里面的函数,而是调用了该包里面的init函数,import的时候其实是执行了该包里面的init函数,初始化了里面的变量,_操作只是说该包引入了,我只初始化里面的 init函数和一些变量,但是往往这些init函数里面是注册自己包里面的引擎,让外部可以方便的使用,就很多实现database/sql的包,在 init函数里面都是调用了sql.Register(name string, driver driver.Driver)注册自己,然后外部就可以使用了。
  
我们用Open()函数来打开一个database handle

db, err := sql.Open("MySQL", "user:password@tcp(ip:port)/database")
  
写一个完整的:

import (
  
"database/sql"
  
_ "github.com/go-sql-driver/MySQL"
  
"log"
  
)
  
func main() {
  
db, err := sql.Open("MySQL", "user:password@tcp(ip:port)/database")
  
if err != nil {
  
log.Println(err)
  
}

//在这里进行一些数据库操作

defer db.Close()
  
}
  
我们在执行Open函数的时候,并不会去获得数据库连接有效性,当执行数据库操作的时候才会去连接,当我们需要在Open之后就知道连接的有效性的时候,可以通过Ping()来进行

err = db.Ping()
  
if err != nil {
  
log.Println(err)
  
}
  
我们通常习惯使用Close来关闭数据库连接,但是sql.DB是被设计成长期有效的类型,我们不应该频繁的Open和Close,相反,我们应该建立一个sql.DB,在程序需要进行数据库操作的时候一直使用它,不要在一个方法里面进行Open和Close,应该把sql.DB作为参数传递给方法

进行数据库操作
  
增删改操作
  
Exec()方法一般用于增删改操作,这里以增加为例:

stmt, err := db.Prepare("insert into user(name,age)values(?,?)")
  
if err != nil {
  
log.Println(err)
  
}

rs, err := stmt.Exec("go-test", 12)
  
if err != nil {
  
log.Println(err)
  
}
  
//我们可以获得插入的id
  
id, err := rs.LastInsertId()
  
//可以获得影响行数
  
affect, err := rs.RowsAffected()
  
查询操作
  
一般的查询
  
var name string
  
var age int
  
rows, err := db.Query("select name,age from user where id = ? ", 1)
  
if err != nil {
  
fmt.Println(err)
  
}
  
defer rows.Close()

for rows.Next() {
  
err := rows.Scan(&name, &age)
  
if err != nil {
  
fmt.Println(err)
  
}
  
}

err = rows.Err()
  
if err != nil {
  
fmt.Println(err)
  
}

fmt.Println("name:", url, "age:", description)
  
我们应该养成关闭rows的习惯,在任何时候,都不要忘记rows.Close().哪怕这个rows在确实循环完之后,已经自动关闭掉了,我们定义rows.Close()也是对我们没有坏处的,因为我们无法保证,rows是否会正常的循环完。

查询单条记录,
  
我们使用db.QueryRow()

var name string
  
err = db.QueryRow("select name from user where id = ?", 222).Scan(&name)
  
没有结果的时候会返回err

处理空值
  
我们用一个name字段为空的记录来举例

var name NullString
  
err := db.QueryRow("SELECT name FROM names WHERE id = ?", id).Scan(&name)
  
...
  
if name.Valid {
  
// use name.String
  
} else {
  
// value is NULL
  
}
  
在这种情况下我们通常使用NullString,但是有时候我们并不关心值是不是Null,我们只需要吧他当一个空字符串来对待就行。这时候我们可以使用[]byte (null byte[]可以转化为空string)  或者 sql.RawBytes,

var col1, col2 []byte

for rows.Next() {
  
// Scan the value to []byte
  
err = rows.Scan(&col1, &col2)

if err != nil {
  
panic(err.Error()) // Just for example purpose. You should use proper error handling instead of panic
  
}

// Use the string value
  
fmt.Println(string(col1), string(col2))
  
}
  
使用*sql.RawBytes

package main

import (
  
"database/sql"
  
"fmt"
  
_ "github.com/go-sql-driver/MySQL"
  
)

func main() {
  
// Open database connection
  
db, err := sql.Open("MySQL", "user:password@/dbname")
  
if err != nil {
  
panic(err.Error()) // Just for example purpose. You should use proper error handling instead of panic
  
}
  
defer db.Close()

// Execute the query
  
rows, err := db.Query("SELECT * FROM table")
  
if err != nil {
  
panic(err.Error()) // proper error handling instead of panic in your app
  
}

// Get column names
  
columns, err := rows.Columns()
  
if err != nil {
  
panic(err.Error()) // proper error handling instead of panic in your app
  
}

// Make a slice for the values
  
values := make([]sql.RawBytes, len(columns))

// rows.Scan wants '[]interface{}' as an argument, so we must copy the
  
// references into such a slice
  
// See [http://code.google.com/p/go-wiki/wiki/InterfaceSlice](http://code.google.com/p/go-wiki/wiki/InterfaceSlice) for details
  
scanArgs := make([]interface{}, len(values))
  
for i := range values {
  
scanArgs[i] = &values[i]
  
}

// Fetch rows
  
for rows.Next() {
  
// get RawBytes from data
  
err = rows.Scan(scanArgs...)
  
if err != nil {
  
panic(err.Error()) // proper error handling instead of panic in your app
  
}

// Now do something with the data.
  
// Here we just print each column as a string.
  
var value string
  
for i, col := range values {
  
// Here we can check if the value is nil (NULL value)
  
if col == nil {
  
value = "NULL"
  
} else {
  
value = string(col)
  
}
  
fmt.Println(columns[i], ": ", value)
  
}
  
fmt.Println("------------")
  
}
  
if err = rows.Err(); err != nil {
  
panic(err.Error()) // proper error handling instead of panic in your app
  
}
  
}
  
### 事务
  
使用 db.Begin() 来开启一个事务, 通过 Commit() 和 Rollback() 方法来关闭。

```go
tx := db.Begin()
tx.Rollback()
tx.Commit()
```
  
Exec, Query, QueryRow and Prepare 方法已经全部可以在tx上面使用。使用方法和在*sql.DB是一样的,事务必须以Commit()或者Rollback()结束

The Connection Pool
  
在database/sql中有一个很基本的连接池,你并没有多大的控制权,仅仅可以设置SetMaxIdleConns和SetMaxOpenConns,也就是最大空闲连接和最大连接数。

db.SetMaxIdleConns(n)
  
db.SetMaxOpenConns(n)

database/sql

database/sql是golang的标准库之一,它提供了一系列接口方法,用于访问关系数据库。它并不会提供数据库特有的方法,那些特有的方法交给数据库驱动去实现。

database/sql库提供了一些type。这些类型对掌握它的用法非常重要。

DB 数据库对象。 sql.DB类型代表了数据库。和其他语言不一样,它并是数据库连接。golang中的连接来自内部实现的连接池,连接的建立是惰性的,当你需要连接的时候,连接池会自动帮你创建。通常你不需要操作连接池。一切都有go来帮你完成。

Results 结果集。数据库查询的时候,都会有结果集。sql.Rows类型表示查询返回多行数据的结果集。sql.Row则表示单行查询结果的结果集。当然,对于插入更新和删除,返回的结果集类型为sql.Result。

Statements 语句。sql.Stmt类型表示sql查询语句,例如DDL,DML等类似的sql语句。可以把当成prepare语句构造查询,也可以直接使用sql.DB的函数对其操作。

warming up

下面就开始我们的sql数据库之旅,我们使用MySQL数据库为例子,驱动使用go-sql-driver/MySQL。

对于其他语言,查询数据的时候需要创建一个连接,对于go而言则是需要创建一个数据库抽象对象。连接将会在查询需要的时候,由连接池创建并维护。使用sql.Open函数创建数据库对象。它的第一个参数是数据库驱动名,第二个参数是一个连接字串 (符合DSN风格,可以是一个tcp连接,一个unix socket等) 。

import (

"database/sql"

"log"

_ "github.com/go-sql-driver/MySQL"
  
)

func main() {

db, err := sql.Open("MySQL", "root:@tcp(127.0.0.1:3306)/test?parseTime=true")

if err != nil{

log.Fatal(err)

}

defer db.Close()
  
}
  
创建了数据库对象之后,在函数退出的时候,需要释放连接,即调用sql.Close方法。例子使用了defer语句设置释放连接。

接下来进行一些基本的数据库操作,首先我们使用Exec方法执行一条sql,创建一个数据表:

func main() {

db, err := sql.Open("MySQL", "root:@tcp(127.0.0.1:3306)/test?parseTime=true")

if err != nil{

log.Fatal(err)

}

defer db.Close()

    _, err = db.Exec("CREATE TABLE IF NOT EXISTS test.hello(world varchar(50))")
    if err != nil{
        log.Fatalln(err)
    }

}
  
此时可以看见,数据库生成了一个新的表。接下来再插入一些数据。

func main() {

db, err := sql.Open("MySQL", "root:@tcp(127.0.0.1:3306)/test?parseTime=true")

    ...
    
    rs, err := db.Exec("INSERT INTO test.hello(world) VALUES ('hello world')")
    if err != nil{
        log.Fatalln(err)
    }
    rowCount, err := rs.RowsAffected()
    if err != nil{
        log.Fatalln(err)
    }
    log.Printf("inserted %d rows", rowCount)

}
  
同样使用Exec方法即可插入数据,返回的结果集对象是是一个sql.Result类型,它有一个LastInsertId方法,返回插入数据后的id。当然此例的数据表并没有id字段,就返回一个0.

插入了一些数据,接下来再简单的查询一下数据:

func main() {

db, err := sql.Open("MySQL", "root:@tcp(127.0.0.1:3306)/test?parseTime=true")

    ... 
    
    rows, err := db.Query("SELECT world FROM test.hello")
    if err != nil{
        log.Fatalln(err)
    }
    
    for rows.Next(){
        var s string
        err = rows.Scan(&s)
        if err !=nil{
            log.Fatalln(err)
        }
        log.Printf("found row containing %q", s)
    }
    rows.Close()

}
  
我们使用了Query方法执行select查询语句,返回的是一个sql.Rows类型的结果集。迭代后者的Next方法,然后使用Scan方法给变量s赋值,以便取出结果。最后再把结果集关闭 (释放连接) 。

通过上面一个简单的例子,介绍了database/sql的基本数据查询操作。而对于开篇所说的几个结构类型尚未进行详细的介绍。下面我们再针对database/sql库的类型和数据库交互做更深的探究。

sql.DB

正如上文所言,sql.DB是数据库的抽象,虽然通常它容易被误以为是数据库连接。它提供了一些跟数据库交互的函数,同时管理维护一个数据库连接池,帮你处理了单调而重复的管理工作,并且在多个goroutines也是十分安全。

sql.DB表示是数据库抽象,因此你有几个数据库就需要为每一个数据库创建一个sql.DB对象。因为它维护了一个连接池,因此不需要频繁的创建和销毁。它需要长时间保持,因此最好是设置成一个全局变量以便其他代码可以访问。

创建数据库对象需要引入标准库database/sql,同时还需要引入驱动go-sql-driver/MySQL。使用_表示引入驱动的变量,这样做的目的是为了在你的代码中不至于和标注库的函数变量namespace冲突。

连接池

只用sql.Open函数创建连接池,可是此时只是初始化了连接池,并没有创建任何连接。连接创建都是惰性的,只有当你真正使用到连接的时候,连接池才会创建连接。连接池很重要,它直接影响着你的程序行为。

连接池的工作原来却相当简单。当你的函数(例如Exec,Query)调用需要访问底层数据库的时候,函数首先会向连接池请求一个连接。如果连接池有空闲的连接,则返回给函数。否则连接池将会创建一个新的连接给函数。一旦连接给了函数,连接则归属于函数。函数执行完毕后,要不把连接所属权归还给连接池,要么传递给下一个需要连接的 (Rows) 对象,最后使用完连接的对象也会把连接释放回到连接池。

请求一个连接的函数有好几种,执行完毕处理连接的方式稍有差别,大致如下:

db.Ping() 调用完毕后会马上把连接返回给连接池。
  
db.Exec() 调用完毕后会马上把连接返回给连接池,但是它返回的Result对象还保留这连接的引用,当后面的代码需要处理结果集的时候连接将会被重用。
  
db.Query() 调用完毕后会将连接传递给sql.Rows类型,当然后者迭代完毕或者显示的调用.Clonse()方法后,连接将会被释放回到连接池。
  
db.QueryRow()调用完毕后会将连接传递给sql.Row类型,当.Scan()方法调用之后把连接释放回到连接池。
  
db.Begin() 调用完毕后将连接传递给sql.Tx类型对象,当.Commit()或.Rollback()方法调用后释放连接。
  
因为每一个连接都是惰性创建的,如何验证sql.Open调用之后,sql.DB对象可用呢？通常使用db.Ping()方法初始化:

db, err := sql.Open("driverName", "dataSourceName")
  
if err != nil{

log.Fatalln(err)
  
}

defer db.Close()

err = db.Ping()
  
if err != nil{

log.Fatalln(err)
  
}
  
调用了Ping之后,连接池一定会初始化一个数据库连接。当然,实际上对于失败的处理,应该定义一个符合自己需要的方式,现在为了演示,简单的使用log.Fatalln(err)表示了。

连接失败

关于连接池另外一个知识点就是你不必检查或者尝试处理连接失败的情况。当你进行数据库操作的时候,如果连接失败了,database/sql会帮你处理。实际上,当从连接池取出的连接断开的时候,database/sql会自动尝试重连10次。仍然无法重连的情况下会自动从连接池再获取一个或者新建另外一个。好比去买鸡蛋,售货员会从箱子里掏出鸡蛋,如果发现是坏蛋则连续掏10次,仍然找不到合适的就会换一个箱子招,或者从别的库房再拿一个给你。

连接池配置

无论哪一个版本的go都不会提供很多控制连接池的接口。知道1.2版本以后才有一些简单的配置。可是1.2版本的连接池有一个bug,请升级更高的版本。

配置连接池有两个的方法:

db.SetMaxOpenConns(n int) 设置打开数据库的最大连接数。包含正在使用的连接和连接池的连接。如果你的函数调用需要申请一个连接,并且连接池已经没有了连接或者连接数达到了最大连接数。此时的函数调用将会被block,直到有可用的连接才会返回。设置这个值可以避免并发太高导致连接MySQL出现too many connections的错误。该函数的默认设置是0,表示无限制。
  
db.SetMaxIdleConns(n int) 设置连接池中的保持连接的最大连接数。默认也是0,表示连接池不会保持释放会连接池中的连接的连接状态: 即当连接释放回到连接池的时候,连接将会被关闭。这会导致连接再连接池中频繁的关闭和创建。
  
对于连接池的使用依赖于你是如何配置连接池,如果使用不当会导致下面问题:

大量的连接空闲,导致额外的工作和延迟。
  
连接数据库的连接过多导致错误。
  
连接阻塞。
  
连接池有超过十个或者更多的死连接,限制就是10次重连。
  
大多数时候,如何使用sql.DB对连接的影响大过连接池配置的影响。这些具体问题我们会再使用sql.DB的时候逐一介绍。

掌握了database/sql关于数据库连接池管理内容,下一步则是使用这些连接,进行数据的交互操作啦。

作者: 人世间
  
链接: [http://www.jianshu.com/p/340eb943be2e](http://www.jianshu.com/p/340eb943be2e)
  
來源: 简书
  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

[https://stackoverflow.com/questions/17845619/how-to-call-the-scan-variadic-function-in-golang-using-reflection](https://stackoverflow.com/questions/17845619/how-to-call-the-scan-variadic-function-in-golang-using-reflection)

[https://golangtc.com/t/521abe66320b523a3500000e](https://golangtc.com/t/521abe66320b523a3500000e)
  
[http://www.jianshu.com/p/340eb943be2e](http://www.jianshu.com/p/340eb943be2e)
[https://www.jianshu.com/p/bc8120bec94e](https://www.jianshu.com/p/bc8120bec94e)
