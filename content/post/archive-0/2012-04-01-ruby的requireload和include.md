---
title: Ruby的require,load,和include
author: "-"
date: 2012-04-01T07:41:42+00:00
url: /?p=2697
categories:
  - Development

---
## Ruby的require,load,和include

  三者之间区别并不像你想的那么难，也不会像有些文章写的那么长。挺简单的。

相同之处: 三者均在kernel中定义的，均含有包含进某物之意。

不同之处: 

1、requre,load用于文件，如.rb等等结尾的文件。

2、include则用于包含一个文件(.rb等结尾的文件)中的模块。

3、requre一般情况下用于加载库文件，而load则用于加载配置文件。

4、requre加载一次，load可加载多次。

怎么样，简单吧！再看个例子。

如果说abc.rb中包含一个模块Ma，和几个类Ca,Cb等等。那么你若想在ef.rb文件中使用abc.rb中的资源，你得这样:

require 'abc.rb'

若还想在ef.rb的某个类中使用abc.rb中的模块，则应在这个类中加入

include Ma

如果你只想在ef.rb文件的某个类中使用abc.rb的模块，你得这样: 

require 'abc.rb'

include Ma