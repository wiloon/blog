---
title: golang 各种数据类型转换, byte, bianary
author: wiloon
type: post
date: 2017-10-31T06:18:25+00:00
url: /?p=11346
categories:
  - Uncategorized

---
### float > int

<pre><code class="language-go line-numbers">//float64 转成转成int64
var x float64 = 5.7
var y int = int64(x)

//
int(math.Floor(f + 0.5))
```

### base64 > hex

<pre><code class="language-go line-numbers">p, err := base64.StdEncoding.DecodeString("QVJWSU4=")
if err != nil {
    // handle error
}
h := hex.EncodeToString(p)
fmt.Println(h) // prints 415256494e
```

### bytes > hex

<pre><code class="language-go line-numbers">hex.EncodeToString(foo))
```

### string, float：

<pre><code class="language-go line-numbers">s := "3.1415926535"
v1, err := strconv.ParseFloat(v, 32)
v2, err := strconv.ParseFloat(v, 64)

// float64 &gt; string
valueStr = strconv.FormatFloat(v, 'f', 3, 64)
```

### int > float

<pre><code class="language-go line-numbers">i:=5
f:=float32(i)

```

### bytes > int

<pre><code class="language-go line-numbers">var ba = []byte{ 56, 66, 73, 77 }
var value int32
value |= int32(ba[0])
value |= int32(ba[1]) &lt;&lt; 8
value |= int32(ba[2]) &lt;&lt; 16
value |= int32(ba[3]) &lt;&lt; 24
reverse the indexing order to switch between big and little endian.
```

### int8>byte

因为两者间的类型及取值范围这些都不相同，不能直接进行转换。int8取值范围为：-128~127，如果要转化的话需要使用bytevalue=256+int8value

<pre><code class="language-go line-numbers">var r byte
var v int8
v = -70
if v &lt; 0 {
    r = byte(256 + int(v))
} else {
    r = byte(v)
}
```

但是，实际上我们可以直接使用byte进行强制转换，因为byte会自动检测v原有类型，然后进行转换的。

<pre><code class="language-go line-numbers">var r byte
var v int8
v = -70
r = byte(v)
```

### string, bool

<pre><code class="language-go line-numbers">strconv.ParseBool("false")

// 将布尔值转换为字符串 true 或 false
func FormatBool(b bool) string

// 将字符串转换为布尔值
// 它接受真值：1, t, T, TRUE, true, True
// 它接受假值：0, f, F, FALSE, false, False
// 其它任何值都返回一个错误。
func ParseBool(str string) (bool, error)
```

### int, string

<pre><code class="language-go line-numbers">// string到int
int,err:=strconv.Atoi(string)
// string到int64
int64, err := strconv.ParseInt(string, 10, 64)
// int到string
string:=strconv.Itoa(int)
// int64到string
string:=strconv.FormatInt(int64,10)

// int32 to string
 strconv.FormatInt(int64(i), 10)

// int to int32
int32(i)

// uint16 &gt; string
var s uint8 = 10
fmt.Print(string(s))

// uint64 &gt; string
str := strconv.FormatUint(myNumber, 10)
```

https://stackoverflow.com/questions/39442167/convert-int32-to-string-in-golang

### int32 > uint16

<pre><code class="language-go line-numbers">var i int
u := uint16(i)
```

### string > []byte

<pre><code class="language-go line-numbers">dataByte:=[]byte(dataStr)
```

### Golang Time互转秒、毫秒

<pre><code class="language-go line-numbers">    fmt.Println(time.Now().Unix()) //获取当前秒
    fmt.Println(time.Now().UnixNano())//获取当前纳秒
    fmt.Println(time.Now().UnixNano()/1e6)//将纳秒转换为毫秒
    fmt.Println(time.Now().UnixNano()/1e9)//将纳秒转换为秒
    c := time.Unix(time.Now().UnixNano()/1e9,0) //将秒转换为 time 类型
    fmt.Println(c.String()) //输出当前英文时间戳格式
```

### 字符串毫秒转时间格式

<pre><code class="language-go line-numbers">package main

import (
    "fmt"
    "strconv"
    "time"
)

func main() {
    fmt.Println(msToTime("1489582166978"))
}

func msToTime(ms string) (time.Time, error) {
    msInt, err := strconv.ParseInt(ms, 10, 64)
    if err != nil {
        return time.Time{}, err
    }

    tm := time.Unix(0, msInt*int64(time.Millisecond))

    fmt.Println(tm.Format("2006-02-01 15:04:05.000"))

    return tm, nil
}

```

### byte > binary string

<pre><code class="language-go line-numbers">&lt;br />package main

import "fmt"

func main() {
    bs := []byte{0x00, 0xfd}
    for _, n := range(bs) {
        fmt.Printf("% 08b", n) // prints 00000000 11111101
    }
}

```

### hex string > []byte

<pre><code class="language-go line-numbers">import "hex"
// 省略部分代码....

hexStr := "fee9ecaadafeee72d2eb66a0bd344cdd"
data, err := hex.DecodeString(hexStr)
if err != nil {
// handle error
}

// continue handling data
```

### []byte > hex string

<pre><code class="language-go line-numbers">import (
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

<pre><code class="language-go line-numbers">// int64 &gt; bytes
func Int64ToBytes(i int64) []byte {
    var buf = make([]byte, 8)
    binary.BigEndian.PutUint64(buf, uint64(i))
    return buf
}
// bytes to int64
func BytesToInt64(buf []byte) int64 {
    return int64(binary.BigEndian.Uint64(buf))
}
// int32 &gt; bytes
func Int32ToBytes(i int32) []byte {
    fmt.Printf("int32: %v\n", i)
    return Uint32ToBytes(uint32(i))
}
// uint32 &gt; bytes
func Uint32ToBytes(i uint32) []byte {
    fmt.Printf("uint32: %v\n", i)
    var buf = make([]byte, 8)
    binary.BigEndian.PutUint32(buf, i)
    return buf
}

```

http://blog.csdn.net/pkueecser/article/details/50433460
  
http://www.cnblogs.com/golove/p/3262925.html
  
https://blog.csdn.net/lwldcr/article/details/78722330
  
https://blog.csdn.net/pingD/article/details/76588648
  
https://www.reddit.com/r/golang/comments/4xn341/converting\_byte\_to_int32/