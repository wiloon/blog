---
title: emacs org-mode TODO状态
author: "-"
date: 2011-12-11T14:02:27+00:00
url: /?p=1860
categories:
  - Inbox
tags:
  - reprint
---
## emacs org-mode TODO状态
https://qiwulun.github.io/posts/org-mode%E5%B8%B8%E7%94%A8%E5%8A%9F%E8%83%BD%EF%BC%8D%EF%BC%8DTODO%E7%8A%B6%E6%80%81%E4%B8%8E%E5%A4%8D%E9%80%89%E6%A1%86.html

org-mode常用功能－－TODO状态与复选框

快捷键

t 将当前项的状态在 (unmarked) ->TODO->DONE 之间循环切换
  
=,/= 各种稀疏树的检索形式
  
=,T= / C-c / t 在稀疏树中显示 TODO 项，同时显示 TODO 项和它们所在的层次的标题
  
=, a t= / SPC a o t (agenda) 显示全局 TODO 列表，将从所有的议程文件中收集 TODO 项到一个缓冲区中
  
S-M-RET 在当前项下插入一个新的 TODO 项
  
格式

定义

用 TODO 关键字来定义不同的状态，用以处理项，比如: 

(setq org-todo-keywords

'((sequence "TODO" "FEEDBACK" "VERIFY" "|" "DONE" "DELEGATED")))
  
竖直线将 TODO 关键字 (还需要进一步的动作) 和 DONE 状态 (不需要进一步的动作) 分隔开。如果你不给出竖直线，最后一个状态会作为 DONE 状态。设置之后，C-c C-t 就会将状态从 TODO 转换到 FEEDBACK，再转换到 VERIFY，最后到 DONE 和 DELEGATED。

有时你可能希望同时使用几个不同的 TODO 状态集合。例如，你可能想要一个基本的 TODO/DONE，以及一个修改 bug 的工作流程和一个隔开的状态来表示取消的项目 (既还是 DONE，也不需要进一步的动作) ，你可以这样设置: 

(setq org-todo-keywords

'((sequence "TODO(t)" "|" "DONE(d)")

(sequence "REPORT(r)" "BUG(b)" "KNOWNCAUSE(k)" "|" "FIXED(f)")

(sequence "|" "CANCELED(c)")))
  
关键字应该各不相同，这样对于一个选项 Org 才知道该用哪个状态序列 (集合) 。例子中也给出了快速使用一个关键字的方法，就是在关键字后面括号中给出快捷字母——当用 C-c C-t时，会询问，让你输入一个字母。

要定义只在一个文件中有效的 TODO 关键字，可以在文件中任意地方给出下面的文本: 

#+TODO: TODO(t) | DONE(d)

#+TODO: REPORT(r) BUG(b) KNOWNCAUSE(k) | FIXED(f)

#+TODO: | CANCELED(c)
  
当改变这些行中的一行后，光标停留在改变行上，用 C-c C-c 让改变生效。

,#+SEQTODO: REPORT(r) BUG(b) KNOWNCAUSE(k) | FIXED(f)#+SEQTODO: TODO(T!) | DONE(D@)3 CANCELED(C@/!)

将光标放在这些内容上，输入 C-c C-c 可以直接生效。此时再用C-c C-t设定任务时，会打开一个新的缓冲区: 

对照前面的定义不难发现: 

可以定义多组状态序列，每个"#+SEQTODO"行定义一组
  
状态之间用空格分隔
  
可以在 () 中定义附加选项，包括: 
  
字符: 该状态的快捷键
  
！: 切换到该状态时会自动增加时间戳
  
@ : 切换到该状态时要求输入文字说明
  
如果同时设定@和！，使用"@/!"
  
用"|"分隔未完成状态和已完成状态。未完成状态在查询待办事项时会列出。
  
使用C-c C-t 或者 S-LEFT/RIGTH 切换一些状态后，任务会变成这个样子: 

会自动生成时间戳，提示填写说明。从而留下完整的记录。

上面的任务状态设置只适用于当前文档。如果希望设定所有.org文档的默认任务状态，需要在.emacs配置文件中定义。 上面的任务状态在配置文件中的等效设置为: 

(setq org-todo-keywords
    
'((sequence "REPORT(r)" "BUG(b)" "KNOWNCAUSE(k)" "|" "FIXED(f)")
      
(sequence "TODO(T!)" "|" "DONE(D@)3" "CANCELED(C@/!)")
      
))
  
除了状态序列外，还可以定义type，来标记任务的分类。可以参考这里 。

子任务

很多时候将一个大的任务分成几个的易于完成的小任务是明智的，你可以通过在TODO项目下新建一个大纲树，并在子树上标记子任务来实现这个功能。

对于有多个子任务的上级任务，很常见的一个需求是随时跟踪子任务的完成情况。 为了能对已经完成的任务有个大致的了解，你可以在标题的任何地方插入'[/]'或者'[%]'。当每个子任务的状态变化时，或者当你在标记上按 C-c C-c 时，这些标记状态也会随之更新。例如: 

, * Organize Party [33%]
  
,
  
, ** TODO Call people [1/2]
  
,
  
, \*** TODO Peter
  
,
  
, \*** DONE Sarah
  
,
  
, ** TODO Buy food
  
,
  
, ** DONE Talk to neighbor
  
当纯文本中的项以'[]'开头时，就会变成一个复选框。

复选框不会包含在全局 TODO 列表中，所以它们很适合地将一个任务划分成几个简单的步骤。下面是一个复选框的例子: 

  * TODO Organize party [1/3]

, - [-] call people [1/2]

, - [ ] Peter

, - [X] Sarah

, - [X] order food

, - [ ] think about what music to play
  
复选框是分层工作的。所以如果一个复选框项目如果还有子复选框，触发子复选框将会使该复选框变化以反映出一个、多个还是没有子复选框被选中。

C-c C-c 触发复选框的状态或者 (加上前缀) 触发复选框的的存在状态

M-S-RET 增加一个带有复选框的项。这只在光标处于纯文本列表项中才起使用

级联配置 (我暂时没用) 
  
当改变子任务状态时，只更新上一级任务的完成情况，不可级联。即使所有的子任务都完成，也只是标记上一级任务的完成情况为100%，而不能自动更新上级任务的完成状态。如果需要自动设定为完成，可以在.emacs中增加如下配置: 

;;在子TODO都完成后设置父TODO项

(defun org-summary-todo (n-done n-not-done)
    
"Switch entry to DONE when all subentries are done, to TODO otherwise."
    
(let (org-log-done org-log-states) ; turn off logging
      
(org-todo (if (= n-not-done 0) "DONE" "TODO"))))
  
(add-hook 'org-after-todo-statistics-hook 'org-summary-todo)
  
记录修改

最基本的日志功能
  
跟踪一个特定项目的完成。这可以这样实现: 

(setq org-log-done 'time)
  
这时当你将一个项目从一个 TODO (未完成) 状态改变为一个完成状态时，标题下面就会插入一行 "CLOSED:[timestamp]"。如果你想和时间戳一起作一个记录，用: 

(setq org-log-done 'note)
  
这时会提示你输入一个记录 (note) ，并将它保存在标题为"Closing Note"项目之下。

一般是用 TODO 带上的
  
你可能想跟踪 TODO 状态的变化。可以只记录一个时间戳，也可以为变化作一个带时间戳的记录。记录会被插入到标题之后形成列表。当有很多记录之后，你可能希望将记录取出放到抽屉里。通过定制变量 org-log-into-drawer 可以实现这个功能。

对于状态记录，Org 可以实现基于每个状态关键字的设置。实现方法是在每个后的括号中指定"！" (记录时间戳) 或"@" (作一个记录) 。例如: 

#+TODO: TODO(t) WAIT(w@/!) | DONE(d!) CANCELED(c@)
  
将会设置 TODO 关键字和快速访问字母，以及当一个项目设为 DONE 时，会记录时间戳，当状态变为 WAIT 或 CANCELED 时，会作一个记录。这个语法也适用于变量 org-todo-keywords。

优先级

如果你广泛地使用 Org 模式，这样你就会有大量的 TODO 项。给它们设定优先级就很有必要。可以在 TODO 项的标题中加入一些标记 (cookie) 来设置它们的优先级，像这样: 

\*** TODO [#A] Write letter to Sam Fortune
  
Org模式支持三个优先级别: 'A'、'B'和'C'。'A'是最高级别，如不指定，'B'是默认的。优先级只在议程中有用。

C-c , 设置当前标题的优先级

S-UP/Down 增加/减少当前标题的优先级

归档

用org-mode来做TODO管理，那么无法避免的是，随着时间的流逝，被DONE的事件会越来越多，那么TODO被会被夹杂在DONE之间，难以查找。同时，由于后期回顾的需要，你也不想简单地将DONE事件删除掉。这个时候，你就需要归档命令了。归档，就是把你不想天天看到的东西，放到你看不到了，或者不怎么影响你的注意力的地方去。org-mode提供了两种归档方式。

内部归档

内部归档是在本文件内部给特定子树打上 ACHIVED 标签或者移动到名为 ACHIVED 的子树中去并打上标签。这个被认为是 ACIVED 的子树，会被移动了本级子树的最末端。

C-c C-x a 将某一个节点打上ARCHIVE标签

C-c C-x A 将当前节点归入一个名为Archive的子树中

并且这个子树是位于当前级别子树的最下方

外部归档

外部归档是指把子树移动到另一个org文件中去。文件名可以自定义。默认情况下，归档的子树会被移动到名为"当年文件名archived"的文件中去。

C-c C-x C-s 把当前的节点移到archived文件中去。

周期性 TODO

这我觉得是一个必不可少的功能……

只要对任务开始日期稍加修改，Org Mode 就能够管理周期性代办事项。比如周四要开会，可以设置如下代办事项: 

, * TODO 开会

如果是每周四都开会，就改写成如下的样子: 

, * TODO 开会

1w表示每周，另外1d表示每天，1m表示每月。对于周期性的任务， C-c C-t 每次将开始日期修改为相应的下一次开始日期，并保持 TODO 状态不变。

通常情况下，任务开始日期总是严格地按照预定间隔变动，但是当我们需要忽略 掉已经过期的日期时，就可以使用 + 或者 . 来修饰时间间隔，如

<2009-01-22 四 ++1w>

的下一次日期一定是今天之后的第一个星期四，而

<2009-01-22 四 .+1w>

的下一次日期是按今天算起的下一个星期，也就是说，不一定是星期四；如果今天是星期二，那么下一次开始日期就是星期二。

TODO TODO事项

Org-mode并不把TODO列表作为单独的一种文档来看待1. 相反,由于在记录的时候常常会有TODO事项发生,因此TODO事项被认为是记录文件中中不可分割的一部分! 使用Org可用很容易的把各级条目标记为TODO事项. 通过这种方法,可用避免信息的重复,同时TODO事项的整个内容也是可见的

当然,这种方式组织的TODO事项就会分散在你的记录文件的各个地方. Org-mode通过提供各种函数(这些函数能够告诉你待办事项的这个概览情况)来补偿这一点.

最基本的TODO功能 :标记和显示TODO事项

任何以·TODO·卡头的标题都被认为是TODO事项，例如 #+BEGINSRC org

\*** TODO Write letter to Sam Fortune
  
#+ENDSRC 关于TODO事项最重要的命令有: 

C-c C-t (org-todo)
  
让当前事项的TODO状态在`无` `TODO`和`DONE`之间切换 在timeline和agenda缓存区中,使用t命令键也能够实现这样的切换(参见agenda缓存区中的命令)
  
C-u C-c C-t
  
使用补全方式或快速选择界面(需要设置)来选择特定的TODO关键字, 若要使用快速选择界面,你需要給每个TODO状态分配快捷键,更多信息,参见为各个文件分配TODO关键字和设置tags
  
S-<right> / S-<left>
  
循环选择下一个/上一个TODO状态. 在事项有超过两个TODO状态的时候最有用(参见章节扩展TODO关键字). 要了解`shift-selection-mode`对改名了的而影响,参见章节与Org mode冲突的包.参见变量`org-treat-S-cursor-todo-selection-as-state-change`变量的说明
  
C-c / t (org-show-todo-key)
  
在一个 sparse tree中查看TODO事项. 这回折叠起整个buffer只显示所有的未完成事项及其标题. 在命令前加上前缀(C-u C-c / t)可用搜索指定的TODO状态,你会被要求输入需要搜索的TODO状态(可用'KWD1|KWD2'的形式输入多个TODO状态),命令会列出匹配的所有事项. 如果调用该命令时附加了一个数字型的前缀参数N,则会匹配变量`org-to-keywords`中的第N个TODO状态. 如果调用该命令时加了两个前缀参数,则所有未完成和已完成的事项都会被找出来
  
C-c a t (org-todo-list)
  
显示全局的TODO列列表,从所有加入agenda的文件(参见Agenda视图)中收集所有的未完成事项到一个缓冲区中. 这个新buffer会处于agenda-mode,agenda-mode提供了很多命令来查看,操作buffer中的这些TODO事项(参见章节agenda buffer中的命令). 更多信息请见章节全局代办列表
  
S-M-<RET> (org-insert-todo-heading)
  
在当前TODO事项下面增加一个新的TODO事项
  
改变TODO状态也会触发tag改变事件. 细节方面请参见选型'org-todo-state-tags-triggers'的docstring

扩充TODO关键字 :工作流和委派

默认情况下,TODO事项只有两种状态:TODO和DONE. Org-mode允许你通过设置`TODO 关键字`来对自己的TODO事项进行划分.(保存在`org-todo-keywords`中). 不同的文件可用有自己独特的TODO关键字设置.

需要注意的是可用通过打tag的方式来对标题和TODO事项进行区分(参见章节Tag)

标示工作流状态的TODO关键字 :一步步的从TODO状态演化到DONE状态
  
你可以使用TODO关键字来标示事项处于工作流程中的不同状态.例如2

(setq org-todo-keywords
    
'((sequence "TODO" "FEEDBACK" "VERIFY" "|" "DONE" "DELEGATED")))
  
这个`|`竖线划分了哪些状态是属于未完结状态,哪些状态是出于已完结状态. 如果你没有提供分隔线,那么最后那个状态被认为是已完结状态. 通过上面这个配置之后,当用命令`C-c C-t`切换状态时,会先从TODO切换到FEEDBACK,然后是FEEDBACK,最后是DONE和DELEGATED状态. 你也可以使用数字前缀来快速选择特定的状态,例如`C-3 C-c C–t`会使得状态立即编程VERIFY. 你也可以使用`S-<left>`来在这个序列中回退状态. 如果你定义了太多的状态,你可以使用in-buffer补全(参见补全章节)甚至是单个特定的选择键(参见章节快速设定TODO状态)来插入特定的TODO状态. 你也可用设定当改变TODO状态时记录下当时的时间戳数据,更多信息请参见跟踪TODO状态的改变

标示类型的TODO关键字 :这件事情我来做,其他的由Fred负责
  
你还可以使用TODO关键字标示事项的不同类型. 例如,你可能向标示有些事情是工作事项,有些事情是生活事项. 或者当你与其他人共同合作一个项目时,你可能想分派任务給某个人,这时你可以直接把那些人的名字当作TODO关键字来使用. 配置可能如下所示

,(setq org-todo-keywords '((type "Fred" "Sara" "Lucy" "|" "DONE")))
  
这时,这些关键字并不是用来标示工作流程中的不同状态的,它们被用来标示不同的类型. 所以这个时候的工作流程是:先把任务分配給某个人,然后等这件事完成了之后,再标记它为DONE状态. 它也支持使用命令`C-c C-t`3来切换状态. 若你连续按几次`C-c C-t`的话(经过了一个循环之后),`C-c C-t`会变回去,再不同人物之间切换循环. 而当你中断了连续的`C-c C-t`做了其他操作之后之后,再按`C-c C-t`,该命令又变回从人物直接跳到DONE状态了. 同样的,你也可以用前缀参数或补完功能来快速选择特定的人物. 你还可以通过在sparse tree中查看某个特定人物的所有代办事项,方法是在`C-c / t`前加前缀的数字参数. 例如,如果你想看分配給Lucy的所有事项,你可以用命令`C- C-c / t`来查看. 同样的道理,若你想在一个单独的buffer中查看Lucy在agenda中各org文件记录的代办事项,你可以用命令`C- C-c a t`

在一个文件中设置多个关键字 :混用所有关键字
  
有时候,你可能想使用平行的多个TODO关键字集合. 举个例子来说,你可能向保留有基本的`TODO/DONE`,但是同时需要为bug修复定义一套工作流程状态,并且你还需要一个独立的状态表示事项已经被取消了(这是事项的状态不能是DONE,但是它也没有下一步的行动了). 这时你的配置可能如下

(setq org-todo-keywords
        
'((sequence "TODO" "|" "DONE")
      
(sequence "REPORT" "BUG" "KNOWNCAUSE" "|" "FIXED")
      
(sequence "|" "CANCELED")))
  
各个平行的关键字集合之间的关键字不能出现重复,因为Org-mode需要根据该关键字决定该事项是属于哪种流程状态的. 这样子配置之后,`C-c C-t`只会在各个子序列内部循环切换状态,在这个例子中,`DONE`会先切换到`无`再切换到`TODO`,`FIXED`会切换到`无`再切换到`REPORT`. 因此你需要一种方法来让你在最初选择错误的时候可以切换到其他平行的子序列中. 除了直接敲入关键字或者使用补全功能选择关键字之外,你还可以通过以下命令实现这个目的:

C-u C-u C-c C-t / C-S-<right> / C-S-<left>
  
这些按键会从一个TODO子序列跳到下一个TODO子序列中,在上一个例子中,`C-u C-u C-c C-t`和`C-S-<right>`会从`TODO`或`DONE`直接跳到`REPORT`状态,然后跳到`CANCELED`状态. 需要注意,这里`C-S-<key>`的键绑定是和`shift-selection-mode与Org-mode冲突的包`冲突的
  
S-<right> / S-<left>
  
这俩命令会遍历所有子序列中的所有关键字,因此S-<right>会从`TODO`到`DONE`再到`REPORT`. 同样的,它也可能与`shift-selection-mode`有冲突,更多细节参见与Org-mode冲突的包
  
快速选择TODO状态 :通过单个字母快速选择TODO状态
  
如果你想快速改变事项的状态为某个状态,而不是在各个状态之间遍历,你可以为每个状态指定一个单字母的快捷键. 方法是在每个状态后面加上用括号括住的快捷键.像这样:

(setq org-todo-keywords
        
'((sequence "TODO(t)" "|" "DONE(d)")
      
(sequence "REPORT(r)" "BUG(b)" "KNOWNCAUSE(k)" "|" "FIXED(f)")
      
(sequence "|" "CANCELED(c)")))
  
你键入`C-c C-t`然后输入状态的快捷键就会立即切换到指定的状态了. 如果你想去掉事项上的状态标识,则用`空格`代替快捷键4

为各个文件设置独立的关键字 :不同的文件有不同的需求
  
很多时候我们需要为不同的文件设置不同的TODO关键字. 通过增加一些特殊的行,你可以为每个文件设置自己独有的TODO关键字. 例如,你可以在文件的任何一行定格写

#+TODO: TODO FEEDBACK VERIFY | DONE CANCELED
  
#+TYP_TODO: Fred Sara Lucy Mike | DONE
  
(你也可以使用`#+SEQTODO`,它的意思跟`#+TODO`一样,但是表达更清晰) 若需要定义多个平行的子序列,则这样配置:

#+TODO: TODO | DONE
  
#+TODO: REPORT BUG KNOWNCAUSE | FIXED
  
#+TODO: | CANCELED
  
你可以用补全的方式保证输入的关键字无误,方法是输入`#+`然后按下`M-<TAB>`

请注意,`|`后面的状态关键字(如果没有`|`则最后一个关键字)必须是代表完结状态的关键字(不一定需要DONE). 在输入完这些以`#+`开头的配置信息后,在配置信息行按下`C-c C-c`使该行的配置信息生效5

TODO关键字的显示方式 :高亮状态
  
Org-mode为不同的状态关键字分配了不同的显示方式(emacs中大概是以face这个概念来表示显示方式). 默认情况下对于那些表示还未完结状态的状态关键字使用`org-todo`这个face,对于那些表示已完结状态的状态关键字使用`org-done`这个face. 如果你用到了2个以上的不同类别的状态,你可以通过配置变量`org-todo-keyword-faces`来为不同的状态关键字分配不同的face. 举个例子

(setq org-todo-keyword-faces
        
'(("TODO" . org-warning) ("STARTED" . "yellow")
      
("CANCELED" . (:foreground "blue" :weight bold))))
  
像上面例子中`CANCELED`关键字这样直接定义face属性列表的方式,有可能不能正确的显示出来. 所以最好还是定义一个face然后使用它. 像`STARTED`这样,后面输入的是一个字符串的话,该字符串被解释成是颜色. 而变量`orgfaceseasyproperties`定义了改颜色是前景色还是背景色.

TODO事项之间的依赖关系 :当一个任务需要等待其他任务的时候
  
Org文件是由层级关系和列表组成的,这样的结构使得定义代办事项之间的依赖关系变得很容易. 通常在所有子任务完成之前是不能把父任务标记为完成状态的. 同时平级任务之间也可能存在一定的逻辑关系,使得后面的任务需要等待前面的任务都完成之后才能完成. 通过定义变量`org-enforce-todo-dependencies`,Org会阻止父任务在其子任务全部都完结的情况下被标记为完结状态. 此外,如果某个事项定义了`ORDERED`属性,那么它的子任务只有在前面子任务都完成之后才能被标识为已完成状态.下面是一个例子

  * TODO Blocked until (two) is done
  
    ** DONE one
  
    ** TODO two 
  * Parent
  
    , :PROPERTIES:
  
    , :ORDERED: t
  
    , :END:
  
    ** TODO a
  
    ** TODO b, needs to wait for (a)
  
    ** TODO c, needs to wait for (a) and (b)
  
    C-c C-x o (orgtoggleorderedproperty)
  
    打开/关闭当前事项的`ORDERED`属性. 之所以要用给事项定义属性的方式来声明这种顺次的逻辑关系是因为这种逻辑关系往往只是对某项任务是这样的,它不像tag一样具有继承的特性. 当然如果你觉得属性常常被折叠起来不容易看到的话,也可以使用tag来跟踪该属性的变化,方法是定义变量`org-track-ordered-property-with-tag`.
  
    C-u C-u C-u C-c C-t
  
    绕开状态的那些限制,强制更改TODO状态
  
    如果你设置了变量`org-agenda-dim-blocked-tasks`, 那么那些由于依赖关系未满足而无法关闭的代办事项在agenda视图中以灰色字体显示甚至是不显示(参见章节Agenda视图).

你也可以使得这种依赖关系对于checkbox也有效(参见章节checkbox).你可以设置变量`org-enforce-todo-checkbox-dependencies`. 然后如果某事项有未勾选掉的checkbox的话,也无法切换成完结状态

如果你需要更复杂的依赖关系(例如在不同的树n型结果或文件之间的依赖关系),请使用`org-depend.el`模块

记录处理过程 :记录处理过程的时间点和附加信息

Org-mode可以在你把代办事项从未完结状态切换到完结状态的时候记录下时间戳和其他一些信息,你甚至可以让它在每次切换状态的时候就记录下这些信息. 这套系统具有很高的可配置性,你可以对某个关键字,或某个文件甚至某个子树范围进行这样的配置. 要了解如何为事项统计所花的工作时间,可以参见章节统计工作时间

结束任务 :你是什么时候结束这项任务的
  
能够跟踪某任务什么时候完成是最基本的记录功能. 这项功能可以通过下面这条语句开启6

(setq org-log-done 'time)
  
之后,每次你把一项未完结状态的任务切换到已完结状态的时候,都会在该任务标题下插入一行`CLOSED:[时间戳]`. 如果你把该任务状态又切换回未完结状态,这一行会被删除掉. 如果你希望除了记录时间戳还可以记录一些附加信息,配置7

(setq org-log-done 'note)
  
这样当你把未完结状态的任务切换到已完结状态时,会被提示输入要保存的附加信息,该附加信息会存储在该任务下面,并以`Closing Note`开头

在timeline(参见章节单个文件的Timeline)和agenda(参见章节周/日agenda)视图中,你可以使用`l`键来显示每日带有'CLOSED'时间戳的代办事项,它会给你一个已完成事项的总括

跟踪任务状态 :什么时候任务状态发生了改变
  
有时候你可能想跟踪任务什么时候状态发生了改变,可能还想在状态发生改变的时候记录一些附加信息. 这些信息在插入时会插入到该事项标题的后面作为最新的信息列在第一排8. 如果记录的附加信息太长了的话,你可能会希望把这些附加信息放入一个'抽屉'(drawer)中. 要实现这一点,需要配置变量`org-log-into-drawer`–推荐使用名为`LOGBOOK`的drawer. 若你想为某个子树设置其他的drawer方式,你可以为这个子树定义`LOGINTODRAWER`属性.

Org-mode可以为每个TODO关键字定义记录时间戳和附加信息的行为. 你可以在关键字后面用括号括住`!`(表示记录时间戳)或者`@`(表示记录时间戳和附加信息).下面是一个配置的例子

(setq org-todo-keywords
    
'((sequence "TODO(t)" "WAIT(w@/!)" "|" "DONE(d!)" "CANCELED(c@)")))
  
如果你想对配置了`@`的关键字只记录时间戳,不记录附加信息的话,只需要在提示输入附加信息的时候直接按下`C-c C-c`就行,这会提交一个空白的附加信息

在上面的例子中,你不仅定义了全局的TODO关键字,定义了它们的快捷键,而且你还指定了当事项设置为`DONE`状态的时候,记录下当时的时间戳9. 当事项状态改为`WAIT`或`CANCELED`的时候,会提示记录下附加信息. 注意到`WAIT`状态有一个`/!`标志,这表示当离开WAIT状态进入到一个不记录任何信息的状态的时候,记录下当时的时间戳. 也就是说,当从`WAIT`切换到`DONE`状态的时候,并不触发记录时间戳的动作,因为DONE已经被配置为记录时间戳了. 而当从WAIT切换到TODO状态的时候,WAIT状态的`/!`设置会触发记录一个时间戳的动作,因为TODO并没有配置任何记录动作

你也可以把上面的设置限定到一个buffer中,方法是在buffer某行定格写

#+TODO: TODO(t) WAIT(w@/!) | DONE(d!) CANCELED(c@)
  
如果只想为某个子树或者某一个事项定义记录动作,你需要为改子树或者事项定义`LOGGING`属性. 如果你定义了非空的`LOGGING`属性,那么原先的记录动作的设置会被清空. 在配置`LOGGING`属性的时候,你可以使用`STARTUP`关键字(例如`lognotedone`或`logrepeat`).也可以明确指定为每个状态指定不同的记录设置(例如`TODO(!)`). 下面是一个例子

  * TODO Log each state with only a time
  
    , :PROPERTIES:
  
    , :LOGGING: TODO(!) WAIT(!) DONE(!) CANCELED(!)
  
    , :END:
  * TODO Only log when switching to WAIT, and when repeating
  
    , :PROPERTIES:
  
    , :LOGGING: WAIT(@) logrepeat
  
    , :END:
  * TODO No logging at all
  
    , :PROPERTIES:
  
    , :LOGGING: nil
  
    , :END:
  
    跟踪你的习惯 :你能坚持习惯多久
  
    Org可以用来追踪习惯的一致性,这里所谓的"习惯"指的是拥有下列特征的待办事项.

通过配置变量`org-modules`,启用了`habits`模块
  
是一个未完成的任务,有一个未完成的状态标示该任务有下一步的行动
  
`STYLE`属性值设置成了`habit`
  
该事项带有规划日期,而且规划日期中可以有`.+时间间隔`用来表示两次重复之间的间隔. `++时间间隔`表示该习惯有时间上的约束(比如,必须在周末完成),`+时间间隔`则表示改习惯不是一个经常性的事项,它可以在之前积压未办之事,然后在未来补完它(比如补写周报)
  
改习惯也可以使用类似`.+2d/3d`这样的符号标示最小/最大的间隔时间. `.+2d/3d`的意思是,你希望至少每三条做一次这个工作,但是最多每两天做一次这个工作
  
你最好为完结状态设置记录行为,这样会保留一些历史数据,这些历史数据可以以连线图的方式展现出来. 你不是必须要这样做,但是由此产生的连线图的意义就不大了.
  
为了给你一个直观的感受,下面展示一个带有历史数据的习惯的例子

** TODO Shave
  
, SCHEDULED: <2009-10-17 Sat .+2d/4d>
  
, - State "DONE" from "TODO" [2009-10-15 Thu]
  
, - State "DONE" from "TODO" [2009-10-12 Mon]
  
, - State "DONE" from "TODO" [2009-10-10 Sat]
  
, - State "DONE" from "TODO" [2009-10-04 Sun]
  
, - State "DONE" from "TODO" [2009-10-02 Fri]
  
, - State "DONE" from "TODO" [2009-09-29 Tue]
  
, - State "DONE" from "TODO" [2009-09-25 Fri]
  
, - State "DONE" from "TODO" [2009-09-19 Sat]
  
, - State "DONE" from "TODO" [2009-09-16 Wed]
  
, - State "DONE" from "TODO" [2009-09-12 Sat]
  
, :PROPERTIES:
  
, :STYLE: habit
  
, :LAST_REPEAT: [2009-10-19 Mon 00:36]
  
, :END:
  
这个例子的意思是:我希望最多每两天,最少每4天做一次这个事情(通过`SCHEDULED`日期和重复的时间间隔给定了). 假设今天是15号,那么在agenda中,该习惯会在17号(也就是2天之后)的地方显示生效. 在19号(也就是4天之后)的地方实效

把习惯用折线图展示出来可以显示在过去你坚持这项习惯的情况如何. 这个折线图显示了过去三个星期每天该习惯的完成情况,每天都根据完成情况用不同的颜色显示出来. 这些颜色有:

蓝色
  
表示当天任务没有完成
  
绿色
  
表示当天任务已经完成
  
黄色
  
表示任务在第二天就会过期了
  
红色
  
表示工作在当天已经延误了
  
另外除了用颜色标注每天的任务完成情况之外,弱于哪些任务在当天已经完成的任务会用星号标注出来. 会用感叹号标注当前日期出来.

org提供很多变量来改变agenda显示habit的方式

org-habit-graph-column
  
设定统计图从那一列开始画. 由于统计图会覆盖该列上的所有文本,因此最好保持你的habit标题简洁明了.
  
org-habit-preceding-days
  
指定从几天前开始统计数据
  
org-habit-following-days
  
指示统计到几天之后的数据
  
org-habit-show-habits-only-for-today
  
如果为非nil值的话,表示只在当天的agenda视图中显示habits. 默认情况下是设置为true的
  
最后,在agenda视图中按下`k`键会暂时让habit隐藏掉. 按'K'之后又会让habit显示出来. 它们也受到tag过滤的影响,例如你可以设定habit只能在某种特定的情况下才能被标记为完成.

优先级 :有些事情更重要一些

如果你经常使用Org-mode来进行任务安排的话,就应该会发现对各项任务分配优先级是很有必要的,方法是在TODO事项的标题前放上优先级标识(`priority cookie`),像这样:

\*** TODO [#A] Write letter to Sam Fortune
  
默认情况下,Org-mode支持从高到低三个优先级,分别表示为`A`,`B`,`C`. 如果某个任务没有分配优先级,则被认为是`B`优先级. 为任务分配优先级的意义仅仅在于在agenda视图(参见周/日agenda)中可以依照优先级对任务进行排序. 通过定义变量`org-priority-faces`,你可以为不同的优先级分配不同的显示方式(face)

优先级标识可以放在任何大纲节点前,而不一定要放在TODO事项前

C-c ,
  
设置当前任务的优先级(`org-priority`). 执行该命令后,会提示你输入代表优先级的`A` `B` `C`. 如果你输入的是<SPC>则标识去除任务中的优先级标识. 若你在timeline或agenda视图中时,则可以使用`,`命令来改变优先级.(参见章节agenda视图中的命令).
  
S-<up> (org-priority-up) / S-<down> (org-priority-down)
  
提升/降低当前任务的优先级10. 需要注意的时,这些键也同样可以用来改变时间戳(参见章节创造时间戳). 同样这些按键也可能与`shift-selection-mode`相互冲突,具体情况参见与Org-mode冲突的包
  
通过设置变量`org-highest-priority`,`org-lowest-priority`和`org-default-priority`的值,你可以自定义优先级的区间. 若想对某个文件设置优先级区间,你可以像下面那样设置(准照最高优先级,最低优先级,默认优先级的顺序来设置,同时请确保最高优先级在字母表上要比最低优先级靠前)

#+PRIORITIES: A C B
  
划分子任务 :划分任务为可管理的碎片

将一件很复杂的任务分解为简单一些,更易管理的子任务是很有必要的. 你可以在任务事项下面创建新的子树大纲(子任务作为子树的各节点)的方式来表达这种分层关系11. 若你想在父任务上显示子任务完成的情况,可以在父任务标题的任何地方插入`[/ ]`或`[% ]`. 每当有子任务被标识为已完结状态之后,这两个标识会被更新为子任务的完成进度,在这两个标识上按下`C-c C-c`也能够强制更新这两个标识的信息.下面是一个例子:

  * Organize Party [33%]
  
    ** TODO Call people [1/2]
  
    \*** TODO Peter
  
    \*** DONE Sarah
  
    ** TODO Buy food
  
    ** DONE Talk to neighbor
  
    如果一个任务标题下面既有check列表,也有代办的TODO子任务,那么org就不清楚应该怎么统计子任务的完成情况了. 这时需要设置属性`COOKIEDATA`的值为`checkbox`或者`todo`来明确指示统计时以哪个为准

如果你想在统计子任务完成情况的时候,不是仅仅统计直接下属的子任务的情况,而是统计所有层级的下属子任务,那么你需要配置变量`org-hierarchical-todo-statistics`. 如果你只是对某个特定的父任务有这种需求,那么为该父任务设置`COOKIEDATA`属性,并且确保该属性的值包含有`recursive`. 下面是一个例子

  * Parent capturing statistics [2/20]
  
    , :PROPERTIES:
  
    , :COOKIE_DATA: todo recursive
  
    , :END:
  
    如果你希望父任务在所有子任务都标记为完结状态后,自动也切换到完结状态,你可以用下面所示的配置:

(defun org-summary-todo (n-done n-not-done)
    
"Switch entry to DONE when all subentries are done, to TODO otherwise."
    
(let (org-log-done org-log-states) ; turn off logging
      
(org-todo (if (= n-not-done 0) "DONE" "TODO"))))

(add-hook 'org-after-todo-statistics-hook 'org-summary-todo)
  
当然,你也可以使用check列表代替子任务的作用

checkbox :标记列表

如果一个事项是不是以标题的形式而是以纯文本列表12(参见纯文本列表)的形式展现的,同时它又是以`[ ]`开头的,那么它就被当成是一个代检查事项(checkbox)看待. checkbox跟待办事项(参见待办事项)很类似,但是相比起来更加的轻量化. checkbox不回显示在全局的未完成事项列表(TODO列表)中,因此它常常用来表示将一个任务分隔成几个简单的步骤,或者用来作为待购清单来使用. 要切换checkbox的状态(完成/未完成状态),需要按下`C-c C-c`,或者使用鼠标点击(多亏了Piotr Zielinski的`org-mouse.el`)

下面是一个checkbox列表的例子

  * TODO Organize party [2/4]
  
    , - [-] call people [1/3]
  
    , - [ ] Peter
  
    , - [X] Sarah
  
    , - [ ] Sam
  
    , - [X] order food
  
    , - [ ] think about what music to play
  
    , - [X] talk to the neighbors
  
    checkbox具有继承的特性,因此如果一个checkbox具有子checkbox的话,对子checkbox的完成状态进行切换的时候,父checkbox也会自动根据是没有/部分/全部子checkbox完成状况来做出相应的改变

在上面例子中,第一行和第二行的`[2/4 ]`和`[1/3 ]`展示了一共有多少个checkbox,其中多少个checkbox一件完成了. 这使得你不用展开就能知道还剩下多少个checkbox没有完成. 这种统计信息的展示可以放在标题或者文本列表的任何地方,而且它只会统计直接子任务的完成情况13. 为了得到这种统计信息的展示,你需要自己输入`[/ ]`或`[% ]`. 如果你使用的是`[/ ]`,那么你会得到`[n/m]`这样的展示方法(n表示已完成数,m表示未完成数). 如果你输入的是`[% ]`,那么你会得到一个百分比的展示. 若在标题的子树下,既有TODO事项,又有checkbox,那么展示的可能为TODO事项的统计结果(若触发改变的是由于子TODO事项的状态改变而引起的)也可能是checkbox的统计结果(若触发改变的结果是由于checkbox的状态改变引起的),这样就显得很混乱. 要解决这个问题,设置该标题的`COOKIEDATA`属性值为`checkbox`或者`todo`即刻

如果在当前的大纲节点上加了`ORDERED`属性,这就告诉orgcheckbox必须从上到下一个一个的被完结, 否则会有报错.

关于checkbox的命令有以下这些:

C-c C-c (org-toggle-checkbox)
  
切换光标所在checkbox的完结状态. 如果加了一个前置参数(也就是用按键`C-u C-c c-c`)则增加/移除checkbox标志(使它在checkbox和普通列表之间切换)14, 如果加了两个前置参数(`C-u C-u C-c C-c`)则checkbox的标志设为`[-]`,这种标志的意思是其为一种中间状态
  
C-c C-x C-b (org-toggle-checkbox)
  
切换光标所在checkbox的完结状态. 如果加了两个前置参数(`C-u C-u C-c C-c`)则checkbox的标志设为`[-]`,这种标志的意思是其为一种中间状态
  
如果存在一个选择域,则切换该选择区域的第一个checkbox的完结状态,同时选择区域的其他checkbox的完结状态都改为以第一个checkbox的完结状态为准. 如果调用该命令时带了一个前置参数(`C-u C-c C-x C-b`)则增加/删除该区域中所有事项的checkbox标志
  
如果对一个标题进行该操作, 则切换该标题到下一标题间的所有checkbox的状态(不是整个子树)
  
如果没有选择区域,则切换光标所在的checkbox的状态
  
M-s-<RET> (org-insert-todo-heading)
  
插入一个新的checkbox,这只有当光标处于普通列表中时才有效(参见普通列表)
  
C-c C-x o (org-toggle-ordered-property)
  
切换是否具有`ORDERED`属性. 如果你希望能够以tag的形式来最终`ORDERED`属性的值,你可以设置变量`org-track-ordered-property-with-tag`
  
C-c # (org-update-statistics-cookies)
  
更新当前大纲项的统计信息, 若使用了`C-u`前缀,则更新整个文件的统计信息. 当你用`C-c C-c`切换一个checkbox的完结状态或者用`M-S-<RET>`新增加一个checkbox的时候,会自动更新checkbox的统计信息. 同样,当改变TODO事项的状态时,也会自动更新TODO事项的统计信息. 但是如果你删除checkbox和TODO事项,或者手工增加/修改checkbox和TODO事项,那你就需要手工调用这个命令,以强制同步更新统计数据
  
footnote

Footnotes:

当然,你可以创建一个只包含TODO事项列表的文档,但这并不是必须的

改变这个变量之后,需要重启Org mode才能生效

这一点对于timeline和agenda缓存区中的t命令也适合

如果你不想区分tag和todo状态的话,通过配置变量`org-fast-tag-selection-include-todo`可以让你在改变tag的时候自动改变TODO状态(参见章节设置tag).注意,这意味着你需要为两组关键字分配相同的快捷键

Org-mode只在读入文件的时候才会去解析这些配置行. 在以`#+`开头的行按下`C-c C-c`的作用是为当前buffer重启一次Org-mode

对应的文件内设置是#+STARTUP: logdone

对应的文件内设置是#+STARTUP: lognotedone

参见变量`org-log-states-order-reversed`

当你设置了STARTUP参数`org-log-done`,同时又为状态设置了记录动作的时候,就有可能出现连续记录了两次时间戳的情况. 然而,即使你两边都配置了记录附加信息的动作,org也不会提示你输入两次附加信息.为状态单独设置的记录动作会优先执行.

另见选项`org-priority-start-cycle-with-default`

如果你希望全局的TODO列表中不现实子任务,参见`org-agenda-todo-list-sublevels`

默认不包括描述列表在内. 但是通过修改`org-list-automatic-rules`你也可以允许描述列表成为checkbox

如果你希望统计的时候统计所有层次的下级checkbox而不仅仅是直接子checkbox,那你需要修改变量`org-hierarchical-checkbox-statistics`

如果在列表的第一行使用`C-u C-c C-c`,而刚好这一行事项没有checkbox标识. 则会给该列表所有事项都加上checkbox的标识