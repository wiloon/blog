---
title: service mesh
author: "-"
date: 2016-10-10T04:39:13+00:00
url: service-mesh
categories:
  - cloud

tags:
  - reprint
---
## service mesh
### 微服务

>wiloon.com/microservice

### service mesh

下一代微服务架构
Service Mesh (服务网格) 被认为是下一代微服务架构,Service Mesh并没有给我们带来新的功能,它是用于解决其他工具已经解决过的服务网络调用、限流、熔断和监控等问题, 只不过这次是在 Cloud Native 的 kubernetes 环境下的实现。

Willian Morgan 对 Service Mesh 的解释。

A Service Mesh is a dedicated infrastructure layer for handling service-to-service communication. It’s responsible for the reliable delivery of requests through the complex topology of services that comprise a modern, cloud native application. In practice, the Service Mesh is typically implemented as an array of lightweight network proxies that are deployed alongside application code, without the application needing to be aware.

服务网格 (Service Mesh）是处理服务间通信的基础设施层。它负责在现代的云原生应用的复杂的服务拓补中可靠的交付请求。在实践中，Service Mesh 通常以轻量级网络代理阵列的形式实现，这些代理与应用程序代码部署在一起，应用程序无需感知代理的存在。


Service Mesh 有如下几个特点：

应用程序间通信的中间层
轻量级网络代理
应用程序无感知
解耦应用程序的重试/超时、监控、追踪和服务发现
目前两款流行的 Service Mesh 开源软件 Istio 和 Linkerd 都可以直接在 Kubernetes 中集成，


Phil Calçado 在他的这篇博客 Pattern: Service Mesh 中详细解释了 Service Mesh 的来龙去脉：

从最原始的主机之间直接使用网线相连
网络层的出现
集成到应用程序内部的控制流
分解到应用程序外部的控制流
应用程序的中集成服务发现和断路器
出现了专门用于服务发现和断路器的软件包/库，如 Twitter 的 Finagle 和 Facebook 的 Proxygen，这时候还是集成在应用程序内部
出现了专门用于服务发现和断路器的开源软件，如 Netflix OSS、Airbnb 的 synapse 和 nerve
最后作为微服务的中间层 Service Mesh 出现


Service Mesh如何工作？
下面以 Istio 为例讲解 Service Mesh 如何工作，后续文章将会详解 Istio 如何在 Kubernetes 中工作。

Sidecar (Istio 中使用 Envoy 作为 sidecar 代理）将服务请求路由到目的地址，根据请求中的参数判断是到生产环境、测试环境还是 staging 环境中的服务 (服务可能同时部署在这三个环境中），是路由到本地环境还是公有云环境？所有的这些路由信息可以动态配置，可以是全局配置也可以为某些服务单独配置。这些配置是由服务网格的控制平面推送给各个 sidecar 的，
当 sidecar 确认了目的地址后，将流量发送到相应服务发现端点，在 Kubernetes 中是 service，然后 service 会将服务转发给后端的实例。
Sidecar 根据它观测到最近请求的延迟时间，选择出所有应用程序的实例中响应最快的实例。
Sidecar 将请求发送给该实例，同时记录响应类型和延迟数据。
如果该实例挂了、不响应了或者进程不工作了，sidecar 会将把请求发送到其他实例上重试。
如果该实例持续返回 error，sidecar 会将该实例从负载均衡池中移除，稍后再周期性得重试。
如果请求的截止时间已过，sidecar 主动标记该请求为失败，而不是再次尝试添加负载。
SIdecar 以 metric 和分布式追踪的形式捕获上述行为的各个方面，这些追踪信息将发送到集中 metric 系统。

<https://jimmysong.io/blog/what-is-a-service-mesh/>  
<https://buoyant.io/what-is-a-service-mesh/>  
<https://philcalcado.com/2017/08/03/pattern_service_mesh.html>


## Istio, Service Mesh
service mesh是微服务时代的TCP协议

Istio是由Google/IBM/Lyft共同开发的新一代Service Mesh开源项目

容错: 当请求失败和重试的时候,使用它能够理解的响应状态码；
  
金丝雀发布: 只将特定百分比的请求转发到服务的新版本上；
  
监控和指标: 统计服务响应所耗费的时间；
  
跟踪和可观察性: 它在每个请求上添加了一个特殊的头部信息,并在集群中跟踪它们；
  
安全性: 抽取 JWT Token 并对用户进行认证和授权。

控制平面由三个组件组成: Pilot、Mixer 和 Citadel,它们组合配置 Envoy 以便于路由流量、执行策略和收集遥测数据。

[http://www.infoq.com/cn/articles/istio-future-service-mesh?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global][1]
  
<https://servicemesh.gitbooks.io/awesome-servicemesh/mesh/2017/service-mesh-next-generation-of-microservice/>

 [1]: http://www.infoq.com/cn/articles/istio-future-service-mesh?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global


https://cloudnative.to/sig-istio/big-talk/overview.html
>https://jimmysong.io/blog/envoy-sidecar-injection-in-istio-service-mesh-deep-dive/

### service mesh 2021
>https://jimmysong.io/blog/service-mesh-2021/

### dapr
>https://www.zhihu.com/question/351298264

### ebpf
>https://cloudnative.to/blog/ebpf-solve-service-mesh-sidecar/

### k8s, istio, Cilium, dapr


### k8s install istio

## install istio

```bash
# 在 k8s master 执行
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.12.2
export PATH=$PWD/bin:$PATH

# 在 worker 节点执行 
crictl pull docker.io/istio/pilot:1.12.2
crictl pull docker.io/istio/proxyv2:1.12.2

# 在 k8s master 执行
istioctl install --set profile=demo -y
istioctl verify-install

kubectl get pods -n istio-system 
kubectl describe pod istiod-5bcb74c764-n52gh -n istio-system
```