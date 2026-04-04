---
title: "Tekton 与 Kaniko：云原生 CI/CD 构建实践"
author: "-"
date: 2026-03-25T10:06:15+08:00
url: tekton-kaniko
categories:
  - Cloud
  - Cloud
tags:
  - kaniko
  - tekton
  - CI/CD
  - k8s
  - remix
  - AI-assisted
---

## Tekton

### 什么是 Tekton

Tekton（发音：/ˈtɛktɒn/，"TEK-ton"）名称来自希腊语 τέκτων，意为"建造者"。

Tekton 是一个**开源的云原生 CI/CD 框架**，运行在 Kubernetes 上，通过 CRD（自定义资源定义）的方式定义流水线。它是**强制 Kubernetes 原生**的，所有流水线组件都以 Pod 方式运行，没有其他执行模式。

与 Jenkins、GitLab CI 等工具不同，Tekton 从设计之初就只能运行在 Kubernetes 上，而不是"可选支持 K8s"。这是架构层面的硬性约束，带来的好处是与 K8s 生态深度集成，代价是强依赖 K8s 环境。

Tekton 是 [CD Foundation](https://cd.foundation/) 旗下项目，前身是 Knative 的 Build 模块。

### 核心概念

#### Step（步骤）

流水线中的最小执行单元，对应容器中的一条命令。

#### Task（任务）

由一组有序的 Step 组成，运行在同一个 Pod 中，Steps 共享存储卷。

```yaml
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: build-and-push
spec:
  params:
    - name: image
      type: string
  steps:
    - name: build
      image: gcr.io/kaniko-project/executor:latest
      args:
        - "--dockerfile=$(workspaces.source.path)/Dockerfile"
        - "--context=$(workspaces.source.path)"
        - "--destination=$(params.image)"
  workspaces:
    - name: source
```

#### Pipeline（流水线）

由多个 Task 按顺序或并行组成，定义完整的 CI/CD 工作流。

```yaml
apiVersion: tekton.dev/v1
kind: Pipeline
metadata:
  name: ci-pipeline
spec:
  params:
    - name: repo-url
    - name: image
  workspaces:
    - name: shared-data
  tasks:
    - name: fetch-source
      taskRef:
        name: git-clone
      workspaces:
        - name: output
          workspace: shared-data
      params:
        - name: url
          value: $(params.repo-url)
    - name: build-push
      runAfter: ["fetch-source"]
      taskRef:
        name: build-and-push
      workspaces:
        - name: source
          workspace: shared-data
      params:
        - name: image
          value: $(params.image)
```

#### PipelineRun / TaskRun（运行实例）

触发 Pipeline 或 Task 实际执行的资源，每次运行对应一个实例。

```yaml
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: ci-pipeline-run-01
spec:
  pipelineRef:
    name: ci-pipeline
  params:
    - name: repo-url
      value: https://github.com/your-org/your-repo
    - name: image
      value: your-registry/your-image:latest
  workspaces:
    - name: shared-data
      volumeClaimTemplate:
        spec:
          accessModes: [ReadWriteOnce]
          resources:
            requests:
              storage: 1Gi
```

#### Workspace（工作区）

Task 和 Pipeline 之间共享数据的机制，底层可以是 PVC、ConfigMap、Secret 或 emptyDir。

### Tekton 组件

| 组件 | 说明 |
|------|------|
| Tekton Pipelines | 核心组件，提供 Task/Pipeline CRD |
| Tekton Triggers | 监听外部事件（如 Git Push）自动触发流水线 |
| Tekton Dashboard | Web UI，查看流水线运行状态 |
| Tekton Catalog | 官方维护的可复用 Task 库 |
| Tekton Chains | 供应链安全，对构建产物进行签名 |

### 安装 Tekton

```shell
# 安装 Tekton Pipelines
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml

# 安装 Tekton Dashboard（可选）
kubectl apply --filename https://storage.googleapis.com/tekton-releases/dashboard/latest/release.yaml
```

### Tekton Triggers：事件驱动

通过 EventListener、TriggerTemplate、TriggerBinding 实现 Git Push 自动触发流水线：

```
Git Push → Webhook → EventListener → TriggerBinding → TriggerTemplate → PipelineRun
```

---

## Kaniko

### 什么是 Kaniko

Kaniko 是 Google 开源的一个工具，用于**在容器或 Kubernetes 集群内无需 Docker daemon 即可构建容器镜像**。

传统的 Docker 构建需要在宿主机上运行有特权的 Docker daemon。在 Kubernetes 中这会带来安全隐患（需要 `privileged` 权限或挂载 Docker socket），而 Kaniko 完全在用户空间运行，不依赖 Docker daemon，安全性更高。

### Kaniko 的工作原理

Kaniko 以容器方式运行，读取 Dockerfile，在用户空间逐层执行每条指令，最终将镜像推送到指定的镜像仓库。

```
Dockerfile → Kaniko executor → 镜像仓库 (Docker Hub / ECR / GCR / Harbor...)
```

核心流程：

1. 解析 Dockerfile
1. 在用户空间逐条执行 `RUN`、`COPY`、`ADD` 等指令
1. 每条指令执行后生成一个文件系统快照（layer）
1. 将所有层打包成镜像并推送到仓库

### Kaniko 的典型用法

在 Kubernetes 中以 Pod 方式运行：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kaniko-build
spec:
  containers:
    - name: kaniko
      image: gcr.io/kaniko-project/executor:latest
      args:
        - "--dockerfile=Dockerfile"
        - "--context=git://github.com/your-org/your-repo"
        - "--destination=your-registry/your-image:tag"
      volumeMounts:
        - name: kaniko-secret
          mountPath: /kaniko/.docker
  volumes:
    - name: kaniko-secret
      secret:
        secretName: regcred
        items:
          - key: .dockerconfigjson
            path: config.json
  restartPolicy: Never
```

### Kaniko 的优势

| 特性 | Docker-in-Docker (DinD) | Kaniko |
|------|------------------------|--------|
| 是否需要特权容器 | 是 | 否 |
| 安全性 | 低 | 高 |
| 层缓存支持 | 是 | 是（需配置） |
| Kubernetes 原生 | 否 | 是 |

### 层缓存

Kaniko 支持通过 `--cache` 和 `--cache-repo` 参数启用层缓存，将缓存层推送到镜像仓库，加快后续构建速度：

```shell
--cache=true
--cache-repo=your-registry/your-image/cache
```

---

## Tekton + Kaniko 组合实践

两者结合是 Kubernetes 原生 CI/CD 的主流方案：

- **Tekton** 负责编排整个流水线（拉代码、构建、测试、部署）
- **Kaniko** 作为 Tekton Task 中的构建步骤，无特权构建容器镜像

`Tekton Catalog` 中已有官方维护的 `kaniko` Task，可直接复用：

```shell
tkn hub install task kaniko
```

### 完整流程示意

```
开发者 git push
    ↓
Tekton Trigger (EventListener)
    ↓
PipelineRun 创建
    ↓
Task: git-clone        → 拉取源码到 Workspace
Task: kaniko (build)   → 构建并推送镜像（无需 Docker daemon）
Task: kubectl-deploy   → 更新 Deployment 镜像版本
```

---

## 对比其他方案

### CI/CD 工具执行单元对比

不同 CI/CD 工具对 Kubernetes 的依赖程度差异很大：

| 工具 | 主要执行单元 | K8s 支持方式 |
|------|------------|-------------|
| **Tekton** | Pod（强制） | 只能运行在 K8s 上 |
| **Argo Workflows** | Pod（强制） | 只能运行在 K8s 上 |
| **Jenkins** | JVM 进程 / Agent 节点 | 可选（需装 Kubernetes 插件） |
| **GitLab CI** | Runner 进程 | 可选（Kubernetes executor） |
| **GitHub Actions** | VM runner | 可选（self-hosted + K8s） |
| **CircleCI** | Docker 容器 / VM | 不直接运行在 K8s Pod 上 |
| **Drone CI** | Docker 容器 | 可选（K8s runner） |

Tekton 和 Argo Workflows 是**强制 K8s 原生**的代表；Jenkins、GitLab CI 等传统工具则是**可选支持 K8s**，本质上不依赖 K8s。

### 方案综合对比

| 方案 | 是否 K8s 原生 | 需要特权 | 适合规模 |
|------|:---:|:---:|------|
| Jenkins + DinD | 否 | 是 | 中小型 |
| GitLab CI | 否 | 可选 | 中大型 |
| Tekton + Kaniko | 是 | 否 | 中大型 |
| Argo Workflows | 是 | 可选 | 大型 |

Tekton + Kaniko 是在纯 Kubernetes 环境中实现安全、可扩展 CI/CD 的推荐组合。
