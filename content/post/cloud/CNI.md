---
title: CNI
author: "-"
date: 2012-09-26T02:12:55+00:00
url: cni
categories:
  - Network

---
## CNI

常见的 CNI 插件包括 Calico、flannel、Terway、Weave Net 以及 Contiv。

在对CNI插件们进行比较之前，我们可以先对网络中会见到的相关术语做一个整体的了解。不论是阅读本文，还是今后接触到其他和CNI有关的内容，了解一些常见术语总是非常有用的。

一些最常见的术语包括：

第2层网络： OSI（Open Systems Interconnections，开放系统互连）网络模型的“数据链路”层。第2层网络会处理网络上两个相邻节点之间的帧传递。第2层网络的一个值得注意的示例是以太网，其中MAC表示为子层。
第3层网络： OSI网络模型的“网络”层。第3层网络的主要关注点，是在第2层连接之上的主机之间路由数据包。IPv4、IPv6和ICMP是第3层网络协议的示例。
VXLAN：代表“虚拟可扩展LAN”。首先，VXLAN用于通过在UDP数据报中封装第2层以太网帧来帮助实现大型云部署。VXLAN虚拟化与VLAN类似，但提供更大的灵活性和功能（VLAN仅限于4096个网络ID）。VXLAN是一种封装和覆盖协议，可在现有网络上运行。
Overlay网络：Overlay网络是建立在现有网络之上的虚拟逻辑网络。Overlay网络通常用于在现有网络之上提供有用的抽象，并分离和保护不同的逻辑网络。
封装：封装是指在附加层中封装网络数据包以提供其他上下文和信息的过程。在overlay网络中，封装被用于从虚拟网络转换到底层地址空间，从而能路由到不同的位置（数据包可以被解封装，并继续到其目的地）。
网状网络：网状网络（Mesh network）是指每个节点连接到许多其他节点以协作路由、并实现更大连接的网络。网状网络允许通过多个路径进行路由，从而提供更可靠的网络。网状网格的缺点是每个附加节点都会增加大量开销。
BGP：代表“边界网关协议”，用于管理边缘路由器之间数据包的路由方式。BGP通过考虑可用路径，路由规则和特定网络策略，帮助弄清楚如何将数据包从一个网络发送到另一个网络。BGP有时被用作CNI插件中的路由机制，而不是封装的覆盖网络。



CNI比较

Flannel

链接：https://github.com/coreos/fla...

由CoreOS开发的项目Flannel，可能是最直接和最受欢迎的CNI插件。它是容器编排系统中最成熟的网络结构示例之一，旨在实现更好的容器间和主机间网络。随着CNI概念的兴起，Flannel CNI插件算是早期的入门。

与其他方案相比，Flannel相对容易安装和配置。它被打包为单个二进制文件flanneld，许多常见的Kubernetes集群部署工具和许多Kubernetes发行版都可以默认安装Flannel。Flannel可以使用Kubernetes集群的现有etcd集群来使用API存储其状态信息，因此不需要专用的数据存储。

Flannel配置第3层IPv4 overlay网络。它会创建一个大型内部网络，跨越集群中每个节点。在此overlay网络中，每个节点都有一个子网，用于在内部分配IP地址。在配置pod时，每个节点上的Docker桥接口都会为每个新容器分配一个地址。同一主机中的Pod可以使用Docker桥接进行通信，而不同主机上的pod会使用flanneld将其流量封装在UDP数据包中，以便路由到适当的目标。

Flannel有几种不同类型的后端可用于封装和路由。默认和推荐的方法是使用VXLAN，因为VXLAN性能更良好并且需要的手动干预更少。

总的来说，Flannel是大多数用户的不错选择。从管理角度来看，它提供了一个简单的网络模型，用户只需要一些基础知识，就可以设置适合大多数用例的环境。一般来说，在初期使用Flannel是一个稳妥安全的选择，直到你开始需要一些它无法提供的东西。

Calico

链接：https://github.com/projectcal...

Calico是Kubernetes生态系统中另一种流行的网络选择。虽然Flannel被公认为是最简单的选择，但Calico以其性能、灵活性而闻名。Calico的功能更为全面，不仅提供主机和pod之间的网络连接，还涉及网络安全和管理。Calico CNI插件在CNI框架内封装了Calico的功能。

在满足系统要求的新配置的Kubernetes集群上，用户可以通过应用单个manifest文件快速部署Calico。如果您对Calico的可选网络策略功能感兴趣，可以向集群应用其他manifest，来启用这些功能。

尽管部署Calico所需的操作看起来相当简单，但它创建的网络环境同时具有简单和复杂的属性。与Flannel不同，Calico不使用overlay网络。相反，Calico配置第3层网络，该网络使用BGP路由协议在主机之间路由数据包。这意味着在主机之间移动时，不需要将数据包包装在额外的封装层中。BGP路由机制可以本地引导数据包，而无需额外在流量层中打包流量。

除了性能优势之外，在出现网络问题时，用户还可以用更常规的方法进行故障排除。虽然使用VXLAN等技术进行封装也是一个不错的解决方案，但该过程处理数据包的方式同场难以追踪。使用Calico，标准调试工具可以访问与简单环境中相同的信息，从而使更多开发人员和管理员更容易理解行为。

除了网络连接外，Calico还以其先进的网络功能而闻名。 网络策略是其最受追捧的功能之一。此外，Calico还可以与服务网格Istio集成，以便在服务网格层和网络基础架构层中解释和实施集群内工作负载的策略。这意味着用户可以配置强大的规则，描述pod应如何发送和接受流量，提高安全性并控制网络环境。

如果对你的环境而言，支持网络策略是非常重要的一点，而且你对其他性能和功能也有需求，那么Calico会是一个理想的选择。此外，如果您现在或未来有可能希望得到技术支持，那么Calico是提供商业支持的。一般来说，当您希望能够长期控制网络，而不是仅仅配置一次并忘记它时，Calico是一个很好的选择。


