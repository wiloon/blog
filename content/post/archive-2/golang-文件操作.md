---
title: golang file,文件操作
author: "-"
date: 2019-01-23T03:11:41.000+00:00
url: go/file
categories:
  - inbox
tags:
  - reprint
---
## golang file,文件操作

## 文件大小

```go
func main() {
    fi,err:=os.Stat("water")
    if err ==nil {
        fmt.Println("file size is ",fi.Size(),err)
    }
}

```

```go
package main

import (
    "bufio"
    "fmt"
    "io"
    "io/ioutil"
    "os"
)

func main() {
    dir := "/tmp/foo/bar"
    fileName := "file0.txt"
    writeTxtFile(dir, fileName, "foo")
    out := readTxtFile(dir, fileName)
    fmt.Println("read result: " + out)
}
func writeTxtFile0(dir, fileName, content string) {
    if !isExist(dir) {
        err := os.MkdirAll(dir, 0777)
        if err != nil {
            fmt.Printf("%s\n", err)
        } else {
            fmt.Println("Create Directory OK!")
        }
    }

    fullFileName := dir + string(os.PathSeparator) + fileName
    file, e := os.OpenFile(fullFileName, os.O_WRONLY|os.O_TRUNC|os.O_CREATE, 0777)
    if e != nil {
        fmt.Println("open file: " + e.Error())
    }
    defer file.Close()

    n, err := file.WriteString(content)
    if err != nil {
        fmt.Println("write string: " + err.Error())
        return
    }
    fmt.Printf("write length: %v\n", n)
}
func writeTxtFile(dir, fileName, content string) {
    if !isExist(dir) {
        err := os.MkdirAll(dir, 0777)
        if err != nil {
            fmt.Printf("%s\n", err)
        } else {
            fmt.Println("Create Directory OK!")
        }
    }
    err := ioutil.WriteFile(dir+string(os.PathSeparator)+fileName, []byte(content), 0777)
    if err != nil {
        fmt.Printf("failed to write file, file name: %v, err: %v", fileName, err)
        return
    }
}

func readTxtFile(dir, fileName string) string {
    path := dir + string(os.PathSeparator) + fileName
    dat, err := ioutil.ReadFile(path)
    if err != nil {
        fmt.Println("failed to read file: " + fileName)
    }
    return string(dat)
}

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func isExist(fileName string) bool {
    _, err := os.Stat(fileName)
    if err == nil {
        fmt.Println("file exist: " + fileName)
        return true
    } else if os.IsNotExist(err) {
        fmt.Println("file not exist")
        return false

    } else {
        fmt.Println("file error")
    }
    return false
}

```

### 判断是文件还是目录

```bash
    f, _ := os.Stat("a.txt")
    f.IsDir()
```

### move file

```go
func main() {
    oldLocation := "/var/www/html/test.txt"
    newLocation := "/var/www/html/src/test.txt"
    err := os.Rename(oldLocation, newLocation)
    if err != nil {
        log.Fatal(err)
    }
}
```

### 判断文件是否存在

```go
os.Stat(parentDir)
```

### 创建目录

```go
os.Mkdir(parentDir, os.ModePerm)
```

### 删除文件

```go
file := "test.txt"
err := os.Remove(file)

package main

import (
"fmt"
"os"
)

    // 判断文件夹是否存在
    func PathExists(path string) (bool, error) {
    _, err := os.Stat(path)
    if err == nil {
    return true, nil
    }
    if os.IsNotExist(err) {
    return false, nil
    }
    return false, err
    }
    
    func main() {
    _dir := "./gzFiles2"
    exist, err := PathExists(_dir)
    if err != nil {
    fmt.Printf("get dir error![%v]\n", err)
    return
    }

    if exist {
        fmt.Printf("has dir![%v]\n", _dir)
    } else {
        fmt.Printf("no dir![%v]\n", _dir)
        // 创建文件夹
        err := os.Mkdir(_dir, os.ModePerm)
        if err != nil {
            fmt.Printf("mkdir failed![%v]\n", err)
        } else {
            fmt.Printf("mkdir success!\n")
        }
    }

}
```

### 写文件

```go
/***************************** 第一种方式: 使用 io.WriteString 写入文件***/
if checkFileIsExist(filename) { //如果文件存在
f, err1 = os.OpenFile(filename, os.O_APPEND, 0666) //打开文件
fmt.Println("文件存在")
} else {
f, err1 = os.Create(filename) //创建文件
fmt.Println("文件不存在")
}
check(err1)
n, err1 := io.WriteString(f, wireteString) //写入文件(字符串)
check(err1)
fmt.Printf("写入 %d 个字节n", n)

    /*****************************  第二种方式: 使用 ioutil.WriteFile 写入文件****/
    var d1 = []byte(wireteString)
    err2 := ioutil.WriteFile("./output2.txt", d1, 0666) //写入文件(字节数组)
    check(err2)
    
    /*****************************  第三种方式:  使用 File(Write,WriteString) 写入文件***/
    f, err3 := os.Create("./output3.txt") //创建文件
    check(err3)
    defer f.Close()
    n2, err3 := f.Write(d1) //写入文件(字节数组)
    check(err3)
    fmt.Printf("写入 %d 个字节n", n2)
    n3, err3 := f.WriteString("writesn") //写入文件(字节数组)
    fmt.Printf("写入 %d 个字节n", n3)
    f.Sync()
    
    /***************************** 第四种方式:  使用 bufio.NewWriter 写入文件****/
    w := bufio.NewWriter(f) //创建新的 Writer 对象
    n4, err3 := w.WriteString("bufferedn")
    fmt.Printf("写入 %d 个字节n", n4)
    w.Flush()
    f.Close()

```

### 一般文件比较小的话可以将文件全部读入内存中,然后转换成string再按行分割一下

```go
func GetFileContentAsStringLines(filePath string) ([]string, error) {
logger.Infof("get file content as lines: %v", filePath)
result := []string{}
b, err := ioutil.ReadFile(filePath)
if err != nil {
logger.Errorf("read file: %v error: %v", filePath, err)
return result, err
}
s := string(b)
for _, lineStr := range strings.Split(s, "\\n") {
lineStr = strings.TrimSpace(lineStr)
if lineStr == "" {
continue
}
result = append(result, lineStr)
}
logger.Infof("get file content as lines: %v, size: %v", filePath, len(result))
return result, nil
}
```

### Golang 超大文件读取的两个方案

#### 第一个是使用流处理方式代码如下

```go
func ReadFile(filePath string, handle func(string)) error {
f, err := os.Open(filePath)
defer f.Close()
if err != nil {
return err
}
buf := bufio.NewReader(f)

    for {
        line, err := buf.ReadLine("\n")
        line = strings.TrimSpace(line)
        handle(line)
        if err != nil {
            if err == io.EOF{
                return nil
            }
            return err
        }
        return nil
    }

}
```

#### 第二个方案就是分片处理, 当读取的是二进制文件,没有换行符的时候,使用下面的方案处理大文件

```go
func ReadBigFile(fileName string, handle func([]byte)) error {
f, err := os.Open(fileName)
if err != nil {
fmt.Println("can't opened this file")
return err
}
defer f.Close()
s := make([]byte, 4096)
for {
switch nr, err := f.Read(s[:]); true {
case nr < 0:
fmt.Fprintf(os.Stderr, "cat: error reading: %s\n", err.Error())
os.Exit(1)
case nr == 0: // EOF
return nil
case nr > 0:
handle(s[0:nr])
}
}
return nil
}
```

<https://learnku.com/articles/23559/two-schemes-for-reading-golang-super-large-files>
<https://blog.csdn.net/xielingyun/article/details/50324423>  
<https://blog.csdn.net/robertkun/article/details/78776585>  
