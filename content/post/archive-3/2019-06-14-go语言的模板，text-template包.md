---
title: go语言的模板，text/template包
author: wiloon
type: post
date: 2019-06-14T05:29:13+00:00
url: /?p=14513
categories:
  - Uncategorized

---
#go语言的模板，text/template包 ##定义 模板就是将一组文本嵌入另一组文本里

##传入string&#8211;最简单的替换

package main

import (
      
&#8220;os&#8221;
      
&#8220;text/template&#8221;
  
)

func main() {
      
name := &#8220;waynehu&#8221;
      
tmpl, err := template.New(&#8220;test&#8221;).Parse(&#8220;hello, {{.}}&#8221;) //建立一个模板，内容是&#8221;hello, {{.}}&#8221;
      
if err != nil {
              
panic(err)
      
}
      
err = tmpl.Execute(os.Stdout, name) //将string与模板合成，变量name的内容会替换掉{{.}}
      
//合成结果放到os.Stdout里
      
if err != nil {
              
panic(err)
      
}
  
}
  
//输出 ： hello, waynehu
  
因为&#8221;hello, {{.}}&#8221;也是一个字符串，所以可以单独拎出来，如下：

//这句
  
tmpl, err := template.New(&#8220;test&#8221;).Parse(&#8220;hello, {{.}}&#8221;)
  
//等于下面的两句
  
muban := &#8220;hello, {{.}}&#8221;
  
tmpl, err := template.New(&#8220;test&#8221;).Parse(muban)
  
//之后的例子都用两句的方式表达
  
##传入struct 模板合成那句，第2个参数是interface{}，所以可以传入任何类型，现在传入struct看看 要取得struct的值，只要使用成员名字即可，看代码吧：

package main

import (
      
&#8220;os&#8221;
      
&#8220;text/template&#8221;
  
)

type Inventory struct {
      
Material string
      
Count uint
  
}

func main() {
      
sweaters := Inventory{&#8220;wool&#8221;, 17}
      
muban := &#8220;{{.Count}} items are made of {{.Material}}&#8221;
      
tmpl, err := template.New(&#8220;test&#8221;).Parse(muban) //建立一个模板
      
if err != nil {
              
panic(err)
      
}
      
err = tmpl.Execute(os.Stdout, sweaters) //将struct与模板合成，合成结果放到os.Stdout里
      
if err != nil {
              
panic(err)
      
}
  
}
  
//输出 ： 17 items are made of wool
  
##多模板，介绍New，Name，Lookup

//一个模板可以有多种，以Name来区分
  
muban_eng := &#8220;{{.Count}} items are made of {{.Material}}&#8221;
  
muban_chn := &#8220;{{.Material}}做了{{.Count}}个项目&#8221;
  
//建立一个模板的名称是china，模板的内容是muban_chn字符串
  
tmpl, err := template.New(&#8220;china&#8221;)
  
tmpl, err = tmpl.Parse(muban_chn)
  
//建立一个模板的名称是english，模板的内容是muban_eng字符串
  
tmpl, err = tmpl.New(&#8220;english&#8221;)
  
tmpl, err = tmpl.Parse(muban_eng)
  
//将struct与模板合成，用名字是china的模板进行合成，结果放到os.Stdout里，内容为“wool做了17个项目”
  
err = tmpl.ExecuteTemplate(os.Stdout, &#8220;china&#8221;, sweaters)
  
//将struct与模板合成，用名字是china的模板进行合成，结果放到os.Stdout里，内容为“17 items are made of wool”
  
err = tmpl.ExecuteTemplate(os.Stdout, &#8220;english&#8221;, sweaters)

tmpl, err = template.New(&#8220;english&#8221;)
  
fmt.Println(tmpl.Name()) //打印出english
  
tmpl, err = tmpl.New(&#8220;china&#8221;)
  
fmt.Println(tmpl.Name()) //打印出china
  
tmpl=tmpl.Lookup(&#8220;english&#8221;)//必须要有返回，否则不生效
  
fmt.Println(tmpl.Name()) //打印出english
  
##文件模板，介绍ParseFiles

//模板可以是一行
  
muban := &#8220;{{.Count}} items are made of {{.Material}}&#8221;
  
//也可以是多行
  
muban := `items number is {{.Count}}<br />
there made of {{.Material}}`
  
把模板的内容发在一个文本文件里，用的时候将文本文件里的所有内容赋值给muban这个变量即可
  
上面的想法可以自己实现，但其实tamplate包已经帮我们封装好了，那就是template.ParseFiles方法

假设有一个文件mb.txt的内容是muban变量的内容
  
$cat mb.txt
  
{{.Count}} items are made of {{.Material}}

那么下面2行
  
muban := &#8220;{{.Count}} items are made of {{.Material}}&#8221;
  
tmpl, err := template.New(&#8220;test&#8221;).Parse(muban) //建立一个模板

等价于
  
tmpl, err := template.ParseFiles(&#8220;mb.txt&#8221;) //建立一个模板，这里不需要new(&#8220;name&#8221;)的方式，因为name自动为文件名
  
##文件模板，介绍ParseGlob

ParseFiles接受一个字符串，字符串的内容是一个模板文件的路径（绝对路径or相对路径）
  
ParseGlob也差不多，是用正则的方式匹配多个文件

假设一个目录里有a.txt b.txt c.txt的话
  
用ParseFiles需要写3行对应3个文件，如果有一万个文件呢？
  
而用ParseGlob只要写成template.ParseGlob(&#8220;*.txt&#8221;) 即可
  
##模板的输出，介绍ExecuteTemplate和Execute

模板下有多套模板，其中有一套模板是当前模板
  
可以使用Name的方式查看当前模板

err = tmpl.ExecuteTemplate(os.Stdout, &#8220;english&#8221;, sweaters) //指定模板名，这次为english
  
err = tmpl.Execute(os.Stdout, sweaters) //模板名省略，打印的是当前模板
  
##模板的复用 模板里可以套模板，以达到复用目的，用template关键字

muban1 := `hi, {{template "M2"}},<br />
hi, {{template "M3"}}`
  
muban2 := &#8220;我是模板2，{{template &#8220;M3&#8243;}}&#8221;
  
muban3 := &#8220;ha我是模板3ha!&#8221;

tmpl, err := template.New(&#8220;M1&#8221;).Parse(muban1)
  
tmpl.New(&#8220;M2&#8221;).Parse(muban2)
  
tmpl.New(&#8220;M3&#8221;).Parse(muban3)
  
err = tmpl.Execute(os.Stdout, nil)
  
完整代码：

package main

import (
      
&#8220;os&#8221;
      
&#8220;text/template&#8221;
  
)

func main() {
      
muban1 := `hi, {{template "M2"}},<br />
hi, {{template "M3"}}`
      
muban2 := `我是模板2，{{template "M3"}}`
      
muban3 := &#8220;ha我是模板3ha!&#8221;

    tmpl, err := template.New("M1").Parse(muban1)
    if err != nil {
            panic(err)
    }   
    tmpl.New("M2").Parse(muban2)
    if err != nil {
            panic(err)
    }   
    tmpl.New("M3").Parse(muban3)
    if err != nil {
            panic(err)
    }   
    err = tmpl.Execute(os.Stdout, nil)
    if err != nil {
            panic(err)
    }   
    

}
  
输出的内容

hi, 我是模板2，ha我是模板3ha!,
  
hi, ha我是模板3ha!
  
##模板的回车 模板文件里的回车也是模板的一部分，如果对回车位置控制不好，合成出来的文章会走样 标准库里的Example(Template)写的还是有点乱，我整理如下：

const letter = \`Dear {{.Name}},

{{if .Attended}}It was a pleasure to see you at the wedding.
  
如果Attended是true的话，这句是第二行{{else}}It is a shame you couldn&#8217;t make it to the wedding.
  
如果Attended是false的话，这句是第二行{{end}}
  
{{with .Gift}}Thank you for the lovely {{.}}.
  
{{end}}
  
Best wishes,
  
Josie

\`
  
解释一下：

Dear某某某的Dear应该是在第一行，所以在D前面不能有回车，否则Dear会跑到第2行去
  
所以Dear要紧贴&#8220;\`
  
信件的称唿和正文有一行空行，最好显式的打出一行，而标准库里的回车是包在if里，成为正文的一部分，这样排版容易出错
  
正确的正文排版如下
  
如果正文就一行，要把true和false的所有内容都写在一行
  
比如{{if .Attended}}true line,hello true{{else}}false line,hi false{{end}}
  
如果正文有多行，就等于把一行拆成多行
  
会发现true的最后一行和false的第一行是在同一行
  
{{if .Attended}}和ture的第一行在同一行
  
{{end}}和false的最后一行在同一行
  
如下

{{if .Attended}}true line
  
hello true{{else}}false line
  
hi false{{end}}
  
关于{{with .Gift}},意思是如果Gift不是为空的话，就打印整行，如果为空，就不打印
  
只有这样写法，with对应的end要写在第2行，才会把“Thank you”这句后面带一个回车进去，这样写法，就像“Thank you”这句是插在正文下面的
  
只有这样写，不管有没有“Thank you”，正文和Best wishes,之间始终只有1行空白

https://my.oschina.net/u/943306/blog/153156