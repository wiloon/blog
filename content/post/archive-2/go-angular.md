---
title: angular basic
author: "-"
date: 2017-10-11T08:59:55+00:00
url: /?p=11249
categories:
  - inbox
tags:
  - reprint
---
## angular basic

## install angular

### install nodejs

@see nodejs basic

### install yarn

    http://blog.wiloon.com/?p=11228

# install angular cli

yarn global add @angular/cli
yarn add angular-in-memory-web-api --dev

ng config -g cli.packageManager yarn
add yarn global bin to $PATH

### angular command

# 创建工作区

ng new project0

# 创建组件

ng generate component heroes

# 创建组件 简写

ng g c heroes

ng generate component hero -it

# 创建service

ng generate service hero

ng serve --host 0.0.0.0 --port 4200 --open
ng build --aot
ng build --prod --build-optimizer

ng generate module app-routing --flat --module=app

# --flat 把这个文件放进了 src/app 中,而不是单独的目录中

# --module=app 告诉 CLI 把它注册到 AppModule 的 imports 数组中

<https://github.com/aralroca/helloworld-angular-with-golang>

### 修改angular编译输出目录

```bash
vim angular.json
...builder/outputPath
```

### 结构型指令

\*ngFor 是一个 "结构型指令"。结构型指令会通过添加、删除和操纵它们的宿主元素等方式塑造或重塑 DOM 的结构。任何带有 \* 的指令都是结构型指令。

#### 把 *ngFor 指令加到

<

div> 上, *ngFor 会导致

<

div> 被列表中的每个商品都重复渲染一次。

```xml

</div>
```

*ngIf

### 插值语法 {{}}

插值会把属性的值作为文本渲染出来。

### 绑定语法 []

```xml

```

插值表达式 {{}} 允许你把属性值渲染为文本；而属性绑定语法 [] 则允许你在模板表达式中使用属性值。

### 事件绑定

事件绑定是通过把事件名称包裹在圆括号 () 中完成的

```xml
<button (click)="share()">
```

### 双向数据绑定

[(ngModel)] 是 Angular 的双向数据绑定语法。

```xml
import { FormsModule } from '@angular/forms';
<input [(ngModel)]="hero.name" placeholder="name"/>
```

<https://zhuanlan.zhihu.com/p/27696268>
  
<https://medium.com/@anshap1719/getting-started-with-angular-and-go-setting-up-a-boilerplate-project-8c273b81aa6>
