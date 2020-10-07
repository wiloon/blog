+++
author = "w1100n"
date = "2020-09-30 13:44:20" 
title = "golang pprof 内存分析"

+++

    import _ "net/http/pprof"

    go func() {
        http.ListenAndServe("0.0.0.0:8080", nil)
    }()

    http://localhost:8080/debug/pprof/
    默认512kb进行 一次采样

https://lrita.github.io/2017/05/26/golang-memory-pprof/#golang-pprof
