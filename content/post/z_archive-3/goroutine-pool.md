---
title: goroutine pool
author: "-"
date: 2020-04-19T03:19:23+00:00
url: /?p=15986
categories:
  - Inbox
tags:
  - reprint
---
## goroutine pool
```go
type worker struct {
    Func func()
}

func main() {
    var wg sync.WaitGroup

    channels := make(chan worker, 10)

    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for ch := range channels {
                //reflect.ValueOf(ch.Func).Call(ch.Args)
                ch.Func()
            }
        }()
    }

    for i := 0; i < 100; i++ {
        j := i
        wk := worker{
            Func: func() {
                fmt.Println(j + j)
            },
        }
        channels <- wk
    }
    close(channels)
    wg.Wait()
}
```

```go
package pool

type PayloadProcessor func(payload interface{})

type Pool struct {
    Size      int
    Channels  chan interface{}
    Processor PayloadProcessor
}

func New(size int, processor func(interface{})) *Pool {
    p := Pool{
        Size:      size,
        Channels:  make(chan interface{}, 0),
        Processor: processor,
    }

    for i := 0; i < p.Size; i++ {
        go func() {
            for payload := range p.Channels {
                p.Processor(payload)
            }
        }()
    }
    return &p
}

func (p *Pool) Process(payload interface{}) {
    p.Channels <- payload
}

```

http://legendtkl.com/2016/09/06/go-pool/