+++
author = "w1100n"
date = "2020-08-27 18:21:10" 
title = "golang 正则"

+++
https://studygolang.com/articles/7256

    func main() {
        fmt.Println(regexp.Match("H.* ", []byte("Hello World!")))
        // true 
    }
