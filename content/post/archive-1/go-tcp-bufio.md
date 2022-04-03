---
title: golang bufio 处理 TCP 粘包
author: "-"
date: 2015-04-27T12:59:51+00:00
url: /?p=7526
categories:
  - golang
tags:
  - reprint
---
## golang bufio 处理 TCP 粘包

http://feixiao.github.io/2016/05/08/bufio/

我们经常需要自定义协议,然后将自己定义的协议打包成二进制数据发送到对端,然后对端根据协议解包,TCP是流式传输所以我们需要自己从数据中找到数据的分隔点, 解析我们的数据包。

经常看到自定义的协议设计类似这样: 第一和第二个字节表示版本号,如V1, 第三、四字节表示数据的大小(不包括前面的四个字节),后面的就是这个数据包的大小。

// 类似这种结构

type Package struct {
      
Version [2]int8
      
Datalen int16
      
Data []byte
  
}
  
Golang里面处理这个包的方式之一如下: 

1:  一直阻塞读取第一个第二个字节,获取版本号(如果错误就做错误处理)；

2:  然后读取第三、四个字节,获取数据的大小；

3:  然后根据第二步中的数据大小,后面下面的数据；

4:  重复上面的过程；

NSQ 就是采取这种方式。

还有一种方式是我下面介绍的,我遇到的问题是这样: 我解析RTP Over RTSP数据,一个数据流里面有两种协议数据,所以我刚开始想到的方式就是,先从conn里面读取数据然后缓存,然后不断peek数据拿来分析(我不能拿走数据,因为数据可能不完整,所以一直做peek),自己管理buffer,其实这种方式很傻,golang的标准库其实已经给我们提供了实现。

使用Scanner就可以完成我们的需求, 实现如下: 
### scanner, 分离函数, 分割函数, split
```go
func main() {
      
// 创建一个包,版本是V1,数据是ABCDEFGHIJK,大小是11
      
var pkg Package
      
pkg.Version[0] = 'V'
      
pkg.Version[1] = 1
      
pkg.Data = []byte("ABCDEFGHIJK")
      
pkg.Datalen = int16(len(pkg.Data))
      
fmt.Println(&pkg)

    // 打包成二进制数据
    var buf bytes.Buffer
    pkg.Pack(&buf)
    
    // 从二进制数据里面获取数据
    var pkg1 Package
    pkg1.Unpack(&buf)
    fmt.Println(&pkg1)
    // 模拟数据流,打包三个数据包
    pkg.Pack(&buf)
    pkg.Pack(&buf)
    pkg.Pack(&buf)
    
    // 创建Scanner,分析buf数据流(r io.Reader,换成net.Conn对象就是处理tcp数据流,自己连数据都不需要去收取)
    scanner :=  bufio.NewScanner(&buf)
    
    // 数据的分离规则,根据协议自定义
    split := func(data []byte, atEOF bool) (advance int, token []byte, err error) {
        if !atEOF && data[0] == 'V'{
            if len(data) > 4 {
                var dataLen int16
                binary.Read(bytes.NewReader(data[2:4]),binary.BigEndian,&dataLen)
                if int(dataLen) + 4 <= len(data) {
                    return int(dataLen) + 4, data[:int(dataLen)+4],nil
                }
            }
        }
        return
    }
    
    // 设置分离函数
    scanner.Split(split)
    
    // 获取分离出来的数据
    for scanner.Scan() {
        fmt.Println(scanner.Bytes())
    }
    
    if err := scanner.Err(); err != nil {
        fmt.Printf("Invalid input: %s", err)
    }
    

}

// 自定义协议的组包和拆包
  
type Package struct {
      
Version [2]int8
      
Datalen int16
      
Data []byte
  
}

func (p *Package) String() string {
      
return fmt.Sprintf("Version:%d DataLen:%d Data:%s",
          
p.Version,p.Datalen,p.Data)
  
}

func (p *Package)Pack(w io.Writer) {
      
binary.Write(w, binary.BigEndian,p.Version)
      
binary.Write(w, binary.BigEndian,p.Datalen)
      
binary.Write(w,binary.BigEndian,p.Data)
  
}

func (p *Package)Unpack(r io.Reader) {
      
binary.Read(r,binary.BigEndian,&p.Version)
      
binary.Read(r,binary.BigEndian,&p.Datalen)
      
if p.Datalen > 0 {
          
p.Data = make([]byte,p.Datalen)
      
}
      
binary.Read(r,binary.BigEndian,&p.Data)
  
}
```