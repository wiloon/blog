---
title: Windows PowerShell
author: "-"
date: 2012-03-12T04:28:25+00:00
url: powershell
categories:
  - Windows
tags:
  - reprint
---
## Windows PowerShell

```Bash
# 查看 power shell 版本
$PSVersionTable

# 查看安装路径 
$PSHOME
```

### install

https://github.com/PowerShell/PowerShell/releases

```bash

Set-Aliasll dir

```

[http://marui.blog.51cto.com/1034148/290067/](http://marui.blog.51cto.com/1034148/290067/)

Windows PowerShell 是一种命令行外壳程序和脚本环境，使命令行用户和脚本编写者可以利用 .NET Framework 的强大功能。它引入了许多非常有用的新概念，从而进一步扩展了您在 Windows 命令提示符和 Windows Script Host 环境中获得的知识和创建的脚本。

目录

Windows PowerShell 简介
  
PowerShell脚本十个基本概念

Windows PowerShell 简介

目标受众
  
Windows PowerShell 入门主要面向之前没有 Windows PowerShell 背景知识的 IT 专业人员、程序员和高级用户。虽然具备脚本和 WMI 方面的背景知识会有所帮助，但是理解本文档并不假定或要求您具备此方面知识。
  
关于 Windows PowerShell
  
通过解决长期存在的问题并添加一些新的功能，Windows PowerShell 旨在改进命令行和脚本环境.
  
关于 Windows PowerShell
  
通过解决长期存在的问题并添加一些新的功能，Windows PowerShell 旨在改进命令行和脚本环境。
  
可发现特性
  
您可轻易发现 Windows Powershell 的功能。例如，若要查找用于查看和更改 Windows 服务的 cmdlet 列表，请键入:
  
get-command *-service
  
在发现可完成任务的 cmdlet 之后，可以使用 Get-Help cmdlet 了解有关该 cmdlet 的详细信息。例如，若要显示有关 Get-Service cmdlet 的帮助，请键入:
  
get-help get-service
  
若要充分理解该 cmdlet 的输出，则可通过管道将其输出传递给 Get-Member cmdlet。例如，以下命令将通过 Get-Service cmdlet 显示有关该对象输出的成员的信息。
  
get-service | get-member
  
一致性
  
管理系统可能是一项复杂的任务，而具有统一接口的工具将有助于控制其固有的复杂性。然而，无论是命令行工具还是可编写脚本的 COM 对象，在一致性方面都乏善可陈。
  
Windows PowerShell 的一致性是其主要优点中的一项。例如，如果您学会了如何使用 Sort-Object cmdlet，则可利用这一知识对任何 cmdlet 的输出进行排序。而无需了解每个 cmdlet 的不同的排序例程。
  
此外，cmdlet 开发人员也不必为其 cmdlet 设计排序功能。Windows PowerShell 为他们提供了框架，而该框架可提供基本的功能，并强制他们在接口的许多方面保持一致。该框架虽然消除了通常会留给开发人员的某些选项，但作为回报，开发强健、易于使用的 cmdlet 的工作将更加简单。
  
交互式脚本环境
  
Windows PowerShell 将交互式环境和脚本环境组合在一起，从而允许您访问命令行工具和 COM 对象，同时还可利用 .NET Framework 类库 (FCL) 的强大功能。
  
此环境对 Windows 命令提示符进行了改进，后者提供了带有多种命令行工具的交互式环境。此外，还对 Windows Script Host (WSH) 脚本进行了改进，后者允许您使用多种命令行工具和 COM 自动对象，但未提供交互式环境。
  
通过将对所有这些功能的访问组合在一起，Windows PowerShell 扩展了交互用户和脚本编写者的能力，从而更易于进行系统管理。
  
面向对象
  
尽管您可以通过以文本方式键入命令与 Windows PowerShell 进行交互，但 Windows PowerShell 是基于对象的，而不是基于文本的。命令的输出即为对象。可以将输出对象发送给另一条命令以作为其输入。因此，Windows PowerShell 为曾使用过其他外壳程序的人员提供了熟悉的界面，同时引入了新的、功能强大的命令行范例。通过允许发送对象 (而不是文本) ，它扩展了在命令之间发送数据的概念。
  
易于过渡到脚本
  
使用 Windows PowerShell，您可以很方便地从以交互方式键入命令过渡到创建和运行脚本。您可以在 Windows PowerShell 命令提示符下键入命令以找到可执行任务的命令。随后，可将这些命令保存到脚本或历史记录中，然后将其复制到文件中以用作脚本。
  
识别你即将使用的Provider 通过识别PowerShell里安装的Provider，你就可以了解默认安装下PowerShell提供了那些能力。 Provider可以使用一种简单的访问方式，暴露位于不同储存位置的数据。就像是浏览不同磁盘上的目录结构一样简单。 Provider把不同的信息存放位置，表示成"驱动器"-目录这种结构，这样很容易被用户所理解。就像我们要访问一个位于D盘的WIN32目录下的SETUP.exe文件，我们要通过浏览器，单击D盘的图标，然后选择WIN32目录并双击一样，如果我们要访问位于"注册表"的数据，那么我们也只需要简单地通过Set-Location命令，来到到"REGISTRY"这个"驱动器"，然后用GET-CHILDITEM命令获取其子数据就行了。 注: 实际上，PowerShell访问磁盘驱动器，也是通过Provider的，切换驱动器其实和切换其他数据容器是一样地操作。 例如:  Set-Location d: 这是切换驱动器 Set-Location HKLM: 这是切换到注册表的HKLM键 另外，Get-PSprovider命令，可以查看当前已经安装的所有PROVIDER。任何熟悉.NET编程的人，都可以编写Provider。当新的provider被安装后，就叫做snap-in。snap-in其实是一个动态连接库dll文件，可以被安装到powershell中。然而，当一个snap-in安装后，却没有办法卸载。 Get-PSProvider:  Name Capabilities Drives -- ---- -- Alias ShouldProcess {Alias} Environment ShouldProcess {Env} FileSystem Filter, ShouldProcess {C, D, F, A...} Function ShouldProcess {Function} Registry ShouldProcess {HKLM, HKCU} Variable ShouldProcess {Variable} Certificate ShouldProcess {cert} 这些就是我机器上的默认安装后的provider。
  
使用Set-Location和Get-ChildItem浏览数据 Set-Location用于改变当前目录，以及选择当前的provider，而Get-ChildItem用于获取当前目录或者指定目录下的子对象:  例子:  set-location hkcu:software get-childitem 例子2:  GCI -path HKLM:software
  
有两种连接WMI服务的方法: l 使用Get-WmiObject可以很容易地连接到WMI服务，并且获取WMI对象。 l 使用一个COM对象，"WbemScripting.SWbemLocator"，可以连接WMI的服务。SWbemLocator对象只有一个方法，就是ConnectServer()。该方法接受5个参数: 用户名，密码，语言代码，验证方法 (Kerberos, NTLM等) ，标志 (超时值) 。下例中，我们使用New-Object命令，创建了一个"WbemScripting.SWbemLocator"的实例。然后用这个实例的ConnectServer方法连接了到了一个WMI的名字空间 (rootcimv2) ，ConnectServer方法返回了一个WMIService对象，接着又用这个对象的subClassesOf () 方法，返回了一系列WMI的CLASS:  $strComputer = "." $wmiNS = "rootcimv2" $strUsr ="" #Blank for current security. DomainUsername $strPWD = "" #Blank for current security. $strLocl = "MS_409" #US English. Can leave blank for current language $strAuth = "" #if specify domain in strUsr this must be blank $iFlag = "0" #only two values allowed: 0 and 128. $objLocator = New-Object -comobject "WbemScripting.SWbemLocator" $objWMIService = $objLocator.ConnectServer($strComputer, \` $wmiNS, $strUsr, $strPWD, $strLocl, $strAuth, $iFLag) $colItems = $objWMIService.subClassesOf() Write-Host "There are: " $colItems.count " classes in $wmiNS" foreach ($objItem In $colItems) { $objItem.path_.class }新脚本语言由于以下原因，Windows PowerShell 使用它自己的语言，而不是重用现有的语言:
  
Windows PowerShell 需要用于管理.NET 对象的语言。该语言需要为使用cmdlet 提供一致的环境。该语言需要支持复杂的任务，而不会使简单的任务变得更复杂。 · 该语言需要与在.NET 编程中使用的高级语言 (如C#) 一致
  
编辑本段
  
PowerShell脚本十个基本概念

1. PS1文件
  
一个PowerShell脚本[1]其实就是一个简单的文本文件，这个文件包含了一系列PowerShell命令，每个命令显示为独立的一行，对于被视为PowerShell脚本的文本文件，它的文件名需要使用.PS1扩展。
  
2. 执行权限
  
为防止恶意脚本的执行，PowerShell有一个执行策略，默认情况下，这个执行策略被设为受限的 (Restricted) ，意味着PowerShell脚本无法执行，你可以使用下面的cmdlet命令确定当前的执行策略:
  
Get-ExecutionPolicy 你可以选择使用的执行策略有:
  
Restricted - 脚本不能运行。 RemoteSigned - 本地创建的脚本可以运行，但从网上下载的脚本不能运行 (除非它们拥有由受信任的发布者签署的数字签名) 。 AllSigned – 仅当脚本由受信任的发布者签名才能运行。 Unrestricted – 脚本执行不受限制，不管来自哪里，也不管它们是否有签名。
  
你可以使用下面的cmdlet命令设置PowerShell的执行策略:
  
Set-ExecutionPolicy 3、运行脚本
  
如果你想从命令行运行一个可执行文件，多年来一个永恒不变的方法是，在命令行转到该执行文件所在的位置，然后键入该执行文件的名称，但这个古老的方法现在却不能适用于PowerShell可执行脚本了。
  
如果你想执行一个PowerShell脚本，通常必须键入完整的路径和文件名，例如，假设你要运行一个名为a.PS1的脚本，你可以键入:
  
C:Scriptsaps1 最大的例外是，如果PowerShell脚本文件刚好位于你的系统目录中，那么你可以直接在命令提示符后键入脚本文件名即可运行，如:
  
.a.ps1 注意前面需要加上.，这和Linux下执行Shell脚本的方法如出一辙。
  
4. 管道
  
管道的作用是将一个命令的输出作为另一个命令的输入，两个命令 (或cmdlet) 之间只需要用管道符号 (|) 连接即可。
  
为了帮助你了解管道是如何工作的，我们以一个例子进行说明，假设你想创建运行在服务器上的进程列表，并按进程的ID号进行排序，可以使用Get-Process cmdlet命令获得进程列表，但默认情况下列表不会排序，如果将这个cmdlet命令的输出用管道输送给Sort-Object ID命令，进程列表将会按进程ID号进行排序，如:
  
Get-Process | Sort-Object ID 5、变量
  
虽然可以使用管道将一个命令的输出输送给另一个命令，但管道本身也是有限制的，当你用管道从一个命令向另一个命令传递输出结果时，输出结果立即被使用，但有时候，你可能需要保存输出结果一段时间，以便以后可以使用 (或重用) ，这个时候管道就应该下场，轮到变量上场了。
  
人们很容易将变量想象成一个仓库，但在PowerShell中，变量可以保存命令的完整输出，例如，假设你想保存服务器处于运行中的进程列表，你可以将它赋给一个变量，如:
  
$a = Get-Process 在这里，变量被命名为$a，如果你想使用这个变量，只需要简单地调用它的名称即可，例如，键入$a便可在屏幕上打印变量的内容。
  
你可以将多个用管道连接的命令的最终输出赋给一个变量，只需要用一对小括号将命令括起来即可，例如，假设你想按进程ID对运行中的进程进行排序，然后将结果输出给一个变量，你可以使用下面这个命令:
  
$a = (Get-Process | Sort-Object ID) 6、@符号
  
通过使用@符号，你可以将列表内容转换成一个数组，例如，下面的代码创建了一个名为$Procs的变量，它包含多行文本内容 (一个数组) : $procs = @{name="explorer","svchost"}
  
使用变量时你也可以使用@符号，为了确保它作为数组而不是单个值处理，例如，下面的代码将在我前面定义的变量上运行Get-Process cmdlet命令:
  
Get-Process @procs Windows将显示Windows资源管理器和Svchost使用的所有进程，注意变量前使用的@符号，而不是常见的$符号。
  
7. Split
  
Split操作符根据你指定的字符拆分一个文本字符串，例如，假设你想将一个句子拆分成一个单词组成的一个数组，你可以使用下面的命令做到:
  
"This is a test" -split " " 拆分后的结果如下:
  
This is a test 8、Join
  
就像Split可以将一个文本字符串拆分成多块一样，Join的操作则是逆向的，将多个独立的块连接成一个整体，例如，下面这行代码将会创建一个文本字符串，由我的名字和姓氏组成:
  
"Brien","Posey" -join " " 命令末尾双引号之间的空格告诉Windows在两个文本字符串之间插入一个空格。
  
9. 断点
  
运行一个新创建的PowerShell脚本时，如果脚本有Bug，会遇到意想不到的后果，保护自己的一个方法是在脚本的关键位置插入断点，这样你就可以确保脚本正常运行先，然后再处理可能存在的问题。
  
插入断点最简单的方法是根据行号插入，例如，假设你要在第10行插入一个断点，可以使用下面的命令:
  
New-PSBreakpoint -Script C:Scriptsa.ps1 -Line 10 你也可以将断点绑定到变量上，如果你希望你的脚本任何时候都可以修改a$的内容，可以使用下面的命令:
  
New-PSBreakpoint -Script C:scriptsa.ps1 -variables a 注意，我在变量名后并没有包括美元符号。
  
可以和PSBreakpoint一起使用的动词包括New，Get，Enable，Disable和Remove。
  
10. Step
  
调试一个脚本时，有时可能需要逐行运行脚本，这时你可以使用Step-Into cmdlet命令，它会使脚本一行一行地执行，不管有没有设置断点，如果你想从这种步进式运行模式退出来，使用Step-Out cmdlet命令即可，但需要注意的是，使用Step-Out cmdlet命令后，断点仍然有效。
  
顺便说一句，如果你的脚本使用了函数，你可能对Step-Out cmdlet更感兴趣，Step-Out的工作方式和Step-Into一样，不过，如果调用了一个函数，Windows不会逐步执行，整个函数将会一次性执行。
