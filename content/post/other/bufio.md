---
title: Go bufio
author: "-"
date: 2015-01-16T03:17:33+00:00
url: bufio
categories:
  - Go
tags:
  - reprint
  - io

---
## golang bufio

bufio 对 io 进行了包装, 提供了缓冲.

bufio包实现了有缓冲的I/O。它包装一个io.Reader或io.Writer接口对象，创建另一个也实现了该接口，且同时还提供了缓冲和一些文本I/O的帮助函数的对象。

简单的说就是bufio会把文件内容读取到缓存中 (内存），然后再取读取需要的内容的时候，直接在缓存中读取，避免文件的i/o操作。同样，通过bufio写入内容，也是先写入到缓存中 (内存），然后由缓存写入到文件。避免多次小内容的写入操作I/O。

bufio.Read(p []byte) 的思路如下：

1、当缓存区有内容的时，将缓存区内容全部填入p并清空缓存区
2、当缓存区没有内容的时候且len(p)>len(buf),即要读取的内容比缓存区还要大，直接去文件读取即可
3、当缓存区没有内容的时候且len(p)<len(buf),即要读取的内容比缓存区小，缓存区从文件读取内容充满缓存区，并将p填满 (此时缓存区有剩余内容）
4、以后再次读取时缓存区有内容，将缓存区内容全部填入p并清空缓存区 (此时和情况1一样）

<https://www.cnblogs.com/ricklz/p/13188188.html>

<http://www.cnblogs.com/golove/p/3282667.html>

// bufio 包实现了带缓存的 I/O 操作

type Reader struct { ... }

// NewReaderSize 将 rd 封装成一个带缓存的 bufio.Reader 对象，
  
// 缓存大小由 size 指定 (如果小于 16 则会被设置为 16) 。
  
// 如果 rd 的基类型就是有足够缓存的 bufio.Reader 类型，则直接将
  
// rd 转换为基类型返回。
  
func NewReaderSize(rd io.Reader, size int) *Reader

// NewReader 相当于 NewReaderSize(rd, 4096)
  
func NewReader(rd io.Reader) *Reader

// bufio.Reader 实现了如下接口:
  
// io.Reader
  
// io.WriterTo
  
// io.ByteScanner
  
// io.RuneScanner

// Peek 返回缓存的一个切片，该切片引用缓存中前 n 个字节的数据，
  
// 该操作不会将数据读出，只是引用，引用的数据在下一次读取操作之
  
// 前是有效的。如果切片长度小于 n，则返回一个错误信息说明原因。
  
// 如果 n 大于缓存的总大小，则返回 ErrBufferFull。
  
func (b *Reader) Peek(n int) ([]byte, error)

// Read 从 b 中读出数据到 p 中，返回读出的字节数和遇到的错误。
  
// 如果缓存不为空，则只能读出缓存中的数据，不会从底层 io.Reader
  
// 中提取数据，如果缓存为空，则:
  
// 1、len(p) >= 缓存大小，则跳过缓存，直接从底层 io.Reader 中读
  
// 出到 p 中。
  
// 2、len(p) < 缓存大小，则先将数据从底层 io.Reader 中读取到缓存
  
// 中，再从缓存读取到 p 中。
  
func (b *Reader) Read(p []byte) (n int, err error)

// Buffered 返回缓存中未读取的数据的长度。
  
func (b *Reader) Buffered() int

// Discard 跳过后续的 n 个字节的数据，返回跳过的字节数。
  
// 如果结果小于 n，将返回错误信息。
  
// 如果 n 小于缓存中的数据长度，则不会从底层提取数据。
  
func (b *Reader) Discard(n int) (discarded int, err error)

// ReadSlice 在 b 中查找 delim 并返回 delim 及其之前的所有数据。
  
// 该操作会读出数据，返回的切片是已读出的数据的引用，切片中的数据
  
// 在下一次读取操作之前是有效的。
  
//
  
// 如果找到 delim，则返回查找结果，err 返回 nil。
  
// 如果未找到 delim，则:
  
// 1、缓存不满，则将缓存填满后再次查找。
  
// 2、缓存是满的，则返回整个缓存，err 返回 ErrBufferFull。
  
//
  
// 如果未找到 delim 且遇到错误 (通常是 io.EOF) ，则返回缓存中的所
  
// 有数据和遇到的错误。
  
//
  
// 因为返回的数据有可能被下一次的读写操作修改，所以大多数操作应该
  
// 使用 ReadBytes 或 ReadString，它们返回的是数据的拷贝。
  
func (b *Reader) ReadSlice(delim byte) (line []byte, err error)

// ReadLine 是一个低水平的行读取原语，大多数情况下，应该使用
  
// ReadBytes('\n') 或 ReadString('\n')，或者使用一个 Scanner。
  
//
  
// ReadLine 通过调用 ReadSlice 方法实现，返回的也是缓存的切片。用于
  
// 读取一行数据，不包括行尾标记 (\n 或 \r\n) 。
  
//
  
// 只要能读出数据，err 就为 nil。如果没有数据可读，则 isPrefix 返回
  
// false，err 返回 io.EOF。
  
//
  
// 如果找到行尾标记，则返回查找结果，isPrefix 返回 false。
  
// 如果未找到行尾标记，则:
  
// 1、缓存不满，则将缓存填满后再次查找。
  
// 2、缓存是满的，则返回整个缓存，isPrefix 返回 true。
  
//
  
// 整个数据尾部"有一个换行标记"和"没有换行标记"的读取结果是一样。
  
//
  
// 如果 ReadLine 读取到换行标记，则调用 UnreadByte 撤销的是换行标记，
  
// 而不是返回的数据。
  
func (b *Reader) ReadLine() (line []byte, isPrefix bool, err error)

// ReadBytes 功能同 ReadSlice，只不过返回的是缓存的拷贝。
  
func (b *Reader) ReadBytes(delim byte) (line []byte, err error)

// ReadString 功能同 ReadBytes，只不过返回的是字符串。
  
func (b *Reader) ReadString(delim byte) (line string, err error)

// Reset 将 b 的底层 Reader 重新指定为 r，同时丢弃缓存中的所有数据，复位
  
// 所有标记和错误信息。 bufio.Reader。
  
func (b *Reader) Reset(r io.Reader)

* * *

// 示例: Peek、Read、Discard、Buffered
  
func main() {

sr := strings.NewReader("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")

buf := bufio.NewReaderSize(sr, 0)

b := make([]byte, 10)

    fmt.Println(buf.Buffered()) // 0
    s, _ := buf.Peek(5)
    s[0], s[1], s[2] = 'a', 'b', 'c'
    fmt.Printf("%d   %q\n", buf.Buffered(), s) // 16   "abcDE"
    
    buf.Discard(1)
    
    for n, err := 0, error(nil); err == nil; {
        n, err = buf.Read(b)
        fmt.Printf("%d   %q   %v\n", buf.Buffered(), b[:n], err)
    }
    // 5   "bcDEFGHIJK"   <nil>
    // 0   "LMNOP"   <nil>
    // 6   "QRSTUVWXYZ"   <nil>
    // 0   "123456"   <nil>
    // 0   "7890"   <nil>
    // 0   ""   EOF

}

* * *

// 示例: ReadLine
  
func main() {

sr := strings.NewReader("ABCDEFGHIJKLMNOPQRSTUVWXYZ\n1234567890")

buf := bufio.NewReaderSize(sr, 0)

    for line, isPrefix, err := []byte{0}, false, error(nil); len(line) > 0 && err == nil; {
        line, isPrefix, err = buf.ReadLine()
        fmt.Printf("%q   %t   %v\n", line, isPrefix, err)
    }
    // "ABCDEFGHIJKLMNOP"   true   <nil>
    // "QRSTUVWXYZ"   false   <nil>
    // "1234567890"   false   <nil>
    // ""   false   EOF
    
    fmt.Println("----------")
    
    // 尾部有一个换行标记
    buf = bufio.NewReaderSize(strings.NewReader("ABCDEFG\n"), 0)
    
    for line, isPrefix, err := []byte{0}, false, error(nil); len(line) > 0 && err == nil; {
        line, isPrefix, err = buf.ReadLine()
        fmt.Printf("%q   %t   %v\n", line, isPrefix, err)
    }
    // "ABCDEFG"   false   <nil>
    // ""   false   EOF
    
    fmt.Println("----------")
    
    // 尾部没有换行标记
    buf = bufio.NewReaderSize(strings.NewReader("ABCDEFG"), 0)
    
    for line, isPrefix, err := []byte{0}, false, error(nil); len(line) > 0 && err == nil; {
        line, isPrefix, err = buf.ReadLine()
        fmt.Printf("%q   %t   %v\n", line, isPrefix, err)
    }
    // "ABCDEFG"   false   <nil>
    // ""   false   EOF

}

* * *

// 示例: ReadSlice
  
func main() {

// 尾部有换行标记

buf := bufio.NewReaderSize(strings.NewReader("ABCDEFG\n"), 0)

    for line, err := []byte{0}, error(nil); len(line) > 0 && err == nil; {
        line, err = buf.ReadSlice('\n')
        fmt.Printf("%q   %v\n", line, err)
    }
    // "ABCDEFG\n"   <nil>
    // ""   EOF
    
    fmt.Println("----------")
    
    // 尾部没有换行标记
    buf = bufio.NewReaderSize(strings.NewReader("ABCDEFG"), 0)
    
    for line, err := []byte{0}, error(nil); len(line) > 0 && err == nil; {
        line, err = buf.ReadSlice('\n')
        fmt.Printf("%q   %v\n", line, err)
    }
    // "ABCDEFG"   EOF

}

* * *

type Writer struct { ... }

// NewWriterSize 将 wr 封装成一个带缓存的 bufio.Writer 对象，
  
// 缓存大小由 size 指定 (如果小于 4096 则会被设置为 4096) 。
  
// 如果 wr 的基类型就是有足够缓存的 bufio.Writer 类型，则直接将
  
// wr 转换为基类型返回。
  
func NewWriterSize(wr io.Writer, size int) *Writer

// NewWriter 相当于 NewWriterSize(wr, 4096)
  
func NewWriter(wr io.Writer) *Writer

// bufio.Writer 实现了如下接口:
  
// io.Writer
  
// io.ReaderFrom
  
// io.ByteWriter

// WriteString 功能同 Write，只不过写入的是字符串
  
func (b *Writer) WriteString(s string) (int, error)

// WriteRune 向 b 写入 r 的 UTF-8 编码，返回 r 的编码长度。
  
func (b *Writer) WriteRune(r rune) (size int, err error)

// Flush 将缓存中的数据提交到底层的 io.Writer 中
  
func (b *Writer) Flush() error

// Available 返回缓存中未使用的空间的长度
  
func (b *Writer) Available() int

// Buffered 返回缓存中未提交的数据的长度
  
func (b *Writer) Buffered() int

// Reset 将 b 的底层 Writer 重新指定为 w，同时丢弃缓存中的所有数据，复位
  
// 所有标记和错误信息。相当于创建了一个新的 bufio.Writer。
  
func (b *Writer) Reset(w io.Writer)

* * *

// 示例: Available、Buffered、WriteString、Flush
  
func main() {

buf := bufio.NewWriterSize(os.Stdout, 0)

fmt.Println(buf.Available(), buf.Buffered()) // 4096 0

    buf.WriteString("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    fmt.Println(buf.Available(), buf.Buffered()) // 4070 26
    
    // 缓存后统一输出，避免终端频繁刷新，影响速度
    buf.Flush() // ABCDEFGHIJKLMNOPQRSTUVWXYZ

}

* * *

// ReadWriter 集成了 bufio.Reader 和 bufio.Writer
  
type ReadWriter struct {

*Reader

*Writer
  
}

// NewReadWriter 将 r 和 w 封装成一个 bufio.ReadWriter 对象
  
func NewReadWriter(r \*Reader, w \*Writer) *ReadWriter

* * *

// Scanner 提供了一个方便的接口来读取数据，例如遍历多行文本中的行。Scan 方法会通过
  
// 一个"匹配函数"读取数据中符合要求的部分，跳过不符合要求的部分。"匹配函数"由调
  
// 用者指定。本包中提供的匹配函数有"行匹配函数"、"字节匹配函数"、"字符匹配函数"
  
// 和"单词匹配函数"，用户也可以自定义"匹配函数"。默认的"匹配函数"为"行匹配函
  
// 数"，用于获取数据中的一行内容 (不包括行尾标记)
  
//
  
// Scanner 使用了缓存，所以匹配部分的长度不能超出缓存的容量。默认缓存容量为 4096 -
  
// bufio.MaxScanTokenSize，用户可以通过 Buffer 方法指定自定义缓存及其最大容量。
  
//
  
// Scan 在遇到下面的情况时会终止扫描并返回 false (扫描一旦终止，将无法再继续) :
  
// 1、遇到 io.EOF
  
// 2、遇到读写错误
  
// 3、"匹配部分"的长度超过了缓存的长度
  
//
  
// 如果需要对错误进行更多的控制，或"匹配部分"超出缓存容量，或需要连续扫描，则应该
  
// 使用 bufio.Reader
  
type Scanner struct { ... }

// NewScanner 创建一个 Scanner 来扫描 r，默认匹配函数为 ScanLines。
  
func NewScanner(r io.Reader) *Scanner

// Buffer 用于设置自定义缓存及其可扩展范围，如果 max 小于 len(buf)，则 buf 的尺寸将
  
// 固定不可调。Buffer 必须在第一次 Scan 之前设置，否则会引发 panic。
  
// 默认情况下，Scanner 会使用一个 4096 - bufio.MaxScanTokenSize 大小的内部缓存。
  
func (s *Scanner) Buffer(buf []byte, max int)

// Split 用于设置"匹配函数"，这个函数必须在调用 Scan 前执行。
  
func (s *Scanner) Split(split SplitFunc)

// SplitFunc 用来定义"匹配函数"，data 是缓存中的数据。atEOF 标记数据是否读完。
  
// advance 返回 data 中已处理的数据的长度。token 返回找到的"匹配部分"，"匹配
  
// 部分"可以是缓存的切片，也可以是自己新建的数据 (比如 bufio.errorRune) 。"匹
  
// 配部分"将在 Scan 之后通过 Bytes 和 Text 反馈给用户。err 返回错误信息。
  
//
  
// 如果在 data 中无法找到一个完整的"匹配部分"则应返回 (0, nil, nil)，以便告诉
  
// Scanner 向缓存中填充更多数据，然后再次扫描 (Scan 会自动重新扫描) 。如果缓存已
  
// 经达到最大容量还没有找到，则 Scan 会终止并返回 false。
  
// 如果 data 为空，则"匹配函数"将不会被调用，意思是在"匹配函数"中不必考虑
  
// data 为空的情况。
  
//
  
// 如果 err != nil，扫描将终止，如果 err == ErrFinalToken，则 Scan 将返回 true，
  
// 表示扫描正常结束，如果 err 是其它错误，则 Scan 将返回 false，表示扫描出错。错误
  
// 信息可以在 Scan 之后通过 Err 方法获取。
  
//
  
// SplitFunc 的作用很简单，从 data 中找出你感兴趣的数据，然后返回，同时返回已经处理
  
// 的数据的长度。
  
type SplitFunc func(data []byte, atEOF bool) (advance int, token []byte, err error)

// Scan 开始一次扫描过程，如果匹配成功，可以通过 Bytes() 或 Text() 方法取出结果，
  
// 如果遇到错误，则终止扫描，并返回 false。
  
func (s *Scanner) Scan() bool

// Bytes 将最后一次扫描出的"匹配部分"作为一个切片引用返回，下一次的 Scan 操作会覆
  
// 盖本次引用的内容。
  
func (s *Scanner) Bytes() []byte

// Text 将最后一次扫描出的"匹配部分"作为字符串返回 (返回副本) 。
  
func (s *Scanner) Text() string

// Err 返回扫描过程中遇到的非 EOF 错误，供用户调用，以便获取错误信息。
  
func (s *Scanner) Err() error

// ScanBytes 是一个"匹配函数"用来找出 data 中的单个字节并返回。
  
func ScanBytes(data []byte, atEOF bool) (advance int, token []byte, err error)

// ScanRunes 是一个"匹配函数"，用来找出 data 中单个 UTF8 字符的编码。如果 UTF8 编
  
// 码错误，则 token 会返回 "\xef\xbf\xbd" (即: U+FFFD) ，但只消耗 data 中的一个字节。
  
// 这使得调用者无法区分"真正的U+FFFD字符"和"解码错误的返回值"。
  
func ScanRunes(data []byte, atEOF bool) (advance int, token []byte, err error)

// ScanLines 是一个"匹配函数"，用来找出 data 中的单行数据并返回 (包括空行) 。
  
// 行尾标记可以是 \n 或 \r\n (返回值不包含行尾标记)
  
func ScanLines(data []byte, atEOF bool) (advance int, token []byte, err error)

// ScanWords 是一个"匹配函数"，用来找出 data 中以空白字符分隔的单词。
  
// 空白字符由 unicode.IsSpace 定义。
  
func ScanWords(data []byte, atEOF bool) (advance int, token []byte, err error)

* * *

// 示例: 扫描
  
func main() {

// 逗号分隔的字符串，最后一项为空

const input = "1,2,3,4,"

scanner := bufio.NewScanner(strings.NewReader(input))

// 定义匹配函数 (查找逗号分隔的字符串)

onComma := func(data []byte, atEOF bool) (advance int, token []byte, err error) {

for i := 0; i < len(data); i++ {

if data[i] == ',' {

return i + 1, data[:i], nil

}

}

if atEOF {

// 告诉 Scanner 扫描结束。

return 0, data, bufio.ErrFinalToken

} else {

// 告诉 Scanner 没找到匹配项，让 Scan 填充缓存后再次扫描。

return 0, nil, nil

}

}

// 指定匹配函数

scanner.Split(onComma)

// 开始扫描

for scanner.Scan() {

fmt.Printf("%q ", scanner.Text())

}

// 检查是否因为遇到错误而结束

if err := scanner.Err(); err != nil {

fmt.Fprintln(os.Stderr, "reading input:", err)

}
  
}

* * *

// 示例: 带检查扫描
  
func main() {

const input = "1234 5678 1234567901234567890 90"

scanner := bufio.NewScanner(strings.NewReader(input))

// 自定义匹配函数

split := func(data []byte, atEOF bool) (advance int, token []byte, err error) {

// 获取一个单词

advance, token, err = bufio.ScanWords(data, atEOF)

// 判断其能否转换为整数，如果不能则返回错误

if err == nil && token != nil {

_, err = strconv.ParseInt(string(token), 10, 32)

}

// 这里包含了 return 0, nil, nil 的情况

return

}

// 设置匹配函数

scanner.Split(split)

// 开始扫描

for scanner.Scan() {

fmt.Printf("%s\n", scanner.Text())

}

if err := scanner.Err(); err != nil {

fmt.Printf("Invalid input: %s", err)

}
  
}

* * *
