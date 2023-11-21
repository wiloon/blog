---
title: dependency-library-service, 依赖 库, 服务
author: "-"
date: ""
url: dependency-library-service
categories:
  - inbox
tags:
  - inbox
---
## dependency-library-service, 依赖 库, 服务

### 依赖管理: 究竟该用库还是服务？

https://www.zybuluo.com/sambodhi/note/642554
http://blog.jessitron.com/2017/01/dependencies.html

依赖管理：究竟该用库还是服务？
当一个系统变得越来越复杂的时候，它必然大量的依赖外部系统和内部其他系统的服务或者库才能达成业务目标，因此，这个时候，对依赖进行有效的管理才能提升业务故障容忍度，这也是大系统小做的核心思路。

在现实生活中，要创造一个没有任何外部依赖的应用并非不可能，但也是极具挑战的。这也是为什么依赖管理对于每个软件项目都是至关重要的一部分。

通常来说，软件中的依赖关系通常包括编译时依赖、测试时依赖和运行时依赖。而从依赖形式上可以分为库依赖和服务依赖。那么问题来了，依赖管理，究竟该用库还是服务的形式呢？如何取舍？

Atomist的软件工程师Jessitron Kerr，日前写了一篇文章，阐述了她对依赖管理究竟用库还是服务的看法，分析了库和服务的对比、利弊、权衡等等方面，她的思路非常清晰，经作者Jessitron Kerr授权，InfoQ翻译并整理成本文，相信对各位读者有所帮助。

以下是正文。

依赖
依赖管理，没有人愿意去想这个问题。我们只是想让这些东西能够运行。它是软件中令人讨厌、悬而未决的问题之一。

每种语言系统都声称它们有包管理器和构建工具。这关系到依赖如何工作。有些系统确实做的比其他更好一些，但是没有一个是完整的。我们真的有点“一叶障目”。

依赖很重要。图像分析中的边界，边界总是罕有很多信息；但是比起图像中的节点，边界却容易被忽视。

依赖可以是相对显式的，比如在pom.xml或package.json中声明。它们可能很难发现，例如HTTP从配置、代码、输入构成的URL调用。

依赖描述了我们如何将事物联系在一起。这意味着，它们也决定我们如何选择分解。将事务分解是我们如何扩展软件系统：在我们自己头脑中调整，也就是说，根据复杂性做出调整，而非体积。

如果仔细看看依赖，希望它们不要再这么麻烦了，也许我们可以让它更接近正确。这个话题与本文相比，还有更多内容，但它只是一个开头。

库和服务的对比
两者最大的区别：定义。

库是编译的。它们在不同的存储库（或庞大的doom（也就是monorepo）库中的目录）中分为不同的模块，它们可能由不同的公司（至少是团队）维护。通过将相同的代码编译成多个应用程序（也称为服务）来实现代码复用。

作者在此处讨论的是编译范围（compile-scope）库。至于Provided-scope，以及像.dll（姑且这么称呼）是另外一个事物，应该可能是单独的类别，但本文不讨论这些。

服务：一个应用通过网络（或者通过同一台机器上的通信接口）调用另一个应用；代码在不同进程中运行。在如何找到对方有些繁琐费时：服务发现完全是自己的事，使用DNS是最常见的解决方案。

权衡
能见度
库是显式声明的，尽管并不总是特地声明。有些东西实际上会将代码引入我的代码中，无论是作为jar还是显式地作为代码。

如果有的话，服务依赖被非正式地声明。它们可能在日志记录中被发现。如果您选择允许哪些应用访问其他应用，则可能会从安全日志中看到它们。

部署
在我看来，这个差异很重要。

库：你可以发布它要求人们升级。如果你的库是内部的，你甚至可以升级其他团队的代码中的库版本。但是，只有用户能够决定何时正式应用这个新版本。当用户选择部署升级代码时，你的新代码才会随之升级。

服务：何时升级由你决定。你将旧代码转为新代码来部署，就这样。每个使用你的服务的人，都会随时使用新代码。就这样，突然间你有了这个权利。这也意味着，你可以选择一次性运行多少服务。这点是人们感到兴奋的独立可扩展性。

如果你的库或者服务有数据支撑，那么控制代码部署意味着数据格式有很多。如果数据库仅由服务来访问，那么可以将任何必要的翻译到代码中去。如果数据库被其他人合并的库访问，那么最好保持模式兼容。

版本控制
Rich Hickey曾经说过关于库的版本控制，其中大部分，也适用于服务。这里是我的笔记。

如果将接口更改为库，那么你就拥有了不同的库。如果你为它用同一个名称，并称为新版本，那么就有了一个不同的库，它拒绝与同一个库一起编译，并为阻碍大打出手。然后你就遇到版本冲突的问题。不同的语言系统的解决方式不同。当应用声明对两个库的依赖时，会发生版本冲突，每个库都声明对同名第四个库的依赖。在JavaScript中，无论如何，我们都可以在两者中编译，它不过是代码复制。而在Java中，你很可能在给定的ClassLoader中每个类名只有一个定义，所以工具选择最新版本，希望每个人都能应付。

服务，你可以弄得很复杂，做成某种版本的路由选择；也可以在生产中，同时运行多个版本的服务。明白了吗？你将同一个服务成为两个版本，但实际上是两个不同的服务，与库相同。或者，你可以在在统一代码中支持API的多个版本。向后兼容性，是你和所有实际可工作软件的痛点。

API更改和向后兼容性
因此，你要改变用户和你的代码的交互方式。这里有一个很重要的区别：更改代码（重构、错误修复、完全重写）与要求客户为正确应用更改代码而更改是非常不同的，这是一个严重的影响。

服务：谁使用它？也许它是一个内部服务，你有通过grep来查看所有公司代码中使用你的URL的念头，对吧？你可以选择与这些团队来更改你的服务的使用。或者采取面向公众的服务。不要改变。你永远不知道谁在使用它。这确实令人沮丧。否则，你需要永久的向后兼容性。没错，你的代码将会变得令人厌恶。

库：如果你的包管理器相当好（意即不可变，如果它提供了某种库的版本，就永远将继续提供相同的下载），那么，旧版本的库仍然存在，他们可以留在生产环境中使用。你不能取消这个代码。但是，你可以令那些对版本号没有明确具体的用户心碎。这就是语义版本控制的所在。除了主版本的API的任何改变是鲁莽的，人们应该谨慎使用库的新的主版本。但如果你很友善，为它们取不同的名字，而不是假装同一个东西的不同版本号。

隔离
关于库的一个窍门：很难知道“什么是API更改？”

有了服务，事情就变得明了了：我们辨别出某些请求，并提供某种回应。

而使用库，就意味着所用的都是公用方法和公共类还有包……嗯，就像Java/Scala编码器那样，我甚至都没有特别注意我是否公开了。但是库的作者需要的话，他们会安全地变更库的内容。

服务是隔离的：你不能依赖我内部，因为你主体无法访问它们。为了显示出任何外部使用，我必须作出明确的决定。这是更为强大的模块化。这也意味着你可以用不同的语言来写它们。这是一个优势。

有几家公司在销售库。那些都是严肃的专业人士。他们必须从历史版本开始测试，在每个操作系统确保它们可以运行。他们必须清楚意识到暴露了什么，还要在很多情况下测试新版本。将它们扔在那里实用得多：即时向后兼容性是一个巨大的痛苦，但至少你知道它在哪里。

失败
库：一旦它失败，你的代码就会随之失败。它耗尽内存、进程中断。故障被同步传送，如果它失败，应用会感知到。

服务：如果它失效，或者没有回应，你真的不会知道它已经失效了。部分故障、不确定的故障，查找出来很难。就算在通过套接字协调的同一台机器上，也不能保证响应时间，或者响应是否传递。这是所有的使用这种模块化机制的主要代价。

结论
我认为选择是使用库还是服务来分配工作/模块化的最大考虑是选择哪种以及决定什么时候部署。谁在给定时间在生产环境中控制那些代码。

库更高效，更容易处理故障。这是一个事物。进程间通信更快，故障更容易处理，并且有可能达到一致性。

实际上，服务是去耦的。让一个团队负责自己的软件，编写并运营它。让团队于给定时间在生产中进行选择：这意味着不断变化的数据源或模式的希望。一般来说，我认为，由于在数据中存在的惯性，数据有很大的价值。在讨论软件架构时，重视不够。如果你有可靠的服务接口来保护你的数据访问，你可以（与棘手的工作）将其移动到不同的数据库或格式。否则，数据迁移就无从谈起。

随着组织的日益壮大，部署时解耦对于保持发展的势头至关重要。功能和语言系统的解耦、版本、工具都有所帮助。要求每个人都使用相同的工具（或但愿不会如此，存储库）是以可避免的方式将每个团队耦合到另一个团队。

总体来说，库更快，直到协调成为瓶颈。而服务能打开更多的瓶颈，它会使你的瓶颈更为难以理解。

其实依赖管理还有很多问题。本文探讨的是依赖管理部分的重要一点。基于实际情况做出何种选择都是可行的。选择好了之后，要“含泪保持微笑”地钻研。

---

Dependencies
Dependency management.
Nobody wants to think about it. We just want this stuff to work.
It is one of the nasty sneaky unsolved problems in software.

Each language system says, we've got a package manager and a build tool. This is how dependencies work. Some are better than others (I <3 Elm; npm OMG) but none of them are complete. We avert our eyes.

Dependencies are important. They're the edges in the software graph, and edges are always where the meaning lies. Edges are also harder to focus on than nodes.

They can be relatively explicit, declared in a pom.xml or package.json.
They can be hard to discover, like HTTP calls to URLs constructed from configuration + code + input.

Dependencies describe how we hook things together. Which means, they also determine our options for breaking things apart. And breaking things apart is how we scale a software system -- scale in our heads, that is; scale in terms of complexity, not volume.

If we look carefully at them, stop wishing they would stop being such a bother, maybe we can get this closer to right. There's a lot more to this topic than is covered in this post, but it's a start.

Libraries v Services

The biggest distinction. Definitions:

Libraries are compiled in. They're separate modules, in different repositories (or directories in a giant repository of doom (aka monorepo)). They are probably maintained by different companies or at least teams. Code re-use is achieved by compiling the same code into multiple applications (aka services). [I'm talking about compile-scope libraries here. Provided-scope, and things like .dll's (what is that even called) are another thing that should probably be a separate category in this post but isn't included.]

Services: one application calls another over the network (or sockets on the same machine); the code runs in different processes. There's some rigmarole in how to find each other: service discovery is totally a problem of its own, with DNS as the most common solution.

Tradeoffs

Visibility

Libraries are declared explicitly, although not always specifically. Something physically brings their code into my code, whether as a jar or as code explicitly.

Service dependencies are declared informally if at all. They may be discovered in logging. They may be discernible from security groups, if you're picky about which applications are allowed to access which other ones.

Deployment

Here's a crucial difference IMO. Libraries: you can release it and ask people to upgrade. If your library is internal, you may even upgrade the version in other teams' code. But it's the users of your library that decide when that new version goes into production. Your new code is upgraded when your users choose to deploy the upgraded code.

Services: You choose when it's upgraded. You deploy that new code, you turn off the old code, and that's it. Everyone who uses your service is using the new code. Bam. You have the power.
This also means you can choose how many of them are running at a time. This is the independent-scalability thing people get excited about.

If your library/service has data backing it, controlling code deployment means a lot for the format of the data. If your database is accessed only by your service, then you can any necessary translations into the code. If your database is accessed by a library that other people incorporate, you'd better keep that schema compatible.

Versioning

There's a lovely Rich Hickey talk, my notes here, about versioning libraries. Much of it also applies to services.

If you change the interface to a library, what you have is a different library. If you name it the same and call it a new version, then what you have is a different library that refuses to compile with the other one and will fight over what gets in. Then you get into the whole question of version conflicts, which different language systems resolve in different ways. Version conflicts occur when the application declares dependencies on two libraries, each of which declares a dependency on the same-name fourth library. In JavaScript, whatever, we can compile in both of them, it's just code copied in anyway. In Java, thou mayest have only one definition of each class name in a given ClassLoader, so the tools choose the newest version and hope everyone can cope.

Services, you can get complicated and do some sort of routing by version; you can run multiple versions of a service in production at the same time. See? You call it two versions of the same service, but it's actually two different services. Same as the libraries. Or, you can support multiple versions of the API within the same code. Backwards compatibility, it's all the pain for you and all the actual-working-software for your users.

API Changes and Backwards Compatibility

So you want to change the way users interact with your code. There's an important distinction here: changing your code (refactoring, bug fix, complete rewrite) is very different from requiring customers to change their code in order to change yours correctly. That's a serious impact.

Services: who uses it? Maybe it's an internal service and you have some hope of grepping all company code for your URL. You have the option of personally coordinating with those teams to change the usage of your service.
Or it's a public-facing service. DON'T CHANGE IT. You can never know who is using it. I mean maybe you don't care about your users, and you're OK with breaking their code. Sad day. Otherwise, you need permanent backwards-compatibility forever, and yes, your code will be ugly.

Libraries: if your package manager is respectable (meaning: immutable, if it ever provides a certain library-version is will continue to provide the same download forever), then your old versions are still around, they can stay in production. You can't take that code away. However, you can break any users who aren't ultra-specific about their version numbers. That's where semantic versioning comes in; it's rude to change the API in anything short of a major version, and people are supposed to be careful about picking up a new major version of your library.
But if you're nice you could name it something different, instead of pretending it's a different number of the same thing.

Isolation

A trick about libraries: it's way harder to know "what is an API change?"
With services it's clear; we recognize certain requests, and provide certain responses.
With libraries, there's all the public methods and public classes and packages and ... well, as a Java/Scala coder, I've never been especially careful about what I expose publicly. But library authors need to be if they're ever going to safely change anything inside the library.

Services are isolated: you can't depend on my internals because you physically can't access them. In order to expose anything to external use I have to make an explicit decision. This is much stronger modularity. It also means you can write them in different languages. That's a bonus.

There are a few companies that sell libraries. Those are some serious professionals, there. They have to test versions from way-back, on every OS they could run on. They have to be super aware of what is exposed, and test the new versions against a lot of scenarios. Services are a lot more practical to throw out there - even though backwards compatibility is a huge pain, at least you know where it is.

Failure

Libraries: it fails, your code fails. It runs out of memory, goodbye process. Failures are communicated synchronously, and if it fails, the app knows it.

Services: it fails, or it doesn't respond, you don't really know that it fails ... ouch. Partial failures, indeterminate failures, are way harder. Even on the same machine coordinating over a socket, we can't guarantee the response time or whether responses are delivered at all. This is all ouch, a major cost of using this modularization mechanism.

Conclusions

I think the biggest consideration in choosing whether to use libraries or services for distribution of effort / modularization is that choice of who decides when it deploys. Who controls which code is in production at a given time.

Libraries are more efficient and easier to handle failures. That's a thing. In-process communication is faster and failures are much easier to handle and consistency is possible.

Services are actual decoupling. They let a team be responsible for their own software, writing it and operating it. They let a team choose what is in production at a given time -- which means there's hope of ever changing data sources or schemas. Generally, I think the inertia present in data, data which has a lot of value, is underemphasized in discussion of software architecture. If you have a solid service interface guarding access to your data, you can (with a lot of painful work) move it into a different database or format. Without that, data migrations may be impossible.

Decoupling of time-of-deployment is essential for maintaining forward momentum as an organization grows from one team to many. Decoupling of features and of language systems, versions, tools helps too. To require everyone use the same tools (or heaven forbid, repository) is to couple every team to another in ways that are avoidable. I want my teams and applications coupled (integrated) in ways that streamline the customer's experience. I don't need them coupled in ways that streamline the development manager's experience.

Overall: libraries are faster until coordination is the bottleneck. Services add more openings to your bottle. That can make your bottle harder to understand.

There's a lot more to the problems of dependency management. This is one crucial distinction. All choices are valid, when made consciously in context. Try to focus through your tears.
