---
title: Ruby的require,load,和include
author: wiloon
type: post
date: 2012-04-01T07:41:42+00:00
url: /?p=2697
categories:
  - Development

---
<p style="text-align: justify;" align="center">
  <span style="font-size: medium;">三者之间区别并不像你想的那么难，也不会像有些文章写的那么长。挺简单的。</span>
</p>

<span style="font-size: medium;">相同之处：三者均在kernel中定义的，均含有包含进某物之意。</span>

<span style="font-size: medium;">不同之处：</span>

<span style="font-size: medium;">1、requre,load用于文件，如.rb等等结尾的文件。</span>

<span style="font-size: medium;">2、include则用于包含一个文件(.rb等结尾的文件)中的模块。</span>

<span style="font-size: medium;">3、requre一般情况下用于加载库文件，而load则用于加载配置文件。</span>

<span style="font-size: medium;">4、requre加载一次，load可加载多次。</span>

<span style="font-size: medium;">怎么样，简单吧！再看个例子。</span>

<span style="font-size: medium;">如果说abc.rb中包含一个模块Ma，和几个类Ca,Cb等等。那么你若想在ef.rb文件中使用abc.rb中的资源，你得这样:</span>

<span style="font-size: medium;">require &#8216;abc.rb&#8217;</span>

<span style="font-size: medium;">若还想在ef.rb的某个类中使用abc.rb中的模块，则应在这个类中加入</span>

<span style="font-size: medium;">include Ma</span>

<span style="font-size: medium;">如果你只想在ef.rb文件的某个类中使用abc.rb的模块，你得这样：</span>

<span style="font-size: medium;">require &#8216;abc.rb&#8217;</span>

<span style="font-size: medium;">include Ma</span>