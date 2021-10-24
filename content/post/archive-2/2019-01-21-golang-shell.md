---
title: golang shell
author: "-"
type: post
date: 2019-01-21T06:53:54+00:00
url: /?p=13440
categories:
  - Uncategorized

---
## golang shell
```golang
func shellExec(s string) string {
    cmd := exec.Command("/bin/sh", "-c", s)
    var out bytes.Buffer

    cmd.Stdout = &out
    err := cmd.Run()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("%s", out.String())
    return out.String()
}

```