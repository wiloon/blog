---
title: gorun, golang, shell
author: "-"
date: 2011-09-18T14:09:37+00:00
url: gorun
categories:
  - golang
tags:
  - shell

---
## gorun
用 golang 语言编写脚本

```golang
/// 2>/dev/null ; gorun "$0" "$@" ; exit $?

package main
import (
    "os/exec"
    "fmt"
    "os"
)
func main() {
    println("Hello world!")
    var whoami []byte
    var err error
    var cmd *exec.Cmd
    cmd = exec.Command("whoami")
    if whoami, err = cmd.Output(); err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    // 默认输出有一个换行
    fmt.Println(string(whoami))
}
```

```bash
./hello.go
```

>https://www.infoq.cn/article/mbzyz8sedtbz5*4mhizo
>https://github.com/erning/gorun