---
title: golang 各种数据类型转换
author: "-"
date: 2017-10-31T06:18:25+00:00
url: go/convert
categories:
  - Go
tags:
  - reprint
---
## golang 各种数据类型转换

Conversions are expressions of the form T(x) where T is a type and x is an expression that can be converted to type T.

## string > duration

```go
d, e := time.ParseDuration("-1h")
d, e := time.ParseDuration("1000ms")
```

### array > slice

```go
    arr := [3]int{1,2,3}
    sli := arr[:]
```

### hex > int, big.Int

```go
// int
n, err := strconv.ParseUint(val, 16, 32)

// big.Int
n := new(big.Int)
n, _ = n.SetString(hex[2:], 16)
```

### float > int

```go
    //float64 转成转成int64
    var x float64 = 5.7
    var y int = int64(x)

    int(math.Floor(f + 0.5))
```

### base64 > hex

```go
p, err := base64.StdEncoding.DecodeString("QVJWSU4=")
if err != nil {
    // handle error
}
h := hex.EncodeToString(p)
fmt.Println(h) // prints 415256494e
```

### bytes > hex

```go
hex.EncodeToString(foo)
```

### string, float

```go
s := "3.1415926535"
v1, err := strconv.ParseFloat(v, 32)
v2, err := strconv.ParseFloat(v, 64)

// float64 > string
valueStr = strconv.FormatFloat(v, 'f', 3, 64)
```

### int > float

```go
i:=5
f:=float32(i)

```

### bytes > int

```go
var ba = []byte{ 56, 66, 73, 77 }
var value int32
value |= int32(ba[0])
value |= int32(ba[1]) << 8
value |= int32(ba[2]) << 16
value |= int32(ba[3]) << 24
reverse the indexing order to switch between big and little endian.
```

### int8 > byte

因为两者间的类型及取值范围这些都不相同,不能直接进行转换。int8取值范围为: -128~127,如果要转化的话需要使用bytevalue=256+int8value

```go
var r byte
var v int8
v = -70
if v < 0 {
    r = byte(256 + int(v))
} else {
    r = byte(v)
}
```

但是,实际上我们可以直接使用byte进行强制转换,因为byte会自动检测v原有类型,然后进行转换的。

```go
var r byte
var v int8
v = -70
r = byte(v)
```

### string, bool

```go
// string > bool
// 将字符串转换为布尔值
// 它接受真值: 1, t, T, TRUE, true, True
// 它接受假值: 0, f, F, FALSE, false, False
// 其它任何值都返回一个错误。
func ParseBool(str string) (bool, error)
strconv.ParseBool("false")

// bool > string
// 将布尔值转换为字符串 true 或 false
func FormatBool(b bool) string


```

### int, string

```go
// string到int
int,err:=strconv.Atoi(string)
// string到int64
int64, err := strconv.ParseInt(string, 10, 64)
// int到string
string:=strconv.Itoa(int)
// int64到string
var foo int64
string:=strconv.FormatInt(foo,10)

// int32 to string
 strconv.FormatInt(int64(i), 10)

// int to int32
int32(i)

// uint8 > string
    var s uint8 = 10
    fmt.Print("out: "+strconv.Itoa(int(s)))

// uint64 > string
str := strconv.FormatUint(myNumber, 10)
```

[https://stackoverflow.com/questions/39442167/convert-int32-to-string-in-golang](https://stackoverflow.com/questions/39442167/convert-int32-to-string-in-golang)

### int32 > uint16

```go
var i int
u := uint16(i)
```

### string > []byte

```go
dataByte:=[]byte(dataStr)
```

### Golang Time互转秒、毫秒

```go
    fmt.Println(time.Now().Unix()) //获取当前秒
    fmt.Println(time.Now().UnixNano())//获取当前纳秒
    fmt.Println(time.Now().UnixNano()/1e6)//将纳秒转换为毫秒
    fmt.Println(time.Now().UnixNano()/1e9)//将纳秒转换为秒
    c := time.Unix(time.Now().UnixNano()/1e9,0) //将秒转换为 time 类型
    fmt.Println(c.String()) //输出当前英文时间戳格式
```

### byte > binary string

```go
package main

import "fmt"

func main() {
    bs := []byte{0x00, 0xfd}
    for _, n := range(bs) {
        fmt.Printf("% 08b", n) // prints 00000000 11111101
    }
}

```

### binary string > int

    tmp, _ := strconv.ParseInt(value, 2, 64)

### hex string > []byte

```go
import "hex"

hexStr := "fee9ecaadafeee72d2eb66a0bd344cdd"
data, err := hex.DecodeString(hexStr)

```

### []byte > hex string

```go
import (
"fmt"
"crypto/md5"
)
// 省略部分代码
data := "test string"
// md5.Sum() return a byte array
h := md5.Sum([]byte(data))

// with "%x" format byte array into hex string
hexStr := fmt.Sprintf("%x", h)

```

### int, byte

```go
// int64 > bytes
func Int64ToBytes(i int64) []byte {
    var buf = make([]byte, 8)
    binary.BigEndian.PutUint64(buf, uint64(i))
    return buf
}
// bytes to int64
func BytesToInt64(buf []byte) int64 {
    return int64(binary.BigEndian.Uint64(buf))
}
// int32 > bytes
func Int32ToBytes(i int32) []byte {
    fmt.Printf("int32: %v\n", i)
    return Uint32ToBytes(uint32(i))
}
// uint32 > bytes
func Uint32ToBytes(i uint32) []byte {
    fmt.Printf("uint32: %v\n", i)
    var buf = make([]byte, 8)
    binary.BigEndian.PutUint32(buf, i)
    return buf
}

```

### hex > signed int

    i, _ := strconv.ParseUint(hexValue, 16, 64)
    result = int32(i) / int32(rule.Rate)

    a := binary.LittleEndian.Uint64(sampleA)
    // If you need int64:
    a2 := int64(a)
    // If you need int32:
    a2 := int32(a)

Converting numeric types into a series of bytes ([]byte) and vice versa is about the endianness. How you interpret the result is entirely up to you.
All you need is to assemble a 16-bit, 32-bit or 64-bit value, once it's done, you can interpret the result as you want.
For example if you already have a uint16 value, to use it as a signed value, all you need is a type conversion because the memory layout of an uint16 and int16 is the same (converting from uint16 to int16 doesn't change the memory representation just the type):

### float

// 将浮点数转为字符串
// bitSize 表示来源类型 (32: float32、64: float64)
// fmt 表示格式: 'f' (-ddd.dddd) 、'b' (-ddddp±ddd,指数为二进制) 、'e' (-d.dddde±dd,十进制指数) 、'E' (-d.ddddE±dd,十进制指数) 、'g' (指数很大时用'e'格式,否则'f'格式) 、'G' (指数很大时用'E'格式,否则'f'格式) 。
// prec 控制精度 (排除指数部分) :对'f'、'e'、'E',它表示小数点后的数字个数；对'g'、'G',它控制总的数字个数。如果prec 为-1,则代表使用最少数量的、但又必需的数字来表示f。
func FormatFloat(f float64, fmt byte, prec, bitSize int) string

// 示例
s32 := strconv.FormatFloat(v, 'E', -1, 32)

作者: 炎灸纹舞
链接: [https://juejin.cn/post/6844903742618222600](https://juejin.cn/post/6844903742618222600)
来源: 掘金
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

// FormatFloat 将浮点数 f 转换为字符串值
// f: 要转换的浮点数
// fmt: 格式标记 (b、e、E、f、g、G)
// prec: 精度 (数字部分的长度,不包括指数部分)
// bitSize: 指定浮点类型 (32:float32、64:float64)
//
// 格式标记:
// 'b' (-ddddp±ddd,二进制指数)
// 'e' (-d.dddde±dd,十进制指数)
// 'E' (-d.ddddE±dd,十进制指数)
// 'f' (-ddd.dddd,没有指数)
// 'g' ('e':大指数,'f':其它情况)
// 'G' ('E':大指数,'f':其它情况)
//
// 如果格式标记为 'e','E'和'f',则 prec 表示小数点后的数字位数
// 如果格式标记为 'g','G',则 prec 表示总的数字位数 (整数部分+小数部分)
func FormatFloat(f float64, fmt byte, prec, bitSize int) string

package main

import (
    "fmt"
    "strconv"
)

func main() {
    f := 100.12345678901234567890123456789
    fmt.Println(strconv.FormatFloat(f, 'b', 5, 32))
    // 13123382p-17
    fmt.Println(strconv.FormatFloat(f, 'e', 5, 32))
    // 1.00123e+02
    fmt.Println(strconv.FormatFloat(f, 'E', 5, 32))
    // 1.00123E+02
    fmt.Println(strconv.FormatFloat(f, 'f', 5, 32))
    // 100.12346
    fmt.Println(strconv.FormatFloat(f, 'g', 5, 32))
    // 100.12
    fmt.Println(strconv.FormatFloat(f, 'G', 5, 32))
    // 100.12
    fmt.Println(strconv.FormatFloat(f, 'b', 30, 32))
    // 13123382p-17
    fmt.Println(strconv.FormatFloat(f, 'e', 30, 32))
    // 1.001234588623046875000000000000e+02
    fmt.Println(strconv.FormatFloat(f, 'E', 30, 32))
    // 1.001234588623046875000000000000E+02
    fmt.Println(strconv.FormatFloat(f, 'f', 30, 32))
    // 100.123458862304687500000000000000
    fmt.Println(strconv.FormatFloat(f, 'g', 30, 32))
    // 100.1234588623046875
    fmt.Println(strconv.FormatFloat(f, 'G', 30, 32))
    // 100.1234588623046875
}

[https://stackoverflow.com/questions/34701187/go-byte-to-little-big-endian-signed-integer-or-float](https://stackoverflow.com/questions/34701187/go-byte-to-little-big-endian-signed-integer-or-float)

[http://blog.csdn.net/pkueecser/article/details/50433460](http://blog.csdn.net/pkueecser/article/details/50433460)
[http://www.cnblogs.com/golove/p/3262925.html](http://www.cnblogs.com/golove/p/3262925.html)
[https://blog.csdn.net/lwldcr/article/details/78722330](https://blog.csdn.net/lwldcr/article/details/78722330)
[https://blog.csdn.net/pingD/article/details/76588648](https://blog.csdn.net/pingD/article/details/76588648)
[https://www.reddit.com/r/golang/comments/4xn341/converting_byte_to_int32/](https://www.reddit.com/r/golang/comments/4xn341/converting_byte_to_int32/)

## int 和 int64 互转

```go
var n int = 97
m := int64(n) // safe

var m int64 = 2 << 32
n := int(m)    // truncated on machines with 32-bit ints
fmt.Println(n) // either 0 or 4,294,967,296
```
