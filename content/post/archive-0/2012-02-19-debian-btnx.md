---
title: debian btnx
author: "-"
type: post
date: 2012-02-19T11:39:24+00:00
url: /?p=2371
categories:
  - Linux

---
## debian btnx
open synaptic package manager, install btnx and btnx-config.

sudo btnx-config

启动出现如下界面,点击右边的Detect mouse & buttons

然后点击最上面的Press to start button detection，开始鼠标按键侦测过程。

反复按某一个键，直到Button detection进度条走满。然后按下最上面的Press to stop button detection大按钮。接下来在下面的Button name文本框中为刚侦测出的这个按键命名。

重复这个过程，直到所有的按键都被侦测出来。最后，按OK回到主界面。

现在，点开Button页签。你会发现刚刚侦测出的所有按键都已经被列出。接下来，就是按键的自定义设置了。

具体的自定义方法我就不多说，能看懂这个界面的人，应该都知道怎么设置。需要注意的是: 
  
a. 只有Enabled前的复选框被选中，btnx才能控制这个键，也就是说，自定义设置才会有效。
  
b. Repeat delay中的数值默认为0，如果不希望某个键按下去就有连续点击的效果，可以为它设置一个适当的数值。
  
c. Force imemediate button release的意思是当这个键被按下后，马上释放该键。选中它也可以防止不希望发生的连续点击。